#!/usr/bin/env python3
"""Tests for amaa_github_issue_create.py (issue #14, M10).

The audit found this script built GitHub issue bodies that did NOT begin with
the PRRD G1.1 self-identification line — a G1.1 violation in shipped code, since
every AI Maestro agent shares the single human-owner gh identity. These tests
assert the body extracted by extract_issue_data() leads with the self-id line.

They import the real functions/constants from the script (no mocks) and exercise
extract_issue_data() with representative frontmatter.
"""

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
SCRIPT = SCRIPTS_DIR / "amaa_github_issue_create.py"


def load_module():
    """Import amaa_github_issue_create.py as a module to read its real symbols."""
    # Replicate the runtime path. These scripts are standalone executables run as
    # `uv run python scripts/<name>.py`, where Python puts the script's own
    # directory on sys.path[0] — which is how the sibling `amaa_self_id` import
    # (the shared PRRD G1.1 byline) resolves in production. importlib does NOT
    # do that, so without this the test fails on a script that runs correctly.
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location("amaa_github_issue_create", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_self_id_line_constant_present():
    """The script must define a non-empty G1.1 self-id constant."""
    module = load_module()
    assert hasattr(module, "SELF_ID_LINE")
    assert module.SELF_ID_LINE.strip()
    # G1.1 self-id must name the plugin/role so the human owner can tell agents apart.
    assert "ai-maestro-architect-agent" in module.SELF_ID_LINE


def test_issue_body_starts_with_self_id_line():
    """extract_issue_data() must put the self-id line first in the body."""
    module = load_module()
    frontmatter = {
        "title": "Test Design",
        "uuid": "PROJ-SPEC-20260611-a1b2c3d4",
        "type": "spec",
        "status": "draft",
        "created": "2026-06-11",
        "author": "AMAA",
    }
    body = "## 1. Overview\n\nA test overview.\n"
    data = module.extract_issue_data(frontmatter, body, Path("design/spec/test.md"))
    assert data["body"].startswith(module.SELF_ID_LINE), (
        "issue body must begin with the G1.1 self-id line; got:\n"
        + data["body"][:120]
    )


def test_self_id_line_precedes_design_heading():
    """The self-id line must come before the '## Design Document' heading."""
    module = load_module()
    frontmatter = {"title": "T", "uuid": "PROJ-SPEC-20260611-00000000"}
    data = module.extract_issue_data(frontmatter, "", Path("design/spec/t.md"))
    lines = data["body"].splitlines()
    self_id_idx = lines.index(module.SELF_ID_LINE)
    heading_idx = next(
        i for i, ln in enumerate(lines) if ln.startswith("## Design Document")
    )
    assert self_id_idx < heading_idx
