---
operation: remove-module
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: amaa-requirements-analysis
parent-plugin: ai-maestro-architect-agent
version: 1.0.0
---

# Remove Module Operation


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Verify Module Status](#step-1-verify-module-status)
  - [Step 2: Execute Removal](#step-2-execute-removal)
  - [Step 3: Verify Removal](#step-3-verify-removal)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Removing a Planned Module](#example-removing-a-planned-module)
  - [Example: Attempting to Remove In-Progress Module](#example-attempting-to-remove-in-progress-module)
  - [Example: Module with GitHub Issue](#example-module-with-github-issue)
  - [Example: State File After Removal](#example-state-file-after-removal)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

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

Check the plan state file at `.claude/orchestrator-plan-phase.local.md` to verify the module exists, its status, and whether it has a GitHub Issue.

### Step 2: Execute Removal

Standard removal (planned/pending only):
```bash
/amaa-remove-requirement module module-id
```

Force removal (any status):
```bash
/amaa-remove-requirement module module-id --force
```

### Step 3: Verify Removal

Check the plan state file at `.claude/orchestrator-plan-phase.local.md` to confirm the module no longer appears.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify module ID by checking the plan state file at `.claude/orchestrator-plan-phase.local.md`
- [ ] Verify module status is planned or pending
- [ ] Check if module has GitHub Issue
- [ ] Confirm removal is intentional (no undo)
- [ ] Execute `/amaa-remove-requirement module ...`
- [ ] Verify module is removed from status

## Examples

### Example: Removing a Planned Module

```bash
# Check current modules in the plan state file
# .claude/orchestrator-plan-phase.local.md
# Shows: oauth-facebook | Medium | ... | planned

# Remove module no longer needed
/amaa-remove-requirement module oauth-facebook

# Expected output:
# Removed module: oauth-facebook

# Verify by checking plan state file
# .claude/orchestrator-plan-phase.local.md
# Module no longer appears
```

### Example: Attempting to Remove In-Progress Module

```bash
# Module is in-progress
/amaa-remove-requirement module auth-core
# ERROR: Cannot remove: status is in-progress

# Force removal (use with caution - work may be lost)
/amaa-remove-requirement module auth-core --force

# Expected output:
# Removed module: auth-core (forced)
# WARNING: Work on this module may be lost
```

### Example: Module with GitHub Issue

```bash
# Module was approved and has GitHub Issue #42
/amaa-remove-requirement module user-mgmt
# ERROR: Cannot remove: module has GitHub Issue #42

# Force removal (issue remains open)
/amaa-remove-requirement module user-mgmt --force

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
| Module not found | ID mismatch | Check exact ID in the plan state file at `.claude/orchestrator-plan-phase.local.md` |
| Cannot remove: in-progress | Work has started | Use --force if intentional (work lost) |
| Cannot remove: complete | Module finished | Use --force if intentional |
| Has GitHub Issue | Issue already created | Close issue first or use --force |
| State file not found | Planning not started | Run `/amaa-start-planning` first |

## Related Operations

- [op-add-module.md](op-add-module.md) - Add modules back
- [op-modify-module.md](op-modify-module.md) - Change properties instead
- [op-check-planning-status.md](op-check-planning-status.md) - View current modules
