---
name: eaa-planning-patterns
description: "Use when creating architecture plans. Trigger with /plan project or design system requests."
version: 1.0.0
license: Apache-2.0
compatibility: Cross-platform compatible. Requires Python 3.8+ for utility scripts. Works with all project types and toolchains. Supports atomic file operations with UTF-8 encoding using pathlib for universal path handling. Requires AI Maestro installed.
metadata:
  author: Emasoft
context: fork
user-invocable: false
workflow-instruction: "Step 7"
procedure: "proc-create-design"
---

# Planning Patterns Skill

## Overview

This skill teaches orchestrators how to create comprehensive planning documents that guide projects from conception to execution. Planning patterns enable you to design system architecture, identify risks, create execution sequences, and break work into actionable tasks.

## Prerequisites

- Python 3.8+ for utility scripts
- Understanding of project scope and stakeholder requirements
- Write access to planning output directories
- Familiarity with project management concepts

## Instructions

Use this skill when:
- Starting a new project and need to plan it properly
- Expanding an existing system and need to plan the expansion
- Facing complex stakeholder requirements and need to organize them
- Building something novel with uncertain risks
- Leading a team and need to communicate a clear roadmap
- Running a project that is falling behind and need to replan

**Execute these phases in order:**
1. Architecture Design - Design the structural blueprint
2. Risk Identification - Discover and plan for obstacles
3. Roadmap Creation - Create a sequenced execution plan
4. Implementation Planning - Break roadmap into actionable tasks

### Checklist

Copy this checklist and track your progress:

- [ ] Read step-by-step-procedures.md for process overview
- [ ] Complete planning-checklist.md prerequisites
- [ ] **Phase 1: Architecture Design**
  - [ ] Identify all system components
  - [ ] Define component responsibilities
  - [ ] Map data flows between components
  - [ ] Identify component dependencies
  - [ ] Define component interfaces
  - [ ] Select design patterns
  - [ ] Create architecture design document
- [ ] **Phase 2: Risk Identification**
  - [ ] Discover all possible risks
  - [ ] Assess impact and probability for each risk
  - [ ] Plan mitigation strategies
  - [ ] Create risk register
  - [ ] Define monitoring plan
- [ ] **Phase 3: Roadmap Creation**
  - [ ] Define phases
  - [ ] Sequence phases by dependencies
  - [ ] Define milestones and deliverables
  - [ ] Allocate resources and estimate effort
  - [ ] Create master roadmap
- [ ] **Phase 4: Implementation Planning**
  - [ ] Break milestones into tasks
  - [ ] Create dependency network
  - [ ] Assign task owners
  - [ ] Create responsibility matrix
  - [ ] Set up tracking mechanism
- [ ] Have stakeholders review and approve outputs

## Output

This skill produces comprehensive planning documentation across four sequential phases:

| Phase | Output Artifact | Contents |
|-------|----------------|----------|
| Architecture Design | Architecture design document | System components, responsibilities, data flows, dependencies, interfaces, design patterns |
| Risk Identification | Risk register | Prioritized risks, impact/probability assessments, mitigation strategies, monitoring plans |
| Roadmap Creation | Master roadmap | Phases, execution sequence, milestones, deliverables, resource allocation, effort estimates |
| Implementation Planning | Task implementation plan | Detailed tasks, ownership assignments, dependency network, success criteria, tracking mechanisms |

## What You Will Learn

This skill teaches four specific planning activities executed in sequence:

1. **Architecture Design** - Design the structural blueprint of your system
2. **Risk Identification** - Discover and plan for obstacles
3. **Roadmap Creation** - Create a sequenced execution plan
4. **Implementation Planning** - Break the roadmap into actionable tasks

## Quick Navigation

| Activity | Output | Effort Level |
|----------|--------|--------------|
| Architecture Design | System architecture document | Significant |
| Risk Identification | Risk register | Moderate |
| Roadmap Creation | Execution sequence with phases/milestones | Moderate |
| Implementation Planning | Detailed task list with ownership | Moderate |

---

## The Planning Process

### Phase 1: Understand the Process

Before diving into details, understand the four-phase process and how they connect.

**Read first**: [step-by-step-procedures.md](./references/step-by-step-procedures.md)
- Overview of all four phases
- Workflow diagram showing dependencies
- Key principles of planning
- Common mistakes to avoid

**Companion checklist**: [planning-checklist.md](./references/planning-checklist.md)
- Pre-planning prerequisites
- Phase-by-phase checklists
- Post-planning verification

### Phase 2: Design Your System Architecture

**Read**: [architecture-design.md](./references/architecture-design.md)

| Your Need | Section to Read |
|-----------|-----------------|
| List all system components | Step 1: Identify System Components |
| Define what each component does | Step 2: Define Component Responsibilities |
| Understand how data moves | Step 3: Map Data Flows |
| Identify component dependencies | Step 4: Identify Component Dependencies |
| Define communication contracts | Step 5: Define Component Interfaces |
| Find proven design patterns | Common Architecture Patterns |
| Start your architecture document | Architecture Design Document Template |

**Output**: Architecture design document with all components mapped

### Phase 3: Identify Risks and Mitigation

**Read**: [risk-identification.md](./references/risk-identification.md)

| Your Need | Section to Read |
|-----------|-----------------|
| Find all possible risks systematically | Discover All Risks |
| Evaluate risk impact and probability | Assess Impact and Probability |
| Find mitigation strategies | Plan Mitigation Strategies |
| Document risks formally | Risk Register Template |
| Track risks over time | Monitoring Plan Definition |

**Output**: Risk register with prioritized risks and mitigations

### Phase 4: Create Your Roadmap

**Read**: [roadmap-creation.md](./references/roadmap-creation.md)

| Your Need | Section to Read |
|-----------|-----------------|
| Group work into logical phases | Step 1: Define Phases |
| Order phases by dependencies | Step 2: Sequence Phases Based on Dependencies |
| Define achievement points | Step 3: Define Milestones and Deliverables |
| Allocate people and estimate timing | Step 4: Allocate Resources and Estimate Effort |
| Create complete roadmap | Step 5: Create the Master Roadmap |

**Output**: Detailed roadmap with phases, execution sequence, milestones, resources

### Phase 5: Plan Implementation Tasks

**Read**: [implementation-planning.md](./references/implementation-planning.md)

| Your Need | Section to Read |
|-----------|-----------------|
| Decompose milestones into work units | Step 1: Break Down Milestones into Tasks |
| Find the critical path | Step 2: Create Dependency Network |
| Assign work to team members | Step 3: Assign Owners and Create Responsibility Matrix |
| Daily tracking during execution | Step 4: Create Daily/Weekly Tracking |

**Output**: Detailed task list with ownership, execution sequence, success criteria

---

## Applying These Patterns

### Scenario 1: Starting a Brand New Project

1. Architecture Design + Risk Identification (parallel)
2. Roadmap Creation
3. Implementation Planning
4. Stakeholder reviews and approvals

### Scenario 2: Expanding Existing System

1. Review existing architecture document
2. Identify what will change (new components, new data flows)
3. Document new risks (expansion risks may differ from original)
4. Create phase for expansion work
5. Plan expansion tasks

### Scenario 3: Replanning a Project in Progress

1. Review what was planned vs what actually happened
2. Update architecture if changes were made
3. Update risk register based on realized risks
4. Adjust roadmap sequence and phases
5. Replan remaining tasks

### Scenario 4: Rapid Planning (Under Pressure)

1. Do architecture quickly (focus on critical components)
2. Do risk identification quickly (focus on critical risks only)
3. Do roadmap quickly (rough sequence, critical path only)
4. Plan immediate next phase in detail
5. Plan remaining phases at higher level (can detail later)

**Important**: Even under pressure, do all four phases. Do them faster, not skip them.

---

## Key Concepts

| Concept | Definition |
|---------|------------|
| Architecture | Blueprint of how your system is organized: components, responsibilities, communication |
| Risk | Something that could prevent you from reaching your goal |
| Roadmap | Sequenced plan showing what will be built, in what order, with what dependencies |
| Milestone | Significant achievement or completion point marking end of phases |
| Task | Small, focused unit of work that one person can complete |

---

## Error Handling

| Problem | Solution |
|---------|----------|
| Architecture is too complex | Break complex components into smaller sub-components with single responsibility |
| Risks are everywhere | Prioritize by impact x probability. Focus on CRITICAL and IMPORTANT risks |
| Progress stalls | Check buffer capacity. If 100% utilization, add buffer work capacity |
| Team does not understand plan | Create multiple formats: executive summary, visual sequence, milestone checklist |
| Plan became irrelevant | Revisit and update plan as conditions change |
| Task owners overcommitted | Reduce tasks, adjust scope, or add team members |

## Examples

### Example 1: New Project Planning

```
Project: Build user authentication system

Phase 1 - Architecture:
- Components: auth-service, user-store, token-manager
- Data flows: login request → auth-service → user-store → token-manager → JWT
- Dependencies: auth-service depends on user-store

Phase 2 - Risks:
- Risk 1: OAuth provider rate limits (HIGH impact, MEDIUM probability)
- Mitigation: Implement caching, prepare fallback providers

Phase 3 - Roadmap:
- Milestone 1: Basic login (Week 1-2)
- Milestone 2: OAuth integration (Week 3-4)
- Milestone 3: Token refresh (Week 5)

Phase 4 - Tasks:
- Task 1.1: Create user schema (Owner: Dev A, 2 days)
- Task 1.2: Implement password hashing (Owner: Dev B, 1 day)
```

### Example 2: Rapid Planning Under Pressure

```
1. Quick architecture: Focus on 3 critical components only
2. Quick risks: Identify top 5 blocking risks
3. Quick roadmap: Define critical path only
4. Detailed next phase: Plan immediate tasks
5. Rough remaining phases: Detail later as needed
```

---

## Resources

### Core Planning References

| Reference | Use When |
|-----------|----------|
| [step-by-step-procedures.md](./references/step-by-step-procedures.md) | Getting the big picture |
| [architecture-design.md](./references/architecture-design.md) | Designing system structure |
| [risk-identification.md](./references/risk-identification.md) | Identifying obstacles |
| [roadmap-creation.md](./references/roadmap-creation.md) | Creating execution plan |
| [implementation-planning.md](./references/implementation-planning.md) | Breaking work into tasks |
| [planning-checklist.md](./references/planning-checklist.md) | Verifying completeness |

### Enforcement and Validation

For plan validation and quality enforcement, see [enforcement-mechanisms.md](./references/enforcement-mechanisms.md):
- 1. Overview of Enforcement - Why enforcement matters
- 2. Plan Validation Script (validate_plan.py) - Automated quality validation
- 3. Shared Thresholds Module (thresholds.py) - Task complexity and quality thresholds
- 4. Handoff Protocols - Required deliverables for handoff
- 5. Integration Workflow - Recommended validation sequence

### Scripts Reference

For all utility scripts, see [scripts-reference.md](./references/scripts-reference.md):
- 1. Universal Analysis Scripts - dependency_resolver.py, project_detector.py, health_auditor.py
- 2. Core Planning Scripts - planner.py, executor.py
- 3. Template Generation Scripts - generate_planning_checklist.py, generate_risk_register.py
- 4. Analysis Scripts - consistency_verifier.py, quality_pattern_detector.py
- 5. Task Tracker Scripts - generate_task_tracker.py, generate_status_report.py

### Test-Driven Development

For TDD integration with planning, see [tdd-planning.md](./references/tdd-planning.md):
- 1. TDD Planning Principles - Test strategy first, RED-GREEN-REFACTOR in timeline
- 2. TDD Phase Planning - Planning questions for each TDD phase
- 3. TDD Task Template Extension - Including TDD sections in task definitions
- 4. TDD Verification Checklist - Pre-completion verification items
- 5. Integration with Planning Phases - TDD in architecture, risks, roadmap, implementation

### Requirement Immutability

For handling user requirements, see [requirement-immutability.md](./references/requirement-immutability.md):
- 1. Planning Phase Requirement Check - Loading and analyzing requirements
- 2. Plan Structure Requirements - Requirement Compliance Table format
- 3. Forbidden Planning Actions - Actions that violate immutability
- 4. Correct Planning Approach - Actions that respect immutability

---

## Additional Resources

| Resource | Location |
|----------|----------|
| Plan format template | `resources/plan-format.md` |
| Plan diff specification | `resources/diff-format.md` |
| Plan verification guide | [plan-verification-guide.md](./references/plan-verification-guide.md) |
| GitHub issue linking | [plan-file-linking.md](./references/plan-file-linking.md) |

---

## Summary

| Phase | Purpose | Deliverable |
|-------|---------|-------------|
| Architecture Design | Design system blueprint | Architecture document |
| Risk Identification | Discover obstacles | Risk register |
| Roadmap Creation | Create execution sequence | Roadmap with phases |
| Implementation Planning | Create task list | Task assignments |

**Key Principles**:
- Every step must be specific and concrete
- All four phases are required - do not skip phases
- Plans change as you execute - revisit and update regularly

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Plan not progressing | Dependencies unclear or blocking | Review dependency graph with `tldr arch`, identify critical path blockers, escalate to stakeholders |
| Roadmap phases out of order | Incorrect dependency sequencing | Use `dependency_resolver.py` to validate dependency order, rebuild phase sequence |
| Stakeholders reject plan | Misaligned expectations or missing requirements | Review `requirement-immutability.md`, verify Requirement Compliance Table, schedule stakeholder alignment meeting |
| Tasks too large to estimate | Insufficient decomposition | Apply task splitting: no task >3 days. Break into sub-tasks with clear acceptance criteria |
| Risk mitigation strategies failing | Risk assessment inaccurate | Update risk register with actual realized risks, adjust impact/probability scores, revise mitigation strategies |
| Team not following plan | Plan unclear or inaccessible | Create multiple formats (executive summary, visual roadmap, daily checklist), ensure plan visibility |
| Plan validation script failing | Quality thresholds not met | Run `validate_plan.py` with `--verbose`, address specific violations in order of priority |
| Architecture becomes obsolete | System evolved differently than planned | Schedule architecture review, update component diagram, revise affected phases |

---

## Next Steps

1. Read `references/step-by-step-procedures.md` for process overview
2. Choose the activity most relevant to your current situation
3. Read the detailed reference for that activity
4. Use the templates and checklists provided
5. If using scripts, run them to generate working documents
6. Apply the planning pattern to your project
7. Have stakeholders review and approve the outputs

---

**Final Note**: Perfect planning is impossible. Good planning is achievable. The goal is to think through the major decisions before executing, so that execution is smooth and changes are managed, not chaotic.
