#!/usr/bin/env python3
"""Tests for eaa_design_create.py - Design document creation script.

Tests cover:
- CLI argument parsing
- GUUID generation with correct format
- Frontmatter population
- Template loading (built-in default)
- File creation in correct subdirectory
- Custom filename support
- Error handling for invalid types
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Path to the script under test
SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "eaa_design_create.py"

# Valid document types as defined in the SKILL.md
VALID_TYPES = ["pdr", "spec", "feature", "decision", "architecture", "template"]

# GUUID format: GUUID-YYYYMMDD-NNNN
GUUID_PATTERN = re.compile(r"^GUUID-\d{8}-\d{4}$")


def run_script(*args, cwd=None):
    """Run eaa_design_create.py with given arguments and return result."""
    cmd = [sys.executable, str(SCRIPT_PATH)] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=30,
    )
    return result


@pytest.fixture
def project_dir(tmp_path):
    """Create a temporary project directory for testing."""
    return tmp_path


class TestCLIArguments:
    """Test CLI argument parsing and validation."""

    def test_requires_type_argument(self, project_dir):
        """Script must fail when --type is not provided."""
        result = run_script("--title", "Test Doc", "--project-root", str(project_dir))
        assert result.returncode != 0

    def test_requires_title_argument(self, project_dir):
        """Script must fail when --title is not provided."""
        result = run_script("--type", "pdr", "--project-root", str(project_dir))
        assert result.returncode != 0

    def test_rejects_invalid_type(self, project_dir):
        """Script must reject invalid document types."""
        result = run_script(
            "--type", "invalid_type",
            "--title", "Test",
            "--project-root", str(project_dir),
        )
        assert result.returncode != 0
        assert "invalid" in result.stderr.lower() or "invalid" in result.stdout.lower()

    def test_accepts_all_valid_types(self, project_dir):
        """Script must accept all six valid document types."""
        for doc_type in VALID_TYPES:
            result = run_script(
                "--type", doc_type,
                "--title", f"Test {doc_type}",
                "--project-root", str(project_dir),
            )
            assert result.returncode == 0, (
                f"Type '{doc_type}' rejected. stderr: {result.stderr}"
            )

    def test_help_flag(self):
        """Script must show help text with --help."""
        result = run_script("--help")
        assert result.returncode == 0
        assert "--type" in result.stdout
        assert "--title" in result.stdout


class TestDocumentCreation:
    """Test that documents are created correctly."""

    def test_creates_file_in_correct_directory(self, project_dir):
        """Document must be created in design/<type>/ directory."""
        result = run_script(
            "--type", "pdr",
            "--title", "Auth Design",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0
        pdr_dir = project_dir / "design" / "pdr"
        assert pdr_dir.exists(), "design/pdr/ directory was not created"
        md_files = list(pdr_dir.glob("*.md"))
        assert len(md_files) == 1, f"Expected 1 file, found {len(md_files)}"

    def test_creates_directory_if_missing(self, project_dir):
        """Script must create the design/<type>/ directory if it does not exist."""
        result = run_script(
            "--type", "spec",
            "--title", "API Spec",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0
        assert (project_dir / "design" / "spec").is_dir()

    def test_file_contains_yaml_frontmatter(self, project_dir):
        """Created file must have YAML frontmatter between --- markers."""
        run_script(
            "--type", "feature",
            "--title", "OAuth Feature",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "feature").glob("*.md"))
        assert len(md_files) == 1
        content = md_files[0].read_text(encoding="utf-8")
        assert content.startswith("---\n"), "File must start with --- frontmatter marker"
        # Find second --- marker
        second_marker = content.index("---", 3)
        assert second_marker > 3, "Must have closing --- frontmatter marker"

    def test_frontmatter_contains_required_fields(self, project_dir):
        """Frontmatter must contain uuid, title, status, created, updated fields."""
        run_script(
            "--type", "pdr",
            "--title", "Test PDR",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")

        required_fields = ["uuid", "title", "status", "created", "updated"]
        for field_name in required_fields:
            assert re.search(
                rf"^{field_name}:", content, re.MULTILINE
            ), f"Missing required field: {field_name}"

    def test_frontmatter_uuid_is_guuid_format(self, project_dir):
        """The uuid field must use GUUID-YYYYMMDD-NNNN format."""
        run_script(
            "--type", "pdr",
            "--title", "UUID Test",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        match = re.search(r"^uuid:\s*(.+)$", content, re.MULTILINE)
        assert match, "uuid field not found in frontmatter"
        uuid_value = match.group(1).strip().strip('"').strip("'")
        assert GUUID_PATTERN.match(uuid_value), (
            f"UUID '{uuid_value}' does not match GUUID-YYYYMMDD-NNNN format"
        )

    def test_frontmatter_status_is_draft(self, project_dir):
        """New documents must have status: draft."""
        run_script(
            "--type", "decision",
            "--title", "DB Choice",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "decision").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        match = re.search(r"^status:\s*(.+)$", content, re.MULTILINE)
        assert match
        assert match.group(1).strip() == "draft"

    def test_frontmatter_title_matches_input(self, project_dir):
        """The title field must match the --title argument."""
        run_script(
            "--type", "spec",
            "--title", "My API Specification",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "spec").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        match = re.search(r"^title:\s*(.+)$", content, re.MULTILINE)
        assert match
        title_value = match.group(1).strip().strip('"').strip("'")
        assert title_value == "My API Specification"

    def test_frontmatter_type_matches_input(self, project_dir):
        """The type field must match the --type argument."""
        run_script(
            "--type", "architecture",
            "--title", "System Arch",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "architecture").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        match = re.search(r"^type:\s*(.+)$", content, re.MULTILINE)
        assert match
        assert match.group(1).strip() == "architecture"


class TestGUUIDGeneration:
    """Test GUUID generation and sequencing."""

    def test_guuid_has_todays_date(self, project_dir):
        """Generated GUUID must contain today's date in YYYYMMDD format."""
        from datetime import datetime
        today = datetime.now().strftime("%Y%m%d")

        run_script(
            "--type", "pdr",
            "--title", "Date Test",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        match = re.search(r"^uuid:\s*(.+)$", content, re.MULTILINE)
        uuid_value = match.group(1).strip().strip('"').strip("'")
        assert today in uuid_value, f"Expected today's date {today} in UUID {uuid_value}"

    def test_guuid_sequence_starts_at_0001(self, project_dir):
        """First document of the day must have sequence 0001."""
        run_script(
            "--type", "pdr",
            "--title", "First Doc",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        match = re.search(r"^uuid:\s*(.+)$", content, re.MULTILINE)
        uuid_value = match.group(1).strip().strip('"').strip("'")
        assert uuid_value.endswith("-0001"), (
            f"First UUID should end with -0001, got {uuid_value}"
        )

    def test_guuid_sequence_increments(self, project_dir):
        """Second document on same day must have sequence 0002."""
        run_script(
            "--type", "pdr",
            "--title", "First",
            "--project-root", str(project_dir),
        )
        run_script(
            "--type", "pdr",
            "--title", "Second",
            "--project-root", str(project_dir),
        )
        md_files = sorted((project_dir / "design" / "pdr").glob("*.md"))
        assert len(md_files) == 2

        # Check both files have different sequence numbers
        uuids = []
        for f in md_files:
            content = f.read_text(encoding="utf-8")
            match = re.search(r"^uuid:\s*(.+)$", content, re.MULTILINE)
            uuids.append(match.group(1).strip().strip('"').strip("'"))

        sequences = [u.split("-")[-1] for u in uuids]
        assert "0001" in sequences
        assert "0002" in sequences


class TestFilenameGeneration:
    """Test filename generation including custom filenames."""

    def test_default_filename_contains_guuid(self, project_dir):
        """Default filename must contain the GUUID."""
        run_script(
            "--type", "pdr",
            "--title", "Test File",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        assert len(md_files) == 1
        filename = md_files[0].name
        assert "GUUID-" in filename, f"Filename should contain GUUID: {filename}"

    def test_default_filename_contains_slugified_title(self, project_dir):
        """Default filename must contain a slugified version of the title."""
        run_script(
            "--type", "pdr",
            "--title", "User Authentication Redesign",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        filename = md_files[0].name.lower()
        assert "user-authentication-redesign" in filename, (
            f"Filename should contain slugified title: {filename}"
        )

    def test_custom_filename(self, project_dir):
        """Custom --filename must be used instead of auto-generated name."""
        run_script(
            "--type", "decision",
            "--title", "DB Selection",
            "--filename", "adr-001-database-selection",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "decision").glob("*.md"))
        assert len(md_files) == 1
        assert md_files[0].name == "adr-001-database-selection.md"

    def test_filename_has_md_extension(self, project_dir):
        """Output file must always have .md extension."""
        run_script(
            "--type", "pdr",
            "--title", "Extension Test",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        assert len(md_files) == 1
        assert md_files[0].suffix == ".md"


class TestAuthorField:
    """Test optional --author argument."""

    def test_author_in_frontmatter_when_provided(self, project_dir):
        """Author field must appear in frontmatter when --author is given."""
        run_script(
            "--type", "pdr",
            "--title", "Author Test",
            "--author", "John Doe",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        match = re.search(r"^author:\s*(.+)$", content, re.MULTILINE)
        assert match
        author_value = match.group(1).strip().strip('"').strip("'")
        assert author_value == "John Doe"

    def test_author_defaults_to_empty(self, project_dir):
        """Author field must default to empty string when not provided."""
        run_script(
            "--type", "pdr",
            "--title", "No Author Test",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        match = re.search(r"^author:\s*(.*)$", content, re.MULTILINE)
        assert match
        author_value = match.group(1).strip().strip('"').strip("'")
        assert author_value == ""


class TestOutputMessages:
    """Test script output messages."""

    def test_outputs_created_file_path(self, project_dir):
        """Script must output the path of the created file."""
        result = run_script(
            "--type", "pdr",
            "--title", "Output Test",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0
        assert "Created:" in result.stdout or "design/pdr/" in result.stdout

    def test_outputs_uuid(self, project_dir):
        """Script must output the generated UUID."""
        result = run_script(
            "--type", "pdr",
            "--title", "UUID Output Test",
            "--project-root", str(project_dir),
        )
        assert result.returncode == 0
        assert "GUUID-" in result.stdout


class TestDocumentBodyTemplate:
    """Test that the document body contains template sections."""

    def test_body_has_heading_with_title(self, project_dir):
        """Document body must contain an H1 heading with the title."""
        run_script(
            "--type", "pdr",
            "--title", "My Feature Design",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        assert "# My Feature Design" in content

    def test_body_has_overview_section(self, project_dir):
        """Document body must contain an Overview section."""
        run_script(
            "--type", "pdr",
            "--title", "Body Test",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        assert "## Overview" in content

    def test_body_has_standard_sections(self, project_dir):
        """Document body must contain standard sections from the template."""
        run_script(
            "--type", "pdr",
            "--title", "Sections Test",
            "--project-root", str(project_dir),
        )
        md_files = list((project_dir / "design" / "pdr").glob("*.md"))
        content = md_files[0].read_text(encoding="utf-8")
        expected_sections = ["## Overview", "## Background", "## Requirements"]
        for section in expected_sections:
            assert section in content, f"Missing section: {section}"
