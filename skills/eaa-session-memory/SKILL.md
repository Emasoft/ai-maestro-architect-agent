---
name: eaa-session-memory
description: "Architecture decision and design pattern persistence. Use when preserving architectural context across sessions or creating design handoffs. Trigger with session start."
version: 1.0.0
license: Apache-2.0
compatibility: "Cross-platform. Requires write access to design output directories. Requires AI Maestro installed."
metadata:
  author: Emasoft
context: fork
agent: eaa-main
user-invocable: false
workflow-instruction: "Steps 15, support"
procedure: "proc-handle-feedback, support-skill"
triggers:
  - when design session starts
  - when architecture decision is made
  - when design pattern is chosen
  - when technology stack is selected
  - when constraint is discovered
  - when open question is identified
  - when session handoff is needed
  - when resuming from previous session
---

# Session Memory Skill

## Overview

This skill defines how the Architect agent (EAA) handles session memory and context persistence. Session memory ensures that architecture decisions, design patterns, technology choices, and discovered constraints survive across multiple sessions, preventing loss of critical design context and enabling seamless session continuity.

The Architect role involves deep analysis and iterative refinement of designs. Without session memory, each new session would start from zero, forcing re-discovery of decisions already made. This skill provides the mechanisms to persist and retrieve architectural context.

## Purpose

Session memory serves four critical functions for the Architect agent:

| Function | Description |
|----------|-------------|
| **Decision Preservation** | Architecture decisions and their rationale persist across sessions |
| **Context Continuity** | Design patterns, technology choices, and constraints are not lost |
| **Handoff Enablement** | Complete context can be transferred to other agents or sessions |
| **Progress Tracking** | Open questions and pending decisions are tracked explicitly |

## Prerequisites

- Write access to design output directories (`docs_dev/design/`, `.claude/`)
- Understanding of EAA role responsibilities (see plugin docs/ROLE_BOUNDARIES.md)
- Familiarity with session state files and design index formats

## Instructions

1. **Session Start**: Check for existing session state and load context
2. **During Work**: Persist decisions, patterns, constraints, and questions as they are discovered
3. **Session End**: Create handoff document if needed
4. **Session Resume**: Load session state and handoff documents to restore context

**When to persist:**
- Architecture decision made → Create decision record (ADR)
- Design pattern selected → Update patterns.md
- Technology chosen → Update stack.md
- Constraint discovered → Add to constraints.md
- Question identified → Add to open-questions.md
- Major milestone → Create handoff document

### Checklist

Copy this checklist and track your progress:

- [ ] **Session Start**
  - [ ] Check for existing session state file at `.claude/eaa-session-state.local.md`
  - [ ] Load design index from `docs_dev/design/index.json`
  - [ ] Report retrieved context summary
- [ ] **During Session**
  - [ ] Create decision record for each architecture decision in `docs_dev/design/decisions/`
  - [ ] Update `patterns.md` when pattern is selected
  - [ ] Update `stack.md` when technology is chosen
  - [ ] Add to `constraints.md` when constraint is discovered
  - [ ] Add to `open-questions.md` when question arises
  - [ ] Update session state after each significant activity
- [ ] **Before Session End**
  - [ ] Review open questions status
  - [ ] Create handoff document if needed
  - [ ] Update session state with handoff reference
  - [ ] Confirm handoff document is complete

## Output

| Output Type | Location | Purpose |
|-------------|----------|---------|
| **Architecture Decisions** | `docs_dev/design/decisions/ADR-NNN-*.md` | Document each decision with rationale and alternatives |
| **Design Patterns** | `docs_dev/design/patterns.md` | Track patterns applied to system |
| **Technology Stack** | `docs_dev/design/stack.md` | Record technology choices |
| **Constraints Registry** | `docs_dev/design/constraints.md` | Track discovered constraints |
| **Open Questions** | `docs_dev/design/open-questions.md` | Track unresolved questions |
| **Session State** | `.claude/eaa-session-state.local.md` | Current session context |
| **Design Index** | `docs_dev/design/index.json` | Quick lookup of all artifacts |
| **Handoff Documents** | `docs_dev/design/handoffs/handoff-{timestamp}.md` | Context transfer documents |

## What to Remember

The Architect agent MUST persist the following categories of information:

### 1. Architecture Decisions Made

Every architecture decision that affects system structure or behavior.

**Required fields for each decision:**
- Decision identifier (ADR-NNN)
- Decision statement (what was decided)
- Rationale (why this decision was made)
- Alternatives considered (what was rejected and why)
- Impact scope (which components/modules affected)
- Decision state (PROPOSED, ACCEPTED, SUPERSEDED)

**Example decision types:**
- Component selection ("Use Redis for caching layer")
- Integration approach ("REST API over GraphQL")
- Data flow patterns ("Event-sourcing for order processing")
- Scaling strategy ("Horizontal scaling with stateless services")

### 2. Design Patterns Chosen

All design patterns selected for the system architecture.

**Required fields for each pattern:**
- Pattern name
- Where applied (component/module)
- Justification (why this pattern fits)
- Constraints introduced (what limitations this creates)

**Pattern categories:**
- Structural patterns (Microservices, Monolith, Modular monolith)
- Communication patterns (Request-response, Event-driven, Message queues)
- Data patterns (CQRS, Event sourcing, Repository pattern)
- Resilience patterns (Circuit breaker, Retry with backoff, Bulkhead)

### 3. Technology Stack Decisions

All technology choices that form the implementation foundation.

**Required fields for each technology choice:**
- Technology name and version
- Purpose (what role it serves)
- Rationale (why chosen over alternatives)
- Compatibility notes (integration considerations)

### 4. Constraints and Requirements Discovered

All constraints discovered during design analysis.

**Required fields for each constraint:**
- Constraint identifier (CON-NNN)
- Constraint statement
- Source (where discovered: user, research, dependency)
- Impact (which design decisions affected)
- Mitigation (how the constraint is addressed)

**Constraint types:**
- Technical ("Must support offline mode", "Maximum 100ms response time")
- Business ("Cannot use cloud services outside EU")
- Resource ("Team has no Go experience")
- Regulatory ("Must comply with GDPR")

### 5. Open Design Questions

All unresolved questions requiring future decisions.

**Required fields for each open question:**
- Question identifier (OQ-NNN)
- Question statement
- Blocking (what is blocked by this question)
- Owner (who should resolve this)
- Status (OPEN, IN_PROGRESS, RESOLVED)

## Memory Storage Location

All session memory is persisted to file-based storage in the project directory:

| Content Type | Location | Format |
|--------------|----------|--------|
| Architecture decisions | `docs_dev/design/decisions/` | Markdown files |
| Design patterns | `docs_dev/design/patterns.md` | Markdown |
| Technology stack | `docs_dev/design/stack.md` | Markdown |
| Constraints registry | `docs_dev/design/constraints.md` | Markdown |
| Open questions | `docs_dev/design/open-questions.md` | Markdown |
| Session state | `.claude/eaa-session-state.local.md` | YAML frontmatter + Markdown |
| Handoff documents | `docs_dev/design/handoffs/` | Markdown files |

## Memory Retrieval Triggers

Memory retrieval is triggered by **state changes**, not by time intervals:

| Trigger | Condition | Action |
|---------|-----------|--------|
| **Session Start** | New Claude Code session begins | Load session state and design index |
| **Design Work Request** | Receiving a design request | Retrieve relevant decisions, constraints, and questions |
| **Architecture Decision Needed** | Design choice requires explicit decision | Retrieve existing decisions and constraints |
| **Design Review Request** | Design document submitted for review | Verify consistency with decisions and constraints |
| **Handoff Creation Request** | Session handoff needed | Package complete session context |

## Memory Update Triggers

Memory updates are triggered by **state changes** in the design process:

| Trigger | Condition | Action |
|---------|-----------|--------|
| **Architecture Decision Made** | New architecture decision finalized | Create decision record, update index |
| **Design Pattern Selected** | Pattern chosen for component/module | Add pattern entry, update index |
| **Technology Stack Choice Made** | Technology selected for stack | Add entry to stack.md |
| **Constraint Discovered** | New constraint identified | Add to constraints.md, update index |
| **Open Question Identified** | Question arises that cannot be resolved | Add to open-questions.md |
| **Open Question Resolved** | Previously open question resolved | Update status to RESOLVED |
| **Session State Change** | Any significant session activity | Update session state file |

## Handoff Document Creation

Handoff documents enable session continuity across context clears or agent transitions.

### When to Create Handoff Documents

Create a handoff document when:
- Context window approaching limit
- Session ending intentionally
- Transitioning to implementation (handoff to EOA)
- Major design milestone reached
- Significant time gap expected

### Handoff Document Types

| Type | Purpose | Target |
|------|---------|--------|
| `session_continuity` | Continue work in new session | Future EAA session |
| `orchestrator_handoff` | Design approved, ready for implementation | EOA (via EAMA) |
| `context_clear` | Save state before context window reset | Future EAA session |

### Handoff Document Structure

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

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Session state file not found | First session or file deleted | Initialize new session state file |
| Design index corrupted | Manual edit or system error | Regenerate index from decision files |
| Handoff document incomplete | Interrupted creation | Re-run handoff creation procedure |
| Decision file missing | Referenced but not found | Check file path, restore from backup if available |
| Constraint ID conflict | Duplicate ID generated | Use higher sequence number, update index |

## Examples

### Example 1: Session Start with Existing Context

```
EAA: Checking for existing session state...
Found: .claude/eaa-session-state.local.md

Session ID: eaa-session-20260203-091500
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
EAA: Recording architecture decision...

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
EAA: Creating handoff document for context preservation...

Gathering session context:
- Session ID: eaa-session-20260204-120000
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

## References

Detailed reference documentation for session memory operations:

| Reference | Description |
|-----------|-------------|
| [record-keeping-formats.md](references/record-keeping-formats.md) | Session record-keeping formats and file structure specifications |

## Resources

| Resource | Location |
|----------|----------|
| Session state file | `.claude/eaa-session-state.local.md` |
| Design index | `docs_dev/design/index.json` |
| Decisions directory | `docs_dev/design/decisions/` |
| Patterns registry | `docs_dev/design/patterns.md` |
| Technology stack | `docs_dev/design/stack.md` |
| Constraints registry | `docs_dev/design/constraints.md` |
| Open questions | `docs_dev/design/open-questions.md` |
| Handoff documents | `docs_dev/design/handoffs/` |

## Related Skills

- eaa-design-lifecycle - Design document states and transitions
- eaa-requirements-analysis - Requirements gathering and management
- eaa-planning-patterns - Architecture planning procedures
- eaa-design-communication-patterns - Inter-agent communication
