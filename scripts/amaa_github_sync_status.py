#!/usr/bin/env python3
"""
eaa_github_sync_status.py - Sync design document status with GitHub issue.

Reads the current status of a design document and updates the corresponding
GitHub issue labels. Optionally adds a status change comment.

Usage:
    # Sync status to linked issues
    python eaa_github_sync_status.py --uuid PROJ-SPEC-20250129-a1b2c3d4

    # Sync status to specific issue
    python eaa_github_sync_status.py --uuid PROJ-SPEC-... --issue 42

    # Sync with comment
    python eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment

    # Batch sync all documents with linked issues
    python eaa_github_sync_status.py --all

    # Dry run
    python eaa_github_sync_status.py --uuid PROJ-SPEC-... --dry-run

Dependencies: Python 3.8+, gh CLI (authenticated)
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, cast


STATUS_LABELS = {
    "draft": "status:draft",
    "review": "status:review",
    "approved": "status:approved",
    "implementing": "status:implementing",
    "implemented": "status:implemented",
    "completed": "status:completed",
    "deprecated": "status:deprecated",
    "superseded": "status:superseded",
    "archived": "status:archived",
}

STATUS_DESCRIPTIONS = {
    "draft": "Design is being drafted",
    "review": "Design is under review",
    "approved": "Design has been approved for implementation",
    "implementing": "Design is being implemented",
    "implemented": "Design implementation is complete",
    "completed": "Design lifecycle is complete",
    "deprecated": "Design has been deprecated",
    "superseded": "Design has been superseded by a newer version",
    "archived": "Design has been archived",
}


def check_gh_cli() -> bool:
    """Check if gh CLI is available and authenticated."""
    if not shutil.which("gh"):
        print(
            "ERROR: gh CLI not found. Install from https://cli.github.com/",
            file=sys.stderr,
        )
        return False

    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("ERROR: gh CLI not authenticated. Run: gh auth login", file=sys.stderr)
        return False

    return True


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


def extract_frontmatter(content: str) -> tuple[Optional[dict], str]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None, content

    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None, content

    frontmatter: dict = {}
    for line in lines[1:end_idx]:
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value.startswith("[") and value.endswith("]"):
                try:
                    value = json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    pass
            frontmatter[key] = value

    body = "\n".join(lines[end_idx + 1 :])
    return frontmatter, body


def find_document_by_uuid(uuid_str: str, design_root: Path) -> Optional[Path]:
    """Find document path by UUID."""
    if not design_root.exists():
        return None

    for md_file in design_root.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, _ = extract_frontmatter(content)
            if frontmatter and frontmatter.get("uuid") == uuid_str:
                return md_file
        except (OSError, UnicodeDecodeError):
            continue

    return None


def find_all_linked_documents(design_root: Path) -> list[tuple[Path, dict]]:
    """Find all documents with linked GitHub issues."""
    results: list[tuple[Path, dict]] = []

    if not design_root.exists():
        return results

    for md_file in design_root.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, _ = extract_frontmatter(content)
            if frontmatter:
                related_issues = frontmatter.get("related_issues", [])
                if isinstance(related_issues, str):
                    try:
                        related_issues = json.loads(related_issues.replace("'", '"'))
                    except json.JSONDecodeError:
                        related_issues = []
                if related_issues:
                    results.append((md_file, frontmatter))
        except (OSError, UnicodeDecodeError):
            continue

    return results


def extract_issue_numbers(frontmatter: dict) -> list[int]:
    """Extract issue numbers from frontmatter."""
    related_issues = frontmatter.get("related_issues", [])
    if isinstance(related_issues, str):
        try:
            related_issues = json.loads(related_issues.replace("'", '"'))
        except json.JSONDecodeError:
            related_issues = []

    issue_numbers = []
    for item in related_issues:
        if isinstance(item, int):
            issue_numbers.append(item)
        elif isinstance(item, str):
            match = re.search(r"#?(\d+)", item)
            if match:
                issue_numbers.append(int(match.group(1)))

    return issue_numbers


def get_issue_labels(issue_number: int) -> list[str]:
    """Get current labels on the issue."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_number), "--json", "labels"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    try:
        data = json.loads(result.stdout)
        return [label["name"] for label in data.get("labels", [])]
    except (json.JSONDecodeError, KeyError):
        return []


def sync_status_to_issue(
    issue_number: int,
    status: str,
    uuid_str: str,
    add_comment: bool = False,
    dry_run: bool = False,
) -> bool:
    """Sync design document status to GitHub issue labels."""
    current_labels = get_issue_labels(issue_number)
    if not current_labels and not dry_run:
        print(
            f"WARNING: Could not get labels for issue #{issue_number}", file=sys.stderr
        )

    labels_to_add = []
    labels_to_remove = []

    new_status_label = STATUS_LABELS.get(status)

    for old_status, old_label in STATUS_LABELS.items():
        if old_label in current_labels and old_status != status:
            labels_to_remove.append(old_label)

    if new_status_label and new_status_label not in current_labels:
        labels_to_add.append(new_status_label)

    if dry_run:
        print(f"DRY RUN - Issue #{issue_number}:")
        print(f"  Current status: {status}")
        if labels_to_add:
            print(f"  Would add labels: {', '.join(labels_to_add)}")
        if labels_to_remove:
            print(f"  Would remove labels: {', '.join(labels_to_remove)}")
        if add_comment:
            print("  Would add status change comment")
        return True

    if labels_to_add:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "edit",
                str(issue_number),
                "--add-label",
                ",".join(labels_to_add),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(
                f"ERROR: Failed to add labels to #{issue_number}: {result.stderr}",
                file=sys.stderr,
            )
            return False

    if labels_to_remove:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "edit",
                str(issue_number),
                "--remove-label",
                ",".join(labels_to_remove),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(
                f"WARNING: Failed to remove labels from #{issue_number}: {result.stderr}",
                file=sys.stderr,
            )

    if add_comment:
        status_desc = STATUS_DESCRIPTIONS.get(status, status)
        comment = f"""## Design Status Update

**Status**: `{status}`
**Description**: {status_desc}
**Design UUID**: `{uuid_str}`
**Updated**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---
*Synchronized from design document*"""

        result = subprocess.run(
            ["gh", "issue", "comment", str(issue_number), "--body", comment],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(
                f"WARNING: Failed to add comment to #{issue_number}: {result.stderr}",
                file=sys.stderr,
            )

    print(f"SYNCED: Issue #{issue_number} -> status:{status}")
    return True


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Sync design document status with GitHub issue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync status to linked issues
  python eaa_github_sync_status.py --uuid PROJ-SPEC-20250129-a1b2c3d4

  # Sync status to specific issue
  python eaa_github_sync_status.py --uuid PROJ-SPEC-... --issue 42

  # Sync with comment
  python eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment

  # Batch sync all documents
  python eaa_github_sync_status.py --all

  # Dry run
  python eaa_github_sync_status.py --uuid PROJ-SPEC-... --dry-run
        """,
    )

    parser.add_argument(
        "--uuid",
        "-u",
        help="Design document UUID",
    )
    parser.add_argument(
        "--issue",
        "-i",
        type=int,
        help="Specific GitHub issue number (overrides linked issues)",
    )
    parser.add_argument(
        "--comment",
        "-c",
        action="store_true",
        help="Add status change comment to issue",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Sync all documents with linked issues",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    args = parser.parse_args()

    if not args.uuid and not args.all:
        print("ERROR: Either --uuid or --all is required", file=sys.stderr)
        parser.print_help()
        return 1

    if not args.dry_run and not check_gh_cli():
        return 1

    config = load_config(args.project_root)
    design_root = args.project_root / config["design_root"]

    if args.all:
        documents = find_all_linked_documents(design_root)
        if not documents:
            print("No documents with linked issues found")
            return 0

        print(f"Found {len(documents)} documents with linked issues\n")

        success_count = 0
        for doc_path, frontmatter in documents:
            uuid_str = frontmatter.get("uuid", "Unknown")
            status = frontmatter.get("status", "draft")
            issue_numbers = extract_issue_numbers(frontmatter)

            print(f"Document: {uuid_str}")
            for issue_num in issue_numbers:
                if sync_status_to_issue(
                    issue_num, status, uuid_str, args.comment, args.dry_run
                ):
                    success_count += 1

        print(f"\nSynced {success_count} issue(s)")
        return 0

    target_doc_path = find_document_by_uuid(args.uuid, design_root)
    if not target_doc_path:
        print(f"ERROR: Document not found with UUID: {args.uuid}", file=sys.stderr)
        return 1

    content = target_doc_path.read_text(encoding="utf-8")
    frontmatter_raw, _ = extract_frontmatter(content)

    if not frontmatter_raw:
        print(f"ERROR: Document has no frontmatter: {target_doc_path}", file=sys.stderr)
        return 1

    frontmatter = cast(dict, frontmatter_raw)
    status = frontmatter.get("status", "draft")
    uuid_str = frontmatter.get("uuid", args.uuid)

    if args.issue:
        issue_numbers = [args.issue]
    else:
        issue_numbers = extract_issue_numbers(frontmatter)
        if not issue_numbers:
            print(
                "ERROR: Document has no linked issues. Use --issue to specify one.",
                file=sys.stderr,
            )
            return 1

    success = True
    for issue_num in issue_numbers:
        if not sync_status_to_issue(
            issue_num, status, uuid_str, args.comment, args.dry_run
        ):
            success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
