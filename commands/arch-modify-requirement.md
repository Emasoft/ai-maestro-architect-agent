---
name: ao-modify-requirement
description: "Modify an existing requirement or module specification during Plan Phase"
argument-hint: "<TYPE> <ID> [--name NAME] [--criteria TEXT] [--status STATUS] [--priority LEVEL]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/atlas_modify_requirement.py:*)"]
---

# Modify Requirement Command

Change the specifications of an existing requirement section or module during Plan Phase.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atlas_modify_requirement.py" modify $ARGUMENTS
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `TYPE` | Yes | Type to modify: `requirement` or `module` |
| `ID` | Yes | ID of the requirement section or module |
| `--name` | No | New display name |
| `--criteria` | No | New acceptance criteria (modules only) |
| `--status` | No | New status: `pending`, `in_progress`, `complete` |
| `--priority` | No | New priority: `critical`, `high`, `medium`, `low` |

## Modifying a Requirement Section

```
/modify-requirement requirement "Functional Requirements" --status complete
```

Marks the Functional Requirements section as complete.

## Modifying a Module

```
/modify-requirement module auth-core --criteria "Support JWT and session tokens" --priority critical
```

Updates the auth-core module with new acceptance criteria and priority.

## What Can Be Modified

| Field | Requirements | Modules |
|-------|--------------|---------|
| name | ✓ | ✓ |
| status | ✓ | ✓ |
| criteria | ✗ | ✓ |
| priority | ✗ | ✓ |

## Restrictions

- Cannot modify modules with status `in_progress` or `complete`
- Cannot change the locked goal (requires user approval)
- Status changes are validated (cannot skip states)

## Dynamic Flexibility

Modifications are reflected immediately in:
- The plan state file
- Exit criteria calculations
- Planning status display

## Examples

```bash
# Mark a requirement section as complete
/modify-requirement requirement "API Requirements" --status complete

# Add criteria to an existing module
/modify-requirement module oauth-google --criteria "Support Google Workspace SSO"

# Change module priority
/modify-requirement module remember-me --priority low

# Rename a module
/modify-requirement module auth-2fa --name "Two-Factor Authentication"
```

## Related Commands

- `/planning-status` - View current state
- `/add-requirement` - Add new requirement/module
- `/remove-requirement` - Remove pending requirement/module
