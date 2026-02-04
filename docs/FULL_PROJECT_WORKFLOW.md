# Full Project Workflow: From Requirements to Delivery

**Version**: 1.0.0
**Last Updated**: 2026-02-02

This document describes the complete workflow for how the Emasoft agent system handles a project from initial requirements to delivery. All agents must understand this workflow to coordinate effectively.

---

## Workflow Overview

```
USER
  │
  ▼
EAMA (Manager) ◄────────────────────────────────────────────┐
  │                                                          │
  │ 1. Creates project                                       │
  │ 2. Sends requirements to ECOS                            │
  ▼                                                          │
ECOS (Chief of Staff)                                        │
  │                                                          │
  │ 3. Evaluates project, suggests team                      │
  │ 4. Creates/assigns agents                                │
  │ 5. Notifies EAMA: team ready                             │
  ▼                                                          │
EAMA ─────────────────────────────────────────────────────►  │
  │                                                          │
  │ 6. Sends requirements to EAA                             │
  ▼                                                          │
EAA (Architect)                                              │
  │                                                          │
  │ 7. Creates design document                               │
  │ 8. Sends design to EAMA                                  │
  ▼                                                          │
EAMA ◄──── USER APPROVAL ─────────────────────────────────►  │
  │                                                          │
  │ 9. Sends approved design to EOA                          │
  ▼                                                          │
EOA (Orchestrator)                                           │
  │                                                          │
  │ 10. Splits design into tasks                             │
  │ 11. Creates task-requirements-documents                  │
  │ 12. Adds tasks to kanban                                 │
  │ 13. Assigns tasks to agents                              │
  ▼                                                          │
IMPLEMENTER AGENTS ◄───────────────────────────────────────► │
  │                                                          │
  │ 14. Work on tasks                                        │
  │ 15. Submit PRs                                           │
  ▼                                                          │
EIA (Integrator)                                             │
  │                                                          │
  │ 16. Reviews PRs                                          │
  │ 17. Merges or rejects                                    │
  ▼                                                          │
EOA ◄─────────────────────────────────────────────────────►  │
  │                                                          │
  │ 18. Reports to EAMA                                      │
  │ 19. Assigns next tasks                                   │
  └──────────────────────────────────────────────────────────┘
```

---

## Detailed Procedure Steps

### Phase 1: Project Creation and Team Setup

#### Step 1: Manager Creates Project
**Actor**: EAMA (Manager)
**Action**:
- Create a new project in a new GitHub repository (or in an existing repository)
- Send the requirements to the Chief of Staff (ECOS)

**Communication**:
- GitHub: Create repository, create initial issue with requirements
- AI Maestro: Message to ECOS with project details and requirements

#### Step 2: Chief of Staff Evaluates Project
**Actor**: ECOS (Chief of Staff)
**Action**:
- Evaluate the project requirements
- Analyze complexity, technologies involved, timeline
- Suggest an optimal team of agents to the Manager

**Communication**:
- AI Maestro: Send team proposal to EAMA with justification

#### Step 3: Team Discussion and Approval
**Actor**: EAMA (Manager) + ECOS (Chief of Staff)
**Action**:
- Manager discusses the team proposal with Chief of Staff
- Negotiate team composition if needed
- Manager ultimately approves a team proposal

**Communication**:
- AI Maestro: Back-and-forth messages until agreement

#### Step 4: Team Creation
**Actor**: ECOS (Chief of Staff)
**Action**:
- Create the agents needed for the project team
- OR move agents from other projects to the new project team
- Configure each agent with appropriate skills and plugins for their role
- Assign agents to the project team

**Communication**:
- AI Maestro: Coordination messages during agent creation
- AI Maestro: Onboarding messages to each new agent

#### Step 5: Team Ready Notification
**Actor**: ECOS (Chief of Staff)
**Action**:
- Notify the Manager that the team is set up and ready to follow instructions
- Provide team roster with agent names and roles

**Communication**:
- AI Maestro: Team ready notification to EAMA

---

### Phase 2: Design and Planning

#### Step 6: Requirements to Architect
**Actor**: EAMA (Manager)
**Action**:
- Send the requirements to the Architect agent (EAA)
- Expand the requirements with more details
- Include the list of team member names in the requirements
- Assign to the Architect the task of developing the design document

**Communication**:
- GitHub: Create issue with requirements, assign label for EAA
- AI Maestro: Message to EAA with full requirements and team roster

#### Step 7: Design Document Creation
**Actor**: EAA (Architect)
**Action**:
- Receive the task (on the kanban) to convert requirements into a full design document
- Create design document with:
  - System architecture
  - Module specifications
  - Detailed technical specs
  - Interface definitions
  - Data models

**Communication**:
- GitHub: Update issue with progress
- AI Maestro: Progress updates to EAMA

#### Step 8: Design Submission
**Actor**: EAA (Architect)
**Action**:
- Send the completed design document back to the Manager

**Communication**:
- GitHub: Attach design document to issue, mark ready for review
- AI Maestro: Notification to EAMA that design is ready

#### Step 9: Design Approval
**Actor**: EAMA (Manager) + USER
**Action**:
- Manager examines the design document
- Manager asks for approval from the User
- If User approves: design is sent to the Orchestrator
- If User rejects: design goes back to Architect with feedback

**Communication**:
- GitHub: Issue comments with design and approval status
- AI Maestro: Message to EOA with approved design

---

### Phase 3: Task Planning and Assignment

#### Step 10: Design Decomposition
**Actor**: EOA (Orchestrator)
**Action**:
- Split the design into actionable small steps
- Split each step into actionable tasks
- Tailor tasks for the current team members and their capabilities

#### Step 11: Task Requirements Documents
**Actor**: EOA (Orchestrator)
**Action**:
- Produce the task-requirements-document for each agent
- Include in each document:
  - Task description
  - Acceptance criteria
  - Related design sections
  - Dependencies
  - Expected deliverables

#### Step 12: Task Plan Creation
**Actor**: EOA (Orchestrator)
**Action**:
- Create a plan where task-requirements-documents are ordered and parallelized
- Ensure tasks can be assigned to the right agent at the right time
- Define task dependencies
- Identify tasks that can run in parallel

#### Step 13: Kanban Population
**Actor**: EOA (Orchestrator)
**Action**:
- Add tasks to the GitHub Project kanban "To-Do" column
- For each task:
  - Set the "Assigned Agent" custom field
  - Attach the task-requirements-document
  - Specify task order and dependencies
  - Ensure task executes only when required previous tasks are completed

**Communication**:
- GitHub: Create issues, add to project, set fields
- AI Maestro: Notification to each agent about their first assigned task

#### Step 14: Agent Clarification
**Actor**: EOA (Orchestrator) + IMPLEMENTER AGENTS
**Action**:
- Send to each agent a notification that their first task has been assigned
- Ask each agent if they need clarifications
- The Orchestrator is the team lead with full project understanding (along with Architect)

**Communication**:
- AI Maestro: Task assignment messages with clarification request

#### Step 15: Feedback and Design Updates (if needed)
**Actor**: IMPLEMENTER AGENTS → EOA → EAA
**Action**:
- If agents reply presenting problems or improvement suggestions:
  - Orchestrator evaluates the feedback
  - If feasible: Orchestrator sends design-change-request to Architect
  - Architect creates new version of design document
  - Architect sends updated design to Orchestrator

**Communication**:
- AI Maestro: Feedback from agents to EOA
- AI Maestro: Design change request from EOA to EAA
- AI Maestro: Updated design from EAA to EOA

#### Step 16: Task Updates from Design Changes
**Actor**: EOA (Orchestrator)
**Action**:
- Evaluate the new version of the design document
- If approved:
  - Update all task-requirements-documents affected by changes
  - Update the attachments in project kanban tasks
  - Send updated documents to assigned agents
  - Explain the changes and motivations

**Communication**:
- GitHub: Update issue attachments
- AI Maestro: Change notifications to affected agents

---

### Phase 4: Implementation

#### Step 17: Task Execution
**Actor**: IMPLEMENTER AGENTS
**Action**:
- Start working on assigned tasks
- Report status of being "in development" to Orchestrator

**Communication**:
- AI Maestro: Status update to EOA

#### Step 18: Kanban Status Update
**Actor**: EOA (Orchestrator)
**Action**:
- Move tasks on project kanban from "To-Do" column to "In-Dev" column

**Communication**:
- GitHub: Update project item status

#### Step 19: Task Completion
**Actor**: IMPLEMENTER AGENTS → EOA
**Action**:
- When an implementer agent finishes a task, notify the Orchestrator
- Orchestrator discusses and asks questions to ensure truly completed
- If OK: Orchestrator gives approval to do the pull-request
- Implementer creates PR

**Communication**:
- AI Maestro: Completion notification from agent to EOA
- AI Maestro: Approval to PR from EOA to agent
- GitHub: PR created

---

### Phase 5: Integration and Review

#### Step 20: PR Review Request
**Actor**: EOA (Orchestrator)
**Action**:
- Send message to Integrator agent (EIA) to evaluate all PRs of completed tasks
- Request merge if they pass all checks

**Communication**:
- AI Maestro: PR review request to EIA
- GitHub: PR ready for review

#### Step 21: PR Evaluation
**Actor**: EIA (Integrator)
**Action**:
- Examine the PR of each task
- Verify compliance with design requirements
- Run tests and linting
- If everything OK: merge to main
- If not OK: refuse PR, report issues to Orchestrator

**Communication**:
- GitHub: PR review comments, approval/rejection
- AI Maestro: Report to EOA with pass/fail details

#### Step 22: Handling Failed PRs
**Actor**: EOA (Orchestrator) → IMPLEMENTER AGENTS
**Action**:
- Evaluate Integrator report about each task PR
- Communicate to agents the issues and shortcomings
- Instruct agents to fix or improve the code
- Provide extended/improved task-requirements-document if needed
- Move task back to "In-Dev" column
- Ask agent if they need anything to complete the task
- If OK: implementer agent resumes work on task

**Communication**:
- AI Maestro: Feedback and instructions to agents
- GitHub: Update task status

---

### Phase 6: Completion and Continuation

#### Step 23: Successful PR Handling
**Actor**: EOA (Orchestrator)
**Action**:
- When Integrator reports successful PR merge:
  - Move task to "Done" column
  - Report to Manager (EAMA) for approval
  - If Manager approves: assign new task to the agent that finished
  - Keep implementer agents always working, never idle

**Communication**:
- GitHub: Update project item to Done
- AI Maestro: Completion report to EAMA
- AI Maestro: New task assignment to agent

#### Step 24: Iteration
**Action**:
- This cycle iterates until all tasks are complete
- Each successful merge triggers:
  - Report to Manager
  - New task assignment to available agent

---

## Communication Matrix

| From | To | Channel | Purpose |
|------|-----|---------|---------|
| EAMA | ECOS | AI Maestro | Requirements, team requests |
| ECOS | EAMA | AI Maestro | Team proposals, status updates |
| EAMA | EAA | GitHub + AI Maestro | Requirements, design requests |
| EAA | EAMA | GitHub + AI Maestro | Design documents |
| EAMA | EOA | GitHub + AI Maestro | Approved designs |
| EOA | Agents | GitHub + AI Maestro | Task assignments |
| Agents | EOA | AI Maestro | Status updates, questions |
| EOA | EAA | AI Maestro | Design change requests |
| EOA | EIA | AI Maestro | PR review requests |
| EIA | EOA | AI Maestro | PR review results |
| EOA | EAMA | AI Maestro | Completion reports |

---

## Role Boundaries Summary

| Role | Creates | Manages | Cannot Do |
|------|---------|---------|-----------|
| **EAMA** | Projects | Approvals, user communication | Task assignment |
| **ECOS** | Agents, teams | Agent lifecycle | Task assignment, projects |
| **EAA** | Designs | Architecture | Task assignment |
| **EOA** | Tasks, plans | Kanban, agent coordination | Agents, projects |
| **EIA** | Nothing | PR reviews, merges | Task assignment |
| **Agents** | Code, PRs | Their assigned tasks | Everything else |

---

## GitHub Integration Points

| Step | GitHub Action | Actor |
|------|---------------|-------|
| 1 | Create repository | EAMA |
| 6 | Create requirements issue | EAMA |
| 7 | Update issue with progress | EAA |
| 8 | Attach design document | EAA |
| 13 | Create task issues, add to project | EOA |
| 13 | Set "Assigned Agent" field | EOA |
| 18 | Move to "In-Dev" column | EOA |
| 19 | Create PR | Agent |
| 21 | Review and merge/reject PR | EIA |
| 23 | Move to "Done" column | EOA |

---

## Document References

- **Requirements Document**: Created by EAMA, sent to EAA
- **Design Document**: Created by EAA, approved by EAMA/User
- **Task-Requirements-Document**: Created by EOA for each task
- **Design-Change-Request**: Created by EOA when agents suggest improvements
- **PR Review Report**: Created by EIA for each PR

---

**This workflow must be followed by all agents. Deviations require Manager approval.**
