#!/usr/bin/env python3
"""
arch_design_export.py - Export design documents for GitHub.

Optionally sanitizes documents by removing internal references
and design-specific metadata. Uses arch_design_search.py to find documents.

Sanitization (when enabled with --sanitize) removes:
- Internal file references (keeps external URLs)
- Architect-specific HTML comments (<!-- ARCHITECT:... -->, <!-- INTERNAL:... -->)
- Private sections marked for internal use

Usage:
    # Export single document (no sanitization by default)
    python arch_design_export.py --uuid PROJ-SPEC-20250108-a7b3f2e1

    # Export to specific directory
    python arch_design_export.py --uuid PROJ-SPEC-... --output-dir exports/

    # Export with sanitization (removes internal markers)
    python arch_design_export.py --uuid PROJ-SPEC-... --sanitize

    # Export all documents of a type
    python arch_design_export.py --type SPEC --output-dir exports/

    # Generate GitHub issue body from spec
    python arch_design_export.py --uuid PROJ-SPEC-... --format issue

Dependencies: Python 3.8+, arch_design_search.py (same directory)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def run_search_script(args: list[str], project_root: Path) -> str:
    """Run arch_design_search.py with given arguments."""
    script_path = Path(__file__).parent / "arch_design_search.py"
    cmd = ["python3", str(script_path)] + args + ["--project-root", str(project_root)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def load_config(project_root: Path) -> dict[str, Path]:
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


def find_documents_by_type(doc_type: str, project_root: Path) -> list[Path]:
    """Find all documents of a type."""
    output = run_search_script(["--type", doc_type, "--output", "path"], project_root)
    if output and not output.startswith("No documents"):
        return [project_root / line for line in output.split("\n") if line]
    return []


def sanitize_content(content: str) -> str:
    """Remove internal markers and references from content."""
    # Remove Architect-internal HTML comments
    content = re.sub(r"<!-- ARCHITECT:.*?-->", "", content, flags=re.DOTALL)
    content = re.sub(r"<!-- INTERNAL:.*?-->", "", content, flags=re.DOTALL)
    content = re.sub(r"<!-- PRIVATE:.*?-->", "", content, flags=re.DOTALL)

    # Remove internal file references (keep external URLs)
    # [text](relative/path.md) -> text
    content = re.sub(r"\[([^\]]+)\]\((?!https?://|#)[^)]+\.md\)", r"\1", content)

    # Remove internal sections marked with INTERNAL_START/INTERNAL_END comments
    content = re.sub(
        r"<!-- INTERNAL_START -->.*?<!-- INTERNAL_END -->", "", content, flags=re.DOTALL
    )

    # Clean up multiple blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip()


def format_for_issue(content: str, uuid_str: str) -> str:
    """Format document as GitHub issue body."""
    # Parse frontmatter to extract title
    title = "Design Document"
    if match := re.search(r'^title:\s*"?([^"\n]+)"?', content, re.MULTILINE):
        title = match.group(1).strip()

    # Remove frontmatter for issue body
    body = re.sub(r"^---\n.*?^---\n", "", content, flags=re.MULTILINE | re.DOTALL)

    # Add header
    issue_body = f"""## {title}

**UUID**: `{uuid_str}`

---

{body.strip()}

---
*Exported from EAA design documents*
"""

    return issue_body


def export_document(
    uuid_str: str,
    project_root: Path,
    output_dir: Path | None = None,
    sanitize: bool = False,
    output_format: str = "markdown",
) -> Path | None:
    """Export a document.

    Returns path to exported file.
    """
    doc_path = find_document(uuid_str, project_root)
    if not doc_path or not doc_path.exists():
        print(f"ERROR: Document not found: {uuid_str}", file=sys.stderr)
        return None

    content = doc_path.read_text(encoding="utf-8")

    if sanitize:
        content = sanitize_content(content)

    if output_format == "issue":
        content = format_for_issue(content, uuid_str)

    # Determine output path
    if output_dir is None:
        config = load_config(project_root)
        output_dir = project_root / config["design_root"] / "exports"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    if output_format == "issue":
        export_filename = f"{uuid_str}-issue.md"
    else:
        export_filename = f"{uuid_str}.md"

    export_path = output_dir / export_filename
    export_path.write_text(content, encoding="utf-8")

    print(f"EXPORTED: {export_path}")

    return export_path


def export_batch(
    doc_type: str,
    project_root: Path,
    output_dir: Path,
    sanitize: bool = False,
) -> list[Path]:
    """Export all documents of a type.

    Returns list of exported paths.
    """
    doc_paths = find_documents_by_type(doc_type, project_root)

    if not doc_paths:
        print(f"No {doc_type} documents found")
        return []

    exported = []
    for doc_path in doc_paths:
        # Extract UUID from frontmatter
        content = doc_path.read_text(encoding="utf-8")
        match = re.search(r"^uuid:\s*(\S+)", content, re.MULTILINE)
        if not match:
            print(f"SKIP: No UUID in {doc_path}")
            continue

        uuid_str = match.group(1)
        result = export_document(uuid_str, project_root, output_dir, sanitize)
        if result:
            exported.append(result)

    print(f"\nExported {len(exported)} documents to {output_dir}")
    return exported


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Export design documents for GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export single document (preserves internal markers)
  python arch_design_export.py --uuid PROJ-SPEC-20250108-a7b3f2e1

  # Export to specific directory
  python arch_design_export.py --uuid PROJ-SPEC-... --output-dir exports/

  # Export as GitHub issue body
  python arch_design_export.py --uuid PROJ-SPEC-... --format issue

  # Export all specs
  python arch_design_export.py --type SPEC --output-dir exports/

  # Export with sanitization (removes internal markers)
  python arch_design_export.py --uuid PROJ-SPEC-... --sanitize
        """,
    )

    parser.add_argument("--uuid", "-u", help="UUID of document to export")
    parser.add_argument(
        "--type",
        "-t",
        choices=["SPEC", "PLAN", "ADR", "spec", "plan", "adr"],
        help="Export all documents of type",
    )
    parser.add_argument("--output-dir", "-o", type=Path, help="Output directory")
    parser.add_argument(
        "--sanitize",
        action="store_true",
        help="Remove internal references and design markers",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "issue"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument("--project-root", type=Path, default=Path.cwd())

    args = parser.parse_args()

    if args.uuid:
        result = export_document(
            args.uuid,
            args.project_root,
            args.output_dir,
            sanitize=args.sanitize,
            output_format=args.format,
        )
        return 0 if result else 1

    elif args.type:
        if not args.output_dir:
            print("ERROR: --output-dir required with --type", file=sys.stderr)
            return 1
        results = export_batch(
            args.type.upper(),
            args.project_root,
            args.output_dir,
            sanitize=args.sanitize,
        )
        return 0 if results else 1

    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
