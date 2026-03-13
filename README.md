# Architect Agent (amaa-)

**Version**: 2.1.0

## Overview

The Architect Agent handles **design documents, requirements analysis, and architecture decisions**. It creates specifications that the Orchestrator uses to coordinate implementation work.

**Prefix**: `amaa-` = AI Maestro Architect Agent

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
| `ai-maestro-architect-agent-main-agent.md` | Main architect agent |
| `amaa-documentation-writer.md` | Creates technical documentation |
| `amaa-api-researcher.md` | Researches APIs and integrations |
| `amaa-modularizer-expert.md` | Breaks work into modules |
| `amaa-planner.md` | Creates implementation plans |
| `amaa-cicd-designer.md` | Designs CI/CD pipelines and workflows |

### Commands

| Command | Description |
|---------|-------------|
| `amaa-start-planning` | Start planning phase |
| `amaa-add-requirement` | Add new requirement |
| `amaa-modify-requirement` | Modify existing requirement |
| `amaa-remove-requirement` | Remove requirement |

### Skills

| Skill | Description |
|-------|-------------|
| `amaa-design-lifecycle` | Design document management |
| `amaa-requirements-analysis` | Requirements patterns |
| `amaa-documentation-writing` | Documentation skills |
| `amaa-api-research` | API research patterns |
| `amaa-planning-patterns` | Planning methodology |
| `amaa-hypothesis-verification` | Test assumptions |
| `amaa-design-communication-patterns` | Shared utilities |
| `amaa-cicd-design` | CI/CD pipeline design patterns |
| `amaa-design-management` | Design document management tools |
| `amaa-github-integration` | GitHub integration patterns |
| `amaa-label-taxonomy` | Label and tagging patterns |
| `amaa-modularization` | Module decomposition patterns |
| `amaa-session-memory` | Session context persistence |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `amaa-stop-check` | Stop | Block exit until all design work is complete |

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

### From Git Repository (recommended)

Install directly from the GitHub repo using the `git-subdir` source type (points to a subdirectory within the repo):

```bash
claude plugin install --source git-subdir --url https://github.com/Emasoft/ai-maestro-architect-agent --scope local
```

After installing, activate changes without restarting:

```bash
/reload-plugins
```

Then start a session with the main agent:

```bash
claude --agent ai-maestro-architect-agent-main-agent
```

### Development Only (--plugin-dir)

`--plugin-dir` loads a plugin directly from a local directory without installation. Use only during plugin development.

```bash
claude --plugin-dir ./ai-maestro-architect-agent
```

## Non-Standard Directories

| Directory | Purpose |
|-----------|---------|
| `scripts/git-hooks/` | Pre-push validation hook. Install: `python3 scripts/setup_git_hooks.py` |
| `lib/` | Shared constants, templates, and schemas used across skills and agents |

## Platform Requirements

- **Sync script** (`scripts/sync_cpv_scripts.py`): Cross-platform Python script. Requires `gh` CLI authenticated.
- **Python scripts**: Cross-platform. Use `uv run --with pyyaml python <script>` or `python3 <script>`.

## Validation

```bash
python3 scripts/validate_plugin.py . --strict --verbose
```
