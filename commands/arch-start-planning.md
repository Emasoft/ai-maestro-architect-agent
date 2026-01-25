---
name: arch-start-planning
description: "Enter Plan Phase Mode - begin requirements gathering and planning before implementation"
argument-hint: "[GOAL_DESCRIPTION]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/arch_start_planning.py:*)"]
---

# Start Planning Command

Enter Plan Phase Mode to create comprehensive requirements and design specifications BEFORE any implementation begins.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/arch_start_planning.py" $ARGUMENTS
```

## What This Command Does

1. **Creates Plan Phase state file** at `.claude/orchestrator-plan-phase.local.md`
2. **Locks the user goal** (cannot be changed without user approval)
3. **Initializes requirements tracking** with sections for:
   - Functional Requirements
   - Non-Functional Requirements
   - Architecture Design
4. **Sets exit criteria** that must be met before transition to Orchestration Phase

## Plan Phase Activities

During Plan Phase, you will:
- Gather user goals and constraints
- Create USER_REQUIREMENTS.md
- Design system architecture
- Break down into modules/phases
- Define acceptance criteria per module
- Prepare GitHub Issues (created AFTER plan approval)
- Create Claude Tasks for orchestrator coordination duties

## State File Created

The command creates `.claude/orchestrator-plan-phase.local.md` with YAML frontmatter tracking:
- `phase: "planning"`
- `status: "drafting|reviewing|approved"`
- `goal` and `goal_locked` fields
- `requirements_sections` progress
- `modules` breakdown
- `exit_criteria` checklist

## Exit Blocking

The stop hook will block exit while in Plan Phase until:
- USER_REQUIREMENTS.md is complete
- All modules defined with acceptance criteria
- User approves the plan via `/approve-plan`

## Next Steps After Starting

1. Run `/planning-status` to see current progress
2. Use `/add-requirement` to add requirements and modules
3. Use `/modify-requirement` to refine specifications
4. Run `/approve-plan` when planning is complete

## Example

```
/start-planning "Build a user authentication system with OAuth2 support"
```

This will:
1. Create the plan phase state file
2. Lock the goal: "Build a user authentication system with OAuth2 support"
3. Initialize empty requirements sections
4. Enable the stop hook to enforce plan completion
