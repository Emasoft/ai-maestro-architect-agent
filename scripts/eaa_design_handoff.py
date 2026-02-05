#!/usr/bin/env python3
"""
arch_design_handoff.py - Export design documents to GitHub issue attachments.

This script exports a design document to a GitHub issue attachment.
Works identically in both single-git and dual-git modes.

NO external dependencies - Python 3.8+ stdlib only.

Usage:
    arch_design_handoff.py <uuid_or_file> <issue_number> [options]

Arguments:
    uuid_or_file    Document UUID (e.g., PROJ-SPEC-20250108-0001) or file path
    issue_number    GitHub issue number (e.g., 234)

Options:
    --sanitize      Remove INTERNAL and SENSITIVE sections before export
    --dry-run       Show what would be done without executing
    -h, --help      Show this help

Examples:
    arch_design_handoff.py PROJ-SPEC-20250108-0001 234
    arch_design_handoff.py PROJ-SPEC-20250108-0001 234 --sanitize
    arch_design_handoff.py docs/design/specs/auth.md 234 --sanitize

The script:
1. Finds the document by UUID or path
2. Optionally sanitizes (removes INTERNAL/SENSITIVE sections)
3. Creates an export copy in ${design_root}/exports/
4. Attaches content to GitHub issue as a comment
5. Updates the source document's frontmatter with related issue
6. Commits the export to appropriate git

Exit codes:
    0 - Success
    1 - Error (document not found, invalid arguments, etc.)
    2 - GitHub CLI not available or not authenticated
"""

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple


def detect_config() -> Tuple[str, str, str]:
    """Detect design configuration from patterns.md or auto-detect.

    Returns:
        Tuple of (design_root, mode, exports_dir)
    """
    patterns_file = Path("design/memory/patterns.md")
    design_root = ""
    mode = ""

    if patterns_file.exists():
        try:
            content = patterns_file.read_text(encoding="utf-8")
            for line in content.splitlines():
                if line.startswith("design_root:"):
                    design_root = line.split(":", 1)[1].strip().strip('"')
                elif line.startswith("mode:"):
                    mode = line.split(":", 1)[1].strip().strip('"')
        except OSError:
            pass

    # Fallback: auto-detect
    if not design_root:
        if Path(".design").is_dir():
            design_root = ".design"
            mode = "dual-git"
        elif Path("docs/design").is_dir():
            design_root = "docs/design"
            mode = "single-git"
        else:
            print("ERROR: No design directory found.", file=sys.stderr)
            sys.exit(1)
    else:
        if design_root in [".design/", ".design"]:
            mode = mode or "dual-git"
        else:
            mode = mode or "single-git"

    design_root = design_root.rstrip("/")
    exports_dir = f"{design_root}/exports"

    return design_root, mode, exports_dir


def find_document(identifier: str, design_root: str) -> str:
    """Find document by UUID or direct path.

    Args:
        identifier: Document UUID or file path
        design_root: Root directory for design documents

    Returns:
        Path to found document or empty string if not found
    """
    # If it's a path and exists, use directly
    if Path(identifier).is_file():
        return identifier

    # Search by UUID in all design directories
    for subdir in ["specs", "plans", "decisions"]:
        search_dir = Path(design_root) / subdir
        if search_dir.is_dir():
            for md_file in search_dir.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding="utf-8")
                    # Check if UUID matches in frontmatter
                    if re.search(
                        rf"^uuid:.*{re.escape(identifier)}", content, re.MULTILINE
                    ):
                        return str(md_file)
                except OSError:
                    continue

    return ""


def sanitize_document(source: Path, target: Path) -> None:
    """Sanitize document by removing INTERNAL and SENSITIVE sections.

    Args:
        source: Source document path
        target: Target document path
    """
    try:
        content = source.read_text(encoding="utf-8")
    except OSError as e:
        print(f"ERROR: Cannot read source file: {e}", file=sys.stderr)
        sys.exit(1)

    # Remove INTERNAL sections: <!-- INTERNAL --> ... <!-- /INTERNAL -->
    content = re.sub(
        r"<!-- INTERNAL -->.*?<!-- /INTERNAL -->", "", content, flags=re.DOTALL
    )

    # Remove SENSITIVE sections: <!-- SENSITIVE --> ... <!-- /SENSITIVE -->
    content = re.sub(
        r"<!-- SENSITIVE -->.*?<!-- /SENSITIVE -->", "", content, flags=re.DOTALL
    )

    try:
        target.write_text(content, encoding="utf-8")
        print("Sanitized: Removed INTERNAL and SENSITIVE sections")
    except OSError as e:
        print(f"ERROR: Cannot write sanitized file: {e}", file=sys.stderr)
        sys.exit(1)


def extract_frontmatter(file_path: Path, field: str) -> str:
    """Extract a field value from YAML frontmatter.

    Args:
        file_path: Path to markdown file
        field: Field name to extract (e.g., 'uuid', 'title')

    Returns:
        Field value or empty string if not found
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        # Extract frontmatter between --- delimiters
        match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
        if match:
            frontmatter = match.group(1)
            # Find the field (handles multi-word values)
            field_match = re.search(rf"^{field}:\s*(.+?)$", frontmatter, re.MULTILINE)
            if field_match:
                return field_match.group(1).strip().strip('"')
    except OSError:
        pass
    return ""


def attach_to_issue(file_path: Path, issue: str, mode: str, dry_run: bool) -> None:
    """Attach document to GitHub issue as a comment.

    Args:
        file_path: Path to export file
        issue: GitHub issue number
        mode: Git mode (single-git or dual-git)
        dry_run: If True, only show what would be done
    """
    # Extract document info
    uuid = extract_frontmatter(file_path, "uuid")
    title = extract_frontmatter(file_path, "title")
    doc_type = extract_frontmatter(file_path, "type")
    status = extract_frontmatter(file_path, "status")

    # Read file content
    try:
        file_content = file_path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"ERROR: Cannot read export file: {e}", file=sys.stderr)
        sys.exit(1)

    # Create comment body
    comment = f"""## Specification Attached

**UUID**: `{uuid}`
**Title**: {title}
**Type**: {doc_type}
**Status**: {status}
**Attached by**: Architect Agent
**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Mode**: {mode}

<details>
<summary>Click to expand specification</summary>

```markdown
{file_content}
```

</details>

---
*Exported via arch_design_handoff.py*"""

    if dry_run:
        print()
        print("=== DRY RUN: Would post to issue #" + issue + " ===")
        print("\n".join(comment.splitlines()[:20]))
        print("...")
        print("=== END DRY RUN ===")
        return

    # Check gh is available
    try:
        subprocess.run(
            ["gh", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: GitHub CLI (gh) not installed", file=sys.stderr)
        print("Install: https://cli.github.com/", file=sys.stderr)
        sys.exit(2)

    # Check authentication
    try:
        subprocess.run(
            ["gh", "auth", "status"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        print("ERROR: Not authenticated to GitHub", file=sys.stderr)
        print("Run: gh auth login", file=sys.stderr)
        sys.exit(2)

    # Post comment
    try:
        subprocess.run(
            ["gh", "issue", "comment", issue, "--body", comment],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to post comment: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    # Add label (ignore if fails)
    try:
        subprocess.run(
            ["gh", "issue", "edit", issue, "--add-label", "spec-attached"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        pass

    print(f"Attached to issue #{issue}")


def update_frontmatter(file_path: Path, issue: str, dry_run: bool) -> None:
    """Update source document frontmatter with related issue.

    Args:
        file_path: Path to source document
        issue: GitHub issue number
        dry_run: If True, only show what would be done
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"ERROR: Cannot read source file: {e}", file=sys.stderr)
        sys.exit(1)

    # Check if issue already in related_issues
    if re.search(rf"related_issues:.*#?{issue}", content):
        print(f"Issue #{issue} already in frontmatter")
        return

    if dry_run:
        print(f"DRY RUN: Would add issue #{issue} to frontmatter")
        return

    # Try to add to existing related_issues array
    if re.search(r"^related_issues:\s*\[", content, re.MULTILINE):
        # Add to existing array
        content = re.sub(
            r"(^related_issues:\s*\[)",
            rf'\1"#{issue}", ',
            content,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        # Add new related_issues field after uuid line
        content = re.sub(
            r"(^uuid:.*$)",
            rf'\1\nrelated_issues: ["#{issue}"]',
            content,
            count=1,
            flags=re.MULTILINE,
        )

    try:
        file_path.write_text(content, encoding="utf-8")
        print(f"Updated frontmatter with issue #{issue}")
    except OSError as e:
        print(f"ERROR: Cannot update frontmatter: {e}", file=sys.stderr)
        sys.exit(1)


def commit_export(
    export_file: Path, uuid: str, issue: str, mode: str, design_root: str, dry_run: bool
) -> None:
    """Commit export to appropriate git repository.

    Args:
        export_file: Path to export file
        uuid: Document UUID
        issue: GitHub issue number
        mode: Git mode (single-git or dual-git)
        design_root: Design root directory
        dry_run: If True, only show what would be done
    """
    if dry_run:
        print("DRY RUN: Would commit export to git")
        return

    commit_msg = f"""[EXPORT] Handoff {uuid} to issue #{issue}

## WHAT Changed
- ADDED: {export_file} (exported copy)

## WHY Changed
Exported design document for attachment to GitHub issue #{issue}.
Enables implementers to access specification via issue tracker.
"""

    try:
        if mode == "dual-git":
            # Commit to design git
            subprocess.run(
                ["git", "add", "exports/"],
                cwd=design_root,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=design_root,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print("No changes to commit in design git")
        else:
            # Commit to project git
            subprocess.run(
                ["git", "add", str(export_file)],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg], capture_output=True, text=True
            )
            if result.returncode != 0:
                print("No changes to commit")
    except subprocess.CalledProcessError:
        print("Git commit failed (non-fatal)")


def main() -> int:
    """Main entry point for design handoff script.

    Returns:
        Exit code: 0 for success, 1 for error, 2 for GitHub CLI issues
    """
    parser = argparse.ArgumentParser(
        description="Export design documents to GitHub issue attachments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  arch_design_handoff.py PROJ-SPEC-20250108-0001 234
  arch_design_handoff.py PROJ-SPEC-20250108-0001 234 --sanitize
  arch_design_handoff.py docs/design/specs/auth.md 234 --sanitize
        """,
    )
    parser.add_argument(
        "uuid_or_file",
        help="Document UUID (e.g., PROJ-SPEC-20250108-0001) or file path",
    )
    parser.add_argument("issue_number", help="GitHub issue number (e.g., 234)")
    parser.add_argument(
        "--sanitize",
        action="store_true",
        help="Remove INTERNAL and SENSITIVE sections before export",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing",
    )

    args = parser.parse_args()

    # Validate issue number
    if not args.issue_number.isdigit():
        print(
            f"ERROR: Issue number must be numeric: {args.issue_number}", file=sys.stderr
        )
        return 1

    # Detect configuration
    design_root, mode, exports_dir = detect_config()

    # Find document
    source = find_document(args.uuid_or_file, design_root)
    if not source:
        print(f"ERROR: Document not found: {args.uuid_or_file}", file=sys.stderr)
        print(
            f"\nSearched in: {design_root}/{{specs,plans,decisions}}/", file=sys.stderr
        )
        return 1

    source_path = Path(source)

    # Extract UUID from source
    source_uuid = extract_frontmatter(source_path, "uuid")

    print("=== Design Document Handoff ===")
    print(f"Mode: {mode}")
    print(f"Source: {source}")
    print(f"UUID: {source_uuid}")
    print(f"Target: GitHub Issue #{args.issue_number}")
    print(f"Sanitize: {args.sanitize}")
    if args.dry_run:
        print("*** DRY RUN MODE ***")
    print()

    # Prepare export directory
    exports_path = Path(exports_dir)
    exports_path.mkdir(parents=True, exist_ok=True)

    # Prepare export file
    basename = source_path.stem
    export_file = exports_path / f"{basename}-export.md"

    # Copy or sanitize
    if args.sanitize:
        sanitize_document(source_path, export_file)
    else:
        try:
            shutil.copy2(source_path, export_file)
            print("Copied to export (no sanitization)")
        except OSError as e:
            print(f"ERROR: Cannot copy file: {e}", file=sys.stderr)
            return 1

    # Attach to GitHub issue
    attach_to_issue(export_file, args.issue_number, mode, args.dry_run)

    # Update source frontmatter
    update_frontmatter(source_path, args.issue_number, args.dry_run)

    # Commit export
    commit_export(
        export_file, source_uuid, args.issue_number, mode, design_root, args.dry_run
    )

    print()
    print("=== Handoff Complete ===")
    print(f"Document: {source_uuid}")
    print(f"Issue: #{args.issue_number}")
    print(f"Export: {export_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
