# State File Format Reference

## Table of Contents
- 4.1 Plan phase state file location and purpose
- 4.2 YAML frontmatter structure
- 4.3 Field definitions and allowed values
- 4.4 Requirements sections schema
- 4.5 Modules schema
- 4.6 Exit criteria schema
- 4.7 Reading and parsing the state file
- 4.8 State file lifecycle

---

## 4.1 Plan phase state file location and purpose

**File location:**
```
.claude/orchestrator-plan-phase.local.md
```

**Purpose:**
- Tracks the current state of Plan Phase
- Stores all requirements, modules, and progress
- Used by all planning commands to read/write state
- Enables stop hook to enforce plan completion

**Why `.local.md` suffix:**
- The `.local` indicates this file is gitignored (not version controlled)
- Contains session-specific state that should not be committed
- Each working session may have its own plan state

**File format:**
- Markdown file with YAML frontmatter
- Frontmatter contains structured data (parseable)
- Body contains human-readable summary and instructions

---

## 4.2 YAML frontmatter structure

The state file uses YAML frontmatter between `---` delimiters:

```yaml
---
phase: "planning"
plan_id: "plan-20260109-143022"
status: "drafting"
created_at: "2026-01-09T14:30:22+00:00"

# User Goal
goal: "Build a REST API for user management"
goal_locked: true

# Requirements
requirements_file: "USER_REQUIREMENTS.md"
requirements_complete: false
requirements_sections:
  - name: "Functional Requirements"
    status: "pending"

# Modules
modules: []

# Completion Tracking
plan_phase_complete: false
exit_criteria:
  - "USER_REQUIREMENTS.md complete"
  - "All modules defined with acceptance criteria"
  - "GitHub Issues created for all modules"
  - "User approved the plan"
---

# Plan Phase: plan-20260109-143022

[Body content here...]
```

---

## 4.3 Field definitions and allowed values

**Top-level fields:**

| Field | Type | Description | Allowed Values |
|-------|------|-------------|----------------|
| `phase` | String | Current workflow phase | "planning" |
| `plan_id` | String | Unique plan identifier | "plan-YYYYMMDD-HHMMSS" |
| `status` | String | Plan status | "drafting", "reviewing", "approved" |
| `created_at` | String | ISO 8601 timestamp | Any valid ISO date |
| `goal` | String | User's project goal | Any non-empty string |
| `goal_locked` | Boolean | Whether goal is locked | true, false |
| `requirements_file` | String | Path to requirements doc | File path (default: "USER_REQUIREMENTS.md") |
| `requirements_complete` | Boolean | All requirements done | true, false |
| `requirements_sections` | Array | List of requirement sections | See section 4.4 |
| `modules` | Array | List of modules | See section 4.5 |
| `plan_phase_complete` | Boolean | Plan approved | true, false |
| `exit_criteria` | Array | Criteria strings | See section 4.6 |

**Status transitions:**
```
drafting --> reviewing --> approved
```

---

## 4.4 Requirements sections schema

Each requirement section is an object in the `requirements_sections` array:

```yaml
requirements_sections:
  - name: "Functional Requirements"
    status: "pending"
  - name: "Non-Functional Requirements"
    status: "in_progress"
  - name: "Architecture Design"
    status: "complete"
```

**Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Display name of the section |
| `status` | String | Yes | Current completion status |

**Status values:**
- `pending` - Not started
- `in_progress` - Currently being documented
- `complete` - Section is fully documented

**Default sections (created by /start-planning):**
1. Functional Requirements
2. Non-Functional Requirements
3. Architecture Design

---

## 4.5 Modules schema

Each module is an object in the `modules` array:

```yaml
modules:
  - id: "auth-core"
    name: "Auth Core"
    status: "planned"
    priority: "high"
    acceptance_criteria: "Support JWT token authentication"
    github_issue: null
  - id: "user-mgmt"
    name: "User Management"
    status: "planned"
    priority: "medium"
    acceptance_criteria: "CRUD operations for users"
    github_issue: "#42"
```

**Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | String | Yes | Kebab-case identifier |
| `name` | String | Yes | Display name |
| `status` | String | Yes | Current status |
| `priority` | String | Yes | Priority level |
| `acceptance_criteria` | String | Recommended | Success criteria |
| `github_issue` | String/Null | No | Issue number (e.g., "#42") |

**Status values:**
- `planned` - Defined but not started
- `pending` - Waiting to be assigned
- `in_progress` - Currently being implemented
- `complete` - Implementation finished

**Priority values:**
- `critical` - Must have, blocking
- `high` - Important, should have
- `medium` - Normal priority (default)
- `low` - Nice to have, can defer

**ID generation rules:**
- Converted to lowercase
- Non-alphanumeric characters replaced with hyphens
- Leading/trailing hyphens removed
- Example: "OAuth2 Handler" becomes "oauth2-handler"

---

## 4.6 Exit criteria schema

Exit criteria is a simple array of strings describing conditions for plan approval:

```yaml
exit_criteria:
  - "USER_REQUIREMENTS.md complete"
  - "All modules defined with acceptance criteria"
  - "GitHub Issues created for all modules"
  - "User approved the plan"
```

**Default exit criteria (created by /start-planning):**
1. USER_REQUIREMENTS.md complete
2. All modules defined with acceptance criteria
3. GitHub Issues created for all modules
4. User approved the plan

These strings are displayed in `/planning-status` output and used by the stop hook to determine if exit should be blocked.

---

## 4.7 Reading and parsing the state file

**Python example to parse frontmatter:**

```python
from pathlib import Path
import yaml

PLAN_STATE_FILE = Path(".claude/orchestrator-plan-phase.local.md")

def parse_frontmatter(file_path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (data, body)."""
    if not file_path.exists():
        return {}, ""

    content = file_path.read_text(encoding="utf-8")

    # Check for frontmatter delimiters
    if not content.startswith("---"):
        return {}, content

    # Find the closing delimiter
    end_index = content.find("---", 3)
    if end_index == -1:
        return {}, content

    # Extract and parse YAML
    yaml_content = content[3:end_index].strip()
    body = content[end_index + 3:].strip()

    try:
        data = yaml.safe_load(yaml_content) or {}
        return data, body
    except yaml.YAMLError:
        return {}, content
```

**Accessing specific fields:**

```python
data, body = parse_frontmatter(PLAN_STATE_FILE)

# Get plan ID
plan_id = data.get("plan_id", "unknown")

# Get all modules
modules = data.get("modules", [])

# Check if plan is complete
is_complete = data.get("plan_phase_complete", False)

# Iterate requirements sections
for section in data.get("requirements_sections", []):
    print(f"{section['name']}: {section['status']}")
```

---

## 4.8 State file lifecycle

**Creation (by /start-planning):**
1. Check if file already exists (error if yes)
2. Generate unique plan_id from timestamp
3. Write initial YAML frontmatter with defaults
4. Write body with instructions

**Updates (by /add-requirement, /modify-requirement, /remove-requirement):**
1. Parse existing frontmatter
2. Modify the relevant section (requirements_sections or modules)
3. Write updated frontmatter back
4. Preserve body content

**Approval (by /approve-plan):**
1. Validate all exit criteria
2. Create GitHub Issues for modules
3. Update `github_issue` field for each module
4. Set `status` to "approved"
5. Set `plan_phase_complete` to true
6. Create orchestration state file

**File relationships after approval:**

```
.claude/
  orchestrator-plan-phase.local.md   <-- Original plan (marked complete)
  orchestrator-exec-phase.local.md   <-- New orchestration state (references plan)
```

**Cleanup:**
- Plan state file is NOT deleted after approval
- It serves as historical record of the planning decisions
- Can be referenced during orchestration for requirements lookup
