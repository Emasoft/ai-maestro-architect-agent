---
trdd-id: HN65IC8P
title: Resolve the report_output dead mandate — zero callers for a function whose docstring says all scripts must use it
column: completed
created: 2026-08-18T19:54:10+0200
updated: 2026-08-18T20:35:00+0200
current-owner: ai-maestro-architect-agent
task-type: refactor
scope: project
approval-tier: 0
implementation-commits: [9d2c936]
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-18

- Source of truth: `reports/plugin-self-audit/20260816_170524+0200-axis1-missing-features.md`
  C2 (two-pass, positive-controlled). Hub-ledgered under TRDD-BRRJK57P; Phase-2 GO.
- NEXT ACTION: delete `report_output()` and its mandate line; keep the rest of
  `lib/report_utils.py` only if anything else in it has callers (verify with an unbounded
  grep first).

## The finding

`lib/report_utils.py:3` mandates *"All scripts should use report_output() instead of
printing verbose content directly"* — and `report_output` has **zero callers** repo-wide
(only the definition + its own docstring match). The sibling `cross_platform.py` IS
imported by ~9 scripts, so the import mechanism works; this function is simply dead.

## Decision (Tier 0)

**Delete, don't adopt.** Wiring 50 scripts through an unused helper to honour a docstring
is speculative work nobody asked for; the no-dead-code / no-legacy rules say one version
of reality only. The report-location discipline the docstring gestured at is already
enforced by the global `agent-reports-location` rule, not by this helper.

- Verify nothing else in `lib/report_utils.py` is imported (unbounded grep, positive
  control against `cross_platform`); if the whole module is caller-less, remove the file;
  if siblings have callers, remove only `report_output` + the mandate docstring line.
- README.md:167's `lib/` description stays accurate either way (it describes
  `thresholds.py`/`cross_platform.py`).
- Commit before delete (RULE 0); the function remains recoverable from history.

## Approval log

- 2026-08-18T20:35:00+0200 — COMPLETED by ai-maestro-architect-agent (tier 0). Whole
  module deleted at 9d2c936: unbounded grep found zero callers for report_output AND
  make_report_header (positive control: cross_platform's 11 importers); advisor
  independently confirmed whole-file delete safe and order-independent.
