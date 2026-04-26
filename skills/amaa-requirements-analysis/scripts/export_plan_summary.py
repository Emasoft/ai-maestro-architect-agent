#!/usr/bin/env python3
"""Export plan as markdown summary. Usage: python3 export_plan_summary.py [--output FILE]"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    try:
        return int(val)
    except ValueError:
        pass
    return val


PLAN_STATE_FILE = Path(".claude/orchestrator-plan-phase.local.md")


def parse_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file (stdlib only, no PyYAML)."""
    if not file_path.exists():
        return {}

    content = file_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}

    end_index = content.find("---", 3)
    if end_index == -1:
        return {}

    yaml_text = content[3:end_index].strip()
    result: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list | None = None

    for line in yaml_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- ") and current_key is not None and current_list is not None:
            item_val = stripped[2:].strip()
            if ": " in item_val:
                item_dict: dict[str, Any] = {}
                for part in item_val.split(", "):
                    if ": " in part:
                        k, v = part.split(": ", 1)
                        item_dict[k.strip()] = _parse_yaml_value(v)
                current_list.append(item_dict)
            else:
                current_list.append(_parse_yaml_value(item_val))
            continue

        if ": " in stripped or stripped.endswith(":"):
            if ": " in stripped:
                key, val = stripped.split(": ", 1)
            else:
                key = stripped[:-1]
                val = ""

            key = key.strip()
            parsed_val = _parse_yaml_value(val)

            if parsed_val == "" or parsed_val is None:
                current_key = key
                current_list = []
                result[key] = current_list
            elif isinstance(parsed_val, list):
                current_key = key
                current_list = parsed_val
                result[key] = current_list
            else:
                current_key = None
                current_list = None
                result[key] = parsed_val

    return result


def generate_summary(data: dict) -> str:
    """Generate a markdown summary of the plan."""
    plan_id = data.get("plan_id", "unknown")
    status = data.get("status", "unknown")
    goal = data.get("goal", "No goal set")
    created_at = data.get("created_at", "Unknown")
    now = datetime.now(timezone.utc).isoformat()

    sections = data.get("requirements_sections", [])
    modules = data.get("modules", [])

    lines = [
        f"# Plan Summary: {plan_id}",
        "",
        f"**Generated:** {now}",
        f"**Created:** {created_at}",
        f"**Status:** {status}",
        "",
        "## Goal",
        "",
        goal,
        "",
        "## Requirements Progress",
        "",
        "| Section | Status |",
        "|---------|--------|",
    ]

    for section in sections:
        name = section.get("name", "Unknown")
        sect_status = section.get("status", "pending")
        icon = "[x]" if sect_status == "complete" else "[ ]"
        lines.append(f"| {icon} {name} | {sect_status} |")

    lines.extend([
        "",
        "## Modules",
        "",
        "| ID | Name | Priority | Status | Criteria |",
        "|----|------|----------|--------|----------|",
    ])

    for module in modules:
        mod_id = module.get("id", "unknown")
        mod_name = module.get("name", mod_id)
        priority = module.get("priority", "medium")
        mod_status = module.get("status", "pending")
        criteria = module.get("acceptance_criteria", "Not defined")
        # Truncate long criteria
        if len(criteria) > 40:
            criteria = criteria[:37] + "..."
        lines.append(f"| {mod_id} | {mod_name} | {priority} | {mod_status} | {criteria} |")

    if not modules:
        lines.append("| (no modules defined) | - | - | - | - |")

    # Exit criteria
    lines.extend([
        "",
        "## Exit Criteria",
        "",
    ])

    req_file_exists = Path(data.get("requirements_file", "USER_REQUIREMENTS.md")).exists()
    all_req_complete = all(s.get("status") == "complete" for s in sections) if sections else False
    all_modules_have_criteria = all(m.get("acceptance_criteria") for m in modules) if modules else False
    has_modules = len(modules) > 0
    plan_complete = data.get("plan_phase_complete", False)

    criteria_status = [
        ("USER_REQUIREMENTS.md complete", req_file_exists and all_req_complete),
        ("All modules defined with acceptance criteria", has_modules and all_modules_have_criteria),
        ("GitHub Issues created for all modules", all(m.get("github_issue") for m in modules) if modules else False),
        ("User approved the plan", plan_complete),
    ]

    for criterion, met in criteria_status:
        icon = "[x]" if met else "[ ]"
        lines.append(f"- {icon} {criterion}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export plan summary")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()

    if not PLAN_STATE_FILE.exists():
        print("ERROR: Not in Plan Phase")
        print("Run /amaa-start-planning to begin planning")
        return 1

    data = parse_frontmatter(PLAN_STATE_FILE)
    if not data:
        print("ERROR: Could not parse plan state file")
        return 1

    summary = generate_summary(data)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(summary, encoding="utf-8")
        print(f"Summary exported to: {output_path}")
    else:
        print(summary)

    return 0


if __name__ == "__main__":
    sys.exit(main())
