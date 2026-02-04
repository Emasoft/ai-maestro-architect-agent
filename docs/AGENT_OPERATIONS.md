# AGENT_OPERATIONS.md - EAA (Emasoft Architect Agent)

**SINGLE SOURCE OF TRUTH for Architect Agent Operations**

---

## 1. SESSION NAMING CONVENTION

### Format
```
eaa-<project>-<descriptive>
```

### Examples
- `eaa-svgbbox-architect` - Architecture work for svgbbox project
- `eaa-design-lead` - General design leadership
- `eaa-pdftools-api-designer` - API design for pdftools project
- `eaa-infrastructure-planner` - Infrastructure architecture

### Rules
- **Prefix MUST be `eaa-`** (all lowercase)
- Project name should be kebab-case
- Descriptive suffix clarifies the architectural focus
- Session name chosen by ECOS (Orchestrator) when spawning EAA

---

## 2. HOW EAA IS CREATED

### Spawning Command (executed by ECOS)

```bash
SESSION_NAME="eaa-<project>-architect"

aimaestro-agent.sh create $SESSION_NAME \
  --dir ~/agents/$SESSION_NAME \
  --task "Design architecture for <project>" \
  -- --dangerously-skip-permissions --chrome --add-dir /tmp \
  --plugin-dir ~/agents/$SESSION_NAME/.claude/plugins/emasoft-architect-agent \
  --agent eaa-architect-main-agent
```

### Spawning Parameters Explained

| Parameter | Purpose |
|-----------|---------|
| `SESSION_NAME` | Unique session identifier following eaa- naming convention |
| `--dir ~/agents/$SESSION_NAME` | Dedicated working directory for this EAA instance |
| `--task "..."` | Task description shown to EAA on startup |
| `--dangerously-skip-permissions` | Skip permission prompts (trusted environment) |
| `--chrome` | Enable Chrome DevTools MCP for UI research |
| `--add-dir /tmp` | Allow temporary file access |
| `--plugin-dir` | Load emasoft-architect-agent plugin |
| `--agent eaa-architect-main-agent` | Start with the main architect agent |

### Who Spawns EAA?

**ONLY ECOS (Emasoft Orchestrator)** spawns EAA agents. EAA cannot self-spawn or spawn other EAA instances.

---

## 3. PLUGIN PATHS

### Environment Variables

| Variable | Points To | Example |
|----------|-----------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | emasoft-architect-agent plugin root | `~/agents/eaa-project/...emasoft-architect-agent/` |
| `${CLAUDE_PROJECT_DIR}` | EAA working directory | `~/agents/eaa-project-architect/` |

### Plugin Structure

```
${CLAUDE_PLUGIN_ROOT}/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── eaa-architect-main-agent.md
│   ├── eaa-pdr-writer.md
│   ├── eaa-requirements-analyst.md
│   ├── eaa-api-researcher.md
│   └── eaa-ci-pipeline-designer.md
├── skills/
│   ├── eaa-design-lifecycle/
│   ├── eaa-requirements-analysis/
│   ├── eaa-pdr-writing/
│   ├── eaa-api-research/
│   └── eaa-ci-pipeline-design/
├── hooks/
│   └── hooks.json
├── scripts/
│   └── eaa-*.py
└── docs/
    ├── AGENT_OPERATIONS.md  ← YOU ARE HERE
    ├── EAA-ARCHITECTURE.md
    └── PLUGIN-VALIDATION.md
```

### Local Plugin Location

Each EAA session has a local copy of the plugin:
```
~/agents/<session-name>/.claude/plugins/emasoft-architect-agent/
```

This allows per-session plugin customization if needed (rare).

---

## 4. PLUGIN MUTUAL EXCLUSIVITY

### What EAA Has

EAA agents have **ONLY** the `emasoft-architect-agent` plugin loaded.

### What EAA Does NOT Have

EAA **CANNOT** access:
- `emasoft-orchestrator-agent` (EOA) - Orchestration skills
- `emasoft-integrator-agent` (EIA) - Code review, quality gates
- `emasoft-assistant-manager-agent` (EAMA) - User communication
- Any other Emasoft plugin

### Why This Matters

- **Clear separation of concerns** - Architecture focus only
- **No orchestration** - EAA cannot spawn other agents
- **No code review** - EAA designs, EIA validates
- **No user communication** - EAA reports to ECOS, not users

### Cross-Role Communication

EAA communicates with other roles **ONLY via AI Maestro messaging**:

```bash
# EAA reports to ECOS
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-project-architect",
    "to": "orchestrator-master",
    "subject": "[DONE] Architecture Design",
    "priority": "high",
    "content": {
      "type": "report",
      "message": "[DONE] /path/to/design-doc.md"
    }
  }'
```

---

## 5. SKILL REFERENCES

### How to Reference Skills

**CORRECT** - Reference by folder name:
```
eaa-design-lifecycle
eaa-requirements-analysis
eaa-pdr-writing
eaa-api-research
eaa-ci-pipeline-design
```

**WRONG** - Do NOT use file paths:
```
/path/to/eaa-design-lifecycle/SKILL.md  ❌
./skills/eaa-design-lifecycle/           ❌
${CLAUDE_PLUGIN_ROOT}/skills/...         ❌
```

### Why?

Claude Code's skill system resolves skill names automatically. Using paths breaks skill activation and causes errors.

### Skill Activation

Skills activate automatically when:
1. User mentions skill-related keywords
2. Perfect Skill Suggester (PSS) detects relevance
3. EAA agent references the skill by folder name

---

## 6. EAA RESPONSIBILITIES

### Core Responsibilities

| Responsibility | Description | Output |
|---------------|-------------|--------|
| **Architecture Design** | System structure, module boundaries, interfaces | Architecture diagrams, module specs |
| **Requirements Analysis** | Gather, document, prioritize requirements | Requirements documents, user stories |
| **Design Documents** | PDR, technical specs, API specs | PDR.md, SPEC.md files |
| **Module Decomposition** | Break system into modules, define interfaces | Module hierarchy, interface definitions |
| **CI/CD Pipeline Design** | Design testing, deployment, release pipelines | Pipeline configs, workflow designs |
| **API Research** | Research external APIs, libraries, tools | API comparison docs, integration guides |

### What EAA Does NOT Do

| NOT EAA's Job | Whose Job? |
|---------------|------------|
| Code implementation | Developer agents (spawned by EOA) |
| Code review | EIA (Integrator) |
| Testing | Developer agents |
| Deployment | Developer agents |
| User communication | EAMA (Assistant Manager) |
| Task coordination | ECOS (Orchestrator) |
| GitHub issue management | EIA (Integrator) |

---

## 7. AI MAESTRO COMMUNICATION

### Communication Protocol

EAA communicates with ECOS via AI Maestro messages.

### Message Format

#### Task Completion Report

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-project-architect",
    "to": "orchestrator-master",
    "subject": "[DONE] Architecture Design",
    "priority": "high",
    "content": {
      "type": "report",
      "message": "[DONE] /absolute/path/to/output.md"
    }
  }'
```

#### Blocking Issue Report

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-project-architect",
    "to": "orchestrator-master",
    "subject": "[BLOCKED] Missing Requirements",
    "priority": "urgent",
    "content": {
      "type": "blocker",
      "message": "[BLOCKED] Cannot design API without requirements. Need: <details>"
    }
  }'
```

#### Question/Clarification Request

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-project-architect",
    "to": "orchestrator-master",
    "subject": "[QUESTION] Database Choice",
    "priority": "normal",
    "content": {
      "type": "question",
      "message": "[QUESTION] Should we use PostgreSQL or MongoDB for <use-case>?"
    }
  }'
```

### Response Format Rules

**CRITICAL:** EAA must return minimal responses to save ECOS context.

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

### EAA Session Directory Layout

```
~/agents/<session-name>/
├── .claude/
│   └── plugins/
│       └── emasoft-architect-agent/  ← Local plugin copy
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
| **eaa-design-lifecycle** | Starting new design, need design process | Design phase checklist, milestones |
| **eaa-requirements-analysis** | Gathering/documenting requirements | Requirements document |
| **eaa-pdr-writing** | Creating Preliminary Design Review doc | PDR.md |
| **eaa-api-research** | Need to choose external API/library | API comparison, recommendations |
| **eaa-ci-pipeline-design** | Designing CI/CD workflow | Pipeline config, workflow diagram |

### Skill Activation Pattern

1. **Receive task** from ECOS via AI Maestro
2. **Identify relevant skill** based on task type
3. **Activate skill** by mentioning its name (folder name)
4. **Follow skill instructions** step-by-step
5. **Produce deliverable** as specified by skill
6. **Report completion** to ECOS with file path

---

## 10. HANDOFF PROTOCOL

### When Task is Complete

1. **Write final document** to `~/agents/<session>/deliverables/`
2. **Send completion message** to ECOS via AI Maestro
3. **Wait for acknowledgment** before session termination
4. **DO NOT** terminate session on your own

### Handoff Message Format

```bash
curl -X POST "$AIMAESTRO_API/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'$SESSION_NAME'",
    "to": "orchestrator-master",
    "subject": "[DONE] Architecture Design Complete",
    "priority": "high",
    "content": {
      "type": "handoff",
      "message": "[DONE] /home/user/agents/'$SESSION_NAME'/deliverables/PDR-svgbbox.md",
      "metadata": {
        "task": "Design architecture for svgbbox",
        "deliverables": [
          "/home/user/agents/'$SESSION_NAME'/deliverables/PDR-svgbbox.md",
          "/home/user/agents/'$SESSION_NAME'/diagrams/architecture.mmd"
        ],
        "status": "complete",
        "blockers": "none"
      }
    }
  }'
```

### What Happens After Handoff

1. ECOS receives handoff message
2. ECOS reviews deliverables
3. ECOS routes to EIA for quality check (if needed)
4. ECOS sends acknowledgment to EAA
5. ECOS terminates EAA session (if task complete)

---

## 11. ERROR HANDLING

### When EAA Encounters Issues

| Issue Type | Action | Message Priority |
|------------|--------|------------------|
| **Missing requirements** | Send [BLOCKED] message to ECOS | urgent |
| **Ambiguous task** | Send [QUESTION] message to ECOS | high |
| **Tool failure** | Retry once, then send [BLOCKED] | urgent |
| **Missing context** | Request context from ECOS | high |

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
| Plugin not found | `${CLAUDE_PLUGIN_ROOT}` incorrect | Check `--plugin-dir` flag used to spawn EAA |
| Can't send message | AIMAESTRO_API not set | Use `http://localhost:23000` as default |
| ECOS not responding | ECOS session crashed | Report to system admin (user) |
| Missing context | Task too vague | Send [QUESTION] message to ECOS |

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

- Keep messages to ECOS under 2 lines
- Write details to files, reference file paths
- Use absolute paths for all file references
- Follow message priority guidelines
- Acknowledge received messages from ECOS

---

## 15. REFERENCE

### Key Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `SESSION_NAME` | `eaa-<project>-<desc>` | Current EAA session name |
| `AIMAESTRO_API` | `http://localhost:23000` | AI Maestro API endpoint |
| `CLAUDE_PLUGIN_ROOT` | Plugin install path | Path to emasoft-architect-agent |
| `CLAUDE_PROJECT_DIR` | Session working dir | EAA's working directory |

### Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| **EAA Architecture** | `${CLAUDE_PLUGIN_ROOT}/docs/EAA-ARCHITECTURE.md` | Plugin design philosophy |
| **Plugin Validation** | `${CLAUDE_PLUGIN_ROOT}/docs/PLUGIN-VALIDATION.md` | Validation procedures |
| **Skill: Design Lifecycle** | `${CLAUDE_PLUGIN_ROOT}/skills/eaa-design-lifecycle/` | Design process guide |
| **Skill: PDR Writing** | `${CLAUDE_PLUGIN_ROOT}/skills/eaa-pdr-writing/` | PDR creation guide |

---

**END OF AGENT_OPERATIONS.md**
