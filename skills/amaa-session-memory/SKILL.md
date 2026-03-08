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

## Checklist

Copy this checklist and track your progress:

- [ ] Load session state and design index on start
- [ ] Persist decisions, patterns, constraints as discovered
- [ ] Create handoff document when session ends

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
| [record-keeping-formats.md](references/record-keeping-formats.md) | Requirements Log Format, [TIMESTAMP] - [PROJECT_NAME], Design Artifacts Structure, ADR Template, Context, Decision, Alternatives Considered |
| [memory-categories-and-triggers.md](references/memory-categories-and-triggers.md) | What to Remember, Memory Storage Location, Memory Retrieval Triggers, Memory Update Triggers |
| [handoff-procedures.md](references/handoff-procedures.md) | When to Create Handoff Documents, Handoff Document Types, Handoff Document Structure, Examples, Decision, Rationale, Alternatives Considered |
| [op-load-session-state.md](references/op-load-session-state.md) | Purpose, When to Use, Inputs, Procedure, Current Focus, Example, Error Handling |
| [op-record-decision.md](references/op-record-decision.md) | Purpose, When to Use, Inputs, Procedure, Example, Status, Error Handling |
| [op-record-pattern.md](references/op-record-pattern.md) | Purpose, When to Use, Inputs, Procedure, Applied Patterns, Example, Error Handling |
| [op-record-stack-choice.md](references/op-record-stack-choice.md) | Purpose, When to Use, Inputs, Procedure, Core Technologies, Example, Error Handling |
| [op-record-constraint.md](references/op-record-constraint.md) | Purpose, When to Use, Inputs, Procedure, Active Constraints, Example, Error Handling |
| [op-record-open-question.md](references/op-record-open-question.md) | Purpose, When to Use, Inputs, Procedure, Open Questions, Example, Error Handling |
| [op-create-handoff.md](references/op-create-handoff.md) | Purpose, When to Use, Inputs, Procedure, Session Summary, Decisions Made This Session, Error Handling |
| [op-resume-from-handoff.md](references/op-resume-from-handoff.md) | Purpose, When to Use, Inputs, Procedure, Open Questions Requiring Attention, Session Resumed from Handoff, Error Handling |

## Resources

- Session state: `.claude/amaa-session-state.local.md`
- Design index: `docs_dev/design/index.json`
