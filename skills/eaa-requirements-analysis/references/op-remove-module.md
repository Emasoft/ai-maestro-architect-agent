---
operation: remove-module
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Remove Module Operation

## When to Use

Use this operation when:
- Scope reduction - user decides feature is not needed
- Consolidation - merging two modules into one
- Error correction - module was added by mistake

## Prerequisites

- [ ] Plan Phase is active
- [ ] Module exists with status `planned` or `pending`
- [ ] Module does NOT have a GitHub Issue (or use --force)

## Procedure

### Step 1: Verify Module Status

```bash
/planning-status --verbose
```

Check the module exists, its status, and whether it has a GitHub Issue.

### Step 2: Execute Removal

Standard removal (planned/pending only):
```bash
/remove-requirement module module-id
```

Force removal (any status):
```bash
/remove-requirement module module-id --force
```

### Step 3: Verify Removal

```bash
/planning-status --verbose
```

Confirm the module no longer appears.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify module ID with `/planning-status --verbose`
- [ ] Verify module status is planned or pending
- [ ] Check if module has GitHub Issue
- [ ] Confirm removal is intentional (no undo)
- [ ] Execute `/remove-requirement module ...`
- [ ] Verify module is removed from status

## Examples

### Example: Removing a Planned Module

```bash
# Check current modules
/planning-status --verbose
# Shows: oauth-facebook | Medium | ... | planned

# Remove module no longer needed
/remove-requirement module oauth-facebook

# Expected output:
# Removed module: oauth-facebook

# Verify
/planning-status --verbose
# Module no longer appears
```

### Example: Attempting to Remove In-Progress Module

```bash
# Module is in-progress
/remove-requirement module auth-core
# ERROR: Cannot remove: status is in-progress

# Force removal (use with caution - work may be lost)
/remove-requirement module auth-core --force

# Expected output:
# Removed module: auth-core (forced)
# WARNING: Work on this module may be lost
```

### Example: Module with GitHub Issue

```bash
# Module was approved and has GitHub Issue #42
/remove-requirement module user-mgmt
# ERROR: Cannot remove: module has GitHub Issue #42

# Force removal (issue remains open)
/remove-requirement module user-mgmt --force

# Expected output:
# Removed module: user-mgmt (forced)
# NOTE: GitHub Issue #42 remains open - close manually if needed
```

### Example: State File After Removal

Before:
```yaml
modules:
  - id: "auth-core"
    status: "planned"
  - id: "oauth-facebook"
    status: "planned"
```

After removal:
```yaml
modules:
  - id: "auth-core"
    status: "planned"
  # oauth-facebook module REMOVED
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Module not found | ID mismatch | Check exact ID with `/planning-status --verbose` |
| Cannot remove: in-progress | Work has started | Use --force if intentional (work lost) |
| Cannot remove: complete | Module finished | Use --force if intentional |
| Has GitHub Issue | Issue already created | Close issue first or use --force |
| State file not found | Planning not started | Run `/start-planning` first |

## Related Operations

- [op-add-module.md](op-add-module.md) - Add modules back
- [op-modify-module.md](op-modify-module.md) - Change properties instead
- [op-check-planning-status.md](op-check-planning-status.md) - View current modules
