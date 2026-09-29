---
trdd-id: 6YT0RQZE
title: Adopt GOV-R41 + PRRD golden-silver citation + G1.2 template bylines (issue 27)
column: ai_review
status: tasked
created: 2026-09-29T13:14:49+0200
updated: 2026-09-29T13:48:40+0200
current-owner: main-agent@autonomous
created-by: user
task-type: feature
min-approval-requirement: none
scope: project
project-id: autonomous
assignee: user
mandate: true
mandated-by: none
approved: true
approval-judge: user
approval-datetime: 2026-09-29T13:14:49+0200
unblock-when: [decision: when the 4.0.0 spec push lands on Emasoft/ai-maestro governance-rules, THEN re-adopt the 3P-ZON-06 express give-up archive ruling]
implementation-commits: [8c7b49d, 12f4f4d, b5aa52b, fb3aaff, 712d294, e57456c]
---

# Adopt GOV-R41 + PRRD golden-silver citation + G1.2 template bylines (issue 27)

Fleet issue 27 adoption wave. Cite R41 by number (governance-spec.md 2.6.1, governance-rules branch), fix the 3-pillars spec version citation 4.0.0->3.0.0 (pushed canon at fork head 0a76ca1c6; the 4.0.0 owner ruling 2026-09-24 TRDD-MQE5D28T is UNPUSHED and recorded pending re-adoption), insert the PRRD G1.2 byline into every GitHub-posting template (per-file judgment; secret-set files excluded; reuse the scripts/amaa_self_id.py SELF_ID_LINE wording), model the AMP self-id line in message templates/examples, and add one test pinning the markdown templates carry the byline. Acceptance per issue 27 checkboxes; report posted in-issue with the self-ID first line (opens with the self-ID line, cites R41/R41.6 by number, states the pending-4.0.0 disposition). The unblock-when predicate lives in frontmatter.

## Approval log

- 2026-09-29T13:14:49+0200 — MANDATE issued by user (min-approval-requirement: none). Pre-approved: issuer authority >= required approver. No approval request was sent.

## Close-out requirements

Acceptance report on issue 27: opens with the PRRD G1.2 self-ID line, cites R41/R41.6/R41.5 by number without restating content, states Pattern B verified-clean (contract form), and declares the pending-4.0.0 disposition explicitly.
Note: this corpus's PRRD project-id is the flagged placeholder 'autonomous'; the main-agent@autonomous owner id on this card is machine-valid but anchored to that pending owner decision.
