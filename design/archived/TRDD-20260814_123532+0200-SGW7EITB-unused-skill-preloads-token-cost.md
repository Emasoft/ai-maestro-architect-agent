---
trdd-id: SGW7EITB
title: Remove or route the 10 unused skill preloads that are paid on every agent invocation
column: complete
created: 2026-08-14T12:35:32+0200
updated: 2026-08-14T13:26:22+0200
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

## 2026-08-14 — main agent analysed. The binary above is WRONG; there are THREE options

Investigated `agents/ai-maestro-architect-agent-main-agent.md` (699 lines, 9 preloaded
skills, 4 flagged). Two corrections to this card's own framing, both found by checking
rather than reasoning.

**Correction 1 — my first measurement was off by two lines and would have inverted a
decision.** I grepped the "body" as `NR>12`, but the frontmatter closes at **line 14**
(9 skills occupy 5–13), so two frontmatter lines leaked in. That produced a spurious
`amaa-prrd-trdd-kanban: 1 mention` — which was its own `skills:` entry, not prose.
True body counts confirm CPV exactly: **all four flagged skills have 0 mentions.**

**Correction 2 — "redundant with an already-routed skill" was an illusion created by
the agent body's own loose summaries.** The body says github-integration covers
"label management" (line 12) and session-memory covers "design artifacts organization"
(line 11). Reading the actual skills refutes both:

```
amaa-label-taxonomy      "GitHub labels: component, effort, type, priority"   81 lines
amaa-github-integration  "syncing designs to issues, managing project boards" 89 lines
amaa-design-management   "creating, searching, validating design docs; UUIDs" 81 lines
amaa-session-memory      "persisting decisions/patterns across sessions"      78 lines
amaa-requirements-analysis                                                    81 lines
amaa-prrd-trdd-kanban    "ARCHITECT's role in PRRD/TRDD/Kanban"              144 lines
```

They are distinct capabilities, not duplicates. Four of the six descriptions even end
`"Loaded by ai-maestro-architect-agent-main-agent"` — they were authored **as** this
agent's preloads. **I would have dropped two real capabilities on the authority of a
body summary line.** A body's prose description of another component is not evidence
about that component.

- **THE MISSING THIRD OPTION.** This card framed the fix as route-or-drop. But a skill
  can be a genuine capability AND still be wrong to preload: routing it from the body
  silences the warning while still paying its full text on EVERY invocation, including
  the majority of turns that never touch it. CPV says as much — *"this agent can use
  the 'Skill' tool, so it could load the skill on demand instead."* The real question
  per skill is **frequency**, not existence:

  ```
  (1) ROUTE + KEEP PRELOAD   needed on most invocations -> body must mention it
  (2) DROP THE PRELOAD       genuine but EPISODIC -> reachable on demand via Skill
  (3) DROP ENTIRELY          not a capability of this agent at all
  ```

  Option (2) is the one this card was missing, and on the evidence it is the common
  case.

- **Per-skill evidence for the main agent** (topic hits = body references to the WORK,
  under any wording; the CPV check only sees the literal skill name):

  ```
  skill                       literal  topic   size   provisional call
  amaa-prrd-trdd-kanban          0       53    144    (1) route — core, constant use
  amaa-requirements-analysis     0       16     81    (1) route — frequent
  amaa-design-management         0        3     81    (1)/(2) — it IS the agent's
                                                       stated DESIGN AUTHORITY
  amaa-label-taxonomy            0        2     81    (2) drop preload — episodic,
                                                       only when touching labels
  ```

  ~387 lines are currently injected on every invocation for these four.

## 2026-08-14 — DONE. All 10 decided and applied; preload WARNINGs 10 → 0.

**The defect had a sharper shape than "the body never mentions it":** the main agent
carries an explicit **`## Required Reading`** list, and it named exactly the 5 skills
that had literal mentions while the frontmatter preloaded **9**. The frontmatter and
the Required Reading list simply disagreed. That reframing is what made the
route-vs-drop calls decidable instead of a matter of taste.

```
agent / skill                        call  evidence
main-agent  amaa-prrd-trdd-kanban    (1)   0 literal / 53 topic — core, constant
main-agent  amaa-requirements-analys (1)   0 / 16 — "You analyze requirements" is the role
main-agent  amaa-design-management   (1)   DESIGN AUTHORITY: creates/owns design docs
main-agent  amaa-label-taxonomy      (2)   0 / 2 — episodic, only while managing labels
planner     amaa-session-memory      (2)   0 / 1
cicd-designer      amaa-session-mem  (2)   0 / 0
documentation-wr   amaa-session-mem  (2)   0 / 1
modularizer-exp    amaa-session-mem  (2)   0 / 0
api-researcher     amaa-session-mem  (2)   0 / 0
api-researcher     amaa-planning-pat (2)   0 / 0
```

The three `(1)` calls were added to **Required Reading** — a real routing entry that
tells the agent when to use each, not a token mention. The seven `(2)` calls were
dropped from `skills:`.

- **`amaa-session-memory` was the copy-paste default this card predicted, and the
  skill itself proves it.** Its description reads *"Loaded by
  ai-maestro-architect-agent-**main-agent**"* — it never claimed the sub-agents.
  Five of them preloaded it anyway, all with **zero** literal mentions and ~zero
  topic hits. Those five are single-turn bounded workers told to "do your bounded
  unit of work and return"; cross-session context restoration is not their job.
  **Dropping it made the skill's own declaration true rather than false.**
- **A coupling that nearly bit:** CPV requires a non-user-invocable skill to declare
  `Loaded by <agent>` **or** `Used by <agent>`. `amaa-label-taxonomy` said "Loaded
  by …main-agent", so dropping its preload would have made that claim false. CPV
  accepts both spellings and the distinction is exactly the one at issue —
  preloaded = *loaded by*, on-demand = *used by* — so its description now reads
  "**Used on demand by** …". `amaa-session-memory` and `amaa-planning-patterns`
  needed no such edit: both name the main agent, which still preloads and routes to
  them.
- **`amaa-planner` KEPT `amaa-planning-patterns`** — CPV flagged planner only for
  session-memory, and the body does route to planning-patterns (1 mention).
  Verified rather than swept up with its neighbours.

**Measured effect — removed from per-invocation context:**

```
amaa-session-memory     78 lines x 5 agents = 390
amaa-label-taxonomy     81 lines x 1 agent  =  81
amaa-planning-patterns  76 lines x 1 agent  =  76
                                       TOTAL 547 lines, on every invocation
```

## Acceptance criteria — final

- [x] All 10 (agent, skill) pairs classified with the reason recorded, decided by
      reading each body — not by pattern (see the table; `amaa-planner` is the case
      that would have been mis-swept by pattern).
- [x] `cpv-remote-validate plugin . --strict`: preload WARNINGs **0** (was 10).
- [x] No agent LOSES a capability — verified directly: **none of the 6 agents
      declares a `tools:` restriction**, so all inherit `Skill` and can load any
      dropped skill on demand.
- [x] Remaining CPV WARNING count accounted for: **5** (was 15). Those 5 are exactly
      the ones `TRDD-DMIRQOCD` documents as expected/by-design; none is new.
- [x] Full suite **404 passed / 3 skipped**, ruff clean.

**N — a skill dropped from `skills:` must remain reachable.** This agent declares no
`tools:` restriction, so it inherits `Skill` and option (2) is safe here. VERIFY that
per agent before applying it to the other five files; an agent with a restricted tool
list would lose the capability outright.

## Out of scope

The ruff/CPV pin work (that is `TRDD-DMIRQOCD`, currently blocked on a policy
decision), and the two `RC-PIPELINE-DRIFT-001` warnings, which are by-design and
already documented there.
