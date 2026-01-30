---
name: eaa-design-lifecycle
description: Use when creating, reviewing, or archiving design documents. Manages the complete lifecycle of design documents from creation through approval, implementation, and archival.
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

## Overview

Manage the complete lifecycle of design documents from creation through approval, implementation, and archival. This skill provides state transitions, procedures, and templates for tracking design documents through their entire journey.

## Prerequisites

- Access to design document templates at `templates/design-template.md`
- Write access to design index at `design/requirements/index.json`
- Understanding of design states and transitions

## Instructions

1. Create new design documents using PROCEDURE 1
2. Submit for review when draft is complete using PROCEDURE 2
3. Track approvals and implementation using PROCEDURES 3-4
4. Archive completed designs using PROCEDURE 5

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

## Examples

### Example 1: Create and Submit Design for Review

```
1. Generate UUID: design-auth-20260130-abc123
2. Create design from template
3. Set state: DRAFT
4. Register in design/requirements/index.json
5. Complete design content
6. Validate completeness checklist
7. Update state: REVIEW
8. Assign reviewers
```

### Example 2: Approve and Track Implementation

```
1. Verify all review comments resolved
2. Update state: APPROVED
3. Create GitHub Issues for implementation tasks
4. Notify implementers
5. Monitor implementation progress
6. Document any deviations
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid state transition | Attempted DRAFT → APPROVED | Must go through REVIEW first |
| Missing UUID | Design document lacks identifier | Generate UUID before registration |
| Index conflict | Duplicate design ID | Use unique timestamp-based UUIDs |
| Review comments unresolved | Attempting approval too early | Resolve all comments first |
| Missing template | Template file not found | Restore template from backup |

## Resources

- `templates/design-template.md` - Design document template
- `design/requirements/index.json` - Design index location
- eaa-requirements-analysis - Requirements input skill
- eaa-planning-patterns - Planning integration skill
- eaa-documentation-writing - Documentation skill
