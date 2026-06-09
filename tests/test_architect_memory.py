#!/usr/bin/env python3
"""Real tests for the architect-memory-recall / architect-memory-write skills.

Every test invokes the actual scripts as subprocesses against real fixture
directories — no mocks. The memgrep-absent fallback path is forced by
stripping PATH down to the Python interpreter's directory, which is the
load-bearing path per issue #13 ("recall degrades, never breaks").
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
RECALL = PLUGIN_ROOT / "skills" / "architect-memory-recall" / "scripts" / "recall.py"
WRITE = PLUGIN_ROOT / "skills" / "architect-memory-write" / "scripts" / "write_note.py"

NO_MEMGREP_ENV = {
    **{k: v for k, v in os.environ.items() if k not in ("PATH",)},
    # PATH without memgrep: just the interpreter dir so python itself resolves.
    "PATH": str(Path(sys.executable).parent),
}


def run_recall(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RECALL), *args],
        capture_output=True,
        text=True,
        env=NO_MEMGREP_ENV,
        timeout=30,
    )


def run_write(*args: str, stdin: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(WRITE), *args],
        capture_output=True,
        text=True,
        input=stdin,
        env=NO_MEMGREP_ENV,
        timeout=30,
    )


@pytest.fixture()
def memdir(tmp_path: Path) -> Path:
    """Fixture memory dir with three notes whose surfaces differ."""
    mem = tmp_path / "memory"
    mem.mkdir()
    (mem / "publish-lockfile-lag.md").write_text(
        "---\n"
        "name: publish-lockfile-lag\n"
        'description: "publish keeps leaving uv.lock dirty after every release"\n'
        "metadata:\n"
        "  node_type: memory\n"
        "  type: project\n"
        "---\n\n"
        "The staging tuple in publish.py omitted uv.lock; fixed in issue #10.\n",
        encoding="utf-8",
    )
    (mem / "graphql-rejected.md").write_text(
        "---\n"
        "name: graphql-rejected\n"
        'description: "why was GraphQL rejected for the inventory API design"\n'
        "metadata:\n"
        "  node_type: memory\n"
        "  type: project\n"
        "---\n\n"
        "REST chosen: the team lacked federation expertise and caching was simpler.\n",
        encoding="utf-8",
    )
    (mem / "user-prefers-tables.md").write_text(
        "---\n"
        "name: user-prefers-tables\n"
        'description: "how should test results be presented to the user"\n'
        "metadata:\n"
        "  node_type: memory\n"
        "  type: feedback\n"
        "---\n\n"
        "Unicode-bordered tables with per-test docstrings. **Why:** scannable.\n"
        "**How to apply:** render the table after every test run.\n",
        encoding="utf-8",
    )
    (mem / "MEMORY.md").write_text(
        "- [Publish Lockfile Lag](publish-lockfile-lag.md) — uv.lock dirty\n",
        encoding="utf-8",
    )
    return mem


def test_recall_ranks_surface_match_first(memdir: Path) -> None:
    """Recall puts the note whose description matches the symptom first."""
    result = run_recall("--memdir", str(memdir), "uv.lock dirty after release")
    assert result.returncode == 0, result.stderr
    lines = [line for line in result.stdout.strip().splitlines() if line]
    assert lines, "expected at least one ranked note"
    assert "publish-lockfile-lag.md" in lines[0]


def test_recall_finds_symptom_not_answer(memdir: Path) -> None:
    """The GraphQL note is found by the QUESTION wording, proving symptom indexing."""
    result = run_recall("--memdir", str(memdir), "why was GraphQL rejected")
    assert result.returncode == 0, result.stderr
    assert "graphql-rejected.md" in result.stdout.splitlines()[0]


def test_recall_no_match_exits_zero(memdir: Path) -> None:
    """A symptom with no matching note exits 0 and says so (absence != error)."""
    result = run_recall("--memdir", str(memdir), "zzqx quantum flux capacitor")
    assert result.returncode == 0
    assert "no matching memories" in result.stdout


def test_recall_missing_memdir_exits_zero(tmp_path: Path) -> None:
    """A project without a memory dir is a normal state, not a failure."""
    result = run_recall("--memdir", str(tmp_path / "nope"), "anything")
    assert result.returncode == 0
    assert "memory dir not found" in result.stdout


def test_recall_skips_the_index_file(memdir: Path) -> None:
    """MEMORY.md itself must never be returned as a memory."""
    result = run_recall("--memdir", str(memdir), "uv.lock dirty")
    assert "MEMORY.md" not in result.stdout


def test_recall_works_without_memgrep_on_path(memdir: Path) -> None:
    """The fallback path engages when memgrep is absent (PATH is stripped)."""
    import shutil as _shutil

    which = _shutil.which("memgrep", path=NO_MEMGREP_ENV["PATH"])
    assert which is None, "test env must not expose memgrep"
    result = run_recall("--memdir", str(memdir), "test results presented")
    assert result.returncode == 0
    assert "user-prefers-tables.md" in result.stdout


def test_write_creates_schema_valid_note(tmp_path: Path) -> None:
    """The writer produces frontmatter with name/description/node_type/type."""
    mem = tmp_path / "memory"
    result = run_write(
        "--memdir", str(mem),
        "--name", "handoff-needs-criteria",
        "--description", "orchestrator rejected the handoff - what was missing",
        "--type", "project",
        "--body", "Handoffs need acceptance criteria. **Why:** AMOA validates them. **How to apply:** fill the criteria section.",
    )
    assert result.returncode == 0, result.stderr
    note = mem / "handoff-needs-criteria.md"
    text = note.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "name: handoff-needs-criteria" in text
    assert 'description: "orchestrator rejected the handoff' in text
    assert "node_type: memory" in text
    assert "type: project" in text
    assert "**Why:**" in text


def test_write_appends_index_line(tmp_path: Path) -> None:
    """MEMORY.md gains exactly one '- [Title](file.md) — hook' line per note."""
    mem = tmp_path / "memory"
    run_write(
        "--memdir", str(mem),
        "--name", "first-note",
        "--description", "first symptom",
        "--type", "reference",
        "--body", "fact one",
    )
    result = run_write(
        "--memdir", str(mem),
        "--name", "second-note",
        "--description", "second symptom",
        "--type", "reference",
        "--title", "Custom Title",
        "--body", "fact two",
    )
    assert result.returncode == 0, result.stderr
    index = (mem / "MEMORY.md").read_text(encoding="utf-8")
    assert "- [First Note](first-note.md) — first symptom" in index
    assert "- [Custom Title](second-note.md) — second symptom" in index
    assert index.count("\n") == 2


def test_write_refuses_overwrite(tmp_path: Path) -> None:
    """A second write with the same name exits 1 and leaves the original intact."""
    mem = tmp_path / "memory"
    run_write("--memdir", str(mem), "--name", "dup", "--description", "d", "--type", "user", "--body", "original")
    result = run_write("--memdir", str(mem), "--name", "dup", "--description", "d", "--type", "user", "--body", "clobber")
    assert result.returncode == 1
    assert "note exists" in result.stderr
    assert "original" in (mem / "dup.md").read_text(encoding="utf-8")


def test_write_rejects_bad_name(tmp_path: Path) -> None:
    """Non-kebab names fail fast with exit 2 and write nothing."""
    mem = tmp_path / "memory"
    result = run_write("--memdir", str(mem), "--name", "Bad Name!", "--description", "d", "--type", "user", "--body", "x")
    assert result.returncode == 2
    assert "invalid name" in result.stderr
    assert not (mem / "Bad Name!.md").exists()


def test_write_rejects_empty_body(tmp_path: Path) -> None:
    """An empty body (no fact) fails fast with exit 2."""
    mem = tmp_path / "memory"
    result = run_write("--memdir", str(mem), "--name", "empty-body", "--description", "d", "--type", "user", "--body", "   ")
    assert result.returncode == 2
    assert "empty body" in result.stderr


def test_roundtrip_write_then_recall(tmp_path: Path) -> None:
    """Write-then-recall: a freshly written note is findable by its symptom."""
    mem = tmp_path / "memory"
    write = run_write(
        "--memdir", str(mem),
        "--name", "ci-macos-flake",
        "--description", "macos CI job randomly times out on the matrix build",
        "--type", "project",
        "--body", "Root cause: shared runner contention. Pin to macos-14.",
    )
    assert write.returncode == 0, write.stderr
    recall = run_recall("--memdir", str(mem), "macos CI randomly times out")
    assert recall.returncode == 0
    assert "ci-macos-flake.md" in recall.stdout.splitlines()[0]
