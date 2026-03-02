# EAA Session Memory Skill

## Purpose

This skill defines how the Architect agent (EAA) handles session memory and context persistence across multiple sessions.

## Contents

| File | Description |
|------|-------------|
| `SKILL.md` | Main skill document with procedures and triggers |
| `references/` | Detailed reference documents (to be added) |

## Key Concepts

- **Session Memory**: Architecture decisions, design patterns, technology choices, constraints, and open questions that persist across sessions
- **State-Based Triggers**: Memory retrieval and updates are triggered by design state changes, not time intervals
- **Handoff Documents**: Enable session continuity across context clears or agent transitions

## Storage Locations

| Content | Location |
|---------|----------|
| Session state | `.claude/eaa-session-state.local.md` |
| Design index | `docs_dev/design/index.json` |
| Decisions | `docs_dev/design/decisions/` |
| Patterns | `docs_dev/design/patterns.md` |
| Stack | `docs_dev/design/stack.md` |
| Constraints | `docs_dev/design/constraints.md` |
| Open questions | `docs_dev/design/open-questions.md` |
| Handoffs | `docs_dev/design/handoffs/` |

## Triggers

### Memory Retrieval Triggers

1. Session start
2. Design work request received
3. Architecture decision needed
4. Design review request
5. Handoff creation request

### Memory Update Triggers

1. Architecture decision made
2. Design pattern selected
3. Technology stack choice made
4. Constraint discovered
5. Open question identified
6. Open question resolved
7. Session state change

## Related Skills

- eaa-design-lifecycle
- eaa-requirements-analysis
- eaa-planning-patterns
- eaa-design-communication-patterns
