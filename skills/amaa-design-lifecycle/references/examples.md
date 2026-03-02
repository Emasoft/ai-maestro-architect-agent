# Design Lifecycle Examples

## Table of Contents

- [Example 1: Design Real-Time Collaborative Editor](#example-1-design-real-time-collaborative-editor)
- [Example 2: Design Stripe Payment Integration](#example-2-design-stripe-payment-integration)
- [Example 3: Create and Submit Design for Review (Lifecycle)](#example-3-create-and-submit-design-for-review-lifecycle)
- [Example 4: Approve and Track Implementation (Lifecycle)](#example-4-approve-and-track-implementation-lifecycle)

## Example 1: Design Real-Time Collaborative Editor

```
User: I need to build a real-time collaborative document editor similar to
Google Docs. Can you help design the architecture?

AMAA (You): Starting architecture design for real-time collaborative document
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
- Generated handoff document for AMOA with implementation phases
- Included dependency graph

Files created:
- docs_dev/design/requirements.md
- docs_dev/design/architecture.md
- docs_dev/design/modules/
- docs_dev/design/handoff-abc123.md
```

## Example 2: Design Stripe Payment Integration

```
User: We need to integrate Stripe payments into our existing e-commerce platform.

AMAA (You): Analyzing Stripe integration requirements for e-commerce platform.

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

## Example 3: Create and Submit Design for Review (Lifecycle)

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

## Example 4: Approve and Track Implementation (Lifecycle)

```
1. Verify all review comments resolved
2. Update state: APPROVED
3. Create GitHub Issues for implementation tasks
4. Notify implementers
5. Monitor implementation progress
6. Document any deviations
```
