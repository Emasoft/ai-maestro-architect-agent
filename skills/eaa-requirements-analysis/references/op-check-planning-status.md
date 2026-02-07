---
operation: check-planning-status
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Check Planning Status Operation

## When to Use

Use this operation when:
- Checking current Plan Phase progress
- Verifying requirements section completion status
- Reviewing defined modules and their status
- Verifying exit criteria before approval
- Resuming work on an existing plan

## Prerequisites

- [ ] Plan Phase is active (`.claude/orchestrator-plan-phase.local.md` exists)
- [ ] Plugin is loaded and enabled

## Procedure

### Step 1: Execute Status Command

```bash
/planning-status
```

For detailed output including all modules:
```bash
/planning-status --verbose
```

### Step 2: Review Output Sections

The status output shows:
1. **Plan ID and Status** - Unique identifier and current phase (drafting/reviewing/approved)
2. **Locked Goal** - The project goal (cannot be changed without approval)
3. **Requirements Progress** - Each section with completion status
4. **Modules Defined** - List of modules with priorities and criteria
5. **Exit Criteria** - Checklist of conditions needed for approval

### Step 3: Identify Action Items

From the status output, identify:
- Requirement sections still pending or in_progress
- Modules missing acceptance criteria
- Exit criteria not yet met

## Checklist

Copy this checklist and track your progress:

- [ ] Execute `/planning-status`
- [ ] Review requirements section statuses
- [ ] Review module definitions and criteria
- [ ] Check exit criteria checklist
- [ ] Identify next actions needed

## Examples

### Example: Basic Status Check

```bash
/planning-status

# Expected output:
# +------------------------------------------------------------------+
# |                    PLAN PHASE STATUS                              |
# +------------------------------------------------------------------+
# | Plan ID: plan-20260109-143022                                     |
# | Status: drafting                                                  |
# | Goal: Build user authentication with OAuth2                       |
# +------------------------------------------------------------------+
# | REQUIREMENTS PROGRESS                                             |
# +------------------------------------------------------------------+
# | [x] Functional Requirements     - complete                        |
# | [>] Non-Functional Requirements - in_progress                     |
# | [ ] Architecture Design         - pending                         |
# +------------------------------------------------------------------+
```

### Example: Verbose Status with Modules

```bash
/planning-status --verbose

# Expected output includes:
# +------------------------------------------------------------------+
# | MODULES                                                           |
# +------------------------------------------------------------------+
# | auth-core    | High     | Support JWT tokens          | planned  |
# | user-mgmt    | Medium   | CRUD operations             | planned  |
# +------------------------------------------------------------------+
# | EXIT CRITERIA                                                     |
# +------------------------------------------------------------------+
# | [x] USER_REQUIREMENTS.md exists                                   |
# | [ ] All requirement sections complete                             |
# | [x] At least one module defined                                   |
# | [x] All modules have acceptance criteria                          |
# +------------------------------------------------------------------+
```

### Example: Status Before Approval

```bash
/planning-status --verbose

# All checkmarks indicate ready for approval:
# | EXIT CRITERIA                                                     |
# +------------------------------------------------------------------+
# | [x] USER_REQUIREMENTS.md exists                                   |
# | [x] All requirement sections complete                             |
# | [x] At least one module defined                                   |
# | [x] All modules have acceptance criteria                          |
# +------------------------------------------------------------------+
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| State file not found | Planning not started | Run `/start-planning` first |
| Invalid YAML in state file | Corrupted state | See troubleshooting.md section 5.7 |
| Cannot read state file | Permission issue | Check file permissions |

## Related Operations

- [op-start-planning.md](op-start-planning.md) - Start a new plan phase
- [op-modify-requirement-section.md](op-modify-requirement-section.md) - Update section status
- [op-approve-plan.md](op-approve-plan.md) - Approve when all criteria met
