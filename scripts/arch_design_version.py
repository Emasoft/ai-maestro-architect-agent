#!/usr/bin/env python3
"""
atlas_design_version.py - Design document version management.

Creates new versions of existing design documents.
Uses atlas_design_search.py to find documents and atlas_design_uuid.py for UUID generation.

Usage:
    # Create new version of a document
    python atlas_design_version.py --uuid PROJ-SPEC-20250108-a7b3f2e1

    # Create version with reason
    python atlas_design_version.py --uuid PROJ-SPEC-... --reason "Major API changes"

    # List all versions of a document
    python atlas_design_version.py --list PROJ-SPEC-20250108-a7b3f2e1

Dependencies: Python 3.8+, atlas_design_search.py, atlas_design_uuid.py (same directory)
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def run_search_script(args: list[str], project_root: Path) -> str:
    """Run atlas_design_search.py with given arguments."""
    script_path = Path(__file__).parent / "atlas_design_search.py"
    cmd = ["python3", str(script_path)] + args + ["--project-root", str(project_root)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def parse_frontmatter(content: str) -> dict[str, Any]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}

    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}

    frontmatter: dict[str, Any] = {}
    for line in lines[1:end_idx]:
        if ":" in line:
            key, _, raw_value = line.partition(":")
            key = key.strip()
            raw_value = raw_value.strip()

            parsed_value: Any
            if raw_value.startswith('"') and raw_value.endswith('"'):
                parsed_value = raw_value[1:-1]
            elif raw_value.startswith("'") and raw_value.endswith("'"):
                parsed_value = raw_value[1:-1]
            elif raw_value.startswith("[") and raw_value.endswith("]"):
                inner = raw_value[1:-1]
                if inner:
                    items = [
                        item.strip().strip('"').strip("'")
                        for item in inner.split(",")
                        if item.strip()
                    ]
                    parsed_value = items
                else:
                    parsed_value = []
            elif raw_value.lower() == "null":
                parsed_value = None
            elif raw_value.isdigit():
                parsed_value = int(raw_value)
            else:
                parsed_value = raw_value

            frontmatter[key] = parsed_value

    return frontmatter


def extract_frontmatter_and_body(content: str) -> tuple[dict[str, Any], str]:
    """Extract frontmatter dict and body content."""
    if not content.startswith("---"):
        return {}, content

    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}, content

    fm = parse_frontmatter(content)
    body = "\n".join(lines[end_idx + 1 :])
    return fm, body


def find_document(uuid_str: str, project_root: Path) -> Path | None:
    """Find document path by UUID using search script."""
    output = run_search_script(["--uuid", uuid_str, "--output", "path"], project_root)
    if output and not output.startswith("No documents"):
        return project_root / output.split("\n")[0]
    return None


def find_all_versions(base_uuid: str, project_root: Path) -> list[tuple[str, Path]]:
    """Find all versions of a document."""
    # Strip version suffix
    base = re.sub(r"_v\d{4}$", "", base_uuid)
    output = run_search_script(
        ["--uuid-prefix", base, "--output", "json"], project_root
    )

    if not output or output.startswith("No documents"):
        return []

    import json

    try:
        docs = json.loads(output)
        return [(d["uuid"], Path(d["path"])) for d in docs]
    except (json.JSONDecodeError, KeyError):
        return []


def create_version(uuid_str: str, project_root: Path, reason: str = "") -> Path | None:
    """Create new version of a document.

    Returns path to new version file.
    """
    # Find source document
    source_path = find_document(uuid_str, project_root)
    if not source_path or not source_path.exists():
        print(f"ERROR: Document not found: {uuid_str}", file=sys.stderr)
        return None

    # Read source content
    content = source_path.read_text(encoding="utf-8")
    fm, body = extract_frontmatter_and_body(content)

    if not fm:
        print(f"ERROR: No frontmatter in source: {source_path}", file=sys.stderr)
        return None

    # Find highest existing version
    base_uuid = re.sub(r"_v\d{4}$", "", uuid_str)
    all_versions = find_all_versions(base_uuid, project_root)

    highest_version = 0
    for doc_uuid, _ in all_versions:
        match = re.search(r"_v(\d{4})$", doc_uuid)
        if match:
            highest_version = max(highest_version, int(match.group(1)))

    new_version = highest_version + 1
    new_uuid = f"{base_uuid}_v{new_version:04d}"

    # Update frontmatter for new version
    today = datetime.now().strftime("%Y-%m-%d")
    fm["uuid"] = new_uuid
    fm["previous_version"] = uuid_str
    fm["version"] = new_version
    fm["updated"] = today
    fm["status"] = "draft"

    # Build new frontmatter string
    fm_lines = ["---"]
    for key, value in fm.items():
        if isinstance(value, list):
            fm_lines.append(f"{key}: {value}")
        elif value is None:
            fm_lines.append(f"{key}: null")
        elif isinstance(value, str):
            fm_lines.append(f'{key}: "{value}"')
        else:
            fm_lines.append(f"{key}: {value}")
    fm_lines.append("---")

    new_content = "\n".join(fm_lines) + "\n" + body

    # Generate new filename
    source_stem = source_path.stem
    # Remove existing version suffix from stem
    source_stem = re.sub(r"_v\d{4}$", "", source_stem)
    new_filename = f"{source_stem}_v{new_version:04d}.md"
    new_path = source_path.parent / new_filename

    # Handle duplicates
    counter = 1
    while new_path.exists():
        new_filename = f"{source_stem}_v{new_version:04d}_{counter}.md"
        new_path = source_path.parent / new_filename
        counter += 1

    # Write new version
    new_path.write_text(new_content, encoding="utf-8")

    print(f"CREATED: {new_path}")
    print(f"UUID: {new_uuid}")
    print(f"Previous: {uuid_str}")
    if reason:
        print(f"Reason: {reason}")

    return new_path


def list_versions(base_uuid: str, project_root: Path) -> int:
    """List all versions of a document."""
    versions = find_all_versions(base_uuid, project_root)

    if not versions:
        print(f"No versions found for: {base_uuid}")
        return 1

    print(f"\nVersions of {re.sub(r'_v\\d{4}$', '', base_uuid)}:\n")
    print(f"{'Version':<10} {'UUID':<45} {'Path'}")
    print("-" * 100)

    for uuid_val, path in sorted(versions, key=lambda x: x[0]):
        match = re.search(r"_v(\d{4})$", uuid_val)
        version = match.group(1) if match else "base"
        rel_path = (
            path.relative_to(project_root)
            if path.is_relative_to(project_root)
            else path
        )
        print(f"{version:<10} {uuid_val:<45} {rel_path}")

    print(f"\nTotal: {len(versions)} version(s)")
    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Design document version management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new version
  python atlas_design_version.py --uuid PROJ-SPEC-20250108-a7b3f2e1

  # Create with reason
  python atlas_design_version.py --uuid PROJ-SPEC-... --reason "API update"

  # List all versions
  python atlas_design_version.py --list PROJ-SPEC-20250108-a7b3f2e1
        """,
    )

    parser.add_argument("--uuid", "-u", help="UUID of document to create version from")
    parser.add_argument("--reason", "-r", default="", help="Reason for new version")
    parser.add_argument(
        "--list", "-l", metavar="UUID", help="List all versions of document"
    )
    parser.add_argument("--project-root", type=Path, default=Path.cwd())

    args = parser.parse_args()

    if args.list:
        return list_versions(args.list, args.project_root)
    elif args.uuid:
        result = create_version(args.uuid, args.project_root, args.reason)
        return 0 if result else 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
