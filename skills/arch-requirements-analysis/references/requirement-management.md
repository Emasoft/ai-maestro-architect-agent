# Requirement Management Reference

## Table of Contents
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

## 2.1 When to add a new requirement section

Add a new requirement section when:

1. **Custom categorization needed** - Default sections (Functional, Non-Functional, Architecture) are not enough
2. **Compliance requirements** - Need to track security, legal, or regulatory requirements separately
3. **Domain-specific grouping** - Project needs specialized requirement categories

Use `/add-requirement requirement "Section Name"` to add a section.

**Default sections already created by /start-planning:**
- Functional Requirements
- Non-Functional Requirements
- Architecture Design

---

## 2.2 When to add a new module

Add a new module when:

1. **Defining implementation units** - Each deployable/testable unit should be a module
2. **Breaking down the project** - Large features should be split into manageable modules
3. **Creating trackable work items** - Each module becomes a GitHub Issue after approval

**Module properties:**
| Property | Required | Description |
|----------|----------|-------------|
| `id` | Auto-generated | Kebab-case from name |
| `name` | Yes | Display name |
| `status` | Auto: "planned" | Current status |
| `acceptance_criteria` | Recommended | Success criteria |
| `priority` | Default: "medium" | critical/high/medium/low |
| `github_issue` | Auto: null | Issue number after approval |

---

## 2.3 Add requirement syntax and arguments

**Adding a requirement section:**
```
/add-requirement requirement "Section Name"
```

**Adding a module:**
```
/add-requirement module "module-name" --criteria "Acceptance criteria text" --priority high
```

**Full argument reference:**

| Argument | Values | Description |
|----------|--------|-------------|
| `TYPE` | `requirement` or `module` | What to add |
| `NAME` | String | Name of section or module |
| `--criteria` | String | Acceptance criteria (modules only) |
| `--priority` | critical/high/medium/low | Priority level (default: medium) |

**Script command:**
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atlas_modify_requirement.py" add $ARGUMENTS
```

**ID normalization:**
Module names are converted to kebab-case IDs:
- "User Authentication" becomes "user-authentication"
- "OAuth2_Handler" becomes "oauth2-handler"

---

## 2.4 When to modify existing requirements

Modify requirements when:

1. **Changing status** - Mark a section as in_progress or complete
2. **Updating acceptance criteria** - Refining success criteria for modules
3. **Changing priority** - Adjusting module importance
4. **Renaming** - Correcting names without deleting

**Restrictions:**
- Cannot modify modules with status `in_progress` or `complete`
- Cannot change the locked goal without user approval
- Status changes must be logical (cannot skip states)

---

## 2.5 Modify requirement syntax and arguments

**Modifying a requirement section:**
```
/modify-requirement requirement "Section Name" --status complete
```

**Modifying a module:**
```
/modify-requirement module module-id --criteria "New criteria" --priority critical
```

**Full argument reference:**

| Argument | Values | Description |
|----------|--------|-------------|
| `TYPE` | `requirement` or `module` | What to modify |
| `ID` | String | ID of section/module |
| `--name` | String | New display name |
| `--status` | pending/in_progress/complete/planned | New status |
| `--criteria` | String | New acceptance criteria (modules only) |
| `--priority` | critical/high/medium/low | New priority (modules only) |

**Field availability by type:**

| Field | Requirements | Modules |
|-------|--------------|---------|
| --name | Yes | Yes |
| --status | Yes | Yes |
| --criteria | No | Yes |
| --priority | No | Yes |

---

## 2.6 When to remove requirements

Remove requirements when:

1. **Scope reduction** - User decides feature is not needed
2. **Consolidation** - Merging two modules into one
3. **Error correction** - Module was added by mistake

**Important:** Removal is only allowed for items with `pending` or `planned` status.

---

## 2.7 Remove requirement syntax and restrictions

**Removing a requirement section:**
```
/remove-requirement requirement "Section Name"
```

**Removing a module:**
```
/remove-requirement module module-id
```

**Force removal (bypass checks):**
```
/remove-requirement module module-id --force
```

**Restrictions:**

| Status | Can Remove | Requires --force |
|--------|------------|------------------|
| pending | Yes | No |
| planned | Yes | No |
| in_progress | No | Yes |
| complete | No | Yes |
| Has GitHub Issue | No | Yes |

**Why these restrictions exist:**
- Once work starts, removing modules causes data loss
- GitHub Issues should be closed manually to maintain history
- Completed work should not be discarded without explicit intent

---

## 2.8 State file changes after operations

**After adding a requirement section:**
```yaml
requirements_sections:
  - name: "Functional Requirements"
    status: "pending"
  - name: "Security Requirements"  # NEW
    status: "pending"
```

**After adding a module:**
```yaml
modules:
  - id: "auth-core"
    name: "Auth Core"
    status: "planned"
    priority: "high"
    acceptance_criteria: "Support JWT tokens"
    github_issue: null
```

**After modifying status:**
```yaml
requirements_sections:
  - name: "Functional Requirements"
    status: "complete"  # CHANGED from "pending"
```

**After removing a module:**
```yaml
modules:
  # Module "legacy-api" REMOVED from list
  - id: "auth-core"
    status: "planned"
```

---

## 2.9 Common operation examples

**Example 1: Building a complete requirement set**
```bash
# Add custom requirement section
/add-requirement requirement "Security Requirements"

# Add multiple modules
/add-requirement module "user-login" --criteria "Email/password authentication" --priority critical
/add-requirement module "session-mgmt" --criteria "Token refresh and expiry" --priority high
/add-requirement module "audit-log" --criteria "Log all auth events" --priority medium

# Update module criteria after discussion
/modify-requirement module user-login --criteria "Email/password auth with rate limiting"

# Change priority based on user feedback
/modify-requirement module audit-log --priority low

# Mark requirement section complete
/modify-requirement requirement "Security Requirements" --status complete
```

**Example 2: Removing a module**
```bash
# Check current modules
/planning-status

# Remove module that's no longer needed
/remove-requirement module oauth-facebook

# Verify removal
/planning-status
```

**Example 3: Renaming a module**
```bash
# Change display name without affecting ID
/modify-requirement module auth-2fa --name "Two-Factor Authentication Module"
```

**Error handling examples:**

```bash
# Attempting to remove in-progress module
/remove-requirement module auth-core
# ERROR: Cannot remove: status is in_progress

# Force removal (use with caution)
/remove-requirement module auth-core --force
# Module removed (work may be lost)

# Adding duplicate module
/add-requirement module auth-core --criteria "Test"
# ERROR: Module 'auth-core' already exists
```
