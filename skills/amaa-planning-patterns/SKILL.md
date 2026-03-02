---
name: amaa-planning-patterns
description: "Use when designing architectures, identifying risks, creating roadmaps, or breaking work into tasks."
context: fork
user-invocable: false
---

# Planning Patterns Skill

## Overview

Guides orchestrators through four sequential planning phases: Architecture Design, Risk Identification, Roadmap Creation, and Implementation Planning. Produces comprehensive planning documentation from conception to actionable tasks.

## Prerequisites

- Clear project scope and stakeholder requirements
- Write access to planning output directories

## Instructions

1. Read step-by-step-procedures.md for the four-phase process overview
2. Complete planning-checklist.md prerequisites
3. **Phase 1 - Architecture**: Identify components, responsibilities, data flows, dependencies, interfaces
4. **Phase 2 - Risks**: Discover risks, assess impact/probability, plan mitigations, create risk register
5. **Phase 3 - Roadmap**: Define phases, sequence by dependencies, set milestones, allocate resources
6. **Phase 4 - Tasks**: Break milestones into tasks, create dependency network, assign owners, set up tracking
7. Have stakeholders review and approve outputs
8. Revisit and update plans as conditions change

## Reference Documents

| Reference | Purpose |
|-----------|---------|
| [step-by-step-procedures.md](./references/step-by-step-procedures.md) | Process overview and workflow |
| [architecture-design.md](./references/architecture-design.md) | System structure design |
| [risk-identification.md](./references/risk-identification.md) | Risk discovery and mitigation |
| [roadmap-creation.md](./references/roadmap-creation.md) | Execution plan creation |
| [implementation-planning.md](./references/implementation-planning.md) | Task breakdown and assignment |
| [planning-checklist.md](./references/planning-checklist.md) | Completeness verification |
| [planning-scenarios.md](./references/planning-scenarios.md) | Scenarios, key concepts, phase navigation |
| [enforcement-mechanisms.md](./references/enforcement-mechanisms.md) | Plan validation and quality enforcement |
| [scripts-reference.md](./references/scripts-reference.md) | Utility scripts documentation |
| [tdd-planning.md](./references/tdd-planning.md) | TDD integration with planning |
| [requirement-immutability.md](./references/requirement-immutability.md) | Handling user requirements |
| [plan-verification-guide.md](./references/plan-verification-guide.md) | Plan verification patterns |
| [plan-file-linking.md](./references/plan-file-linking.md) | GitHub issue linking |

## Examples

Auth system: Phase 1 (components: auth-service, user-store), Phase 2 (risks: rate limits), Phase 3 (roadmap milestones), Phase 4 (task breakdown).

## Error Handling

| Problem | Solution |
|---------|----------|
| Architecture too complex | Break into smaller sub-components with single responsibility |
| Risks overwhelming | Prioritize by impact x probability; focus on CRITICAL risks |
| Progress stalls | Check buffer capacity; review dependency graph |
| Plan became irrelevant | Revisit and update as conditions change |
| Validation script failing | Run `validate_plan.py --verbose`; address violations by priority |

## Output

| Phase | Deliverable |
|-------|-------------|
| Architecture Design | Architecture document (components, flows, interfaces) |
| Risk Identification | Risk register (prioritized risks, mitigations) |
| Roadmap Creation | Master roadmap (phases, milestones, resources) |
| Implementation Planning | Task plan (assignments, dependencies, tracking) |

## Resources

- [step-by-step-procedures.md](./references/step-by-step-procedures.md) - Start here
- [planning-scenarios.md](./references/planning-scenarios.md) - Application scenarios
- [enforcement-mechanisms.md](./references/enforcement-mechanisms.md) - Quality validation
- [scripts-reference.md](./references/scripts-reference.md) - Utility scripts
