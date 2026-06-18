# AMAMA Role Boundaries

> **⚠️ SECONDARY ECOSYSTEM-OVERVIEW DOC — NOT AUTHORITATIVE FOR COMMUNICATION**
>
> This file is a high-level overview of how the AI Maestro roles relate to
> each other. It is **NOT** the authoritative source for the ARCHITECT's
> communication model. The authoritative communication model is **R6 v3**,
> defined in:
> - `agents/ai-maestro-architect-agent-main-agent.md` (the **Communication
>   Permissions** section), and
> - the rules under `~/.claude/rules/`.
>
> **On any conflict, those sources win over this document.** In particular,
> under R6 v3 the ARCHITECT (AMAA) is **team-internal**: all intake and
> completion reporting flow through **AMCOS (Chief of Staff)** at the team
> boundary; **MANAGER (AMAMA) reaches team-internal agents ONLY via AMCOS**;
> there is a direct **AMAA → AMOA** edge for design handoffs; and ARCHITECT
> peers route via the **ORCHESTRATOR (AMOA)**.

> **Note**: This is a local reference copy. The authoritative source for role boundaries and governance rules is the `team-governance` skill in the AI Maestro core system.

**CRITICAL: This document defines the strict boundaries between agent roles. Violating these boundaries breaks the system architecture.**

---

## Role Hierarchy

Under **R6 v3**, MANAGER (AMAMA) does **not** reach the team-internal
agents (AMOA, AMIA, AMAA) directly — every message crosses the team
boundary through **AMCOS (Chief of Staff)**:

```
┌─────────────────────────────────────────────────────────────────┐
│                           MAESTRO                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              AMAMA (AI Maestro Assistant Manager Agent)            │
│              - User's sole interlocutor                          │
│              - Creates projects                                  │
│              - Approves AMCOS requests                           │
│              - Supervises all operations                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │  (MANAGER ⇄ team-internal agents
                           │   ONLY via AMCOS — the team boundary)
                           ▼
              ┌─────────────────────────┐
              │          AMCOS          │
              │     Chief of Staff      │
              │      TEAM-SCOPED        │
              │     (one per team)      │
              │  = the team boundary    │
              └────────────┬────────────┘
                           │  (intake + completion reporting
         ┌─────────────────┼─────────────────┐  for every team-internal agent)
         │                 │                 │
         ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│      AMOA       │ │      AMIA       │ │      AMAA       │
│  Orchestrator   │ │   Integrator    │ │   Architect     │
│                 │ │                 │ │                 │
│ PROJECT-        │ │ PROJECT-        │ │ PROJECT-        │
│ LINKED          │ │ LINKED          │ │ LINKED          │
│ (one per proj)  │ │ (one per proj)  │ │ (one per proj)  │
└────────┬────────┘ └─────────────────┘ └────────┬────────┘
         │                                       │
         │   ◄───── direct AMAA → AMOA ──────────┘
         │          design-handoff edge
         ▼
   (ARCHITECT peers route via the ORCHESTRATOR)
```

**Team-internal routing (R6 v3):** AMAA, AMOA, and AMIA are
**team-internal**. Their intake and completion reporting flow through
**AMCOS** at the team boundary. The one exception edge is the direct
**AMAA → AMOA** handoff for delivering a finished design; ARCHITECT
peers route via the **ORCHESTRATOR (AMOA)**.

---

## AMCOS (Chief of Staff) - Responsibilities

### AMCOS CAN:
- ✅ Create agents under a MANAGER team-creation mandate (R30 — no per-agent approval)
- ✅ Terminate agents within its own team (R29/R30 mandate scope)
- ✅ Hibernate/wake agents within its own team
- ✅ Configure agents with skills and plugins
- ✅ Assign agents to project teams
- ✅ Handle handoff protocols between agents
- ✅ Monitor agent health and availability
- ✅ Replace failed base members to keep the 5-member base intact (R30/R31 — within mandate)
- ✅ Report agent performance up through the team boundary to the MANAGER

### AMCOS CANNOT:
- ❌ Create projects (AMAMA only)
- ❌ Assign tasks to agents (AMOA only)
- ❌ Manage GitHub Project kanban (AMOA only)
- ❌ Make architectural decisions (AMAA only)
- ❌ Perform code review (AMIA only)
- ❌ Communicate directly with users (users interact via their own ASSISTANT agent — R38/R39)

### AMCOS Scope:
- **Team-scoped**: One AMCOS per team manages agents within the team
- **Team boundary (R6 v3)**: AMCOS is the communication boundary for the
  team — MANAGER (AMAMA) reaches the team-internal agents (AMOA, AMIA,
  AMAA) **only via AMCOS**, and those agents' intake and completion
  reporting flow back out through AMCOS
- **Infrastructure-focused**: Ensures agents exist and are configured

---

## AMOA (Orchestrator) - Responsibilities

### AMOA CAN:
- ✅ Assign tasks to agents
- ✅ Manage GitHub Project kanban for their project
- ✅ Track task progress
- ✅ Reassign tasks between agents
- ✅ Generate handoff documents
- ✅ Coordinate agent work within their project
- ✅ Request AMCOS to create/replace agents for their project

### AMOA CANNOT:
- ❌ Create agents directly (request via AMCOS)
- ❌ Configure agent skills/plugins (AMCOS only)
- ❌ Create projects (AMAMA only)
- ❌ Manage agents outside their project

### AMOA Scope:
- **Project-linked**: One AMOA per project
- **Task-focused**: Manages what agents DO, not what agents EXIST
- **Kanban owner**: Owns the GitHub Project board for their project

---

## AMAMA (Manager) - Responsibilities

### AMAMA CAN:
- ✅ Create projects
- ✅ Create and delete teams on its own authority — team creation auto-creates the COS + 5 base members (R29.1)
- ✅ Grant the COS a team-creation mandate to populate the team with extra MEMBER agents (R29.2 / R30)
- ✅ Create and delete AUTONOMOUS and MAINTAINER agents on its own authority (R29.3)
- ✅ Serve the MAESTRO and relay MAESTRO-directed decisions (R37.1)
- ✅ Set strategic direction
- ✅ Override any agent decision
- ✅ Grant autonomous operation directives

### AMAMA CANNOT:
- ❌ Create individual extra MEMBER agents itself — the COS builds those out under the mandate; the MANAGER's team creation only auto-provisions the COS + 5 base members (R29/R30)
- ❌ Assign tasks directly (delegates to AMOA)
- ❌ Change its own identity, or obey any user other than the MAESTRO (R26 / R37.1)

### AMAMA Scope:
- **Organization-wide**: Oversees all projects and agents
- **MAESTRO-facing**: serves the MAESTRO; non-MAESTRO users interact through their own ASSISTANT agent (R38/R39), never via a direct agent↔user channel
- **Decision authority**: Final approval on all significant operations

---

## Interaction Patterns

### Creating an Agent for a Project

```
AMOA: "I need a frontend developer agent for Project X"
  │
  ▼
AMCOS: Receives request, prepares agent specification
  │
  ▼
AMCOS: Confirms the request is within its MANAGER team-creation mandate
       (an extra MEMBER agent; the 5-member base stays intact — R30.2).
       Only a request BEYOND the mandate needs a fresh MANAGER mandate (R30.1)
  │
  ▼
AMCOS: Creates agent, configures skills, assigns to Project X team
  │
  ▼
AMCOS → AMOA: "Agent frontend-dev ready, assigned to your project"
  │
  ▼
AMOA: Assigns tasks from kanban to new agent
```

### Task Assignment

```
User/AMAMA: Creates GitHub issue in Project X
  │
  ▼
AMOA (Project X): Detects new issue, decides assignment
  │
  ▼
AMOA: Updates GitHub Project custom field "Assigned Agent"
AMOA: Sends AI Maestro notification to assigned agent
  │
  ▼
Agent: Receives task, begins work
```

### Agent Replacement

```
AMCOS: Detects agent-123 is unresponsive (terminal failure)
  │
  ▼
AMCOS: Replacing a failed base member is within the team-creation mandate
       and is required to keep the 5-member base present (R30 / R31)
  │
  ▼
AMCOS: Creates replacement agent-456, configures it
  │
  ▼
AMCOS → AMOA: "agent-123 replaced by agent-456, generate handoff"
  │
  ▼
AMOA: Generates handoff document with task context
AMOA: Reassigns kanban tasks from agent-123 to agent-456
AMOA: Sends handoff to agent-456
```

---

## Governance Titles

Each agent role maps to a governance title:

| Role | Governance Title | Scope |
|------|-----------------|-------|
| AMAMA | Manager | Organization-wide, user-facing |
| AMCOS | Chief of Staff | Team-scoped, agent lifecycle |
| AMOA | Member (Orchestrator) | Project-linked, task management |
| AMIA | Member (Integrator) | Project-linked, code integration |
| AMAA | Member (Architect) | Project-linked, architecture |

---

## Summary Table

| Responsibility | AMAMA | AMCOS | AMOA | AMIA | AMAA |
|----------------|------|------|-----|-----|-----|
| Create projects | ✅ | ❌ | ❌ | ❌ | ❌ |
| Create agents | Team + 5 base (R29) | ✅ under mandate (R30) | Requests | ❌ | ❌ |
| Configure agents | ❌ | ✅ | ❌ | ❌ | ❌ |
| Assign agents to teams | ❌ | ✅ | ❌ | ❌ | ❌ |
| Assign tasks | ❌ | ❌ | ✅ | ❌ | ❌ |
| Manage kanban | ❌ | ❌ | ✅ | ❌ | ❌ |
| Code review | ❌ | ❌ | ❌ | ✅ | ❌ |
| Architecture | ❌ | ❌ | ❌ | ❌ | ✅ |
| Serve the MAESTRO (user-facing via ASSISTANT model, R37/R39) | ✅ | ❌ | ❌ | ❌ | ❌ |

---

**Document Version**: 2.8.0
**Last Updated**: 2026-06-19
**Author**: AMCOS Plugin Development

> Governance model updated to R26–R40 (GOVERNANCE-RULES.md v4.0.2): MANAGER team-lifecycle authority (R29), COS mandate + invariant 5-member base (R30/R31), and the MAESTRO apex + ASSISTANT user model (R37/R39). This secondary overview defers to R6 v3 and the canonical governance rules on any conflict.
