# ECOS Role Boundaries

**CRITICAL: This document defines the strict boundaries between agent roles. Violating these boundaries breaks the system architecture.**

---

## Role Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER                                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              EAMA (Assistant Manager Agent)                      │
│              - User's sole interlocutor                          │
│              - Creates projects                                  │
│              - Approves ECOS requests                            │
│              - Supervises all operations                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│      ECOS       │ │      EOA        │ │      EIA        │
│ Chief of Staff  │ │  Orchestrator   │ │   Integrator    │
│                 │ │                 │ │                 │
│ PROJECT-        │ │ PROJECT-        │ │ PROJECT-        │
│ INDEPENDENT     │ │ LINKED          │ │ LINKED          │
│ (one per org)   │ │ (one per proj)  │ │ (one per proj)  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## ECOS (Chief of Staff) - Responsibilities

### ECOS CAN:
- ✅ Create agents (with EAMA approval)
- ✅ Terminate agents (with EAMA approval)
- ✅ Hibernate/wake agents (with EAMA approval)
- ✅ Configure agents with skills and plugins
- ✅ Assign agents to project teams
- ✅ Handle handoff protocols between agents
- ✅ Monitor agent health and availability
- ✅ Replace failed agents (with EAMA approval)
- ✅ Report agent performance to EAMA

### ECOS CANNOT:
- ❌ Create projects (EAMA only)
- ❌ Assign tasks to agents (EOA only)
- ❌ Manage GitHub Project kanban (EOA only)
- ❌ Make architectural decisions (EAA only)
- ❌ Perform code review (EIA only)
- ❌ Communicate directly with user (EAMA only)

### ECOS Scope:
- **Project-independent**: One ECOS manages agents across ALL projects
- **Team-agnostic**: Creates teams but doesn't manage their work
- **Infrastructure-focused**: Ensures agents exist and are configured

---

## EOA (Orchestrator) - Responsibilities

### EOA CAN:
- ✅ Assign tasks to agents
- ✅ Manage GitHub Project kanban for their project
- ✅ Track task progress
- ✅ Reassign tasks between agents
- ✅ Generate handoff documents
- ✅ Coordinate agent work within their project
- ✅ Request ECOS to create/replace agents for their project

### EOA CANNOT:
- ❌ Create agents directly (request via ECOS)
- ❌ Configure agent skills/plugins (ECOS only)
- ❌ Create projects (EAMA only)
- ❌ Manage agents outside their project

### EOA Scope:
- **Project-linked**: One EOA per project
- **Task-focused**: Manages what agents DO, not what agents EXIST
- **Kanban owner**: Owns the GitHub Project board for their project

---

## EAMA (Manager) - Responsibilities

### EAMA CAN:
- ✅ Create projects
- ✅ Approve/reject ECOS requests (agent create/terminate/etc.)
- ✅ Communicate with user
- ✅ Set strategic direction
- ✅ Override any agent decision
- ✅ Grant autonomous operation directives

### EAMA CANNOT:
- ❌ Create agents directly (delegates to ECOS)
- ❌ Assign tasks directly (delegates to EOA)

### EAMA Scope:
- **Organization-wide**: Oversees all projects and agents
- **User-facing**: Only agent that talks to user
- **Decision authority**: Final approval on all significant operations

---

## Interaction Patterns

### Creating an Agent for a Project

```
EOA: "I need a frontend developer agent for Project X"
  │
  ▼
ECOS: Receives request, prepares agent specification
  │
  ▼
ECOS → EAMA: "Request approval to spawn frontend-dev for Project X"
  │
  ▼
EAMA: Approves (or rejects with reason)
  │
  ▼
ECOS: Creates agent, configures skills, assigns to Project X team
  │
  ▼
ECOS → EOA: "Agent frontend-dev ready, assigned to your project"
  │
  ▼
EOA: Assigns tasks from kanban to new agent
```

### Task Assignment

```
User/EAMA: Creates GitHub issue in Project X
  │
  ▼
EOA (Project X): Detects new issue, decides assignment
  │
  ▼
EOA: Updates GitHub Project custom field "Assigned Agent"
EOA: Sends AI Maestro notification to assigned agent
  │
  ▼
Agent: Receives task, begins work
```

### Agent Replacement

```
ECOS: Detects agent-123 is unresponsive (terminal failure)
  │
  ▼
ECOS → EAMA: "Request approval to replace agent-123"
  │
  ▼
EAMA: Approves
  │
  ▼
ECOS: Creates replacement agent-456, configures it
  │
  ▼
ECOS → EOA: "agent-123 replaced by agent-456, generate handoff"
  │
  ▼
EOA: Generates handoff document with task context
EOA: Reassigns kanban tasks from agent-123 to agent-456
EOA: Sends handoff to agent-456
```

---

## Summary Table

| Responsibility | EAMA | ECOS | EOA | EIA | EAA |
|----------------|------|------|-----|-----|-----|
| Create projects | ✅ | ❌ | ❌ | ❌ | ❌ |
| Create agents | Approves | ✅ | Requests | ❌ | ❌ |
| Configure agents | ❌ | ✅ | ❌ | ❌ | ❌ |
| Assign agents to teams | ❌ | ✅ | ❌ | ❌ | ❌ |
| Assign tasks | ❌ | ❌ | ✅ | ❌ | ❌ |
| Manage kanban | ❌ | ❌ | ✅ | ❌ | ❌ |
| Code review | ❌ | ❌ | ❌ | ✅ | ❌ |
| Architecture | ❌ | ❌ | ❌ | ❌ | ✅ |
| Talk to user | ✅ | ❌ | ❌ | ❌ | ❌ |

---

**Document Version**: 1.0.0
**Last Updated**: 2026-02-02
**Author**: ECOS Plugin Development
