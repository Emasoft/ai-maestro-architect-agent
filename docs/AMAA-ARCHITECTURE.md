# AMAA-ARCHITECTURE.md - Plugin Design Philosophy

> **Note**: The authoritative source for the communication model is **R6 v3**
> as encoded in this plugin's main agent
> (`agents/ai-maestro-architect-agent-main-agent.md` -> *Communication
> Permissions*) and `~/.claude/rules/`; the authoritative task-pipeline model
> is the **v2 `column:` schema** in `skills/amaa-prrd-trdd-kanban/SKILL.md`.
> Where this document disagrees with those, **they win.**

**Why the ai-maestro-architect-agent plugin is shaped the way it is** — what
single problem the **ARCHITECT (AMAA)** role-plugin solves, how its components
are split, and where it sits in the AI Maestro ecosystem. Companion to
`AGENT_OPERATIONS.md` (operations) and `PLUGIN-VALIDATION.md` (validation).

---

## 1. Single Responsibility

The ARCHITECT does exactly one thing, end to end:

> **requirements -> reviewed design documents -> handoff.**

Everything in the plugin exists to serve that pipeline and nothing else. AMAA
gathers and clarifies requirements, researches the APIs a design depends on,
makes and records architecture decisions, breaks the system into independently
implementable modules, and packages the result as an unambiguous handoff for
the Orchestrator (AMOA) to turn into tasks.

What AMAA deliberately does **NOT** do is just as important as what it does:

| NOT AMAA's job | Owner |
|----------------|-------|
| Code implementation | Developer agents (spawned by AMOA) |
| Code review / quality gates | AMIA (Integrator) |
| Task assignment / kanban | AMOA (Orchestrator) |
| Agent lifecycle / team config | AMCOS (Chief of Staff) |
| User communication | AMAMA (Manager) |

This narrow charter is what keeps the plugin small and its outputs trustworthy.
A design AMAA hands off carries no `[TBD]` markers, no placeholders, and a
rationale for every decision — because producing that artifact is the *whole*
job, not a side effect of something else.

---

## 2. Thin Agent, Rich Skill

The plugin follows a strict **thin-agent / rich-skill** split — the single most
important structural decision it makes.

- **Agents orchestrate. Skills carry knowledge.** The main agent
  (`ai-maestro-architect-agent-main-agent`) is a short orchestration layer: it
  decides *which* skill to load and *which* sub-agent to route to, then gets out
  of the way — it does not inline procedures, templates, or judgment rules.
- **Sub-agents are specialists.** Five sub-agents each own one slice of the
  pipeline and are routed to by category:

  | Task category | Sub-agent |
  |---------------|-----------|
  | Requirements planning | `amaa-planner` |
  | API research | `amaa-api-researcher` |
  | Module breakdown | `amaa-modularizer-expert` |
  | CI/CD pipeline design | `amaa-cicd-designer` |
  | Documentation writing | `amaa-documentation-writer` |

  A sub-agent gets its own context window, does its bounded unit of work, and
  returns a one-line result plus a report file path — never code blocks or
  verbose prose back into the main agent's context.

### The base + `-ops` skill pairing

Each of the 14 base skills ships with an `-ops` companion. The split is a
**progressive-discovery** technique that keeps the always-loaded surface small:

- **Base skill** (e.g. `amaa-design-lifecycle`) — the *what* and *when*: the
  core concept, the checklist, the state model, and an index of reference
  files. This is what an agent loads first to understand the domain.
- **`-ops` skill** (e.g. `amaa-design-lifecycle-ops`) — the *how*: the
  operational quick-reference for that domain — judgment guidelines, success
  criteria, troubleshooting, exact templates, and handoff formats. Loaded only
  when the agent actually needs to *perform* the operation.

The 14 base skills are: `amaa-api-research`, `amaa-cicd-design`,
`amaa-design-communication-patterns`, `amaa-design-lifecycle`,
`amaa-design-management`, `amaa-documentation-writing`,
`amaa-github-integration`, `amaa-hypothesis-verification`,
`amaa-label-taxonomy`, `amaa-modularization`, `amaa-planning-patterns`,
`amaa-prrd-trdd-kanban`, `amaa-requirements-analysis`, `amaa-session-memory` —
each with its `-ops` twin. Two further skills, `architect-memory-recall` and
`architect-memory-write`, give AMAA a durable, symptom-indexed markdown memory
(recall before acting; write decisions, not artifacts).

Deeper material that even an `-ops` skill would bloat lives one level further
down in each skill's `references/` and `templates/` directories, linked from
the SKILL.md rather than inlined. The net effect: the main agent's working
context stays lean, and detail is pulled in on demand exactly when needed.

---

## 3. Single-Writer-Per-Domain

Every mutable surface in a project has **exactly one owner**. AMAA owns the
**design surface only** — design documents, the design state machine, and TRDD
shaping for its slice. Other roles *read* those artifacts; they never edit them.

This is what prevents two agents (or two ARCHITECTs) from silently clobbering
each other's work:

- **AMAA writes the design; everyone else reads it.** When a MEMBER surfaces a
  design problem mid-implementation, it does not edit the design — it comes back
  to AMAA (relayed by ORCH) and AMAA revises (see the redesign loop in §5).
- **A task needing a domain AMAA does not own must delegate or claim it.** AMAA
  never reaches across an ownership boundary to edit code, CI, or another team's
  surface on assumption — it hands the need to that domain's owner or claims it
  explicitly first.
- **Multi-ARCH coordination partitions the design surface up front.** When more
  than one ARCHITECT works the same project, each owns disjoint TRDDs / modules
  / design files; ARCHITECT peers do not message each other directly — ORCH
  assigns the non-overlapping slices.

---

## 4. R6 v3 Placement in the Ecosystem

AMAA is a **team-internal, project-linked** role. Its position in the R6 v3
communication graph is enforced at the AI Maestro API — forbidden edges return
HTTP 403 with a routing suggestion, so the placement below is not advisory, it
is the actual topology.

```
                        AMAMA (Manager) ── governance layer
                          |
                          | (reaches the team ONLY via AMCOS)
                          v
                        AMCOS (Chief of Staff) ── the team boundary
                          |
            work intake / |  ^ completion reporting
                          v  |
                    >>>  AMAA (Architect — YOU)  <<<
                          |
                          | direct AMAA -> AMOA edge
                          v   (design handoffs only)
                        AMOA (Orchestrator)
```

The load-bearing facts:

- **AMCOS is the team boundary.** Work intake *and* completion reporting flow
  through the Chief of Staff. AMAA receives requirements from AMCOS and reports
  done to AMCOS.
- **MANAGER (AMAMA) reaches team-internal agents only via AMCOS.** AMAA may not
  message MANAGER directly — every governance / cross-team / release proposal it
  cannot self-authorize routes up the ladder **Tier 0 -> AMCOS -> MANAGER ->
  USER**.
- **A direct AMAA -> AMOA edge exists for design handoffs.** Once a design is
  approved, AMAA hands it straight to the Orchestrator (the one cross-role edge
  AMAA may initiate besides AMCOS).
- **ARCHITECT peers route through ORCHESTRATOR.** AMAA never reaches another
  ARCHITECT, INTEGRATOR, or MEMBER directly; ORCH is the routing point.
- **The user is reply-only.** AMAA may reply once to a prior user message but
  may never proactively initiate user contact — only governance titles can.

---

## 5. The Design State Machine

AMAA's design artifacts run a six-state lifecycle, owned and enforced by the
`amaa-design-lifecycle` skill:

```
DRAFT -> REVIEW -> APPROVED -> IMPLEMENTING -> COMPLETED -> ARCHIVED
                     ^                |
                     |                |
                     +----------------+
                   the redesign loop
              (IMPLEMENTING -> REVIEW)
```

| State | Meaning | Forward transition |
|-------|---------|--------------------|
| DRAFT | Initial creation | -> REVIEW |
| REVIEW | Under review | -> APPROVED (or -> DRAFT to revise) |
| APPROVED | Ready for implementation | -> IMPLEMENTING |
| IMPLEMENTING | Being implemented | -> COMPLETED, or -> REVIEW (redesign) |
| COMPLETED | Fully implemented | -> ARCHIVED |
| ARCHIVED | Historical reference | (terminal) |

### The redesign loop

`IMPLEMENTING -> REVIEW` is the **redesign loop** — the re-entry edge that makes
the machine more than a one-way street. It exists so that when a design flaw is
discovered *after* implementation has started (during the task-comprehension
handshake, an in-dev issue dialog, or the pre-PR gate), the ARCHITECT can pull
the design back into REVIEW, revise it (or split / group it into new TRDDs), and
re-approve — instead of letting the team silently improvise around the flaw.

Who triggers it: a MEMBER surfaces the issue, ORCH relays it to AMAA (within-team
ORCH<->ARCH is a direct edge), and AMAA decides whether it is a genuine design
flaw (re-enter REVIEW) or just an implementation question (answer in the dialog,
no state change). Without this edge, the dialog loops would have nowhere to send
a surfaced design problem.

> This design-artifact state machine is **distinct** from the project-wide
> per-TRDD `proposal -> planned` approval gate (`design/proposals/` vs
> `design/tasks/`): one governs an individual design document, the other
> whether a task is authorized to execute at all.

---

## 6. Integration With AI Maestro

The plugin is one role in a larger system; its integration points are narrow and
explicit:

- **AMCOS intake.** A design job begins when AMCOS routes requirements to AMAA
  (R6 v3 — AMCOS guards the team boundary). AMAA acknowledges, analyzes, and
  begins design. This is the *only* sanctioned intake path.
- **The v2 column model.** Within the TRDD kanban, AMAA owns the **`design`**
  column — the only column that supports a **1->N split** (decompose one
  proto-TRDD into many full TRDDs) or an **N->1 group** (merge several into one).
  When a TRDD is fully shaped, AMAA moves it to **`dispatch`**, where ORCH picks
  it up for assignment.
- **AMOA handoff.** The terminal output of a design is a handoff package
  delivered straight to the Orchestrator over the direct AMAA -> AMOA edge.
  After handoff, AMAA reports completion back to AMCOS and waits for
  acknowledgment — it does not self-terminate.
- **Stop-hook enforcement.** The `amaa-stop-check` Stop hook
  (`scripts/amaa_stop_check.py`) blocks session exit while draft designs,
  pending tasks, orphan requirements, or open architect-assigned GitHub issues
  remain — so a session cannot quietly end with the design pipeline half-done
  (capped at 3 blocks per session via `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`).

The result: a plugin that does one job well, keeps its knowledge in skills
rather than its agent, never writes outside the surface it owns, and plugs into
the AI Maestro graph through exactly two doors — AMCOS for intake/reporting and
AMOA for handoff.
