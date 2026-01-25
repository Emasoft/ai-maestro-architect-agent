# Architect Agent (arch-)

**Version**: 1.0.0

## Overview

The Architect Agent handles **design documents, requirements analysis, and architecture decisions**. It creates specifications that the Orchestrator uses to coordinate implementation work.

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
| `arch-main.md` | Main architect agent |
| `arch-documentation-writer.md` | Creates technical documentation |
| `arch-api-researcher.md` | Researches APIs and integrations |
| `arch-modularizer-expert.md` | Breaks work into modules |
| `arch-planner.md` | Creates implementation plans |

### Commands

| Command | Description |
|---------|-------------|
| `arch-start-planning` | Start planning phase |
| `arch-add-requirement` | Add new requirement |
| `arch-modify-requirement` | Modify existing requirement |
| `arch-remove-requirement` | Remove requirement |

### Skills

| Skill | Description |
|-------|-------------|
| `arch-design-lifecycle` | Design document management |
| `arch-requirements-analysis` | Requirements patterns |
| `arch-documentation-writing` | Documentation skills |
| `arch-api-research` | API research patterns |
| `arch-planning-patterns` | Planning methodology |
| `arch-hypothesis-verification` | Test assumptions |
| `arch-shared` | Shared utilities |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `arch-skill-activation` | UserPromptSubmit | Activate relevant design skills |

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
uv run python scripts/arch_validate_plugin.py --verbose
```
