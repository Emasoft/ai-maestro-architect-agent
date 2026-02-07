---
operation: plan-implementation
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-planning-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Plan Implementation Tasks

## When to Use

Use this operation when:
- Roadmap phases need to be broken into actionable tasks
- Team members need specific assignments
- Daily/weekly work tracking is needed
- Critical path analysis is required
- Sprint or iteration planning is happening

## Prerequisites

- Completed roadmap with defined phases and milestones
- Identified team members and their availability
- Understanding of task dependencies
- Access to task tracking system (GitHub Issues, Jira, etc.)

## Procedure

### Step 1: Break Down Milestones into Tasks

Decompose each milestone into small, focused tasks.

**Task characteristics:**
- Single person can complete
- Completable in 1-3 days
- Has clear acceptance criteria
- Has clear deliverable

**Task sizing guideline:**
| Size | Duration | Description |
|------|----------|-------------|
| Small | 0.5-1 day | Single function, config change |
| Medium | 1-2 days | Feature component, integration |
| Large | 2-3 days | Complex feature, significant refactor |

**If task exceeds 3 days:** Split into smaller tasks.

```markdown
## Milestone M2: Users Can Login

### Tasks

| ID | Task | Size | Estimate | Acceptance Criteria |
|----|------|------|----------|---------------------|
| T1 | Create user table schema | Small | 0.5d | Migration runs successfully |
| T2 | Implement user registration | Medium | 1.5d | POST /register creates user |
| T3 | Implement password hashing | Small | 0.5d | Passwords stored hashed |
| T4 | Implement login endpoint | Medium | 1d | POST /login returns token |
| T5 | Implement token validation | Medium | 1d | Invalid tokens rejected |
| T6 | Write integration tests | Medium | 1d | All auth flows tested |
```

### Step 2: Create Dependency Network

Map which tasks depend on others.

**Dependency types:**
- Finish-to-Start (FS): Task B cannot start until Task A finishes
- Start-to-Start (SS): Task B cannot start until Task A starts
- Finish-to-Finish (FF): Task B cannot finish until Task A finishes

**Document dependencies:**
```markdown
## Task Dependencies

T1 (Schema) → T2 (Registration) → T3 (Hashing) → T4 (Login) → T5 (Validation) → T6 (Tests)
                                                    ↑
                                                 parallel
                                                    ↓
                                              T5 (Validation)
```

**Critical path:** The longest sequence of dependent tasks determines minimum duration.

### Step 3: Assign Owners and Create Responsibility Matrix

Assign each task to a specific person.

**RACI Matrix:**
| Role | Meaning |
|------|---------|
| Responsible | Does the work |
| Accountable | Approves the work |
| Consulted | Provides input |
| Informed | Kept updated |

```markdown
## Responsibility Matrix

| Task | Alice (Backend) | Bob (Backend) | Carol (QA) |
|------|-----------------|---------------|------------|
| T1 Schema | R, A | I | I |
| T2 Registration | R | A | C |
| T3 Hashing | C | R, A | I |
| T4 Login | R | A | C |
| T5 Validation | A | R | C |
| T6 Tests | C | C | R, A |
```

### Step 4: Create Daily/Weekly Tracking

Set up tracking mechanism for execution.

```markdown
## Week 3 Plan

### Monday
- T1 Schema [Alice] - START
- T2 Registration [Alice] - START

### Tuesday
- T1 Schema [Alice] - COMPLETE
- T2 Registration [Alice] - IN PROGRESS
- T3 Hashing [Bob] - START

### Wednesday
- T2 Registration [Alice] - COMPLETE
- T3 Hashing [Bob] - COMPLETE
- T4 Login [Alice] - START

### Thursday
- T4 Login [Alice] - IN PROGRESS
- T5 Validation [Bob] - START

### Friday
- T4 Login [Alice] - COMPLETE
- T5 Validation [Bob] - IN PROGRESS
- T6 Tests [Carol] - START
```

### Step 5: Define Success Criteria

Each task needs measurable completion criteria.

```markdown
## Task Success Criteria

### T4: Implement Login Endpoint

**Definition of Done:**
- [ ] POST /login endpoint exists
- [ ] Accepts email and password in request body
- [ ] Returns 200 with JWT token on success
- [ ] Returns 401 on invalid credentials
- [ ] Returns 400 on missing fields
- [ ] Unit tests pass (>80% coverage)
- [ ] Code reviewed and approved
- [ ] Documentation updated
```

## Checklist

Copy this checklist and track your progress:

- [ ] List all milestones to break down
- [ ] Break each milestone into tasks (max 3 days)
- [ ] Size each task (Small/Medium/Large)
- [ ] Estimate effort for each task
- [ ] Define acceptance criteria for each task
- [ ] Map task dependencies
- [ ] Identify critical path
- [ ] Assign owner to each task
- [ ] Create RACI matrix
- [ ] Set up tracking board (GitHub Projects, etc.)
- [ ] Create first week's daily plan
- [ ] Schedule daily standups

## Examples

### Example: Authentication Implementation Plan

```markdown
# Implementation Plan: Authentication System

## Phase 2: Core Authentication (Weeks 3-5)

### Milestone M2: Basic Login Working

#### Task Breakdown

| ID | Task | Owner | Size | Est | Dependencies | Status |
|----|------|-------|------|-----|--------------|--------|
| T2.1 | Create users table migration | Alice | S | 4h | None | TODO |
| T2.2 | Implement User model | Alice | S | 4h | T2.1 | TODO |
| T2.3 | Create registration endpoint | Bob | M | 8h | T2.2 | TODO |
| T2.4 | Implement password hashing | Bob | S | 4h | T2.3 | TODO |
| T2.5 | Create login endpoint | Alice | M | 8h | T2.4 | TODO |
| T2.6 | Implement JWT generation | Alice | M | 6h | T2.5 | TODO |
| T2.7 | Create auth middleware | Bob | M | 6h | T2.6 | TODO |
| T2.8 | Write unit tests | Carol | M | 8h | T2.7 | TODO |
| T2.9 | Write integration tests | Carol | M | 8h | T2.8 | TODO |

Total: 56 hours (7 person-days)

#### Critical Path

T2.1 → T2.2 → T2.3 → T2.4 → T2.5 → T2.6 → T2.7 → T2.8 → T2.9

Duration: 9 tasks, minimum 7 days (with parallelization)

#### Week 3 Schedule

| Day | Alice | Bob | Carol |
|-----|-------|-----|-------|
| Mon | T2.1, T2.2 | - | - |
| Tue | - | T2.3 | - |
| Wed | - | T2.4 | - |
| Thu | T2.5 | - | - |
| Fri | T2.6 | T2.7 | - |

| Day | Alice | Bob | Carol |
|-----|-------|-----|-------|
| Mon | Review | Review | T2.8 |
| Tue | - | - | T2.8 |
| Wed | - | - | T2.9 |
```

### Example: Task Card Template

```markdown
## Task T2.5: Create Login Endpoint

**Owner:** Alice
**Size:** Medium (8h)
**Sprint:** Week 3
**Dependencies:** T2.4 (password hashing)

### Description
Create POST /login endpoint that authenticates users with email/password
and returns a JWT token.

### Acceptance Criteria
- [ ] POST /api/auth/login endpoint exists
- [ ] Request body: { "email": string, "password": string }
- [ ] Response 200: { "token": string, "expires_at": timestamp }
- [ ] Response 401: { "error": "Invalid credentials" }
- [ ] Response 400: { "error": "Missing required fields" }
- [ ] Password compared using bcrypt
- [ ] Login attempts logged for audit

### Technical Notes
- Use existing User model from T2.2
- Use password hashing from T2.4
- JWT secret from environment variable

### Definition of Done
- [ ] Code implemented
- [ ] Unit tests written (>80% coverage)
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Merged to main branch
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Tasks too large | Insufficient decomposition | Split any task >3 days |
| Missing dependencies | Incomplete analysis | Review each task's inputs |
| Unrealistic estimates | Optimism bias | Add buffer, use historical data |
| Overloaded owner | Too much assigned | Balance load across team |
| Unclear acceptance criteria | Vague definition | Write specific, testable criteria |
| Critical path too long | Sequential dependencies | Find opportunities for parallelization |

## Related Operations

- [op-create-roadmap.md](op-create-roadmap.md) - Roadmap defines phases to plan
- [op-identify-risks.md](op-identify-risks.md) - Risks inform task priorities
- [op-design-architecture.md](op-design-architecture.md) - Architecture defines what to build
