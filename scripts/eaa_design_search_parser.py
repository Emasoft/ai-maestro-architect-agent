#!/usr/bin/env python3
"""
arch_design_search_parser.py - Parsing and metadata extraction for design documents.

This module provides the core parsing functionality for Architect Agent design documents:
- Configuration loading from patterns.md
- YAML frontmatter parsing (without external dependencies)
- Metadata extraction from design document files

Used by arch_design_search.py for filesystem-based document search.

Dependencies: Python 3.8+ (uses pathlib only)
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

__all__ = [
    "DesignConfig",
    "DocumentMetadata",
    "parse_frontmatter",
    "extract_metadata",
    "get_type_directory",
]


@dataclass
class DesignConfig:
    """Configuration loaded from patterns.md or defaults."""

    mode: str = "single-git"
    design_root: Path = field(default_factory=lambda: Path("docs/design"))
    uuid_prefix: str = "PROJ"

    @classmethod
    def load(cls, project_root: Optional[Path] = None) -> "DesignConfig":
        """Load configuration from patterns.md file."""
        if project_root is None:
            project_root = Path.cwd()

        config = cls()
        patterns_file = project_root / ".claude" / "architect" / "patterns.md"

        if not patterns_file.exists():
            patterns_file = project_root / ".design" / "memory" / "patterns.md"

        if patterns_file.exists():
            content = patterns_file.read_text(encoding="utf-8")

            if match := re.search(r"^mode:\s*(\S+)", content, re.MULTILINE):
                config.mode = match.group(1)

            if match := re.search(r"^design_root:\s*(\S+)", content, re.MULTILINE):
                config.design_root = Path(match.group(1).rstrip("/"))

            if match := re.search(r"^uuid_prefix:\s*(\S+)", content, re.MULTILINE):
                config.uuid_prefix = match.group(1).upper()

        return config


@dataclass
class DocumentMetadata:
    """Parsed metadata from a design document."""

    path: Path
    uuid: str = ""
    version: int = 1
    title: str = ""
    doc_type: str = ""
    status: str = ""
    created: str = ""
    updated: str = ""
    author: str = ""
    tags: list[str] = field(default_factory=list)
    related_issues: list[str] = field(default_factory=list)
    related_docs: list[str] = field(default_factory=list)
    previous_version: Optional[str] = None

    def to_dict(self) -> dict[str, str | int | list[str] | None]:
        """Convert to dictionary for JSON output."""
        return {
            "path": str(self.path),
            "uuid": self.uuid,
            "version": self.version,
            "title": self.title,
            "type": self.doc_type,
            "status": self.status,
            "created": self.created,
            "updated": self.updated,
            "author": self.author,
            "tags": self.tags,
            "related_issues": self.related_issues,
            "related_docs": self.related_docs,
            "previous_version": self.previous_version,
        }


def parse_frontmatter(content: str) -> dict[str, str | int | list[str] | None]:
    """Parse YAML frontmatter from markdown content.

    Fast parsing - only reads the frontmatter section.
    Handles basic YAML types: strings, quoted strings, arrays, integers, null.

    Args:
        content: Raw markdown content starting with frontmatter.

    Returns:
        Dictionary of parsed frontmatter key-value pairs.
    """
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

    frontmatter: dict[str, str | int | list[str] | None] = {}
    for line in lines[1:end_idx]:
        if ":" in line:
            key, _, raw_value = line.partition(":")
            key = key.strip()
            raw_value = raw_value.strip()
            parsed_value: str | int | list[str] | None

            # Handle quoted strings
            if raw_value.startswith('"') and raw_value.endswith('"'):
                parsed_value = raw_value[1:-1]
            elif raw_value.startswith("'") and raw_value.endswith("'"):
                parsed_value = raw_value[1:-1]
            # Handle arrays
            elif raw_value.startswith("[") and raw_value.endswith("]"):
                inner = raw_value[1:-1]
                if inner:
                    items: list[str] = []
                    for item in inner.split(","):
                        item = item.strip().strip('"').strip("'")
                        if item:
                            items.append(item)
                    parsed_value = items
                else:
                    parsed_value = []
            # Handle null
            elif raw_value.lower() == "null":
                parsed_value = None
            # Handle integers
            elif raw_value.isdigit():
                parsed_value = int(raw_value)
            else:
                parsed_value = raw_value

            frontmatter[key] = parsed_value

    return frontmatter


def extract_metadata(file_path: Path) -> Optional[DocumentMetadata]:
    """Extract metadata from a design document file.

    Only reads the first 4KB for speed - frontmatter should be at the top.

    Args:
        file_path: Path to the markdown design document.

    Returns:
        DocumentMetadata object or None if parsing fails.
    """
    try:
        # Read only the first 4KB - frontmatter should be at the top
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(4096)

        fm = parse_frontmatter(content)
        if not fm:
            return None

        # Extract and type-cast string fields
        uuid_val = fm.get("uuid", "")
        uuid_str = str(uuid_val) if uuid_val is not None else ""

        version_val = fm.get("version", 1)
        version_int = int(version_val) if isinstance(version_val, int) else 1

        title_val = fm.get("title", "")
        title_str = str(title_val) if title_val is not None else ""

        type_val = fm.get("type", "")
        type_str = str(type_val).upper() if type_val is not None else ""

        status_val = fm.get("status", "")
        status_str = str(status_val) if status_val is not None else ""

        created_val = fm.get("created", "")
        created_str = str(created_val) if created_val is not None else ""

        updated_val = fm.get("updated", "")
        updated_str = str(updated_val) if updated_val is not None else ""

        author_val = fm.get("author", "")
        author_str = str(author_val) if author_val is not None else ""

        prev_val = fm.get("previous_version")
        prev_str: Optional[str] = str(prev_val) if prev_val is not None else None

        # Extract list fields
        tags_val = fm.get("tags", [])
        if isinstance(tags_val, list):
            tags: list[str] = tags_val
        elif isinstance(tags_val, str):
            tags = [tags_val]
        else:
            tags = []

        issues_val = fm.get("related_issues", [])
        if isinstance(issues_val, list):
            issues: list[str] = issues_val
        elif isinstance(issues_val, str):
            issues = [issues_val]
        else:
            issues = []

        docs_val = fm.get("related_docs", [])
        if isinstance(docs_val, list):
            docs: list[str] = docs_val
        elif isinstance(docs_val, str):
            docs = [docs_val]
        else:
            docs = []

        return DocumentMetadata(
            path=file_path,
            uuid=uuid_str,
            version=version_int,
            title=title_str,
            doc_type=type_str,
            status=status_str,
            created=created_str,
            updated=updated_str,
            author=author_str,
            tags=tags,
            related_issues=issues,
            related_docs=docs,
            previous_version=prev_str,
        )
    except (OSError, UnicodeDecodeError):
        return None


def get_type_directory(doc_type: str) -> str:
    """Map document type to directory name (filesystem index).

    Args:
        doc_type: Document type (SPEC, PLAN, ADR).

    Returns:
        Directory name for the type, or empty string if unknown.
    """
    type_map = {
        "SPEC": "specs",
        "PLAN": "plans",
        "ADR": "decisions",
    }
    return type_map.get(doc_type.upper(), "")
