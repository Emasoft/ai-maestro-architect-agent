# Architect Agent (amaa-)

Claude Code role-plugin for the AI Maestro multi-agent ecosystem: the
**ARCHITECT (AMAA)** persona that turns requirements into reviewed,
implementable design documents — requirements analysis, API research,
architecture decisions, module breakdowns, and handoff packages.

**Version**: 2.4.8

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
| `architect-memory-recall` | Symptom-ranked recall over markdown memory notes (memgrep with grep fallback) |
| `architect-memory-write` | Capture one durable, symptom-indexed memory note + index line |

### Hooks

| Hook | Event | Description |
|------|-------|-------------|
| `amaa-stop-check` | Stop | Block exit until all design work is complete |

## Workflow

1. Receives requirements from AMAMA (Manager)
2. Analyzes requirements and creates design documents
3. Breaks work into implementable modules
4. Creates handoff document for AMOA (Orchestrator)
5. Reports completion to AMAMA (Manager)

## Output Artifacts

- Design documents (markdown)
- Module specifications
- API integration plans
- Architecture diagrams (mermaid)
- Handoff files for AMOA (Orchestrator)

## Recommended MCP Servers

The architect agent benefits from these MCP servers when available:

| MCP Server | Purpose |
|------------|---------|
| **LLM Externalizer** (`llm-externalizer`) | Offload file analysis/scanning to external LLMs, saving orchestrator context tokens |
| **Serena MCP** (`serena-mcp`) | Symbol-level code navigation (find definitions, references, overviews) |

The `tldr` CLI tool is also recommended for token-efficient code structure analysis (`tldr structure`, `tldr arch`, `tldr imports`).

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

## Usage

Start a session as the architect:

```bash
claude --agent ai-maestro-architect-agent-main-agent
```

Then drive the planning workflow with the slash commands:

```bash
/amaa-start-planning Build a REST API for inventory management
/amaa-add-requirement REQ "User authentication" --criteria "JWT-based login" --priority high
/amaa-modify-requirement REQ R-001 --status approved
/amaa-remove-requirement REQ R-002
```

The agent produces design documents under `docs_dev/design/`, registers
each one in the design index with a UUID, walks it through the
DRAFT → REVIEW → APPROVED → IMPLEMENTING → COMPLETED → ARCHIVED lifecycle,
and prepares handoff packages for the Orchestrator (AMOA). The `Stop` hook
blocks session exit while draft designs, pending tasks, orphan
requirements, or open architect-assigned GitHub issues remain (capped at 3
blocks per session via `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`).

## Non-Standard Directories

| Directory | Purpose |
|-----------|---------|
| `scripts/git-hooks/` | Pre-push validation hook. Install: `python3 scripts/setup_git_hooks.py` |
| `lib/` | Shared constants, templates, and schemas used across skills and agents |

## Platform Requirements

- **Sync script**: Cross-platform Python script. Requires `gh` CLI authenticated.
- **Python scripts**: Cross-platform. Use `uv run --with pyyaml python <script>` or `python3 <script>`.

## Validation

Whole-plugin validation uses the remote CPV validator (always current,
never vendored):

```bash
uvx cpv-remote-validate plugin . --strict
```
