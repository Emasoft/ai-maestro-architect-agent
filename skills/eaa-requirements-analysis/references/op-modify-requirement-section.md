---
operation: modify-requirement-section
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Modify Requirement Section Operation

## When to Use

Use this operation when:
- Marking a requirement section as in-progress or complete
- Renaming a requirement section
- Tracking progress through requirement gathering

Status progression: `pending` -> `in-progress` -> `complete`

## Prerequisites

- [ ] Plan Phase is active
- [ ] Section exists in the plan
- [ ] Status change is logical (cannot skip states)

## Procedure

### Step 1: Identify Section to Modify

```bash
/planning-status
```

Review the requirements sections and their current statuses.

### Step 2: Execute Modification

To change status:
```bash
/modify-requirement requirement "Section Name" --status complete
```

To rename:
```bash
/modify-requirement requirement "Section Name" --name "New Section Name"
```

### Step 3: Verify Change

```bash
/planning-status
```

Confirm the section shows the updated status or name.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify section to modify with `/planning-status`
- [ ] Determine new status or name
- [ ] Execute `/modify-requirement requirement ...`
- [ ] Verify change in `/planning-status`
- [ ] Update USER_REQUIREMENTS.md if section content changed

## Examples

### Example: Marking Section Complete

```bash
# Check current status
/planning-status
# Shows: Functional Requirements - pending

# Mark as in progress
/modify-requirement requirement "Functional Requirements" --status in-progress

# After documenting requirements, mark complete
/modify-requirement requirement "Functional Requirements" --status complete

# Verify
/planning-status
# Shows: Functional Requirements - complete
```

### Example: Completing All Default Sections

```bash
# Mark all sections as complete after documenting
/modify-requirement requirement "Functional Requirements" --status complete
/modify-requirement requirement "Non-Functional Requirements" --status complete
/modify-requirement requirement "Architecture Design" --status complete

# Verify all complete
/planning-status
# All sections show checkmarks
```

### Example: Renaming a Section

```bash
# Rename for clarity
/modify-requirement requirement "Architecture Design" --name "System Architecture"

# Verify
/planning-status
# Shows: System Architecture - pending
```

### Example: State File After Modification

```yaml
requirements_sections:
  - name: "Functional Requirements"
    status: "complete"           # CHANGED from pending
  - name: "Non-Functional Requirements"
    status: "in-progress"        # CHANGED from pending
  - name: "System Architecture"  # RENAMED from Architecture Design
    status: "pending"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Section not found | Name mismatch | Check exact name with `/planning-status` |
| Invalid status | Unknown status value | Use: pending, in-progress, or complete |
| Invalid transition | Skipping status | Progress through statuses in order |
| State file not found | Planning not started | Run `/start-planning` first |

## Related Operations

- [op-add-requirement-section.md](op-add-requirement-section.md) - Add new sections
- [op-remove-requirement-section.md](op-remove-requirement-section.md) - Remove pending sections
- [op-check-planning-status.md](op-check-planning-status.md) - View current statuses
