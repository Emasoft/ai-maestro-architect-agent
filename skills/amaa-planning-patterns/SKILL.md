---
name: amaa-planning-patterns
description: "Use when designing architectures, identifying risks, creating roadmaps, or breaking work into tasks. Trigger with planning or architecture design request."
context: fork
agent: amaa-planner
user-invocable: false
---

# Planning Patterns Skill

## Overview

Four sequential phases: Architecture Design, Risk Identification, Roadmap Creation, Implementation Planning.

## Prerequisites

- Clear project scope and requirements
- Write access to planning output directories

## Instructions

1. Read step-by-step-procedures.md for the four-phase process overview
2. Complete planning-checklist.md prerequisites
3. **Phase 1 - Architecture**: Identify components, data flows, dependencies, interfaces
4. **Phase 2 - Risks**: Discover risks, assess impact/probability, plan mitigations
5. **Phase 3 - Roadmap**: Define phases, sequence by dependencies, set milestones
6. **Phase 4 - Tasks**: Break milestones into tasks, assign owners, set up tracking
7. Have stakeholders review and approve outputs

## Checklist

Copy this checklist and track your progress:

- [ ] Complete architecture design
- [ ] Identify and assess risks
- [ ] Create roadmap with milestones

## Reference Documents

| Reference | Purpose |
|-----------|---------|
| step-by-step-procedures.md | Four phases overview and principles |
| architecture-design.md | Architecture steps and templates |
| risk-identification.md | Risk categories and checklist |
| roadmap-creation.md | Roadmap steps and communication |
| implementation-planning.md | Implementation steps and change mgmt |
| planning-checklist.md | All phase checklists combined |
| planning-scenarios.md | Four common planning scenarios |
| enforcement-mechanisms.md | Validation scripts and handoffs |
| scripts-reference.md | Planning and analysis scripts |
| tdd-planning.md | TDD integration with planning |
| requirement-immutability.md | Plan structure requirements |
| plan-verification-guide.md | Verification patterns and examples |
| plan-file-linking.md | Plan file naming and linking |

## Examples

Example: `"Design auth system"` triggers all four phases sequentially.

## Error Handling

| Problem | Solution |
|---------|----------|
| Architecture too complex | Break into sub-components |
| Risks overwhelming | Prioritize by impact x probability |
| Progress stalls | Review dependency graph |
| Plan irrelevant | Revisit and update |
| Validation failing | Run `validate_plan.py --verbose` |

## Output

| Phase | Deliverable |
|-------|-------------|
| Architecture Design | Architecture document |
| Risk Identification | Risk register |
| Roadmap Creation | Roadmap document |
| Implementation Planning | Task plan |

## Resources

See Reference Documents table above.
