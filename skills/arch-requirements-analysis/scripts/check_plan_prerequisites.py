#!/usr/bin/env python3
"""
Check Plan Prerequisites Script

Verifies all prerequisites are met before running /approve-plan.
Provides a checklist of what needs to be completed.

Usage:
    python3 check_plan_prerequisites.py
    python3 check_plan_prerequisites.py --fix-suggestions
"""

import argparse
import sys
from pathlib import Path

import yaml

PLAN_STATE_FILE = Path(".claude/orchestrator-plan-phase.local.md")
REQUIREMENTS_FILE = Path("USER_REQUIREMENTS.md")


def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    if not file_path.exists():
        return {}

    content = file_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}

    end_index = content.find("---", 3)
    if end_index == -1:
        return {}

    yaml_content = content[3:end_index].strip()
    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return {}


def check_prerequisites(show_fixes: bool = False) -> tuple[list, list]:
    """Check all prerequisites and return (passed, failed) lists."""
    passed = []
    failed = []

    # Check 1: Plan phase state file exists
    if PLAN_STATE_FILE.exists():
        passed.append("Plan phase state file exists")
    else:
        failed.append(("Plan phase state file missing", "/start-planning \"Your goal\""))
        return passed, failed  # Cannot continue without state file

    data = parse_frontmatter(PLAN_STATE_FILE)
    if not data:
        failed.append(("State file parse error", "Check YAML syntax"))
        return passed, failed

    # Check 2: Requirements file exists
    req_file = Path(data.get("requirements_file", "USER_REQUIREMENTS.md"))
    if req_file.exists():
        passed.append(f"Requirements file exists: {req_file}")
    else:
        failed.append((f"Requirements file missing: {req_file}", f"Create {req_file}"))

    # Check 3: All requirement sections complete
    sections = data.get("requirements_sections", [])
    for section in sections:
        name = section.get("name", "Unknown")
        status = section.get("status", "pending")
        if status == "complete":
            passed.append(f"Requirement section complete: {name}")
        else:
            failed.append(
                (f"Requirement section incomplete: {name} ({status})",
                 f"/modify-requirement requirement \"{name}\" --status complete")
            )

    # Check 4: Modules defined
    modules = data.get("modules", [])
    if modules:
        passed.append(f"Modules defined: {len(modules)}")
    else:
        failed.append(("No modules defined", "/add-requirement module \"name\" --criteria \"criteria\""))

    # Check 5: All modules have acceptance criteria
    for module in modules:
        mod_id = module.get("id", "unknown")
        criteria = module.get("acceptance_criteria")
        if criteria:
            passed.append(f"Module has criteria: {mod_id}")
        else:
            failed.append(
                (f"Module missing criteria: {mod_id}",
                 f"/modify-requirement module {mod_id} --criteria \"criteria\"")
            )

    # Check 6: Not already approved
    if data.get("plan_phase_complete"):
        passed.append("Plan already approved")
    else:
        passed.append("Plan ready for approval")

    return passed, failed


def main() -> int:
    parser = argparse.ArgumentParser(description="Check plan prerequisites")
    parser.add_argument("--fix-suggestions", "-f", action="store_true",
                        help="Show fix suggestions for failed checks")
    args = parser.parse_args()

    print("Checking Plan Prerequisites")
    print("=" * 50)

    passed, failed = check_prerequisites(args.fix_suggestions)

    # Print passed checks
    print("\nPassed:")
    for item in passed:
        print(f"  [PASS] {item}")

    # Print failed checks
    if failed:
        print("\nFailed:")
        for item, fix in failed:
            print(f"  [FAIL] {item}")
            if args.fix_suggestions:
                print(f"         Fix: {fix}")

    # Summary
    print("\n" + "=" * 50)
    total = len(passed) + len(failed)
    print(f"Result: {len(passed)}/{total} checks passed")

    if failed:
        print("\nPlan is NOT ready for approval.")
        print("Run with --fix-suggestions to see how to fix issues.")
        return 1
    else:
        print("\nPlan is ready for approval.")
        print("Run /approve-plan to proceed.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
