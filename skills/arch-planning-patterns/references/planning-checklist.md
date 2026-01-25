# Planning Checklist: Complete Reference

## Table of Contents

1. [Pre-Planning Checklist](#pre-planning-checklist)
2. [Architecture Design Phase Checklist](#architecture-design-phase-checklist)
   - [Component Identification](#component-identification)
   - [Component Responsibilities](#component-responsibilities)
   - [Data Flows](#data-flows)
   - [Dependencies](#dependencies)
   - [Interfaces](#interfaces)
   - [Architecture Document](#architecture-document)
3. [Risk Identification Phase Checklist](#risk-identification-phase-checklist)
   - [Risk Discovery](#risk-discovery)
   - [Risk Assessment](#risk-assessment)
   - [Mitigation Planning](#mitigation-planning)
   - [Risk Monitoring](#risk-monitoring)
   - [Risk Register](#risk-register)
4. [Roadmap Creation Phase Checklist](#roadmap-creation-phase-checklist)
   - [Phase Definition](#phase-definition)
   - [Dependencies and Sequencing](#dependencies-and-sequencing)
   - [Milestones and Deliverables](#milestones-and-deliverables)
   - [Resource Planning](#resource-planning)
   - [Master Roadmap](#master-roadmap)
   - [Communication](#communication)
5. [Implementation Planning Phase Checklist](#implementation-planning-phase-checklist)
   - [Task Breakdown](#task-breakdown)
   - [Ownership and Assignment](#ownership-and-assignment)
   - [Scheduling](#scheduling)
   - [Tracking and Status](#tracking-and-status)
   - [Change Management](#change-management)
   - [Team Communication](#team-communication)
6. [Post-Planning Verification Checklist](#post-planning-verification-checklist)
   - [Documentation](#documentation)
   - [Stakeholder Alignment](#stakeholder-alignment)
   - [Team Readiness](#team-readiness)
   - [Risk Readiness](#risk-readiness)
   - [Infrastructure Readiness](#infrastructure-readiness)
   - [Success Metrics Defined](#success-metrics-defined)
7. [Quick Reference by Phase](#quick-reference-by-phase)
   - [Architecture Design Checkpoint](#architecture-design-checkpoint)
   - [Risk Identification Checkpoint](#risk-identification-checkpoint)
   - [Roadmap Creation Checkpoint](#roadmap-creation-checkpoint)
   - [Implementation Planning Checkpoint](#implementation-planning-checkpoint)

Use this checklist to ensure you have covered all required elements for each planning phase.

## Pre-Planning Checklist

Before you begin planning, verify these prerequisites:

- ☐ Project goal is clear and documented
- ☐ Stakeholders are identified (who needs the system, who approves)
- ☐ Success criteria are defined (how do we know we succeeded?)
- ☐ Constraints are documented (timeline, budget, resources)
- ☐ Key assumptions are listed (what are we assuming to be true?)
- ☐ Planning team is assembled (who will do the planning?)
- ☐ Scope is allocated for planning (architecture + risks + roadmap + implementation phases)
- ☐ Stakeholders understand planning will take effort across multiple phases

## Architecture Design Phase Checklist

Use this checklist as you design your system architecture:

### Component Identification
- ☐ All functional requirements have been reviewed
- ☐ Each requirement has been mapped to required components
- ☐ Components are named with concrete nouns (singular)
- ☐ Each component has a single, clear primary responsibility
- ☐ No component is named after a technology ("Database" bad, "UserStore" good)
- ☐ Component list has been validated by technical team
- ☐ No obvious components are missing

### Component Responsibilities
- ☐ Each component has a detailed responsibility statement
- ☐ Responsibilities are clearly bounded (what it IS and what it IS NOT responsible for)
- ☐ Inputs and outputs are defined for each component
- ☐ At least one concrete example is provided for each component
- ☐ Responsibilities have been reviewed and agreed by team

### Data Flows
- ☐ At least one major use case has been traced completely
- ☐ For each use case, component interactions are documented step-by-step
- ☐ Data format is specified (JSON, binary, etc.)
- ☐ Error cases are documented (what happens when something fails?)
- ☐ Data flows show realistic volumes and timing
- ☐ Flows have been reviewed for correctness by technical team

### Dependencies
- ☐ All component dependencies are listed
- ☐ Direct dependencies (required) are distinguished from optional
- ☐ Dependency ordering is defined (what must initialize first?)
- ☐ Circular dependencies are identified and resolved
- ☐ Cascade effects are documented (if X fails, what else fails?)

### Interfaces
- ☐ Each component interface is formally defined
- ☐ Each method/function has input schema, output schema, behavior, errors
- ☐ Contracts are specified (what callers must always do)
- ☐ Guarantees are specified (what this component always does)
- ☐ Error conditions and responses are explicitly listed
- ☐ Interfaces have been reviewed for completeness
- ☐ **Testability Requirements**:
  - ☐ Components designed for dependency injection
  - ☐ External dependencies can be mocked/stubbed
  - ☐ Interfaces enable test isolation
  - ☐ Side effects are controllable in tests

### Architecture Document
- ☐ Component inventory section is complete
- ☐ Responsibility statements are complete
- ☐ Data flow documentation is complete
- ☐ Dependency graph is complete
- ☐ Interface specifications are complete
- ☐ Design decisions are explained in writing
- ☐ Assumptions are documented
- ☐ Constraints are documented
- ☐ Architecture pattern is clearly identified
- ☐ Document is readable by both technical and non-technical stakeholders
- ☐ Stakeholders have reviewed and approved the architecture

## Risk Identification Phase Checklist

Use this checklist as you identify and plan for risks:

### Risk Discovery
- ☐ Every component has been reviewed for possible failure modes
- ☐ Every dependency has been assessed for cascade failures
- ☐ Timeline-based risks have been identified (pre-launch, launch, post-launch)
- ☐ Stakeholders have been asked: "What keeps you up at night?"
- ☐ At least 15 distinct risks have been identified
- ☐ Risks come from multiple categories:
  - ☐ Technical risks (at least 3)
  - ☐ Resource risks (at least 2)
  - ☐ Business risks (at least 2)
  - ☐ External risks (at least 2)
  - ☐ Security risks (at least 2)
  - ☐ Operational risks (at least 2)
  - ☐ **Testing risks** (at least 2):
    - ☐ Insufficient test coverage delaying releases
    - ☐ Slow tests blocking development workflow
    - ☐ Flaky tests causing false failures
    - ☐ Missing test infrastructure/environment

### Risk Assessment
- ☐ Each risk has specific description (not vague)
- ☐ Impact is assessed (CRITICAL / HIGH / MEDIUM / LOW)
- ☐ Probability is assessed (HIGH / MEDIUM / LOW)
- ☐ Risk score is calculated (Impact × Probability)
- ☐ Affected parties are documented
- ☐ Financial impact is estimated (if applicable)
- ☐ Reputational impact is assessed (if applicable)

### Mitigation Planning
- ☐ At least one mitigation strategy for each risk
- ☐ Mitigation strategy type is specified (Prevent / Reduce / Transfer / Accept)
- ☐ Mitigation steps are specific and concrete
- ☐ Cost is estimated (scope and resources)
- ☐ Effectiveness is assessed (how much does this reduce risk?)
- ☐ Owner is assigned (who implements mitigation?)
- ☐ Sequence is set (which phase must include this mitigation?)
- ☐ High-risk mitigations are scheduled in project roadmap

### Risk Monitoring
- ☐ Monitoring indicators are defined for each risk
- ☐ How to detect risk (what signs show it is happening?)
- ☐ Who is responsible for monitoring each risk
- ☐ Monitoring frequency is specified
- ☐ Response plan is documented (what action if risk is detected?)

### Risk Register
- ☐ Risk register is formatted (table or document)
- ☐ All identified risks are in register
- ☐ Risks are prioritized by score (highest first)
- ☐ High-priority risks are visible to stakeholders
- ☐ Register includes all fields: ID, name, description, impact, probability, score, mitigation, owner, timeline, status
- ☐ Risk register is reviewed and accepted by stakeholders

## Roadmap Creation Phase Checklist

Use this checklist as you create your execution roadmap:

### Phase Definition
- ☐ Project broken into 4-8 phases (not too many, not too few)
- ☐ Each phase has clear purpose (what will be accomplished)
- ☐ Entry criteria defined for each phase (must be true before starting)
- ☐ Exit criteria defined for each phase (done when...)
- ☐ Scope classified for each phase (trivial/small/medium/large based on component count)
- ☐ Components assigned to each phase
- ☐ Phases sequenced by dependencies (prerequisites are clear)
- ☐ Critical path identified (longest chain of dependent phases)

### Dependencies and Sequencing
- ☐ Each phase lists what phases must come before it
- ☐ External dependencies are identified (third parties, other teams)
- ☐ No phase depends on a phase that comes after it (no circular dependencies)
- ☐ Parallel work opportunities are identified
- ☐ Slack/float is identified for non-critical phases

### Milestones and Deliverables
- ☐ Each phase has 1-3 milestones (not 10, not 1)
- ☐ Each milestone has specific deliverables
- ☐ Deliverables are concrete (code, documents, deployed systems)
- ☐ Definition of Done is specified for each deliverable
- ☐ Success criteria are measurable
- ☐ Milestone deliverables are clearly defined
- ☐ Milestones are spaced by logical completion points

### Resource Planning
- ☐ Team composition is specified (roles and people)
- ☐ Effort is estimated for each component (scope: trivial/small/medium/large/epic)
- ☐ Resource allocation is specified (% of time for each person)
- ☐ External resource needs are identified
- ☐ Budget is estimated (personnel, infrastructure, services)
- ☐ Budget is allocated across phases
- ☐ Risks affecting delivery are identified (and mitigations from risk register)
- ☐ Buffer capacity is included (additional scope allowance per phase)
- ☐ **TDD Time Allocation**:
  - ☐ Test writing time included (30-50% of implementation time)
  - ☐ Refactoring phases scheduled after GREEN phase
  - ☐ Test infrastructure setup time allocated in early phases
  - ☐ Code review time includes TDD compliance verification

### Master Roadmap
- ☐ Sequence view shows all phases visually
- ☐ Phases are labeled with names and deliverables
- ☐ Milestones are marked with deliverables
- ☐ Dependencies are shown
- ☐ Resource allocation is visible by phase
- ☐ Key risks and mitigations are noted
- ☐ Assumptions are listed
- ☐ Critical path is highlighted
- ☐ Launch milestone is clearly marked with deliverables

### Communication
- ☐ Executive summary (1 page) is created
- ☐ Detailed roadmap (visual timeline) is created
- ☐ Milestone checklist is created
- ☐ Risk/mitigation table is created
- ☐ Resource plan is created
- ☐ Q&A document is created (answers to common questions)
- ☐ Roadmap has been presented to stakeholders
- ☐ Stakeholders have approved roadmap

## Implementation Planning Phase Checklist

Use this checklist as you plan implementation tasks:

### Task Breakdown
- ☐ Each milestone has been broken into tasks
- ☐ Each task is scoped as trivial or small (not larger than small)
- ☐ Tasks are concrete and specific
- ☐ Each task produces a specific deliverable
- ☐ Success criteria are defined for each task
- ☐ Dependencies are mapped between tasks
- ☐ Tasks are ordered by dependency
- ☐ **TDD Plan**: Each code implementation task includes:
  - ☐ RED Phase specification (tests to write)
  - ☐ GREEN Phase scope (minimal implementation)
  - ☐ REFACTOR Phase candidates (improvements to make)
- ☐ **Test Coverage**: Target coverage percentage defined (minimum threshold)
- ☐ **Test Types**: Required test types specified (unit, integration, e2e)

### Ownership and Assignment
- ☐ Each task has one owner (not shared ownership)
- ☐ Owner has required skills (or has support plan)
- ☐ Owner is committed to deliverables
- ☐ Owner understands success criteria
- ☐ Reviewer is assigned (for code review, etc.)
- ☐ Stakeholders are identified (who is affected by outcome)
- ☐ Responsibility matrix (RACI) is created

### Scheduling
- ☐ Sequence is created showing task order
- ☐ Dependencies are honored (prerequisite tasks come first)
- ☐ Parallel work is identified and sequenced
- ☐ Critical path is identified
- ☐ Buffer capacity is allocated
- ☐ Deliverable milestones are specific (not vague)
- ☐ Workload is balanced (no person has too many tasks)

### Tracking and Status
- ☐ Daily stand-up process is defined
- ☐ Daily tracker template is created
- ☐ Weekly status reporting is planned
- ☐ Status report template is created
- ☐ Progress tracking dashboard is set up
- ☐ How will you know tasks are complete? (definition of done)
- ☐ How will you track blockers and risks?
- ☐ Who receives status reports (stakeholders)?
- ☐ **TDD Compliance Tracking**:
  - ☐ Commit message pattern verification (test/feat/refactor)
  - ☐ Test-first workflow compliance monitoring
  - ☐ Test coverage metrics in status reports
  - ☐ RED-GREEN-REFACTOR phase completion tracking

### Change Management
- ☐ Change request process is defined
- ☐ Who approves changes?
- ☐ How are changes communicated to team?
- ☐ How are changes tracked?
- ☐ Who updates the plan when changes are approved?

### Team Communication
- ☐ All task owners understand their tasks
- ☐ All dependencies are understood
- ☐ Success criteria are clear to everyone
- ☐ Communication plan is established (daily standup, weekly review, etc.)
- ☐ Escalation path is defined (what to do when blocked)
- ☐ Team has committed to the plan

## Post-Planning Verification Checklist

After all four phases are complete, verify everything is in place:

### Documentation
- ☐ Architecture design document is complete and approved
- ☐ Risk register is complete and approved
- ☐ Roadmap is complete and approved
- ☐ Implementation plan is complete and team committed
- ☐ All documents are shared with stakeholders
- ☐ Version control is set up (who has latest version?)

### Stakeholder Alignment
- ☐ All stakeholders have reviewed all documents
- ☐ Stakeholders have asked questions and received answers
- ☐ Stakeholders have approved proceeding with execution
- ☐ Stakeholder concerns are documented
- ☐ Any stakeholder objections have been addressed

### Team Readiness
- ☐ Team understands the goal
- ☐ Team understands the architecture
- ☐ Team understands the roadmap
- ☐ Team understands their tasks and deliverables
- ☐ Team has resources needed (tools, access, training)
- ☐ Team has committed to the plan

### Risk Readiness
- ☐ High-risk mitigations are in progress or scheduled
- ☐ Risk monitoring is set up
- ☐ Contingency plans exist for critical risks
- ☐ Team knows how to escalate when risks are detected

### Infrastructure Readiness
- ☐ Development environment is ready
- ☐ Version control (git, etc.) is set up
- ☐ Deployment environment exists (staging, production)
- ☐ Monitoring and alerting is planned
- ☐ Logging is configured
- ☐ Backup and recovery procedures exist

### Success Metrics Defined
- ☐ Project success criteria are clear
- ☐ How success will be measured is documented
- ☐ Launch criteria are defined (when is project "done"?)
- ☐ Post-launch metrics are defined (what will be measured after launch?)

## Quick Reference by Phase

### Architecture Design Checkpoint
Use this when you finish architecture phase:
- Every component has single responsibility ☐
- All data flows documented with examples ☐
- All dependencies mapped ☐
- Component interfaces defined ☐
- Stakeholders approved architecture ☐

### Risk Identification Checkpoint
Use this when you finish risk phase:
- At least 15 risks identified ☐
- Each risk assessed for impact × probability ☐
- Mitigation strategies planned ☐
- Risk monitoring defined ☐
- Stakeholders approved risk register ☐

### Roadmap Creation Checkpoint
Use this when you finish roadmap phase:
- All phases defined with entry/exit criteria ☐
- Phases sequenced by dependencies ☐
- Milestones with specific deliverables ☐
- Resources allocated ☐
- Buffer capacity included ☐
- Stakeholders approved roadmap ☐

### Implementation Planning Checkpoint
Use this when you finish implementation planning phase:
- Each milestone broken into tasks ☐
- Tasks have owners and deliverables ☐
- Task dependencies mapped ☐
- Daily tracking set up ☐
- Team committed to plan ☐
- **TDD Requirements Defined** ☐:
  - Each code task has TDD plan (RED-GREEN-REFACTOR phases)
  - Test coverage thresholds specified
  - Commit message pattern requirements documented
  - Code review includes TDD compliance verification

---

**Usage Note**: Do not use this checklist to bypass the detailed references. This checklist is a summary to ensure completeness, not a substitute for reading the detailed guidance in each reference document.

Use this checklist to:
1. Track progress through each planning phase
2. Ensure nothing important is missed
3. Verify you are ready to move to next phase
4. Hand off to stakeholders for review

Each checkbox should represent work that was actually done, not just "yes, we did that."
