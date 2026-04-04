---
name: amaa-planning-patterns
description: "Use when designing architectures, identifying risks, creating roadmaps, or breaking work into tasks. Trigger with planning or architecture design request. Loaded by ai-maestro-architect-agent-main-agent"
context: fork
agent: ai-maestro-architect-agent-main-agent
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
| [step-by-step-procedures.md](./references/step-by-step-procedures.md) | Overview, The Four Phases of Planning, Key Principles, Planning Workflow Summary, What Each Phase Contains, Common Mistakes to Avoid, When to Use Each Phase |
| [architecture-design.md](./references/architecture-design.md) | What is Architecture Design?, Architecture Design in Five Steps, Architecture Design Document Template, Component Inventory, Component Responsibilities, Data Flow Diagrams, Dependency Graph |
| [risk-identification.md](./references/risk-identification.md) | What is Risk Identification?, Risk Identification in Four Steps, Risk Categories, Risk Identification Checklist, Common Mistakes in Risk Identification, Next Steps |
| [roadmap-creation.md](./references/roadmap-creation.md) | What is Roadmap Creation?, Roadmap Creation in Five Steps, Roadmap Communication, Common Mistakes in Roadmap Creation, Roadmap Checklist, Next Steps |
| [implementation-planning.md](./references/implementation-planning.md) | What is Implementation Planning?, Implementation Planning in Four Steps, Change Management During Implementation, Implementation Planning Checklist, Common Mistakes in Implementation Planning, Next Steps |
| [planning-checklist.md](./references/planning-checklist.md) | Pre-Planning Checklist, Architecture Design Phase Checklist, Risk Identification Phase Checklist, Roadmap Creation Phase Checklist, Implementation Planning Phase Checklist, Post-Planning Verification Checklist, Quick Reference by Phase |
| [planning-scenarios.md](./references/planning-scenarios.md) | Scenario 1: Starting a Brand New Project, Scenario 2: Expanding Existing System, Scenario 3: Replanning a Project in Progress, Scenario 4: Rapid Planning (Under Pressure), Key Concepts, Phase Navigation |

## Examples

Example: `"Design auth system"` triggers all four phases sequentially.

## Error Handling

| Problem | Solution |
|---------|----------|
| Architecture too complex | Break into sub-components |
| Risks overwhelming | Prioritize by impact x probability |
| Progress stalls | Review dependency graph |
| Plan irrelevant | Revisit and update |
| Validation failing | See amaa-planning-patterns-ops skill |

## Output

| Phase | Deliverable |
|-------|-------------|
| Architecture Design | Architecture document |
| Risk Identification | Risk register |
| Roadmap Creation | Roadmap document |
| Implementation Planning | Task plan |

## Resources

See Reference Documents table above.
