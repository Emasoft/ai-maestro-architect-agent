---
name: amaa-planning-patterns
description: "Use when designing architectures, identifying risks, creating roadmaps, or breaking work into tasks. Trigger with planning or architecture design request."
context: fork
user-invocable: false
---

# Planning Patterns Skill

## Overview

Four sequential planning phases: Architecture Design, Risk Identification, Roadmap Creation, Implementation Planning.

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

Copy this checklist and track your progress:
- [ ] Phase 1 - Architecture Design complete
- [ ] Phase 2 - Risk Identification complete
- [ ] Phase 3 - Roadmap Creation complete
- [ ] Phase 4 - Implementation Planning complete

## Reference Documents

| Reference | Purpose |
|-----------|---------|
| [step-by-step-procedures.md](./references/step-by-step-procedures.md) | Process overview (Overview, The Four Phases of Planning, Phase 1: Architecture Design) |
| [architecture-design.md](./references/architecture-design.md) | System structure design (What is Architecture Design?, Architecture Design in Five Steps) |
| [risk-identification.md](./references/risk-identification.md) | Risk discovery and mitigation (What is Risk Identification?, Risk Identification in Four Steps) |
| [roadmap-creation.md](./references/roadmap-creation.md) | Execution plan creation (What is Roadmap Creation?, Roadmap Creation in Five Steps) |
| [implementation-planning.md](./references/implementation-planning.md) | Task breakdown (What is Implementation Planning?, Implementation Planning in Four Steps) |
| [planning-checklist.md](./references/planning-checklist.md) | Completeness (Pre-Planning Checklist, Phase Checklist) |
| [planning-scenarios.md](./references/planning-scenarios.md) | Scenarios (Starting a New Project, Key Concepts) |
| [enforcement-mechanisms.md](./references/enforcement-mechanisms.md) | Plan validation (Overview of Enforcement, Plan Validation Script) |
| [scripts-reference.md](./references/scripts-reference.md) | Utility scripts |
| [tdd-planning.md](./references/tdd-planning.md) | TDD integration (TDD Planning Principles, 1 Test strategy first - Defining tests before implementation) |
| [requirement-immutability.md](./references/requirement-immutability.md) | Requirements (Planning Phase Requirement Check, 1 Loading USER_REQUIREMENTS.md) |
| [plan-verification-guide.md](./references/plan-verification-guide.md) | Verification patterns (Overview, Patterns) |
| [plan-file-linking.md](./references/plan-file-linking.md) | GitHub issue linking (Purpose, Linking Requirements) |

## Examples

```
input: "Design architecture for a new auth system"
output:
  Phase 1: components=[auth-service, user-store, token-cache], flows=[login→auth-service→user-store]
  Phase 2: [{risk:"rate-limit abuse", impact:HIGH, mitigation:"throttle middleware"}]
  Phase 3: milestones=[MVP auth, token refresh, MFA], timeline=6w
  Phase 4: [TASK-1 setup auth-service, TASK-2 integrate user-store, TASK-3 add throttle]
```

## Error Handling

| Problem | Solution |
|---------|----------|
| Architecture too complex | Break into sub-components with single responsibility |
| Risks overwhelming | Prioritize by impact x probability; focus on CRITICAL |
| Progress stalls | Check buffer capacity; review dependency graph |
| Plan became irrelevant | Revisit and update as conditions change |
| Validation failing | Run `validate_plan.py --verbose`; fix by priority |

## Output

| Phase | Deliverable |
|-------|-------------|
| Architecture Design | Architecture document (components, flows, interfaces) |
| Risk Identification | Risk register (prioritized risks, mitigations) |
| Roadmap Creation | Master roadmap (phases, milestones, resources) |
| Implementation Planning | Task plan (assignments, dependencies, tracking) |

## Resources

- [step-by-step-procedures.md](./references/step-by-step-procedures.md) - Start here (Overview, The Four Phases of Planning, Phase 1: Architecture Design)
- [planning-scenarios.md](./references/planning-scenarios.md) - Scenarios (Scenario 1: Starting a Brand New Project, Scenario 2: Expanding Existing System)
- [enforcement-mechanisms.md](./references/enforcement-mechanisms.md) - Quality validation (Overview of Enforcement, 1 Why enforcement matters)
- [scripts-reference.md](./references/scripts-reference.md) - Utility scripts (Universal Analysis Scripts, dependency_resolver)
