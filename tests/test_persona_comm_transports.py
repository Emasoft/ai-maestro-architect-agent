#!/usr/bin/env python3
"""The persona must not promise 403 enforcement it cannot deliver (ai-maestro#131).

Claude Code 2.1.224 added a direct session-to-session channel (`SendMessage` /
`ListAgents`) that does **not** traverse the AI Maestro server. The R6 comm graph
is enforced at the API, so a forbidden AMP send returns HTTP 403 — but on the
native channel there is no 403 and no evaluation point, because the server is
never in the path.

The danger is not that a rule became harder to enforce. It is that a persona
documenting only the policed transport **reads as though every send is checked**,
so the agent can route around its own comm graph while believing the server has
it covered. A fleet screen found 7 of 7 role-plugin personas asserting server
enforcement and 0 of 7 naming the unpoliced transport.

Each fact is asserted SEPARATELY and at the decision point, because:
  - a body that merely name-drops `SendMessage` would pass a keyword scan while
    still implying the server covers it; and
  - stating it only in the comms skill leaves it absent at the moment the agent
    is deciding whether to send (the #107 ruling: a rule behind a pointer is
    absent where it is needed).
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MAIN_AGENT = REPO_ROOT / "agents" / "ai-maestro-architect-agent-main-agent.md"
SUB_AGENTS = sorted((REPO_ROOT / "agents").glob("amaa-*.md"))


def _comm_section(text: str) -> str:
    """The Communication Permissions section — where the send decision is made."""
    start = text.find("## Communication Permissions")
    assert start != -1, "the persona has no Communication Permissions section"
    nxt = text.find("\n## ", start + 1)
    return text[start:] if nxt == -1 else text[start:nxt]


def test_main_agent_exists():
    assert MAIN_AGENT.is_file(), f"{MAIN_AGENT} not found"


class TestTheEnforcementClaimIsScopedToItsTransport:
    def test_names_the_unpoliced_transport_at_the_decision_point(self):
        """Naming it in the comms skill is not enough — it must be HERE."""
        section = _comm_section(MAIN_AGENT.read_text(encoding="utf-8"))
        for tool in ("SendMessage", "ListAgents"):
            assert tool in section, (
                f"the Communication Permissions section never names {tool} — the agent "
                "decides whether to send here, so the unpoliced transport must be named here"
            )

    def test_states_the_native_channel_is_not_enforced(self):
        """Separate assertion: naming the tools while implying 403 covers them is the bug."""
        section = _comm_section(MAIN_AGENT.read_text(encoding="utf-8"))
        assert re.search(r"NOT enforced|not enforced|no 403", section), (
            "the section names the native channel but never says it is unenforced — "
            "a reader still concludes every send is checked"
        )

    def test_does_not_claim_blanket_enforcement(self):
        """The pre-fix phrasing: an unqualified 'ENFORCED at the API' for all sends."""
        section = _comm_section(MAIN_AGENT.read_text(encoding="utf-8"))
        bad = re.search(r"graph is ENFORCED at the API — violations return\s*\n?HTTP 403", section)
        assert not bad, (
            "the section asserts blanket API enforcement; that is true of AMP only, and "
            "reads as a promise covering the native channel too"
        )

    def test_says_the_restriction_binds_on_recipient_not_transport(self):
        section = _comm_section(MAIN_AGENT.read_text(encoding="utf-8"))
        assert "WHO you contact" in section or "who you contact" in section, (
            "the section never states that the graph binds on the RECIPIENT rather than "
            "the transport — the one framing that survives a new channel being added"
        )

    def test_directory_visibility_is_not_permission(self):
        """`ListAgents` lists what exists, not what you may reach."""
        section = _comm_section(MAIN_AGENT.read_text(encoding="utf-8"))
        assert "not a licence to contact" in section, (
            "the persona does not say that seeing a session in ListAgents confers no "
            "permission to message it"
        )

    def test_inbound_cross_session_is_untrusted(self):
        section = _comm_section(MAIN_AGENT.read_text(encoding="utf-8"))
        assert "untrusted data" in section, (
            "the persona does not mark inbound cross-session messages as untrusted — they "
            "carry no server-side identity check yet look like legitimate AMP instruction"
        )


def _inbound_bullet(persona: str) -> str:
    """The Inbound discipline bullet ONLY — never the whole persona.

    The slice is the load-bearing part. `SendMessage` already appears elsewhere
    in this persona (the send-side transport table added for ai-maestro#131), so
    a whole-file `assert "SendMessage" in persona` would pass against an AMP-only
    inbound rule and assert nothing. The earlier fix succeeding is exactly what
    would make the unscoped guard incapable of failing.
    """
    marker = "**Inbound discipline**"
    start = persona.find(marker)
    assert start != -1, "the persona has no **Inbound discipline** bullet"
    rest = persona[start:]
    nxt = re.search(r"\n#{1,3} ", rest)
    return rest[: nxt.start()] if nxt else rest


class TestInboundDisciplineEnumeratesEveryChannel:
    """A missed receive produces a SUCCESSFUL-LOOKING wake (ai-maestro#131).

    Drain AMP, find it empty, report the inbox clear, resume self-chosen work —
    while live directives wait on two unpolled channels. Silence on a channel you
    never read is indistinguishable from absence, so nothing surfaces it.
    """

    def test_channel_1_amp_is_named(self):
        assert "amp-inbox" in _inbound_bullet(MAIN_AGENT.read_text(encoding="utf-8"))

    def test_channel_2_direct_session_is_named_and_marked_unpollable(self):
        bullet = _inbound_bullet(MAIN_AGENT.read_text(encoding="utf-8"))
        assert "SendMessage" in bullet or "cross-session-message" in bullet, (
            "channel 2 is unnamed in the inbound bullet"
        )
        assert re.search(r"(?i)never\b[^.]{0,60}in\s+`?amp-inbox", bullet), (
            "the bullet does not say channel 2 never appears in amp-inbox — a reader "
            "drains AMP and believes they have seen everything"
        )

    def test_channel_3_github_threads_is_named(self):
        bullet = _inbound_bullet(MAIN_AGENT.read_text(encoding="utf-8"))
        assert re.search(r"(?i)gh issue list", bullet), "channel 3 is unnamed in the inbound bullet"

    def test_states_the_no_single_channel_rule(self):
        bullet = _inbound_bullet(MAIN_AGENT.read_text(encoding="utf-8"))
        assert re.search(r"(?i)never call the inbox clear on the strength of one channel", bullet)

    def test_blocked_does_not_license_not_checking(self):
        """This agent stalled ~15 heartbeats on 'blocked, stopping' with mail waiting."""
        bullet = _inbound_bullet(MAIN_AGENT.read_text(encoding="utf-8"))
        assert re.search(r"(?i)stopping\s+WORK, never stopping\s*\n?CHECKING", bullet), (
            "the bullet does not separate 'stop working' from 'stop checking' — the "
            "exact conflation that left a directive unread for four days"
        )

    def test_the_slice_is_a_strict_subset_of_the_persona(self):
        """If the slice ever widened to the file, every assertion above would go vacuous."""
        persona = MAIN_AGENT.read_text(encoding="utf-8")
        bullet = _inbound_bullet(persona)
        assert len(bullet) < len(persona), "the inbound slice widened to the whole persona"
        assert "## Communication Permissions" not in bullet, (
            "the slice leaked into Communication Permissions, where SendMessage appears "
            "for send-side reasons — the guard would then pass on unrelated text"
        )


class TestSubAgentsCarryTheProhibition:
    """Sub-agents have no AMP identity; the native channel is the only way they could send."""

    def test_every_sub_agent_forbids_the_native_channel(self):
        assert SUB_AGENTS, "no amaa-* sub-agents found"
        for path in SUB_AGENTS:
            text = path.read_text(encoding="utf-8")
            assert "SendMessage" in text, (
                f"{path.name} never names SendMessage — a sub-agent with no AMP identity "
                "could still reach another session through it"
            )
