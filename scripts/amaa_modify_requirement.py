#!/usr/bin/env python3
"""
Architect Modify Requirement Script

Handles add, modify, and remove operations for requirements and modules
during Plan Phase. Supports dynamic flexibility in the planning process.

Usage:
    python3 arch_modify_requirement.py add requirement "Security Requirements"
    python3 arch_modify_requirement.py add module "auth-core" --criteria "Support JWT"
    python3 arch_modify_requirement.py modify module auth-core --priority critical
    python3 arch_modify_requirement.py remove module legacy-api
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

# Plan phase state file location
PLAN_STATE_FILE = Path(".claude/orchestrator-plan-phase.local.md")


def parse_frontmatter(file_path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (data, body)."""
    if not file_path.exists():
        return {}, ""

    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return {}, content

    end_index = content.find("---", 3)
    if end_index == -1:
        return {}, content

    yaml_content = content[3:end_index].strip()
    body = content[end_index + 3 :].strip()

    try:
        data = yaml.safe_load(yaml_content) or {}
        return data, body
    except yaml.YAMLError:
        return {}, content


def write_state_file(data: dict, body: str) -> bool:
    """Write the state file with updated frontmatter."""
    try:
        yaml_content = yaml.dump(
            data, default_flow_style=False, allow_unicode=True, sort_keys=False
        )
        content = f"---\n{yaml_content}---\n\n{body}"
        PLAN_STATE_FILE.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"ERROR: Failed to write state file: {e}")
        return False


def normalize_id(name: str) -> str:
    """Convert a name to a valid ID (kebab-case)."""
    # Convert to lowercase and replace spaces/underscores with hyphens
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower())
    # Remove leading/trailing hyphens
    return normalized.strip("-")


def add_requirement(data: dict, name: str) -> bool:
    """Add a new requirement section."""
    sections = data.get("requirements_sections", [])

    # Check if already exists
    for section in sections:
        if section.get("name") == name:
            print(f"ERROR: Requirement section '{name}' already exists")
            return False

    sections.append({"name": name, "status": "pending"})
    data["requirements_sections"] = sections
    print(f"✓ Added requirement section: {name}")
    return True


def add_module(data: dict, name: str, criteria: str | None, priority: str) -> bool:
    """Add a new module."""
    modules = data.get("modules", [])
    module_id = normalize_id(name)

    # Check if already exists
    for module in modules:
        if module.get("id") == module_id:
            print(f"ERROR: Module '{module_id}' already exists")
            return False

    new_module = {
        "id": module_id,
        "name": name,
        "status": "planned",
        "priority": priority,
        "github_issue": None,
    }

    if criteria:
        new_module["acceptance_criteria"] = criteria

    modules.append(new_module)
    data["modules"] = modules
    print(f"✓ Added module: {module_id}")
    print(f"  Name: {name}")
    print(f"  Priority: {priority}")
    if criteria:
        print(f"  Criteria: {criteria}")
    return True


def modify_requirement(data: dict, name: str, new_status: str | None) -> bool:
    """Modify an existing requirement section."""
    sections = data.get("requirements_sections", [])

    for section in sections:
        if section.get("name") == name:
            if new_status:
                section["status"] = new_status
                print(f"✓ Updated requirement section '{name}' status to: {new_status}")
            return True

    print(f"ERROR: Requirement section '{name}' not found")
    return False


def modify_module(
    data: dict,
    module_id: str,
    new_name: str | None,
    new_criteria: str | None,
    new_status: str | None,
    new_priority: str | None,
) -> bool:
    """Modify an existing module."""
    modules = data.get("modules", [])

    for module in modules:
        if module.get("id") == module_id:
            # Check if can be modified
            current_status = module.get("status", "pending")
            if current_status in ("in-progress", "complete"):
                if new_status != current_status:  # Allow same status updates
                    print(f"ERROR: Cannot modify module with status '{current_status}'")
                    return False

            if new_name:
                module["name"] = new_name
                print(f"  Name updated to: {new_name}")
            if new_criteria:
                module["acceptance_criteria"] = new_criteria
                print("  Criteria updated")
            if new_status:
                module["status"] = new_status
                print(f"  Status updated to: {new_status}")
            if new_priority:
                module["priority"] = new_priority
                print(f"  Priority updated to: {new_priority}")

            print(f"✓ Modified module: {module_id}")
            return True

    print(f"ERROR: Module '{module_id}' not found")
    return False


def remove_requirement(data: dict, name: str, force: bool) -> bool:
    """Remove a requirement section."""
    sections = data.get("requirements_sections", [])

    for i, section in enumerate(sections):
        if section.get("name") == name:
            status = section.get("status", "pending")
            if status != "pending" and not force:
                print(f"ERROR: Cannot remove requirement with status '{status}'")
                print("Use --force to remove anyway")
                return False

            sections.pop(i)
            data["requirements_sections"] = sections
            print(f"✓ Removed requirement section: {name}")
            return True

    print(f"ERROR: Requirement section '{name}' not found")
    return False


def remove_module(data: dict, module_id: str, force: bool) -> bool:
    """Remove a module."""
    modules = data.get("modules", [])

    for i, module in enumerate(modules):
        if module.get("id") == module_id:
            status = module.get("status", "pending")
            if status in ("in-progress", "complete") and not force:
                print(f"ERROR: Cannot remove module with status '{status}'")
                print("Use --force to remove anyway (not recommended)")
                return False

            if module.get("github_issue") and not force:
                print("ERROR: Cannot remove module with GitHub Issue assigned")
                print("Close the issue first or use --force")
                return False

            modules.pop(i)
            data["modules"] = modules
            print(f"✓ Removed module: {module_id}")
            return True

    print(f"ERROR: Module '{module_id}' not found")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add, modify, or remove requirements and modules"
    )
    parser.add_argument(
        "action", choices=["add", "modify", "remove"], help="Action to perform"
    )
    parser.add_argument("type", choices=["requirement", "module"], help="Type of item")
    parser.add_argument("name", help="Name or ID of the item")
    parser.add_argument("--criteria", "-c", help="Acceptance criteria (for modules)")
    parser.add_argument(
        "--status",
        "-s",
        choices=["pending", "in-progress", "complete", "planned"],
        help="New status",
    )
    parser.add_argument(
        "--priority",
        "-p",
        choices=["critical", "high", "medium", "low"],
        default="medium",
        help="Priority level (for modules)",
    )
    parser.add_argument("--new-name", "-n", help="New name (for modify)")
    parser.add_argument(
        "--force", "-f", action="store_true", help="Force the operation"
    )

    args = parser.parse_args()

    # Check if in plan phase
    if not PLAN_STATE_FILE.exists():
        print("ERROR: Not in Plan Phase")
        print("Run /start-planning to begin planning")
        return 1

    data, body = parse_frontmatter(PLAN_STATE_FILE)
    if not data:
        print("ERROR: Could not parse plan state file")
        return 1

    success = False

    if args.action == "add":
        if args.type == "requirement":
            success = add_requirement(data, args.name)
        else:  # module
            success = add_module(data, args.name, args.criteria, args.priority)

    elif args.action == "modify":
        if args.type == "requirement":
            success = modify_requirement(data, args.name, args.status)
        else:  # module
            success = modify_module(
                data,
                args.name,
                args.new_name,
                args.criteria,
                args.status,
                args.priority,
            )

    elif args.action == "remove":
        if args.type == "requirement":
            success = remove_requirement(data, args.name, args.force)
        else:  # module
            success = remove_module(data, args.name, args.force)

    if success:
        if not write_state_file(data, body):
            return 1

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
