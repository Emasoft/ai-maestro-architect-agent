# Handoff Document Procedures

## Table of Contents

- When to Create Handoff Documents
- Handoff Document Types
- Handoff Document Structure
- Examples
- Decision
- Rationale
- Alternatives Considered

## When to Create Handoff Documents

Create a handoff document when:
- Context window approaching limit
- Session ending intentionally
- Transitioning to implementation (handoff to AMOA)
- Major design milestone reached
- Significant time gap expected

## Handoff Document Types

| Type | Purpose | Target |
|------|---------|--------|
| `session_continuity` | Continue work in new session | Future AMAA session |
| `orchestrator_handoff` | Design approved, ready for implementation | AMOA (via AMAMA) |
| `context_clear` | Save state before context window reset | Future AMAA session |

## Handoff Document Structure

**Location:** `docs_dev/design/handoffs/handoff-{timestamp}.md`

**Sections:**
- Session Summary (project, duration, primary focus)
- Decisions Made This Session
- Patterns Applied
- Constraints Active
- Open Questions
- Current Work State
- Files Modified This Session
- Resume Instructions

## Examples

### Example 1: Session Start with Existing Context

```
AMAA: Checking for existing session state...
Found: .claude/amaa-session-state.local.md

Session ID: amaa-session-20260203-091500
Last Activity: architecture_decision_made
Decisions: 4
Constraints: 6
Open Questions: 2

Loading design index...
Index loaded: 4 decisions, 2 patterns, 6 constraints, 2 open questions

Context retrieved. Active design: design-payments-xyz789
Current phase: architecture
Next recommended action: Resolve OQ-002 (Payment processor selection)

Ready to continue design work.
```

### Example 2: Architecture Decision Made

```
AMAA: Recording architecture decision...

Creating: docs_dev/design/decisions/ADR-005-session-storage.md

---
id: ADR-005
title: Session Storage Selection
status: ACCEPTED
date: 2026-02-04
---

# ADR-005: Session Storage Selection

## Decision
Use Redis for session storage with 24-hour TTL.

## Rationale
- High read/write performance for session data
- Built-in expiration support
- Cluster mode for horizontal scaling
- Team familiarity with Redis

## Alternatives Considered
- PostgreSQL sessions: Rejected due to higher latency
- In-memory sessions: Rejected due to no horizontal scaling

## Impact
- Affects: auth-module, user-service
- Requires: Redis cluster setup in infrastructure

---

Updating design index... Done.
Updating session state... Done.

Decision ADR-005 recorded. Session state: 5 decisions, 6 constraints, 2 open questions.
```

### Example 3: Handoff Creation for Context Clear

```
AMAA: Creating handoff document for context preservation...

Gathering session context:
- Session ID: amaa-session-20260204-120000
- Decisions made: 3 (ADR-003, ADR-004, ADR-005)
- Constraints discovered: 1 (CON-007)
- Open questions: 1 resolved, 1 remaining

Generating handoff document...
Saved: docs_dev/design/handoffs/handoff-20260204-143022.md

Handoff document created. Type: context_clear
To resume: Read handoff document at docs_dev/design/handoffs/handoff-20260204-143022.md

Session state updated with handoff reference.
Ready for context clear.
```
