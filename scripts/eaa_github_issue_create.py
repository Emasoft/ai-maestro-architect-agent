#!/usr/bin/env python3
"""
eaa_github_issue_create.py - Create GitHub issue from design document.

Reads a design document by UUID, extracts metadata from frontmatter,
and creates a corresponding GitHub issue using the gh CLI.
Updates the design document with the created issue number.

Usage:
    # Create issue from design document
    python eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4

    # Create issue with custom labels
    python eaa_github_issue_create.py --uuid PROJ-SPEC-... --labels "design,priority:high"

    # Dry run (show what would be created)
    python eaa_github_issue_create.py --uuid PROJ-SPEC-... --dry-run

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
        print("ERROR: gh CLI not found. Install from https://cli.github.com/", file=sys.stderr)
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
    """Extract YAML frontmatter from markdown content.

    Returns (frontmatter_dict, body_content).
    If no frontmatter, returns (None, content).
    """
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


def extract_issue_data(frontmatter: dict, body: str, doc_path: Path) -> dict:
    """Extract GitHub issue data from design document."""
    title = frontmatter.get("title", doc_path.stem.replace("-", " ").replace("_", " ").title())
    uuid_str = frontmatter.get("uuid", "")
    doc_type = frontmatter.get("type", "design").upper()
    status = frontmatter.get("status", "draft")

    description_parts = [
        f"## Design Document: {title}",
        f"",
        f"**UUID**: `{uuid_str}`",
        f"**Type**: {doc_type}",
        f"**Status**: {status}",
        f"**Created**: {frontmatter.get('created', 'Unknown')}",
        f"**Author**: {frontmatter.get('author', 'Unknown')}",
        f"",
        f"---",
        f"",
    ]

    overview_match = re.search(r"## 1\. Overview\s*\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
    if overview_match:
        overview = overview_match.group(1).strip()
        if len(overview) > 1000:
            overview = overview[:1000] + "..."
        description_parts.append("### Overview")
        description_parts.append("")
        description_parts.append(overview)
        description_parts.append("")

    description_parts.extend([
        "---",
        "",
        f"*This issue is linked to design document `{uuid_str}`*",
        "*Use `/eaa-sync-status` to synchronize status changes*",
    ])

    labels = ["design"]
    if doc_type:
        labels.append(f"design:{doc_type.lower()}")

    status_label_map = {
        "draft": "status:draft",
        "review": "status:review",
        "approved": "status:approved",
        "implementing": "status:implementing",
        "completed": "status:completed",
    }
    if status in status_label_map:
        labels.append(status_label_map[status])

    if "tags" in frontmatter and isinstance(frontmatter["tags"], list):
        for tag in frontmatter["tags"]:
            if isinstance(tag, str) and len(tag) < 50:
                labels.append(tag)

    return {
        "title": f"[{doc_type}] {title}",
        "body": "\n".join(description_parts),
        "labels": labels,
    }


def create_github_issue(issue_data: dict, dry_run: bool = False) -> Optional[int]:
    """Create GitHub issue using gh CLI.

    Returns issue number if successful, None otherwise.
    """
    if dry_run:
        print("DRY RUN - Would create issue:")
        print(f"  Title: {issue_data['title']}")
        print(f"  Labels: {', '.join(issue_data['labels'])}")
        print(f"  Body preview: {issue_data['body'][:200]}...")
        return None

    cmd = [
        "gh", "issue", "create",
        "--title", issue_data["title"],
        "--body", issue_data["body"],
    ]

    for label in issue_data["labels"]:
        cmd.extend(["--label", label])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: Failed to create issue: {result.stderr}", file=sys.stderr)
        return None

    issue_url = result.stdout.strip()
    print(f"CREATED: {issue_url}")

    match = re.search(r"/issues/(\d+)$", issue_url)
    if match:
        return int(match.group(1))

    return None


def update_document_with_issue(doc_path: Path, issue_number: int) -> bool:
    """Update design document frontmatter with GitHub issue number."""
    try:
        content = doc_path.read_text(encoding="utf-8")
        frontmatter, body = extract_frontmatter(content)

        if not frontmatter:
            print(f"ERROR: No frontmatter in {doc_path}", file=sys.stderr)
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
                new_frontmatter_lines.append(f"related_issues: {json.dumps(related_issues)}")
                found_related_issues = True
            elif line.startswith("updated:"):
                new_frontmatter_lines.append(f"updated: {today}")
                found_updated = True
            else:
                new_frontmatter_lines.append(line)

        if not found_related_issues:
            new_frontmatter_lines.insert(-1, f"related_issues: {json.dumps(related_issues)}")
        if not found_updated:
            new_frontmatter_lines.insert(-1, f"updated: {today}")

        new_frontmatter_lines.append("---")
        new_content = "\n".join(new_frontmatter_lines) + "\n" + body

        doc_path.write_text(new_content, encoding="utf-8")
        print(f"UPDATED: {doc_path} with issue #{issue_number}")
        return True

    except (OSError, UnicodeDecodeError) as e:
        print(f"ERROR: Failed to update document: {e}", file=sys.stderr)
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create GitHub issue from design document",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create issue from design document
  python eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4

  # Create issue with custom labels
  python eaa_github_issue_create.py --uuid PROJ-SPEC-... --labels "priority:high"

  # Dry run
  python eaa_github_issue_create.py --uuid PROJ-SPEC-... --dry-run
        """,
    )

    parser.add_argument(
        "--uuid",
        "-u",
        required=True,
        help="Design document UUID",
    )
    parser.add_argument(
        "--labels",
        "-l",
        help="Additional labels (comma-separated)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without creating",
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

    content = doc_path.read_text(encoding="utf-8")
    frontmatter, body = extract_frontmatter(content)

    if not frontmatter:
        print(f"ERROR: Document has no frontmatter: {doc_path}", file=sys.stderr)
        return 1

    if not frontmatter.get("uuid"):
        print(f"ERROR: Document has no UUID in frontmatter: {doc_path}", file=sys.stderr)
        return 1

    related_issues = frontmatter.get("related_issues", [])
    if isinstance(related_issues, list) and len(related_issues) > 0:
        print(f"WARNING: Document already linked to issues: {related_issues}", file=sys.stderr)
        print("Use --force to create another issue (not implemented)", file=sys.stderr)

    issue_data = extract_issue_data(frontmatter, body, doc_path)

    if args.labels:
        extra_labels = [label.strip() for label in args.labels.split(",")]
        issue_data["labels"].extend(extra_labels)

    issue_number = create_github_issue(issue_data, dry_run=args.dry_run)

    if issue_number and not args.dry_run:
        update_document_with_issue(doc_path, issue_number)

    return 0


if __name__ == "__main__":
    sys.exit(main())
