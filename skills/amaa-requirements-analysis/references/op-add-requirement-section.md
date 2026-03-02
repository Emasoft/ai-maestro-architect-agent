---
operation: add-requirement-section
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Add Requirement Section Operation


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Review Existing Sections](#step-1-review-existing-sections)
  - [Step 2: Add the Section](#step-2-add-the-section)
  - [Step 3: Verify Addition](#step-3-verify-addition)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Adding Security Requirements](#example-adding-security-requirements)
  - [Example: Adding Multiple Custom Sections](#example-adding-multiple-custom-sections)
  - [Example: State File After Addition](#example-state-file-after-addition)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Custom categorization is needed beyond default sections
- Tracking compliance requirements separately (security, legal, regulatory)
- Creating domain-specific requirement categories
- Organizing requirements by stakeholder or feature area

Default sections created by `/start-planning`:
- Functional Requirements
- Non-Functional Requirements
- Architecture Design

## Prerequisites

- [ ] Plan Phase is active
- [ ] Section name is not already defined
- [ ] Section name is descriptive and unique

## Procedure

### Step 1: Review Existing Sections

```bash
/planning-status
```

Verify the section does not already exist.

### Step 2: Add the Section

```bash
/add-requirement requirement "Section Name"
```

### Step 3: Verify Addition

```bash
/planning-status
```

Confirm the new section appears in the requirements progress list with status "pending".

## Checklist

Copy this checklist and track your progress:

- [ ] Check existing sections with `/planning-status`
- [ ] Determine appropriate section name
- [ ] Execute `/add-requirement requirement "Name"`
- [ ] Verify section appears in status output
- [ ] Document requirements for this section in USER_REQUIREMENTS.md

## Examples

### Example: Adding Security Requirements

```bash
# Check existing sections
/planning-status
# Shows: Functional, Non-Functional, Architecture Design

# Add security section
/add-requirement requirement "Security Requirements"

# Expected output:
# Added requirement section: Security Requirements
# Status: pending

# Verify
/planning-status
# Now shows: Functional, Non-Functional, Architecture Design, Security Requirements
```

### Example: Adding Multiple Custom Sections

```bash
# Add compliance section
/add-requirement requirement "Compliance Requirements"

# Add performance section
/add-requirement requirement "Performance Requirements"

# Add integration section
/add-requirement requirement "Integration Requirements"

# Verify all added
/planning-status --verbose
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
| State file not found | Planning not started | Run `/start-planning` first |
| Empty section name | No name provided | Provide section name in quotes |
| Invalid characters | Special characters in name | Use alphanumeric characters and spaces only |

## Related Operations

- [op-modify-requirement-section.md](op-modify-requirement-section.md) - Mark section complete
- [op-remove-requirement-section.md](op-remove-requirement-section.md) - Remove pending section
- [op-add-module.md](op-add-module.md) - Add implementation modules
