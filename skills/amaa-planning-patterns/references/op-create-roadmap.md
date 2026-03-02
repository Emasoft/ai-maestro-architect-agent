---
operation: create-roadmap
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-planning-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Create Roadmap


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Define Phases](#step-1-define-phases)
- [Phases](#phases)
  - [Phase 1: Foundation (Weeks 1-2)](#phase-1-foundation-weeks-1-2)
  - [Phase 2: Core Features (Weeks 3-6)](#phase-2-core-features-weeks-3-6)
  - [Phase 3: Integration (Weeks 7-8)](#phase-3-integration-weeks-7-8)
  - [Step 2: Sequence Phases by Dependencies](#step-2-sequence-phases-by-dependencies)
- [Phase Dependencies](#phase-dependencies)
  - [Step 3: Define Milestones and Deliverables](#step-3-define-milestones-and-deliverables)
- [Milestones](#milestones)
  - [Step 4: Allocate Resources and Estimate Effort](#step-4-allocate-resources-and-estimate-effort)
- [Resource Allocation](#resource-allocation)
  - [Step 5: Create the Master Roadmap](#step-5-create-the-master-roadmap)
- [Master Roadmap](#master-roadmap)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Authentication System Roadmap](#example-authentication-system-roadmap)
- [Timeline: 8 Weeks](#timeline-8-weeks)
  - [Phase 1: Foundation (Weeks 1-2)](#phase-1-foundation-weeks-1-2)
  - [Phase 2: Core Authentication (Weeks 3-5)](#phase-2-core-authentication-weeks-3-5)
  - [Phase 3: OAuth Integration (Weeks 6-7)](#phase-3-oauth-integration-weeks-6-7)
  - [Phase 4: Security & Polish (Week 8)](#phase-4-security-polish-week-8)
- [Total Effort: 80 person-days](#total-effort-80-person-days)
- [Buffer: 16 person-days (20%)](#buffer-16-person-days-20)
- [Total with Buffer: 96 person-days](#total-with-buffer-96-person-days)
  - [Example: Dependency Graph](#example-dependency-graph)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Architecture is designed and risks are identified
- You need a sequenced execution plan
- Stakeholders need visibility into timeline and milestones
- Resource allocation needs to be planned
- Dependencies between work items need to be documented

## Prerequisites

- Completed architecture design document
- Risk register with prioritized risks
- Understanding of available resources
- Stakeholder alignment on priorities

## Procedure

### Step 1: Define Phases

Group related work into logical phases.

**Phase characteristics:**
- Each phase has a clear goal
- Phases are roughly similar in duration
- Phases produce demonstrable outcomes
- Phases can be reviewed and approved

**Example phases:**
```markdown
## Phases

### Phase 1: Foundation (Weeks 1-2)
**Goal:** Establish core infrastructure
**Deliverables:**
- Development environment setup
- CI/CD pipeline
- Base project structure

### Phase 2: Core Features (Weeks 3-6)
**Goal:** Implement primary functionality
**Deliverables:**
- User authentication
- Core business logic
- Data persistence

### Phase 3: Integration (Weeks 7-8)
**Goal:** Connect all components
**Deliverables:**
- API integration
- Third-party services
- End-to-end testing
```

### Step 2: Sequence Phases by Dependencies

Order phases based on what must come first.

**Dependency rules:**
- Infrastructure before application
- Core before extensions
- Internal before external integrations
- Security throughout

**Document dependencies:**
```markdown
## Phase Dependencies

Phase 1: Foundation
  └── Phase 2: Core Features (depends on Phase 1)
        └── Phase 3: Integration (depends on Phase 2)
              └── Phase 4: Polish (depends on Phase 3)
```

### Step 3: Define Milestones and Deliverables

Identify specific checkpoints within each phase.

**Milestone characteristics:**
- Clear completion criteria
- Demonstrable to stakeholders
- Marks meaningful progress
- Gates for go/no-go decisions

```markdown
## Milestones

| ID | Milestone | Phase | Target Date | Success Criteria |
|----|-----------|-------|-------------|------------------|
| M1 | Environment Ready | 1 | Week 1 | All devs can build locally |
| M2 | Auth Complete | 2 | Week 4 | Users can login/logout |
| M3 | Core MVP | 2 | Week 6 | Primary workflow functional |
| M4 | Integration Done | 3 | Week 8 | All APIs connected |
```

### Step 4: Allocate Resources and Estimate Effort

Assign people and estimate work.

**Estimation guidelines:**
- Use story points or time-based estimates
- Include buffer for unknowns (typically 20-30%)
- Consider parallel vs sequential work
- Account for meetings, reviews, testing

```markdown
## Resource Allocation

| Phase | Team Members | Duration | Effort (person-days) |
|-------|--------------|----------|---------------------|
| Phase 1 | DevOps, Backend | 2 weeks | 20 |
| Phase 2 | Backend (2), Frontend (2) | 4 weeks | 80 |
| Phase 3 | Backend, QA | 2 weeks | 20 |
```

### Step 5: Create the Master Roadmap

Compile everything into a visual and textual roadmap.

**Roadmap formats:**
- Timeline view (Gantt-style)
- Milestone view (checkpoints)
- Dependency view (network diagram)

```markdown
## Master Roadmap

Week 1-2: Foundation
  |-- Environment setup
  |-- CI/CD pipeline
  |-- [M1] Environment Ready

Week 3-4: Core Features - Part 1
  |-- Authentication service
  |-- User management
  |-- [M2] Auth Complete

Week 5-6: Core Features - Part 2
  |-- Business logic
  |-- Data persistence
  |-- [M3] Core MVP

Week 7-8: Integration
  |-- API integration
  |-- Testing
  |-- [M4] Integration Done
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify all major phases
- [ ] Define goal for each phase
- [ ] List deliverables for each phase
- [ ] Sequence phases by dependencies
- [ ] Create dependency graph
- [ ] Define milestones with success criteria
- [ ] Estimate effort for each phase
- [ ] Allocate resources to phases
- [ ] Add buffer time (20-30%)
- [ ] Create master roadmap document
- [ ] Have stakeholders review roadmap
- [ ] Get sign-off on timeline

## Examples

### Example: Authentication System Roadmap

```markdown
# Authentication System Roadmap

## Timeline: 8 Weeks

### Phase 1: Foundation (Weeks 1-2)

**Goal:** Development infrastructure ready

**Deliverables:**
- [ ] Local development environment
- [ ] CI/CD pipeline with automated tests
- [ ] Database schema v1
- [ ] API specification draft

**Milestone M1:** Dev environment operational
**Success Criteria:** All developers can run tests locally

**Resources:** 1 DevOps, 1 Backend (20 person-days)

---

### Phase 2: Core Authentication (Weeks 3-5)

**Goal:** Basic authentication working end-to-end

**Deliverables:**
- [ ] User registration
- [ ] Email/password login
- [ ] JWT token issuance
- [ ] Token validation middleware

**Dependencies:** Phase 1 complete

**Milestone M2:** Users can register and login
**Success Criteria:**
- Registration creates user in database
- Login returns valid JWT
- Protected endpoints reject invalid tokens

**Resources:** 2 Backend (30 person-days)

---

### Phase 3: OAuth Integration (Weeks 6-7)

**Goal:** Third-party authentication working

**Deliverables:**
- [ ] Google OAuth integration
- [ ] GitHub OAuth integration
- [ ] Account linking
- [ ] Session management

**Dependencies:** Phase 2 complete (base auth needed for linking)

**Milestone M3:** OAuth providers functional
**Success Criteria:** Users can login with Google or GitHub

**Resources:** 2 Backend (20 person-days)

---

### Phase 4: Security & Polish (Week 8)

**Goal:** Production-ready security

**Deliverables:**
- [ ] Rate limiting
- [ ] Security audit fixes
- [ ] Documentation
- [ ] Load testing

**Dependencies:** Phase 3 complete

**Milestone M4:** Security review passed
**Success Criteria:** All security checklist items complete

**Resources:** 1 Backend, 1 Security (10 person-days)

---

## Total Effort: 80 person-days
## Buffer: 16 person-days (20%)
## Total with Buffer: 96 person-days
```

### Example: Dependency Graph

```
Week 1-2          Week 3-5          Week 6-7          Week 8
[Foundation] --> [Core Auth] --> [OAuth Integration] --> [Security]
     |                |                   |
     v                v                   v
   [M1]             [M2]                [M3]
Environment      Login/Logout       OAuth Working
   Ready                                 |
                                        v
                                      [M4]
                                   Production
                                     Ready
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Phases overlap confusingly | Poor phase boundaries | Ensure each phase has clear start/end |
| Unrealistic timeline | Insufficient buffer | Add 20-30% buffer for unknowns |
| Missing dependencies | Incomplete analysis | Review each phase for inputs it needs |
| Resource conflicts | Same person in multiple phases | Stagger work or add resources |
| Milestones not measurable | Vague success criteria | Define specific, testable criteria |

## Related Operations

- [op-design-architecture.md](op-design-architecture.md) - Architecture defines what to build
- [op-identify-risks.md](op-identify-risks.md) - Risks inform buffer allocation
- [op-plan-implementation.md](op-plan-implementation.md) - Break roadmap into tasks
