# Memory Categories and Triggers

## Table of Contents

- [What to Remember](#what-to-remember)
- [Memory Storage Location](#memory-storage-location)
- [Memory Retrieval Triggers](#memory-retrieval-triggers)
- [Memory Update Triggers](#memory-update-triggers)
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
| Session state | `.claude/amaa-session-state.local.md` | YAML frontmatter + Markdown |
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
