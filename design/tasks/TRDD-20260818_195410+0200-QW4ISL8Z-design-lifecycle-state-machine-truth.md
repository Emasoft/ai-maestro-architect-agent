---
trdd-id: QW4ISL8Z
title: Reconcile the design-lifecycle state machine with its docs and close the archive bypass
column: todo
created: 2026-08-18T19:54:10+0200
updated: 2026-08-18T19:54:10+0200
current-owner: ai-maestro-architect-agent
task-type: bugfix
scope: project
approval-tier: 0
implementation-commits: []
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-18

- Source of truth: `reports/plugin-self-audit/20260816_170524+0200-axis1-missing-features.md`
  (C1 + the 2026-08-16 CORRECTION section — the hub-re-derived "two writers" finding).
  Hub-ledgered under TRDD-BRRJK57P; Phase-2 GO 2026-08-18. Specs move FIRST.
- NEXT ACTION: ratify the 5-state code machine as source of truth; correct the three docs;
  then route the archive writers through the guard.

## The findings

1. **Doc-vs-code drift:** `README.md:157`, `skills/amaa-design-lifecycle/SKILL.md:14`, and
   `references/op-manage-state-transitions.md:41-52` promise
   `DRAFT → REVIEW → APPROVED → IMPLEMENTING → COMPLETED → ARCHIVED`. The machine in
   `scripts/amaa_design_lifecycle.py:39-63` has neither `implementing` nor `completed` —
   only `implemented`. `SKILL.md:73`'s error-recovery advice cites the three states that
   do not exist, so the remedy offered at the moment of failure produces a second failure.
2. **The archive path bypasses the state machine (two writers):**
   `VALID_TRANSITIONS` contains no edge into `archived`, yet
   `amaa_design_lifecycle.py:189` (`archive_document`) writes `status: archived` via regex,
   and `amaa_github_sync_status.py:49,95` also maps/announces `archived` — so whatever
   invariant the transition guard should enforce before archiving is enforced nowhere.

## Decision (taken here, Tier 0 — code is truth)

The **5-state machine is the better design** — `implementing`/`completed` as separate
states carried no information the single `implemented` state lacks, and the
`implemented → review` redesign-loop edge (load-bearing comment at lines 55-60) must be
preserved. So:

- **Docs change, not the enum:** rewrite the three doc sites (+ SKILL.md:73 recovery row)
  to the real lifecycle `DRAFT → REVIEW → APPROVED → IMPLEMENTED → (archive subcommand)`,
  with `deprecated`/`superseded` as the exception exits.
- **Archive stays a subcommand, but gains a guard:** `archive_document()` must refuse to
  archive from a state the design does not sanction (allow from `implemented`,
  `deprecated`, `superseded`; refuse from `draft`/`review`/`approved` without `--force`),
  and set the status through one shared code path instead of a raw regex, so there is ONE
  writer. `amaa_github_sync_status.py` only *reads/relays* the status — verify, and leave
  it a reader.
- Check: transition-map extraction script (the axis1 verification snippet) + an
  archive-from-draft refusal test.

## Approval log
