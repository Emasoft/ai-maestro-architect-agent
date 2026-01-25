#!/usr/bin/env python3
"""
Project Type Detection and Capability Inference Engine

WHY: Orchestrators need to understand what kind of project they're working with
to make intelligent decisions about tooling, testing strategies, and build processes.
This script uses pattern-matching to detect project types and infer available capabilities.

WHY Class-based: Encapsulates detection logic and state, making it easier to extend
with new project types and capability inference rules.

WHY JSON output: Structured data can be consumed by other tools, scripts, and orchestration
systems without parsing text output.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Any

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import atomic_write_json  # type: ignore[import-not-found]  # noqa: E402


class ProjectDetector:
    """
    Detects project types and infers capabilities based on file patterns.

    WHY: Centralized detection logic that can be easily extended with new project types.
    The detector supports multi-language projects and monorepos.
    """

    # WHY: File patterns are the most reliable indicators of project type
    # These patterns are checked in the project directory to determine what kind of project it is
    PROJECT_PATTERNS = {
        "python": [
            "pyproject.toml",
            "setup.py",
            "setup.cfg",
            "requirements.txt",
            "Pipfile",
            "poetry.lock",
            "uv.lock",
        ],
        "nodejs": [
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
        ],
        "rust": [
            "Cargo.toml",
            "Cargo.lock",
        ],
        "go": [
            "go.mod",
            "go.sum",
        ],
        "swift": [
            "Package.swift",
            "Package.resolved",
        ],
        "cmake": [
            "CMakeLists.txt",
        ],
        "java": [
            "pom.xml",
            "build.gradle",
            "build.gradle.kts",
        ],
        "dotnet": [
            "*.csproj",
            "*.fsproj",
            "*.vbproj",
            "*.sln",
        ],
    }

    # WHY: Subtypes help distinguish between libraries, applications, and other variants
    # This affects what commands and workflows are available
    SUBTYPE_PATTERNS = {
        "python": {
            "library": ["src/", "pyproject.toml"],
            "application": ["main.py", "app.py", "__main__.py"],
            "django": ["manage.py", "settings.py"],
            "flask": ["app.py", "wsgi.py"],
            "fastapi": ["main.py"],  # WHY: Often combined with uvicorn in dependencies
        },
        "nodejs": {
            "library": [],  # WHY: Detected by "main" field in package.json
            "application": [],  # WHY: Detected by "bin" or "scripts.start" in package.json
            "react": ["src/App.jsx", "src/App.tsx", "public/index.html"],
            "nextjs": ["next.config.js", "next.config.mjs", "pages/", "app/"],
            "express": [],  # WHY: Detected from dependencies in package.json
        },
    }

    def __init__(self, project_path: Path, verbose: bool = False):
        """
        Initialize the detector with a project path.

        WHY: Store state (path, verbose flag) for use across multiple detection methods.
        """
        self.project_path = project_path
        self.verbose = verbose
        self.detected_types: Set[str] = set()
        self.detected_subtypes: Dict[str, List[str]] = {}
        self.capabilities: Dict[str, Any] = {}

    def log(self, message: str) -> None:
        """Print verbose logging messages."""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)

    def detect_project_types(self) -> Set[str]:
        """
        Detect all project types present in the directory.

        WHY: A directory can contain multiple project types (polyglot/monorepo).
        Returns all detected types instead of just the first match.
        """
        detected = set()

        for project_type, patterns in self.PROJECT_PATTERNS.items():
            for pattern in patterns:
                # WHY: Use glob to support wildcard patterns like *.csproj
                if "*" in pattern:
                    matches = list(self.project_path.glob(pattern))
                    if matches:
                        self.log(
                            f"Found {project_type} via pattern '{pattern}': {matches[0].name}"
                        )
                        detected.add(project_type)
                        break
                else:
                    file_path = self.project_path / pattern
                    if file_path.exists():
                        self.log(f"Found {project_type} via file '{pattern}'")
                        detected.add(project_type)
                        break

        self.detected_types = detected
        return detected

    def detect_subtypes(self, project_type: str) -> List[str]:
        """
        Detect subtypes for a specific project type.

        WHY: Subtypes determine specific tooling and workflows (e.g., Django vs Flask).
        """
        subtypes: List[str] = []

        if project_type not in self.SUBTYPE_PATTERNS:
            return subtypes

        patterns = self.SUBTYPE_PATTERNS[project_type]

        for subtype, indicators in patterns.items():
            # WHY: Check file-based indicators first
            found = False
            for indicator in indicators:
                if "*" in indicator:
                    if list(self.project_path.glob(indicator)):
                        found = True
                        break
                else:
                    if (self.project_path / indicator).exists():
                        found = True
                        break

            if found:
                self.log(f"Detected {project_type} subtype: {subtype}")
                subtypes.append(subtype)

        # WHY: Check package.json for Node.js subtypes
        if project_type == "nodejs":
            subtypes.extend(self._detect_nodejs_subtypes())

        return subtypes

    def _detect_nodejs_subtypes(self) -> List[str]:
        """
        Detect Node.js subtypes from package.json.

        WHY: Many Node.js project characteristics are defined in package.json,
        not in file structure alone.
        """
        subtypes: List[str] = []
        package_json = self.project_path / "package.json"

        if not package_json.exists():
            return subtypes

        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))

            # WHY: Check if it's a library (has "main" but no "bin")
            if "main" in data and "bin" not in data:
                if "library" not in subtypes:
                    subtypes.append("library")

            # WHY: Check if it's an application (has "bin" or start script)
            if "bin" in data or data.get("scripts", {}).get("start"):
                if "application" not in subtypes:
                    subtypes.append("application")

            # WHY: Check dependencies for framework indicators
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

            if "react" in deps or "react-dom" in deps:
                if "react" not in subtypes:
                    subtypes.append("react")

            if "next" in deps:
                if "nextjs" not in subtypes:
                    subtypes.append("nextjs")

            if "express" in deps:
                if "express" not in subtypes:
                    subtypes.append("express")

        except (json.JSONDecodeError, OSError) as e:
            self.log(f"Error reading package.json: {e}")

        return subtypes

    def infer_python_capabilities(self) -> Dict[str, Any]:
        """
        Infer Python project capabilities.

        WHY: Different Python projects have different tooling available.
        Knowing what's available helps orchestrators choose the right commands.
        """
        caps: Dict[str, str | None] = {
            "package_manager": None,
            "test_framework": None,
            "linter": None,
            "formatter": None,
            "type_checker": None,
        }

        # WHY: Detect package manager by manifest files
        if (self.project_path / "uv.lock").exists():
            caps["package_manager"] = "uv"
        elif (self.project_path / "poetry.lock").exists():
            caps["package_manager"] = "poetry"
        elif (self.project_path / "Pipfile").exists():
            caps["package_manager"] = "pipenv"
        elif (self.project_path / "requirements.txt").exists():
            caps["package_manager"] = "pip"

        # WHY: Check for common test directories and config files
        if (self.project_path / "pytest.ini").exists() or (
            self.project_path / "pyproject.toml"
        ).exists():
            caps["test_framework"] = "pytest"
        elif (self.project_path / "tests").exists():
            caps["test_framework"] = "unittest"

        # WHY: Check for linter/formatter configs
        if (self.project_path / "ruff.toml").exists() or (
            self.project_path / "pyproject.toml"
        ).exists():
            caps["linter"] = "ruff"
            caps["formatter"] = "ruff"

        if (self.project_path / ".flake8").exists():
            caps["linter"] = "flake8"

        if (self.project_path / ".mypy.ini").exists() or (
            self.project_path / "mypy.ini"
        ).exists():
            caps["type_checker"] = "mypy"

        return caps

    def infer_nodejs_capabilities(self) -> Dict[str, Any]:
        """
        Infer Node.js project capabilities.

        WHY: Node.js ecosystem has many package managers and testing frameworks.
        Detecting the right one prevents command failures.
        """
        caps: Dict[str, str | None] = {
            "package_manager": None,
            "test_framework": None,
            "linter": None,
            "formatter": None,
        }

        # WHY: Detect package manager by lock files
        if (self.project_path / "pnpm-lock.yaml").exists():
            caps["package_manager"] = "pnpm"
        elif (self.project_path / "yarn.lock").exists():
            caps["package_manager"] = "yarn"
        elif (self.project_path / "package-lock.json").exists():
            caps["package_manager"] = "npm"

        # WHY: Check package.json for testing and linting tools
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text(encoding="utf-8"))

                deps = {
                    **data.get("dependencies", {}),
                    **data.get("devDependencies", {}),
                }

                # WHY: Common test frameworks
                if "vitest" in deps:
                    caps["test_framework"] = "vitest"
                elif "jest" in deps:
                    caps["test_framework"] = "jest"
                elif "mocha" in deps:
                    caps["test_framework"] = "mocha"

                # WHY: Common linters/formatters
                if "eslint" in deps:
                    caps["linter"] = "eslint"

                if "prettier" in deps:
                    caps["formatter"] = "prettier"

            except (json.JSONDecodeError, OSError) as e:
                self.log(f"Error reading package.json: {e}")

        return caps

    def infer_rust_capabilities(self) -> Dict[str, Any]:
        """
        Infer Rust project capabilities.

        WHY: Rust has standard tooling (cargo), but knowing if clippy/rustfmt
        are configured helps orchestrators provide better feedback.
        """
        return {
            "package_manager": "cargo",
            "test_framework": "cargo-test",
            "linter": "clippy",
            "formatter": "rustfmt",
        }

    def infer_go_capabilities(self) -> Dict[str, Any]:
        """
        Infer Go project capabilities.

        WHY: Go has standard tooling, but linters vary.
        """
        caps: Dict[str, str | None] = {
            "package_manager": "go",
            "test_framework": "go-test",
            "linter": None,
            "formatter": "gofmt",
        }

        # WHY: Check for common Go linter configs
        if (self.project_path / ".golangci.yml").exists():
            caps["linter"] = "golangci-lint"

        return caps

    def infer_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """
        Infer capabilities for all detected project types.

        WHY: Returns a dictionary keyed by project type, supporting polyglot projects.
        Each project type has its own capability set.
        """
        all_caps = {}

        for project_type in self.detected_types:
            if project_type == "python":
                all_caps["python"] = self.infer_python_capabilities()
            elif project_type == "nodejs":
                all_caps["nodejs"] = self.infer_nodejs_capabilities()
            elif project_type == "rust":
                all_caps["rust"] = self.infer_rust_capabilities()
            elif project_type == "go":
                all_caps["go"] = self.infer_go_capabilities()
            # WHY: Other project types get basic capabilities
            else:
                all_caps[project_type] = {}

        self.capabilities = all_caps
        return all_caps

    def analyze(self) -> Dict[str, Any]:
        """
        Run full analysis: detect types, subtypes, and capabilities.

        WHY: Single entry point for complete project analysis.
        Returns structured data ready for JSON serialization.
        """
        types = self.detect_project_types()

        if not types:
            self.log("No recognized project types found")
            return {
                "project_path": str(self.project_path),
                "types": [],
                "subtypes": {},
                "capabilities": {},
            }

        # WHY: Detect subtypes for each detected type
        for project_type in types:
            subtypes = self.detect_subtypes(project_type)
            if subtypes:
                self.detected_subtypes[project_type] = subtypes

        # WHY: Infer capabilities for each type
        capabilities = self.infer_capabilities()

        # WHY: Return comprehensive analysis in structured format
        return {
            "project_path": str(self.project_path),
            "types": sorted(list(types)),
            "subtypes": self.detected_subtypes,
            "capabilities": capabilities,
        }


def main() -> None:
    """
    CLI entry point for project detection.

    WHY: Provides a command-line interface for scripting and automation.
    Supports output to file or stdout, with optional verbose logging.
    """
    parser = argparse.ArgumentParser(
        description="Detect project type and infer capabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python project_detector.py --path ./my-project --output project_info.json
  python project_detector.py --path . --verbose
  python project_detector.py --path ~/projects/monorepo --output analysis.json --verbose
        """,
    )

    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Project directory to analyze (default: current directory)",
    )

    parser.add_argument(
        "--output", type=Path, help="Output JSON file (default: print to stdout)"
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose debug output to stderr"
    )

    args = parser.parse_args()

    # WHY: Validate project path exists before proceeding
    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        sys.exit(1)

    if not args.path.is_dir():
        print(f"Error: Path is not a directory: {args.path}", file=sys.stderr)
        sys.exit(1)

    # WHY: Run analysis
    detector = ProjectDetector(args.path, verbose=args.verbose)
    result = detector.analyze()

    if args.output:
        # WHY: Write to file if specified
        try:
            atomic_write_json(result, args.output)
            print(f"Analysis written to {args.output}", file=sys.stderr)
        except OSError as e:
            print(f"Error writing to {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # WHY: Print to stdout for piping to other tools
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
