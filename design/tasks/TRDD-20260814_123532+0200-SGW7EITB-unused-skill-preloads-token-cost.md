---
trdd-id: SGW7EITB
title: Remove or route the 10 unused skill preloads that are paid on every agent invocation
column: todo
created: 2026-08-14T12:35:32+0200
updated: 2026-08-14T12:35:32+0200
current-owner: ai-maestro-architect-agent
task-type: refactor
scope: project
approval-tier: 0
relevant-rules: []
implementation-commits: []
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-14

- **WHY this card exists at all:** it was deferred *inside* `TRDD-DMIRQOCD` with the
  words *"a token-cost signal worth its own pass — not a blocker, and NOT part of
  this card"*, and then no card was filed. `TRDD-ZT5TP8YO` exists because that exact
  pattern nearly erased a different deferral: **a deferral recorded only inside
  another card is not a handoff, it is a note in a file nobody re-reads.** Filed now
  so it survives DMIRQOCD closing.
- **The finding is CURRENT, not remembered.** Re-confirmed in the real publish run
  that shipped v2.15.20 today — not read back off the old card.

## What the gate reports

CPV strict, 10 WARNINGs, all the same shape:

```
[WARNING] Skill '<skill>' is preloaded but the body never mentions it. A preload
injects the skill's FULL content into EVERY invocation of this agent, so an unused
one is paid for every turn; this agent can use the 'Skill' tool, so it could load
the skill on demand instead. Either route to it from the body (a prose/table
mention is enough) or drop it from 'skills'.
```

Distribution — 10 warnings over 6 agent files:

```
agents/ai-maestro-architect-agent-main-agent.md   4   amaa-design-management,
                                                      amaa-label-taxonomy,
                                                      amaa-requirements-analysis,
                                                      amaa-prrd-trdd-kanban
agents/amaa-api-researcher.md                     2   amaa-session-memory,
                                                      amaa-planning-patterns
agents/amaa-planner.md                            1   amaa-session-memory
agents/amaa-documentation-writer.md               1   amaa-session-memory
agents/amaa-modularizer-expert.md                 1   amaa-session-memory
agents/amaa-cicd-designer.md                      1   amaa-session-memory
```

The main agent is the worst case: **four** skills injected in full on every one of
its invocations, none of them referenced by its body.

## Why this is worth doing rather than suppressing

The cost is per-invocation and permanent: a preloaded skill's full text enters the
context of every single call to that agent, whether or not the agent needs it. That
is the same class of waste the token-economy rule targets (`~/.claude/rules/
token-economy-agents-and-scenarios.md` — L2, curate the tool/context surface), and
it compounds across a fleet where these agents are dispatched repeatedly.

`amaa-session-memory` accounts for **5 of the 10** — it looks like a
copy-paste default that spread across agents that never route to it.

## The decision each warning needs — and it is NOT uniform

CPV offers two remedies and they are not interchangeable. Per skill, per agent, ask
which is true:

1. **The agent genuinely uses it** → the defect is the BODY, not the frontmatter.
   Route to it in prose (a mention is enough) so the preload is justified and the
   reader can see why it is there.
2. **The agent does not use it** → drop it from `skills:`. It can still reach the
   skill on demand via the `Skill` tool, so dropping removes cost without removing
   capability.

**N — do NOT resolve these by adding a token mention to each body just to silence
the linter.** That converts a real cost signal into a permanent lie: the preload
still costs full price every turn, and the body now falsely implies the agent uses
it. Choosing (1) means the agent really does use the skill.

## Acceptance criteria

- [ ] Each of the 10 (agent, skill) pairs classified as (1) route or (2) drop, with
      the reason recorded — decided by reading the agent body, not by pattern.
- [ ] Changes applied; `cpv-remote-validate plugin . --strict` reports **0** of these
      preload WARNINGs.
- [ ] No agent LOSES a capability: any skill dropped from `skills:` must still be
      reachable via the `Skill` tool (confirm the agent's tool list includes it).
- [ ] The remaining CPV WARNING count is accounted for — 15 today, of which these are
      10; the other 5 (2 × `RC-PIPELINE-DRIFT-001`, 1 × `RC-TEST-COVERAGE`, …) are
      documented in DMIRQOCD as expected and are NOT in scope here.

## NEXT ACTION

Read `agents/ai-maestro-architect-agent-main-agent.md` first — it carries 4 of the 10
and is the highest-traffic agent, so it is both the biggest win and the best test of
whether the "route vs drop" call can be made from the body alone.

## Out of scope

The ruff/CPV pin work (that is `TRDD-DMIRQOCD`, currently blocked on a policy
decision), and the two `RC-PIPELINE-DRIFT-001` warnings, which are by-design and
already documented there.
