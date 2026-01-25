---
name: arch-planning-patterns
description: Teaches orchestrators to create comprehensive planning documents through four sequential phases - architecture design, risk identification, roadmap creation, and implementation planning. Enables strategic system design, obstacle identification, execution sequencing, and actionable task breakdown for projects from conception to execution.
license: Apache-2.0
compatibility: Cross-platform compatible. Requires Python 3.8+ for utility scripts. Works with all project types and toolchains. Supports atomic file operations with UTF-8 encoding using pathlib for universal path handling.
metadata:
  author: Anthropic
  version: 1.0.0
context: fork
---

# Planning Patterns Skill

## Purpose

This skill teaches orchestrators how to create comprehensive planning documents that guide projects from conception to execution. Planning patterns enable you to design system architecture, identify risks, create execution sequences, and break work into actionable tasks.

## When to Use This Skill

Use this skill when:
- Starting a new project and need to plan it properly
- Expanding an existing system and need to plan the expansion
- Facing complex stakeholder requirements and need to organize them
- Building something novel with uncertain risks
- Leading a team and need to communicate a clear roadmap
- Running a project that is falling behind and need to replan

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

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Architecture is too complex | Break complex components into smaller sub-components with single responsibility |
| Risks are everywhere | Prioritize by impact x probability. Focus on CRITICAL and IMPORTANT risks |
| Progress stalls | Check buffer capacity. If 100% utilization, add buffer work capacity |
| Team does not understand plan | Create multiple formats: executive summary, visual sequence, milestone checklist |
| Plan became irrelevant | Revisit and update plan as conditions change |
| Task owners overcommitted | Reduce tasks, adjust scope, or add team members |

---

## Reference Documents

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

## Bun Support for JavaScript/TypeScript

When planning JavaScript or TypeScript projects, consider Bun as the primary bundler and runtime.

| Your Need | Reference |
|-----------|-----------|
| Getting Bun running | [bun-installation.md](./references/bun-installation.md) |
| Building JavaScript bundles | [bun-build-api.md](./references/bun-build-api.md) |
| Running tests | [bun-testing.md](./references/bun-testing.md) |
| Setting up CI/CD | [bun-github-actions.md](./references/bun-github-actions.md) |
| Publishing to npm | [bun-npm-publishing.md](./references/bun-npm-publishing.md) |
| Configuring package.json | [bun-package-json.md](./references/bun-package-json.md) |
| Optimizing bundles | [bun-advanced-features.md](./references/bun-advanced-features.md) |
| Solving build problems | [bun-troubleshooting.md](./references/bun-troubleshooting.md) |
| Migrating from npm/webpack | [bun-migration-checklist.md](./references/bun-migration-checklist.md) |

**Key Bun Considerations**:
1. Pin Bun versions in CI - Use `bun-version: '1.1.42'`, not `latest`
2. Use npm for publishing - `bun publish` does NOT support OIDC
3. Mark Node.js modules external - For browser builds, use `external: ["fs", "path"]`

---

## LSP Server Integration

When planning projects with remote agents or multi-language codebases, enable LSP support.

| Your Need | Reference |
|-----------|-----------|
| Understanding LSP benefits | [lsp-servers-overview.md](./references/lsp-servers-overview.md) |
| Setting up language servers | [lsp-installation-guide.md](./references/lsp-installation-guide.md) |
| Configuring LSP for project | [lsp-plugin-template.md](./references/lsp-plugin-template.md) |
| Validating LSP is working | [lsp-enforcement-checklist.md](./references/lsp-enforcement-checklist.md) |
| Managing LSP for remote agents | [orchestrator-lsp-management.md](./references/orchestrator-lsp-management.md) |

**Key LSP Considerations**:
1. Install language servers before project start
2. Use dedicated .lsp.json for configuration
3. Validate LSP health before handoff

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
