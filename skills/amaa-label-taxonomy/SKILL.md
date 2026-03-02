---
name: eaa-label-taxonomy
description: GitHub label taxonomy reference for the Architect Agent. Use when designing architecture, identifying components, or recommending labels. Trigger with architecture label requests.
version: 1.0.0
compatibility: Requires AI Maestro installed.
context: fork
user-invocable: false
workflow-instruction: "support"
procedure: "support-skill"
---

# EAA Label Taxonomy

## Overview

This skill provides the label taxonomy relevant to the Architect Agent (EAA) role. Each role plugin has its own label-taxonomy skill covering the labels that role manages.

---

## Prerequisites

1. GitHub CLI (`gh`) installed and authenticated
2. Active issue number for architecture work
3. Understanding of EAA role responsibilities (see **AGENT_OPERATIONS.md**)
4. Completed architecture analysis for the feature

---

## Instructions

1. Analyze requirements to identify all affected components
2. Review priority labels to understand design constraints
3. Check effort labels against design complexity
4. Recommend component labels based on module breakdown
5. Create sub-issues with appropriate type and component labels
6. Validate effort estimates and recommend changes if needed

### Checklist

Copy this checklist and track your progress:

**Architecture Label Workflow:**
- [ ] Analyze requirements to identify all affected components
- [ ] Review priority labels to understand design constraints
- [ ] Check effort labels against design complexity
- [ ] Recommend component labels based on module breakdown
- [ ] Create sub-issues with appropriate type and component labels
- [ ] Validate effort estimates and recommend changes if needed
- [ ] Add component labels to parent issue (e.g., `component:api`, `component:database`)
- [ ] If effort needs adjustment, update effort label (e.g., `effort:s` → `effort:m`)

**Architecture Handoff Checklist:**
- [ ] Ensure all `component:*` labels are set
- [ ] Ensure `effort:*` is validated and correct
- [ ] Create sub-issues if `type:epic`
- [ ] Document component breakdown in handoff to EOA

---

## Output

| Output Type | Format | Example |
|-------------|--------|---------|
| Component recommendations | Issue comment | `Affected components: api, database, auth` |
| Label updates | CLI stdout | `✓ Labels updated for #456` |
| Sub-issue creation | Issue URL | `Created #457 for API changes` |
| Effort validation | Issue comment | `Recommend upgrading effort:s → effort:m` |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `label not found` | Component label doesn't exist | Create label first via `gh label create` |
| `permission denied` | No write access to repo | Verify GitHub token scopes |
| `issue not found` | Invalid issue number | Verify issue number with `gh issue list` |
| `duplicate label` | Label already applied | No action needed, continue |

---

## Labels EAA Manages

### Component Labels (`component:*`)

**EAA recommends component labels during architecture design.**

| Label | Description | When EAA Recommends It |
|-------|-------------|------------------------|
| `component:api` | API endpoints | Feature touches REST/GraphQL APIs |
| `component:ui` | User interface | Feature has UI changes |
| `component:database` | Database/storage | Schema or query changes |
| `component:auth` | Authentication | Auth/authorization changes |
| `component:infra` | Infrastructure | DevOps/deployment changes |
| `component:core` | Core business logic | Central logic changes |
| `component:tests` | Test infrastructure | Test framework changes |
| `component:docs` | Documentation | Doc system changes |

**EAA Component Responsibilities:**
- Analyze requirements to identify affected components
- Recommend component labels in handoff to EOA
- Update component labels when design changes

### Kanban Columns (Canonical 8-Column System)

The full workflow uses these 8 status columns:

| # | Column Code | Display Name | Label | Description |
|---|-------------|-------------|-------|-------------|
| 1 | `backlog` | Backlog | `status:backlog` | Entry point for new tasks |
| 2 | `todo` | Todo | `status:todo` | Ready to start |
| 3 | `in-progress` | In Progress | `status:in-progress` | Active work |
| 4 | `ai-review` | AI Review | `status:ai-review` | Integrator agent reviews ALL tasks |
| 5 | `human-review` | Human Review | `status:human-review` | User reviews BIG tasks only (via EAMA) |
| 6 | `merge-release` | Merge/Release | `status:merge-release` | Ready to merge |
| 7 | `done` | Done | `status:done` | Completed |
| 8 | `blocked` | Blocked | `status:blocked` | Blocked at any stage |

**Task Routing Rules:**
- **Small tasks**: In Progress -> AI Review -> Merge/Release -> Done
- **Big tasks**: In Progress -> AI Review -> Human Review -> Merge/Release -> Done
- **Human Review** is requested via EAMA (Assistant Manager asks user to test/review)
- Not all tasks go through Human Review -- only significant changes requiring human judgment

### Type Labels EAA Clarifies

EAA may recommend type changes based on architecture analysis:

| Scenario | Type Recommendation |
|----------|---------------------|
| "Add feature" requires refactoring first | `type:refactor` for prep issue |
| Feature spans multiple systems | `type:epic` parent + `type:feature` children |
| Security implications discovered | Add `type:security` issue |

---

## Labels EAA Reads (Set by Others)

### Priority Labels (`priority:*`)

EAA uses priority to scope architecture:
- `priority:critical` - Minimal viable design, fastest path
- `priority:high` - Solid design, balance speed/quality
- `priority:normal` - Full architecture consideration
- `priority:low` - Can consider future extensibility

### Effort Labels (`effort:*`)

EAA validates effort estimates:
- Does design complexity match effort label?
- Should `effort:m` be upgraded to `effort:l`?
- EAA recommends effort changes to EOA

---

## EAA Label Commands

### When Completing Architecture

```bash
# Add component labels based on analysis
gh issue edit $ISSUE_NUMBER --add-label "component:api" --add-label "component:database"

# If effort estimate needs adjustment
gh issue edit $ISSUE_NUMBER --remove-label "effort:s" --add-label "effort:m"
```

### When Creating Sub-Issues

```bash
# Create component-specific sub-issues
gh issue create \
  --title "[$PARENT_ID] API changes for $FEATURE" \
  --body "Part of #$PARENT_ISSUE" \
  --label "type:feature" \
  --label "component:api" \
  --label "status:backlog"
```

### When Design Changes Scope

```bash
# Update type if scope changed during design
gh issue edit $ISSUE_NUMBER --remove-label "type:feature" --add-label "type:epic"

# Create child issues for the epic
```

---

## Architecture-to-Labels Mapping

### Module Breakdown → Component Labels

When EAA breaks down a feature:

```markdown
## Architecture Breakdown

### Feature: User Authentication

**Components Affected:**
- API layer (new endpoints) → `component:api`
- Database (user schema) → `component:database`
- Auth module (new) → `component:auth`
- UI (login form) → `component:ui`

**Recommended Labels:**
- `component:api`
- `component:database`
- `component:auth`
- `component:ui`
```

### Complexity Analysis → Effort Labels

| Architecture Complexity | Effort Recommendation |
|------------------------|----------------------|
| Single component, clear pattern | `effort:s` |
| 2-3 components, existing patterns | `effort:m` |
| Multiple components, new patterns | `effort:l` |
| System-wide, new architecture | `effort:xl` |

---

## Examples

### Example 1: Adding Component Labels After Architecture Analysis

```bash
# Scenario: Issue #123 requires API endpoint and database schema changes
# Action: Add component labels based on architecture breakdown
gh issue edit 123 --add-label "component:api" --add-label "component:database"
# Result: Issue now tagged with all affected components
```

### Example 2: Validating Effort Estimate

```bash
# Scenario: Issue #123 labeled effort:s but architecture reveals 3 components
# Action: Recommend effort upgrade
gh issue comment 123 --body "Architecture analysis suggests effort:m (3 components: API, DB, Auth)"
gh issue edit 123 --remove-label "effort:s" --add-label "effort:m"
# Result: Effort estimate now matches architecture complexity
```

### Example 3: Creating Component-Specific Sub-Issues

```bash
# Scenario: Issue #123 is complex, needs breakdown
# Action: Create sub-issues for each component
gh issue create \
  --title "[#123] API endpoints for user authentication" \
  --body "Part of #123 - Implements REST API for auth flow" \
  --label "type:feature" \
  --label "component:api" \
  --label "status:backlog" \
  --label "effort:s"
# Repeat for database and auth components
# Result: Epic decomposed into manageable sub-issues
```

### Example 4: Architecture Decision Record (ADR)

```bash
# Scenario: Major architecture decision needs documentation
# Action: Create ADR issue with appropriate labels
gh issue create \
  --title "[ADR-005] PostgreSQL vs MongoDB for user storage" \
  --body "Evaluating database options..." \
  --label "type:docs" \
  --label "component:database" \
  --label "priority:high"
# Result: ADR tracked and linked to affected component
```

---

## Quick Reference

### EAA Label Responsibilities

| Action | Labels Involved |
|--------|-----------------|
| Analyze requirements | Read `type:*`, `priority:*` |
| Identify components | Recommend `component:*` |
| Validate effort | Recommend `effort:*` changes |
| Create sub-issues | Set `type:*`, `component:*`, `status:backlog` |
| Design change | May update `type:*` (with EOA approval) |

### Labels EAA Never Sets

- `assign:*` - Set by EOA/ECOS
- `status:*` - Set by working agent
- `review:*` - Managed by EIA
- `priority:*` - Set by EAMA/EOA

### EAA Handoff Labels

When handing off design to EOA, EAA should ensure:
1. All `component:*` labels are set
2. `effort:*` is validated
3. Sub-issues created if `type:epic`

---

## ADR Labels Pattern

When creating Architecture Decision Records:

```bash
# Create ADR-related issue
gh issue create \
  --title "[ADR-001] Database choice for user storage" \
  --body "Architecture decision record..." \
  --label "type:docs" \
  --label "component:database" \
  --label "priority:high"
```

---

## Resources

- **AGENT_OPERATIONS.md** - EAA role definition and responsibilities
- **eaa-modularization** - Module breakdown procedures
