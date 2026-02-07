---
operation: create-design-document
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-design-lifecycle
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Create New Design Document

## When to Use

Use this operation when:
- Starting a new design effort from scratch
- Requirements have been received from ECOS or directly from user
- A new feature, system, or architectural change needs to be documented

## Prerequisites

- Access to design document templates at `templates/design-template.md`
- Write access to design directories (`docs_dev/design/`, `design/requirements/`)
- Requirements document or clear understanding of what needs to be designed
- Understanding of the GUUID format for unique identification

## Procedure

### Step 1: Generate Design UUID

Generate a unique identifier for the design document using the UUID generation script.

```bash
python scripts/eaa_design_uuid.py --type design
```

The UUID follows the format: `design-<feature-name>-<YYYYMMDD>-<unique-id>`

Example: `design-auth-20260130-abc123`

### Step 2: Create Design Document from Template

Copy the design template to the appropriate directory and rename it with the generated UUID.

```bash
cp templates/design-template.md docs_dev/design/design-<name>-<date>-<id>.md
```

### Step 3: Populate Required Frontmatter

Update the frontmatter section with required fields:

```yaml
---
uuid: design-auth-20260130-abc123
title: "Feature Name Design"
status: draft
created: 2026-01-30
updated: 2026-01-30
author: "Your Name"
type: design
---
```

### Step 4: Set State to DRAFT

The initial state must always be DRAFT. This is set in the frontmatter `status` field.

### Step 5: Register in Design Index

Add the new design to the design index file:

```bash
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action register
```

This updates `design/requirements/index.json` with the new entry.

### Step 6: Complete Design Content

Fill in the template sections:
- Overview / Problem Statement
- Requirements Summary
- Proposed Architecture
- Component Breakdown
- Data Flow Diagrams
- API Specifications
- Implementation Notes
- Testing Strategy
- Risk Assessment

### Step 7: Notify Stakeholders

After creating the design document, notify relevant stakeholders that a new design is available for input.

## Checklist

Copy this checklist and track your progress:

- [ ] Generate design UUID using `eaa_design_uuid.py`
- [ ] Copy template to `docs_dev/design/` with UUID-based filename
- [ ] Populate all required frontmatter fields
- [ ] Verify status is set to `draft`
- [ ] Register design in index using `eaa_design_lifecycle.py --action register`
- [ ] Complete all template sections with design content
- [ ] Add data flow diagrams if applicable
- [ ] Document API specifications if applicable
- [ ] Include risk assessment section
- [ ] Notify stakeholders of new design

## Examples

### Example: Create Authentication System Design

```bash
# Step 1: Generate UUID
python scripts/eaa_design_uuid.py --type design
# Output: design-20260130-7f3a2b

# Step 2: Create document
cp templates/design-template.md docs_dev/design/design-auth-system-20260130-7f3a2b.md

# Step 3: Register in index
python scripts/eaa_design_lifecycle.py --uuid design-auth-system-20260130-7f3a2b --action register
# Output: Registered design-auth-system-20260130-7f3a2b in design index
```

### Example: Frontmatter for New Design

```yaml
---
uuid: design-auth-system-20260130-7f3a2b
title: "User Authentication System Design"
status: draft
created: 2026-01-30
updated: 2026-01-30
author: "Architect Team"
type: design
description: "Design document for implementing secure user authentication with OAuth2 and JWT"
tags: [security, authentication, oauth, jwt]
---
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| UUID generation failed | Script not found or Python not available | Verify Python 3.8+ is installed; check script path |
| Template not found | Missing template file | Restore template from backup or create from skeleton |
| Permission denied | No write access to directory | Check directory permissions; ensure write access |
| Index registration failed | Malformed index.json or duplicate UUID | Validate JSON syntax; regenerate UUID if duplicate |
| Frontmatter validation error | Missing required fields | Add all required fields: uuid, title, status, created, updated |

## Related Operations

- [op-generate-design-uuid.md](op-generate-design-uuid.md) - UUID generation details
- [op-manage-state-transitions.md](op-manage-state-transitions.md) - State transition rules
- [op-submit-design-review.md](op-submit-design-review.md) - Next step after draft completion
