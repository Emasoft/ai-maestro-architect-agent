#!/usr/bin/env python3
"""The board must not lie about what is open (derived from TRDD-M3RV5THO).

`TRDD-M3RV5THO` sat at `column: complete` inside `design/tasks/` for five days
after its work shipped. Nothing caught it: the hourly sweep polls GitHub issues,
the test suite had no opinion about the board, and the summary carried the card
forward as handled. It surfaced only because a compaction handoff printed the
board's column census and the two didn't match the story.

That is the failure this guards. A card in `design/tasks/` ASSERTS "open work".
A terminal card sitting there is not merely untidy — it is strictly worse than
an unfiled task, because the one view anyone consults reports it as live, so the
stall is invisible exactly where someone would look for it.

The predicate is not "terminal column ⇒ wrong folder", which would be wrong:

    complete   + release-via: publish  -> LEGITIMATE, mid-pipeline
                                          (complete -> publish -> published)
    complete   + release-via: none     -> TERMINAL, belongs in archived/
    completed / cancelled / superseded -> TERMINAL, always
    refused                            -> belongs in refused/, never tasks/

`complete` is a lifecycle column AND a release terminal depending on a field
one line away, and conflating the two is how the stale card looked normal. The
distinction is the whole check; a coarser rule would either miss this card or
red on every card legitimately awaiting publish.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TASKS = REPO_ROOT / "design" / "tasks"
ARCHIVED = REPO_ROOT / "design" / "archived"

# Terminal regardless of anything else — these leave the open zone on the same
# edit that sets them.
ALWAYS_TERMINAL = {"completed", "cancelled", "superseded"}

# Belongs in design/refused/ (a proposal never approved), never in tasks/.
REFUSED = "refused"

# Terminal only when the card's release branch ends there. `release-via` absent
# defaults to `none`, so an unstated release branch makes these terminal — which
# is precisely the case that shipped.
RELEASE_TERMINALS = {"none": "complete", "publish": "published", "deploy": "live"}


def _field(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:[ \t]*(\S+)[ \t]*$", text, re.MULTILINE)
    return match.group(1) if match else None


def card_is_terminal(column: str, release_via: str | None) -> bool:
    """Is this card DONE — i.e. does it no longer belong in the open zone?

    Pure, so the controls below can drive it with values that do not exist on
    disk. A guard only fed real repo state cannot be shown to fail.
    """
    if column in ALWAYS_TERMINAL or column == REFUSED:
        return True
    branch = release_via or "none"
    return RELEASE_TERMINALS.get(branch) == column


def _cards(folder: Path):
    return sorted(folder.glob("TRDD-*.md")) if folder.is_dir() else []


def test_tasks_folder_exists():
    assert TASKS.is_dir(), "design/tasks/ is missing — the open zone must exist"


def test_no_terminal_card_sits_in_the_open_zone():
    """The literal defect: a done card asserting it is open work."""
    offenders = []
    for card in _cards(TASKS):
        text = card.read_text(encoding="utf-8")
        column = _field(text, "column")
        assert column, (
            f"{card.name} has no `column:` — it cannot be placed on the board"
        )
        if card_is_terminal(column, _field(text, "release-via")):
            offenders.append(
                f"{card.name} (column: {column}, release-via: {_field(text, 'release-via') or 'none'})"
            )

    assert not offenders, (
        "terminal cards are sitting in design/tasks/, where they assert OPEN work:\n  "
        + "\n  ".join(offenders)
        + "\nClose the card (set the terminal column, append to `## Approval log`) and "
        "`git mv` it to design/archived/ — and check its deferrals still have owners first."
    )


def test_archived_cards_are_actually_terminal():
    """The mirror. An open card filed under archived/ is invisible the other way."""
    strays = []
    for card in _cards(ARCHIVED):
        text = card.read_text(encoding="utf-8")
        column = _field(text, "column")
        if column and not card_is_terminal(column, _field(text, "release-via")):
            strays.append(f"{card.name} (column: {column})")
    assert not strays, (
        "non-terminal cards are buried in design/archived/, where nobody will work them:\n  "
        + "\n  ".join(strays)
    )


class TestThePredicateSeparatesTheTwoMeaningsOfComplete:
    """`complete` is the whole difficulty; four controls pin both readings.

    Written because a guard that merely reports green on today's repo proves
    nothing — the question is whether it would have reddened on the card that
    shipped, and whether it stays quiet on the cards that are legitimately open.
    """

    def test_reds_on_the_card_that_actually_shipped(self):
        """M3RV5THO's real values: `complete`, no `release-via`."""
        assert card_is_terminal("complete", None) is True

    def test_greens_on_a_card_legitimately_awaiting_publish(self):
        """Same column, different release branch — must NOT red.

        This is the control that stops the obvious over-broad fix ("`complete`
        is terminal"), which would red on every card queued for release.
        """
        assert card_is_terminal("complete", "publish") is False
        assert card_is_terminal("publish", "publish") is False

    def test_published_is_terminal_only_on_the_publish_branch(self):
        assert card_is_terminal("published", "publish") is True
        assert card_is_terminal("live", "deploy") is True
        assert card_is_terminal("live", "publish") is False

    def test_always_terminal_states_ignore_the_release_branch(self):
        for column in ("completed", "cancelled", "superseded", "refused"):
            assert card_is_terminal(column, "publish") is True, column
            assert card_is_terminal(column, None) is True, column

    def test_ordinary_open_columns_stay_open(self):
        for column in (
            "backburner",
            "todo",
            "design",
            "dispatch",
            "dev",
            "testing",
            "ai_review",
            "human_review",
            "blocked",
            "failed",
        ):
            assert card_is_terminal(column, None) is False, column
            assert card_is_terminal(column, "publish") is False, column
