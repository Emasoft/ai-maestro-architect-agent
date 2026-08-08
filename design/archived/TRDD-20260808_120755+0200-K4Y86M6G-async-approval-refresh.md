---
trdd-id: K4Y86M6G
title: Bring AMAA's choice trees onto the async-approval model
column: completed
created: 2026-08-08T12:07:55+0200
updated: 2026-08-08T15:23:02+0200
current-owner: ai-maestro-architect-agent
task-type: docs
scope: project
min-approval-requirement: none
mandate: true
mandated-by: self
project-id: ai-maestro-architect-agent
npt: []
eht: []
relevant-rules: []
external-refs: [TRDD-O16UGID8]
implementation-commits: [ce40b21ba063b294704f3c7ff7cf46411a2d19d8]
---

# Bring AMAA's choice trees onto the async-approval model

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body)

Implements the spec in **TRDD-O16UGID8** (`Emasoft/ai-maestro`, branch
`governance-rules`, blob `f74736c7a731`). That card owns the fleet sweep and the
two work orders; **this card owns AMAA's tree only** — I never edit the hub's repo.

## Why

The fleet-readiness sweep measured the mandate/approval overlay fields at
core=12, programmer=8, maintainer=6, **architect=0**. Reproduced first-hand on this
repo before starting: `min-approval-requirement` 0 files, `mandated-by` 0 files,
`^mandate:` 0 files.

AMAA's checklist/decision-tree corpus predates the async-approval model in
`rules/aimaestro/aimaestro-trdd-approval.md` (blob `ed1bc35310f6`). An agent whose
trees assume synchronous approval **waits** where the model says author-as-planned-
and-proceed. That is the stall class unsupervised operation cannot afford, and it
fails silently — a waiting agent looks like a working one.

## The five spec points, and where each landed

1. **Tier-0 is the default (self-mandate).** `agents/…-main-agent.md` — the tier
   list is rewritten around `min-approval-requirement:` titles; in-scope work and
   derived cards are authored `column: planned` with `mandate: true`,
   `mandated-by: self`, and proceed immediately.
2. **D1 never-block.** New section, placed *before* the obligations so it governs
   them rather than qualifying them afterwards. Also removed the three stale
   "and wait" instructions (below).
3. **The frontmatter fields.** Documented in the main agent (with the yaml block
   and the `## Approval log` no-round-trip line) and taught as an authoring step
   in `skills/amaa-prrd-trdd-kanban/SKILL.md`, including depth-1 derived fields.
   `approval-tier:` recorded as deprecated/decode-only in both.
4. **Completion gate.** Added to both: `complete` requires every `npt:` ∪ `eht:`
   child terminal, else `blocked` + `blocked-by:` + `pre-block-column:`.
5. **Trees REWRITTEN, not appended** — the discipline that made this worth doing.

## Stale "wait" instructions removed (rewritten in place)

| File | Was | Now |
|---|---|---|
| `agents/…-main-agent.md` (baseline deviation) | "file a proposal … and wait." | file with `min-approval-requirement: manager`, **then move on**; do-not-apply and do-not-idle separated as two different things |
| `agents/amaa-api-researcher.md` (RULE 14) | "escalate … WAIT for decision" | escalate, then continue the rest of the research; the escalation is filed, not attended |
| `skills/amaa-api-research-ops/SKILL.md` | "Orchestrator unresponsive → use [BLOCKED] format and wait" | report [BLOCKED], then continue other in-scope research |

**Deliberately NOT changed:** `skills/amaa-cicd-design/references/secret-management.md`
— its "will wait for approval if required reviewers configured" describes a GitHub
Actions environment gate in a design template for a *user's* pipeline, not an AI
Maestro approval path. Rewriting it would have been a false positive.

## Legacy field migration (on next touch, never a mass rewrite)

- `TRDD-M3RV5THO` — `approval-tier: 0` → `min-approval-requirement: none` +
  `mandate: true` + `mandated-by: self`. Mechanical re-spelling of the same fact,
  so `updated:` deliberately NOT bumped (bumping it would silently reorder the
  board on a repair that changed nothing).
- `TRDD-TYB3Q1NJ` — `approval-tier: 2` → `min-approval-requirement: manager` +
  `mandate: false` (it is a genuine request, not a mandate — AMAA cannot issue at
  the `manager` floor).
- `TRDD-DMIRQOCD` — untouched by this work, so **not** migrated. Adding fields to a
  card I have no other reason to open would be exactly the mass rewrite the rule
  forbids.

## Acceptance criteria

- [x] Reproduce the finding first-hand before building (0/0/0 confirmed)
- [x] Read the model at its SSOT (`aimaestro-trdd-approval.md`), not from the work order's summary
- [x] Tier list rewritten around `min-approval-requirement:` titles
- [x] D1 never-block stated, and placed so it governs the obligations
- [x] Mandate field set + `## Approval log` form documented and taught
- [x] Depth-1 derived fields + completion gate in both agent and skill
- [x] All in-scope "wait" instructions rewritten, none appended-beside
- [x] Legacy `approval-tier:` migrated on the two cards actually touched
- [x] Verification greps run and counts recorded, with the population stated
- [x] Published, CI green, closure record sent

## Verification (run on the working tree before publish)

Recorded in the closure message: the grep for each mandate field with its count,
and the "wait for approval" grep with its count **and its population**, so a zero
is distinguishable from a query that searched nothing.

## Approval log

- 2026-08-08T12:07:55+0200 — MANDATE issued by ARCHITECT ai-maestro-architect-agent
  (min-approval-requirement: none). Pre-approved: issuer authority >= required
  approver. No approval request was sent. In-scope docs work on AMAA's own tree,
  reversible, no baseline deviation, no other project touched.
- 2026-08-08T15:23:02+0200 — COMPLETED by ARCHITECT ai-maestro-architect-agent.
  All acceptance criteria checked; shipped in v2.13.0 (`ce40b21`); closure record
  sent and acknowledged by the hub, which archived its parent `TRDD-O16UGID8` as
  `completed` after reading my 9 stall-language grep hits individually (7 are the
  D1 doctrine's own phrasing, 2 legitimately gated).

  **This card was late to close, and that is the lesson.** The work finished and
  shipped hours before the column said so, leaving it asserting `planned` —
  indistinguishable on the board from a card nobody had started. A done card that
  stays open is worse than an unstarted one, because it hides the truth in the one
  view anyone consults. Close in the same session the work lands.
