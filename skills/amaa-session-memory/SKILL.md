---
name: amaa-session-memory
description: "Use when persisting decisions, patterns, and constraints across sessions. Trigger with session memory or handoff request."
context: fork
user-invocable: false
agent: amaa-architect-main-agent
---

# Session Memory Skill

## Overview

This skill defines how the Architect agent (AMAA) handles session memory and context persistence. Session memory ensures that architecture decisions, design patterns, technology choices, and discovered constraints survive across multiple sessions, preventing loss of critical design context and enabling seamless session continuity.

## Prerequisites

- Write access to design output directories (`docs_dev/design/`, `.claude/`)
- Understanding of AMAA role responsibilities (see plugin `docs/ROLE_BOUNDARIES.md`)
- Familiarity with session state files and design index formats

## Instructions

1. **Session Start** -- Check for existing session state at `.claude/amaa-session-state.local.md` and load the design index from `docs_dev/design/index.json`
2. **During Work** -- Persist decisions, patterns, constraints, and questions as discovered
3. **Session End** -- Create handoff document if context window is near limit or session is ending
4. **Session Resume** -- Load session state and latest handoff document to restore context

### Checklist

Copy this checklist and track your progress:

- [ ] Load session state and design index on start
- [ ] Create ADR in `docs_dev/design/decisions/` for each architecture decision
- [ ] Update `patterns.md`, `stack.md`, `constraints.md`, `open-questions.md` as needed
- [ ] Update session state after each significant activity
- [ ] Review open questions before session end
- [ ] Create handoff document when needed (see [handoff-procedures.md](references/handoff-procedures.md))

## Examples

```
AMAA: Loading session state...
Found 4 decisions, 6 constraints, 2 open questions.
Active design: design-payments-xyz789 (architecture phase)
Next action: Resolve OQ-002 (Payment processor selection)
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Session state not found | First session or file deleted | Initialize new session state file |
| Design index corrupted | Manual edit or system error | Regenerate index from decision files |
| Handoff document incomplete | Interrupted creation | Re-run handoff creation procedure |

## Output

| Output Type | Location |
|-------------|----------|
| Architecture Decisions | `docs_dev/design/decisions/ADR-NNN-*.md` |
| Session State | `.claude/amaa-session-state.local.md` |
| Design Index | `docs_dev/design/index.json` |
| Handoff Documents | `docs_dev/design/handoffs/handoff-{timestamp}.md` |

## References

| Reference | Description |
|-----------|-------------|
| [record-keeping-formats.md](references/record-keeping-formats.md) | Session record-keeping formats and file structure specs (ADR Template, Handoff Document Template) |
| [memory-categories-and-triggers.md](references/memory-categories-and-triggers.md) | Detailed memory categories, required fields, storage locations, and triggers (What to Remember, Architecture Decisions Made) |
| [handoff-procedures.md](references/handoff-procedures.md) | Handoff document types, structure, and extended examples (Handoff Document Types, Handoff Document Structure) |
| [op-load-session-state.md](references/op-load-session-state.md) | Procedure: load session state (Procedure, Check for Existing Session State) |
| [op-record-decision.md](references/op-record-decision.md) | Procedure: record architecture decision (Procedure, Determine ADR Number) |
| [op-record-pattern.md](references/op-record-pattern.md) | Procedure: record design pattern (Purpose, When to Use, Procedure) |
| [op-record-stack-choice.md](references/op-record-stack-choice.md) | Procedure: record technology stack choice (Purpose, When to Use, Procedure) |
| [op-record-constraint.md](references/op-record-constraint.md) | Procedure: record constraint (Purpose, When to Use, Procedure) |
| [op-record-open-question.md](references/op-record-open-question.md) | Procedure: record open question (Procedure, Ensure Open Questions File Exists) |
| [op-create-handoff.md](references/op-create-handoff.md) | Procedure: create handoff document (Purpose, When to Use, Procedure) |
| [op-resume-from-handoff.md](references/op-resume-from-handoff.md) | Procedure: resume from handoff (Purpose, When to Use, Procedure) |

## Resources

| Resource | Location |
|----------|----------|
| Session state file | `.claude/amaa-session-state.local.md` |
| Design index | `docs_dev/design/index.json` |
| Decisions directory | `docs_dev/design/decisions/` |
| Handoff documents | `docs_dev/design/handoffs/` |
