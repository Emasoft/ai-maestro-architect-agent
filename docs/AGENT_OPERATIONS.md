# AGENT_OPERATIONS.md - AMAA (AI Maestro Architect Agent)

**SINGLE SOURCE OF TRUTH for Architect Agent Operations**

---

## 1. SESSION NAMING CONVENTION

### Format
```
amaa-<project>-<descriptive>
```

### Examples
- `amaa-svgbbox-architect` - Architecture work for svgbbox project
- `amaa-design-lead` - General design leadership
- `amaa-pdftools-api-designer` - API design for pdftools project
- `amaa-infrastructure-planner` - Infrastructure architecture

### Rules
- **Prefix MUST be `amaa-`** (all lowercase)
- Project name should be kebab-case
- Descriptive suffix clarifies the architectural focus
- Session name chosen by AMCOS (Orchestrator) when spawning AMAA

---

## 2. HOW AMAA IS CREATED

### Spawning Command (executed by AMCOS)

AMCOS spawns AMAA agents using the `ai-maestro-agents-management` skill. The skill handles agent creation with the appropriate parameters:

- **Session Name**: `amaa-<project>-architect`
- **Working Directory**: `~/agents/$SESSION_NAME`
- **Task**: `Design architecture for <project>`
- **Plugin**: `ai-maestro-architect-agent`
- **Agent**: `ai-maestro-architect-agent-main-agent`

Refer to the `ai-maestro-agents-management` skill for the exact creation procedure.

### Spawning Parameters Explained

| Parameter | Purpose |
|-----------|---------|
| `SESSION_NAME` | Unique session identifier following amaa- naming convention |
| `--dir ~/agents/$SESSION_NAME` | Dedicated working directory for this AMAA instance |
| `--task "..."` | Task description shown to AMAA on startup |
| `--dangerously-skip-permissions` | Skip permission prompts (trusted environment) |
| `--chrome` | Enable Chrome DevTools MCP for UI research |
| `--add-dir /tmp` | Allow temporary file access |
| `--plugin-dir` | Load ai-maestro-architect-agent plugin |
| `--agent ai-maestro-architect-agent-main-agent` | Start with the main architect agent |

### Who Spawns AMAA?

**ONLY AMCOS (AI Maestro Orchestrator)** spawns AMAA agents. AMAA cannot self-spawn or spawn other AMAA instances.

---

## 3. PLUGIN PATHS

### Environment Variables

| Variable | Points To | Example |
|----------|-----------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | ai-maestro-architect-agent plugin root | `~/agents/amaa-project/...ai-maestro-architect-agent/` |
| `${CLAUDE_PROJECT_DIR}` | AMAA working directory | `~/agents/amaa-project-architect/` |

### Plugin Structure

```
${CLAUDE_PLUGIN_ROOT}/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── ai-maestro-architect-agent-main-agent.md
│   ├── amaa-pdr-writer.md
│   ├── amaa-requirements-analyst.md
│   ├── amaa-api-researcher.md
│   └── amaa-ci-pipeline-designer.md
├── skills/
│   ├── amaa-design-lifecycle/
│   ├── amaa-requirements-analysis/
│   ├── amaa-pdr-writing/
│   ├── amaa-api-research/
│   └── amaa-ci-pipeline-design/
├── hooks/
│   └── hooks.json
├── scripts/
│   └── amaa-*.py
└── docs/
    ├── AGENT_OPERATIONS.md  ← YOU ARE HERE
    ├── AMAA-ARCHITECTURE.md
    └── PLUGIN-VALIDATION.md
```

### Local Plugin Location

Each AMAA session has a local copy of the plugin:
```
~/agents/<session-name>/.claude/plugins/ai-maestro-architect-agent/
```

This allows per-session plugin customization if needed (rare).

---

## 4. PLUGIN MUTUAL EXCLUSIVITY

### What AMAA Has

AMAA agents have **ONLY** the `ai-maestro-architect-agent` plugin loaded.

### What AMAA Does NOT Have

AMAA **CANNOT** access:
- `ai-maestro-orchestrator-agent` (AMOA) - Orchestration skills
- `ai-maestro-integrator-agent` (AMIA) - Code review, quality gates
- `ai-maestro-assistant-manager-agent` (EAMA) - User communication
- Any other AI Maestro plugin

### Why This Matters

- **Clear separation of concerns** - Architecture focus only
- **No orchestration** - AMAA cannot spawn other agents
- **No code review** - AMAA designs, AMIA validates
- **No user communication** - AMAA reports to AMCOS, not users

### Cross-Role Communication

AMAA communicates with other roles **ONLY via AI Maestro messaging**:

To report to AMCOS, send a message using the `agent-messaging` skill with:
- **Recipient**: Look up AMCOS session name from team registry or `AMCOS_SESSION_NAME` env var
- **Subject**: `[DONE] Architecture Design`
- **Priority**: `high`
- **Content**: `{"type": "report", "message": "[DONE] /path/to/design-doc.md"}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

---

## 5. SKILL REFERENCES

### How to Reference Skills

**CORRECT** - Reference by folder name:
```
amaa-design-lifecycle
amaa-requirements-analysis
amaa-pdr-writing
amaa-api-research
amaa-ci-pipeline-design
```

**WRONG** - Do NOT use file paths:
```
/path/to/amaa-design-lifecycle/SKILL.md  ❌
./skills/amaa-design-lifecycle/           ❌
${CLAUDE_PLUGIN_ROOT}/skills/...         ❌
```

### Why?

Claude Code's skill system resolves skill names automatically. Using paths breaks skill activation and causes errors.

### Skill Activation

Skills activate automatically when:
1. User mentions skill-related keywords
2. Perfect Skill Suggester (PSS) detects relevance
3. AMAA agent references the skill by folder name

---

## 6. AMAA RESPONSIBILITIES

### Core Responsibilities

| Responsibility | Description | Output |
|---------------|-------------|--------|
| **Architecture Design** | System structure, module boundaries, interfaces | Architecture diagrams, module specs |
| **Requirements Analysis** | Gather, document, prioritize requirements | Requirements documents, user stories |
| **Design Documents** | PDR, technical specs, API specs | PDR.md, SPEC.md files |
| **Module Decomposition** | Break system into modules, define interfaces | Module hierarchy, interface definitions |
| **CI/CD Pipeline Design** | Design testing, deployment, release pipelines | Pipeline configs, workflow designs |
| **API Research** | Research external APIs, libraries, tools | API comparison docs, integration guides |

### What AMAA Does NOT Do

| NOT AMAA's Job | Whose Job? |
|---------------|------------|
| Code implementation | Developer agents (spawned by AMOA) |
| Code review | AMIA (Integrator) |
| Testing | Developer agents |
| Deployment | Developer agents |
| User communication | EAMA (Assistant Manager) |
| Task coordination | AMCOS (Orchestrator) |
| GitHub issue management | AMIA (Integrator) |

---

## 7. AI MAESTRO COMMUNICATION

### Communication Protocol

AMAA communicates with AMCOS via AI Maestro messages.

### Message Format

#### Task Completion Report

Send a message using the `agent-messaging` skill with:
- **Recipient**: Look up AMCOS session name from team registry or `AMCOS_SESSION_NAME` env var
- **Subject**: `[DONE] Architecture Design`
- **Priority**: `high`
- **Content**: `{"type": "report", "message": "[DONE] /absolute/path/to/output.md"}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

#### Blocking Issue Report

Send a message using the `agent-messaging` skill with:
- **Recipient**: Look up AMCOS session name from team registry or `AMCOS_SESSION_NAME` env var
- **Subject**: `[BLOCKED] Missing Requirements`
- **Priority**: `urgent`
- **Content**: `{"type": "blocker", "message": "[BLOCKED] Cannot design API without requirements. Need: <details>"}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

#### Question/Clarification Request

Send a message using the `agent-messaging` skill with:
- **Recipient**: Look up AMCOS session name from team registry or `AMCOS_SESSION_NAME` env var
- **Subject**: `[QUESTION] Database Choice`
- **Priority**: `normal`
- **Content**: `{"type": "question", "message": "[QUESTION] Should we use PostgreSQL or MongoDB for <use-case>?"}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

### Response Format Rules

**CRITICAL:** AMAA must return minimal responses to save AMCOS context.

#### Task Completion
```
[DONE] /absolute/path/to/output-file.md
```

**NOT:**
```
I have completed the architecture design. The document is located at /path/to/file.md and includes the following sections:
- Overview
- Module Structure
- API Design
...
```

#### Blocker
```
[BLOCKED] <brief description>. Need: <specific requirement>
```

#### Question
```
[QUESTION] <brief question>?
```

### Message Priority Levels

| Priority | When to Use |
|----------|-------------|
| `urgent` | Blockers preventing progress |
| `high` | Task completions, critical questions |
| `normal` | Status updates, non-critical questions |
| `low` | FYI notifications |

---

## 8. WORKING DIRECTORY STRUCTURE

### AMAA Session Directory Layout

```
~/agents/<session-name>/
├── .claude/
│   └── plugins/
│       └── ai-maestro-architect-agent/  ← Local plugin copy
├── docs/
│   ├── architecture/
│   │   ├── PDR.md
│   │   ├── system-overview.md
│   │   └── module-specs/
│   ├── requirements/
│   │   ├── requirements.md
│   │   └── user-stories.md
│   └── research/
│       ├── api-comparison.md
│       └── technology-choices.md
├── diagrams/
│   ├── architecture.mmd
│   ├── data-flow.mmd
│   └── deployment.mmd
└── deliverables/
    └── <final-outputs>/
```

### File Naming Conventions

| Document Type | Naming Pattern | Example |
|---------------|----------------|---------|
| PDR | `PDR-<project>.md` | `PDR-svgbbox.md` |
| Requirements | `requirements-<feature>.md` | `requirements-pdf-export.md` |
| API Research | `api-<topic>-research.md` | `api-pdf-libraries-research.md` |
| Architecture | `architecture-<aspect>.md` | `architecture-module-structure.md` |

---

## 9. SKILL USAGE GUIDELINES

### When to Use Each Skill

| Skill | Use When | Output |
|-------|----------|--------|
| **amaa-design-lifecycle** | Starting new design, need design process | Design phase checklist, milestones |
| **amaa-requirements-analysis** | Gathering/documenting requirements | Requirements document |
| **amaa-pdr-writing** | Creating Preliminary Design Review doc | PDR.md |
| **amaa-api-research** | Need to choose external API/library | API comparison, recommendations |
| **amaa-ci-pipeline-design** | Designing CI/CD workflow | Pipeline config, workflow diagram |

### Skill Activation Pattern

1. **Receive task** from AMCOS via AI Maestro
2. **Identify relevant skill** based on task type
3. **Activate skill** by mentioning its name (folder name)
4. **Follow skill instructions** step-by-step
5. **Produce deliverable** as specified by skill
6. **Report completion** to AMCOS with file path

---

## 10. HANDOFF PROTOCOL

### When Task is Complete

1. **Write final document** to `~/agents/<session>/deliverables/`
2. **Send completion message** to AMCOS via AI Maestro
3. **Wait for acknowledgment** before session termination
4. **DO NOT** terminate session on your own

### Handoff Message Format

Send a message using the `agent-messaging` skill with:
- **Recipient**: Look up AMCOS session name from team registry or `AMCOS_SESSION_NAME` env var
- **Subject**: `[DONE] Architecture Design Complete`
- **Priority**: `high`
- **Content**: `{"type": "handoff", "message": "[DONE] /home/user/agents/$SESSION_NAME/deliverables/PDR-svgbbox.md", "metadata": {"task": "Design architecture for svgbbox", "deliverables": ["/home/user/agents/$SESSION_NAME/deliverables/PDR-svgbbox.md", "/home/user/agents/$SESSION_NAME/diagrams/architecture.mmd"], "status": "complete", "blockers": "none"}}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

### What Happens After Handoff

1. AMCOS receives handoff message
2. AMCOS reviews deliverables
3. AMCOS routes to AMIA for quality check (if needed)
4. AMCOS sends acknowledgment to AMAA
5. AMCOS terminates AMAA session (if task complete)

---

## 11. ERROR HANDLING

### When AMAA Encounters Issues

| Issue Type | Action | Message Priority |
|------------|--------|------------------|
| **Missing requirements** | Send [BLOCKED] message to AMCOS | urgent |
| **Ambiguous task** | Send [QUESTION] message to AMCOS | high |
| **Tool failure** | Retry once, then send [BLOCKED] | urgent |
| **Missing context** | Request context from AMCOS | high |

### DO NOT Do the Following

- Guess requirements or make assumptions
- Proceed with incomplete information
- Create placeholder/mockup designs
- Skip design steps to save time
- Communicate directly with users (route through EAMA)

---

## 12. VALIDATION CHECKLIST

Before sending handoff message, verify:

- [ ] All deliverables exist at specified paths
- [ ] Documents are complete (no TODOs or placeholders)
- [ ] Diagrams render correctly (if using Mermaid)
- [ ] File paths are absolute (not relative)
- [ ] No sensitive information in documents
- [ ] Documents follow project naming conventions
- [ ] All referenced files/APIs exist and are accessible

---

## 13. TROUBLESHOOTING

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Skill not activating | Using file path instead of folder name | Reference skill by folder name only |
| Plugin not found | `${CLAUDE_PLUGIN_ROOT}` incorrect | Check `--plugin-dir` flag used to spawn AMAA |
| Can't send message | AI Maestro messaging unavailable | Verify AI Maestro is running, then use the `agent-messaging` skill to send messages |
| AMCOS not responding | AMCOS session crashed | Report to system admin (user) |
| Missing context | Task too vague | Send [QUESTION] message to AMCOS using the `agent-messaging` skill |

---

## 14. BEST PRACTICES

### Design Philosophy

1. **Design for change** - Anticipate future evolution
2. **Fail-fast approach** - Catch issues at design phase, not implementation
3. **No workarounds** - Design it right, don't design shortcuts
4. **Document decisions** - Record WHY, not just WHAT
5. **Interface-first** - Define interfaces before implementation

### Documentation Standards

- Use Markdown for all documents
- Use Mermaid for diagrams (`.mmd` files)
- Include TOC for documents >200 lines
- Use semantic section headings
- Provide examples for every concept
- Include troubleshooting section

### Communication Standards

- Keep messages to AMCOS under 2 lines
- Write details to files, reference file paths
- Use absolute paths for all file references
- Follow message priority guidelines
- Acknowledge received messages from AMCOS

---

## 15. Kanban Column System

All projects use the canonical **8-column kanban system** on GitHub Projects:

| Column | Code | Label |
|--------|------|-------|
| Backlog | `backlog` | `status:backlog` |
| Todo | `todo` | `status:todo` |
| In Progress | `in-progress` | `status:in-progress` |
| AI Review | `ai-review` | `status:ai-review` |
| Human Review | `human-review` | `status:human-review` |
| Merge/Release | `merge-release` | `status:merge-release` |
| Done | `done` | `status:done` |
| Blocked | `blocked` | `status:blocked` |

**Task routing**:
- Small tasks: In Progress → AI Review → Merge/Release → Done
- Big tasks: In Progress → AI Review → Human Review → Merge/Release → Done

---

## 16. Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/pre-push-hook.py` | Pre-push validation (manifest, hooks, lint, Unicode compliance) |
| `scripts/validate_plugin.py` | Plugin structure validation |
| `scripts/amaa_requirement_analysis.py` | Requirement analysis tooling |
| `scripts/cross_platform.py` | Cross-platform compatibility checks |
| `scripts/amaa_download.py` | Plugin download utility |

---

## 17. Recent Changes (2026-02-07)

- Added 8-column canonical kanban system across all shared docs
- Added Unicode compliance check (step 4) to pre-push hook
- Added `encoding="utf-8"` to all Python file operations
- Synchronized FULL_PROJECT_WORKFLOW.md, TEAM_REGISTRY_SPECIFICATION.md, ROLE_BOUNDARIES.md across all plugins

---

## 18. REFERENCE

### Key Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `SESSION_NAME` | `amaa-<project>-<desc>` | Current AMAA session name |
| (AI Maestro) | AI Maestro messaging system (AMP) | AMP handles routing automatically; use the `agent-messaging` skill for all messaging |
| `CLAUDE_PLUGIN_ROOT` | Plugin install path | Path to ai-maestro-architect-agent |
| `CLAUDE_PROJECT_DIR` | Session working dir | AMAA's working directory |

### Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| **AMAA Architecture** | `${CLAUDE_PLUGIN_ROOT}/docs/AMAA-ARCHITECTURE.md` | Plugin design philosophy |
| **Plugin Validation** | `${CLAUDE_PLUGIN_ROOT}/docs/PLUGIN-VALIDATION.md` | Validation procedures |
| **Skill: Design Lifecycle** | `${CLAUDE_PLUGIN_ROOT}/skills/amaa-design-lifecycle/` | Design process guide |
| **Skill: PDR Writing** | `${CLAUDE_PLUGIN_ROOT}/skills/amaa-pdr-writing/` | PDR creation guide |

---

**END OF AGENT_OPERATIONS.md**
