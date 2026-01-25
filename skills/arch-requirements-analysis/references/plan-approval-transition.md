# Plan Approval and Transition Reference

## Table of Contents
- 3.1 When to approve the plan
- 3.2 Prerequisites for plan approval
- 3.3 Approve plan syntax and options
- 3.4 Validation checks performed
- 3.5 GitHub Issue creation process
- 3.6 State file transitions
- 3.7 Post-approval next steps
- 3.8 Approval workflow example

---

## 3.1 When to approve the plan

Approve the plan when ALL of these conditions are met:

1. **USER_REQUIREMENTS.md is complete** - All requirements documented
2. **All requirement sections are complete** - Each section marked as "complete"
3. **All modules have acceptance criteria** - Every module has defined success criteria
4. **User has reviewed and agreed** - User confirms the plan is ready for implementation

Do NOT approve the plan when:
- Requirements are still being gathered
- Module acceptance criteria are not defined
- User has not reviewed the final plan
- You want to make more changes (use modify commands first)

---

## 3.2 Prerequisites for plan approval

**Checklist before running /approve-plan:**

| Prerequisite | How to Verify | How to Fix |
|--------------|---------------|------------|
| USER_REQUIREMENTS.md exists | `ls USER_REQUIREMENTS.md` | Create the file |
| All sections complete | `/planning-status` | `/modify-requirement requirement "Name" --status complete` |
| All modules have criteria | `/planning-status --verbose` | `/modify-requirement module id --criteria "..."` |
| At least one module defined | `/planning-status` | `/add-requirement module "name" --criteria "..."` |

**Quick verification:**
```bash
/planning-status --verbose
```

All exit criteria should show checkmarks before approval.

---

## 3.3 Approve plan syntax and options

**Basic syntax:**
```
/approve-plan
```

**Skip GitHub Issue creation:**
```
/approve-plan --skip-issues
```

**Options:**

| Option | Description | Use Case |
|--------|-------------|----------|
| `--skip-issues` | Skip GitHub Issue creation | Offline work, manual issue creation |

**Script command:**
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/arch_approve_plan.py" $ARGUMENTS
```

---

## 3.4 Validation checks performed

The /approve-plan command validates the plan before approval:

**Check 1: Requirements file exists**
- Looks for file specified in `requirements_file` field (default: USER_REQUIREMENTS.md)
- Fails if file does not exist

**Check 2: All requirement sections complete**
- Iterates through `requirements_sections` array
- Fails if any section has status other than "complete"

**Check 3: Modules defined**
- Checks that `modules` array is not empty
- Fails if no modules are defined

**Check 4: All modules have acceptance criteria**
- Iterates through all modules
- Fails if any module lacks `acceptance_criteria` field

**Validation error messages:**

| Error | Cause | Solution |
|-------|-------|----------|
| "Requirements file not found" | USER_REQUIREMENTS.md missing | Create the file |
| "Requirement section incomplete" | Section not marked complete | Use /modify-requirement |
| "No modules defined" | modules array empty | Use /add-requirement module |
| "Module missing acceptance criteria" | Module lacks criteria | Use /modify-requirement |

---

## 3.5 GitHub Issue creation process

For each module, the command creates a GitHub Issue:

**Issue title format:**
```
[Module] {module_name}
```

**Issue body format:**
```markdown
## Module: {module_name}

### Description
Implementation of the {module_name} module as part of plan {plan_id}.

### Acceptance Criteria
- [ ] {acceptance_criteria}

### Priority
{priority}

### Related
- Plan ID: {plan_id}
- Module ID: {module_id}
- Requirements: USER_REQUIREMENTS.md
```

**Labels applied:**
- `module` - Identifies as module issue
- `priority-{level}` - Priority indicator (e.g., priority-high)
- `status-todo` - Initial status

**GitHub CLI command used:**
```bash
gh issue create --title "[Module] {name}" --body "{body}" --label "module,priority-{priority},status-todo"
```

**Issue number storage:**
After creation, the issue number (e.g., "#42") is stored in the module's `github_issue` field.

---

## 3.6 State file transitions

**Before /approve-plan:**

Plan state file (`.claude/orchestrator-plan-phase.local.md`):
```yaml
phase: "planning"
status: "drafting"
plan_phase_complete: false
modules:
  - id: "auth-core"
    github_issue: null
```

**After /approve-plan:**

Plan state file (updated):
```yaml
phase: "planning"
status: "approved"
plan_phase_complete: true
modules:
  - id: "auth-core"
    github_issue: "#42"  # Added
```

Orchestration state file (`.claude/orchestrator-exec-phase.local.md`) created:
```yaml
phase: "orchestration"
plan_id: "plan-20260109-143022"
status: "ready"
started_at: "2026-01-09T14:30:22+00:00"
plan_file: ".claude/orchestrator-plan-phase.local.md"
requirements_file: "USER_REQUIREMENTS.md"
current_module: null
modules_status:
  - id: "auth-core"
    name: "Auth Core"
    status: "pending"
    assigned_to: null
    github_issue: "#42"
    pr: null
    verification_loops: 0
registered_agents:
  ai_agents: []
  human_developers: []
active_assignments: []
modules_completed: 0
modules_total: 1
all_modules_complete: false
```

---

## 3.7 Post-approval next steps

After plan approval, proceed with these steps:

**Step 1: Verify transition**
```bash
# Check that orchestration state file exists
ls .claude/orchestrator-exec-phase.local.md

# View orchestration status (should show "ready")
/orchestration-status
```

**Step 2: Start orchestration**
```bash
/start-orchestration
```

**Step 3: Register agents**
```bash
# Register AI agents
/register-agent ai "agent-session-name" --capabilities "python,testing"

# Register human developers (optional)
/register-agent human "developer@email.com" --name "John Doe"
```

**Step 4: Assign modules**
```bash
# Assign first module to an agent
/assign-module auth-core agent-session-name
```

**Step 5: Monitor progress**
```bash
# Check overall status
/orchestration-status

# Poll agents for updates
/check-agents
```

---

## 3.8 Approval workflow example

**Complete workflow from verification to transition:**

```bash
# Step 1: Verify plan is ready
/planning-status --verbose

# Expected output shows all checkmarks:
# [x] USER_REQUIREMENTS.md complete
# [x] All modules defined with acceptance criteria
# [ ] GitHub Issues created for all modules
# [ ] User approved the plan

# Step 2: Approve the plan
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

**Offline workflow (skip GitHub Issues):**

```bash
# Approve without creating issues
/approve-plan --skip-issues

# Issues can be created manually later via gh CLI
gh issue create --title "[Module] Auth Core" --body "..." --label "module"
```
