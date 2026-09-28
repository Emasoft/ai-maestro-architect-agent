---
trdd-id: G4OVFAJI
title: Align plugin to Claude Code 2.1.249-2.1.284 and 3-pillars spec vocabulary
column: complete
status: archived
created: 2026-09-28T21:56:15+0200
updated: 2026-09-28T22:09:29+0200
current-owner: main-agent@autonomous
created-by: main-agent@autonomous
task-type: docs
min-approval-requirement: none
scope: project
project-id: autonomous
assignee: main-agent@autonomous
mandate: true
mandated-by: none
approved: true
approval-judge: main-agent@autonomous
approval-datetime: 2026-09-28T21:56:15+0200
relevant-rules: [2.1]
implementation-commits: [4641396, aab7138]
---

# Align plugin to Claude Code 2.1.249-2.1.284 and 3-pillars spec vocabulary

Align published guidance to current canon: 22-column kanban vocabulary (19 lifecycle + 3 exception, 3P-KAN), five bracket values, transition-authority rows (no design-to-dispatch for ARCH), channel-reference rows 2.1.251-2.1.284, executor todo-tools note to the 2.1.268 allowlist. Spec source of truth: ai-maestro design/specs/3-pillars-spec.md at governance-rules fde29683. Acceptance: zero 17-column hits; positive checks for 19 lifecycle / 22 columns; channel table carries the six new rows; executor cites 2.1.268; py-compile clean.

## Approval log

- 2026-09-28T21:56:15+0200 — MANDATE issued by main-agent@autonomous (min-approval-requirement: none). Pre-approved: issuer authority >= required approver. No approval request was sent.
- 2026-09-28T21:56:23+0200 — column → todo. Reviewed proposal, both gate spawns returned, spec canon verified first-hand
- 2026-09-28T22:00:40+0200 — column → dev. Canary passed; five workers dispatched on verified plan
- 2026-09-28T22:06:45+0200 — column → testing. All five worker reports verified first-hand; review fixes applied; committed 4641396
- 2026-09-28T22:06:57+0200 — column → ai_review. Acceptance checklist all green (A1-A6); awaiting review verdict on final state
- 2026-09-28T22:09:29+0200 — COMPLETE by main-agent@autonomous. All five acceptance criteria verified first-hand this session; ai_review findings fixed at 762f451.

## Acceptance criteria

- [x] Zero hits for 17-column vocabulary across agents/, skills/, commands/ (verified 2026-09-28)
- [x] Persona carries the 22-column canon (19 lifecycle + 3 exception) matching spec 4.0.0 §3P-KAN in substance
- [x] Channel reference carries rows 2.1.251/260/261/271/277/284, each attributed against the fetched changelog
- [x] executor.py cites 2.1.268 allowlist; py_compile clean
- [x] AMOA handoff blockquote sourced to governance-spec R6.5 (arch-int-member-edges), not to the removed transition row
