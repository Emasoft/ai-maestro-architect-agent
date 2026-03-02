#!/usr/bin/env python3
"""Universal Health Audit Framework for Project Quality Checks.

WHY: Orchestrators need a consistent way to verify project health before delegating tasks.
WHY: Pluggable architecture allows adding custom checks without modifying core logic.
WHY: Severity levels enable filtering and prioritization of issues.
"""

import argparse
import json
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import atomic_write_json, run_command  # type: ignore[import-not-found]  # noqa: E402
from thresholds import TIMEOUTS  # type: ignore[import-not-found]  # noqa: E402


class Severity(Enum):
    """Severity levels for health check results.

    WHY: Enables filtering and prioritization of issues.
    WHY: CRITICAL issues should block deployment, WARNING should be reviewed, INFO is advisory.
    """

    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"

    @classmethod
    def from_string(cls, value: str) -> "Severity":
        """Convert string to Severity enum, case-insensitive."""
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(
                f"Invalid severity: {value}. Must be one of: {', '.join(s.name for s in cls)}"
            )

    def __ge__(self, other: "Severity") -> bool:
        """Enable severity comparison for filtering."""
        severity_order = {Severity.INFO: 0, Severity.WARNING: 1, Severity.CRITICAL: 2}
        return severity_order[self] >= severity_order[other]


@dataclass
class CheckResult:
    """Result of a single health check.

    WHY: Standardized structure makes results easy to parse, aggregate, and report.
    """

    name: str
    passed: bool
    severity: Severity
    message: str
    fix_hint: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "name": self.name,
            "passed": self.passed,
            "severity": self.severity.value,
            "message": self.message,
            "fix_hint": self.fix_hint,
            "details": self.details,
        }


class HealthCheck(ABC):
    """Base class for all health checks.

    WHY: Abstract base enforces consistent interface across all check types.
    WHY: Subclasses only need to implement check logic, not result formatting.
    """

    def __init__(self, project_path: Path, verbose: bool = False):
        """Initialize health check with project path.

        WHY: All checks need project context to operate.
        WHY: Verbose mode helps debug check failures.
        """
        self.project_path = project_path
        self.verbose = verbose

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this check."""
        pass

    @abstractmethod
    def run(self) -> CheckResult:
        """Execute the health check and return result.

        WHY: Each check implements its own validation logic.
        """
        pass

    def _run_command(
        self, cmd: list[str], cwd: Path | None = None
    ) -> tuple[int, str, str]:
        """Run shell command and return exit code, stdout, stderr.

        WHY: Many checks need to run external commands (git, test runners).
        WHY: Centralized command execution ensures consistent error handling.
        WHY: Uses TIMEOUTS.COMMAND for consistent timeout behavior across all scripts.
        """
        if cwd is None:
            cwd = self.project_path

        try:
            result: tuple[int, str, str] = run_command(
                cmd, cwd=cwd, timeout=TIMEOUTS.COMMAND
            )
            return result
        except TimeoutError as e:
            return -1, "", str(e)
        except Exception as e:
            return -1, "", f"Command failed: {e}"


class GitCheck(HealthCheck):
    """Verify git repository health.

    WHY: Git status affects safe delegation - can't commit if repo is dirty.
    WHY: Missing .git means version control tracking is broken.
    """

    @property
    def name(self) -> str:
        return "git"

    def run(self) -> CheckResult:
        """Check git repository exists and is clean."""
        git_dir = self.project_path / ".git"

        # Check if .git exists
        if not git_dir.exists():
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.CRITICAL,
                message=f"No git repository found at {self.project_path}",
                fix_hint="Run: git init",
                details={"git_dir": str(git_dir), "exists": False},
            )

        # Check git status
        returncode, stdout, stderr = self._run_command(["git", "status", "--porcelain"])

        if returncode != 0:
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.CRITICAL,
                message=f"Git command failed: {stderr}",
                fix_hint="Check git installation and repository integrity",
                details={"error": stderr},
            )

        # WHY: Empty stdout means clean working tree
        is_clean = len(stdout.strip()) == 0
        uncommitted_files = stdout.strip().split("\n") if not is_clean else []

        if not is_clean:
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.WARNING,
                message=f"Git repository has {len(uncommitted_files)} uncommitted changes",
                fix_hint="Run: git status to review changes, then git add/commit",
                details={
                    "uncommitted_count": len(uncommitted_files),
                    "files": uncommitted_files[:10],
                },
            )

        return CheckResult(
            name=self.name,
            passed=True,
            severity=Severity.INFO,
            message="Git repository is clean",
            fix_hint="",
            details={"clean": True},
        )


class DepsCheck(HealthCheck):
    """Verify dependency management files exist.

    WHY: Missing dependency files means project can't be reproduced.
    WHY: Lockfiles ensure deterministic builds.
    """

    @property
    def name(self) -> str:
        return "deps"

    def run(self) -> CheckResult:
        """Check for dependency and lockfile presence."""
        # WHY: Different ecosystems use different files
        dep_files = {
            "python": ["pyproject.toml", "requirements.txt", "setup.py"],
            "node": ["package.json"],
            "rust": ["Cargo.toml"],
        }

        lock_files = {
            "python": ["uv.lock", "poetry.lock", "Pipfile.lock"],
            "node": ["package-lock.json", "yarn.lock", "pnpm-lock.yaml"],
            "rust": ["Cargo.lock"],
        }

        found_deps = []
        found_locks = []

        # Check for any dependency file
        for ecosystem, files in dep_files.items():
            for filename in files:
                if (self.project_path / filename).exists():
                    found_deps.append((ecosystem, filename))

        # Check for lockfiles
        for ecosystem, files in lock_files.items():
            for filename in files:
                if (self.project_path / filename).exists():
                    found_locks.append((ecosystem, filename))

        if not found_deps:
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.CRITICAL,
                message="No dependency files found (pyproject.toml, package.json, Cargo.toml, etc.)",
                fix_hint="Create appropriate dependency file for your project type",
                details={"found_deps": [], "found_locks": []},
            )

        if not found_locks:
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.WARNING,
                message=f"Dependency files found but no lockfiles: {[f for _, f in found_deps]}",
                fix_hint="Generate lockfile with: uv lock / npm install / cargo build",
                details={"found_deps": [f for _, f in found_deps], "found_locks": []},
            )

        return CheckResult(
            name=self.name,
            passed=True,
            severity=Severity.INFO,
            message=f"Dependencies managed: {[f for _, f in found_deps]} with locks: {[f for _, f in found_locks]}",
            fix_hint="",
            details={
                "found_deps": [f for _, f in found_deps],
                "found_locks": [f for _, f in found_locks],
            },
        )


class TestsCheck(HealthCheck):
    """Verify test infrastructure exists.

    WHY: Projects without tests can't verify correctness before deployment.
    WHY: Empty test directories indicate incomplete testing setup.
    """

    @property
    def name(self) -> str:
        return "tests"

    def run(self) -> CheckResult:
        """Check for test directory and test files."""
        # WHY: Common test directory patterns
        test_dirs = ["tests", "test", "__tests__", "spec"]

        found_dirs = [d for d in test_dirs if (self.project_path / d).is_dir()]

        if not found_dirs:
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.CRITICAL,
                message="No test directory found (tests/, test/, __tests__/, spec/)",
                fix_hint="Create tests/ directory and add test files",
                details={"found_dirs": [], "test_file_count": 0},
            )

        # Count test files
        test_files: list[Path] = []
        for test_dir in found_dirs:
            test_path = self.project_path / test_dir
            # WHY: Common test file patterns
            patterns = [
                "test_*.py",
                "*_test.py",
                "test*.js",
                "*.test.js",
                "*.test.ts",
                "*_spec.rb",
                "test_*.rs",
            ]
            for pattern in patterns:
                test_files.extend(test_path.rglob(pattern))

        test_file_count = len(test_files)

        if test_file_count == 0:
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.WARNING,
                message=f"Test directory exists ({found_dirs}) but no test files found",
                fix_hint="Add test files matching pattern: test_*.py, *.test.js, etc.",
                details={"found_dirs": found_dirs, "test_file_count": 0},
            )

        return CheckResult(
            name=self.name,
            passed=True,
            severity=Severity.INFO,
            message=f"Found {test_file_count} test files in {found_dirs}",
            fix_hint="",
            details={"found_dirs": found_dirs, "test_file_count": test_file_count},
        )


class DocsCheck(HealthCheck):
    """Verify documentation files exist.

    WHY: Projects need README for onboarding and CLAUDE.md for AI context.
    WHY: Missing docs makes delegation harder - agents need project context.
    """

    @property
    def name(self) -> str:
        return "docs"

    def run(self) -> CheckResult:
        """Check for essential documentation files."""
        readme_exists = (self.project_path / "README.md").exists()
        claude_md_exists = (self.project_path / "CLAUDE.md").exists()

        missing = []
        if not readme_exists:
            missing.append("README.md")
        if not claude_md_exists:
            missing.append("CLAUDE.md")

        if missing:
            severity = Severity.CRITICAL if "README.md" in missing else Severity.WARNING
            return CheckResult(
                name=self.name,
                passed=False,
                severity=severity,
                message=f"Missing documentation files: {', '.join(missing)}",
                fix_hint=f"Create {' and '.join(missing)} with project overview and context",
                details={
                    "readme_exists": readme_exists,
                    "claude_md_exists": claude_md_exists,
                },
            )

        return CheckResult(
            name=self.name,
            passed=True,
            severity=Severity.INFO,
            message="Documentation files present (README.md, CLAUDE.md)",
            fix_hint="",
            details={
                "readme_exists": readme_exists,
                "claude_md_exists": claude_md_exists,
            },
        )


class CICheck(HealthCheck):
    """Verify CI/CD configuration exists.

    WHY: GitHub Actions ensures automated testing on push.
    WHY: Missing CI means manual testing only - error-prone.
    """

    @property
    def name(self) -> str:
        return "ci"

    def run(self) -> CheckResult:
        """Check for GitHub Actions workflows."""
        workflows_dir = self.project_path / ".github" / "workflows"

        if not workflows_dir.exists():
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.WARNING,
                message="No .github/workflows directory found",
                fix_hint="Create .github/workflows/ and add CI workflow YAML",
                details={"workflows_dir_exists": False, "workflow_count": 0},
            )

        # Count workflow files
        workflow_files = list(workflows_dir.glob("*.yml")) + list(
            workflows_dir.glob("*.yaml")
        )
        workflow_count = len(workflow_files)

        if workflow_count == 0:
            return CheckResult(
                name=self.name,
                passed=False,
                severity=Severity.WARNING,
                message=".github/workflows exists but no workflow files found",
                fix_hint="Add workflow YAML files to .github/workflows/",
                details={"workflows_dir_exists": True, "workflow_count": 0},
            )

        return CheckResult(
            name=self.name,
            passed=True,
            severity=Severity.INFO,
            message=f"Found {workflow_count} GitHub Actions workflow(s)",
            fix_hint="",
            details={"workflows_dir_exists": True, "workflow_count": workflow_count},
        )


class HealthAuditor:
    """Orchestrates health checks and generates aggregate reports.

    WHY: Provides unified interface for running multiple checks.
    WHY: Aggregates results for easy interpretation and JSON export.
    """

    # WHY: Registry enables dynamic check selection via CLI
    AVAILABLE_CHECKS = {
        "git": GitCheck,
        "deps": DepsCheck,
        "tests": TestsCheck,
        "docs": DocsCheck,
        "ci": CICheck,
    }

    def __init__(self, project_path: Path, verbose: bool = False):
        """Initialize auditor with project path.

        WHY: Project path is needed by all checks.
        """
        self.project_path = project_path.resolve()
        self.verbose = verbose
        self.results: list[CheckResult] = []

    def run_checks(
        self, check_names: list[str] | None = None, min_severity: Severity | None = None
    ) -> list[CheckResult]:
        """Run specified checks and return results.

        WHY: Allows selective check execution and severity filtering.
        """
        if check_names is None:
            check_names = list(self.AVAILABLE_CHECKS.keys())

        # Validate check names
        invalid_checks = set(check_names) - set(self.AVAILABLE_CHECKS.keys())
        if invalid_checks:
            available = ", ".join(self.AVAILABLE_CHECKS.keys())
            raise ValueError(
                f"Invalid check names: {invalid_checks}. Available: {available}"
            )

        self.results = []

        for check_name in check_names:
            check_class = self.AVAILABLE_CHECKS[check_name]
            # NOTE: mypy sees abstract HealthCheck but all entries are concrete subclasses
            check = check_class(self.project_path, verbose=self.verbose)  # type: ignore[abstract]

            if self.verbose:
                print(f"Running check: {check_name}...", file=sys.stderr)

            result = check.run()

            # WHY: Filter by severity if specified
            if min_severity is None or result.severity >= min_severity:
                self.results.append(result)

        return self.results

    def generate_report(self) -> dict[str, Any]:
        """Generate aggregate report from check results.

        WHY: Provides overview statistics for quick health assessment.
        """
        passed_count = sum(1 for r in self.results if r.passed)
        failed_count = len(self.results) - passed_count

        # WHY: Group failures by severity for prioritization
        failed_by_severity = {
            "CRITICAL": [
                r
                for r in self.results
                if not r.passed and r.severity == Severity.CRITICAL
            ],
            "WARNING": [
                r
                for r in self.results
                if not r.passed and r.severity == Severity.WARNING
            ],
            "INFO": [
                r for r in self.results if not r.passed and r.severity == Severity.INFO
            ],
        }

        return {
            "project_path": str(self.project_path),
            "total_checks": len(self.results),
            "passed": passed_count,
            "failed": failed_count,
            "failed_by_severity": {
                "CRITICAL": len(failed_by_severity["CRITICAL"]),
                "WARNING": len(failed_by_severity["WARNING"]),
                "INFO": len(failed_by_severity["INFO"]),
            },
            "checks": [r.to_dict() for r in self.results],
        }


def main() -> None:
    """CLI entry point for health auditor.

    WHY: Provides command-line interface for scripting and CI integration.
    """
    parser = argparse.ArgumentParser(
        description="Universal Health Audit Framework for Project Quality Checks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --path ./project --checks git,deps,tests
  %(prog)s --path . --severity WARNING --output health.json
  %(prog)s --path ~/myproject --verbose
        """,
    )

    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Project directory to audit (default: current directory)",
    )

    parser.add_argument(
        "--checks",
        type=str,
        help=f"Comma-separated check names (default: all). Available: {', '.join(HealthAuditor.AVAILABLE_CHECKS.keys())}",
    )

    parser.add_argument(
        "--severity",
        type=str,
        help="Minimum severity level to report (CRITICAL, WARNING, INFO)",
    )

    parser.add_argument(
        "--output", type=Path, help="Write JSON report to file instead of stdout"
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Parse check names
    check_names = None
    if args.checks:
        check_names = [c.strip() for c in args.checks.split(",")]

    # Parse severity
    min_severity = None
    if args.severity:
        try:
            min_severity = Severity.from_string(args.severity)
        except ValueError as e:
            parser.error(str(e))

    # Validate project path
    if not args.path.exists():
        parser.error(f"Project path does not exist: {args.path}")

    if not args.path.is_dir():
        parser.error(f"Project path is not a directory: {args.path}")

    # Run audit
    auditor = HealthAuditor(args.path, verbose=args.verbose)

    try:
        auditor.run_checks(check_names=check_names, min_severity=min_severity)
    except ValueError as e:
        parser.error(str(e))

    report = auditor.generate_report()

    # Output report
    if args.output:
        atomic_write_json(args.output, report)
        if args.verbose:
            print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(json.dumps(report, indent=2))

    # WHY: Exit with non-zero if any checks failed
    sys.exit(0 if report["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
