#!/usr/bin/env python3
"""Validate design document YAML frontmatter.

CLI tool that validates markdown files with YAML frontmatter (delimited by ---).
Uses only Python stdlib (no PyYAML or external dependencies).

Usage:
    python amaa_design_validate.py FILE [--project-root PATH] [--format {json,text}] [--verbose]
    python amaa_design_validate.py --all [--type TYPE] [--project-root PATH] [--format {json,text}] [--verbose]

Exit codes:
    0 - All validated documents are valid
    1 - One or more documents have errors, or no files found
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Required frontmatter fields that must be present in every design document
REQUIRED_FIELDS = ["uuid", "title", "status", "created", "updated"]

# Valid status values (case-insensitive matching)
VALID_STATUSES = ["draft", "review", "approved", "implemented", "deprecated", "rejected"]

# Regex pattern for GUUID format: GUUID-YYYYMMDD-NNNN
GUUID_PATTERN = re.compile(r"^GUUID-\d{8}-\d{4}$")

# Regex pattern for ISO date format: YYYY-MM-DD
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file.

    The file must start with '---' on line 1, and have a closing '---'
    on a subsequent line. Between them, each line is 'key: value'.
    Quoted values have surrounding quotes stripped.

    Args:
        filepath: Path to the markdown file to parse.

    Returns:
        A dict of frontmatter key-value pairs, or None if no valid
        frontmatter is found.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, IOError):
        return None

    if not lines or lines[0].strip() != "---":
        return None

    # Find the closing --- delimiter
    closing_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing_index = i
            break

    if closing_index is None:
        return None

    # Parse key: value pairs between the delimiters
    frontmatter = {}
    for line in lines[1:closing_index]:
        line = line.strip()
        if not line:
            continue
        # Split on first colon only
        colon_pos = line.find(":")
        if colon_pos == -1:
            continue
        key = line[:colon_pos].strip()
        value = line[colon_pos + 1:].strip()
        # Strip surrounding quotes from the value
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        frontmatter[key] = value

    return frontmatter


def validate_uuid(uuid_value):
    """Validate that the UUID follows GUUID-YYYYMMDD-NNNN format.

    The prefix must be exactly 'GUUID', the date must be 8 digits,
    and the sequence must be exactly 4 digits >= 0001.

    Args:
        uuid_value: The UUID string to validate.

    Returns:
        An error message string if invalid, or None if valid.
    """
    if not GUUID_PATTERN.match(uuid_value):
        return f"Invalid UUID format: '{uuid_value}' (expected GUUID-YYYYMMDD-NNNN)"
    # Check that the sequence number is not 0000
    sequence = uuid_value.split("-")[-1]
    if sequence == "0000":
        return f"Invalid UUID sequence: '{uuid_value}' (sequence must be >= 0001)"
    return None


def validate_status(status_value):
    """Validate that the status is one of the allowed values.

    Matching is case-insensitive.

    Args:
        status_value: The status string to validate.

    Returns:
        An error message string if invalid, or None if valid.
    """
    if status_value.lower() not in VALID_STATUSES:
        return f"Invalid status: '{status_value}' (valid: {', '.join(VALID_STATUSES)})"
    return None


def validate_date(date_value, field_name):
    """Validate that a date string follows YYYY-MM-DD format.

    Args:
        date_value: The date string to validate.
        field_name: Name of the field (for error messages).

    Returns:
        An error message string if invalid, or None if valid.
    """
    if not DATE_PATTERN.match(date_value):
        return f"Invalid date format for '{field_name}': '{date_value}' (expected YYYY-MM-DD)"
    return None


def validate_document(filepath):
    """Validate a single design document's YAML frontmatter.

    Checks for:
    - Presence of YAML frontmatter
    - All required fields present
    - UUID format (GUUID-YYYYMMDD-NNNN, sequence >= 0001)
    - Status value (must be one of the valid statuses)
    - Date format for created and updated fields (YYYY-MM-DD)

    Args:
        filepath: Path to the markdown file to validate.

    Returns:
        A list of error message strings. Empty list means valid.
    """
    errors = []
    filepath = str(filepath)

    frontmatter = parse_frontmatter(filepath)
    if frontmatter is None:
        errors.append("No frontmatter found (missing '---' delimiters)")
        return errors

    # Check for required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # If uuid is present, validate its format
    if "uuid" in frontmatter:
        uuid_error = validate_uuid(frontmatter["uuid"])
        if uuid_error:
            errors.append(uuid_error)

    # If status is present, validate its value
    if "status" in frontmatter:
        status_error = validate_status(frontmatter["status"])
        if status_error:
            errors.append(status_error)

    # Validate date fields if present
    for date_field in ("created", "updated"):
        if date_field in frontmatter:
            date_error = validate_date(frontmatter[date_field], date_field)
            if date_error:
                errors.append(date_error)

    return errors


def collect_files(design_dir, type_filter=None):
    """Collect all .md files from the design directory.

    Args:
        design_dir: Path to the design/ directory.
        type_filter: If set, only collect files from design/<type_filter>/.

    Returns:
        A sorted list of Path objects for .md files found.
    """
    if not design_dir.is_dir():
        return []

    if type_filter:
        search_dir = design_dir / type_filter
        if not search_dir.is_dir():
            return []
        md_files = sorted(search_dir.rglob("*.md"))
    else:
        md_files = sorted(design_dir.rglob("*.md"))

    return md_files


def format_json_output(total, passed, failed, error_details):
    """Format validation results as JSON.

    Args:
        total: Total number of documents validated.
        passed: Number of documents that passed.
        failed: Number of documents that failed.
        error_details: List of dicts with 'file' and 'error' keys.

    Returns:
        A JSON string with the results.
    """
    result = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": error_details,
    }
    return json.dumps(result, indent=2)


def format_text_output(total, passed, failed, error_details, verbose=False):
    """Format validation results as human-readable text.

    Args:
        total: Total number of documents validated.
        passed: Number of documents that passed.
        failed: Number of documents that failed.
        error_details: List of dicts with 'file' and 'error' keys.
        verbose: If True, show extra details about passing files.

    Returns:
        A text string with the results.
    """
    lines = []
    lines.append(f"Validated {total} document(s): {passed} passed, {failed} failed.")

    if error_details:
        for err in error_details:
            lines.append(f"  [FAIL] {err['file']}: {err['error']}")

    if verbose and passed > 0:
        lines.append(f"  ({passed} document(s) passed validation)")

    return "\n".join(lines)


def main():
    """Main entry point for the design document validator CLI."""
    parser = argparse.ArgumentParser(
        description="Validate design document YAML frontmatter.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Path to a single .md file to validate.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="validate_all",
        help="Validate all .md files under design/ directory.",
    )
    parser.add_argument(
        "--type",
        default=None,
        dest="doc_type",
        help="When used with --all, only validate files under design/<TYPE>/.",
    )
    parser.add_argument(
        "--project-root",
        default=None,
        help="Root directory to find design/ folder (default: cwd).",
    )
    parser.add_argument(
        "--design-dir",
        default=None,
        help="Alternative path to design directory (overrides project-root-based detection).",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default=None,
        dest="output_format",
        help="Output format (default: json for single file, text for --all).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show extra details (e.g., passing files in text mode).",
    )

    args = parser.parse_args()

    # Determine the project root directory
    project_root = Path(args.project_root) if args.project_root else Path.cwd()

    # Determine the design directory
    if args.design_dir:
        design_dir = Path(args.design_dir)
    else:
        design_dir = project_root / "design"

    # Determine output format: default is json for single file, text for --all
    if args.output_format:
        output_format = args.output_format
    elif args.validate_all:
        output_format = "text"
    else:
        output_format = "json"

    # Collect files to validate
    files_to_validate = []

    if args.validate_all:
        files_to_validate = collect_files(design_dir, type_filter=args.doc_type)
        if not files_to_validate:
            # No files found - report and exit
            if output_format == "json":
                print(format_json_output(0, 0, 0, []))
            else:
                print("Validated 0 document(s): 0 passed, 0 failed.")
            sys.exit(1)
    elif args.file:
        filepath = Path(args.file)
        if not filepath.is_file():
            if output_format == "json":
                print(format_json_output(0, 0, 1, [{"file": str(filepath), "error": "File not found"}]))
            else:
                print(f"Error: File not found: {filepath}")
            sys.exit(1)
        files_to_validate = [filepath]
    else:
        parser.print_help()
        sys.exit(1)

    # Validate all collected files
    total = len(files_to_validate)
    passed = 0
    failed = 0
    error_details = []

    for fpath in files_to_validate:
        errors = validate_document(fpath)
        if errors:
            failed += 1
            for err in errors:
                error_details.append({"file": str(fpath), "error": err})
        else:
            passed += 1

    # Output results
    if output_format == "json":
        print(format_json_output(total, passed, failed, error_details))
    else:
        print(format_text_output(total, passed, failed, error_details, verbose=args.verbose))

    # Exit code: 0 if all valid, 1 if any errors
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
