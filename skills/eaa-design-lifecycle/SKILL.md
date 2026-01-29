---
name: eaa-design-lifecycle
description: Design document lifecycle management for architect agents
context: fork
agent: eaa-planner
user-invocable: false
triggers:
  - when creating design documents
  - when reviewing design status
  - when archiving completed designs
  - when tracking design evolution
---

# Design Lifecycle Skill

## Purpose

Manage the complete lifecycle of design documents from creation through approval, implementation, and archival.

## Design States

| State | Description | Transitions |
|-------|-------------|-------------|
| DRAFT | Initial creation | → REVIEW |
| REVIEW | Under review | → APPROVED / → DRAFT |
| APPROVED | Ready for implementation | → IMPLEMENTING |
| IMPLEMENTING | Being implemented | → COMPLETED |
| COMPLETED | Fully implemented | → ARCHIVED |
| ARCHIVED | Historical reference | (terminal) |

## Lifecycle Procedures

### PROCEDURE 1: Create New Design

1. Generate design UUID
2. Create design document from template
3. Set state to DRAFT
4. Register in design index
5. Notify stakeholders

### PROCEDURE 2: Submit for Review

1. Validate completeness checklist
2. Update state to REVIEW
3. Create review request
4. Assign reviewers
5. Track review comments

### PROCEDURE 3: Approve Design

1. Verify all review comments resolved
2. Update state to APPROVED
3. Create implementation tasks
4. Notify implementers
5. Link to GitHub Issues

### PROCEDURE 4: Track Implementation

1. Monitor implementation progress
2. Update design if changes needed
3. Maintain requirements traceability
4. Document deviations

### PROCEDURE 5: Complete and Archive

1. Verify all requirements implemented
2. Update state to COMPLETED
3. Archive to historical folder
4. Update design index
5. Create completion report

## Design Document Template

Located at: `templates/design-template.md`

## Design Index Location

`design/requirements/index.json`

## Related Skills

- eaa-requirements-analysis (requirements input)
- eaa-planning-patterns (planning integration)
- eaa-documentation-writing (documentation)
