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
| record-keeping-formats.md | Log formats and ADR templates |
| memory-categories-and-triggers.md | What to remember and when |
| handoff-procedures.md | Handoff document types and structure |
| op-load-session-state.md | Load session state on start |
| op-record-decision.md | Record architecture decisions |
| op-record-pattern.md | Record design patterns |
| op-record-stack-choice.md | Record technology choices |
| op-record-constraint.md | Record discovered constraints |
| op-record-open-question.md | Record open questions |
| op-create-handoff.md | Create session handoff document |
| op-resume-from-handoff.md | Resume session from handoff |

## Resources

- Session state: `.claude/amaa-session-state.local.md`
- Design index: `docs_dev/design/index.json`
