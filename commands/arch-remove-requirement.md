---
name: ao-remove-requirement
description: "Remove a pending requirement or module from the plan (only if not started)"
argument-hint: "<TYPE> <ID> [--force]"
allowed-tools: ["Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/atlas_modify_requirement.py:*)"]
---

# Remove Requirement Command

Remove a requirement section or module from the current plan. Only items with `pending` or `planned` status can be removed.

## Usage

```!
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/atlas_modify_requirement.py" remove $ARGUMENTS
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `TYPE` | Yes | Type to remove: `requirement` or `module` |
| `ID` | Yes | ID of the requirement section or module |
| `--force` | No | Skip confirmation prompt |

## Removing a Requirement Section

```
/remove-requirement requirement "Legacy Support"
```

Removes the "Legacy Support" requirement section if it has `pending` status.

## Removing a Module

```
/remove-requirement module legacy-api
```

Removes the legacy-api module if it has `planned` or `pending` status.

## Restrictions

**Cannot remove items that are:**
- In progress (`in_progress` status)
- Complete (`complete` status)
- Already have GitHub Issues assigned

**Rationale**: Once work has started, the orchestrator must complete it. Use `/modify-requirement` to adjust scope instead.

## Dynamic Flexibility

When you remove an item:
- It is immediately removed from the plan state file
- Stop hook no longer blocks exit for that item
- Exit criteria are recalculated without the removed item

```
Before removal:
  - Modules: [A: done, B: in_progress, C: pending]
  - Pending: 2

/remove-requirement module C

After removal:
  - Modules: [A: done, B: in_progress]
  - Pending: 1
```

## State File Update

The command updates `.claude/orchestrator-plan-phase.local.md`:

**Before:**
```yaml
modules:
  - id: "auth-core"
    status: "planned"
  - id: "legacy-api"
    status: "planned"
```

**After `/remove-requirement module legacy-api`:**
```yaml
modules:
  - id: "auth-core"
    status: "planned"
```

## Examples

```bash
# Remove a pending requirement section
/remove-requirement requirement "Legacy Compatibility"

# Remove a planned module
/remove-requirement module oauth-facebook

# Remove with force (skip confirmation)
/remove-requirement module oauth-twitter --force
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Cannot remove: status is in_progress" | Module work started | Complete or reassign instead |
| "Cannot remove: status is complete" | Work already done | Cannot undo completed work |
| "Cannot remove: has GitHub Issue" | Issue already created | Close issue manually first |
| "Not found: module X" | Invalid ID | Check `/planning-status` for correct IDs |

## Related Commands

- `/planning-status` - View all requirements and modules
- `/add-requirement` - Add new requirement/module
- `/modify-requirement` - Change existing specifications
