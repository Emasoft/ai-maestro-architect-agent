---
name: amaa-design-lifecycle-ops
description: "Use when applying judgment guidelines, success criteria, or handoff formats. Trigger with lifecycle ops request."
context: fork
user-invocable: false
agent: ai-maestro-architect-agent-main-agent
---

# Design Lifecycle Operations

## Overview

Operational references for design lifecycle: judgment calls, success verification, workflow checklists, ADR templates, and handoff document format.

## Prerequisites

- Familiarity with design lifecycle states (see amaa-design-lifecycle skill)

## Instructions

1. Use judgment guidelines to decide when to research APIs, create ADRs, modularize, or escalate
2. Verify each phase completion against success criteria before proceeding
3. Follow workflow checklists for requirements analysis, design, and handoff phases
4. Use ADR templates for architectural decisions and handoff format for AMOA delivery

## Checklist

Copy this checklist and track your progress:
- [ ] Review judgment guidelines for current decision
- [ ] Verify phase success criteria met
- [ ] Complete workflow checklist for current phase
- [ ] Create ADRs for significant decisions
- [ ] Prepare handoff document using template

## Reference Documents

| Document | Content |
|----------|---------|
| [judgment-guidelines.md](references/judgment-guidelines.md) | When to research external APIs instead of using existing documentation, When to create an ADR instead of just documenting the decision, When to modularize a system instead of keeping it simple, When to escalate unclear requirements to AMCOS for clarification |
| [success-criteria.md](references/success-criteria.md) | Overview, Requirements Captured, Architecture Designed, APIs Researched, Modules Specified, Handoff Prepared |
| [workflow-checklists.md](references/workflow-checklists.md) | Introduction, Checklist: Requirements Analysis, Checklist: Design Phase, Checklist: Handoff Preparation |
| [adr-templates.md](references/adr-templates.md) | Standard ADR Template, Context, Decision, Alternatives Considered, Rationale, Consequences, Related Decisions |
| [handoff-format.md](references/handoff-format.md) | Overview, Handoff Validation Checklist, Handoff Document Template, Executive Summary, Design Artifacts, Implementation Sequence, Risks and Mitigations |

## Examples

Example: `Use judgment-guidelines.md to decide whether to create ADR for database choice, then verify with success-criteria.md`

## Error Handling

| Issue | Fix |
|-------|-----|
| Success criteria not met | Review checklist, complete missing items before proceeding |
| ADR incomplete | Use template sections, ensure all fields populated |

## Output

| Type | Description |
|------|-------------|
| ADR documents | `docs_dev/design/adrs/` |
| Handoff documents | `docs_dev/design/handoff-{uuid}.md` |

## Resources

See Reference Documents table above.
