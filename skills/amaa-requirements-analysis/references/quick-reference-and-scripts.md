# Quick Reference and Utility Scripts

## Table of Contents

- [Command Quick Reference](#command-quick-reference)
- [Status Values](#status-values)
- [Priority Values](#priority-values)
- [Modifiable Fields](#modifiable-fields)
- [Utility Scripts](#utility-scripts)
  - [Check Plan Prerequisites](#check-plan-prerequisites)
  - [Export Plan Summary](#export-plan-summary)
  - [Reset Plan Phase](#reset-plan-phase)
- [Complete Planning Workflow Example](#complete-planning-workflow-example)
- [Requirement Analysis Scripts](#requirement-analysis-scripts)
  - [amaa_requirement_analysis.py](#amaa_requirement_analysispy)
  - [When to Use](#when-to-use)
  - [RULE 14 Enforcement](#rule-14-enforcement)

## Command Quick Reference

| Action | Command |
|--------|---------|
| Start planning | `/amaa-start-planning "goal"` |
| Check status | `python3 scripts/check_plan_prerequisites.py` |
| Add requirement section | `/amaa-add-requirement requirement "Name"` |
| Add module | `/amaa-add-requirement module "name" --criteria "..." --priority high` |
| Mark section complete | `/amaa-modify-requirement requirement "Name" --status complete` |
| Update module criteria | `/amaa-modify-requirement module id --criteria "..."` |
| Remove module | `/amaa-remove-requirement module id` |
| Approve plan | Mark all requirements complete, then set `plan_phase_complete: true` in state file |

## Status Values

| Type | Allowed Status Values |
|------|----------------------|
| Requirement sections | pending, in-progress, complete |
| Modules | planned, pending, in-progress, complete |
| Plan | drafting, reviewing, approved |

## Priority Values

| Priority | Description |
|----------|-------------|
| critical | Must have, blocking |
| high | Important, should have |
| medium | Normal priority (default) |
| low | Nice to have, can defer |

## Modifiable Fields

| Field | Requirements | Modules |
|-------|--------------|---------|
| --name | Yes | Yes |
| --status | Yes | Yes |
| --criteria | No | Yes |
| --priority | No | Yes |

## Utility Scripts

### Check Plan Prerequisites

Verify all prerequisites are met before approval:
```bash
python3 scripts/check_plan_prerequisites.py
python3 scripts/check_plan_prerequisites.py --fix-suggestions
```

### Export Plan Summary

Export the plan as a formatted markdown summary:
```bash
python3 scripts/export_plan_summary.py
python3 scripts/export_plan_summary.py --output plan-summary.md
```

### Reset Plan Phase

Safely reset the plan phase (creates backup):
```bash
python3 scripts/reset_plan_phase.py --confirm
python3 scripts/reset_plan_phase.py --confirm --no-backup
```

## Complete Planning Workflow Example

```bash
# Step 1: Start planning
/amaa-start-planning "Build a REST API for user management"

# Step 2: Add modules
/amaa-add-requirement module "user-crud" --criteria "CRUD operations" --priority critical
/amaa-add-requirement module "auth-jwt" --criteria "JWT authentication" --priority high

# Step 3: Create USER_REQUIREMENTS.md manually

# Step 4: Mark sections complete
/amaa-modify-requirement requirement "Functional Requirements" --status complete
/amaa-modify-requirement requirement "Non-Functional Requirements" --status complete
/amaa-modify-requirement requirement "Architecture Design" --status complete

# Step 5: Verify and approve
python3 scripts/check_plan_prerequisites.py --fix-suggestions
# Then approve plan transition: set plan_phase_complete: true in state file

# Step 6: Begin orchestration
/start-orchestration
```

## Requirement Analysis Scripts

The following scripts automate RULE 14 (User Requirements Are Immutable) enforcement.

### amaa_requirement_analysis.py

Located at `../../scripts/amaa_requirement_analysis.py` relative to the skill.

| Command | Purpose | Usage |
|---------|---------|-------|
| `init` | Initialize requirements tracking structure | `python scripts/amaa_requirement_analysis.py init --project-root <PATH> --project-name "<NAME>"` |
| `parse` | Parse requirements from user text | `python scripts/amaa_requirement_analysis.py parse --input "<TEXT_OR_FILE>"` |
| `report` | Generate requirement issue report | `python scripts/amaa_requirement_analysis.py report --project-root <PATH> --requirement-id REQ-001 --requirement-text "<TEXT>" --issue-type Feasibility --description "<ISSUE>"` |
| `validate` | Validate implementation against requirements | `python scripts/amaa_requirement_analysis.py validate --project-root <PATH> --implementation <IMPL_PATH>` |

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
