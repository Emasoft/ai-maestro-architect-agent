#!/usr/bin/env python3
"""Tests for amaa_stop_check.py (issue #14, M12).

amaa_stop_check.py is the Stop hook that blocks a session from exiting while
design work is incomplete. These tests drive the REAL script as a subprocess
with real stdin JSON and a real, controlled tmp_path project tree so the
check_* gates fire deterministically — nothing about the script's own logic is
mocked.

Determinism note: the script shells out to `gh` (check_github_issues) and
`amp-send` (_notify_amcos_blocked_exit). Both host binaries exist on this
machine, so each subprocess runs with an EMPTY PATH (`PATH=""`). The Python
interpreter is launched by its absolute path (sys.executable), so it still
starts, but the script's internal `["gh", ...]` / `["amp-send", ...]` lookups
raise FileNotFoundError — exactly the "tool not on PATH" branch the script
already handles by returning no blockers. We exercise that real branch instead
of inventing a fake `gh`/`amp-send`.

Each subprocess is given an explicit cwd=<project tree>; the project tree
carries a `.git` dir so find_project_root() resolves to it (and never walks up
into a real parent repo).
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "scripts" / "amaa_stop_check.py"


def run_stop_check(
    project_root: Path,
    stdin_json: str = "{}",
    session_id: str = "test-session",
    block_cap: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run the real stop-check script as a subprocess rooted at project_root.

    Uses an empty PATH so the script's `gh`/`amp-send` calls hit their real
    FileNotFoundError branch (no host binaries leak in to add nondeterministic
    blockers). The interpreter is sys.executable (absolute), so Python still
    launches despite the empty PATH.
    """
    env = {
        "HOME": str(project_root),
        "PATH": "",
        "CLAUDE_CODE_SESSION_ID": session_id,
    }
    if block_cap is not None:
        env["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"] = block_cap
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=stdin_json,
        capture_output=True,
        text=True,
        cwd=str(project_root),
        env=env,
        timeout=30,
        check=False,
    )


def make_project(tmp_path: Path) -> Path:
    """Create a minimal project tree (with .git) that find_project_root finds."""
    (tmp_path / ".git").mkdir()
    return tmp_path


def test_clean_project_allows_exit(tmp_path):
    """An empty project (no draft docs / tasks / orphan reqs) exits 0 with no output."""
    project = make_project(tmp_path)
    result = run_stop_check(project, stdin_json='{"session_id": "x"}')
    assert result.returncode == 0, f"expected allow-exit (0), got {result.returncode}"
    assert result.stdout.strip() == "", f"clean exit must print nothing: {result.stdout!r}"


def test_draft_design_doc_blocks_exit(tmp_path):
    """A design doc flagged `status: draft` is a blocker that blocks exit (code 2)."""
    project = make_project(tmp_path)
    design = project / "design"
    design.mkdir()
    (design / "spec.md").write_text("---\nstatus: draft\n---\n# Spec\n", encoding="utf-8")

    result = run_stop_check(project)
    assert result.returncode == 2, f"draft doc must block exit; got {result.returncode}"
    decision = json.loads(result.stdout)
    assert decision["decision"] == "block"
    blockers = decision["hookSpecificOutput"]["blockers"]
    assert any("design/spec.md" in b and "Draft" in b for b in blockers), blockers


def test_pending_task_json_blocks_exit(tmp_path):
    """A .claude/tasks/*.json with status in-progress blocks exit and is named."""
    project = make_project(tmp_path)
    tasks = project / ".claude" / "tasks"
    tasks.mkdir(parents=True)
    (tasks / "t1.json").write_text(
        json.dumps({"name": "wire-up-auth", "status": "in-progress"}),
        encoding="utf-8",
    )

    result = run_stop_check(project)
    assert result.returncode == 2, f"pending task must block; got {result.returncode}"
    decision = json.loads(result.stdout)
    blockers = decision["hookSpecificOutput"]["blockers"]
    assert any("wire-up-auth" in b and "in-progress" in b for b in blockers), blockers


def test_completed_task_does_not_block(tmp_path):
    """A task whose status is `completed` is NOT a blocker — exit is allowed (0)."""
    project = make_project(tmp_path)
    tasks = project / ".claude" / "tasks"
    tasks.mkdir(parents=True)
    (tasks / "done.json").write_text(
        json.dumps({"name": "ship-it", "status": "completed"}),
        encoding="utf-8",
    )

    result = run_stop_check(project)
    assert result.returncode == 0, (
        f"a completed task must not block exit; stdout={result.stdout!r}"
    )
    assert result.stdout.strip() == ""


def test_orphan_requirement_blocks_exit(tmp_path):
    """A requirements.md with a REQ id and no matching design doc blocks exit."""
    project = make_project(tmp_path)
    (project / "requirements.md").write_text(
        "# Requirements\n\n- REQ-001: the system shall do a thing\n",
        encoding="utf-8",
    )

    result = run_stop_check(project)
    assert result.returncode == 2, f"orphan req must block; got {result.returncode}"
    decision = json.loads(result.stdout)
    blockers = decision["hookSpecificOutput"]["blockers"]
    assert any("REQ-001" in b and "without design" in b for b in blockers), blockers


def test_github_issue_check_is_silent_without_gh(tmp_path):
    """With no `gh` on PATH, the GitHub-issue gate adds zero blockers (graceful skip)."""
    # Project is otherwise clean, so the ONLY thing that could block is the
    # github-issues check. With PATH="" the gh lookup is FileNotFoundError, the
    # handled branch — so the run must allow exit (proving the gate added nothing).
    project = make_project(tmp_path)
    result = run_stop_check(project)
    assert result.returncode == 0, (
        "github-issue gate must not block when gh is unavailable; "
        f"stdout={result.stdout!r}"
    )
    assert result.stdout.strip() == ""


def test_block_cap_yields_gracefully_once_reached(tmp_path):
    """Once the per-session block count reaches the cap, the hook stops blocking (exit 0)."""
    project = make_project(tmp_path)
    design = project / "design"
    design.mkdir()
    (design / "spec.md").write_text("status: draft\n", encoding="utf-8")

    # Pre-seed the per-session counter at the cap so this run is the (cap+1)th.
    state = project / ".claude" / "state"
    state.mkdir(parents=True)
    session_id = "capped-session"
    counter = state / f"amaa-stop-block-count-{session_id}.txt"
    counter.write_text("3")

    result = run_stop_check(project, session_id=session_id, block_cap="3")
    # Even though a real blocker (draft doc) exists, the cap forces a graceful
    # allow-exit so the platform's 8-block auto-kill never fires.
    assert result.returncode == 0, (
        f"at/over the cap the hook must yield (exit 0); got {result.returncode}, "
        f"stdout={result.stdout!r}"
    )
    # And the counter is reset (unlinked) so the next session starts fresh.
    assert not counter.exists(), "counter must be cleared once the cap is reached"


def test_block_increments_counter_below_cap(tmp_path):
    """Below the cap, a blocking run blocks (exit 2) and bumps the per-session counter."""
    project = make_project(tmp_path)
    design = project / "design"
    design.mkdir()
    (design / "spec.md").write_text("status: draft\n", encoding="utf-8")

    session_id = "counting-session"
    counter = (
        project / ".claude" / "state" / f"amaa-stop-block-count-{session_id}.txt"
    )
    assert not counter.exists(), "precondition: no counter yet"

    result = run_stop_check(project, session_id=session_id, block_cap="3")
    assert result.returncode == 2, f"first block below cap must block; {result.returncode}"
    # The script persists the bumped count (0 -> 1) for this session.
    assert counter.exists(), "counter file must be created on first block"
    assert counter.read_text().strip() == "1", (
        f"counter should be 1 after first block, got {counter.read_text()!r}"
    )
