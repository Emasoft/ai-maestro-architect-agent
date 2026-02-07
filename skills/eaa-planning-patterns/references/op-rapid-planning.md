---
operation: rapid-planning
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-planning-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Rapid Planning Under Pressure

## When to Use

Use this operation when:
- Deadline is imminent and full planning is not possible
- Crisis situation requires quick action plan
- Minimum viable plan is needed immediately
- Time pressure prevents thorough analysis
- Need to start work while planning continues in parallel

## Prerequisites

- Clear understanding of the primary goal
- Knowledge of critical constraints (time, resources)
- Access to key decision makers
- Ability to iterate and refine plan later

## Procedure

### Step 1: Quick Architecture (30-60 minutes)

Focus on critical components only.

**Do:**
- Identify the 3-5 most critical components
- Define their single most important responsibility
- Map the primary data flow only
- Identify the most critical dependency

**Skip (for now):**
- Comprehensive component list
- All possible data flows
- Secondary integrations
- Nice-to-have features

```markdown
## Quick Architecture

### Critical Components (3)
1. auth-service - User authentication
2. api-gateway - Request routing
3. user-store - Credential storage

### Primary Data Flow
Client -> api-gateway -> auth-service -> user-store -> response

### Critical Dependency
auth-service MUST have user-store available
```

### Step 2: Quick Risk Identification (15-30 minutes)

Identify only blocking risks.

**Focus on:**
- Risks that would stop the project entirely
- Risks with probability > 50%
- Risks with no workaround

**Questions:**
1. What could prevent us from starting?
2. What could cause complete failure?
3. What has no fallback?

```markdown
## Top 5 Blocking Risks

1. [HIGH] No database access - blocker
   Mitigation: Verify credentials NOW

2. [HIGH] API rate limits - could block testing
   Mitigation: Request limit increase TODAY

3. [MEDIUM] Key developer on vacation next week
   Mitigation: Get knowledge transfer by Friday

4. [MEDIUM] Unclear requirements for feature X
   Mitigation: Meeting with stakeholder TODAY

5. [LOW] Third-party service might deprecate endpoint
   Mitigation: Check documentation, low priority
```

### Step 3: Quick Roadmap (15-30 minutes)

Define rough sequence and critical path.

**Do:**
- Identify the first deliverable
- Identify the critical path only
- Set rough time estimates
- Define the MVP milestone

**Skip (for now):**
- Detailed phase breakdown
- Resource allocation
- Buffer calculations

```markdown
## Quick Roadmap

### Week 1: Foundation + Auth
Day 1-2: Environment setup
Day 3-4: Basic auth implementation
Day 5: MVP auth working

### Week 2: Core + Integration
Day 6-7: Core feature
Day 8-9: Integration
Day 10: MVP complete

### Critical Path
Setup -> Auth -> Core -> Integration -> MVP
```

### Step 4: Plan Immediate Next Phase (30-60 minutes)

Detail only the next phase thoroughly.

**For next 3-5 days:**
- Specific tasks with owners
- Clear acceptance criteria
- Daily checkpoints

```markdown
## Immediate Plan (Next 5 Days)

### Day 1 (Today)
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| AM | Database setup | Alice | Connection working |
| PM | Project skeleton | Bob | Hello world endpoint |

### Day 2
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| AM | User schema | Alice | Migration runs |
| PM | Registration | Bob | POST /register works |

### Day 3
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| AM | Login endpoint | Alice | POST /login works |
| PM | Token validation | Bob | Middleware rejects invalid |

### Day 4
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| AM | Integration | Both | End-to-end flow |
| PM | Testing | Both | Basic tests pass |

### Day 5
| Time | Task | Owner | Deliverable |
|------|------|-------|-------------|
| AM | Bug fixes | Both | Critical issues resolved |
| PM | Demo prep | Both | MVP demo ready |
```

### Step 5: Plan Remaining Phases at High Level

Rough plan for later phases (detail will come later).

```markdown
## Later Phases (High Level)

### Week 2: Enhancement
- OAuth integration
- Session management
- Detailed logging

### Week 3: Polish
- Security hardening
- Performance tuning
- Documentation

(Will detail each phase when we get there)
```

## Key Principle

**All four phases required, but faster execution:**

| Phase | Normal Duration | Rapid Duration |
|-------|-----------------|----------------|
| Architecture | 1-2 days | 30-60 minutes |
| Risk Identification | 1 day | 15-30 minutes |
| Roadmap | 1-2 days | 15-30 minutes |
| Immediate Tasks | 1 day | 30-60 minutes |
| **Total** | 4-6 days | 1.5-3 hours |

## Checklist

Copy this checklist and track your progress:

- [ ] Quick architecture: identify 3-5 critical components
- [ ] Map primary data flow only
- [ ] Identify top 5 blocking risks
- [ ] Define mitigation for top 2 risks
- [ ] Create rough 2-week roadmap
- [ ] Identify MVP milestone
- [ ] Detail next 5 days with tasks and owners
- [ ] Schedule daily checkpoint meeting
- [ ] Document assumptions and unknowns
- [ ] Plan follow-up planning session

## Examples

### Example: Emergency Auth System Plan

```markdown
# Rapid Plan: Authentication System
**Time Budget:** 2 hours
**Deadline:** 2 weeks

## Quick Architecture (45 min)

### Critical Components
1. **auth-service** - Handle login/register
2. **user-db** - Store credentials
3. **token-cache** - Fast token validation

### Primary Flow
```
Login: Client -> auth-service -> user-db -> token-cache -> Client (token)
Validate: Client (token) -> token-cache -> allow/deny
```

## Quick Risks (20 min)

| # | Risk | Impact | Action Today |
|---|------|--------|--------------|
| 1 | DB access pending | BLOCKER | Get credentials NOW |
| 2 | Redis not provisioned | HIGH | Request from ops |
| 3 | No clear password policy | MEDIUM | Confirm with security |

## Quick Roadmap (15 min)

```
Week 1: Basic auth working
  Day 1-3: Setup + registration
  Day 4-5: Login + tokens

Week 2: Hardening + OAuth
  Day 6-8: OAuth integration
  Day 9-10: Security review
```

**MVP:** Users can register and login with email/password (Day 5)

## Immediate Tasks (40 min)

### Today (Day 1)
- [ ] Alice: Set up project, get DB credentials (AM)
- [ ] Bob: Create user schema draft (AM)
- [ ] Alice: Implement registration (PM)
- [ ] Bob: Set up Redis (PM)

### Tomorrow (Day 2)
- [ ] Alice: Password hashing (AM)
- [ ] Bob: Token generation (AM)
- [ ] Both: Integration (PM)

### Day 3
- [ ] Both: Login endpoint complete
- [ ] Both: Basic tests

## Unknowns (to resolve this week)
- Exact password requirements
- Token expiration policy
- Audit logging requirements

## Follow-up Planning
- Detailed Week 2 plan: Friday 4pm
```

### Example: Time-Boxed Planning Session

```markdown
## Rapid Planning Session Agenda

Total Time: 2 hours

### 0:00-0:10 - Context Setting (10 min)
- What is the goal?
- What is the hard deadline?
- What resources do we have?

### 0:10-0:40 - Quick Architecture (30 min)
- Whiteboard critical components
- Draw primary data flow
- Identify one critical dependency

### 0:40-1:00 - Quick Risks (20 min)
- Brainstorm blocking risks
- Pick top 5
- Assign mitigation owners

### 1:00-1:20 - Quick Roadmap (20 min)
- Define 2-3 phases
- Set MVP milestone
- Rough timeline

### 1:20-1:50 - Immediate Tasks (30 min)
- Detail next 5 days
- Assign owners
- Set daily checkpoints

### 1:50-2:00 - Wrap-up (10 min)
- Document unknowns
- Schedule follow-up
- Confirm first actions
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Still trying to plan everything | Perfectionism | Enforce time boxes ruthlessly |
| Skipping phases entirely | Over-correction | Do all 4 phases, just faster |
| No follow-up planned | Crisis mode | Always schedule detailed planning later |
| Unclear immediate tasks | Rushed task definition | Spend more time on Day 1-2 tasks |
| Missing critical risk | Too fast risk analysis | Check: "What stops us completely?" |

## Related Operations

- [op-design-architecture.md](op-design-architecture.md) - Full architecture when time permits
- [op-identify-risks.md](op-identify-risks.md) - Full risk analysis when time permits
- [op-create-roadmap.md](op-create-roadmap.md) - Full roadmap when time permits
- [op-plan-implementation.md](op-plan-implementation.md) - Full task planning when time permits
