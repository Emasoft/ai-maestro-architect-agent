#!/usr/bin/env python3
"""Tests for the redesign loop (issue #14, M7).

The redesign loop is the IMPLEMENTING -> REVIEW re-entry edge that lets the
ARCHITECT pull a design back into review when a flaw surfaces mid-dev. Before
this edge existed the design state machine was a one-way street and a surfaced
design problem had nowhere to go.

These tests assert the edge is real in THREE places that must stay in sync:
  1. the runtime enforcement table (VALID_TRANSITIONS in amaa_design_lifecycle.py)
  2. the state-machine docs (design-states.md, op-manage-state-transitions.md)
  3. the three dialog-loop templates that feed the loop

They import the real module constant (the same table update_status() consults at
runtime) — no mocks — and read the real shipped docs/templates.
"""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
LIFECYCLE_SCRIPT = REPO_ROOT / "scripts" / "amaa_design_lifecycle.py"
SKILL_REFS = REPO_ROOT / "skills" / "amaa-design-lifecycle" / "references"
SKILL_TEMPLATES = REPO_ROOT / "skills" / "amaa-design-lifecycle" / "templates"


def load_lifecycle_module():
    """Import amaa_design_lifecycle.py as a module to read its real constants."""
    spec = importlib.util.spec_from_file_location(
        "amaa_design_lifecycle", LIFECYCLE_SCRIPT
    )
    assert spec is not None and spec.loader is not None, (
        f"could not load module spec for {LIFECYCLE_SCRIPT}"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestRuntimeTransitionTable:
    """The redesign edge must exist in the table the script actually enforces."""

    def test_implemented_can_re_enter_review(self):
        """VALID_TRANSITIONS must allow implemented -> review (the redesign loop)."""
        module = load_lifecycle_module()
        assert "review" in module.VALID_TRANSITIONS["implemented"], (
            "redesign loop missing: a design being implemented cannot return to "
            "review, so a mid-dev design flaw has nowhere to go"
        )

    def test_review_is_a_valid_status(self):
        """review must be a known status (target of the redesign edge)."""
        module = load_lifecycle_module()
        assert "review" in module.VALID_STATUSES

    def test_terminal_states_stay_terminal(self):
        """The redesign edge must not accidentally open up terminal states."""
        module = load_lifecycle_module()
        assert module.VALID_TRANSITIONS["deprecated"] == set()
        assert module.VALID_TRANSITIONS["superseded"] == set()
        assert module.VALID_TRANSITIONS["archived"] == set()

    def test_happy_path_intact(self):
        """Adding the re-entry edge must not break the forward path."""
        module = load_lifecycle_module()
        t = module.VALID_TRANSITIONS
        assert "review" in t["draft"]
        assert "approved" in t["review"]
        assert "implemented" in t["approved"]


class TestDocsEncodeTheEdge:
    """The state-machine docs must document the same edge (no code/doc drift)."""

    def test_design_states_doc_has_re_entry(self):
        """design-states.md must show IMPLEMENTING -> REVIEW."""
        text = (SKILL_REFS / "design-states.md").read_text(encoding="utf-8")
        assert "REVIEW" in text and "redesign" in text.lower()
        assert "IMPLEMENTING" in text

    def test_transitions_doc_has_re_entry_rule(self):
        """op-manage-state-transitions.md must carry the redesign-loop rule."""
        text = (SKILL_REFS / "op-manage-state-transitions.md").read_text(
            encoding="utf-8"
        )
        assert "IMPLEMENTING to REVIEW" in text or "IMPLEMENTING → REVIEW" in text
        assert "redesign" in text.lower()

    def test_transitions_matrix_allows_implementing_to_review(self):
        """The transition matrix row for IMPLEMENTING must mark To REVIEW = YES."""
        text = (SKILL_REFS / "op-manage-state-transitions.md").read_text(
            encoding="utf-8"
        )
        # Two tables have a row starting "| IMPLEMENTING": the State Definitions
        # table (3 cols) and the State Transition Matrix (6 YES/NO/- columns).
        # Select the matrix row: the one whose data cells are only YES/NO/-.
        matrix_row = None
        for line in text.splitlines():
            if not line.strip().startswith("| IMPLEMENTING"):
                continue
            cells = [c.strip() for c in line.split("|")][1:-1]  # drop edge empties
            if len(cells) >= 6 and set(cells[1:]) <= {"YES", "NO", "-"}:
                matrix_row = cells
                break
        assert matrix_row is not None, "IMPLEMENTING matrix row not found"
        # cells: [From=IMPLEMENTING, To DRAFT, To REVIEW, To APPROVED, ...]
        assert matrix_row[2] == "YES", (
            f"To REVIEW cell was {matrix_row[2]!r}, expected YES"
        )

    def test_accept_redesign_request_op_exists(self):
        """The op doc for accepting a redesign request must ship."""
        assert (SKILL_REFS / "op-accept-redesign-request.md").is_file()


class TestDialogLoopTemplates:
    """All three dialog-loop templates must ship and name their loop."""

    @pytest.mark.parametrize(
        "filename,marker",
        [
            ("dialog-loop-comprehension-handshake.md", "comprehension handshake"),
            ("dialog-loop-in-dev-issue.md", "in-dev issue"),
            ("dialog-loop-pre-pr-gate.md", "pre-PR gate"),
        ],
    )
    def test_template_ships_and_names_its_loop(self, filename, marker):
        """Each dialog-loop template file exists and identifies its loop."""
        path = SKILL_TEMPLATES / filename
        assert path.is_file(), f"missing dialog-loop template: {filename}"
        assert marker.lower() in path.read_text(encoding="utf-8").lower()

    def test_in_dev_template_routes_design_flaw_to_arch(self):
        """The in-dev dialog must route a design flaw to ARCH (the redesign loop)."""
        text = (SKILL_TEMPLATES / "dialog-loop-in-dev-issue.md").read_text(
            encoding="utf-8"
        )
        assert "ARCH" in text
        assert "redesign" in text.lower() or "IMPLEMENTING → REVIEW" in text
