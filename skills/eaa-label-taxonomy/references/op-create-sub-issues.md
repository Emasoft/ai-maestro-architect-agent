---
name: op-create-sub-issues
description: Operation procedure for creating component-specific sub-issues from an epic.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Create Sub-Issues

## Purpose

Break down a complex issue (epic) into smaller, component-specific sub-issues that can be assigned and tracked independently.

## When to Use

- When issue is labeled `type:epic`
- When architecture analysis reveals multiple distinct work items
- When work spans multiple components and needs parallel execution

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Parent issue number
- Completed architecture breakdown identifying sub-tasks
- Component labels defined in repository

## Procedure

### Step 1: Verify Parent Issue is Epic

```bash
IS_EPIC=$(gh issue view $PARENT_ISSUE --json labels --jq '.labels[].name | select(. == "type:epic")')
if [ -z "$IS_EPIC" ]; then
  # Mark as epic if complex
  gh issue edit $PARENT_ISSUE --add-label "type:epic"
fi
```

### Step 2: Define Sub-Issues from Architecture

For each distinct component/task:

| Sub-Issue | Component | Effort | Description |
|-----------|-----------|--------|-------------|
| API endpoints | component:api | effort:s | Implement REST endpoints |
| Database schema | component:database | effort:s | Add user table columns |
| Auth integration | component:auth | effort:m | Connect to auth service |

### Step 3: Create Each Sub-Issue

```bash
gh issue create \
  --title "[$PARENT_ISSUE] $SUB_TASK_TITLE" \
  --body "Part of #$PARENT_ISSUE

## Description
$SUB_TASK_DESCRIPTION

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Parent Issue
Closes part of #$PARENT_ISSUE" \
  --label "type:feature" \
  --label "component:$COMPONENT" \
  --label "status:backlog" \
  --label "effort:$EFFORT"
```

### Step 4: Link Sub-Issues to Parent

Update parent issue with links:

```bash
gh issue comment $PARENT_ISSUE --body "## Sub-Issues Created

This epic has been decomposed into:
- #$SUB_ISSUE_1 - API endpoints
- #$SUB_ISSUE_2 - Database schema
- #$SUB_ISSUE_3 - Auth integration

All sub-issues must be completed before this epic can be closed."
```

### Step 5: Update Parent Status

```bash
# Parent stays in backlog until sub-issues start
gh issue edit $PARENT_ISSUE --add-label "status:backlog"
```

### Step 6: Verify Sub-Issues Created

```bash
# Search for linked issues
gh issue list --search "in:body #$PARENT_ISSUE"
```

## Example

**Scenario:** Issue #123 is an epic for "User Authentication". Create sub-issues.

```bash
PARENT=123

# Create API sub-issue
gh issue create \
  --title "[#123] API endpoints for user authentication" \
  --body "Part of #123

## Description
Implement REST API endpoints for authentication flow:
- POST /auth/login
- POST /auth/logout
- GET /auth/me

## Acceptance Criteria
- [ ] Endpoints return proper HTTP codes
- [ ] Validation on all inputs
- [ ] Unit tests for each endpoint

## Parent Issue
Closes part of #123" \
  --label "type:feature" \
  --label "component:api" \
  --label "status:backlog" \
  --label "effort:s"

# Create Database sub-issue
gh issue create \
  --title "[#123] Database schema for user storage" \
  --body "Part of #123

## Description
Add database tables/columns for user authentication:
- users table with password_hash
- sessions table for token storage

## Acceptance Criteria
- [ ] Migration files created
- [ ] Rollback migration works
- [ ] Indexes on lookup columns

## Parent Issue
Closes part of #123" \
  --label "type:feature" \
  --label "component:database" \
  --label "status:backlog" \
  --label "effort:s"

# Update parent with links
gh issue comment 123 --body "## Sub-Issues Created

This epic has been decomposed into:
- #124 - API endpoints for user authentication
- #125 - Database schema for user storage

All sub-issues must be completed before this epic can be closed."
```

## Sub-Issue Naming Convention

```
[#PARENT_ID] COMPONENT - Brief description
```

Examples:
- `[#123] API endpoints for user authentication`
- `[#123] Database schema for user storage`
- `[#123] Auth service integration`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Duplicate titles | Similar sub-issues | Differentiate by component in title |
| Label not found | Component label missing | Create label first |
| Too many sub-issues | Over-decomposition | Combine related tasks |
| Circular reference | Sub-issue references itself | Remove self-reference from body |

## Notes

- Keep sub-issues small enough to be completed in one session
- Each sub-issue should be independently testable
- Use consistent naming conventions for easy tracking
