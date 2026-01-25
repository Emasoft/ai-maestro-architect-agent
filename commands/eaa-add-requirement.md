---
name: eaa-add-requirement
description: "Add a new requirement or module to the plan during Plan Phase"
argument-hint: "<TYPE> <NAME> [--criteria TEXT] [--priority LEVEL]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/eaa_modify_requirement.py:*)"]
---

# Add Requirement Command

Add a new requirement section or module to the current plan during Plan Phase.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/eaa_modify_requirement.py" add $ARGUMENTS
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `TYPE` | Yes | Type to add: `requirement` or `module` |
| `NAME` | Yes | Name of the requirement section or module |
| `--criteria` | No | Acceptance criteria (for modules) |
| `--priority` | No | Priority level: `critical`, `high`, `medium`, `low` |

## Adding a Requirement Section

```
/add-requirement requirement "Security Requirements"
```

This adds a new requirement section to track in USER_REQUIREMENTS.md.

## Adding a Module

```
/add-requirement module "password-reset" --criteria "Users can reset password via email link" --priority high
```

This adds a new module to the plan with:
- Module ID: `password-reset`
- Name derived from ID
- Acceptance criteria specified
- Priority: high

## Dynamic Flexibility

You can add requirements or modules at ANY time during Plan Phase:
- New requirements are immediately tracked
- New modules become part of the completion criteria
- Stop hook will block exit until ALL current items complete

## State File Update

The command updates `.claude/orchestrator-plan-phase.local.md`:

**For requirements:**
```yaml
requirements_sections:
  - name: "Security Requirements"
    status: "pending"
```

**For modules:**
```yaml
modules:
  - id: "password-reset"
    name: "Password Reset"
    status: "planned"
    acceptance_criteria: "Users can reset password via email link"
    priority: "high"
    github_issue: null
```

## Examples

```bash
# Add functional requirement section
/add-requirement requirement "API Requirements"

# Add a critical module
/add-requirement module "auth-2fa" --criteria "Support TOTP-based 2FA" --priority critical

# Add a low-priority enhancement module
/add-requirement module "remember-me" --criteria "Remember login for 30 days" --priority low
```

## Related Commands

- `/planning-status` - View all requirements and modules
- `/modify-requirement` - Change existing requirement/module
- `/remove-requirement` - Remove pending requirement/module
