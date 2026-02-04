# Team Registry Specification

**Version**: 1.0.0
**Last Updated**: 2026-02-03

This document specifies the format and location of team registries, agent contacts, and naming conventions.

---

## Overview

Every project team maintains a **Team Registry** file that contains:
- Team identification
- Agent roster with contact details
- Role assignments
- Communication addresses

This file is **git-tracked** and stored in the repository, ensuring all team members have access.

---

## File Location

```
<repository-root>/
└── .emasoft/
    └── team-registry.json
```

**Why `.emasoft/`**: This directory contains all Emasoft agent system configuration for the project.

---

## Team Naming Convention

### Format

```
<repo-name>-<project-type>-team
```

### Components

| Component | Description | Examples |
|-----------|-------------|----------|
| `repo-name` | GitHub repository name (lowercase, hyphens) | `svgbbox`, `ai-maestro`, `myapp` |
| `project-type` | Descriptive keyword for the project type | `library`, `webapp`, `api`, `cli`, `mobile` |
| `team` | Literal suffix to identify as team name | `team` |

### Examples

| Repository | Project Type | Team Name |
|------------|--------------|-----------|
| `svgbbox` | Library | `svgbbox-library-team` |
| `ai-maestro` | Backend API | `ai-maestro-api-team` |
| `my-mobile-app` | Mobile App | `my-mobile-app-mobile-team` |
| `company-website` | Web App | `company-website-webapp-team` |

### Uniqueness Requirement

Team names must be **globally unique** across all projects managed by ECOS. ECOS maintains a master list of all team names to prevent collisions.

---

## Team Registry Format (team-registry.json)

```json
{
  "$schema": "https://emasoft.github.io/schemas/team-registry.v1.json",
  "version": "1.0.0",
  "team": {
    "name": "svgbbox-library-team",
    "project": {
      "repository": "https://github.com/Emasoft/svgbbox",
      "github_project": "https://github.com/orgs/Emasoft/projects/12",
      "created_by": "eama-assistant-manager",
      "created_at": "2026-02-03T10:00:00Z"
    },
    "created_by": "ecos-chief-of-staff",
    "created_at": "2026-02-03T10:30:00Z"
  },
  "agents": [
    {
      "name": "svgbbox-orchestrator",
      "role": "orchestrator",
      "plugin": "emasoft-orchestrator-agent",
      "host": "macbook-dev-01",
      "ai_maestro_address": "svgbbox-orchestrator",
      "status": "active",
      "assigned_at": "2026-02-03T10:30:00Z"
    },
    {
      "name": "svgbbox-architect",
      "role": "architect",
      "plugin": "emasoft-architect-agent",
      "host": "macbook-dev-01",
      "ai_maestro_address": "svgbbox-architect",
      "status": "active",
      "assigned_at": "2026-02-03T10:30:00Z"
    },
    {
      "name": "svgbbox-impl-01",
      "role": "implementer",
      "plugin": "emasoft-implementer-agent",
      "host": "macbook-dev-01",
      "ai_maestro_address": "svgbbox-impl-01",
      "status": "active",
      "assigned_at": "2026-02-03T10:35:00Z"
    },
    {
      "name": "svgbbox-impl-02",
      "role": "implementer",
      "plugin": "emasoft-implementer-agent",
      "host": "macbook-dev-02",
      "ai_maestro_address": "svgbbox-impl-02",
      "status": "active",
      "assigned_at": "2026-02-03T10:35:00Z"
    },
    {
      "name": "svgbbox-tester-01",
      "role": "tester",
      "plugin": "emasoft-tester-agent",
      "host": "macbook-dev-01",
      "ai_maestro_address": "svgbbox-tester-01",
      "status": "active",
      "assigned_at": "2026-02-03T10:40:00Z"
    }
  ],
  "shared_agents": [
    {
      "name": "emasoft-integrator",
      "role": "integrator",
      "plugin": "emasoft-integrator-agent",
      "host": "server-ci-01",
      "ai_maestro_address": "emasoft-integrator",
      "note": "Shared across multiple teams"
    }
  ],
  "organization_agents": [
    {
      "name": "eama-assistant-manager",
      "role": "manager",
      "plugin": "emasoft-assistant-manager-agent",
      "host": "macbook-main",
      "ai_maestro_address": "eama-assistant-manager",
      "note": "Organization-wide, not team-specific"
    },
    {
      "name": "ecos-chief-of-staff",
      "role": "chief-of-staff",
      "plugin": "emasoft-chief-of-staff",
      "host": "macbook-main",
      "ai_maestro_address": "ecos-chief-of-staff",
      "note": "Organization-wide, not team-specific"
    }
  ],
  "github_bot": {
    "username": "emasoft-bot",
    "type": "shared-bot-account",
    "note": "All GitHub operations use this account. Real agent identity tracked in commit messages and PR bodies."
  },
  "contacts_last_updated": "2026-02-03T10:45:00Z",
  "contacts_updated_by": "ecos-chief-of-staff"
}
```

---

## Field Definitions

### Team Section

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique team name (format: `<repo>-<type>-team`) |
| `project.repository` | string | Yes | GitHub repository URL |
| `project.github_project` | string | No | GitHub Projects board URL |
| `project.created_by` | string | Yes | Agent that created the project |
| `project.created_at` | ISO8601 | Yes | Project creation timestamp |
| `created_by` | string | Yes | Agent that created the team (always ECOS) |
| `created_at` | ISO8601 | Yes | Team creation timestamp |

### Agent Entry

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique agent name |
| `role` | string | Yes | Agent role (see Role Types below) |
| `plugin` | string | Yes | Plugin name the agent uses |
| `host` | string | Yes | Host machine identifier |
| `ai_maestro_address` | string | Yes | Address for AI Maestro messaging |
| `status` | string | Yes | `active`, `hibernated`, `offline`, `terminated` |
| `assigned_at` | ISO8601 | Yes | When agent was assigned to team |
| `note` | string | No | Optional notes |

### Role Types

| Role | Plugin | Count per Team | Description |
|------|--------|----------------|-------------|
| `manager` | emasoft-assistant-manager-agent | 0 (org-wide) | User interface, approvals |
| `chief-of-staff` | emasoft-chief-of-staff | 0 (org-wide) | Agent lifecycle |
| `orchestrator` | emasoft-orchestrator-agent | **Exactly 1** | Task management, kanban |
| `architect` | emasoft-architect-agent | **Exactly 1** | Design documents |
| `integrator` | emasoft-integrator-agent | 1+ (can be shared) | PR review, merge |
| `implementer` | emasoft-implementer-agent | 1+ | Code implementation |
| `tester` | emasoft-tester-agent | 0+ | Testing, QA |
| `devops` | emasoft-devops-agent | 0+ | CI/CD, deployment |

---

## Agent Naming Convention

### Format

```
<team-prefix>-<role>[-<instance>]
```

### Components

| Component | Description | Examples |
|-----------|-------------|----------|
| `team-prefix` | Short form of repo name | `svgbbox`, `maestro`, `myapp` |
| `role` | Agent role identifier | `orchestrator`, `architect`, `impl`, `tester` |
| `instance` | Instance number (for multiple same-role agents) | `01`, `02`, `03` |

### Examples

| Team | Role | Instance | Agent Name |
|------|------|----------|------------|
| svgbbox-library-team | orchestrator | - | `svgbbox-orchestrator` |
| svgbbox-library-team | architect | - | `svgbbox-architect` |
| svgbbox-library-team | implementer | 1 | `svgbbox-impl-01` |
| svgbbox-library-team | implementer | 2 | `svgbbox-impl-02` |
| ai-maestro-api-team | tester | 1 | `maestro-tester-01` |

### Organization-Wide Agents (No Team Prefix)

| Agent | Name |
|-------|------|
| Manager | `eama-assistant-manager` |
| Chief of Staff | `ecos-chief-of-staff` |
| Shared Integrator | `emasoft-integrator` |

---

## How to Send Messages

Every agent can look up contact information from `team-registry.json`:

```python
import json

def get_agent_address(agent_name: str, registry_path: str = ".emasoft/team-registry.json") -> str:
    """Get AI Maestro address for an agent."""
    with open(registry_path) as f:
        registry = json.load(f)

    # Check team agents
    for agent in registry["agents"]:
        if agent["name"] == agent_name:
            return agent["ai_maestro_address"]

    # Check shared agents
    for agent in registry.get("shared_agents", []):
        if agent["name"] == agent_name:
            return agent["ai_maestro_address"]

    # Check organization agents
    for agent in registry.get("organization_agents", []):
        if agent["name"] == agent_name:
            return agent["ai_maestro_address"]

    raise ValueError(f"Agent not found: {agent_name}")

# Example: Send message to orchestrator
address = get_agent_address("svgbbox-orchestrator")
# Returns: "svgbbox-orchestrator"

# Use in curl:
# curl -X POST "http://localhost:23000/api/messages" \
#   -d '{"to": "svgbbox-orchestrator", ...}'
```

---

## Message Format with Agent Identity

All AI Maestro messages must include full agent identity:

```json
{
  "from": "svgbbox-impl-01",
  "to": "svgbbox-orchestrator",
  "subject": "[PROGRESS] Task #42: Login fix 80% complete",
  "priority": "normal",
  "content": {
    "type": "progress-report",
    "message": "Login fix implementation 80% complete. Running tests now.",
    "sender_identity": {
      "name": "svgbbox-impl-01",
      "role": "implementer",
      "plugin": "emasoft-implementer-agent",
      "host": "macbook-dev-01",
      "team": "svgbbox-library-team"
    },
    "task_reference": {
      "issue_number": 42,
      "issue_url": "https://github.com/Emasoft/svgbbox/issues/42"
    }
  }
}
```

---

## Git Commit Message Format

To track which agent made each commit:

```
Fix login validation bug

- Added email format validation
- Fixed password length check
- Added unit tests

Agent: svgbbox-impl-01
Role: implementer
Plugin: emasoft-implementer-agent
Host: macbook-dev-01
Team: svgbbox-library-team
GitHub-Bot: emasoft-bot
```

---

## PR Body Format

```markdown
## Summary
Fix login validation bug

## Changes
- Added email format validation
- Fixed password length check
- Added unit tests

## Testing
- [x] Unit tests pass
- [x] Integration tests pass

---
**Agent Identity**
| Field | Value |
|-------|-------|
| Agent | svgbbox-impl-01 |
| Role | implementer |
| Plugin | emasoft-implementer-agent |
| Host | macbook-dev-01 |
| Team | svgbbox-library-team |

*PR created via emasoft-bot (shared GitHub account)*
```

---

## ECOS Responsibilities for Team Registry

1. **Create team-registry.json** when creating a new team
2. **Add agents** to the registry when assigning to team
3. **Update status** when agents hibernate/wake/terminate
4. **Commit and push** registry changes to GitHub
5. **Notify all team agents** when registry changes

### Registry Update Message

When ECOS updates the registry, it sends:

```json
{
  "from": "ecos-chief-of-staff",
  "to": "<all-team-agents>",
  "subject": "[REGISTRY UPDATE] Team contacts updated",
  "priority": "normal",
  "content": {
    "type": "registry-update",
    "message": "Team registry has been updated. Please pull latest changes.",
    "changes": [
      {"action": "added", "agent": "svgbbox-impl-03"},
      {"action": "status_change", "agent": "svgbbox-impl-02", "new_status": "hibernated"}
    ],
    "registry_commit": "abc123"
  }
}
```

---

## Validation Rules

1. **Team name must be unique** across all projects
2. **Agent name must be unique** within the team
3. **Exactly one orchestrator** per team
4. **Exactly one architect** per team
5. **At least one implementer** per team
6. **All agents must have valid AI Maestro addresses**
7. **Organization agents cannot be assigned to teams**

---

## Quick Reference: Who to Message

| When I need to... | Message this agent | Address lookup |
|-------------------|--------------------|----------------|
| Report task progress | Orchestrator | `registry.agents[role=orchestrator]` |
| Ask design questions | Architect | `registry.agents[role=architect]` |
| Submit PR for review | Integrator | `registry.shared_agents[role=integrator]` |
| Request approval | Manager | `registry.organization_agents[role=manager]` |
| Report agent issues | Chief of Staff | `registry.organization_agents[role=chief-of-staff]` |
| Message teammate | By name | `registry.agents[name=<name>]` |

---

**This specification must be followed by all agents. Deviations require Manager approval.**
