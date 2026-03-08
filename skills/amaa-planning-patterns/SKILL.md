---
name: amaa-planning-patterns
description: "Use when designing architectures, identifying risks, creating roadmaps, or breaking work into tasks. Trigger with planning or architecture design request."
context: fork
agent: amaa-planner
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
| [step-by-step-procedures.md](./references/step-by-step-procedures.md) | Overview, The Four Phases of Planning, Key Principles, Planning Workflow Summary, What Each Phase Contains, Common Mistakes to Avoid, When to Use Each Phase |
| [architecture-design.md](./references/architecture-design.md) | What is Architecture Design?, Architecture Design in Five Steps, Architecture Design Document Template, Component Inventory, Component Responsibilities, Data Flow Diagrams, Dependency Graph |
| [risk-identification.md](./references/risk-identification.md) | What is Risk Identification?, Risk Identification in Four Steps, Risk Categories, Risk Identification Checklist, Common Mistakes in Risk Identification, Next Steps |
| [roadmap-creation.md](./references/roadmap-creation.md) | What is Roadmap Creation?, Roadmap Creation in Five Steps, Roadmap Communication, Common Mistakes in Roadmap Creation, Roadmap Checklist, Next Steps |
| [implementation-planning.md](./references/implementation-planning.md) | What is Implementation Planning?, Implementation Planning in Four Steps, Change Management During Implementation, Implementation Planning Checklist, Common Mistakes in Implementation Planning, Next Steps |
| [planning-checklist.md](./references/planning-checklist.md) | Pre-Planning Checklist, Architecture Design Phase Checklist, Risk Identification Phase Checklist, Roadmap Creation Phase Checklist, Implementation Planning Phase Checklist, Post-Planning Verification Checklist, Quick Reference by Phase |
| [planning-scenarios.md](./references/planning-scenarios.md) | Scenario 1: Starting a Brand New Project, Scenario 2: Expanding Existing System, Scenario 3: Replanning a Project in Progress, Scenario 4: Rapid Planning (Under Pressure), Key Concepts, Phase Navigation |
| [enforcement-mechanisms.md](./references/enforcement-mechanisms.md) | Overview of Enforcement, Plan Validation Script (validate_plan.py), Shared Thresholds Module (thresholds.py), Handoff Protocols, Integration Workflow |
| [scripts-reference.md](./references/scripts-reference.md) | Universal Analysis Scripts, Core Planning Scripts, Template Generation Scripts, Analysis Scripts, Task Tracker Scripts |
| [tdd-planning.md](./references/tdd-planning.md) | TDD Planning Principles, TDD Phase Planning, TDD Task Template Extension, TDD Verification Checklist, Integration with Planning Phases |
| [requirement-immutability.md](./references/requirement-immutability.md) | Planning Phase Requirement Check, Plan Structure Requirements, Forbidden Planning Actions, Correct Planning Approach |
| [plan-verification-guide.md](./references/plan-verification-guide.md) | Overview, Part 1: Verification Patterns, Part 2: Checklist Template & Task Tracker Integration, Part 3: Examples, Best Practices, Troubleshooting, Related Documentation |
| [plan-file-linking.md](./references/plan-file-linking.md) | Purpose, Linking Requirements, Overview, Implementation Plan, Sub-Plans, Plan File Naming Convention, Automatic Linking |

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

- [step-by-step-procedures.md](./references/step-by-step-procedures.md) - Overview, The Four Phases of Planning, Key Principles, Planning Workflow Summary, What Each Phase Contains, Common Mistakes to Avoid, When to Use Each Phase
- [planning-scenarios.md](./references/planning-scenarios.md) - Scenario 1: Starting a Brand New Project, Scenario 2: Expanding Existing System, Scenario 3: Replanning a Project in Progress, Scenario 4: Rapid Planning (Under Pressure), Key Concepts, Phase Navigation
- [enforcement-mechanisms.md](./references/enforcement-mechanisms.md) - Overview of Enforcement, Plan Validation Script (validate_plan.py), Shared Thresholds Module (thresholds.py), Handoff Protocols, Integration Workflow
- [scripts-reference.md](./references/scripts-reference.md) - Universal Analysis Scripts, Core Planning Scripts, Template Generation Scripts, Analysis Scripts, Task Tracker Scripts
