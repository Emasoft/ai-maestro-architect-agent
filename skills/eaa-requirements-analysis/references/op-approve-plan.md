---
operation: approve-plan
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Approve Plan Operation

## When to Use

Use this operation when:
- All requirement sections are marked complete
- All modules have defined acceptance criteria
- USER_REQUIREMENTS.md exists and is documented
- User has reviewed and approved the plan
- Ready to transition from Plan Phase to Orchestration Phase

## Prerequisites

All of these must be true:
- [ ] USER_REQUIREMENTS.md exists
- [ ] All requirement sections marked "complete"
- [ ] At least one module defined
- [ ] All modules have acceptance criteria
- [ ] User has explicitly approved the plan

## Procedure

### Step 1: Verify All Prerequisites

```bash
/planning-status --verbose
```

All exit criteria should show checkmarks.

### Step 2: Execute Approval

```bash
/approve-plan
```

To skip GitHub Issue creation (offline work):
```bash
/approve-plan --skip-issues
```

### Step 3: Verify Transition

```bash
# Check orchestration state file was created
ls .claude/orchestrator-exec-phase.local.md

# View orchestration status
/orchestration-status
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify USER_REQUIREMENTS.md exists
- [ ] Confirm all requirement sections are complete
- [ ] Confirm all modules have acceptance criteria
- [ ] Confirm at least one module is defined
- [ ] Get explicit user approval
- [ ] Execute `/approve-plan`
- [ ] Verify GitHub Issues created for each module
- [ ] Verify orchestration state file created
- [ ] Begin orchestration with `/start-orchestration`

## Examples

### Example: Standard Approval Workflow

```bash
# Step 1: Verify readiness
/planning-status --verbose

# Expected output shows all checkmarks:
# | EXIT CRITERIA                                                     |
# +------------------------------------------------------------------+
# | [x] USER_REQUIREMENTS.md exists                                   |
# | [x] All requirement sections complete                             |
# | [x] At least one module defined                                   |
# | [x] All modules have acceptance criteria                          |
# +------------------------------------------------------------------+

# Step 2: Approve
/approve-plan

# Expected output:
# Validating plan...
# Plan validation passed
#
# Creating GitHub Issues...
#   #42 - Auth Core (auth-core)
#   #43 - User Management (user-mgmt)
#
# Creating Orchestration Phase state file...
#
# +------------------------------------------------------------------+
# |                        PLAN APPROVED                              |
# +------------------------------------------------------------------+
# | Plan ID: plan-20260109-143022                                     |
# | Goal: Build a REST API for user management                        |
# +------------------------------------------------------------------+
# | GITHUB ISSUES CREATED                                             |
# +------------------------------------------------------------------+
# | #42 - Auth Core (auth-core)                    [priority-high]    |
# | #43 - User Management (user-mgmt)              [priority-medium]  |
# +------------------------------------------------------------------+
# | NEXT STEPS                                                        |
# +------------------------------------------------------------------+
# | 1. Run /start-orchestration to begin implementation               |
# | 2. Register remote agents with /register-agent                    |
# | 3. Assign modules with /assign-module                             |
# +------------------------------------------------------------------+

# Step 3: Begin orchestration
/start-orchestration
```

### Example: Offline Approval (Skip Issues)

```bash
# Approve without GitHub Issue creation
/approve-plan --skip-issues

# Expected output:
# Validating plan...
# Plan validation passed
#
# Skipping GitHub Issue creation (--skip-issues)
#
# Creating Orchestration Phase state file...
# ...

# Create issues manually later
gh issue create --title "[Module] Auth Core" --body "..." --label "module,priority-high"
```

### Example: Failed Approval

```bash
/approve-plan

# If prerequisites not met:
# Validating plan...
# Plan validation FAILED
#
# Missing prerequisites:
#   [ ] All requirement sections complete
#       - Architecture Design: in_progress
#   [ ] USER_REQUIREMENTS.md exists
#
# Fix these issues and try again.

# Fix and retry
/modify-requirement requirement "Architecture Design" --status complete
# Create USER_REQUIREMENTS.md
/approve-plan
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Requirements file not found | USER_REQUIREMENTS.md missing | Create the file |
| Requirement section incomplete | Section not marked complete | Use `/modify-requirement` |
| No modules defined | modules array empty | Use `/add-requirement module` |
| Module missing criteria | Module lacks acceptance_criteria | Use `/modify-requirement module` |
| gh CLI auth failed | Not logged in | Run `gh auth login` |
| State file not found | Planning not started | Run `/start-planning` first |

## Related Operations

- [op-check-planning-status.md](op-check-planning-status.md) - Verify prerequisites
- [op-modify-requirement-section.md](op-modify-requirement-section.md) - Mark sections complete
- [op-modify-module.md](op-modify-module.md) - Add missing criteria
