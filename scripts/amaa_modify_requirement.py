#!/usr/bin/env python3
"""
Architect Modify Requirement Script

Handles add, modify, and remove operations for requirements and modules
during Plan Phase. Supports dynamic flexibility in the planning process.

Usage:
    python3 amaa_modify_requirement.py add requirement "Security Requirements"
    python3 amaa_modify_requirement.py add module "auth-core" --criteria "Support JWT"
    python3 amaa_modify_requirement.py modify module auth-core --priority critical
    python3 amaa_modify_requirement.py remove module legacy-api
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any

# Plan phase state file location
PLAN_STATE_FILE = Path(".claude/orchestrator-plan-phase.local.md")


def _parse_yaml_value(val: str) -> Any:
    """Parse a simple YAML scalar value (no external dependency)."""
    val = val.strip()
    if val in ('true', 'True'):
        return True
    if val in ('false', 'False'):
        return False
    if val in ('null', 'None', '~', ''):
        return None
    if val == '[]':
        return []
    # Remove surrounding quotes
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    # Try integer
    try:
        return int(val)
    except ValueError:
        pass
    return val


def parse_frontmatter(file_path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (data, body). No PyYAML dependency."""
    if not file_path.exists():
        return {}, ""

    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return {}, content

    end_index = content.find("---", 3)
    if end_index == -1:
        return {}, content

    yaml_text = content[3:end_index].strip()
    body = content[end_index + 3:].strip()

    data: dict[str, Any] = {}
    lines = yaml_text.split("\n")
    i = 0
    current_key: str | None = None
    current_list: list[Any] | None = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip comments and blank lines
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # List item (starts with "- ")
        if stripped.startswith("- ") and current_key is not None:
            item_text = stripped[2:]
            # Check if it's a dict item (key: value)
            if ": " in item_text:
                item_dict: dict[str, Any] = {}
                # Parse first key-value of this list item
                k, v = item_text.split(": ", 1)
                item_dict[k.strip()] = _parse_yaml_value(v)
                # Check subsequent indented lines for more keys in this dict
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    next_stripped = next_line.strip()
                    # Must be indented more than the "- " and be a key: value
                    if next_stripped and not next_stripped.startswith("- ") and not next_stripped.startswith("#") and ": " in next_stripped:
                        indent = len(next_line) - len(next_line.lstrip())
                        if indent >= 4:  # Part of the dict item
                            nk, nv = next_stripped.split(": ", 1)
                            item_dict[nk.strip()] = _parse_yaml_value(nv)
                            i += 1
                            continue
                    break
                if current_list is not None:
                    current_list.append(item_dict)
                continue
            else:
                # Simple list item
                if current_list is not None:
                    current_list.append(_parse_yaml_value(item_text))
                i += 1
                continue

        # Top-level key: value
        if ": " in stripped or stripped.endswith(":"):
            if ": " in stripped:
                key, val = stripped.split(": ", 1)
            else:
                key = stripped[:-1]
                val = ""
            key = key.strip()

            parsed_val = _parse_yaml_value(val)
            if parsed_val == [] or val.strip() == "":
                # Could be a list that follows
                data[key] = []
                current_key = key
                current_list = data[key]
            else:
                data[key] = parsed_val
                current_key = key
                current_list = None

            i += 1
            continue

        i += 1

    return data, body


def write_state_file(data: dict, body: str) -> bool:
    """Write the state file with YAML frontmatter. No PyYAML dependency."""
    try:
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, list):
                if not value:
                    lines.append(f"{key}: []")
                else:
                    lines.append(f"{key}:")
                    for item in value:
                        if isinstance(item, dict):
                            first = True
                            for ik, iv in item.items():
                                formatted_v = _format_yaml_value(iv)
                                if first:
                                    lines.append(f"  - {ik}: {formatted_v}")
                                    first = False
                                else:
                                    lines.append(f"    {ik}: {formatted_v}")
                        else:
                            lines.append(f"  - {_format_yaml_value(item)}")
            elif isinstance(value, bool):
                lines.append(f"{key}: {'true' if value else 'false'}")
            elif value is None:
                lines.append(f"{key}: null")
            else:
                lines.append(f"{key}: {_format_yaml_value(value)}")

        yaml_content = "\n".join(lines)
        content = f"---\n{yaml_content}\n---\n\n{body}"
        PLAN_STATE_FILE.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"ERROR: Failed to write state file: {e}")
        return False


def _format_yaml_value(val: Any) -> str:
    """Format a value for YAML output."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, str):
        # Quote strings that contain special characters
        if any(c in val for c in ':#{}[]|>&*!%@`') or val in ('true', 'false', 'null'):
            return f'"{val}"'
        return f'"{val}"'
    return str(val)


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
        print("Run /amaa-start-planning to begin planning")
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
