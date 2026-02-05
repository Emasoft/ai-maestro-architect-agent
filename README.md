# Architect Agent (eaa-)

**Version**: 1.0.0

## Overview

The Architect Agent handles **design documents, requirements analysis, and architecture decisions**. It creates specifications that the Orchestrator uses to coordinate implementation work.

**Prefix**: `eaa-` = Emasoft Architect Agent

## Core Responsibilities

1. **Requirements Analysis**: Gather and document requirements
2. **Design Documents**: Create technical specifications and architecture docs
3. **API Research**: Investigate APIs and integration points
4. **Planning**: Break down work into implementable modules
5. **Hypothesis Verification**: Test assumptions before committing to design

## Components

### Agents

| Agent | Description |
|-------|-------------|
| `eaa-architect-main-agent.md` | Main architect agent |
| `eaa-documentation-writer.md` | Creates technical documentation |
| `eaa-api-researcher.md` | Researches APIs and integrations |
| `eaa-modularizer-expert.md` | Breaks work into modules |
| `eaa-planner.md` | Creates implementation plans |
| `eaa-cicd-designer.md` | Designs CI/CD pipelines and workflows |

### Commands

| Command | Description |
|---------|-------------|
| `eaa-start-planning` | Start planning phase |
| `eaa-add-requirement` | Add new requirement |
| `eaa-modify-requirement` | Modify existing requirement |
| `eaa-remove-requirement` | Remove requirement |

### Skills

| Skill | Description |
|-------|-------------|
| `eaa-design-lifecycle` | Design document management |
| `eaa-requirements-analysis` | Requirements patterns |
| `eaa-documentation-writing` | Documentation skills |
| `eaa-api-research` | API research patterns |
| `eaa-planning-patterns` | Planning methodology |
| `eaa-hypothesis-verification` | Test assumptions |
| `eaa-design-communication-patterns` | Shared utilities |
| `eaa-cicd-design` | CI/CD pipeline design patterns |
| `eaa-design-management` | Design document management tools |
| `eaa-github-integration` | GitHub integration patterns |
| `eaa-label-taxonomy` | Label and tagging patterns |
| `eaa-modularization` | Module decomposition patterns |
| `eaa-session-memory` | Session context persistence |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `eaa-skill-activation` | UserPromptSubmit | Activate relevant design skills |

## Workflow

1. Receives requirements from Assistant Manager
2. Analyzes requirements and creates design documents
3. Breaks work into implementable modules
4. Creates handoff document for Orchestrator
5. Reports completion to Assistant Manager

## Output Artifacts

- Design documents (markdown)
- Module specifications
- API integration plans
- Architecture diagrams (mermaid)
- Handoff files for Orchestrator

## Installation

```bash
claude --plugin-dir ./OUTPUT_SKILLS/architect-agent
```

## Validation

```bash
cd OUTPUT_SKILLS/architect-agent
uv run python scripts/eaa_validate_plugin.py --verbose
```
