# Planning Patterns: Step-by-Step Procedures

## Table of Contents

1. [Overview](#overview)
2. [The Four Phases of Planning](#the-four-phases-of-planning)
   - [Phase 1: Architecture Design](#phase-1-architecture-design)
   - [Phase 2: Risk Identification](#phase-2-risk-identification)
   - [Phase 3: Roadmap Creation](#phase-3-roadmap-creation)
   - [Phase 4: Implementation Planning](#phase-4-implementation-planning)
3. [Key Principles](#key-principles)
4. [Planning Workflow Summary](#planning-workflow-summary)
5. [What Each Phase Contains](#what-each-phase-contains)
6. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
7. [When to Use Each Phase](#when-to-use-each-phase)

## Overview

Planning is the process of creating a comprehensive roadmap that guides your team from current state to desired future state. This document outlines the sequential phases that constitute professional planning.

## The Four Phases of Planning

Planning consists of these four distinct phases, executed in order:

### Phase 1: Architecture Design
**Purpose**: Define the structural blueprint of your solution
**Output**: System architecture document with all components mapped

### Phase 2: Risk Identification
**Purpose**: Discover and catalog all potential obstacles and threats
**Output**: Risk register with categorized and prioritized risks

### Phase 3: Roadmap Creation
**Purpose**: Transform architecture and risks into a time-bound execution plan
**Output**: Detailed roadmap with phases, milestones, and success criteria

### Phase 4: Implementation Planning
**Purpose**: Break down roadmap into actionable tasks with clear ownership
**Output**: Task assignments, timelines, and responsibility matrix

## Key Principles

1. **Sequential Execution**: Each phase builds upon the previous one. Do not skip phases.

2. **Specificity**: Every step must be concrete and measurable. Avoid vague statements.

3. **Documentation**: Record decisions and assumptions at each phase. These become constraints for later phases.

4. **Stakeholder Alignment**: At the end of each phase, validate outputs with stakeholders.

5. **Risk-Aware Design**: Architecture decisions must be informed by risk assessment.

## Planning Workflow Summary

```
Architecture Design
       ↓
     (produces: component map, interface definitions)
       ↓
Risk Identification
       ↓
     (produces: risk register, mitigation strategies)
       ↓
Roadmap Creation
       ↓
     (produces: timeline, dependencies, milestones)
       ↓
Implementation Planning
       ↓
     (produces: task list, ownership, success metrics)
```

## What Each Phase Contains

See the reference documents below for detailed procedures:

- **Architecture Design** (`architecture-design.md`): Component definition, interface mapping, dependency analysis
- **Risk Identification** (`risk-identification.md`): Threat discovery, impact assessment, mitigation planning
- **Roadmap Creation** (`roadmap-creation.md`): Timeline development, phase sequencing, resource planning
- **Implementation Planning** (`implementation-planning.md`): Task decomposition, ownership assignment, success criteria

## Common Mistakes to Avoid

1. **Skipping Architecture**: Do not create a roadmap without first designing the architecture
2. **Ignoring Risks**: Do not skip risk identification - it informs all downstream decisions
3. **Vague Definitions**: Every component, risk, and task must be specifically named and described
4. **Undocumented Assumptions**: If you assume something, write it down explicitly
5. **Missing Stakeholder Review**: Each phase output must be validated before proceeding

## When to Use Each Phase

- **Starting a new project**: Use all four phases in sequence
- **Expanding existing system**: Start with architecture review, then proceed through remaining phases
- **Urgent changes**: Never skip phases - document them faster, but always execute all four
- **Post-mortem analysis**: Work backwards from implementation to validate planning was sound

---

**Next Steps**: Read the reference documents in the order listed above to master each planning phase.
