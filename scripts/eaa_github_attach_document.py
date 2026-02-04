#!/usr/bin/env python3
"""
eaa_github_attach_document.py - Attach design document to existing GitHub issue.

Takes a design document UUID and an existing GitHub issue number,
posts the document content as a comment, and updates issue labels.

Usage:
    # Attach design document to issue
    python eaa_github_attach_document.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --issue 42

    # Attach with custom comment header
    python eaa_github_attach_document.py --uuid PROJ-SPEC-... --issue 42 --header "Updated design"

    # Dry run
    python eaa_github_attach_document.py --uuid PROJ-SPEC-... --issue 42 --dry-run

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
from typing import Optional


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


def verify_issue_exists(issue_number: int) -> bool:
    """Verify that the GitHub issue exists."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_number), "--json", "number"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


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


def format_document_comment(frontmatter: dict, body: str, header: str) -> str:
    """Format design document content as GitHub comment."""
    uuid_str = frontmatter.get("uuid", "Unknown")
    title = frontmatter.get("title", "Untitled")
    doc_type = frontmatter.get("type", "design").upper()
    status = frontmatter.get("status", "draft")
    created = frontmatter.get("created", "Unknown")
    author = frontmatter.get("author", "Unknown")

    comment_parts = [
        f"## {header}",
        "",
        f"### {title}",
        "",
        "| Property | Value |",
        "|----------|-------|",
        f"| **UUID** | `{uuid_str}` |",
        f"| **Type** | {doc_type} |",
        f"| **Status** | {status} |",
        f"| **Created** | {created} |",
        f"| **Author** | {author} |",
        "",
        "---",
        "",
    ]

    body_content = body.strip()
    if len(body_content) > 5000:
        body_content = (
            body_content[:5000] + "\n\n... *[Content truncated - see full document]*"
        )

    comment_parts.append("<details>")
    comment_parts.append("<summary>Full Design Document Content</summary>")
    comment_parts.append("")
    comment_parts.append(body_content)
    comment_parts.append("")
    comment_parts.append("</details>")
    comment_parts.append("")
    comment_parts.append("---")
    comment_parts.append(
        f"*Attached from design document `{uuid_str}` on {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
    )

    return "\n".join(comment_parts)


def add_comment_to_issue(
    issue_number: int, comment: str, dry_run: bool = False
) -> bool:
    """Add comment to GitHub issue."""
    if dry_run:
        print("DRY RUN - Would add comment to issue:")
        print(f"  Issue: #{issue_number}")
        print(f"  Comment preview: {comment[:300]}...")
        return True

    result = subprocess.run(
        ["gh", "issue", "comment", str(issue_number), "--body", comment],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"ERROR: Failed to add comment: {result.stderr}", file=sys.stderr)
        return False

    print(f"COMMENTED: Added design document to issue #{issue_number}")
    return True


def update_issue_labels(
    issue_number: int, frontmatter: dict, dry_run: bool = False
) -> bool:
    """Update issue labels based on design document status."""
    status = frontmatter.get("status", "draft")
    doc_type = frontmatter.get("type", "design").lower()

    current_labels = get_issue_labels(issue_number)

    labels_to_add = []
    labels_to_remove = []

    if "design" not in current_labels:
        labels_to_add.append("design")

    type_label = f"design:{doc_type}"
    if type_label not in current_labels:
        labels_to_add.append(type_label)

    status_labels = {
        "draft": "status:draft",
        "review": "status:review",
        "approved": "status:approved",
        "implementing": "status:implementing",
        "completed": "status:completed",
        "deprecated": "status:deprecated",
        "superseded": "status:superseded",
    }

    new_status_label = status_labels.get(status)

    for old_status, old_label in status_labels.items():
        if old_label in current_labels and old_status != status:
            labels_to_remove.append(old_label)

    if new_status_label and new_status_label not in current_labels:
        labels_to_add.append(new_status_label)

    if dry_run:
        if labels_to_add or labels_to_remove:
            print("DRY RUN - Would update labels:")
            if labels_to_add:
                print(f"  Add: {', '.join(labels_to_add)}")
            if labels_to_remove:
                print(f"  Remove: {', '.join(labels_to_remove)}")
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
            print(f"WARNING: Failed to add labels: {result.stderr}", file=sys.stderr)

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
            print(f"WARNING: Failed to remove labels: {result.stderr}", file=sys.stderr)

    if labels_to_add or labels_to_remove:
        print(f"LABELS: Updated issue #{issue_number} labels")

    return True


def update_document_with_issue(doc_path: Path, issue_number: int) -> bool:
    """Update design document frontmatter with GitHub issue number."""
    try:
        content = doc_path.read_text(encoding="utf-8")
        frontmatter, body = extract_frontmatter(content)

        if not frontmatter:
            return False

        today = datetime.now().strftime("%Y-%m-%d")

        related_issues = frontmatter.get("related_issues", [])
        if isinstance(related_issues, str):
            try:
                related_issues = json.loads(related_issues.replace("'", '"'))
            except json.JSONDecodeError:
                related_issues = []

        issue_str = f"#{issue_number}"
        if issue_str not in related_issues and issue_number not in related_issues:
            related_issues.append(issue_str)

            lines = content.split("\n")
            end_idx = None
            for i, line in enumerate(lines[1:], start=1):
                if line.strip() == "---":
                    end_idx = i
                    break

            new_frontmatter_lines = ["---"]
            found_related_issues = False
            found_updated = False

            for line in lines[1:end_idx]:
                if line.startswith("related_issues:"):
                    new_frontmatter_lines.append(
                        f"related_issues: {json.dumps(related_issues)}"
                    )
                    found_related_issues = True
                elif line.startswith("updated:"):
                    new_frontmatter_lines.append(f"updated: {today}")
                    found_updated = True
                else:
                    new_frontmatter_lines.append(line)

            if not found_related_issues:
                new_frontmatter_lines.insert(
                    -1, f"related_issues: {json.dumps(related_issues)}"
                )
            if not found_updated:
                new_frontmatter_lines.insert(-1, f"updated: {today}")

            new_frontmatter_lines.append("---")
            new_content = "\n".join(new_frontmatter_lines) + "\n" + body

            doc_path.write_text(new_content, encoding="utf-8")
            print(f"LINKED: {doc_path} -> issue #{issue_number}")

        return True

    except (OSError, UnicodeDecodeError) as e:
        print(f"ERROR: Failed to update document: {e}", file=sys.stderr)
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Attach design document to existing GitHub issue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Attach design document to issue
  python eaa_github_attach_document.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --issue 42

  # Attach with custom header
  python eaa_github_attach_document.py --uuid PROJ-SPEC-... --issue 42 --header "Updated design"

  # Dry run
  python eaa_github_attach_document.py --uuid PROJ-SPEC-... --issue 42 --dry-run
        """,
    )

    parser.add_argument(
        "--uuid",
        "-u",
        required=True,
        help="Design document UUID",
    )
    parser.add_argument(
        "--issue",
        "-i",
        type=int,
        required=True,
        help="GitHub issue number",
    )
    parser.add_argument(
        "--header",
        default="Design Document Attached",
        help="Comment header text (default: 'Design Document Attached')",
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

    if not args.dry_run and not check_gh_cli():
        return 1

    config = load_config(args.project_root)
    design_root = args.project_root / config["design_root"]

    doc_path = find_document_by_uuid(args.uuid, design_root)
    if not doc_path:
        print(f"ERROR: Document not found with UUID: {args.uuid}", file=sys.stderr)
        return 1

    if not args.dry_run and not verify_issue_exists(args.issue):
        print(f"ERROR: Issue #{args.issue} not found", file=sys.stderr)
        return 1

    content = doc_path.read_text(encoding="utf-8")
    frontmatter, body = extract_frontmatter(content)

    if not frontmatter:
        print(f"ERROR: Document has no frontmatter: {doc_path}", file=sys.stderr)
        return 1

    comment = format_document_comment(frontmatter, body, args.header)

    if not add_comment_to_issue(args.issue, comment, dry_run=args.dry_run):
        return 1

    update_issue_labels(args.issue, frontmatter, dry_run=args.dry_run)

    if not args.dry_run:
        update_document_with_issue(doc_path, args.issue)

    return 0


if __name__ == "__main__":
    sys.exit(main())
