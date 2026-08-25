"""Guards on delegation/comms claims that an upstream DEFAULT can silently invalidate.

AMAA documents how it spawns sub-agents and how it addresses other sessions. Both
descriptions are only true relative to a Claude Code default, and defaults move:

    2.1.218  fork SKILLS became background-by-default
    2.1.232  non-teammate AGENT-TOOL spawns became background-by-default
             `subagent_type: "fork"` became on-by-default and inherits the
             full parent conversation
    2.1.232  a bare session name now delivers without a ref confirmation

The fork-skill surface already survives this class of change, because every fork
skill states `background:` explicitly instead of inheriting it — see
`test_amaa_skills.py::test_fork_skill_declares_background`. When 2.1.232 flipped the
agent-spawn default, those skills did not move. This module extends the same idea to
the prose protocol: the rules that make a flipped default harmless must not be
deletable without a test noticing.

WHAT THIS GUARD CANNOT DO — stated so nobody trusts it further than it goes:
it catches DELETION of an operative sentence, not WEAKENING in place. Rewriting
"do not spawn" into "prefer not to spawn" keeps the collocation and stays green.
Changing a rule's force still requires a human reading it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

# Each entry: (file, collocation, what the rule protects).
#
# The needle is a SHORT COLLOCATION lifted from the rule's OPERATIVE sentence,
# never its distinctive TERM. A well-explained rule repeats its own vocabulary in
# the prose written AROUND it, so a term-presence check survives deleting the rule
# itself — the rationale's copies keep it green. Distance predicates ("term within
# N chars of evidence") do not repair that: any threshold that catches a gutted
# short file also reddens a correct long one, because it cannot tell "the rule was
# deleted" from "the document is long".
#
# Cost accepted deliberately: this couples to the rule's WORDING, so REWORDING the
# operative sentence reds the test. That is correct — changing what a rule says
# should require acknowledging its guard. Adding rationale around it must NOT red,
# which is exactly the asymmetry a collocation buys and a term check does not.
CLAIMS: list[tuple[str, str, str]] = [
    (
        "agents/ai-maestro-architect-agent-main-agent.md",
        "you will not get it by default",
        (
            "spawn results must be requested explicitly (CC 2.1.232 made non-teammate "
            "Agent-tool spawns background-by-default, so 'subagents return results to "
            "you' is no longer what the platform does on its own)"
        ),
    ),
    (
        "agents/ai-maestro-architect-agent-main-agent.md",
        "do not spawn your bundled sub-agents with",
        (
            "the fork stance: a fork inherits the full parent conversation, which would "
            "copy unauthenticated inbound native-channel content into an agent that "
            "never evaluated it"
        ),
    ),
    (
        (
            "skills/amaa-design-communication-patterns/references/"
            "native-cross-session-channel.md"
        ),
        "rather than reusing a name you learned",
        (
            "a session name is not a stable identity since CC 2.1.232 renames "
            "collisions, so recipients are resolved at send time"
        ),
    ),
    (
        (
            "skills/amaa-design-communication-patterns/references/"
            "native-cross-session-channel.md"
        ),
        "is the only gate",
        (
            "self-enforcement is load-bearing: this channel has no 403, and 2.1.232 "
            "removed the ref-confirmation step that used to sit in front of a send"
        ),
    ),
]


def _prose(text: str) -> str:
    """Collapse whitespace AND blockquote markers to single spaces, lowercased.

    Markdown wraps at ~88 columns, so an operative sentence can split across a
    newline and a raw substring search then reports absence for a rule that is
    sitting right there. Blockquote `>` prefixes break a sentence the same way.

    MUST be applied to BOTH sides of the comparison. Normalizing only the haystack
    is a defect, not a shortcut: a needle written with the wrapping still present
    would ask for a two-space form the collapsed haystack no longer contains, and
    the failure would read as "the rule is gone" while pointing the reader at
    restoring something that was never missing.

    (Same convention as `test_github_self_id.py::_prose`; duplicated rather than
    imported because this repo's test modules are self-contained.)
    """
    return re.sub(r"[\s>]+", " ", text.lower()).strip()


@pytest.mark.parametrize(
    ("rel_path", "collocation", "protects"),
    CLAIMS,
    ids=[f"{Path(c[0]).stem}::{c[1][:34]}" for c in CLAIMS],
)
def test_operative_sentence_still_present(rel_path: str, collocation: str, protects: str) -> None:
    """The rule's operative sentence is still in the file that carries it."""
    path = REPO / rel_path
    assert path.is_file(), f"{rel_path}: file is missing entirely"
    haystack = _prose(path.read_text(encoding="utf-8"))
    needle = _prose(collocation)
    assert needle in haystack, (
        f"{rel_path}: the operative sentence for this rule is gone.\n"
        f"  missing collocation: {collocation!r}\n"
        f"  the rule protects:   {protects}\n"
        "If the rule was deliberately removed or reworded, update CLAIMS in this "
        "file in the same commit — that edit is the acknowledgement this guard "
        "exists to force."
    )


def test_normalizer_is_applied_to_both_sides() -> None:
    """A needle spanning a line break must still be found (the defect above)."""
    wrapped = "pass the flag\nat the spawn site"
    assert _prose("at the spawn site") in _prose(wrapped)


def test_guard_would_notice_a_deletion() -> None:
    """Falsification: the predicate must FAIL on text with the rule removed.

    A guard never shown to fail is not known to be a guard — it may be asserting
    something trivially true of any input.
    """
    for _rel, collocation, _protects in CLAIMS:
        assert _prose(collocation) not in _prose("a document with the rule deleted")


# Claude Code 2.1.233 removed the todo tools on Opus 4.8, Sonnet 5, Fable 5, Mythos 5
# and newer. Guidance we EMIT that calls one names a tool the executing agent does not
# have — and unlike a wrong default, nothing errors: the agent just silently skips the
# tracking step. The removal is upstream, so a well-meaning re-add here looks correct.
TODO_TOOLS = ("TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "TodoWrite", "TodoRead")
EMITTERS = ("skills/amaa-planning-patterns/scripts/executor.py",)


@pytest.mark.parametrize("rel_path", EMITTERS)
def test_emitted_guidance_names_no_removed_todo_tool(rel_path: str) -> None:
    """Guidance we hand an agent must not instruct a tool removed at 2.1.233."""
    text = (REPO / rel_path).read_text(encoding="utf-8")
    found = _todo_tools_in_emitted_body(text)
    assert not found, (
        f"{rel_path} emits guidance naming {found}, removed from current models at "
        "2.1.233. Track in the plan file instead, or gate it on "
        "CLAUDE_CODE_ENABLE_TODO_TOOLS=1."
    )


def _todo_tools_in_emitted_body(text: str) -> list[str]:
    body = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))
    return sorted({t for t in TODO_TOOLS if t in body})


def test_todo_guard_would_notice_a_reintroduction() -> None:
    """Falsification: the SAME predicate must fire on a re-added instruction.

    Asserting only that the needle list is non-empty would pass without the
    comment-stripping ever running — the part most likely to be wrong.
    """
    assert _todo_tools_in_emitted_body('"  1. Use TaskCreate to track phases",') == [
        "TaskCreate"
    ]
    # ...and must NOT fire on the explanatory comment that legitimately names them.
    assert _todo_tools_in_emitted_body("# TaskCreate was removed at 2.1.233") == []
