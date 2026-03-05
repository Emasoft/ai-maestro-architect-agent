---
name: amaa-design-lifecycle
description: Use when managing design document states or lifecycle transitions. Trigger with design lifecycle or state transition request.
context: fork
agent: amaa-architect-main-agent
user-invocable: false
---

# Design Lifecycle Skill

## Overview

Manages the complete lifecycle of design documents: creation, review, approval, implementation tracking, and archival. Enforces valid state transitions (DRAFT->REVIEW->APPROVED->IMPLEMENTING->COMPLETED->ARCHIVED) and generates handoff documents for implementers.

## Checklist

Copy this checklist and track your progress:
- [ ] Receive requirements from AMCOS or user
- [ ] Research APIs/technologies
- [ ] Create design documents in `docs_dev/design/`
- [ ] Generate design UUID and register in index with state DRAFT
- [ ] Complete design and validate checklist
- [ ] Submit for review (state: REVIEW)
- [ ] Address review comments
- [ ] Update state to APPROVED
- [ ] Create handoff document for AMOA
- [ ] Report completion to AMCOS
- [ ] Track implementation progress
- [ ] Archive when complete (state: ARCHIVED)

## Prerequisites

- Design document template at `templates/design-template.md`
- Write access to design index at `design/requirements/index.json`

## Instructions

1. Receive requirements from AMCOS or user
2. Research APIs/technologies and create design documents in `docs_dev/design/`
3. Generate design UUID and register in index with state DRAFT
4. Complete design, validate checklist, submit for review (state: REVIEW)
5. Address review comments, update state to APPROVED
6. Create handoff document for AMOA, report completion to AMCOS
7. Track implementation progress, archive when complete (state: ARCHIVED)

## Reference Documents

| Reference | Description |
|-----------|-------------|
| [procedures.md](references/procedures.md) | Detailed procedures for each lifecycle phase |
| [design-states.md](references/design-states.md) | State machine with valid transitions |
| [examples.md](references/examples.md) | Full worked examples (Example 1: Design Real-Time Collaborative Editor, Example 2: Design Stripe Payment Integration) |
| [scripts.md](references/scripts.md) | Automation scripts reference |
| [rule-14-enforcement.md](references/rule-14-enforcement.md) | RULE 14: User Requirements Are Immutable (1 When handling user requirements in any workflow, 2 When detecting potential requirement deviations) |
| [judgment-guidelines.md](references/judgment-guidelines.md) | Architecture judgment guidelines (When to research external APIs instead of using existing documentation, When to create an ADR instead of just documenting the decision) |
| [success-criteria.md](references/success-criteria.md) | Design validation checklist (Overview, Requirements Captured, Architecture Designed, APIs Researched, Modules Specified) |
| [workflow-checklists.md](references/workflow-checklists.md) | Per-phase workflow checklists (Introduction, Checklist: Requirements Analysis, Checklist: Design Phase, Checklist: Handoff Preparation) |
| [adr-templates.md](references/adr-templates.md) | Architecture Decision Record templates |
| [handoff-format.md](references/handoff-format.md) | Handoff format specification (Overview, Handoff Validation Checklist, Validation Script, Handoff Document Template) |

## Examples

```
User: Design architecture for a real-time collaborative editor.
AMAA: Research (OT vs CRDT) -> Requirements -> Architecture (Y.js + Socket.io)
      -> Module breakdown (5 modules) -> Handoff document for AMOA
Output: docs_dev/design/{requirements,architecture,handoff-<uuid>}.md
```

## Error Handling

| Error | Solution |
|-------|----------|
| Invalid state transition | Follow valid path: DRAFT->REVIEW->APPROVED->IMPLEMENTING->COMPLETED->ARCHIVED |
| Missing UUID | Generate UUID before registration |
| Index conflict | Use unique timestamp-based UUIDs |
| Unresolved review comments | Resolve all comments before approval |

## Output

| Output Type | Location |
|-------------|----------|
| Design documents | `docs_dev/design/` |
| Handoff documents | `docs_dev/design/handoff-{uuid}.md` |
| Design index entry | `design/requirements/index.json` |

## Resources

- `templates/design-template.md` - Design document template
- amaa-requirements-analysis - Requirements input skill
- amaa-planning-patterns - Planning integration skill
