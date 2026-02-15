#!/usr/bin/env python3
"""
eaa_design_validate.py - Validate design document frontmatter and structure.

Validates that design documents have correct YAML frontmatter with all
required fields, valid GUUID format, valid status values, valid date formats,
and valid document types.

Required frontmatter fields:
    - uuid: GUUID-YYYYMMDD-NNNN format
    - title: Non-empty string
    - status: One of draft, review, approved, implemented, deprecated, rejected
    - created: YYYY-MM-DD format
    - updated: YYYY-MM-DD format

Usage:
    # Validate a single document
    python scripts/eaa_design_validate.py design/pdr/my-doc.md

    # Validate all documents in design/
    python scripts/eaa_design_validate.py --all

    # Validate all documents of a specific type
    python scripts/eaa_design_validate.py --all --type pdr

    # Verbose output with all checks shown
    python scripts/eaa_design_validate.py --all --verbose

    # JSON output for CI/CD integration
    python scripts/eaa_design_validate.py --all --format json

Dependencies: Python 3.8+ (stdlib only, no external packages)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Valid statuses as defined in the SKILL.md specification
VALID_STATUSES = {"draft", "review", "approved", "implemented", "deprecated", "rejected"}

# Valid document types as defined in the SKILL.md specification
VALID_TYPES = {"pdr", "spec", "feature", "decision", "architecture", "template"}

# GUUID format: GUUID-YYYYMMDD-NNNN
# - GUUID prefix is fixed
# - YYYYMMDD is an 8-digit date
# - NNNN is a 4-digit sequence number starting at 0001
GUUID_PATTERN = re.compile(r"^GUUID-(\d{4})(\d{2})(\d{2})-(\d{4})$")

# ISO date format: YYYY-MM-DD
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Required frontmatter fields that every design document must have
REQUIRED_FIELDS = ["uuid", "title", "status", "created", "updated"]


def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
    """Parse YAML frontmatter from a markdown document.

    Frontmatter is the content between two --- markers at the start of the file.
    This parser handles simple key: value pairs without requiring a YAML library.

    Args:
        content: The full content of the markdown file.

    Returns:
        A tuple of (frontmatter_dict, error_message).
        If parsing succeeds, frontmatter_dict contains the parsed fields and
        error_message is None.
        If parsing fails, frontmatter_dict is None and error_message describes
        the problem.
    """
    # Check that the file starts with ---
    if not content.startswith("---"):
        return None, "No frontmatter found: file does not start with '---'"

    # Find the closing --- marker (skip the first one)
    # Split on newlines to handle the markers properly
    lines = content.split("\n")
    if len(lines) < 2:
        return None, "No frontmatter found: file too short"

    # Find the second --- marker
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index is None:
        return None, "No frontmatter found: missing closing '---' marker"

    # Parse the frontmatter lines between the markers
    frontmatter = {}
    for line_num, line in enumerate(lines[1:end_index], start=2):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Parse key: value pairs
        colon_pos = line.find(":")
        if colon_pos == -1:
            continue

        key = line[:colon_pos].strip()
        value = line[colon_pos + 1:].strip()

        # Remove surrounding quotes from values
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        frontmatter[key] = value

    return frontmatter, None


def validate_guuid(uuid_str: str) -> Optional[str]:
    """Validate that a UUID string matches the GUUID-YYYYMMDD-NNNN format.

    Checks:
    1. Matches the GUUID-YYYYMMDD-NNNN pattern
    2. Date components are plausible (month 01-12, day 01-31)
    3. Sequence number is >= 1 (0000 is not valid)

    Args:
        uuid_str: The UUID string to validate.

    Returns:
        An error message string if invalid, or None if valid.
    """
    match = GUUID_PATTERN.match(uuid_str)
    if not match:
        return f"Invalid UUID format: '{uuid_str}' does not match GUUID-YYYYMMDD-NNNN"

    year, month, day, seq = match.groups()
    month_int = int(month)
    day_int = int(day)
    seq_int = int(seq)

    if not (1 <= month_int <= 12):
        return f"Invalid UUID date: month {month} is not in range 01-12"

    if not (1 <= day_int <= 31):
        return f"Invalid UUID date: day {day} is not in range 01-31"

    if seq_int < 1:
        return f"Invalid UUID sequence: {seq} must be >= 0001"

    return None


def validate_date(date_str: str, field_name: str) -> Optional[str]:
    """Validate that a date string is in YYYY-MM-DD format.

    Args:
        date_str: The date string to validate.
        field_name: The frontmatter field name (for error messages).

    Returns:
        An error message string if invalid, or None if valid.
    """
    if not DATE_PATTERN.match(date_str):
        return f"Invalid date format for '{field_name}': expected YYYY-MM-DD, got '{date_str}'"
    return None


def validate_status(status_str: str) -> Optional[str]:
    """Validate that a status value is one of the allowed values.

    Valid statuses: draft, review, approved, implemented, deprecated, rejected.

    Args:
        status_str: The status string to validate.

    Returns:
        An error message string if invalid, or None if valid.
    """
    if status_str.lower() not in VALID_STATUSES:
        return (
            f"Invalid status: '{status_str}'. "
            f"Valid values: {', '.join(sorted(VALID_STATUSES))}"
        )
    return None


def validate_type(type_str: str) -> Optional[str]:
    """Validate that a type value is one of the allowed values.

    Valid types: pdr, spec, feature, decision, architecture, template.

    Args:
        type_str: The type string to validate.

    Returns:
        An error message string if invalid, or None if valid.
    """
    if type_str.lower() not in VALID_TYPES:
        return (
            f"Invalid type: '{type_str}'. "
            f"Valid values: {', '.join(sorted(VALID_TYPES))}"
        )
    return None


def validate_document(filepath: Path, verbose: bool = False) -> Tuple[List[Dict], List[Dict]]:
    """Validate a single design document's frontmatter.

    Checks:
    1. Frontmatter exists (between --- markers)
    2. All required fields are present (uuid, title, status, created, updated)
    3. UUID matches GUUID-YYYYMMDD-NNNN format
    4. Status is a valid value
    5. Date fields are in YYYY-MM-DD format
    6. Type field (if present) is a valid value

    Args:
        filepath: Path to the markdown file to validate.
        verbose: If True, also report passing checks.

    Returns:
        A tuple of (errors, warnings) where each is a list of dicts with
        keys: file, line, level, message.
    """
    errors: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []

    # Read file content
    try:
        content = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        errors.append({
            "file": str(filepath),
            "line": 0,
            "level": "ERROR",
            "message": f"Cannot read file: {e}",
        })
        return errors, warnings

    # Parse frontmatter
    frontmatter, parse_error = parse_frontmatter(content)
    if parse_error:
        errors.append({
            "file": str(filepath),
            "line": 1,
            "level": "ERROR",
            "message": parse_error,
        })
        return errors, warnings

    if frontmatter is None:
        errors.append({
            "file": str(filepath),
            "line": 1,
            "level": "ERROR",
            "message": "No frontmatter found",
        })
        return errors, warnings

    # Check required fields
    for field_name in REQUIRED_FIELDS:
        if field_name not in frontmatter:
            # Estimate line number (within first 20 lines of frontmatter)
            errors.append({
                "file": str(filepath),
                "line": 3,
                "level": "ERROR",
                "message": f"Missing required field: {field_name}",
            })

    # Validate UUID format if present
    if "uuid" in frontmatter:
        uuid_error = validate_guuid(frontmatter["uuid"])
        if uuid_error:
            errors.append({
                "file": str(filepath),
                "line": _find_field_line(content, "uuid"),
                "level": "ERROR",
                "message": uuid_error,
            })

    # Validate status if present
    if "status" in frontmatter:
        status_error = validate_status(frontmatter["status"])
        if status_error:
            errors.append({
                "file": str(filepath),
                "line": _find_field_line(content, "status"),
                "level": "ERROR",
                "message": status_error,
            })

    # Validate date fields if present
    for date_field in ("created", "updated"):
        if date_field in frontmatter:
            date_error = validate_date(frontmatter[date_field], date_field)
            if date_error:
                errors.append({
                    "file": str(filepath),
                    "line": _find_field_line(content, date_field),
                    "level": "ERROR",
                    "message": date_error,
                })

    # Validate type if present (optional field, but must be valid if present)
    if "type" in frontmatter:
        type_error = validate_type(frontmatter["type"])
        if type_error:
            warnings.append({
                "file": str(filepath),
                "line": _find_field_line(content, "type"),
                "level": "WARNING",
                "message": type_error,
            })

    # Check for empty optional fields (warnings only)
    if "author" in frontmatter and not frontmatter["author"]:
        warnings.append({
            "file": str(filepath),
            "line": _find_field_line(content, "author"),
            "level": "WARNING",
            "message": "Empty 'author' field",
        })

    if "description" in frontmatter and not frontmatter["description"]:
        warnings.append({
            "file": str(filepath),
            "line": _find_field_line(content, "description"),
            "level": "WARNING",
            "message": "Empty description",
        })

    return errors, warnings


def _find_field_line(content: str, field_name: str) -> int:
    """Find the line number of a frontmatter field in the document.

    Args:
        content: The full document content.
        field_name: The field name to search for.

    Returns:
        The 1-based line number where the field appears, or 3 as fallback.
    """
    for i, line in enumerate(content.split("\n"), start=1):
        if line.strip().startswith(f"{field_name}:"):
            return i
    return 3  # Default fallback line number


def find_design_documents(
    project_root: Path,
    type_filter: Optional[str] = None,
) -> List[Path]:
    """Find all design documents under the design/ directory.

    Scans design/ subdirectories for .md files. If a type filter is provided,
    only scans the corresponding type subdirectory.

    Args:
        project_root: The project root directory.
        type_filter: Optional type name to filter by (e.g., 'pdr').

    Returns:
        A sorted list of Path objects for found .md files.
    """
    design_root = project_root / "design"
    if not design_root.exists():
        return []

    if type_filter:
        # Only scan the specific type directory
        type_dir = design_root / type_filter
        if not type_dir.exists():
            return []
        return sorted(type_dir.glob("*.md"))

    # Scan all type directories
    files = []
    for subdir in sorted(design_root.iterdir()):
        if subdir.is_dir():
            files.extend(sorted(subdir.glob("*.md")))
    return files


def format_text_output(
    results: List[Dict],
    verbose: bool = False,
) -> str:
    """Format validation results as human-readable text.

    Args:
        results: List of per-file result dicts with keys:
            file, passed, errors, warnings.
        verbose: If True, show individual check results.

    Returns:
        Formatted text string.
    """
    lines = []
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    total_errors = sum(len(r["errors"]) for r in results)
    total_warnings = sum(len(r["warnings"]) for r in results)

    for i, result in enumerate(results, start=1):
        filepath = result["file"]
        if verbose:
            lines.append(f"\n[{i}/{total}] {filepath}")
            if result["passed"]:
                lines.append("  [PASS] All checks passed")
            else:
                for err in result["errors"]:
                    lines.append(f"  [ERROR] Line {err['line']}: {err['message']}")
                for warn in result["warnings"]:
                    lines.append(f"  [WARNING] Line {warn['line']}: {warn['message']}")
        else:
            if not result["passed"]:
                lines.append(f"\nValidating: {filepath}")
                for err in result["errors"]:
                    lines.append(f"[ERROR] Line {err['line']}: {err['message']}")
                for warn in result["warnings"]:
                    lines.append(f"[WARNING] Line {warn['line']}: {warn['message']}")

    # Summary
    lines.append("")
    if failed == 0:
        lines.append(f"Validation passed: {total} files validated, 0 errors, {total_warnings} warnings")
    else:
        lines.append(f"Summary: {total} files validated, {passed} passed, {failed} failed")
        lines.append(f"Errors: {total_errors}, Warnings: {total_warnings}")

    return "\n".join(lines)


def format_json_output(results: List[Dict]) -> str:
    """Format validation results as JSON.

    Args:
        results: List of per-file result dicts.

    Returns:
        JSON string with total, passed, failed, errors, and warnings.
    """
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed

    all_errors = []
    all_warnings = []
    for r in results:
        all_errors.extend(r["errors"])
        all_warnings.extend(r["warnings"])

    output = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": all_errors,
        "warnings": all_warnings,
    }
    return json.dumps(output, indent=2)


def main() -> int:
    """Main entry point for the CLI.

    Parses arguments, finds and validates documents, formats and prints results.

    Returns:
        Exit code: 0 if all documents pass, 1 if any errors found.
    """
    parser = argparse.ArgumentParser(
        description="Validate design document frontmatter and structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single file
  python scripts/eaa_design_validate.py design/pdr/my-design.md

  # Validate all documents
  python scripts/eaa_design_validate.py --all

  # Validate all PDR documents with verbose output
  python scripts/eaa_design_validate.py --all --type pdr --verbose

  # JSON output for CI/CD
  python scripts/eaa_design_validate.py --all --format json
""",
    )

    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        default=None,
        help="Path to a single design document to validate",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="validate_all",
        help="Validate all design documents under design/ directory",
    )
    parser.add_argument(
        "--type",
        choices=sorted(VALID_TYPES),
        default=None,
        help="Filter by document type (only with --all)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output including passing checks",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format: text (default) or json",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    args = parser.parse_args()

    # Determine which files to validate
    if args.file:
        # Single file mode
        if not args.file.exists():
            print(f"ERROR: File not found: {args.file}", file=sys.stderr)
            return 1
        files = [args.file]
    elif args.validate_all:
        # Bulk validation mode
        files = find_design_documents(args.project_root, args.type)
        if not files:
            msg = "No design documents found"
            if args.type:
                msg += f" for type '{args.type}'"
            if args.format == "json":
                print(json.dumps({"total": 0, "passed": 0, "failed": 0, "errors": [], "warnings": []}))
            else:
                print(msg)
            return 0
    else:
        parser.print_help()
        return 1

    # Validate each file
    results = []
    for filepath in files:
        errors, warnings = validate_document(filepath, args.verbose)
        results.append({
            "file": str(filepath),
            "passed": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        })

    # Format and print output
    if args.format == "json":
        print(format_json_output(results))
    else:
        print(format_text_output(results, args.verbose))

    # Return exit code: 0 if all passed, 1 if any errors
    has_errors = any(not r["passed"] for r in results)
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
