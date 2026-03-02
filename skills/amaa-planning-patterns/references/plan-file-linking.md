# Plan-to-GitHub Linking

## Table of Contents

1. [Purpose](#purpose)
2. [Linking Requirements](#linking-requirements)
   - [1. Plan → Issue Link](#1-plan--issue-link)
   - [2. Issue → Plan Link](#2-issue--plan-link)
   - [3. Sub-Issues Linking](#3-sub-issues-linking)
3. [Plan File Naming Convention](#plan-file-naming-convention)
4. [Automatic Linking](#automatic-linking)
5. [Progress Synchronization](#progress-synchronization)
   - [Plan → GitHub](#plan--github)
   - [GitHub → Plan](#github--plan)
6. [Traceability Matrix](#traceability-matrix)
7. [Orphan Detection](#orphan-detection)

## Purpose

Every implementation plan MUST be linked to GitHub issues for traceability and progress tracking.

## Linking Requirements

### 1. Plan → Issue Link

Every plan file must reference its GitHub issue:

```markdown
# Implementation Plan: User Authentication

**GitHub Issue**: [GH-42](https://github.com/owner/repo/issues/42)
**Status**: In Progress
**Assigned Agent**: dev-agent-1

## Overview
...
```

### 2. Issue → Plan Link

Every GitHub issue must reference its plan:

```markdown
## Implementation Plan

See detailed plan: `docs/plans/GH-42-user-auth.md`

**Plan Location**: docs/plans/GH-42-user-auth.md
**Plan Status**: Approved
```

### 3. Sub-Issues Linking

For epics with sub-issues:

```markdown
# Epic Plan: User Management

**GitHub Issue**: [GH-40](https://github.com/owner/repo/issues/40) (Epic)

## Sub-Plans

| Sub-Issue | Plan File | Status |
|-----------|-----------|--------|
| [GH-42](https://github.com/owner/repo/issues/42) | `plans/GH-42-auth.md` | Complete |
| [GH-43](https://github.com/owner/repo/issues/43) | `plans/GH-43-profile.md` | In Progress |
| [GH-44](https://github.com/owner/repo/issues/44) | `plans/GH-44-settings.md` | Not Started |
```

## Plan File Naming Convention

```
docs/plans/GH-{ISSUE_NUMBER}-{SHORT_DESCRIPTION}.md
```

Examples:
- `docs/plans/GH-42-user-auth.md`
- `docs/plans/GH-123-api-refactor.md`
- `docs/plans/GH-45-performance-optimization.md`

## Automatic Linking

When creating a plan, automatically:

1. Add plan reference to GitHub issue comment:

```bash
gh issue comment 42 --body "Implementation plan created: docs/plans/GH-42-user-auth.md"
```

2. Add issue reference to plan header

3. Create checklist in issue from plan steps:

```bash
gh issue edit 42 --body "$(cat <<'EOF'
## Implementation Checklist

- [ ] Step 1: Write tests
- [ ] Step 2: Implement endpoints
- [ ] Step 3: Add validation
- [ ] Step 4: Update documentation
EOF
)"
```

## Progress Synchronization

### Plan → GitHub

When plan step completes:
```bash
# Update issue checklist
gh issue edit 42 --body "$(sed 's/- \[ \] Step 1/- [x] Step 1/' current_body.md)"

# Add progress comment
gh issue comment 42 --body "Completed: Step 1 - Tests written"
```

### GitHub → Plan

When issue status changes:
- Update plan status header
- Add completion timestamp

## Traceability Matrix

Maintain in project root:

```markdown
# docs/TRACEABILITY.md

| Issue | Plan | PR | Status |
|-------|------|-----|--------|
| GH-42 | plans/GH-42-auth.md | PR-55 | Merged |
| GH-43 | plans/GH-43-profile.md | PR-58 | Review |
| GH-44 | plans/GH-44-settings.md | - | Planning |
```

## Orphan Detection

Check for:
- Plans without linked issues (orphan plans)
- Issues without plans (unplanned work)
- Stale links (renamed/moved files)

```bash
# Find orphan plans
for plan in docs/plans/GH-*.md; do
  issue=$(echo $plan | grep -oP 'GH-\d+')
  if ! gh issue view ${issue#GH-} &>/dev/null; then
    echo "ORPHAN: $plan"
  fi
done
```
