---
trdd-id: WDM195GD
title: Repair the planning-patterns script surface — broken cross_platform import and phantom docstring filenames
column: completed
created: 2026-08-18T19:54:10+0200
updated: 2026-08-18T20:50:00+0200
current-owner: ai-maestro-architect-agent
task-type: bugfix
scope: project
approval-tier: 0
implementation-commits: [2ca94c3]
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-18

- Source of truth: `reports/plugin-self-audit/20260816_171026+0200-axis3-scripts.md`
  (C1 + C3, ARCHITECT-verified count-exact) — hub-ledgered under programme TRDD-BRRJK57P,
  Phase-2 GO received 2026-08-18.
- NEXT ACTION: docs first (fix the 8 phantom filenames), then the import fix, then the
  runnable check.
- 2026-08-18 advisor expansion (Fable, verified first-hand): analyzer_scaffold.py has the
  broken insert TWICE — line 15-16 (own import) AND lines 251-253 inside the generated
  template, which `--help` can never exercise; fix the template by INLINING the two atomic
  helpers so generated analyzers are standalone, and smoke-test with generate+py_compile.
  validate_plan.py:26 and health_auditor.py:24 also import `thresholds` — the lib/ retarget
  covers it (lib/thresholds.py exists).

## The two stacked defects (one card, per axis3's own Phase-2 note)

1. **10 scripts crash on ANY invocation** (`--help` included). Every one under
   `skills/amaa-planning-patterns/scripts/` does
   `sys.path.insert(0, str(SKILLS_DIR / "shared"))` — but `skills/shared/` does not exist;
   the module lives at repo-root `lib/cross_platform.py`. The insert is a no-op and
   `from cross_platform import …` raises `ModuleNotFoundError` before argparse runs.
   The 10: analyzer_scaffold, dependency_resolver, generate_planning_checklist,
   generate_risk_register, generate_roadmap_template, generate_status_report,
   generate_task_tracker, health_auditor, project_detector, validate_plan.
2. **8 phantom hyphenated filenames in docstrings/docs** (debug-workflow.py,
   generate-planning-checklist.py, generate-risk-register.py, generate-roadmap-template.py,
   generate-task-tracker.py, list-runners.py, setup-secrets.py, validate-yaml.py) — the
   real files use underscores. Four overlap the crash set: a user fixes the filename
   themselves and is then met with the C1 traceback.

## Fix direction (ratified by the axis3 verification note)

- Do NOT create `skills/shared/` — that adds a second home for a module that already has
  one. Point the insert at the existing `lib/` (`Path(__file__).resolve().parents[3] / "lib"`)
  — one-line change per script, same line in all 10.
- `planner.py` carries the same dead insert but never imports `cross_platform` — remove the
  vestigial line there too (no-legacy rule).
- Fix all 8 phantom filenames at their citation sites (docstrings + skill READMEs/references
  listed in axis3 C1/C3).
- Check: run all 14 scripts in the dir with `--help`; PASS = 14/14 exit 0. The 4 that work
  today (bun-build-template, executor, install_lsp, ruff-config-template) are the positive
  control.

## Approval log

- 2026-08-18T20:50:00+0200 — COMPLETED by ai-maestro-architect-agent (tier 0), impl
  2ca94c3. All checks green: 15/15 scripts --help exit 0, generated scaffold compiles
  and runs (standalone, helpers inlined), phantom-name grep zero, ruff gate clean.
  Advisor expansion (template site + thresholds imports) covered.
