#!/usr/bin/env python3
"""Tests for amaa_design_validate.py - Design document validation script.

Tests cover:
- CLI argument parsing (single file, --all, --type, --verbose, --format)
- YAML frontmatter parsing
- Required fields validation (uuid, title, status, created, updated)
- GUUID format validation
- Status value validation
- Type value validation
- Date format validation
- Bulk validation (--all)
- Output formats (text and json)
- Exit codes (0 for valid, 1 for errors)
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# Path to the script under test
SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "amaa_design_validate.py"

# Valid statuses from the SKILL.md
VALID_STATUSES = ["draft", "review", "approved", "implemented", "deprecated", "rejected"]

# Valid types from the SKILL.md
VALID_TYPES = ["pdr", "spec", "feature", "decision", "architecture", "template"]


def run_script(*args, cwd=None):
    """Run amaa_design_validate.py with given arguments and return result."""
    cmd = [sys.executable, str(SCRIPT_PATH)] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=30,
    )
    return result


def create_design_doc(directory, filename, frontmatter_lines):
    """Create a test design document with given frontmatter.

    Args:
        directory: Parent directory (e.g., tmp_path / "design" / "pdr")
        filename: Filename for the document
        frontmatter_lines: List of key: value strings for frontmatter
    """
    directory.mkdir(parents=True, exist_ok=True)
    filepath = directory / filename
    frontmatter = "---\n" + "\n".join(frontmatter_lines) + "\n---\n\n# Test Document\n"
    filepath.write_text(frontmatter, encoding="utf-8")
    return filepath


@pytest.fixture
def project_dir(tmp_path):
    """Create a temporary project directory for testing."""
    return tmp_path


@pytest.fixture
def valid_doc(project_dir):
    """Create a valid design document with all required fields."""
    return create_design_doc(
        project_dir / "design" / "pdr",
        "GUUID-20260130-0001-test-doc.md",
        [
            "uuid: GUUID-20260130-0001",
            'title: "Test Document"',
            "status: draft",
            "created: 2026-01-30",
            "updated: 2026-01-30",
            "type: pdr",
            'author: "Test Author"',
        ],
    )


@pytest.fixture
def invalid_doc_missing_uuid(project_dir):
    """Create a document missing the uuid field."""
    return create_design_doc(
        project_dir / "design" / "pdr",
        "bad-doc.md",
        [
            'title: "Missing UUID"',
            "status: draft",
            "created: 2026-01-30",
            "updated: 2026-01-30",
        ],
    )


@pytest.fixture
def invalid_doc_bad_uuid(project_dir):
    """Create a document with invalid UUID format."""
    return create_design_doc(
        project_dir / "design" / "pdr",
        "bad-uuid-doc.md",
        [
            "uuid: 12345",
            'title: "Bad UUID"',
            "status: draft",
            "created: 2026-01-30",
            "updated: 2026-01-30",
        ],
    )


class TestCLIArguments:
    """Test CLI argument parsing."""

    def test_help_flag(self):
        """Script must show help text with --help."""
        result = run_script("--help")
        assert result.returncode == 0
        assert "--all" in result.stdout or "all" in result.stdout.lower()

    def test_accepts_single_file_argument(self, valid_doc, project_dir):
        """Script must accept a single file path as argument."""
        result = run_script(
            str(valid_doc),
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0

    def test_accepts_all_flag(self, valid_doc, project_dir):
        """Script must accept --all flag for bulk validation."""
        result = run_script(
            "--all",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0

    def test_accepts_type_filter_with_all(self, valid_doc, project_dir):
        """Script must accept --type filter with --all flag."""
        result = run_script(
            "--all",
            "--type", "pdr",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0

    def test_accepts_verbose_flag(self, valid_doc, project_dir):
        """Script must accept --verbose flag."""
        result = run_script(
            str(valid_doc),
            "--verbose",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0

    def test_accepts_format_text(self, valid_doc, project_dir):
        """Script must accept --format text."""
        result = run_script(
            str(valid_doc),
            "--format", "text",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0

    def test_accepts_format_json(self, valid_doc, project_dir):
        """Script must accept --format json and produce valid JSON."""
        result = run_script(
            str(valid_doc),
            "--format", "json",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0
        parsed = json.loads(result.stdout)
        assert isinstance(parsed, dict)


class TestValidDocument:
    """Test validation of a valid document."""

    def test_valid_doc_passes(self, valid_doc, project_dir):
        """A document with all required fields in correct format must pass."""
        result = run_script(
            str(valid_doc),
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0

    def test_valid_doc_reports_pass(self, valid_doc, project_dir):
        """Output must indicate the document passed validation."""
        result = run_script(
            str(valid_doc),
            "--project-root", str(project_dir),
        )
        output = result.stdout.lower()
        assert "pass" in output or "0 error" in output or "valid" in output


class TestMissingFields:
    """Test detection of missing required fields."""

    def test_missing_uuid_detected(self, project_dir):
        """Missing uuid field must be reported as error."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "no-uuid.md",
            [
                'title: "No UUID"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1
        assert "uuid" in result.stdout.lower() or "uuid" in result.stderr.lower()

    def test_missing_title_detected(self, project_dir):
        """Missing title field must be reported as error."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "no-title.md",
            [
                "uuid: GUUID-20260130-0001",
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1
        assert "title" in result.stdout.lower() or "title" in result.stderr.lower()

    def test_missing_status_detected(self, project_dir):
        """Missing status field must be reported as error."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "no-status.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "No Status"',
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1

    def test_missing_created_detected(self, project_dir):
        """Missing created field must be reported as error."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "no-created.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "No Created"',
                "status: draft",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1

    def test_missing_updated_detected(self, project_dir):
        """Missing updated field must be reported as error."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "no-updated.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "No Updated"',
                "status: draft",
                "created: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1


class TestUUIDValidation:
    """Test UUID format validation."""

    def test_valid_guuid_accepted(self, project_dir):
        """GUUID-YYYYMMDD-NNNN format must be accepted."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "good-uuid.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "Good UUID"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 0

    def test_numeric_uuid_rejected(self, project_dir):
        """Plain numeric UUID must be rejected."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "num-uuid.md",
            [
                "uuid: 12345",
                'title: "Numeric UUID"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1

    def test_wrong_prefix_rejected(self, project_dir):
        """UUID with wrong prefix (not GUUID-) must be rejected."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "wrong-prefix.md",
            [
                "uuid: UUID-20260130-0001",
                'title: "Wrong Prefix"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1

    def test_sequence_0000_rejected(self, project_dir):
        """Sequence number 0000 must be rejected (must start at 0001)."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "zero-seq.md",
            [
                "uuid: GUUID-20260130-0000",
                'title: "Zero Sequence"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1


class TestStatusValidation:
    """Test status value validation."""

    def test_valid_statuses_accepted(self, project_dir):
        """All valid status values must be accepted."""
        for i, status in enumerate(VALID_STATUSES, start=1):
            doc = create_design_doc(
                project_dir / "design" / "pdr",
                f"status-{status}.md",
                [
                    f"uuid: GUUID-20260130-{i:04d}",
                    f'title: "Status {status}"',
                    f"status: {status}",
                    "created: 2026-01-30",
                    "updated: 2026-01-30",
                ],
            )
            result = run_script(str(doc), "--project-root", str(project_dir))
            assert result.returncode == 0, (
                f"Valid status '{status}' was rejected. stderr: {result.stderr}"
            )

    def test_invalid_status_rejected(self, project_dir):
        """Invalid status value must be reported as error."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "bad-status.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "Bad Status"',
                "status: bogus",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1


class TestDateValidation:
    """Test date format validation."""

    def test_valid_date_accepted(self, project_dir):
        """YYYY-MM-DD date format must be accepted."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "good-date.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "Good Date"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 0

    def test_wrong_date_format_rejected(self, project_dir):
        """Non-ISO date format must be rejected."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "bad-date.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "Bad Date"',
                "status: draft",
                "created: January 30, 2026",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1


class TestNoFrontmatter:
    """Test handling of documents without frontmatter."""

    def test_no_frontmatter_detected(self, project_dir):
        """A file without YAML frontmatter must be reported as error."""
        doc_dir = project_dir / "design" / "pdr"
        doc_dir.mkdir(parents=True, exist_ok=True)
        doc = doc_dir / "no-frontmatter.md"
        doc.write_text("# Just a heading\n\nNo frontmatter here.\n", encoding="utf-8")
        result = run_script(str(doc), "--project-root", str(project_dir))
        assert result.returncode == 1
        output = (result.stdout + result.stderr).lower()
        assert "frontmatter" in output or "no frontmatter" in output or "missing" in output


class TestBulkValidation:
    """Test --all flag for bulk validation."""

    def test_all_scans_design_directory(self, project_dir):
        """--all must scan all .md files under design/ subdirectories."""
        create_design_doc(
            project_dir / "design" / "pdr",
            "doc1.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "Doc 1"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        create_design_doc(
            project_dir / "design" / "spec",
            "doc2.md",
            [
                "uuid: GUUID-20260130-0002",
                'title: "Doc 2"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(
            "--all",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0
        # Output should mention both files or a count of 2
        output = result.stdout
        assert "2" in output  # Should report 2 files validated

    def test_type_filter_limits_scope(self, project_dir):
        """--type filter with --all must only validate that type's directory."""
        create_design_doc(
            project_dir / "design" / "pdr",
            "pdr-doc.md",
            [
                "uuid: GUUID-20260130-0001",
                'title: "PDR Doc"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        # Create an invalid spec doc
        create_design_doc(
            project_dir / "design" / "spec",
            "bad-spec.md",
            [
                'title: "Bad Spec (no uuid)"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        # Validate only pdr type - should pass because pdr doc is valid
        result = run_script(
            "--all",
            "--type", "pdr",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0

    def test_all_with_no_design_dir(self, project_dir):
        """--all with no design/ directory must report no files found."""
        result = run_script(
            "--all",
            "--project-root", str(project_dir),
        )
        # Should not crash; should report 0 files or "no files"
        output = (result.stdout + result.stderr).lower()
        assert "0" in output or "no" in output or "not found" in output


class TestJSONOutput:
    """Test --format json output structure."""

    def test_json_output_has_total(self, valid_doc, project_dir):
        """JSON output must include total count."""
        result = run_script(
            str(valid_doc),
            "--format", "json",
            "--project-root", str(project_dir),
        )
        parsed = json.loads(result.stdout)
        assert "total" in parsed

    def test_json_output_has_passed(self, valid_doc, project_dir):
        """JSON output must include passed count."""
        result = run_script(
            str(valid_doc),
            "--format", "json",
            "--project-root", str(project_dir),
        )
        parsed = json.loads(result.stdout)
        assert "passed" in parsed

    def test_json_output_has_errors_list(self, project_dir):
        """JSON output must include errors list when errors found."""
        doc = create_design_doc(
            project_dir / "design" / "pdr",
            "bad.md",
            [
                'title: "No UUID"',
                "status: draft",
                "created: 2026-01-30",
                "updated: 2026-01-30",
            ],
        )
        result = run_script(
            str(doc),
            "--format", "json",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 1
        parsed = json.loads(result.stdout)
        assert "errors" in parsed
        assert len(parsed["errors"]) > 0


class TestExitCodes:
    """Test that exit codes are correct."""

    def test_exit_0_on_valid(self, valid_doc, project_dir):
        """Exit code must be 0 when all documents are valid."""
        result = run_script(str(valid_doc), "--project-root", str(project_dir))
        assert result.returncode == 0

    def test_exit_1_on_errors(self, invalid_doc_missing_uuid, project_dir):
        """Exit code must be 1 when errors are found."""
        result = run_script(
            str(invalid_doc_missing_uuid),
            "--project-root", str(project_dir),
        )
        assert result.returncode == 1

    def test_exit_1_on_bad_uuid(self, invalid_doc_bad_uuid, project_dir):
        """Exit code must be 1 when UUID format is invalid."""
        result = run_script(
            str(invalid_doc_bad_uuid),
            "--project-root", str(project_dir),
        )
        assert result.returncode == 1
