#!/usr/bin/env python3
"""PRRD G1 regression tests for AMAA's GitHub-posting scripts (architect#24 B2).

Two defects are pinned here, both of which shipped and neither of which any
existing test caught:

1.  **A missing byline.** Every AI Maestro agent posts under the one shared
    human-owner `gh` identity, so a comment without the self-id line is
    indistinguishable from a human's. Two of the three posting scripts omitted
    it entirely.

2.  **A byline that pages a stranger.** The one script that DID carry a byline
    embedded a bare `@owner`. On GitHub an `@name` outside a code span at a word
    boundary is a MENTION — so every issue that script opened notified a real
    account. This is the failure mode that is invisible in review (it looks like
    prose) and irreversible once posted (edit history is retained).

Both are asserted against the shared constant AND against each call site, since
a correct constant that no site imports fixes nothing.
"""

import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS = REPO_ROOT / "scripts"

# Every script that writes a body to GitHub. Adding a new poster without adding
# it here is the gap this list exists to close.
POSTING_SCRIPTS = [
    "amaa_github_issue_create.py",
    "amaa_github_sync_status.py",
    "amaa_github_attach_document.py",
]


def _load_self_id():
    spec = importlib.util.spec_from_file_location(
        "amaa_self_id", SCRIPTS / "amaa_self_id.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    return module


def test_self_id_module_exists():
    assert (SCRIPTS / "amaa_self_id.py").is_file(), (
        "the shared G1 constant module is missing"
    )


def test_byline_carries_no_at_mention():
    """A bare `@name` in the byline pages a real account on every post."""
    mod = _load_self_id()
    assert "@" not in mod.SELF_ID_LINE, (
        f"SELF_ID_LINE contains '@' and would render as a GitHub mention: {mod.SELF_ID_LINE!r}. "
        "Name the owner in plain words — the '@' adds only a notification to a stranger."
    )


def test_byline_identifies_the_plugin():
    mod = _load_self_id()
    assert "ai-maestro-architect-agent" in mod.SELF_ID_LINE
    assert mod.SELF_ID_LINE.startswith("_Posted by"), (
        "byline must be recognisable at a glance"
    )


def test_with_self_id_is_idempotent():
    """Call sites compose bodies from several helpers; a doubled byline is visible."""
    mod = _load_self_id()
    once = mod.with_self_id("## Design Status Update")
    assert once.startswith(mod.SELF_ID_LINE)
    assert mod.with_self_id(once) == once


def test_with_self_id_preserves_the_body():
    mod = _load_self_id()
    assert "## Design Status Update" in mod.with_self_id("## Design Status Update")


class TestEverySiteActuallyUsesIt:
    """A correct constant that no call site imports fixes nothing."""

    def test_every_posting_script_imports_the_shared_constant(self):
        for name in POSTING_SCRIPTS:
            src = (SCRIPTS / name).read_text(encoding="utf-8")
            assert "from amaa_self_id import" in src, (
                f"{name} posts to GitHub but does not import the shared G1 byline"
            )

    def test_no_script_redefines_the_byline_locally(self):
        """A local copy is how the `@owner` bug survived: one site, one definition."""
        for name in POSTING_SCRIPTS:
            src = (SCRIPTS / name).read_text(encoding="utf-8")
            assert not re.search(r"^SELF_ID_LINE\s*=", src, re.M), (
                f"{name} redefines SELF_ID_LINE locally — import it from amaa_self_id instead"
            )

    def test_no_posting_script_contains_a_bare_at_mention(self):
        """Catches an `@name` reintroduced anywhere in a posted body, not just the byline."""
        for name in POSTING_SCRIPTS:
            for i, line in enumerate(
                (SCRIPTS / name).read_text(encoding="utf-8").splitlines(), 1
            ):
                if "`" in line or line.lstrip().startswith("#"):
                    continue  # code spans are inert; comments are never posted
                hit = re.search(r"(?<![\w`/])@[A-Za-z][\w-]{2,}", line)
                assert not hit, (
                    f"{name}:{i} carries a bare mention {hit.group(0)!r}: {line.strip()!r}"
                )


# Prose that agents COPY into GitHub bodies. A byline template lives here, and the
# `@owner` that shipped in the script constant was copied FROM this layer — so
# guarding only the scripts leaves the source intact and every future agent
# re-derives the bug from the document.
PROSE_SCANNED = [
    "design/requirements/PRRD.md",
    "docs/GOVERNANCE-RULES.md",
    "docs/AGENT_OPERATIONS.md",
]

# The collocation lifted from G1's OPERATIVE sentence — long enough to be
# rule-unique, short enough that rewording the surrounding prose does not red.
BYLINE_CANON = "via the shared <owner> gh auth"


def sole_occurrence(text: str, phrase: str) -> bool:
    """Is `phrase` anchored to ONE place in `text`?

    The discriminator `in` cannot express (ai-maestro#131): a phrase occurring
    twice is anchored to the DOCUMENT, not to the rule, so deleting the rule
    leaves the other copy holding the guard up. Pure, so the controls below can
    drive it with the duplicate case that does not exist on disk.
    """
    return text.count(phrase) == 1


def _strip_code_spans(line: str) -> str:
    """Remove `...` spans — inert on GitHub, so a mention inside one pages nobody.

    Coarse line-level skipping (what the script scan uses) is wrong for prose: a
    markdown line routinely mixes a code span with real text, so skipping the whole
    line would hide a live mention sitting beside an inert one.
    """
    return re.sub(r"`[^`]*`", "", line)


class TestProseTemplatesCarryNoMention:
    """architect#24 follow-up: the same defect class, one file over.

    A byline in a governance document is a TEMPLATE — it is pasted verbatim as
    finished prose, so backticks protect it where it sits and not where it is used.
    Canon (governance-spec blob b1ffe5998966; GOVERNANCE-RULES R22.2, marked
    Explicit USER) is `<owner>`, carrying no `@` deliberately.
    """

    def test_no_bare_mention_in_prose_agents_copy_from(self):
        for rel in PROSE_SCANNED:
            path = REPO_ROOT / rel
            if not path.is_file():
                continue  # optional doc; absence is not a defect
            for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                line = _strip_code_spans(raw)
                hit = re.search(r"(?<![\w`/])@[A-Za-z][\w-]{2,}", line)
                assert not hit, (
                    f"{rel}:{i} carries a bare mention {hit.group(0)!r} outside a code span — "
                    f"it pages a real account when copied. Use <owner>. Line: {raw.strip()[:120]!r}"
                )

    def test_the_prrd_byline_matches_ratified_canon(self):
        """Pins the exact repaired form, so a stale copy cannot drift back in.

        Asserts a COUNT, not membership (ai-maestro#131). `in` cannot tell "the
        rule is present" from "something quoting the rule is present" — so the
        day a rationale paragraph quotes the byline while explaining it, an
        `in` guard survives the rule's deletion and holds itself up on the
        commentary. That is not hypothetical here: this PRRD documents its own
        conventions, which is exactly the document class where prose quotes the
        rule it explains.

        Today the phrase occurs once, so `in` would pass for the right reason —
        by accident of state, not by construction, and nothing would report the
        day that stopped being true.
        """
        prrd = (REPO_ROOT / "design" / "requirements" / "PRRD.md").read_text(
            encoding="utf-8"
        )
        occurrences = prrd.count(BYLINE_CANON)
        assert occurrences == 1, (
            f"expected the ratified byline exactly once in the PRRD, found {occurrences}. "
            + (
                "Zero means the rule is gone or reworded — restore it or update this guard."
                if occurrences == 0
                else "More than one means the guard is no longer anchored to the RULE: "
                "deleting the rule would leave the other copy passing this test. "
                "Lengthen the pinned phrase until it is rule-unique."
            )
        )
        assert "@owner" not in prrd, "the stale @owner byline is back in the PRRD"


class TestTheCountDiscriminatorBites:
    """Seeded both directions, because `in` and `count == 1` agree on today's file.

    A change that cannot be shown to alter any outcome is indistinguishable from
    no change at all — and this one is invisible against the current PRRD, which
    is exactly why it needs the duplicate case driven explicitly.
    """

    RULE = f"- **G1.2** — … begin the body with a one-line self-id ({BYLINE_CANON})."
    RATIONALE = (
        f"The byline is written `{BYLINE_CANON}` deliberately, carrying no at-sign."
    )

    def test_membership_survives_the_rule_deletion_but_the_count_does_not(self):
        """The whole point: on a document that quotes its own rule, `in` is vacuous."""
        both = f"{self.RULE}\n\n{self.RATIONALE}\n"
        rule_deleted = f"{self.RATIONALE}\n"  # only the commentary is left

        assert BYLINE_CANON in rule_deleted, (
            "precondition: `in` cannot see this deletion — if that ever changes, "
            "the count discriminator has become redundant"
        )
        assert sole_occurrence(both, BYLINE_CANON) is False, (
            "two copies means the guard is anchored to the document, not the rule"
        )
        assert sole_occurrence(rule_deleted, BYLINE_CANON) is True, (
            "one copy left after deleting the rule — the count is not a silver bullet "
            "either; it detects the DUPLICATE, which is the state that makes deletion invisible"
        )

    def test_sole_occurrence_reds_on_absence(self):
        assert sole_occurrence("no byline anywhere", BYLINE_CANON) is False

    def test_sole_occurrence_greens_on_exactly_one(self):
        assert sole_occurrence(self.RULE, BYLINE_CANON) is True
