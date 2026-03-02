#!/usr/bin/env python3
"""
arch_design_uuid.py - UUID generator for Architect Agent design documents.

This script generates globally unique UUIDs for design documents and can:
1. Generate new UUIDs for document types (SPEC, PLAN, ADR)
2. Create versioned UUIDs from existing base UUIDs
3. Add/update frontmatter in .md files with generated UUIDs
4. Batch-process directories to add UUIDs to all .md files

UUID Format: {PREFIX}-{TYPE}-{YYYYMMDD}-{UUID8}[_v{VERSION}]
- PREFIX: 4-char project identifier from patterns.md (default: PROJ)
- TYPE: SPEC, PLAN, ADR
- YYYYMMDD: Creation date
- UUID8: First 8 chars of UUID v4 (guarantees global uniqueness)
- VERSION: 4-digit padded version suffix (_v0001, _v0002, etc.)

Usage:
    # Generate new UUID
    python arch_design_uuid.py --type SPEC
    python arch_design_uuid.py --type PLAN --prefix AUTH

    # Generate versioned UUID
    python arch_design_uuid.py --version PROJ-SPEC-20250108-a7b3f2e1

    # Add frontmatter to file
    python arch_design_uuid.py --file docs/design/specs/auth-service.md --type SPEC

    # Batch add frontmatter to directory
    python arch_design_uuid.py --dir docs/design/specs --type SPEC

    # List all UUIDs in design root
    python arch_design_uuid.py --list

Dependencies: Python 3.8+ (uses pathlib, uuid, dataclasses)
"""

import argparse
import re
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class DesignConfig:
    """Configuration loaded from patterns.md or defaults."""

    mode: str = "single-git"
    design_root: Path = field(default_factory=lambda: Path("docs/design"))
    uuid_prefix: str = "PROJ"
    memory_root: Path = field(default_factory=lambda: Path("design/memory"))

    @classmethod
    def load(cls, project_root: Optional[Path] = None) -> "DesignConfig":
        """Load configuration from patterns.md file."""
        if project_root is None:
            project_root = Path.cwd()

        config = cls()
        patterns_file = project_root / "design" / "memory" / "patterns.md"

        if not patterns_file.exists():
            # Try alternative location for dual-git mode
            patterns_file = project_root / ".design" / "memory" / "patterns.md"

        if patterns_file.exists():
            content = patterns_file.read_text(encoding="utf-8")

            # Parse configuration values
            if match := re.search(r"^mode:\s*(\S+)", content, re.MULTILINE):
                config.mode = match.group(1)

            if match := re.search(r"^design_root:\s*(\S+)", content, re.MULTILINE):
                config.design_root = Path(match.group(1).rstrip("/"))

            if match := re.search(r"^uuid_prefix:\s*(\S+)", content, re.MULTILINE):
                config.uuid_prefix = match.group(1).upper()

            if match := re.search(r"^memory_root:\s*(\S+)", content, re.MULTILINE):
                config.memory_root = Path(match.group(1).rstrip("/"))

        return config


@dataclass
class DocumentUUID:
    """Represents a design document UUID."""

    prefix: str
    doc_type: str
    date: str
    uuid8: str
    version: Optional[int] = None

    @property
    def base_uuid(self) -> str:
        """Return base UUID without version suffix."""
        return f"{self.prefix}-{self.doc_type}-{self.date}-{self.uuid8}"

    @property
    def full_uuid(self) -> str:
        """Return full UUID with version suffix if present."""
        if self.version is not None:
            return f"{self.base_uuid}_v{self.version:04d}"
        return self.base_uuid

    @classmethod
    def parse(cls, uuid_str: str) -> Optional["DocumentUUID"]:
        """Parse a UUID string into DocumentUUID object."""
        # Pattern: PREFIX-TYPE-YYYYMMDD-UUID8[_vNNNN]
        pattern = r"^([A-Z]{2,6})-([A-Z]+)-(\d{8})-([a-f0-9]{8})(?:_v(\d{4}))?$"
        if match := re.match(pattern, uuid_str, re.IGNORECASE):
            version = int(match.group(5)) if match.group(5) else None
            return cls(
                prefix=match.group(1).upper(),
                doc_type=match.group(2).upper(),
                date=match.group(3),
                uuid8=match.group(4).lower(),
                version=version,
            )
        return None

    @classmethod
    def generate(cls, prefix: str, doc_type: str) -> "DocumentUUID":
        """Generate a new UUID with UUID v4 segment."""
        # Generate UUID v4 and take first 8 characters for uniqueness
        uuid8 = uuid.uuid4().hex[:8]
        date = datetime.now().strftime("%Y%m%d")
        return cls(
            prefix=prefix.upper(),
            doc_type=doc_type.upper(),
            date=date,
            uuid8=uuid8,
        )


def generate_uuid8() -> str:
    """Generate 8-character UUID segment from UUID v4."""
    return uuid.uuid4().hex[:8]


def generate_new_uuid(prefix: str, doc_type: str) -> str:
    """Generate a new UUID for a design document."""
    doc_uuid = DocumentUUID.generate(prefix, doc_type)
    return doc_uuid.full_uuid


def generate_version_uuid(base_uuid: str, design_root: Path) -> str:
    """Generate a new versioned UUID from a base UUID.

    Scans design_root for existing versions and generates the next version.
    """
    # Strip any existing version suffix to get base UUID
    parsed = DocumentUUID.parse(base_uuid)
    if parsed:
        base_uuid = parsed.base_uuid
    else:
        # Try to strip version suffix manually
        base_uuid = re.sub(r"_v\d{4}$", "", base_uuid)

    # Find highest existing version
    highest_version = 0

    if design_root.exists():
        for md_file in design_root.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                # Look for UUIDs containing this base UUID
                pattern = rf"{re.escape(base_uuid)}(?:_v(\d{{4}}))?"
                for match in re.finditer(pattern, content):
                    if match.group(1):
                        version = int(match.group(1))
                        highest_version = max(highest_version, version)
            except (OSError, UnicodeDecodeError):
                continue

    new_version = highest_version + 1
    return f"{base_uuid}_v{new_version:04d}"


def extract_frontmatter(content: str) -> tuple[Optional[dict[str, str]], str]:
    """Extract YAML frontmatter from markdown content.

    Returns (frontmatter_dict, body_content).
    If no frontmatter, returns (None, content).
    """
    if not content.startswith("---"):
        return None, content

    # Find closing ---
    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None, content

    # Parse frontmatter as simple key-value pairs
    frontmatter: dict[str, str] = {}
    for line in lines[1:end_idx]:
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Handle quoted strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            # Handle arrays
            elif value.startswith("[") and value.endswith("]"):
                value = value  # Keep as string for simplicity
            frontmatter[key] = value

    body = "\n".join(lines[end_idx + 1 :])
    return frontmatter, body


def create_frontmatter(
    doc_uuid: str,
    title: str,
    doc_type: str,
    status: str = "draft",
    author: str = "Architect Agent",
    tags: Optional[list[str]] = None,
    related_issues: Optional[list[str]] = None,
    related_docs: Optional[list[str]] = None,
    previous_version: Optional[str] = None,
) -> str:
    """Create YAML frontmatter string for a design document."""
    today = datetime.now().strftime("%Y-%m-%d")

    tags_str = str(tags) if tags else "[]"
    issues_str = str(related_issues) if related_issues else "[]"
    docs_str = str(related_docs) if related_docs else "[]"
    prev_version_str = f'"{previous_version}"' if previous_version else "null"

    return f'''---
uuid: {doc_uuid}
version: 1
title: "{title}"
type: {doc_type.lower()}
status: {status}
created: {today}
updated: {today}
author: "{author}"
related_issues: {issues_str}
related_docs: {docs_str}
supersedes: null
superseded_by: null
previous_version: {prev_version_str}
tags: {tags_str}
---
'''


def add_frontmatter_to_file(
    file_path: Path,
    doc_type: str,
    config: DesignConfig,
    force: bool = False,
) -> Optional[str]:
    """Add UUID frontmatter to a markdown file.

    Returns the generated UUID if successful, None if skipped.
    """
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        return None

    content = file_path.read_text(encoding="utf-8")
    existing_fm, body = extract_frontmatter(content)

    # Check if already has UUID
    if existing_fm and "uuid" in existing_fm and not force:
        print(f"SKIP: {file_path} already has UUID: {existing_fm['uuid']}")
        return existing_fm["uuid"]

    # Generate new UUID
    doc_uuid = generate_new_uuid(config.uuid_prefix, doc_type)

    # Extract title from first heading or filename
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = file_path.stem.replace("-", " ").replace("_", " ").title()

    # Create new frontmatter
    new_frontmatter = create_frontmatter(
        doc_uuid=doc_uuid,
        title=title,
        doc_type=doc_type,
    )

    # Write updated file
    new_content = new_frontmatter + "\n" + body.lstrip()
    file_path.write_text(new_content, encoding="utf-8")

    print(f"ADDED: {file_path} -> {doc_uuid}")
    return doc_uuid


def batch_add_frontmatter(
    directory: Path,
    doc_type: str,
    config: DesignConfig,
    force: bool = False,
) -> list[str]:
    """Add frontmatter to all .md files in a directory.

    Returns list of generated UUIDs.
    """
    if not directory.exists():
        print(f"ERROR: Directory not found: {directory}", file=sys.stderr)
        return []

    uuids = []
    for md_file in sorted(directory.rglob("*.md")):
        # Skip files that look like templates or READMEs
        if md_file.name.lower() in ("readme.md", "template.md", "index.md"):
            continue

        result = add_frontmatter_to_file(md_file, doc_type, config, force)
        if result:
            uuids.append(result)

    return uuids


def list_all_uuids(design_root: Path) -> list[tuple[str, Path]]:
    """List all UUIDs found in design documents.

    Returns list of (uuid, file_path) tuples.
    """
    results: list[tuple[str, Path]] = []

    if not design_root.exists():
        return results

    for md_file in sorted(design_root.rglob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, _ = extract_frontmatter(content)
            if frontmatter and "uuid" in frontmatter:
                results.append((frontmatter["uuid"], md_file))
        except (OSError, UnicodeDecodeError):
            continue

    return results


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate UUIDs for EAA design documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate new UUID
  python arch_design_uuid.py --type SPEC

  # Generate versioned UUID
  python arch_design_uuid.py --version PROJ-SPEC-20250108-a7b3f2e1

  # Add frontmatter to file
  python arch_design_uuid.py --file docs/design/specs/auth.md --type SPEC

  # Batch process directory
  python arch_design_uuid.py --dir docs/design/specs --type SPEC

  # List all UUIDs
  python arch_design_uuid.py --list
        """,
    )

    parser.add_argument(
        "--type",
        "-t",
        choices=["SPEC", "PLAN", "ADR", "spec", "plan", "adr"],
        help="Document type (SPEC, PLAN, ADR)",
    )
    parser.add_argument(
        "--prefix",
        "-p",
        help="UUID prefix (overrides patterns.md config)",
    )
    parser.add_argument(
        "--version",
        "-v",
        metavar="BASE_UUID",
        help="Generate versioned UUID from existing base UUID",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        help="Add frontmatter to specific .md file",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=Path,
        help="Batch add frontmatter to all .md files in directory",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all UUIDs in design root",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing UUIDs when adding frontmatter",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    args = parser.parse_args()

    # Load configuration
    config = DesignConfig.load(args.project_root)

    # Override prefix if specified
    if args.prefix:
        config.uuid_prefix = args.prefix.upper()

    # Handle --version mode
    if args.version:
        design_root = args.project_root / config.design_root
        versioned_uuid = generate_version_uuid(args.version, design_root)
        print(versioned_uuid)
        return 0

    # Handle --list mode
    if args.list:
        design_root = args.project_root / config.design_root
        uuid_list = list_all_uuids(design_root)

        if not uuid_list:
            print(f"No UUIDs found in {design_root}")
            return 0

        print(f"\n{'UUID':<45} {'File'}")
        print("-" * 80)
        for doc_uuid, file_path in uuid_list:
            rel_path = file_path.relative_to(args.project_root)
            print(f"{doc_uuid:<45} {rel_path}")
        print(f"\nTotal: {len(uuid_list)} documents")
        return 0

    # Handle --file mode
    if args.file:
        if not args.type:
            print("ERROR: --type is required when using --file", file=sys.stderr)
            return 1
        add_frontmatter_to_file(args.file, args.type.upper(), config, args.force)
        return 0

    # Handle --dir mode
    if args.dir:
        if not args.type:
            print("ERROR: --type is required when using --dir", file=sys.stderr)
            return 1
        generated_uuids = batch_add_frontmatter(
            args.dir, args.type.upper(), config, args.force
        )
        print(f"\nProcessed {len(generated_uuids)} files")
        return 0

    # Default: generate new UUID
    if args.type:
        new_uuid = generate_new_uuid(config.uuid_prefix, args.type.upper())
        print(new_uuid)
        return 0

    # No action specified
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
