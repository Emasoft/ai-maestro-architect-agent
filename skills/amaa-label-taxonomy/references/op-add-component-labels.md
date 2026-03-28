---
name: op-add-component-labels
description: Operation procedure for adding component labels to an issue after architecture analysis.
---

# Operation: Add Component Labels




## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Example](#example)
- [Component Label Reference](#component-label-reference)
- [Error Handling](#error-handling)

## Purpose

After completing architecture analysis, apply component labels to an issue to indicate which parts of the system are affected by the work.

## When to Use

- After completing architecture breakdown for a feature
- When design reveals additional components
- When updating scope after design changes

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Target repo identified: `OWNER_REPO=<owner>/<repo>` (use `amp-project-repos.sh`)
- Issue number to label
- Completed architecture analysis identifying affected components

> **Multi-Repo Rule**: All `gh` commands below MUST include `--repo "$OWNER_REPO"`.

## Procedure

### Step 1: Review Architecture Analysis

Document which components are affected:

| Component | Label | Affected Because |
|-----------|-------|------------------|
| API layer | `component:api` | New/modified endpoints |
| User interface | `component:ui` | UI changes required |
| Database | `component:database` | Schema or query changes |
| Authentication | `component:auth` | Auth flow changes |
| Infrastructure | `component:infra` | DevOps/deployment changes |
| Core logic | `component:core` | Business logic changes |
| Tests | `component:tests` | Test framework changes |
| Documentation | `component:docs` | Doc system changes |

### Step 2: Verify Labels Exist in Repository

```bash
# Check if component labels exist
for COMP in api ui database auth infra core tests docs; do
  gh label list --repo "$OWNER_REPO" --search "component:$COMP" --json name --jq '.[].name'
done
```

If missing, create them:

```bash
gh label create "component:api" --description "API endpoints" --color "0052CC" --repo "$OWNER_REPO"
```

### Step 3: Add Component Labels to Issue

```bash
# Add multiple component labels
gh issue edit $ISSUE_NUMBER \
  --add-label "component:api" \
  --add-label "component:database" \
  --repo "$OWNER_REPO"
```

### Step 4: Document Component Breakdown in Comment

```bash
gh issue comment $ISSUE_NUMBER --repo "$OWNER_REPO" --body "## Architecture Analysis

**Components Affected:**
- \`component:api\` - New REST endpoints for user authentication
- \`component:database\` - User schema modifications

**Rationale:** [Brief explanation of why these components are involved]"
```

### Step 5: Verify Labels Applied

```bash
gh issue view $ISSUE_NUMBER --repo "$OWNER_REPO" --json labels --jq '.labels[].name | select(startswith("component:"))'
```

## Example

**Scenario:** Issue #123 requires API endpoint and database schema changes.

```bash
OWNER_REPO="myorg/backend-api"  # Always set target repo first

# Step 1: Add component labels based on analysis
gh issue edit 123 --add-label "component:api" --add-label "component:database" --repo "$OWNER_REPO"

# Step 2: Document in comment
gh issue comment 123 --repo "$OWNER_REPO" --body "## Architecture Analysis

**Components Affected:**
- \`component:api\` - New REST endpoints for authentication flow
- \`component:database\` - User table schema modifications

**Sub-tasks will be created for each component.**"

# Step 3: Verify
gh issue view 123 --repo "$OWNER_REPO" --json labels --jq '.labels[].name'
# Output includes: component:api, component:database
```

## Component Label Reference

| Label | Description | Common Triggers |
|-------|-------------|-----------------|
| `component:api` | API endpoints | REST/GraphQL changes |
| `component:ui` | User interface | Frontend changes |
| `component:database` | Database/storage | Schema, queries |
| `component:auth` | Authentication | Login, permissions |
| `component:infra` | Infrastructure | Docker, CI/CD, configs |
| `component:core` | Core business logic | Domain logic |
| `component:tests` | Test infrastructure | Test framework |
| `component:docs` | Documentation | Doc system changes |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Label not found | Component label doesn't exist | Create label with `gh label create --repo "$OWNER_REPO"` |
| Permission denied | No write access | Verify GitHub token scopes |
| Issue not found | Invalid issue number | Verify with `gh issue list --repo "$OWNER_REPO"` |
| Duplicate label | Already applied | No action needed, continue |
