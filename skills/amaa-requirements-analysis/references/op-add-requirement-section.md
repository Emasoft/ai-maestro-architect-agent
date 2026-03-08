---
operation: add-requirement-section
---

# Add Requirement Section Operation




## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Checklist](#checklist)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Custom categorization is needed beyond default sections
- Tracking compliance requirements separately (security, legal, regulatory)
- Creating domain-specific requirement categories
- Organizing requirements by stakeholder or feature area

Default sections created by `/amaa-start-planning`:
- Functional Requirements
- Non-Functional Requirements
- Architecture Design

## Prerequisites

- [ ] Plan Phase is active
- [ ] Section name is not already defined
- [ ] Section name is descriptive and unique

## Procedure

### Step 1: Review Existing Sections

Check the plan state file at `.claude/orchestrator-plan-phase.local.md` to verify the section does not already exist.

### Step 2: Add the Section

```bash
/amaa-add-requirement requirement "Section Name"
```

### Step 3: Verify Addition

Check the plan state file at `.claude/orchestrator-plan-phase.local.md` to confirm the new section appears in the requirements progress list with status "pending".

## Checklist

Copy this checklist and track your progress:

- [ ] Check existing sections in the plan state file at `.claude/orchestrator-plan-phase.local.md`
- [ ] Determine appropriate section name
- [ ] Execute `/amaa-add-requirement requirement "Name"`
- [ ] Verify section appears in status output
- [ ] Document requirements for this section in USER_REQUIREMENTS.md

## Examples

### Example: Adding Security Requirements

```bash
# Check existing sections in plan state file (.claude/orchestrator-plan-phase.local.md)
# Shows: Functional, Non-Functional, Architecture Design

# Add security section
/amaa-add-requirement requirement "Security Requirements"

# Expected output:
# Added requirement section: Security Requirements
# Status: pending

# Verify in plan state file (.claude/orchestrator-plan-phase.local.md)
# Now shows: Functional, Non-Functional, Architecture Design, Security Requirements
```

### Example: Adding Multiple Custom Sections

```bash
# Add compliance section
/amaa-add-requirement requirement "Compliance Requirements"

# Add performance section
/amaa-add-requirement requirement "Performance Requirements"

# Add integration section
/amaa-add-requirement requirement "Integration Requirements"

# Verify all added in plan state file (.claude/orchestrator-plan-phase.local.md)
```

### Example: State File After Addition

```yaml
requirements_sections:
  - name: "Functional Requirements"
    status: "pending"
  - name: "Non-Functional Requirements"
    status: "pending"
  - name: "Architecture Design"
    status: "pending"
  - name: "Security Requirements"    # NEW
    status: "pending"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Section already exists | Duplicate name | Use a different name or modify existing |
| State file not found | Planning not started | Run `/amaa-start-planning` first |
| Empty section name | No name provided | Provide section name in quotes |
| Invalid characters | Special characters in name | Use alphanumeric characters and spaces only |

## Related Operations

- [op-modify-requirement-section.md](op-modify-requirement-section.md) - Mark section complete
- [op-remove-requirement-section.md](op-remove-requirement-section.md) - Remove pending section
- [op-add-module.md](op-add-module.md) - Add implementation modules
