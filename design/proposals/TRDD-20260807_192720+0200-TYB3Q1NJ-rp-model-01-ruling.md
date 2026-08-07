---
trdd-id: TYB3Q1NJ
title: Rule request — resolve RP-MODEL-01 against CPV CA-04 for the ARCHITECT role plugin
column: proposal
created: 2026-08-07T19:27:20+0200
updated: 2026-08-07T19:27:20+0200
current-owner: ai-maestro-architect-agent
task-type: infra
scope: project
approval-tier: 2
relevant-rules: []
npt: []
eht: []
implementation-commits: []
---

# Rule request — resolve RP-MODEL-01 against CPV CA-04 for the ARCHITECT role plugin

## The question

Should `agents/ai-maestro-architect-agent-main-agent.md` and
`ai-maestro-architect-agent.agent.toml` pin `model: opus`?

AMAA currently pins no model anywhere. Two authorities disagree, and AMAA cannot
satisfy both.

## Why AMAA is not deciding this itself

This is filed as a **Tier-2 proposal**, not authored as `planned`, because
resolving a contradiction between two standing authorities is architectural and
affects the release pipeline — outside AMAA's Tier-0 slice. AMAA does not
self-approve it, and has deliberately left the gap open rather than pick a side.

## The two authorities

**RP-MODEL-01** — `design/specs/role-plugins-spec.md`, `status: authoritative`,
`authority: PRRD ▶ SPEC ▶ TRDD`, on the `governance-rules` branch of
`Emasoft/ai-maestro` (unmerged; 2906 ahead of `main`):

> Every shipped role-plugin PINS `model: opus` on the main-agent (frontmatter) and
> in the toml, and OMITS `model:` on subagents. This contradicts the general
> "omit `model:`, inherit session" guidance (CLAUDE.md distillation / CPV CA-04);
> it validates + installs fine today and is the established pattern. Recorded as a
> live inconsistency, not resolved — a new role-plugin SHOULD copy the pattern.

**CPV CA-04** — the cache-warmth invariant enforced by the validator that gates
AMAA's publish: an agent inherits the session model; the dispatch site decides any
override at call time. Under CA-04 an unpinned agent is the correct default.

## What is actually true of AMAA today (verified)

| Rule | AMAA | Verdict |
|---|---|---|
| RP-VAL-01/03 quad-identity | matches across all four | ✅ |
| RP-VAL-02 toml mandatory fields | `compatible-titles = ["ARCHITECT"]`, `compatible-clients = ["claude-code"]` | ✅ |
| RP-VAL-04 element prefix | every non-main element carries `amaa-` / `amaa_` | ✅ |
| RP-VAL-06 subagents carry NO `model:` / `hooks:` | none do | ✅ |
| RP-MODEL-01 main-agent + toml pin `model: opus` | absent in both | ⚠️ open |

So the gap is a single field in two files. Nothing else in the spec is unmet.

## Arguments for leaving AMAA unpinned (status quo)

- RP-MODEL-01 says **SHOULD**, and scopes it to a **new** role-plugin. AMAA is an
  existing shipped one.
- The spec's own validation checklist (RP-VAL-01…07) contains **no** main-agent
  model-pin check. A conformance tool built from RP-VAL passes AMAA as-is.
- The spec labels the rule an unresolved inconsistency **in its own text**.
- Pinning puts the spec in direct conflict with the gate that guards AMAA's
  release.

## Arguments for pinning

- Fleet consistency: the other seven predefined role-plugins reportedly pin it, so
  AMAA is the odd one out, and "established pattern" has real value for anyone
  reading several role-plugins side by side.
- A pin makes the intended model explicit rather than dependent on whatever the
  invoking session happens to be running.

## New information the ruling should account for

Claude Code **2.1.219** made **Opus 5** (`claude-opus-5`, 1M context) the default
Opus. `model: opus` therefore resolves to a different, larger-context, differently
priced model than when the RP-MODEL-01 pattern was established. Whoever rules
should rule on what the token means **now**, not on what it meant historically.
Separately, CC 2.1.223 added a warning when a requested subagent model is
restricted and the parent model runs instead — a pin that cannot resolve degrades
silently to the parent.

## Requested decision

One of:

1. **Pin** — AMAA adds `model: opus` to the main-agent frontmatter and the toml,
   and CPV's CA-04 guidance is amended to exempt role-plugin main-agents.
2. **Do not pin** — RP-MODEL-01 is amended to record that role-plugin main-agents
   omit `model:`, aligning the spec with CA-04, and the other role-plugins drop
   their pins.
3. **Explicit split** — RP-MODEL-01 is amended to say the pin is optional and
   non-conformance-bearing, so both shapes are valid and neither tool flags it.

Any of the three closes the contradiction. AMAA has no preference between them
and will implement whichever is ruled; what it cannot do is keep shipping against
two rules that disagree.

## Approval log

- 2026-08-07T19:27:20+0200 — Filed as a Tier-2 proposal by the ARCHITECT. Routes
  to MANAGER via AMCOS. Not authorized to execute; awaiting a ruling.
