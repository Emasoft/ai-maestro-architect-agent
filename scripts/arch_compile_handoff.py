#!/usr/bin/env python3
"""
atlas_compile_handoff.py - Compile template to handoff document for implementer.

Takes a module specification and compiles it with the handoff template,
filling in all placeholders with module-specific data.

NO shell wrappers - runs via 'python3 script.py' directly.
NO external dependencies - Python 3.8+ stdlib only.

Usage:
    # Compile handoff for module assignment
    python3 atlas_compile_handoff.py auth-core implementer-1 --platform web

    # With custom template
    python3 atlas_compile_handoff.py auth-core implementer-1 --platform web \
        --template custom-handoff-template.md

    # Preview without saving
    python3 atlas_compile_handoff.py auth-core implementer-1 --platform web --preview

Exit codes:
    0 - Success
    1 - Error (module not found, template not found, etc.)

Environment variables:
    CLAUDE_PROJECT_ROOT - Project root directory (defaults to current directory)
"""

import argparse
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


def log(level: str, message: str) -> None:
    """Write log message to stderr.

    Args:
        level: Log level (INFO, ERROR, SUCCESS)
        message: Log message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)


def parse_yaml_frontmatter(content: str) -> tuple[dict[str, str | list[str]], str]:
    """Parse YAML frontmatter from markdown content.

    Args:
        content: Markdown content with optional YAML frontmatter

    Returns:
        Tuple of (frontmatter dict, body content)
    """
    if not content.startswith("---"):
        return {}, content

    end_index = content.find("---", 3)
    if end_index == -1:
        return {}, content

    yaml_content = content[3:end_index].strip()
    body = content[end_index + 3 :].strip()

    # Simple YAML parsing (no external deps)
    data: dict[str, str | list[str]] = {}
    current_list: list[str] | None = None

    for line in yaml_content.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue

        # Handle list items
        if line.startswith("  - "):
            if current_list is not None:
                current_list.append(line[4:].strip())
            continue

        # Handle key: value pairs
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()

            if value == "":
                # Start of a list or nested object
                _ = key  # noqa: F841 - key tracked via data[key]
                current_list = []
                data[key] = current_list
            else:
                # Simple value - reset list context
                _ = key  # Track key for potential future use
                current_list = None
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                data[key] = value

    return data, body


def load_state_file(project_root: Path) -> dict[str, str | list[str]]:
    """Load orchestration phase state file.

    Args:
        project_root: Project root directory

    Returns:
        State file data dictionary
    """
    state_path = project_root / ".claude" / "orchestrator-exec-phase.local.md"
    if not state_path.exists():
        return {}

    content = state_path.read_text(encoding="utf-8")
    data, _ = parse_yaml_frontmatter(content)
    return data


def find_module(state_data: dict[str, Any], module_id: str) -> dict[str, Any] | None:
    """Find module by ID in state data.

    Args:
        state_data: State file data
        module_id: Module identifier

    Returns:
        Module dict or None if not found
    """
    modules = state_data.get("modules_status", [])
    for module in modules:
        if isinstance(module, dict) and module.get("id") == module_id:
            return module
    return None


def load_template(template_path: Path) -> str:
    """Load template file.

    Args:
        template_path: Path to template file

    Returns:
        Template content
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def load_spec(spec_path: Path) -> tuple[dict[str, str | list[str]], str]:
    """Load module specification file.

    Args:
        spec_path: Path to spec file

    Returns:
        Tuple of (spec metadata, spec body)
    """
    if not spec_path.exists():
        return {}, ""
    content = spec_path.read_text(encoding="utf-8")
    return parse_yaml_frontmatter(content)


def compile_handoff(
    template: str,
    module: dict[str, Any],
    agent_id: str,
    spec_content: str,
    platform: str,
    project_root: Path,
) -> str:
    """Compile handoff from template with module data.

    Args:
        template: Template content with placeholders
        module: Module data dictionary
        agent_id: Agent identifier
        spec_content: Module specification content
        platform: Platform name
        project_root: Project root directory

    Returns:
        Compiled handoff content
    """
    # Generate task UUID
    task_uuid = f"task-{uuid.uuid4().hex[:12]}"

    # Current timestamp
    assigned_at = datetime.now().isoformat()

    # Placeholder replacements
    replacements = {
        "{{MODULE_NAME}}": module.get("name", "Unknown Module"),
        "{{MODULE_ID}}": module.get("id", "unknown"),
        "{{MODULE_DESCRIPTION}}": module.get("description", ""),
        "{{AGENT_ID}}": agent_id,
        "{{TASK_UUID}}": task_uuid,
        "{{GITHUB_ISSUE}}": module.get("github_issue", "N/A"),
        "{{ASSIGNED_AT}}": assigned_at,
        "{{PRIORITY}}": module.get("priority", "medium"),
        "{{ACCEPTANCE_CRITERIA}}": module.get(
            "acceptance_criteria", "See specification"
        ),
        "{{MODULE_SPEC_CONTENT}}": spec_content or "See linked specification file",
        "{{PLATFORM}}": platform,
        "{{CONFIG_FILES}}": f"See .atlas/config/{platform}/",
        "{{SPEC_PATH}}": f".atlas/designs/{platform}/specs/{module.get('id', 'unknown')}.md",
        "{{RDD_PATH}}": f".atlas/designs/{platform}/rdd/{module.get('id', 'unknown')}-rdd.md",
        "{{ARCH_PATH}}": ".atlas/designs/shared/ARCHITECTURE.md",
        "{{SUCCESS_METRICS}}": "All acceptance criteria met, tests passing, code reviewed",
        "{{REQUIREMENTS_LIST}}": module.get("requirements", "See specification"),
        "{{DEPENDENCIES}}": ", ".join(module.get("dependencies", [])) or "None",
        "{{TECHNICAL_DESIGN}}": "See specification",
        "{{TEST_REQUIREMENTS}}": "Unit tests, integration tests required",
    }

    compiled = template
    for placeholder, value in replacements.items():
        compiled = compiled.replace(placeholder, str(value))

    # Handle any remaining placeholders with default empty string
    compiled = re.sub(r"\{\{[A-Z_]+\}\}", "", compiled)

    return compiled


def save_handoff(
    handoff_content: str,
    module_id: str,
    agent_id: str,
    project_root: Path,
) -> Path:
    """Save compiled handoff to file.

    Args:
        handoff_content: Compiled handoff content
        module_id: Module identifier
        agent_id: Agent identifier
        project_root: Project root directory

    Returns:
        Path to saved handoff file
    """
    handoff_dir = project_root / ".atlas" / "handoffs" / agent_id
    handoff_dir.mkdir(parents=True, exist_ok=True)

    handoff_path = handoff_dir / f"{module_id}-handoff.md"
    handoff_path.write_text(handoff_content, encoding="utf-8")

    return handoff_path


def main() -> int:
    """Main entry point.

    Returns:
        Exit code: 0 for success, 1 for error
    """
    parser = argparse.ArgumentParser(description="Compile template to handoff document")
    parser.add_argument(
        "module_id",
        help="Module identifier",
    )
    parser.add_argument(
        "agent_id",
        help="Agent identifier",
    )
    parser.add_argument(
        "--platform",
        required=True,
        help="Platform name (e.g., web, ios, android)",
    )
    parser.add_argument(
        "--template",
        help="Custom template path (default: uses platform handoff-template.md)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview compiled handoff without saving",
    )
    parser.add_argument(
        "--root",
        default=".atlas",
        help="Design folder root (default: .atlas)",
    )

    args = parser.parse_args()

    # Get project root
    project_root = Path(os.environ.get("CLAUDE_PROJECT_ROOT", os.getcwd()))
    atlas_root = project_root / args.root

    log("INFO", f"Compiling handoff for module: {args.module_id}")
    log("INFO", f"Agent: {args.agent_id}")
    log("INFO", f"Platform: {args.platform}")

    try:
        # Load state file to get module data
        state_data = load_state_file(project_root)
        module = find_module(state_data, args.module_id)

        if not module:
            # Try to create minimal module data if not in state
            log("INFO", "Module not found in state file, using minimal data")
            module = {
                "id": args.module_id,
                "name": args.module_id.replace("-", " ").title(),
                "priority": "medium",
                "github_issue": "N/A",
            }

        # Load template
        if args.template:
            template_path = Path(args.template)
        else:
            template_path = (
                atlas_root
                / "designs"
                / args.platform
                / "templates"
                / "handoff-template.md"
            )

        template = load_template(template_path)

        # Load spec content if exists
        spec_path = (
            atlas_root / "designs" / args.platform / "specs" / f"{args.module_id}.md"
        )
        _, spec_content = load_spec(spec_path)

        # Compile handoff
        handoff_content = compile_handoff(
            template=template,
            module=module,
            agent_id=args.agent_id,
            spec_content=spec_content,
            platform=args.platform,
            project_root=project_root,
        )

        if args.preview:
            print("\n--- PREVIEW ---\n")
            print(handoff_content)
            print("\n--- END PREVIEW ---\n")
            return 0

        # Save handoff
        handoff_path = save_handoff(
            handoff_content=handoff_content,
            module_id=args.module_id,
            agent_id=args.agent_id,
            project_root=project_root,
        )

        print("\nHandoff compiled successfully!")
        print(f"  Module: {args.module_id}")
        print(f"  Agent: {args.agent_id}")
        print(f"  Saved to: {handoff_path}")

        return 0

    except FileNotFoundError as e:
        log("ERROR", str(e))
        return 1
    except PermissionError as e:
        log("ERROR", f"Permission denied: {e}")
        return 1
    except OSError as e:
        log("ERROR", f"OS error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
