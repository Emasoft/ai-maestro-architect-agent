# AMAA Label Taxonomy - Extended Examples

> **Multi-Repo Rule**: All `gh` commands MUST include `--repo "$OWNER_REPO"`. Set `OWNER_REPO=<owner>/<repo>` before running any command.

## Table of Contents

- Example 1: Adding Component Labels After Architecture Analysis
- Example 2: Validating Effort Estimate
- Example 3: Creating Component-Specific Sub-Issues
- Example 4: Architecture Decision Record (ADR)

## Example 1: Adding Component Labels After Architecture Analysis

```bash
# Scenario: Issue #123 requires API endpoint and database schema changes
# Action: Add component labels based on architecture breakdown
gh issue edit 123 --add-label "component:api" --add-label "component:database" --repo "$OWNER_REPO"
# Result: Issue now tagged with all affected components
```

## Example 2: Validating Effort Estimate

```bash
# Scenario: Issue #123 labeled effort:s but architecture reveals 3 components
# Action: Recommend effort upgrade
gh issue comment 123 --repo "$OWNER_REPO" --body "Architecture analysis suggests effort:m (3 components: API, DB, Auth)"
gh issue edit 123 --remove-label "effort:s" --add-label "effort:m" --repo "$OWNER_REPO"
# Result: Effort estimate now matches architecture complexity
```

## Example 3: Creating Component-Specific Sub-Issues

```bash
# Scenario: Issue #123 is complex, needs breakdown
# Action: Create sub-issues for each component
gh issue create \
  --repo "$OWNER_REPO" \
  --title "[#123] API endpoints for user authentication" \
  --body "Part of #123 - Implements REST API for auth flow" \
  --label "type:feature" \
  --label "component:api" \
  --label "status:backlog" \
  --label "effort:s"
# Repeat for database and auth components
# Result: Epic decomposed into manageable sub-issues
```

## Example 4: Architecture Decision Record (ADR)

```bash
# Scenario: Major architecture decision needs documentation
# Action: Create ADR issue with appropriate labels
gh issue create \
  --repo "$OWNER_REPO" \
  --title "[ADR-005] PostgreSQL vs MongoDB for user storage" \
  --body "Evaluating database options..." \
  --label "type:docs" \
  --label "component:database" \
  --label "priority:high"
# Result: ADR tracked and linked to affected component
```
