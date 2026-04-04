# Fix Log — ai-maestro-architect-agent — 2026-04-04

## Summary

Fixed 26 of 26 actionable issues (25 MINOR + 1 NIT). 7 WARNINGs skipped (advisory only).

## Issues Fixed

### MINOR (25 issues) — Non-user-invocable skills missing "Loaded by" attribution

**Root cause:** All 25 skills have `user-invocable: false` but lacked a "Loaded by <agent-name>" line
in the body, which the validator requires so it is clear which agent consumes the skill.

**Fix applied:** Added `Loaded by ai-maestro-architect-agent-main-agent` as a line immediately
after the H1 title in each SKILL.md file.

**Files modified:**
- skills/amaa-api-research/SKILL.md
- skills/amaa-api-research-ops/SKILL.md
- skills/amaa-cicd-design/SKILL.md
- skills/amaa-cicd-design-ops/SKILL.md
- skills/amaa-design-communication-patterns/SKILL.md
- skills/amaa-design-communication-patterns-ops/SKILL.md
- skills/amaa-design-lifecycle/SKILL.md
- skills/amaa-design-lifecycle-ops/SKILL.md
- skills/amaa-design-management/SKILL.md
- skills/amaa-design-management-ops/SKILL.md
- skills/amaa-documentation-writing/SKILL.md
- skills/amaa-documentation-writing-ops/SKILL.md
- skills/amaa-github-integration-ops/SKILL.md
- skills/amaa-hypothesis-verification/SKILL.md
- skills/amaa-hypothesis-verification-ops/SKILL.md
- skills/amaa-label-taxonomy/SKILL.md
- skills/amaa-label-taxonomy-ops/SKILL.md
- skills/amaa-modularization/SKILL.md
- skills/amaa-modularization-ops/SKILL.md
- skills/amaa-planning-patterns/SKILL.md
- skills/amaa-planning-patterns-ops/SKILL.md
- skills/amaa-requirements-analysis/SKILL.md
- skills/amaa-requirements-analysis-ops/SKILL.md
- skills/amaa-session-memory/SKILL.md
- skills/amaa-session-memory-ops/SKILL.md

### NIT (1 issue) — Referenced file 'design-template.md' missing Table of Contents

**Root cause:** `skills/amaa-design-lifecycle/templates/design-template.md` (111 lines) had no
Table of Contents section, violating the rule that all .md reference files should include a TOC
for progressive discovery.

**Fix applied:** Added a `## Table of Contents` section with links to all 8 sections after the
metadata header in `skills/amaa-design-lifecycle/templates/design-template.md`.

**File modified:** skills/amaa-design-lifecycle/templates/design-template.md

## Skipped (WARNINGs — advisory only)

- .python-version not found
- Unknown top-level field '_note' in hooks/hooks.json
- README.md missing badge markers
- Possible broken backtick paths in SKILL.md files
- Dead URL in planning-patterns reference file
- No cliff.toml found

## Result

CRITICAL=0, MAJOR=0, MINOR=0, NIT=0 (expected after fixes). WARNING=7 (skipped by policy).
