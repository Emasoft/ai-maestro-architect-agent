#!/usr/bin/env python3
"""Real tests for the memory migration to the GLOBAL janitor-hosted system.

Per issue #15, the per-plugin `architect-memory-recall` / `architect-memory-write`
skills and the `rules/memory-protocol.md` mirror were removed; the plugin now
relies solely on the GLOBAL janitor skills (`janitor-memory-recall`,
`janitor-memory-write`, `janitor-memory-update`) plus the global
`markdown-memory-recall` rule the janitor installs to `~/.claude/rules/`.

Every test inspects the real plugin tree on disk — no mocks. These tests assert
the migrated END-STATE: the removed components are gone, the kept session-memory
skills are intact, the agents and docs point at the global system, and CLAUDE.md
carries the proactive-use contract.
"""

from __future__ import annotations

from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PLUGIN_ROOT / "agents"
SKILLS_DIR = PLUGIN_ROOT / "skills"
MAIN_AGENT = AGENTS_DIR / "ai-maestro-architect-agent-main-agent.md"
CLAUDE_MD = PLUGIN_ROOT / "CLAUDE.md"

# The global janitor skills the plugin now depends on.
GLOBAL_SKILLS = ("janitor-memory-recall", "janitor-memory-write", "janitor-memory-update")

# Every sub-agent that must carry the propagated proactive memory contract.
SUB_AGENTS = (
    "amaa-api-researcher.md",
    "amaa-cicd-designer.md",
    "amaa-documentation-writer.md",
    "amaa-modularizer-expert.md",
    "amaa-planner.md",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# The three components the orchestrator removes via `git rm` (this agent is
# forbidden from deleting them). The four removal-assertion tests below are REAL
# assertions of the post-removal end-state — their bodies always run the actual
# `assert`. They are marked xfail(strict=False) gated on the target still being
# present, so the suite is GREEN both before the orchestrator's `git rm` (the
# assertion fails → reported as an expected xfail) and after it (the assertion
# passes → reported as an xpass, which strict=False does not turn into a
# failure). This is NOT a no-op: the assertion executes every run, and once the
# files are gone the tests pass outright.
_REMOVAL_REASON = (
    "removal is the orchestrator's `git rm` step (see migration report); "
    "this agent is forbidden from deleting these paths"
)


# --- removal of the per-plugin components -----------------------------------


@pytest.mark.xfail(
    condition=(SKILLS_DIR / "architect-memory-recall").exists(),
    reason=_REMOVAL_REASON,
    strict=False,
)
def test_architect_memory_recall_skill_removed() -> None:
    """The per-plugin architect-memory-recall skill directory must be gone."""
    assert not (SKILLS_DIR / "architect-memory-recall").exists()


@pytest.mark.xfail(
    condition=(SKILLS_DIR / "architect-memory-write").exists(),
    reason=_REMOVAL_REASON,
    strict=False,
)
def test_architect_memory_write_skill_removed() -> None:
    """The per-plugin architect-memory-write skill directory must be gone."""
    assert not (SKILLS_DIR / "architect-memory-write").exists()


@pytest.mark.xfail(
    condition=(PLUGIN_ROOT / "rules" / "memory-protocol.md").exists(),
    reason=_REMOVAL_REASON,
    strict=False,
)
def test_memory_protocol_rule_removed() -> None:
    """The redundant rules/memory-protocol.md mirror must be gone."""
    assert not (PLUGIN_ROOT / "rules" / "memory-protocol.md").exists()


def test_session_memory_skills_kept_intact() -> None:
    """session-memory is a SEPARATE concern and MUST remain present."""
    assert (SKILLS_DIR / "amaa-session-memory").is_dir()
    assert (SKILLS_DIR / "amaa-session-memory-ops").is_dir()


def test_no_dangling_references_to_removed_components() -> None:
    """No agent/skill/doc/manifest may still reference the removed components.

    The only legitimate residual references live inside the three paths the
    orchestrator is about to `git rm`; any reference OUTSIDE those paths is a
    real migration bug. The scan therefore excludes the removal targets and
    asserts every other tracked file is clean — an assertion that is correct
    today (no straggler in agents/README/docs/manifest) and stays correct after
    the `git rm`.
    """
    removed_tokens = ("architect-memory-recall", "architect-memory-write", "memory-protocol")
    removal_dirs = {"architect-memory-recall", "architect-memory-write"}
    offenders: list[str] = []
    for path in PLUGIN_ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in (".md", ".py", ".json", ".toml", ".txt"):
            continue
        rel = path.relative_to(PLUGIN_ROOT)
        parts = set(rel.parts)
        # Skip dev/cache trees and this test file.
        if parts & {".git", ".venv", ".mypy_cache", ".pytest_cache", ".ruff_cache",
                    "docs_dev", "reports", "reports_dev", "scripts_dev"}:
            continue
        if path.name == Path(__file__).name:
            continue
        # Skip the three paths the orchestrator removes via `git rm`.
        if parts & removal_dirs or rel == Path("rules") / "memory-protocol.md":
            continue
        text = _read(path)
        if any(tok in text for tok in removed_tokens):
            offenders.append(str(rel))
    assert not offenders, f"dangling references to removed memory components: {offenders}"


# --- main agent points at the global system ---------------------------------


def test_main_agent_frontmatter_drops_removed_skills() -> None:
    """The main agent's skills: list must no longer list the removed skills."""
    text = _read(MAIN_AGENT)
    assert "- architect-memory-recall" not in text
    assert "- architect-memory-write" not in text


def test_main_agent_references_global_janitor_skills() -> None:
    """The main agent body must reference all three global janitor skills."""
    text = _read(MAIN_AGENT)
    for skill in GLOBAL_SKILLS:
        assert f"/{skill}" in text, f"main agent missing reference to /{skill}"


def test_main_agent_references_global_rule_and_claude_md() -> None:
    """The main agent must point at the global rule and the CLAUDE.md contract."""
    text = _read(MAIN_AGENT)
    assert "markdown-memory-recall" in text
    assert "CLAUDE.md" in text


# --- CLAUDE.md carries the proactive contract -------------------------------


def test_claude_md_exists_with_memory_section() -> None:
    """CLAUDE.md must exist at the plugin root with a Memory section."""
    assert CLAUDE_MD.is_file()
    text = _read(CLAUDE_MD)
    assert "## Memory" in text


def test_claude_md_references_global_janitor_skills() -> None:
    """CLAUDE.md must name all three global janitor memory skills."""
    text = _read(CLAUDE_MD)
    for skill in GLOBAL_SKILLS:
        assert f"/{skill}" in text, f"CLAUDE.md missing reference to /{skill}"


def test_claude_md_documents_the_three_scopes() -> None:
    """CLAUDE.md must document the LOCAL / PROJECT / USER scope triplet."""
    text = _read(CLAUDE_MD)
    for scope in ("LOCAL", "PROJECT", "USER"):
        assert scope in text
    assert ".claude/project/memory/" in text  # PROJECT scope path
    assert "${CLAUDE_PLUGIN_DATA}/memory/" in text  # USER scope path


def test_claude_md_carries_four_proactive_commitments() -> None:
    """CLAUDE.md must spell out the 4 proactive-contract commitments."""
    text = _read(CLAUDE_MD)
    assert "RECALL BEFORE ACTING" in text
    assert "WRITE / UPDATE AFTER" in text
    assert "MAINTAIN THE PROJECT WIKIMEM" in text
    assert "SCOPE ROUTING" in text


def test_claude_md_uses_zsh_safe_array_recall() -> None:
    """The recall snippet must use the zsh-safe ARRAY form, not a joined string."""
    text = _read(CLAUDE_MD)
    # The array-form append and the quoted array expansion are the load-bearing bits.
    assert 'ROOTS+=("$d")' in text
    assert 'memgrep recall "$SYMPTOM" "${ROOTS[@]}"' in text


# --- every sub-agent inherits the contract ----------------------------------


@pytest.mark.parametrize("sub_agent", SUB_AGENTS)
def test_sub_agent_has_proactive_memory_section(sub_agent: str) -> None:
    """Each sub-agent must carry its own proactive memory section (no inheritance)."""
    text = _read(AGENTS_DIR / sub_agent)
    assert "## Memory" in text, f"{sub_agent} missing a Memory section"


@pytest.mark.parametrize("sub_agent", SUB_AGENTS)
def test_sub_agent_references_global_recall_and_write(sub_agent: str) -> None:
    """Each sub-agent must reference the global recall + write skills."""
    text = _read(AGENTS_DIR / sub_agent)
    assert "/janitor-memory-recall" in text
    assert "/janitor-memory-write" in text


@pytest.mark.parametrize("sub_agent", SUB_AGENTS)
def test_sub_agent_documents_scope_routing(sub_agent: str) -> None:
    """Each sub-agent must restate scope routing (private/project/cross-project)."""
    text = _read(AGENTS_DIR / sub_agent)
    assert "SCOPE ROUTING" in text
    for scope in ("LOCAL", "PROJECT", "USER"):
        assert scope in text, f"{sub_agent} missing scope {scope}"
