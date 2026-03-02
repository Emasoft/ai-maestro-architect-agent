#!/usr/bin/env python3
"""
Validate GitHub Actions workflow YAML files.

Usage:
    python validate-yaml.py [path]

Examples:
    python validate-yaml.py                           # Validate all workflows
    python validate-yaml.py .github/workflows/ci.yml  # Validate specific file
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Please install PyYAML: pip install pyyaml")
    sys.exit(1)


class WorkflowValidator:
    """Validate GitHub Actions workflow files."""

    VALID_TRIGGERS = {
        "push",
        "pull_request",
        "pull_request_target",
        "workflow_dispatch",
        "workflow_call",
        "schedule",
        "release",
        "issues",
        "issue_comment",
        "watch",
        "fork",
        "create",
        "delete",
        "repository_dispatch",
    }

    VALID_RUNNERS = {
        "ubuntu-latest",
        "ubuntu-22.04",
        "ubuntu-24.04",
        "ubuntu-24.04-arm",
        "macos-latest",
        "macos-14",
        "macos-13",
        "windows-latest",
        "windows-2022",
    }

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_file(self, path: Path) -> bool:
        """Validate a single workflow file."""
        self.errors = []
        self.warnings = []

        print(f"\nValidating: {path}")

        # Check file extension
        if path.suffix not in {".yml", ".yaml"}:
            self.errors.append("File must have .yml or .yaml extension")

        # Parse YAML
        try:
            with open(path) as f:
                workflow = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parse error: {e}")
            self._print_results()
            return False

        if not isinstance(workflow, dict):
            self.errors.append("Workflow must be a YAML mapping")
            self._print_results()
            return False

        # Validate structure
        self._validate_name(workflow)
        self._validate_triggers(workflow)
        self._validate_permissions(workflow)
        self._validate_jobs(workflow)

        self._print_results()
        return len(self.errors) == 0

    def _validate_name(self, workflow: dict[str, Any]) -> None:
        """Validate workflow name."""
        if "name" not in workflow:
            self.warnings.append("Missing 'name' field (recommended)")
        elif not isinstance(workflow["name"], str):
            self.errors.append("'name' must be a string")

    def _validate_triggers(self, workflow: dict[str, Any]) -> None:
        """Validate workflow triggers."""
        if "on" not in workflow:
            self.errors.append("Missing 'on' trigger field")
            return

        triggers = workflow["on"]

        # Can be string, list, or dict
        if isinstance(triggers, str):
            if triggers not in self.VALID_TRIGGERS:
                self.warnings.append(f"Unknown trigger: {triggers}")

        elif isinstance(triggers, list):
            for t in triggers:
                if t not in self.VALID_TRIGGERS:
                    self.warnings.append(f"Unknown trigger: {t}")

        elif isinstance(triggers, dict):
            for trigger, config in triggers.items():
                if trigger not in self.VALID_TRIGGERS:
                    self.warnings.append(f"Unknown trigger: {trigger}")

                # Validate schedule cron
                if trigger == "schedule" and config:
                    for item in config:
                        if "cron" in item:
                            self._validate_cron(item["cron"])

    def _validate_cron(self, cron: str) -> None:
        """Validate cron expression."""
        parts = cron.split()
        if len(parts) != 5:
            self.errors.append(f"Invalid cron expression: {cron} (need 5 fields)")

    def _validate_permissions(self, workflow: dict[str, Any]) -> None:
        """Validate permissions."""
        if "permissions" not in workflow:
            return

        perms = workflow["permissions"]
        if isinstance(perms, str):
            if perms not in {"read-all", "write-all"}:
                self.errors.append(f"Invalid permissions value: {perms}")

        elif isinstance(perms, dict):
            valid_scopes = {
                "actions",
                "checks",
                "contents",
                "deployments",
                "id-token",
                "issues",
                "packages",
                "pages",
                "pull-requests",
                "repository-projects",
                "security-events",
                "statuses",
            }
            valid_levels = {"read", "write", "none"}

            for scope, level in perms.items():
                if scope not in valid_scopes:
                    self.warnings.append(f"Unknown permission scope: {scope}")
                if level not in valid_levels:
                    self.errors.append(f"Invalid permission level: {level}")

    def _validate_jobs(self, workflow: dict[str, Any]) -> None:
        """Validate jobs."""
        if "jobs" not in workflow:
            self.errors.append("Missing 'jobs' field")
            return

        jobs = workflow["jobs"]
        if not isinstance(jobs, dict):
            self.errors.append("'jobs' must be a mapping")
            return

        if not jobs:
            self.errors.append("No jobs defined")
            return

        job_names = set(jobs.keys())

        for name, job in jobs.items():
            self._validate_job(name, job, job_names)

    def _validate_job(self, name: str, job: dict[str, Any], all_jobs: set[str]) -> None:
        """Validate a single job."""
        prefix = f"Job '{name}'"

        if not isinstance(job, dict):
            self.errors.append(f"{prefix}: must be a mapping")
            return

        # runs-on
        if "runs-on" not in job:
            self.errors.append(f"{prefix}: missing 'runs-on'")
        else:
            runner = job["runs-on"]
            if isinstance(runner, str):
                if runner not in self.VALID_RUNNERS and not runner.startswith("${{"):
                    self.warnings.append(f"{prefix}: unknown runner '{runner}'")

        # needs (dependencies)
        if "needs" in job:
            needs = job["needs"]
            if isinstance(needs, str):
                needs = [needs]
            for dep in needs:
                if dep not in all_jobs:
                    self.errors.append(f"{prefix}: depends on unknown job '{dep}'")

        # steps
        if "steps" not in job and "uses" not in job:
            self.errors.append(f"{prefix}: missing 'steps' or 'uses'")
        elif "steps" in job:
            steps = job["steps"]
            if not isinstance(steps, list):
                self.errors.append(f"{prefix}: 'steps' must be a list")
            else:
                for i, step in enumerate(steps):
                    self._validate_step(name, i, step)

    def _validate_step(self, job_name: str, index: int, step: dict[str, Any]) -> None:
        """Validate a single step."""
        prefix = f"Job '{job_name}' step {index + 1}"

        if not isinstance(step, dict):
            self.errors.append(f"{prefix}: must be a mapping")
            return

        has_uses = "uses" in step
        has_run = "run" in step

        if not has_uses and not has_run:
            self.warnings.append(f"{prefix}: no 'uses' or 'run'")

        if has_uses and has_run:
            self.errors.append(f"{prefix}: cannot have both 'uses' and 'run'")

        # Validate action version
        if has_uses:
            action = step["uses"]
            if "@" not in action and not action.startswith("./"):
                self.warnings.append(f"{prefix}: action '{action}' missing version")
            elif (
                "@v" not in action
                and "@main" not in action
                and not action.startswith("./")
            ):
                # Check if using commit SHA (40 chars)
                version = action.split("@")[-1]
                if len(version) != 40:
                    self.warnings.append(
                        f"{prefix}: consider pinning action to specific version"
                    )

    def _print_results(self) -> None:
        """Print validation results."""
        if self.warnings:
            print("\n  Warnings:")
            for w in self.warnings:
                print(f"    - {w}")

        if self.errors:
            print("\n  Errors:")
            for e in self.errors:
                print(f"    - {e}")

        if not self.errors and not self.warnings:
            print("  OK")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GitHub Actions workflows")
    parser.add_argument(
        "path",
        nargs="?",
        default=".github/workflows",
        help="File or directory to validate",
    )

    args = parser.parse_args()
    path = Path(args.path)

    validator = WorkflowValidator()
    all_valid = True

    if path.is_file():
        all_valid = validator.validate_file(path)
    elif path.is_dir():
        workflows = list(path.glob("*.yml")) + list(path.glob("*.yaml"))
        if not workflows:
            print(f"No workflow files found in {path}")
            return 1

        for workflow in workflows:
            if not validator.validate_file(workflow):
                all_valid = False
    else:
        print(f"Path not found: {path}")
        return 1

    print("\n" + "=" * 60)
    if all_valid:
        print("All workflows valid!")
        return 0
    else:
        print("Validation failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
