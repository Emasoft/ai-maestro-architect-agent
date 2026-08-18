#!/usr/bin/env python3
"""The single source of truth for AMAA's GitHub self-identification line (PRRD G1).

Every issue, PR, comment, or review body an AI Maestro agent posts MUST begin
with a one-line self-identification, because every agent in the fleet shares the
one human-owner `gh` CLI identity. Without it, a post is indistinguishable from
one a human — or a different agent — wrote.

Two rules are enforced here rather than restated at each call site, because both
have already failed in production when left to per-site discipline:

1.  **No bare `@name`.** On GitHub an `@name` outside a code span at a word
    boundary PAGES a real account. A self-id line names the owner in plain
    words; the `@` adds nothing but a notification to a stranger. Backticks are
    NOT a fix for a template — a template is copied *out* of its code span and
    pasted as finished prose, which is exactly how the PRRD byline paged a real
    org for months. So the literal form carries no `@` at all.

2.  **One definition, imported.** The line was previously inlined in one script
    and simply absent from the two others that post comments, so a reader could
    not tell an agent's comment from a human's. A shared constant makes the
    omission impossible to reintroduce by copy-paste.
"""

from __future__ import annotations

# PLAIN WORDS, NO `@`. See rule 1 above before "improving" this into a mention.
SELF_ID_LINE = (
    "_Posted by the Claude developing the **ai-maestro-architect-agent** "
    "(the ARCHITECT role; via the shared owner gh auth)._"
)

# Commit trailer counterpart (PRRD G1): identifies the authoring plugin on
# commits, where the shared git identity has the same ambiguity as the gh one.
AGENT_TRAILER = "Agent: ai-maestro-architect-agent"


def with_self_id(body: str) -> str:
    """Prepend the G1 self-id line to a GitHub body, exactly once.

    Idempotent on purpose: call sites compose bodies from several helpers, and a
    doubled byline is a visible defect on a public post that no test would fail
    on. Returns the body unchanged if it already opens with the line.
    """
    stripped = body.lstrip()
    if stripped.startswith(SELF_ID_LINE):
        return body
    return f"{SELF_ID_LINE}\n\n{body}"
