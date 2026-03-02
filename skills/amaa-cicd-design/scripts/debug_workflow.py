#!/usr/bin/env python3
"""
Debug script for GitHub Actions workflows.
Simulates workflow execution locally and identifies issues.

Usage:
    python debug-workflow.py [workflow-file] [--job JOB_NAME] [--verbose]

Examples:
    python debug-workflow.py .github/workflows/ci.yml
    python debug-workflow.py .github/workflows/release.yml --job build
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Please install PyYAML: pip install pyyaml")
    sys.exit(1)


class WorkflowDebugger:
    """Debug GitHub Actions workflows locally."""

    def __init__(self, workflow_path: Path, verbose: bool = False):
        self.workflow_path = workflow_path
        self.verbose = verbose
        self.workflow = self._load_workflow()
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def _load_workflow(self) -> dict[str, Any]:
        """Load and parse workflow YAML."""
        if not self.workflow_path.exists():
            raise FileNotFoundError(f"Workflow not found: {self.workflow_path}")

        with open(self.workflow_path) as f:
            content: dict[str, Any] = yaml.safe_load(f)
            return content

    def validate(self) -> bool:
        """Validate workflow structure."""
        print(f"\nValidating: {self.workflow_path}")
        print("=" * 60)

        # Check required fields
        if "name" not in self.workflow:
            self.warnings.append("Missing 'name' field")

        if "on" not in self.workflow:
            self.errors.append("Missing 'on' trigger field")

        if "jobs" not in self.workflow:
            self.errors.append("Missing 'jobs' field")
            return False

        # Validate each job
        for job_name, job in self.workflow.get("jobs", {}).items():
            self._validate_job(job_name, job)

        # Print results
        if self.warnings:
            print("\nWarnings:")
            for w in self.warnings:
                print(f"  - {w}")

        if self.errors:
            print("\nErrors:")
            for e in self.errors:
                print(f"  - {e}")
            return False

        print("\nValidation passed!")
        return True

    def _validate_job(self, name: str, job: dict[str, Any]) -> None:
        """Validate a single job."""
        if "runs-on" not in job:
            self.errors.append(f"Job '{name}': missing 'runs-on'")

        if "steps" not in job:
            self.errors.append(f"Job '{name}': missing 'steps'")
            return

        for i, step in enumerate(job.get("steps", [])):
            self._validate_step(name, i, step)

    def _validate_step(self, job_name: str, index: int, step: dict[str, Any]) -> None:
        """Validate a single step."""
        if "uses" not in step and "run" not in step:
            self.warnings.append(f"Job '{job_name}' step {index}: no 'uses' or 'run'")

        # Check for deprecated actions
        if "uses" in step:
            action = step["uses"]
            deprecated = {
                "actions/checkout@v2": "actions/checkout@v4",
                "actions/checkout@v3": "actions/checkout@v4",
                "actions/upload-artifact@v2": "actions/upload-artifact@v4",
                "actions/upload-artifact@v3": "actions/upload-artifact@v4",
                "actions/download-artifact@v2": "actions/download-artifact@v4",
                "actions/download-artifact@v3": "actions/download-artifact@v4",
                "actions/cache@v2": "actions/cache@v4",
                "actions/cache@v3": "actions/cache@v4",
            }

            for old, new in deprecated.items():
                if action == old:
                    self.warnings.append(f"Job '{job_name}': update {old} to {new}")

    def simulate_job(self, job_name: str) -> bool:
        """Simulate running a specific job locally."""
        if job_name not in self.workflow.get("jobs", {}):
            print(f"Job '{job_name}' not found in workflow")
            return False

        job = self.workflow["jobs"][job_name]
        print(f"\nSimulating job: {job_name}")
        print("=" * 60)

        runner = job.get("runs-on", "unknown")
        print(f"Runner: {runner}")

        # Check if we can run locally
        current_os = self._get_current_os()
        if not self._can_run_locally(runner, current_os):
            print(f"\nCannot simulate: requires {runner}, running on {current_os}")
            print("Use 'act' for full local simulation: https://github.com/nektos/act")
            return False

        # Execute steps
        for i, step in enumerate(job.get("steps", [])):
            step_name = step.get("name", f"Step {i + 1}")
            print(f"\n[{i + 1}] {step_name}")

            if "uses" in step:
                print(f"    Action: {step['uses']}")
                print("    (Actions cannot be simulated locally)")
                continue

            if "run" in step:
                if self.verbose:
                    print(f"    Command: {step['run'][:100]}...")

                # Ask before running
                response = input("    Run this step? [y/N]: ")
                if response.lower() == "y":
                    success = self._run_command(step["run"], step.get("env", {}))
                    if not success:
                        print("    FAILED")
                        return False
                    print("    OK")

        print("\nSimulation complete!")
        return True

    def _get_current_os(self) -> str:
        """Get current operating system."""
        import platform

        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        return system

    def _can_run_locally(self, runner: str, current_os: str) -> bool:
        """Check if runner can be simulated on current OS."""
        runner_map = {
            "ubuntu-latest": "linux",
            "ubuntu-22.04": "linux",
            "ubuntu-24.04": "linux",
            "macos-14": "macos",
            "macos-13": "macos",
            "macos-latest": "macos",
            "windows-latest": "windows",
        }

        required_os = runner_map.get(runner, runner)
        return required_os == current_os

    def _run_command(self, command: str, env: dict[str, str]) -> bool:
        """Run a shell command."""
        import os

        full_env = os.environ.copy()
        full_env.update(env)

        try:
            result = subprocess.run(
                command,
                shell=True,
                env=full_env,
                capture_output=not self.verbose,
                text=True,
            )
            return result.returncode == 0
        except Exception as e:
            print(f"    Error: {e}")
            return False

    def list_jobs(self) -> None:
        """List all jobs in the workflow."""
        print(f"\nJobs in {self.workflow_path}:")
        print("-" * 40)

        for job_name, job in self.workflow.get("jobs", {}).items():
            runner = job.get("runs-on", "unknown")
            needs = job.get("needs", [])
            if isinstance(needs, str):
                needs = [needs]

            deps = f" (needs: {', '.join(needs)})" if needs else ""
            print(f"  {job_name}: {runner}{deps}")

    def check_secrets(self) -> list[str]:
        """Find all secrets referenced in the workflow."""
        secrets: set[str] = set()

        def find_secrets(obj: str | dict[str, Any] | list[Any] | Any) -> None:
            if isinstance(obj, str):
                import re

                matches = re.findall(r"\$\{\{\s*secrets\.(\w+)\s*\}\}", obj)
                secrets.update(matches)
            elif isinstance(obj, dict):
                for v in obj.values():
                    find_secrets(v)
            elif isinstance(obj, list):
                for item in obj:
                    find_secrets(item)

        find_secrets(self.workflow)

        print(f"\nSecrets required by {self.workflow_path}:")
        print("-" * 40)
        for secret in sorted(secrets):
            print(f"  - {secret}")

        return list(secrets)


def main() -> int:
    parser = argparse.ArgumentParser(description="Debug GitHub Actions workflows")
    parser.add_argument(
        "workflow",
        nargs="?",
        default=".github/workflows/ci.yml",
        help="Path to workflow file",
    )
    parser.add_argument("--job", "-j", help="Simulate specific job")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--list", "-l", action="store_true", help="List all jobs")
    parser.add_argument(
        "--secrets", "-s", action="store_true", help="List required secrets"
    )

    args = parser.parse_args()

    try:
        debugger = WorkflowDebugger(Path(args.workflow), args.verbose)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1

    if args.list:
        debugger.list_jobs()
        return 0

    if args.secrets:
        debugger.check_secrets()
        return 0

    if not debugger.validate():
        return 1

    if args.job:
        return 0 if debugger.simulate_job(args.job) else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
