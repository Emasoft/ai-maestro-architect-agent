# Start Planning Procedure Reference

## Table of Contents
- 1.1 When to use /amaa-start-planning command
- 1.2 Prerequisites before starting planning
- 1.3 Command syntax and arguments
- 1.4 What the command creates
- 1.5 Post-initialization steps
- Functional Requirements
- 1.6 Example workflow after starting planning

## 1.1 When to use /amaa-start-planning command

Use the `/amaa-start-planning` command when you need to:

1. **Begin a new project** - Before any implementation, enter Plan Phase to define requirements
2. **Transition from discussion to planning** - When user goals are clear enough to document
3. **Create formal requirements** - When you need trackable, versioned requirements
4. **Enable exit blocking** - When you want the stop hook to enforce plan completion

Do NOT use `/amaa-start-planning` when:
- A Plan Phase is already active (check planning status first)
- You want to jump directly to implementation (use `/start-orchestration` instead)
- Requirements are already documented and approved elsewhere

---

## 1.2 Prerequisites before starting planning

Before running `/amaa-start-planning`, ensure:

1. **Clear user goal** - You must have a concise description of what to build
2. **No existing Plan Phase** - Check that `.claude/orchestrator-plan-phase.local.md` does not exist
3. **Working directory is project root** - The state file will be created in `.claude/`
4. **User agreement** - The user should understand that exit will be blocked until plan completion

If a Plan Phase already exists, you must either:
- Resume it by running `check_plan_prerequisites.py` to check planning status
- Delete the state file manually to start fresh (requires user approval)

---

## 1.3 Command syntax and arguments

**Basic syntax:**
```
/amaa-start-planning "Goal description here"
```

**Alternative syntax with flag:**
```
/amaa-start-planning --goal "Goal description here"
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `goal` | Yes | The project goal (positional or via --goal flag) |

**Goal requirements:**
- Must not be empty
- Surrounding quotes are automatically stripped
- Will be locked after creation (changes require user approval)

**Script location:**
```
${CLAUDE_PLUGIN_ROOT}/scripts/amaa_start_planning.py
```

---

## 1.4 What the command creates

The command creates a state file at `.claude/orchestrator-plan-phase.local.md` containing:

**YAML frontmatter fields:**

| Field | Initial Value | Description |
|-------|---------------|-------------|
| `phase` | "planning" | Current workflow phase |
| `plan_id` | "plan-YYYYMMDD-HHMMSS" | Unique identifier |
| `status` | "drafting" | Plan status: drafting/reviewing/approved |
| `created_at` | ISO timestamp | When plan was created |
| `goal` | User-provided | The locked goal description |
| `goal_locked` | true | Whether goal can be modified |
| `requirements_file` | "USER_REQUIREMENTS.md" | Path to requirements document |
| `requirements_complete` | false | Whether requirements are done |
| `requirements_sections` | Array | Sections to complete |
| `modules` | [] | Empty array for modules |
| `plan_phase_complete` | false | Overall completion status |
| `exit_criteria` | Array | Criteria for transition |

**Default requirements sections created:**
1. Functional Requirements - status: pending
2. Non-Functional Requirements - status: pending
3. Architecture Design - status: pending

---

## 1.5 Post-initialization steps

After `/amaa-start-planning` succeeds, perform these steps in order:

**Step 1: Verify initialization**
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py
```
Run check_plan_prerequisites.py to check planning status. Confirm the state file was created with correct goal.

**Step 2: Create USER_REQUIREMENTS.md**
Create the requirements document at project root:
```markdown
# User Requirements

## Functional Requirements
[Document functional requirements here]

## Non-Functional Requirements
[Document non-functional requirements here]

## Architecture Design
[Document architecture here]
```

**Step 3: Add modules**
For each implementation unit:
```
/amaa-add-requirement module "module-name" --criteria "Acceptance criteria" --priority high
```

**Step 4: Mark sections complete**
As you complete each section:
```
/amaa-modify-requirement requirement "Functional Requirements" --status complete
```

**Step 5: Review and approve**
Mark all requirements as complete to approve plan transition. When all criteria are met, set `plan_phase_complete: true` in the state file.

---

## 1.6 Example workflow after starting planning

Complete example from start to approval:

```bash
# Step 1: Start planning
/amaa-start-planning "Build a REST API for user management"

# Step 2: Check status
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py

# Step 3: Add modules
/amaa-add-requirement module "user-crud" --criteria "Create, read, update, delete users" --priority critical
/amaa-add-requirement module "auth-jwt" --criteria "JWT token generation and validation" --priority high
/amaa-add-requirement module "api-docs" --criteria "OpenAPI/Swagger documentation" --priority medium

# Step 4: Create USER_REQUIREMENTS.md manually (write the document)

# Step 5: Mark requirement sections as complete
/amaa-modify-requirement requirement "Functional Requirements" --status complete
/amaa-modify-requirement requirement "Non-Functional Requirements" --status complete
/amaa-modify-requirement requirement "Architecture Design" --status complete

# Step 6: Verify all criteria met
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py --fix-suggestions

# Step 7: Approve plan transition (set plan_phase_complete: true in state file)
```

**Expected output after /amaa-start-planning:**
```
Planning initialized
  Plan ID: plan-20260109-143022
  Goal: Build a REST API for user management
  State file: .claude/orchestrator-plan-phase.local.md

Next steps:
  1. Create USER_REQUIREMENTS.md with detailed requirements
  2. Use /amaa-add-requirement to define modules
  3. Run check_plan_prerequisites.py to check planning status
  4. Mark all requirements as complete to approve plan transition
```
