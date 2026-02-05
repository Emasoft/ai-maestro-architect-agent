---
name: eaa-design-lifecycle
description: Use when creating, reviewing, or archiving design documents. Manages design lifecycle from draft to archival. Trigger with design creation, review, or archival requests.
version: 1.0.0
compatibility: Requires AI Maestro installed.
context: fork
agent: eaa-main
user-invocable: false
triggers:
  - when creating design documents
  - when reviewing design status
  - when archiving completed designs
  - when tracking design evolution
---

# Design Lifecycle Skill

## Overview

This skill manages the complete lifecycle of design documents from creation through approval, implementation, and archival.

## Prerequisites

- Access to design document templates at `templates/design-template.md`
- Write access to design index at `design/requirements/index.json`
- Understanding of design states and transitions

## Instructions

1. Create new design documents using PROCEDURE 1
2. Submit for review when draft is complete using PROCEDURE 2
3. Track approvals and implementation using PROCEDURES 3-4
4. Archive completed designs using PROCEDURE 5

### Checklist

Copy this checklist and track your progress:

- [ ] Receive requirements from ECOS or user
- [ ] Analyze and clarify requirements
- [ ] Research APIs and technologies
- [ ] Create design documents in `docs_dev/design/`
- [ ] Break work into implementable modules
- [ ] Generate design UUID
- [ ] Register design in index
- [ ] Set initial state to DRAFT
- [ ] Complete design content
- [ ] Validate completeness checklist
- [ ] Submit for review (state: REVIEW)
- [ ] Address all review comments
- [ ] Update state to APPROVED
- [ ] Create handoff document for EOA
- [ ] Report completion to ECOS
- [ ] Track implementation progress
- [ ] Archive completed design (state: ARCHIVED)

## Output

| Output Type | Format | Location |
|-------------|--------|----------|
| Design document | Markdown | `docs_dev/design/` |
| Requirements doc | Markdown | `docs_dev/design/requirements.md` |
| Architecture doc | Markdown | `docs_dev/design/architecture.md` |
| Module specs | Markdown | `docs_dev/design/modules/` |
| Handoff document | Markdown | `docs_dev/design/handoff-{uuid}.md` |
| Design index entry | JSON | `design/requirements/index.json` |
| Completion report | Markdown | `docs_dev/design/completed/` |

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

### Example 1: Design Real-Time Collaborative Editor

```
User: I need to build a real-time collaborative document editor similar to
Google Docs. Can you help design the architecture?

EAA (You): Starting architecture design for real-time collaborative document
editor.

Phase 1 - Research:
- Researched collaborative editing technologies (OT vs CRDT)
- Analyzed requirements (concurrent editing, conflict resolution, persistence)
- Gathered information about WebSocket libraries and document storage

Phase 2 - Requirements:
- Created requirements.md documenting user specifications
- Covered: real-time sync, multiple cursors, revision history

Phase 3 - Architecture:
- Selected Y.js CRDT library and Socket.io for WebSocket handling
- Designed components:
  * WebSocket server (Node.js)
  * CRDT sync engine (Y.js)
  * Document store (PostgreSQL + Redis)
  * Client library (TypeScript)

Phase 4 - Module Breakdown:
- Created 5 core modules:
  * Connection manager
  * CRDT resolver
  * Persistence layer
  * Auth service
  * Client SDK

Phase 5 - Handoff:
- Generated handoff document for EOA with implementation phases
- Included dependency graph

Files created:
- docs_dev/design/requirements.md
- docs_dev/design/architecture.md
- docs_dev/design/modules/
- docs_dev/design/handoff-abc123.md
```

### Example 2: Design Stripe Payment Integration

```
User: We need to integrate Stripe payments into our existing e-commerce platform.

EAA (You): Analyzing Stripe integration requirements for e-commerce platform.

Phase 1 - Research:
- Read existing codebase to understand current payment flow
- Researched Stripe API capabilities (payments, subscriptions, webhooks)
- Analyzed existing order system to identify integration points

Phase 2 - Architecture:
- Recommended three components:
  * Payment Gateway module (wraps Stripe API)
  * Webhook Handler service (processes Stripe events)
  * Order State Manager (coordinates payment status with fulfillment)

Phase 3 - Security:
- Documented webhook signature verification requirements
- PCI compliance considerations

Phase 4 - Modules:
- Created module specifications with clear interfaces
- Included error handling strategies

Phase 5 - Handoff:
- Created handoff document with 3 implementation phases:
  1. Payment Gateway module
  2. Webhook integration
  3. Order system integration
- Included risk assessment (webhook delivery failures, idempotency)
- Added testing strategy

Files created:
- docs_dev/design/stripe-integration-architecture.md
- docs_dev/design/modules/payment-gateway.md
- docs_dev/design/handoff-def456.md
```

### Example 3: Create and Submit Design for Review (Lifecycle)

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

### Example 4: Approve and Track Implementation (Lifecycle)

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

## Scripts

The following scripts automate design lifecycle operations:

| Script | Purpose | Usage |
|--------|---------|-------|
| `eaa_design_lifecycle.py` | Manage design document state transitions | `python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition <STATE>` |
| `eaa_design_transition.py` | Validate and execute state transitions | `python scripts/eaa_design_transition.py --from <STATE> --to <STATE>` |
| `eaa_design_uuid.py` | Generate GUUIDs for new design documents | `python scripts/eaa_design_uuid.py --type <DOC_TYPE>` |
| `eaa_design_version.py` | Track document versions | `python scripts/eaa_design_version.py --uuid <UUID> --bump` |
| `eaa_design_export.py` | Export design documents to various formats | `python scripts/eaa_design_export.py --uuid <UUID> --format <FORMAT>` |
| `eaa_design_handoff.py` | Generate handoff documents for EOA | `python scripts/eaa_design_handoff.py --design <UUID> --target eoa` |
| `eaa_init_design_folders.py` | Initialize design folder structure | `python scripts/eaa_init_design_folders.py --project-root <PATH>` |

### Script Locations

All scripts are located at `../../scripts/` relative to this skill.

## Resources

- `templates/design-template.md` - Design document template
- `design/requirements/index.json` - Design index location
- eaa-requirements-analysis - Requirements input skill
- eaa-planning-patterns - Planning integration skill
- eaa-documentation-writing - Documentation skill
