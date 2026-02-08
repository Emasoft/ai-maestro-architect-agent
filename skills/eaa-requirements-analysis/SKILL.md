---
name: eaa-requirements-analysis
description: "Use when managing planning phase: start planning, track progress, manage requirements/modules, or approve plans. Trigger with /start-planning or /planning-status commands."
version: 1.0.0
license: Apache-2.0
compatibility: "Requires Python 3.8+, PyYAML, GitHub CLI for issue creation. Cross-platform compatible. Requires AI Maestro installed."
metadata:
  author: Emasoft
user-invocable: false
context: fork
workflow-instruction: "Step 6"
procedure: "proc-route-requirements"
---

# Planning Commands Skill

## Overview

This skill documents all planning phase commands for the Architect Agent plugin. The planning phase is the first stage of the Two-Phase workflow where requirements are gathered, modules are defined, and the implementation plan is created before any code is written.

## Prerequisites

- Python 3.8+ with PyYAML installed
- GitHub CLI for issue creation
- Write access to `.claude/` directory for state files
- Understanding of Two-Phase workflow

## Instructions

Use this skill when you need to:
- Start a new project with formal requirements gathering
- Track planning progress and requirements completion
- Add, modify, or remove requirements and modules during planning
- Approve a plan and transition to the orchestration phase

**Typical workflow:**
1. Start planning with `/start-planning "goal"`
2. Add requirements and modules with `/add-requirement`
3. Track progress with `/planning-status`
4. Modify as needed with `/modify-requirement`
5. Approve plan with `/approve-plan`

### Checklist

Copy this checklist and track your progress:

- [ ] Start planning: `/start-planning "goal description"`
- [ ] Verify state file created at `.claude/orchestrator-plan-phase.local.md`
- [ ] Add requirement sections as needed: `/add-requirement requirement "Name"`
- [ ] Add modules with criteria: `/add-requirement module "name" --criteria "..." --priority high`
- [ ] Create USER_REQUIREMENTS.md manually
- [ ] Track progress: `/planning-status`
- [ ] Mark requirement sections complete: `/modify-requirement requirement "Name" --status complete`
- [ ] Verify all prerequisites met:
  - [ ] USER_REQUIREMENTS.md exists
  - [ ] All requirement sections marked complete
  - [ ] All modules have acceptance criteria
  - [ ] At least one module defined
- [ ] Verify plan: `/planning-status --verbose`
- [ ] Approve plan: `/approve-plan`
- [ ] Verify GitHub Issues created for each module
- [ ] Begin orchestration: `/start-orchestration`

## Commands Overview

| Command | Purpose | Section |
|---------|---------|---------|
| `/start-planning` | Enter Plan Phase Mode | 1.0 |
| `/planning-status` | View requirements progress | 2.0 |
| `/add-requirement` | Add requirement or module | 3.0 |
| `/modify-requirement` | Change requirement specs | 4.0 |
| `/remove-requirement` | Remove pending requirement | 5.0 |
| `/approve-plan` | Transition to Orchestration | 6.0 |

---

## 1.0 When Starting a New Project

Use `/start-planning` to enter Plan Phase Mode and begin requirements gathering.

**Command:**
```
/start-planning "Goal description here"
```

**What happens:**
1. Creates state file at `.claude/orchestrator-plan-phase.local.md`
2. Locks the user goal (cannot change without approval)
3. Initializes default requirement sections
4. Enables stop hook to enforce plan completion

**For complete procedure details, see [start-planning-procedure.md](references/start-planning-procedure.md):**
- 1.1 When to use /start-planning command
- 1.2 Prerequisites before starting planning
- 1.3 Command syntax and arguments
- 1.4 What the command creates
- 1.5 Post-initialization steps
- 1.6 Example workflow after starting planning

---

## 2.0 When Checking Planning Progress

Use `/planning-status` to view the current state of Plan Phase.

**Command:**
```
/planning-status
/planning-status --verbose
```

**Output shows:**
- Phase status (drafting/reviewing/approved)
- Locked goal
- Requirements section progress
- Modules defined with status
- Exit criteria checklist

**Example output:**
```
+------------------------------------------------------------------+
|                    PLAN PHASE STATUS                              |
+------------------------------------------------------------------+
| Plan ID: plan-20260109-143022                                     |
| Status: drafting                                                  |
| Goal: Build user authentication with OAuth2                       |
+------------------------------------------------------------------+
| REQUIREMENTS PROGRESS                                             |
+------------------------------------------------------------------+
| [x] Functional Requirements     - complete                        |
| [>] Non-Functional Requirements - in-progress                     |
| [ ] Architecture Design         - pending                         |
+------------------------------------------------------------------+
```

---

## 3.0 When Adding Requirements or Modules

Use `/add-requirement` to add new requirement sections or modules to the plan.

**Adding a requirement section:**
```
/add-requirement requirement "Security Requirements"
```

**Adding a module:**
```
/add-requirement module "auth-core" --criteria "Support JWT tokens" --priority high
```

**For complete details, see [requirement-management.md](references/requirement-management.md):**
- 2.1 When to add a new requirement section
- 2.2 When to add a new module
- 2.3 Add requirement syntax and arguments
- 2.4 When to modify existing requirements
- 2.5 Modify requirement syntax and arguments
- 2.6 When to remove requirements
- 2.7 Remove requirement syntax and restrictions
- 2.8 State file changes after operations
- 2.9 Common operation examples

---

## 4.0 When Modifying Existing Requirements

Use `/modify-requirement` to change existing requirement sections or modules.

**Modifying a requirement section:**
```
/modify-requirement requirement "Functional Requirements" --status complete
```

**Modifying a module:**
```
/modify-requirement module auth-core --criteria "Support JWT and OAuth2" --priority critical
```

**Modifiable fields:**

| Field | Requirements | Modules |
|-------|--------------|---------|
| --name | Yes | Yes |
| --status | Yes | Yes |
| --criteria | No | Yes |
| --priority | No | Yes |

**Restrictions:**
- Cannot modify modules with status `in-progress` or `complete`
- Cannot change the locked goal without user approval

See [requirement-management.md](references/requirement-management.md) section 2.4-2.5 for details.

---

## 5.0 When Removing Requirements

Use `/remove-requirement` to remove pending requirements or modules.

**Removing a requirement section:**
```
/remove-requirement requirement "Legacy Support"
```

**Removing a module:**
```
/remove-requirement module legacy-api
```

**Force removal (bypass checks):**
```
/remove-requirement module in-progress-module --force
```

**Removal restrictions:**
- Can only remove items with `pending` or `planned` status
- Cannot remove items with GitHub Issues without `--force`
- Force removal may cause data loss

See [requirement-management.md](references/requirement-management.md) section 2.6-2.7 for details.

---

## 6.0 When Approving the Plan

Use `/approve-plan` to validate the plan and transition to Orchestration Phase.

**Command:**
```
/approve-plan
/approve-plan --skip-issues
```

**Prerequisites (all must be met):**
- [ ] USER_REQUIREMENTS.md exists
- [ ] All requirement sections marked complete
- [ ] All modules have acceptance criteria
- [ ] At least one module defined

**What happens on approval:**
1. Validates all exit criteria
2. Creates GitHub Issues for each module
3. Updates plan state to "approved"
4. Creates orchestration state file
5. Displays transition summary

**For complete details, see [plan-approval-transition.md](references/plan-approval-transition.md):**
- 3.1 When to approve the plan
- 3.2 Prerequisites for plan approval
- 3.3 Approve plan syntax and options
- 3.4 Validation checks performed
- 3.5 GitHub Issue creation process
- 3.6 State file transitions
- 3.7 Post-approval next steps
- 3.8 Approval workflow example

---

## 7.0 State File Reference

The plan phase uses a state file at `.claude/orchestrator-plan-phase.local.md` to track all planning progress.

**For state file details, see [state-file-format.md](references/state-file-format.md):**
- 4.1 Plan phase state file location and purpose
- 4.2 YAML frontmatter structure
- 4.3 Field definitions and allowed values
- 4.4 Requirements sections schema
- 4.5 Modules schema
- 4.6 Exit criteria schema
- 4.7 Reading and parsing the state file
- 4.8 State file lifecycle

---

## 8.0 Error Handling

**For troubleshooting issues, see [troubleshooting.md](references/troubleshooting.md):**
- 5.1 When /start-planning fails
- 5.2 When /planning-status shows errors
- 5.3 When /add-requirement fails
- 5.4 When /modify-requirement fails
- 5.5 When /remove-requirement fails
- 5.6 When /approve-plan fails
- 5.7 State file corruption recovery
- 5.8 GitHub Issue creation problems
- 5.9 Exit blocking issues

| Error | Cause | Solution |
|-------|-------|----------|
| State file not found | Planning not started | Run `/start-planning` first |
| Invalid status transition | Wrong status order | Follow: pending → in-progress → complete |
| Module has GitHub Issue | Cannot remove linked module | Use `--force` flag or close issue first |
| Approval prerequisites failed | Incomplete requirements | Mark all sections complete first |
| gh CLI auth failed | Not logged in | Run `gh auth login` |

---

## 9.0 Utility Scripts

This skill includes utility scripts for common operations.

### 9.1 Check Plan Prerequisites

Verify all prerequisites are met before approval:
```bash
python3 scripts/check_plan_prerequisites.py
python3 scripts/check_plan_prerequisites.py --fix-suggestions
```

### 9.2 Export Plan Summary

Export the plan as a formatted markdown summary:
```bash
python3 scripts/export_plan_summary.py
python3 scripts/export_plan_summary.py --output plan-summary.md
```

### 9.3 Reset Plan Phase

Safely reset the plan phase (creates backup):
```bash
python3 scripts/reset_plan_phase.py --confirm
python3 scripts/reset_plan_phase.py --confirm --no-backup
```

---

## 10.0 Quick Reference

### Complete Planning Workflow

```bash
# Step 1: Start planning
/start-planning "Build a REST API for user management"

# Step 2: Add modules
/add-requirement module "user-crud" --criteria "CRUD operations" --priority critical
/add-requirement module "auth-jwt" --criteria "JWT authentication" --priority high

# Step 3: Create USER_REQUIREMENTS.md manually

# Step 4: Mark sections complete
/modify-requirement requirement "Functional Requirements" --status complete
/modify-requirement requirement "Non-Functional Requirements" --status complete
/modify-requirement requirement "Architecture Design" --status complete

# Step 5: Verify and approve
/planning-status --verbose
/approve-plan

# Step 6: Begin orchestration
/start-orchestration
```

### Command Quick Reference

| Action | Command |
|--------|---------|
| Start planning | `/start-planning "goal"` |
| Check status | `/planning-status` |
| Add requirement section | `/add-requirement requirement "Name"` |
| Add module | `/add-requirement module "name" --criteria "..." --priority high` |
| Mark section complete | `/modify-requirement requirement "Name" --status complete` |
| Update module criteria | `/modify-requirement module id --criteria "..."` |
| Remove module | `/remove-requirement module id` |
| Approve plan | `/approve-plan` |

### Status Values

| Type | Allowed Status Values |
|------|----------------------|
| Requirement sections | pending, in-progress, complete |
| Modules | planned, pending, in-progress, complete |
| Plan | drafting, reviewing, approved |

### Priority Values

| Priority | Description |
|----------|-------------|
| critical | Must have, blocking |
| high | Important, should have |
| medium | Normal priority (default) |
| low | Nice to have, can defer |

---

## 11.0 Examples

### Example 1: Complete Planning Workflow

```bash
# Step 1: Start planning
/start-planning "Build a REST API for user management"

# Step 2: Add modules
/add-requirement module "user-crud" --criteria "CRUD operations" --priority critical
/add-requirement module "auth-jwt" --criteria "JWT authentication" --priority high

# Step 3: Create USER_REQUIREMENTS.md manually

# Step 4: Mark sections complete
/modify-requirement requirement "Functional Requirements" --status complete
/modify-requirement requirement "Non-Functional Requirements" --status complete
/modify-requirement requirement "Architecture Design" --status complete

# Step 5: Verify and approve
/planning-status --verbose
/approve-plan

# Step 6: Begin orchestration
/start-orchestration
```

### Example 2: Modify Existing Module

```bash
# Check current status
/planning-status

# Update module criteria
/modify-requirement module auth-core --criteria "Support JWT and OAuth2" --priority critical

# Verify change
/planning-status --verbose
```

## Requirement Analysis Scripts

The following scripts automate RULE 14 (User Requirements Are Immutable) enforcement:

### eaa_requirement_analysis.py

Manages requirement tracking documents and validates implementations against requirements.

| Command | Purpose | Usage |
|---------|---------|-------|
| `init` | Initialize requirements tracking structure | `python scripts/eaa_requirement_analysis.py init --project-root <PATH> --project-name "<NAME>"` |
| `parse` | Parse requirements from user text | `python scripts/eaa_requirement_analysis.py parse --input "<TEXT_OR_FILE>"` |
| `report` | Generate requirement issue report | `python scripts/eaa_requirement_analysis.py report --project-root <PATH> --requirement-id REQ-001 --requirement-text "<TEXT>" --issue-type Feasibility --description "<ISSUE>"` |
| `validate` | Validate implementation against requirements | `python scripts/eaa_requirement_analysis.py validate --project-root <PATH> --implementation <IMPL_PATH>` |

### When to Use

- **init**: At project start to create `docs_dev/requirements/` folder structure
- **parse**: When receiving user requirements to extract and categorize them
- **report**: When identifying potential issues with requirements before implementation
- **validate**: After implementation to verify compliance with user requirements

### RULE 14 Enforcement

This script enforces RULE 14: User Requirements Are Immutable. When issues arise:
1. Generate a Requirement Issue Report
2. Present alternatives to the user
3. Wait for explicit user decision
4. Only modify requirements after user approval

### Script Location

The script is located at `../../scripts/eaa_requirement_analysis.py` relative to this skill.

## 12.0 Resources

- [start-planning-procedure.md](references/start-planning-procedure.md) - Start planning command details
- [requirement-management.md](references/requirement-management.md) - Add/modify/remove requirements
- [plan-approval-transition.md](references/plan-approval-transition.md) - Approval and transition details
- [state-file-format.md](references/state-file-format.md) - State file schema and lifecycle
- [troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
- `scripts/check_plan_prerequisites.py` - Verify prerequisites
- `scripts/export_plan_summary.py` - Export plan summary
- `scripts/reset_plan_phase.py` - Reset plan phase

**Related Skills:**
- orchestration-commands - Implementation phase
- agent-management - Registering and assigning agents
- module-lifecycle - Tracking module progress

---

## Output

Each planning command produces specific output. See detailed command documentation in sections 1.0-6.0.

| Command | Output Type | Details |
|---------|-------------|---------|
| `/start-planning` | State file creation + confirmation message | See section 1.0 |
| `/planning-status` | Formatted status table with progress | See section 2.0 |
| `/add-requirement` | Confirmation message + updated state | See section 3.0 |
| `/modify-requirement` | Confirmation message + updated state | See section 4.0 |
| `/remove-requirement` | Confirmation message + updated state | See section 5.0 |
| `/approve-plan` | Validation results + GitHub Issues created | See section 6.0 |
