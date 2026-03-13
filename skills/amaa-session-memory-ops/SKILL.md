---
name: amaa-session-memory-ops
description: "Use when recording stack choices, constraints, or managing handoffs. Trigger with session memory ops request."
context: fork
user-invocable: false
agent: ai-maestro-architect-agent-main-agent
---

# Session Memory Operations

## Overview

Operations for recording technology stack choices, constraints, open questions, and managing session handoff creation and resumption.

## Prerequisites

- Familiarity with session memory core skill (amaa-session-memory)

## Instructions

1. **Record Stack Choice** -- Use op-record-stack-choice when a technology is selected
2. **Record Constraint** -- Use op-record-constraint when a limitation is discovered
3. **Record Open Question** -- Use op-record-open-question for unresolved design questions
4. **Create Handoff** -- Use op-create-handoff when session is ending or context limit nears
5. **Resume from Handoff** -- Use op-resume-from-handoff to restore context in a new session

## Checklist

Copy this checklist and track your progress:

- [ ] Record all technology selections in stack file
- [ ] Document discovered constraints with type and impact
- [ ] Track open questions with owner and blocking info
- [ ] Create handoff document before session ends
- [ ] Resume from latest handoff when starting new session

## Reference Documents

| Document | Content |
|----------|---------|
| [op-record-stack-choice.md](references/op-record-stack-choice.md) | Purpose, When to Use, Inputs, Procedure, Core Technologies, Example, Error Handling |
| [op-record-constraint.md](references/op-record-constraint.md) | Purpose, When to Use, Inputs, Procedure, Active Constraints, Example, Error Handling |
| [op-record-open-question.md](references/op-record-open-question.md) | Purpose, When to Use, Inputs, Procedure, Open Questions, Example, Error Handling |
| [op-create-handoff.md](references/op-create-handoff.md) | Purpose, When to Use, Inputs, Procedure, Session Summary, Decisions Made This Session, Error Handling |
| [op-resume-from-handoff.md](references/op-resume-from-handoff.md) | Purpose, When to Use, Inputs, Procedure, Open Questions Requiring Attention, Session Resumed from Handoff, Error Handling |

## Examples

Example: `Record Redis 7.2 as Infrastructure stack choice with rationale for session caching`

## Error Handling

| Issue | Fix |
|-------|-----|
| Duplicate entry | Merge with existing or update version |
| Missing design index | Initialize from available design files |
| Handoff not found | Check handoffs directory path |

## Output

| Type | Description |
|------|-------------|
| Stack entries | `docs_dev/design/stack.md` |
| Constraints | `docs_dev/design/constraints.md` |
| Open questions | `docs_dev/design/open-questions.md` |
| Handoff docs | `docs_dev/design/handoffs/handoff-{timestamp}.md` |

## Resources

See Reference Documents table above.
