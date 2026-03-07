---
operation: modify-requirement-section
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: amaa-requirements-analysis
parent-plugin: ai-maestro-architect-agent
version: 1.0.0
---

# Modify Requirement Section Operation


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Identify Section to Modify](#step-1-identify-section-to-modify)
  - [Step 2: Execute Modification](#step-2-execute-modification)
  - [Step 3: Verify Change](#step-3-verify-change)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Marking Section Complete](#example-marking-section-complete)
  - [Example: Completing All Default Sections](#example-completing-all-default-sections)
  - [Example: Renaming a Section](#example-renaming-a-section)
  - [Example: State File After Modification](#example-state-file-after-modification)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

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

Check the plan state file at `.claude/orchestrator-plan-phase.local.md` to review the requirements sections and their current statuses.

### Step 2: Execute Modification

To change status:
```bash
/amaa-modify-requirement requirement "Section Name" --status complete
```

To rename:
```bash
/amaa-modify-requirement requirement "Section Name" --name "New Section Name"
```

### Step 3: Verify Change

Check the plan state file at `.claude/orchestrator-plan-phase.local.md` to confirm the section shows the updated status or name.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify section to modify by checking the plan state file at `.claude/orchestrator-plan-phase.local.md`
- [ ] Determine new status or name
- [ ] Execute `/amaa-modify-requirement requirement ...`
- [ ] Verify change in the plan state file at `.claude/orchestrator-plan-phase.local.md`
- [ ] Update USER_REQUIREMENTS.md if section content changed

## Examples

### Example: Marking Section Complete

```bash
# Check current status in plan state file (.claude/orchestrator-plan-phase.local.md)
# Shows: Functional Requirements - pending

# Mark as in progress
/amaa-modify-requirement requirement "Functional Requirements" --status in-progress

# After documenting requirements, mark complete
/amaa-modify-requirement requirement "Functional Requirements" --status complete

# Verify in plan state file (.claude/orchestrator-plan-phase.local.md)
# Shows: Functional Requirements - complete
```

### Example: Completing All Default Sections

```bash
# Mark all sections as complete after documenting
/amaa-modify-requirement requirement "Functional Requirements" --status complete
/amaa-modify-requirement requirement "Non-Functional Requirements" --status complete
/amaa-modify-requirement requirement "Architecture Design" --status complete

# Verify all complete in plan state file (.claude/orchestrator-plan-phase.local.md)
# All sections show checkmarks
```

### Example: Renaming a Section

```bash
# Rename for clarity
/amaa-modify-requirement requirement "Architecture Design" --name "System Architecture"

# Verify in plan state file (.claude/orchestrator-plan-phase.local.md)
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
| Section not found | Name mismatch | Check exact name in the plan state file at `.claude/orchestrator-plan-phase.local.md` |
| Invalid status | Unknown status value | Use: pending, in-progress, or complete |
| Invalid transition | Skipping status | Progress through statuses in order |
| State file not found | Planning not started | Run `/amaa-start-planning` first |

## Related Operations

- [op-add-requirement-section.md](op-add-requirement-section.md) - Add new sections
- [op-remove-requirement-section.md](op-remove-requirement-section.md) - Remove pending sections
- [op-check-planning-status.md](op-check-planning-status.md) - View current statuses
