---
operation: start-planning
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Start Planning Operation

## When to Use

Use this operation when:
- Beginning a new project before any implementation
- Transitioning from discussion to formal planning
- Creating trackable, versioned requirements
- Enabling exit blocking to enforce plan completion

Do NOT use when:
- A Plan Phase is already active (check with `/planning-status`)
- Jumping directly to implementation (use `/start-orchestration` instead)
- Requirements are already documented and approved elsewhere

## Prerequisites

- [ ] Clear user goal description available
- [ ] No existing Plan Phase (`.claude/orchestrator-plan-phase.local.md` does not exist)
- [ ] Working directory is project root
- [ ] User understands exit will be blocked until plan completion

## Procedure

### Step 1: Verify No Existing Plan Phase

```bash
ls -la .claude/orchestrator-plan-phase.local.md
```

If file exists, either resume with `/planning-status` or delete to start fresh (requires user approval).

### Step 2: Execute Start Planning Command

```bash
/start-planning "Goal description here"
```

Alternative syntax:
```bash
/start-planning --goal "Goal description here"
```

### Step 3: Verify Initialization

```bash
/planning-status
```

Confirm state file was created with correct goal.

### Step 4: Review Created State

The command creates `.claude/orchestrator-plan-phase.local.md` containing:
- `phase`: "planning"
- `plan_id`: "plan-YYYYMMDD-HHMMSS"
- `status`: "drafting"
- `goal`: User-provided goal (locked)
- Default requirement sections: Functional, Non-Functional, Architecture Design

## Checklist

Copy this checklist and track your progress:

- [ ] Verify no existing plan phase active
- [ ] Obtain clear goal description from user
- [ ] Execute `/start-planning "goal"`
- [ ] Verify state file created at `.claude/orchestrator-plan-phase.local.md`
- [ ] Confirm goal is correctly recorded
- [ ] Proceed to create USER_REQUIREMENTS.md

## Examples

### Example: Starting a REST API Project

```bash
# Check for existing plan
ls -la .claude/orchestrator-plan-phase.local.md
# ls: .claude/orchestrator-plan-phase.local.md: No such file or directory

# Start planning
/start-planning "Build a REST API for user management"

# Expected output:
# Planning initialized
#   Plan ID: plan-20260109-143022
#   Goal: Build a REST API for user management
#   State file: .claude/orchestrator-plan-phase.local.md
#
# Next steps:
#   1. Create USER_REQUIREMENTS.md with detailed requirements
#   2. Use /add-requirement to define modules
#   3. Use /planning-status to track progress
#   4. Use /approve-plan when ready to implement

# Verify
/planning-status
```

### Example: Goal with Special Characters

```bash
/start-planning "Build OAuth2/OIDC authentication with JWT tokens"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| State file already exists | Plan Phase active | Use `/planning-status` to resume or delete file with user approval |
| Goal is empty | No goal provided | Provide goal as positional argument or with --goal flag |
| Permission denied | Cannot write to .claude/ | Ensure write access to project directory |
| Script not found | Plugin not loaded | Verify plugin is enabled with `/plugins` |

## Related Operations

- [op-check-planning-status.md](op-check-planning-status.md) - Check progress after starting
- [op-add-requirement-section.md](op-add-requirement-section.md) - Add custom requirement sections
- [op-add-module.md](op-add-module.md) - Add implementation modules
