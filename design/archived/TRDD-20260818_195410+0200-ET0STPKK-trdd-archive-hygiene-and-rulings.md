---
trdd-id: ET0STPKK
title: Archive-column hygiene for the 9 archived cards and record the two governance rulings
column: todo
created: 2026-08-18T19:54:10+0200
updated: 2026-08-18T19:54:10+0200
current-owner: ai-maestro-architect-agent
task-type: docs
scope: project
approval-tier: 0
implementation-commits: []
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-18

- Source of truth: `reports/plugin-self-audit/20260816_170123+0200-axis2-governance.md`
  (V1, V2, V3) + hub rulings relayed in the Phase-2 GO dispatch (2026-08-18).
- NEXT ACTION: fix the 2 `column: complete` outliers, then record the two rulings in
  PROJECT wikimem.

## The three items

1. **Archived-column population (9 cards, 2 outliers).** `design/archived/` holds 9 cards;
   SGW7EITB and JKBVDN7G carry `column: complete` (mid-pipeline), not an archive-eligible
   terminal value. Per TRDD rule 12's narrow exception (a value FALSELY, machine-verifiably
   contradicting the terminal location may be corrected), set both to `column: completed`
   and bump `updated:`. The 7 siblings (`completed` ×5 pattern, `published` ×3) are already
   conformant.
2. **Legacy-UUID filenames — RECORD, DON'T MIGRATE (hub ruling).** The two 2026-06 cards
   (536c42e3, 364ccafc) predate the v2 8-char base36 id scheme. Renaming archived files
   destroys inbound references for zero operational gain; the ruling is to record the
   exception. Action: one PROJECT wikimem note stating the two filenames are grandfathered
   v1 ids, so no future lint pass "fixes" them.
3. **baseline-tag-protect — ruled RATIFIED-BASELINE COMPLIANCE (hub ruling).** The third
   ruleset (id 17715767, tag-target, deletion+update on `refs/tags/v*.*.*`,
   `bypass_actors: []`) is additive hardening consistent with the ratified baseline's
   intent; the hub ruling closes axis2 V1's provenance question. Action: record the ruling
   in the same wikimem note + this card's Approval log, so the next governance audit finds
   the provenance it could not find in-repo.

## Approval log

- 2026-08-18 — Hub dispatch (ai-maestro session, under USER verbatim delegation) ruled:
  legacy-uuid = record-don't-migrate; baseline-tag-protect = ratified-baseline compliance.
