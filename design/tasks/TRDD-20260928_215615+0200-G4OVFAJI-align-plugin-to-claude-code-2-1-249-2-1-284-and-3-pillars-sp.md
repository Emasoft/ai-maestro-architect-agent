---
trdd-id: G4OVFAJI
title: Align plugin to Claude Code 2.1.249-2.1.284 and 3-pillars spec vocabulary
column: ai_review
status: tasked
created: 2026-09-28T21:56:15+0200
updated: 2026-09-28T22:06:57+0200
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
---

# Align plugin to Claude Code 2.1.249-2.1.284 and 3-pillars spec vocabulary

Align published guidance to current canon: 22-column kanban vocabulary (19 lifecycle + 3 exception, 3P-KAN), five bracket values, transition-authority rows (no design-to-dispatch for ARCH), channel-reference rows 2.1.251-2.1.284, executor todo-tools note to the 2.1.268 allowlist. Spec source of truth: ai-maestro design/specs/3-pillars-spec.md at governance-rules fde29683. Acceptance: zero 17-column hits; positive checks for 19 lifecycle / 22 columns; channel table carries the six new rows; executor cites 2.1.268; py-compile clean.

## Approval log

- 2026-09-28T21:56:15+0200 — MANDATE issued by main-agent@autonomous (min-approval-requirement: none). Pre-approved: issuer authority >= required approver. No approval request was sent.
- 2026-09-28T21:56:23+0200 — column → todo. Reviewed proposal, both gate spawns returned, spec canon verified first-hand
- 2026-09-28T22:00:40+0200 — column → dev. Canary passed; five workers dispatched on verified plan
- 2026-09-28T22:06:45+0200 — column → testing. All five worker reports verified first-hand; review fixes applied; committed 4641396
- 2026-09-28T22:06:57+0200 — column → ai_review. Acceptance checklist all green (A1-A6); awaiting review verdict on final state
