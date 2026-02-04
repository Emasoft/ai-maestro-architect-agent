#!/usr/bin/env python3
"""
arch_design_search.py - Filesystem-based design document search (Manus principle).

This script searches design documents using the filesystem as the database,
following the Manus principle: "Use the filesystem as the DB and filenames as indexes."

NO INDEXING. NO SQLITE. Claude is extremely efficient at reading .md files directly,
making database indexing unnecessary and actually slower for typical design document
operations. The filesystem IS the database.

Search Strategies (in order of speed):
1. UUID search - O(1) direct file lookup via directory structure
2. Filename search - O(n) glob pattern matching
3. Frontmatter search - O(n) parse frontmatter only (fast)
4. Full-text search - O(n*m) search all content (slowest, use sparingly)

Directory Structure as Index:
    docs/design/
    ├── specs/      <- doc_type == SPEC
    ├── plans/      <- doc_type == PLAN
    ├── decisions/  <- doc_type == ADR
    └── exports/    <- sanitized exports for GitHub

Usage:
    python arch_design_search.py --uuid PROJ-SPEC-20250108-a7b3f2e1
    python arch_design_search.py --type SPEC --status draft
    python arch_design_search.py --text "JWT token" --output json

Dependencies: Python 3.8+ (uses pathlib only)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

# Add scripts directory to path for imports
_SCRIPT_DIR = Path(__file__).parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from eaa_design_search_parser import (  # noqa: E402
    DesignConfig,
    DocumentMetadata,
    extract_metadata,
    get_type_directory,
)

__all__ = [
    "search_by_uuid",
    "search_by_type",
    "search_by_status",
    "search_by_tag",
    "search_by_issue",
    "search_full_text",
    "filter_results",
    "format_output",
    "main",
]


def search_by_uuid(
    uuid_str: str,
    design_root: Path,
    exact: bool = True,
) -> list[DocumentMetadata]:
    """Search for document by UUID.

    FASTEST search - uses directory structure as index.
    If UUID contains type (e.g., PROJ-SPEC-...), searches only that type's directory.
    """
    results = []
    uuid_upper = uuid_str.upper()
    target_dirs = []

    if "-SPEC-" in uuid_upper:
        target_dirs = [design_root / "specs"]
    elif "-PLAN-" in uuid_upper:
        target_dirs = [design_root / "plans"]
    elif "-ADR-" in uuid_upper:
        target_dirs = [design_root / "decisions"]
    else:
        target_dirs = [
            design_root / "specs",
            design_root / "plans",
            design_root / "decisions",
            design_root,
        ]

    base_uuid = re.sub(r"_v\d{4}$", "", uuid_str)

    for target_dir in target_dirs:
        if not target_dir.exists():
            continue

        for md_file in target_dir.glob("*.md"):
            metadata = extract_metadata(md_file)
            if metadata and metadata.uuid:
                if exact:
                    if metadata.uuid == uuid_str:
                        results.append(metadata)
                else:
                    metadata_base = re.sub(r"_v\d{4}$", "", metadata.uuid)
                    if metadata_base == base_uuid:
                        results.append(metadata)

    return results


def search_by_type(doc_type: str, design_root: Path) -> list[DocumentMetadata]:
    """Search for documents by type. FAST - uses directory structure as index."""
    results = []
    type_dir = get_type_directory(doc_type)

    if type_dir:
        target_dir = design_root / type_dir
        if target_dir.exists():
            for md_file in target_dir.glob("*.md"):
                metadata = extract_metadata(md_file)
                if metadata:
                    results.append(metadata)
    else:
        for md_file in design_root.rglob("*.md"):
            metadata = extract_metadata(md_file)
            if metadata and metadata.doc_type.upper() == doc_type.upper():
                results.append(metadata)

    return results


def search_by_status(status: str, design_root: Path) -> list[DocumentMetadata]:
    """Search for documents by status. MEDIUM speed - parses frontmatter."""
    results = []
    status_lower = status.lower()

    for md_file in design_root.rglob("*.md"):
        metadata = extract_metadata(md_file)
        if metadata and metadata.status.lower() == status_lower:
            results.append(metadata)

    return results


def search_by_tag(tag: str, design_root: Path) -> list[DocumentMetadata]:
    """Search for documents by tag. MEDIUM speed - parses frontmatter."""
    results = []
    tag_lower = tag.lower()

    for md_file in design_root.rglob("*.md"):
        metadata = extract_metadata(md_file)
        if metadata:
            if any(t.lower() == tag_lower for t in metadata.tags):
                results.append(metadata)

    return results


def search_by_issue(issue: str, design_root: Path) -> list[DocumentMetadata]:
    """Search for documents related to a GitHub issue. MEDIUM speed."""
    results = []
    issue_normalized = issue.lstrip("#")

    for md_file in design_root.rglob("*.md"):
        metadata = extract_metadata(md_file)
        if metadata:
            for rel_issue in metadata.related_issues:
                if rel_issue.lstrip("#") == issue_normalized:
                    results.append(metadata)
                    break

    return results


def search_full_text(query: str, design_root: Path) -> list[DocumentMetadata]:
    """Full-text search across all documents. SLOWEST - reads entire files."""
    results = []
    query_lower = query.lower()

    for md_file in design_root.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8").lower()
            if query_lower in content:
                metadata = extract_metadata(md_file)
                if metadata:
                    results.append(metadata)
        except (OSError, UnicodeDecodeError):
            continue

    return results


def filter_results(
    results: list[DocumentMetadata],
    doc_type: Optional[str] = None,
    status: Optional[str] = None,
    tag: Optional[str] = None,
) -> list[DocumentMetadata]:
    """Filter results by additional criteria."""
    filtered = results

    if doc_type:
        filtered = [r for r in filtered if r.doc_type.upper() == doc_type.upper()]

    if status:
        filtered = [r for r in filtered if r.status.lower() == status.lower()]

    if tag:
        tag_lower = tag.lower()
        filtered = [r for r in filtered if any(t.lower() == tag_lower for t in r.tags)]

    return filtered


def format_output(
    results: list[DocumentMetadata],
    output_format: str,
    project_root: Path,
) -> str:
    """Format search results for output."""
    if output_format == "json":
        return json.dumps([r.to_dict() for r in results], indent=2)

    elif output_format == "path":
        return "\n".join(str(r.path.relative_to(project_root)) for r in results)

    elif output_format == "uuid":
        return "\n".join(r.uuid for r in results if r.uuid)

    elif output_format == "content":
        output_parts = []
        for r in results:
            try:
                content = r.path.read_text(encoding="utf-8")
                rel_path = r.path.relative_to(project_root)
                output_parts.append(f"--- FILE: {rel_path} ---\n{content}")
            except (OSError, UnicodeDecodeError):
                continue
        return "\n\n".join(output_parts)

    else:  # table format (default)
        if not results:
            return "No documents found."

        lines = [
            f"\n{'UUID':<45} {'Type':<6} {'Status':<12} {'Title'}",
            "-" * 100,
        ]
        for r in sorted(results, key=lambda x: x.uuid):
            title = r.title[:35] + "..." if len(r.title) > 38 else r.title
            lines.append(f"{r.uuid:<45} {r.doc_type:<6} {r.status:<12} {title}")
        lines.append(f"\nTotal: {len(results)} documents")
        return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Search Atlas design documents (filesystem as DB)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Search Speed (fastest to slowest):
  1. --uuid       : Direct lookup via directory structure
  2. --type       : Uses directory as index
  3. --status/tag : Parses frontmatter only
  4. --text       : Full file content search (slowest)

Examples:
  python arch_design_search.py --uuid PROJ-SPEC-20250108-a7b3f2e1
  python arch_design_search.py --type SPEC --status draft
  python arch_design_search.py --text "JWT token" --output json
        """,
    )

    parser.add_argument("--uuid", "-u", help="Search by exact UUID")
    parser.add_argument("--uuid-prefix", help="Search by UUID prefix (all versions)")
    parser.add_argument(
        "--type",
        "-t",
        choices=["SPEC", "PLAN", "ADR", "spec", "plan", "adr"],
        help="Filter by document type",
    )
    parser.add_argument(
        "--status",
        "-s",
        choices=["draft", "review", "approved", "superseded", "deprecated"],
        help="Filter by status",
    )
    parser.add_argument("--tag", help="Filter by tag")
    parser.add_argument("--issue", "-i", help="Find documents related to GitHub issue")
    parser.add_argument("--text", "-q", help="Full-text search (slowest)")
    parser.add_argument(
        "--output",
        "-o",
        choices=["table", "json", "path", "uuid", "content"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    args = parser.parse_args()
    config = DesignConfig.load(args.project_root)
    design_root = args.project_root / config.design_root

    if not design_root.exists():
        print(f"ERROR: Design root not found: {design_root}", file=sys.stderr)
        return 1

    results: list[DocumentMetadata] = []

    # Execute primary search (order by speed)
    if args.uuid:
        results = search_by_uuid(args.uuid, design_root, exact=True)
    elif args.uuid_prefix:
        results = search_by_uuid(args.uuid_prefix, design_root, exact=False)
    elif args.type and not args.status and not args.tag:
        results = search_by_type(args.type, design_root)
    elif args.status and not args.type and not args.tag:
        results = search_by_status(args.status, design_root)
    elif args.tag and not args.type and not args.status:
        results = search_by_tag(args.tag, design_root)
    elif args.issue:
        results = search_by_issue(args.issue, design_root)
    elif args.text:
        results = search_full_text(args.text, design_root)
        results = filter_results(results, args.type, args.status, args.tag)
    else:
        for md_file in design_root.rglob("*.md"):
            metadata = extract_metadata(md_file)
            if metadata:
                results.append(metadata)
        results = filter_results(results, args.type, args.status, args.tag)

    # Apply post-filters for combined searches
    if args.uuid or args.uuid_prefix:
        results = filter_results(results, args.type, args.status, args.tag)
    elif args.type and (args.status or args.tag):
        results = filter_results(results, None, args.status, args.tag)
    elif args.status and args.tag:
        results = filter_results(results, None, None, args.tag)

    print(format_output(results, args.output, args.project_root))
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
