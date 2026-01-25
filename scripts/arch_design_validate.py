#!/usr/bin/env python3
"""
arch_design_validate.py - Validate design document frontmatter.

Checks that documents have required UUID and metadata fields.
Validates UUID format, status values, and date formats.

Required Fields:
- uuid: Globally unique identifier
- title: Human-readable title
- type: Document type (spec, plan, adr)
- status: Current status

Recommended Fields:
- created: Creation date (YYYY-MM-DD)
- updated: Last update date
- author: Document author
- version: Version number

Usage:
    # Validate single file
    python arch_design_validate.py --file docs/design/specs/auth.md

    # Validate directory
    python arch_design_validate.py --dir docs/design/specs

    # Validate all design docs
    python arch_design_validate.py --all

    # Strict mode (warnings become errors)
    python arch_design_validate.py --all --strict

Dependencies: Python 3.8+
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ValidationResult:
    """Result of document validation."""

    path: Path
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


REQUIRED_FIELDS = {
    "uuid": "Globally unique document identifier",
    "title": "Human-readable document title",
    "type": "Document type: spec, plan, adr",
    "status": "Document status",
}

RECOMMENDED_FIELDS = {
    "created": "Creation date (YYYY-MM-DD)",
    "updated": "Last update date (YYYY-MM-DD)",
    "author": "Document author",
    "version": "Document version number",
}

VALID_TYPES = {"spec", "plan", "adr"}
VALID_STATUSES = {
    "draft",
    "review",
    "approved",
    "implemented",
    "deprecated",
    "superseded",
    "archived",
}

UUID_PATTERN = re.compile(
    r"^[A-Z]{2,6}-[A-Z]+-\d{8}-[a-f0-9]{8}(?:_v\d{4})?$", re.IGNORECASE
)
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(content: str) -> dict[str, Any] | None:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None

    lines = content.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None

    frontmatter: dict[str, Any] = {}
    for line in lines[1:end_idx]:
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            parsed_value: Any = value

            if value.startswith('"') and value.endswith('"'):
                parsed_value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                parsed_value = value[1:-1]
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1]
                if inner:
                    items = [
                        item.strip().strip('"').strip("'")
                        for item in inner.split(",")
                        if item.strip()
                    ]
                    parsed_value = items
                else:
                    parsed_value = []
            elif value.lower() == "null":
                parsed_value = None
            elif value.isdigit():
                parsed_value = int(value)

            frontmatter[key] = parsed_value

    return frontmatter


def validate_file(file_path: Path, strict: bool = False) -> ValidationResult:
    """Validate a single design document.

    Args:
        file_path: Path to the markdown file
        strict: If True, warnings become errors

    Returns:
        ValidationResult with errors and warnings
    """
    result = ValidationResult(path=file_path)

    if not file_path.exists():
        result.valid = False
        result.errors.append("File not found")
        return result

    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        result.valid = False
        result.errors.append(f"Cannot read file: {e}")
        return result

    # Check for frontmatter
    fm = parse_frontmatter(content)
    if fm is None:
        result.valid = False
        result.errors.append("No frontmatter (must start with ---)")
        return result

    # Check required fields
    for field_name, description in REQUIRED_FIELDS.items():
        if field_name not in fm or not fm[field_name]:
            result.valid = False
            result.errors.append(f"Missing required: {field_name} ({description})")

    # Check recommended fields
    for field_name, description in RECOMMENDED_FIELDS.items():
        if field_name not in fm or not fm[field_name]:
            result.warnings.append(f"Missing recommended: {field_name}")

    # Validate UUID format
    if "uuid" in fm and fm["uuid"]:
        if not UUID_PATTERN.match(fm["uuid"]):
            result.valid = False
            result.errors.append(
                f"Invalid UUID format: {fm['uuid']} "
                f"(expected: PREFIX-TYPE-YYYYMMDD-uuid8)"
            )

    # Validate type
    if "type" in fm and fm["type"]:
        if fm["type"].lower() not in VALID_TYPES:
            result.valid = False
            result.errors.append(
                f"Invalid type: {fm['type']} (valid: {', '.join(VALID_TYPES)})"
            )

    # Validate status
    if "status" in fm and fm["status"]:
        if fm["status"].lower() not in VALID_STATUSES:
            result.valid = False
            result.errors.append(
                f"Invalid status: {fm['status']} (valid: {', '.join(VALID_STATUSES)})"
            )

    # Validate date formats
    for date_field in ["created", "updated"]:
        if date_field in fm and fm[date_field]:
            if not DATE_PATTERN.match(str(fm[date_field])):
                result.warnings.append(
                    f"Invalid date format for {date_field}: {fm[date_field]} "
                    f"(expected: YYYY-MM-DD)"
                )

    # Strict mode: warnings become errors
    if strict and result.warnings:
        result.valid = False
        result.errors.extend([f"[strict] {w}" for w in result.warnings])

    return result


def validate_directory(
    directory: Path,
    strict: bool = False,
    recursive: bool = True,
) -> list[ValidationResult]:
    """Validate all .md files in a directory.

    Args:
        directory: Directory to scan
        strict: If True, warnings become errors
        recursive: If True, scan subdirectories

    Returns:
        List of ValidationResults
    """
    results: list[ValidationResult] = []

    if not directory.exists():
        return results

    pattern = "**/*.md" if recursive else "*.md"
    for md_file in sorted(directory.glob(pattern)):
        # Skip index, readme, template files
        if md_file.name.lower() in ("index.md", "readme.md", "template.md"):
            continue
        results.append(validate_file(md_file, strict))

    return results


def load_config(project_root: Path) -> dict[str, Path]:
    """Load configuration from patterns.md."""
    config: dict[str, Path] = {"design_root": Path("docs/design")}
    patterns_file = project_root / ".claude" / "atlas" / "patterns.md"

    if not patterns_file.exists():
        patterns_file = project_root / ".design" / "memory" / "patterns.md"

    if patterns_file.exists():
        content = patterns_file.read_text(encoding="utf-8")
        if match := re.search(r"^design_root:\s*(\S+)", content, re.MULTILINE):
            config["design_root"] = Path(match.group(1).rstrip("/"))

    return config


def print_result(
    result: ValidationResult, project_root: Path, verbose: bool = False
) -> None:
    """Print validation result."""
    rel_path = (
        result.path.relative_to(project_root)
        if result.path.is_relative_to(project_root)
        else result.path
    )
    status = "✓ VALID" if result.valid else "✗ INVALID"

    print(f"{status}: {rel_path}")

    for error in result.errors:
        print(f"    ERROR: {error}")

    if verbose:
        for warning in result.warnings:
            print(f"    WARN:  {warning}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate design document frontmatter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Required Fields:
  uuid    - Globally unique identifier (PREFIX-TYPE-YYYYMMDD-uuid8)
  title   - Human-readable title
  type    - Document type (spec, plan, adr)
  status  - Current status (draft, review, approved, etc.)

Examples:
  # Validate single file
  python arch_design_validate.py --file docs/design/specs/auth.md

  # Validate directory
  python arch_design_validate.py --dir docs/design/specs

  # Validate all design docs
  python arch_design_validate.py --all

  # Strict mode
  python arch_design_validate.py --all --strict
        """,
    )

    parser.add_argument("--file", "-f", type=Path, help="Validate single file")
    parser.add_argument("--dir", "-d", type=Path, help="Validate directory")
    parser.add_argument(
        "--all", "-a", action="store_true", help="Validate all design docs"
    )
    parser.add_argument(
        "--strict", "-s", action="store_true", help="Treat warnings as errors"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show warnings")
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Only show invalid files"
    )
    parser.add_argument("--project-root", type=Path, default=Path.cwd())

    args = parser.parse_args()

    results: list[ValidationResult] = []

    if args.file:
        results = [validate_file(args.file, args.strict)]
    elif args.dir:
        results = validate_directory(args.dir, args.strict)
    elif args.all:
        config = load_config(args.project_root)
        design_root = args.project_root / config["design_root"]
        results = validate_directory(design_root, args.strict)
    else:
        parser.print_help()
        return 1

    # Print results
    valid_count = 0
    invalid_count = 0

    for result in results:
        if result.valid:
            valid_count += 1
            if not args.quiet:
                print_result(result, args.project_root, args.verbose)
        else:
            invalid_count += 1
            print_result(result, args.project_root, args.verbose)

    # Summary
    print(f"\nSummary: {valid_count} valid, {invalid_count} invalid")

    return 0 if invalid_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
