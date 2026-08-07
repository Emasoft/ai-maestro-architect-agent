---
name: amaa-design-lifecycle
description: "Use when managing design document states or lifecycle transitions. Trigger with design lifecycle or state transition request. Loaded by ai-maestro-architect-agent-main-agent"
context: fork
background: false
agent: ai-maestro-architect-agent-main-agent
user-invocable: false
---

# Design Lifecycle Skill

## Overview

Manages the complete lifecycle of design documents: creation, review, approval, implementation tracking, and archival. Enforces valid state transitions (DRAFT->REVIEW->APPROVED->IMPLEMENTING->COMPLETED->ARCHIVED) plus the redesign-loop re-entry edge `IMPLEMENTING->REVIEW` (so a design flaw surfaced mid-dev can be pulled back and revised), and generates handoff documents for implementers.

## Checklist

Copy this checklist and track your progress:
- [ ] Receive requirements via AMCOS (the team boundary)
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
- [ ] If a design flaw surfaces mid-dev (relayed by ORCH): run the redesign loop (IMPLEMENTING->REVIEW), revise or split/group, re-approve
- [ ] Archive when complete (state: ARCHIVED)

## Prerequisites

- Write access to `docs_dev/design/` directory for design documents
- Design scripts available at `${CLAUDE_PLUGIN_ROOT}/scripts/amaa_design_*.py`

## Instructions

1. Receive requirements via AMCOS (the team boundary)
2. Research APIs/technologies and create design documents in `docs_dev/design/`
3. Generate design UUID and register in index with state DRAFT
4. Complete design, validate checklist, submit for review (state: REVIEW)
5. Address review comments, update state to APPROVED
6. Create handoff document for AMOA, report completion to AMCOS
7. Track implementation progress, archive when complete (state: ARCHIVED)

## Reference Documents

| Reference | Description |
|-----------|-------------|
| [procedures.md](references/procedures.md) | PROCEDURE 1: Create New Design, PROCEDURE 2: Submit for Review, PROCEDURE 3: Approve Design, PROCEDURE 4: Track Implementation, PROCEDURE 5: Complete and Archive |
| [design-states.md](references/design-states.md) | State Definitions + the redesign loop (mid-dev re-entry) |
| [op-manage-state-transitions.md](references/op-manage-state-transitions.md) | When to Use, Prerequisites, Procedure, State Transition Rules, Checklist, Examples, Error Handling |
| [op-accept-redesign-request.md](references/op-accept-redesign-request.md) | When to Use, Prerequisites, Procedure, Checklist, Related Operations, Related Templates |
| [examples.md](references/examples.md) | Example 1: Design Real-Time Collaborative Editor, Example 2: Design Stripe Payment Integration, Example 3: Create and Submit Design for Review (Lifecycle), Example 4: Approve and Track Implementation (Lifecycle) |
| [scripts.md](references/scripts.md) | Script Reference |
| [rule-14-enforcement.md](references/rule-14-enforcement.md) | 1 When handling user requirements in any workflow, 2 When detecting potential requirement deviations, 3 When a technical constraint conflicts with a requirement, 4 When documenting requirement compliance |

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
| Invalid state transition | Follow valid path: DRAFT->REVIEW->APPROVED->IMPLEMENTING->COMPLETED->ARCHIVED, plus the redesign re-entry IMPLEMENTING->REVIEW |
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

- [design-template.md](templates/design-template.md) - Design document template
  - Table of Contents
  - 1. Overview
  - 2. Requirements
  - 3. Design
  - 4. Implementation Plan
  - 5. Testing Strategy
  - 6. Review History
  - 7. Change Log
  - Completeness Checklist
- [dialog-loop-comprehension-handshake.md](templates/dialog-loop-comprehension-handshake.md) - Loop A: ORCH⇄MEMBER task-comprehension handshake before coding starts
  - ORCH → MEMBER (question set)
  - MEMBER → ORCH (answers)
  - Resolution
- [dialog-loop-in-dev-issue.md](templates/dialog-loop-in-dev-issue.md) - Loop B: MEMBER⇄ORCH in-dev issue dialog (design flaw → ARCH redesign loop)
  - MEMBER → ORCH (issue report)
  - ORCH routing
  - Resolution
- [dialog-loop-pre-pr-gate.md](templates/dialog-loop-pre-pr-gate.md) - Loop C: MEMBER⇄ORCH pre-PR gate before notifying INT
  - MEMBER → ORCH (readiness claim)
  - ORCH decision
  - Resolution
- amaa-requirements-analysis - Requirements input skill
- amaa-planning-patterns - Planning integration skill
- amaa-design-lifecycle-ops - Operations and troubleshooting quick-reference companion to this skill (loaded on demand for runtime ops/debugging)
