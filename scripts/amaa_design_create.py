#!/usr/bin/env python3
"""
eaa_design_create.py - Create new design documents from templates.

Creates a new design document with proper GUUID-based filename, populated
YAML frontmatter, and template body sections. Documents are placed in the
correct subdirectory under design/<type>/.

UUID Format: GUUID-YYYYMMDD-NNNN
- GUUID: Fixed prefix for design document UUIDs
- YYYYMMDD: Date of document creation (8 digits)
- NNNN: Sequence number for that day (4 digits, zero-padded, starts at 0001)

Usage:
    # Create a PDR document
    python scripts/eaa_design_create.py --type pdr --title "User Auth Design"

    # Create with author
    python scripts/eaa_design_create.py --type feature --title "OAuth" --author "John"

    # Create with custom filename
    python scripts/eaa_design_create.py --type decision --title "DB Selection" --filename "adr-001-db"

    # Specify project root
    python scripts/eaa_design_create.py --type spec --title "API v2" --project-root /path/to/project

Dependencies: Python 3.8+ (stdlib only, no external packages)
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# Valid document types as defined in the SKILL.md specification
VALID_TYPES = ("pdr", "spec", "feature", "decision", "architecture", "template")

# GUUID regex pattern for parsing existing UUIDs in filenames and frontmatter
GUUID_PATTERN = re.compile(r"GUUID-(\d{8})-(\d{4})")


def slugify(title: str) -> str:
    """Convert a title string into a URL-friendly slug.

    Replaces spaces and non-alphanumeric characters with hyphens,
    lowercases everything, and strips leading/trailing hyphens.

    Args:
        title: The human-readable title to slugify.

    Returns:
        A lowercase hyphen-separated slug string.

    Examples:
        >>> slugify("User Authentication Redesign")
        'user-authentication-redesign'
        >>> slugify("REST API v2.0 Spec!")
        'rest-api-v2-0-spec'
    """
    # Replace non-alphanumeric characters (except hyphens) with hyphens
    slug = re.sub(r"[^a-zA-Z0-9-]", "-", title.lower())
    # Collapse multiple hyphens into one
    slug = re.sub(r"-+", "-", slug)
    # Strip leading and trailing hyphens
    slug = slug.strip("-")
    return slug


def find_next_sequence(design_type_dir: Path, today_str: str) -> int:
    """Find the next available sequence number for today's date.

    Scans all .md files in the given directory for GUUID patterns matching
    today's date, finds the highest sequence number, and returns the next one.

    Args:
        design_type_dir: The design/<type>/ directory to scan.
        today_str: Today's date as YYYYMMDD string.

    Returns:
        The next available sequence number (starting from 1).
    """
    max_seq = 0

    if design_type_dir.exists():
        for md_file in design_type_dir.glob("*.md"):
            # Check filename for GUUID pattern
            match = GUUID_PATTERN.search(md_file.name)
            if match and match.group(1) == today_str:
                seq = int(match.group(2))
                if seq > max_seq:
                    max_seq = seq

            # Also check frontmatter uuid field inside the file
            try:
                content = md_file.read_text(encoding="utf-8")
                for fm_match in GUUID_PATTERN.finditer(content):
                    if fm_match.group(1) == today_str:
                        seq = int(fm_match.group(2))
                        if seq > max_seq:
                            max_seq = seq
            except (OSError, UnicodeDecodeError):
                pass

    return max_seq + 1


def generate_guuid(design_type_dir: Path) -> str:
    """Generate a new GUUID for a design document.

    Format: GUUID-YYYYMMDD-NNNN where NNNN auto-increments based on
    existing documents for today's date.

    Args:
        design_type_dir: The directory to scan for existing GUUIDs.

    Returns:
        A new GUUID string (e.g., 'GUUID-20260130-0001').
    """
    today_str = datetime.now().strftime("%Y%m%d")
    seq = find_next_sequence(design_type_dir, today_str)
    return f"GUUID-{today_str}-{seq:04d}"


def load_template(doc_type: str, design_root: Path) -> Optional[str]:
    """Load a document template from the templates directory if it exists.

    Looks for a file at design/templates/<type>-template.md and returns
    its content if found.

    Args:
        doc_type: The document type (e.g., 'pdr', 'spec').
        design_root: The design/ root directory.

    Returns:
        Template content as string, or None if template file not found.
    """
    template_path = design_root / "templates" / f"{doc_type}-template.md"
    if template_path.exists():
        try:
            return template_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass
    return None


def get_default_template(title: str) -> str:
    """Return the default document body template.

    This template is used when no type-specific template file exists
    in design/templates/.

    Args:
        title: The document title for the H1 heading.

    Returns:
        A markdown string with the default template sections.
    """
    return f"""# {title}

## Overview
[Describe the purpose and scope of this design]

## Background
[Provide context and background information]

## Requirements
[List the requirements this design addresses]

## Proposed Design
[Describe the proposed design in detail]

## Alternatives Considered
[Document alternatives that were considered]

## Implementation Plan
[Outline the implementation approach]

## References
[List related documents and resources]
"""


def build_frontmatter(
    uuid_str: str,
    title: str,
    doc_type: str,
    author: str,
) -> str:
    """Build the YAML frontmatter block for a design document.

    Args:
        uuid_str: The GUUID for this document.
        title: The document title.
        doc_type: The document type (e.g., 'pdr', 'spec').
        author: The author name (empty string if not provided).

    Returns:
        A complete YAML frontmatter string including --- delimiters.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "---",
        f"uuid: {uuid_str}",
        f'title: "{title}"',
        f"type: {doc_type}",
        "status: draft",
        f'author: "{author}"',
        f"created: {today}",
        f"updated: {today}",
        'description: ""',
        "tags: []",
        "related: []",
        "---",
    ]
    return "\n".join(lines) + "\n"


def create_design_document(
    doc_type: str,
    title: str,
    project_root: Path,
    author: str = "",
    filename: Optional[str] = None,
) -> Optional[tuple[Path, str]]:
    """Create a new design document with frontmatter and template body.

    This is the main function that orchestrates document creation:
    1. Creates the design/<type>/ directory if it does not exist
    2. Generates a GUUID with auto-incrementing sequence number
    3. Builds YAML frontmatter with all required and optional fields
    4. Loads a template from disk or uses the built-in default
    5. Writes the complete document to the correct directory

    Args:
        doc_type: Document type (pdr, spec, feature, decision, architecture, template).
        title: Human-readable document title.
        project_root: The project root directory path.
        author: Optional author name.
        filename: Optional custom filename (without .md extension).

    Returns:
        Tuple of (filepath, guuid) on success, or None if creation failed.
    """
    design_root = project_root / "design"
    type_dir = design_root / doc_type

    # Create the directory structure if it does not exist
    type_dir.mkdir(parents=True, exist_ok=True)

    # Generate GUUID
    guuid = generate_guuid(type_dir)

    # Determine filename
    if filename:
        # Use custom filename, ensure .md extension
        if not filename.endswith(".md"):
            filename = f"{filename}.md"
    else:
        # Auto-generate filename: GUUID-YYYYMMDD-NNNN-slugified-title.md
        slug = slugify(title)
        filename = f"{guuid}-{slug}.md"

    filepath = type_dir / filename

    # Build frontmatter
    frontmatter = build_frontmatter(guuid, title, doc_type, author)

    # Load template or use default
    template = load_template(doc_type, design_root)
    if template is not None:
        body = template
    else:
        body = get_default_template(title)

    # Write the complete document
    content = frontmatter + "\n" + body
    filepath.write_text(content, encoding="utf-8")

    return filepath, guuid


def main() -> int:
    """Main entry point for the CLI.

    Parses arguments, validates inputs, creates the document, and prints
    the result summary.

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    parser = argparse.ArgumentParser(
        description="Create a new design document from a template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a PDR document
  python scripts/eaa_design_create.py --type pdr --title "User Auth Design"

  # Create with author
  python scripts/eaa_design_create.py --type feature --title "OAuth" --author "John"

  # Create with custom filename
  python scripts/eaa_design_create.py --type decision --title "DB Selection" --filename "adr-001-db"
""",
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=VALID_TYPES,
        help="Document type: pdr, spec, feature, decision, architecture, template",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Document title (human-readable)",
    )
    parser.add_argument(
        "--author",
        default="",
        help="Author name (default: empty)",
    )
    parser.add_argument(
        "--filename",
        default=None,
        help="Custom filename (without .md extension). If omitted, auto-generated from GUUID and title.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    args = parser.parse_args()

    # Validate project root exists
    if not args.project_root.exists():
        print(
            f"ERROR: Project root does not exist: {args.project_root}",
            file=sys.stderr,
        )
        return 1

    if not args.project_root.is_dir():
        print(
            f"ERROR: Project root is not a directory: {args.project_root}",
            file=sys.stderr,
        )
        return 1

    # Create the document
    result = create_design_document(
        doc_type=args.type,
        title=args.title,
        project_root=args.project_root,
        author=args.author,
        filename=args.filename,
    )

    if result is None:
        print("ERROR: Failed to create design document", file=sys.stderr)
        return 1

    filepath, guuid = result

    # Output the result summary
    try:
        rel_path = filepath.relative_to(args.project_root)
    except ValueError:
        rel_path = filepath

    print(f"Created: {rel_path}")
    print(f"UUID: {guuid}")
    print(f"Type: {args.type}")
    print("Status: draft")

    return 0


if __name__ == "__main__":
    sys.exit(main())
