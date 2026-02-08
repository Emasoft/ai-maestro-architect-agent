#!/usr/bin/env python3
"""
arch_design_lifecycle.py - Design document lifecycle management.

Handles status transitions and archiving of design documents.
Uses arch_design_search.py to find documents.

Lifecycle States:
    draft -> review -> approved -> implemented -> deprecated
                   |-> superseded (when replaced by newer version)

Usage:
    # Update status
    python arch_design_lifecycle.py status --uuid PROJ-SPEC-... --status approved

    # Archive a document
    python arch_design_lifecycle.py archive --uuid PROJ-SPEC-... --reason "Obsolete"

    # Supersede with new document
    python arch_design_lifecycle.py supersede --uuid OLD-UUID --by NEW-UUID

    # Show document history
    python arch_design_lifecycle.py history --uuid PROJ-SPEC-...

Dependencies: Python 3.8+, arch_design_search.py (same directory)
"""

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


VALID_STATUSES = {
    "draft",
    "review",
    "approved",
    "implemented",
    "deprecated",
    "superseded",
    "archived",
}

# Valid status transitions
VALID_TRANSITIONS = {
    "draft": {"review", "deprecated"},
    "review": {"draft", "approved", "deprecated"},
    "approved": {"implemented", "deprecated", "superseded"},
    "implemented": {"deprecated", "superseded"},
    "deprecated": set(),  # Terminal state
    "superseded": set(),  # Terminal state
    "archived": set(),  # Terminal state
}


def run_search_script(args: list[str], project_root: Path) -> str:
    """Run arch_design_search.py with given arguments."""
    script_path = Path(__file__).parent / "arch_design_search.py"
    cmd = ["python3", str(script_path)] + args + ["--project-root", str(project_root)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def load_config(project_root: Path) -> dict:
    """Load configuration from patterns.md."""
    config = {"design_root": Path("docs/design")}
    patterns_file = project_root / ".claude" / "architect" / "patterns.md"

    if not patterns_file.exists():
        patterns_file = project_root / ".design" / "memory" / "patterns.md"

    if patterns_file.exists():
        content = patterns_file.read_text(encoding="utf-8")
        if match := re.search(r"^design_root:\s*(\S+)", content, re.MULTILINE):
            config["design_root"] = Path(match.group(1).rstrip("/"))

    return config


def find_document(uuid_str: str, project_root: Path) -> Path | None:
    """Find document path by UUID."""
    output = run_search_script(["--uuid", uuid_str, "--output", "path"], project_root)
    if output and not output.startswith("No documents"):
        return project_root / output.split("\n")[0]
    return None


def get_document_status(file_path: Path) -> str | None:
    """Get current status of a document."""
    try:
        content = file_path.read_text(encoding="utf-8")
        if match := re.search(r"^status:\s*(\S+)", content, re.MULTILINE):
            return match.group(1).lower()
    except (OSError, UnicodeDecodeError):
        pass
    return None


def update_status(
    uuid_str: str, new_status: str, project_root: Path, force: bool = False
) -> bool:
    """Update document status.

    Returns True if successful.
    """
    new_status = new_status.lower()

    if new_status not in VALID_STATUSES:
        print(f"ERROR: Invalid status: {new_status}", file=sys.stderr)
        print(f"Valid statuses: {', '.join(sorted(VALID_STATUSES))}", file=sys.stderr)
        return False

    doc_path = find_document(uuid_str, project_root)
    if not doc_path or not doc_path.exists():
        print(f"ERROR: Document not found: {uuid_str}", file=sys.stderr)
        return False

    current_status = get_document_status(doc_path)
    if current_status:
        allowed = VALID_TRANSITIONS.get(current_status, set())
        if new_status not in allowed and not force:
            print(
                f"ERROR: Invalid transition: {current_status} -> {new_status}",
                file=sys.stderr,
            )
            allowed_str = ", ".join(allowed) or "none (terminal)"
            print(
                f"Allowed from '{current_status}': {allowed_str}",
                file=sys.stderr,
            )
            print("Use --force to override", file=sys.stderr)
            return False

    # Update file
    content = doc_path.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    content = re.sub(
        r"^status:\s*\S+", f"status: {new_status}", content, flags=re.MULTILINE
    )
    content = re.sub(
        r"^updated:\s*\S+", f"updated: {today}", content, flags=re.MULTILINE
    )

    doc_path.write_text(content, encoding="utf-8")

    print(f"UPDATED: {doc_path}")
    print(f"Status: {current_status or 'unknown'} -> {new_status}")

    return True


def archive_document(
    uuid_str: str,
    project_root: Path,
    reason: str = "",
    superseded_by: str | None = None,
) -> bool:
    """Archive a document by moving to archive directory.

    Returns True if successful.
    """
    config = load_config(project_root)
    design_root = project_root / config["design_root"]

    doc_path = find_document(uuid_str, project_root)
    if not doc_path or not doc_path.exists():
        print(f"ERROR: Document not found: {uuid_str}", file=sys.stderr)
        return False

    # Create archive directory
    archive_dir = design_root / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Update metadata
    content = doc_path.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    content = re.sub(r"^status:\s*\S+", "status: archived", content, flags=re.MULTILINE)
    content = re.sub(
        r"^updated:\s*\S+", f"updated: {today}", content, flags=re.MULTILINE
    )

    if superseded_by:
        content = re.sub(
            r"^superseded_by:\s*.*$",
            f'superseded_by: "{superseded_by}"',
            content,
            flags=re.MULTILINE,
        )

    # Write updated content
    doc_path.write_text(content, encoding="utf-8")

    # Move to archive
    archive_path = archive_dir / doc_path.name
    counter = 1
    while archive_path.exists():
        archive_path = archive_dir / f"{doc_path.stem}_{counter}.md"
        counter += 1

    shutil.move(str(doc_path), str(archive_path))

    print(f"ARCHIVED: {archive_path}")
    if reason:
        print(f"Reason: {reason}")
    if superseded_by:
        print(f"Superseded by: {superseded_by}")

    return True


def supersede_document(old_uuid: str, new_uuid: str, project_root: Path) -> bool:
    """Mark document as superseded by another.

    Updates both documents:
    - Old: status=superseded, superseded_by=new_uuid
    - New: supersedes=old_uuid

    Returns True if successful.
    """
    old_path = find_document(old_uuid, project_root)
    new_path = find_document(new_uuid, project_root)

    if not old_path or not old_path.exists():
        print(f"ERROR: Old document not found: {old_uuid}", file=sys.stderr)
        return False

    if not new_path or not new_path.exists():
        print(f"ERROR: New document not found: {new_uuid}", file=sys.stderr)
        return False

    today = datetime.now().strftime("%Y-%m-%d")

    # Update old document
    old_content = old_path.read_text(encoding="utf-8")
    old_content = re.sub(
        r"^status:\s*\S+", "status: superseded", old_content, flags=re.MULTILINE
    )
    old_content = re.sub(
        r"^updated:\s*\S+", f"updated: {today}", old_content, flags=re.MULTILINE
    )
    old_content = re.sub(
        r"^superseded_by:\s*.*$",
        f'superseded_by: "{new_uuid}"',
        old_content,
        flags=re.MULTILINE,
    )
    old_path.write_text(old_content, encoding="utf-8")

    # Update new document
    new_content = new_path.read_text(encoding="utf-8")
    new_content = re.sub(
        r"^supersedes:\s*.*$",
        f'supersedes: "{old_uuid}"',
        new_content,
        flags=re.MULTILINE,
    )
    new_content = re.sub(
        r"^updated:\s*\S+", f"updated: {today}", new_content, flags=re.MULTILINE
    )
    new_path.write_text(new_content, encoding="utf-8")

    print(f"SUPERSEDED: {old_uuid}")
    print(f"BY: {new_uuid}")

    return True


def show_history(uuid_str: str, project_root: Path) -> int:
    """Show version history of a document."""
    import json

    # Strip version suffix to get base
    base_uuid = re.sub(r"_v\d{4}$", "", uuid_str)

    output = run_search_script(
        ["--uuid-prefix", base_uuid, "--output", "json"], project_root
    )

    if not output or output.startswith("No documents"):
        print(f"No history found for: {uuid_str}")
        return 1

    try:
        docs = json.loads(output)
    except json.JSONDecodeError:
        print("ERROR: Failed to parse search results", file=sys.stderr)
        return 1

    print(f"\nHistory of {base_uuid}:\n")
    print(f"{'Version':<10} {'Status':<12} {'Updated':<12} {'UUID'}")
    print("-" * 90)

    for doc in sorted(docs, key=lambda d: d.get("uuid", "")):
        uuid_val = doc.get("uuid", "")
        match = re.search(r"_v(\d{4})$", uuid_val)
        version = match.group(1) if match else "base"
        status = doc.get("status", "unknown")
        updated = doc.get("updated", "unknown")
        print(f"{version:<10} {status:<12} {updated:<12} {uuid_val}")

        # Show supersession info
        if doc.get("superseded_by"):
            print(f"           └─ superseded by: {doc['superseded_by']}")
        if doc.get("supersedes"):
            print(f"           └─ supersedes: {doc['supersedes']}")

    print(f"\nTotal: {len(docs)} version(s)")
    return 0


def cmd_status(args) -> int:
    """Handle status command."""
    return (
        0 if update_status(args.uuid, args.status, args.project_root, args.force) else 1
    )


def cmd_archive(args) -> int:
    """Handle archive command."""
    return (
        0
        if archive_document(
            args.uuid, args.project_root, args.reason, args.superseded_by
        )
        else 1
    )


def cmd_supersede(args) -> int:
    """Handle supersede command."""
    return 0 if supersede_document(args.uuid, args.by, args.project_root) else 1


def cmd_history(args) -> int:
    """Handle history command."""
    return show_history(args.uuid, args.project_root)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Design document lifecycle management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Lifecycle States:
  draft -> review -> approved -> implemented -> deprecated
                 \\-> superseded

Examples:
  # Update status
  python arch_design_lifecycle.py status --uuid PROJ-SPEC-... --status approved

  # Archive
  python arch_design_lifecycle.py archive --uuid PROJ-SPEC-... --reason "Obsolete"

  # Supersede
  python arch_design_lifecycle.py supersede --uuid OLD-UUID --by NEW-UUID

  # Show history
  python arch_design_lifecycle.py history --uuid PROJ-SPEC-...
        """,
    )

    parser.add_argument("--project-root", type=Path, default=Path.cwd())

    subparsers = parser.add_subparsers(dest="command")

    # status command
    status_parser = subparsers.add_parser("status", help="Update document status")
    status_parser.add_argument("--uuid", "-u", required=True)
    status_parser.add_argument(
        "--status", "-s", required=True, choices=sorted(VALID_STATUSES)
    )
    status_parser.add_argument(
        "--force", "-f", action="store_true", help="Override transition rules"
    )

    # archive command
    archive_parser = subparsers.add_parser("archive", help="Archive a document")
    archive_parser.add_argument("--uuid", "-u", required=True)
    archive_parser.add_argument("--reason", "-r", default="")
    archive_parser.add_argument("--superseded-by", help="UUID of replacing document")

    # supersede command
    supersede_parser = subparsers.add_parser(
        "supersede", help="Mark document as superseded"
    )
    supersede_parser.add_argument(
        "--uuid", "-u", required=True, help="Old document UUID"
    )
    supersede_parser.add_argument("--by", "-b", required=True, help="New document UUID")

    # history command
    history_parser = subparsers.add_parser("history", help="Show document history")
    history_parser.add_argument("--uuid", "-u", required=True)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "status": cmd_status,
        "archive": cmd_archive,
        "supersede": cmd_supersede,
        "history": cmd_history,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
