# AMAA Label Taxonomy - Detailed Reference

## Table of Contents

- Component Labels (`component:*`)
- Kanban Columns (Canonical 5-Column System)
- Type Labels AMAA Clarifies
- Priority Labels (`priority:*`) - Read by AMAA
- Effort Labels (`effort:*`) - Validated by AMAA
- Architecture-to-Labels Mapping
- Architecture Breakdown

## Component Labels (`component:*`)

AMAA recommends component labels during architecture design.

| Label | Description | When AMAA Recommends It |
|-------|-------------|------------------------|
| `component:api` | API endpoints | Feature touches REST/GraphQL APIs |
| `component:ui` | User interface | Feature has UI changes |
| `component:database` | Database/storage | Schema or query changes |
| `component:auth` | Authentication | Auth/authorization changes |
| `component:infra` | Infrastructure | DevOps/deployment changes |
| `component:core` | Core business logic | Central logic changes |
| `component:tests` | Test infrastructure | Test framework changes |
| `component:docs` | Documentation | Doc system changes |

**AMAA Component Responsibilities:**
- Analyze requirements to identify affected components
- Recommend component labels in handoff to AMOA
- Update component labels when design changes

## Kanban Columns (Canonical 5-Column System)

| # | Column Code | Display Name | Label | Description |
|---|-------------|-------------|-------|-------------|
| 1 | `backlog` | Backlog | `status:backlog` | Entry point for new tasks |
| 2 | `pending` | Pending | `status:pending` | Ready to start |
| 3 | `in_progress` | In Progress | `status:in_progress` | Active work |
| 4 | `review` | Review | `status:review` | Agent or human reviews task |
| 5 | `completed` | Completed | `status:completed` | Done |

**Task Routing Rules:**
- **Small tasks**: Pending -> In Progress -> Review -> Completed
- **Big tasks**: Pending -> In Progress -> Review (AI) -> Review (Human via AMAMA) -> Completed
- **Human Review** is requested via AMAMA (AI Maestro Assistant Manager asks user to test/review)
- Not all tasks go through Human Review -- only significant changes requiring human judgment

## Type Labels AMAA Clarifies

AMAA may recommend type changes based on architecture analysis:

| Scenario | Type Recommendation |
|----------|---------------------|
| "Add feature" requires refactoring first | `type:refactor` for prep issue |
| Feature spans multiple systems | `type:epic` parent + `type:feature` children |
| Security implications discovered | Add `type:security` issue |

## Priority Labels (`priority:*`) - Read by AMAA

AMAA uses priority to scope architecture:
- `priority:critical` - Minimal viable design, fastest path
- `priority:high` - Solid design, balance speed/quality
- `priority:normal` - Full architecture consideration
- `priority:low` - Can consider future extensibility

## Effort Labels (`effort:*`) - Validated by AMAA

AMAA validates effort estimates:
- Does design complexity match effort label?
- Should `effort:m` be upgraded to `effort:l`?
- AMAA recommends effort changes to AMOA

## Architecture-to-Labels Mapping

### Module Breakdown -> Component Labels

When AMAA breaks down a feature:

```markdown
## Architecture Breakdown

### Feature: User Authentication

**Components Affected:**
- API layer (new endpoints) -> `component:api`
- Database (user schema) -> `component:database`
- Auth module (new) -> `component:auth`
- UI (login form) -> `component:ui`

**Recommended Labels:**
- `component:api`
- `component:database`
- `component:auth`
- `component:ui`
```

### Complexity Analysis -> Effort Labels

| Architecture Complexity | Effort Recommendation |
|------------------------|----------------------|
| Single component, clear pattern | `effort:s` |
| 2-3 components, existing patterns | `effort:m` |
| Multiple components, new patterns | `effort:l` |
| System-wide, new architecture | `effort:xl` |

## AMAA Label Commands

### When Completing Architecture

```bash
# Add component labels based on analysis
gh issue edit $ISSUE_NUMBER --add-label "component:api" --add-label "component:database"

# If effort estimate needs adjustment
gh issue edit $ISSUE_NUMBER --remove-label "effort:s" --add-label "effort:m"
```

### When Creating Sub-Issues

```bash
gh issue create \
  --title "[$PARENT_ID] API changes for $FEATURE" \
  --body "Part of #$PARENT_ISSUE" \
  --label "type:feature" \
  --label "component:api" \
  --label "status:backlog"
```

### When Design Changes Scope

```bash
gh issue edit $ISSUE_NUMBER --remove-label "type:feature" --add-label "type:epic"
```

## Quick Reference

### AMAA Label Responsibilities

| Action | Labels Involved |
|--------|-----------------|
| Analyze requirements | Read `type:*`, `priority:*` |
| Identify components | Recommend `component:*` |
| Validate effort | Recommend `effort:*` changes |
| Create sub-issues | Set `type:*`, `component:*`, `status:backlog` |
| Design change | May update `type:*` (with AMOA approval) |

### Labels AMAA Never Sets

- `assign:*` - Set by AMOA/AMCOS
- `status:*` - Set by working agent
- `review:*` - Managed by AMIA
- `priority:*` - Set by AMAMA/AMOA

### AMAA Handoff Labels

When handing off design to AMOA, AMAA should ensure:
1. All `component:*` labels are set
2. `effort:*` is validated
3. Sub-issues created if `type:epic`

## ADR Labels Pattern

When creating Architecture Decision Records:

```bash
gh issue create \
  --title "[ADR-001] Database choice for user storage" \
  --body "Architecture decision record..." \
  --label "type:docs" \
  --label "component:database" \
  --label "priority:high"
```
