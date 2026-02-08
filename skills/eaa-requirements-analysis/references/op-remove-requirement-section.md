---
operation: remove-requirement-section
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Remove Requirement Section Operation

## When to Use

Use this operation when:
- A custom requirement section is no longer needed
- Consolidating sections into fewer categories
- Correcting a section added by mistake

**Important**: Only sections with `pending` status can be removed without `--force`.

## Prerequisites

- [ ] Plan Phase is active
- [ ] Section exists in the plan
- [ ] Section status is `pending` (or use --force)
- [ ] Section is not one of the default required sections

## Procedure

### Step 1: Verify Section Status

```bash
/planning-status
```

Check the section exists and its current status.

### Step 2: Execute Removal

Standard removal (pending sections only):
```bash
/remove-requirement requirement "Section Name"
```

Force removal (any status):
```bash
/remove-requirement requirement "Section Name" --force
```

### Step 3: Verify Removal

```bash
/planning-status
```

Confirm the section no longer appears.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify section to remove with `/planning-status`
- [ ] Verify section status is pending (or use --force)
- [ ] Confirm removal is intentional (no undo)
- [ ] Execute `/remove-requirement requirement ...`
- [ ] Verify section is removed from status

## Examples

### Example: Removing a Pending Section

```bash
# Check current sections
/planning-status
# Shows: ..., Legacy Support - pending, ...

# Remove unused section
/remove-requirement requirement "Legacy Support"

# Expected output:
# Removed requirement section: Legacy Support

# Verify
/planning-status
# Section no longer appears
```

### Example: Force Removing an In-Progress Section

```bash
# Section is in-progress but user decided it's not needed
/remove-requirement requirement "Integration Requirements"
# ERROR: Cannot remove: status is in-progress

# Force removal (use with caution)
/remove-requirement requirement "Integration Requirements" --force

# Expected output:
# Removed requirement section: Integration Requirements (forced)
```

### Example: State File After Removal

Before:
```yaml
requirements_sections:
  - name: "Functional Requirements"
    status: "pending"
  - name: "Legacy Support"
    status: "pending"
```

After removal:
```yaml
requirements_sections:
  - name: "Functional Requirements"
    status: "pending"
  # Legacy Support section REMOVED
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Section not found | Name mismatch | Check exact name with `/planning-status` |
| Cannot remove | Status not pending | Use --force flag if intentional |
| State file not found | Planning not started | Run `/start-planning` first |
| Cannot remove default | Trying to remove core section | Default sections required for approval |

## Related Operations

- [op-add-requirement-section.md](op-add-requirement-section.md) - Add sections back
- [op-modify-requirement-section.md](op-modify-requirement-section.md) - Change status instead
- [op-check-planning-status.md](op-check-planning-status.md) - View current sections
