#!/usr/bin/env python3
"""PRRD container-stamp guards (ai-maestro#145, the fifth clause).

`design/requirements/PRRD.md` carries two machine-readable claims about ITSELF:

    prrd-version: 1.2
    updated: 2026-08-12T14:31:57+0200

Both went stale and nothing noticed. Across `de834aa` (Aug 8) and `bcfac08`
(Aug 12) the document asserted `1.1` and a June `updated:` — while line 18 of
that same file states the requirement outright ("Edit first. Bump
`prrd-version:`. Update `updated:`."). `bcfac08` is the commit that fixed
silent mutation at RULE level while committing it at DOCUMENT level.

Why no existing check caught it: a rule citation (`PRRD G1.2`) is a REFERENCE,
so a checker can resolve it and find it dangling. A container version is cited
by nothing, so there is no reference to resolve and a citation gate stays green
straight through the lie.

The shape of the guard therefore matters more than its presence. CORE's tree
had the same defect for 52 days *despite* a tool (`prrd-edit.py`) that sets both
fields on every mutation and literally cannot produce the stale state — because
the offending commit hand-edited the file, bypassing the tool. A guard on the
writer would have stayed green through the entire incident.

    A machine-readable claim needs a check against something that is NOT the
    writer that maintains it.

Here that is git. And the argument is stronger for AMAA than for CORE: this
repo has NO `prrd-edit.py` at all, so hand-editing is not a bypass of the
maintaining writer — it is the only writer there is.

Two arms, because the stamp can lie in two different tenses:

  * COMMITTED — `updated:` must not trail the newest commit touching the file.
    Catches the defect for every future reader and every clone.
  * DIRTY — when PRRD.md has uncommitted changes, `updated:` must be recent.
    This is the arm that reds at AUTHORING time, which is when the defect was
    actually introduced (the file was dirty, the stamp said June, and it was
    committed anyway).
"""

import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
PRRD = REPO_ROOT / "design" / "requirements" / "PRRD.md"

# A day of slack: an edit and its commit can straddle midnight, and a rebase
# rewrites committer dates. Tight enough that 52 days is loud, loose enough
# that honest workflows never red.
MAX_LAG = timedelta(days=1)


def _field(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:[ \t]*(\S+)[ \t]*$", text, re.M)
    return match.group(1) if match else None


def _git(*args: str) -> str | None:
    """Run a git query in the repo; None when git cannot answer at all."""
    try:
        done = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, timeout=30
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def stamp_lag(
    updated: datetime,
    newest_commit: datetime | None,
    dirty: bool,
    now: datetime,
) -> timedelta:
    """How far the stamp trails its INDEPENDENT witness.

    The witness is never the thing that writes the stamp — that is the whole
    point. A dirty file is witnessed by the clock (the edit is happening now);
    a clean one by git (the last time the content actually changed).
    """
    witness = now if dirty else newest_commit
    assert witness is not None, (
        "a clean file with no commit has no witness — skip, do not judge"
    )
    return witness - updated


# --------------------------------------------------------------------------
# The live assertions, against this repo's real PRRD.
# --------------------------------------------------------------------------


def test_prrd_exists():
    assert PRRD.is_file(), "the project PRRD is missing"


def test_prrd_version_is_well_formed():
    """A malformed version is worse than a stale one: the next bump restarts.

    Staleness is a wrong-but-comparable value. A version that does not parse
    makes the next bump start over from scratch, silently discarding the
    document's entire revision history with no diff that looks wrong.
    """
    raw = _field(PRRD.read_text(encoding="utf-8"), "prrd-version")
    assert raw is not None, "PRRD.md has no `prrd-version:` field"
    assert re.fullmatch(r"\d+\.\d+", raw), (
        f"prrd-version must be `<major>.<minor>`, got {raw!r} — an unparseable "
        "version makes the next bump restart and lose the document's history"
    )


def test_updated_is_iso_with_an_offset():
    """A naive timestamp cannot be compared against a committer date."""
    raw = _field(PRRD.read_text(encoding="utf-8"), "updated")
    assert raw is not None, "PRRD.md has no `updated:` field"
    stamp = datetime.fromisoformat(raw)
    assert stamp.tzinfo is not None, (
        f"`updated: {raw}` carries no UTC offset — it is ambiguous across machines"
    )


def test_stamp_is_not_behind_its_git_witness():
    """The defect itself: `updated:` asserting June for an August edit."""
    if _git("rev-parse", "--is-inside-work-tree") != "true":
        pytest.skip("not a git work tree — no witness available")
    if _git("rev-parse", "--is-shallow-repository") == "true":
        pytest.skip("shallow clone — commit history is truncated, witness unreliable")

    rel = PRRD.relative_to(REPO_ROOT).as_posix()
    dirty = bool(_git("status", "--porcelain", "--", rel))
    newest_raw = _git("log", "-1", "--format=%cI", "--", rel)
    if not dirty and not newest_raw:
        pytest.skip("PRRD.md is untracked and unmodified — nothing to witness against")

    updated_raw = _field(PRRD.read_text(encoding="utf-8"), "updated")
    assert updated_raw is not None, "PRRD.md has no `updated:` field to check"
    updated = datetime.fromisoformat(updated_raw)
    newest = datetime.fromisoformat(newest_raw) if newest_raw else None
    lag = stamp_lag(updated, newest, dirty, datetime.now(timezone.utc))

    assert lag <= MAX_LAG, (
        f"`updated:` trails its witness by {lag} (limit {MAX_LAG}). "
        + (
            "PRRD.md has uncommitted edits, so the stamp must be current."
            if dirty
            else f"Newest commit touching it: {newest_raw}."
        )
        + " Edit first, bump `prrd-version:`, then update `updated:` (PRRD §0)."
    )


# --------------------------------------------------------------------------
# Controls. A guard nobody has seen red is a guess about the future.
# --------------------------------------------------------------------------


class TestThePredicateActuallyBites:
    """Both directions, both arms — four independent controls.

    Written because the guard being ADDED is not evidence the guard WORKS: the
    only thing that distinguishes a real check from decoration is having watched
    it fail on the exact input it exists to reject.
    """

    NOW = datetime(2026, 8, 12, 12, 0, 0, tzinfo=timezone.utc)

    def test_committed_arm_reds_on_the_real_historical_stale_stamp(self):
        """The literal values that shipped: June stamp, August commit."""
        lag = stamp_lag(
            updated=datetime.fromisoformat("2026-06-11T11:41:33+02:00"),
            newest_commit=datetime.fromisoformat("2026-08-12T10:15:00+02:00"),
            dirty=False,
            now=self.NOW,
        )
        assert lag > MAX_LAG, "the guard is blind to the defect it was written for"
        assert lag.days == 61

    def test_committed_arm_greens_when_the_stamp_matches_the_commit(self):
        lag = stamp_lag(
            updated=datetime.fromisoformat("2026-08-12T14:31:57+02:00"),
            newest_commit=datetime.fromisoformat("2026-08-12T14:33:00+02:00"),
            dirty=False,
            now=self.NOW,
        )
        assert lag <= MAX_LAG, (
            "an honest stamp must not red — a guard that cries wolf gets deleted"
        )

    def test_dirty_arm_reds_on_an_edit_carrying_a_stale_stamp(self):
        """The authoring-time case; git alone cannot see this one.

        With uncommitted edits the newest commit is OLD, so the committed arm
        passes trivially. Only the clock witnesses an edit in progress.
        """
        stale = datetime.fromisoformat("2026-06-11T11:41:33+02:00")
        old_commit = datetime.fromisoformat("2026-06-11T11:42:00+02:00")
        assert stamp_lag(stale, old_commit, dirty=False, now=self.NOW) <= MAX_LAG, (
            "precondition: the committed arm is blind here, which is why the dirty arm exists"
        )
        assert stamp_lag(stale, old_commit, dirty=True, now=self.NOW) > MAX_LAG

    def test_dirty_arm_greens_when_the_author_stamped_the_edit(self):
        fresh = self.NOW - timedelta(minutes=3)
        old_commit = datetime.fromisoformat("2026-06-11T11:42:00+02:00")
        assert stamp_lag(fresh, old_commit, dirty=True, now=self.NOW) <= MAX_LAG
