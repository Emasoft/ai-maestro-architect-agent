---
name: architecture
description: "how does ai-maestro-architect-agent (AMAA) work — the ARCHITECT role plugin: overview, the main parts (agents, skills, design pipeline, hooks), where the key pieces live"
ocd: 2026-06-16
lmd: 2026-06-16
metadata:
  node_type: memory
  type: project
  tier: hub
  functionality: architecture
  globs: ["agents/**", "skills/**", "scripts/**", "commands/**", "hooks/**", "lib/**"]
---
ai-maestro-architect-agent (AMAA) is the **ARCHITECT** role plugin of the AI Maestro fleet: one architect per project, owning technical architecture design, requirements analysis, API research, the design-document lifecycle, and complete implementation handoffs to the orchestrator. It does not write production code — it produces specifications and design artifacts.

## Parts map
- **agents/** — the main agent (`ai-maestro-architect-agent-main-agent`) + LOCAL HELPER sub-agents (documentation-writer, modularizer-expert, planner, api-researcher, cicd-designer). Sub-agents are AMP-restricted (only the main agent messages other agents).
- **skills/** — the `amaa-*` capability skills: design-lifecycle, design-management, requirements-analysis, planning-patterns, cicd-design, hypothesis-verification, github-integration, session-memory (transcript/session restore — distinct from the wiki memory). The design state machine + redesign loop live in `scripts/amaa_design_lifecycle.py`.
- **design/** — the 3-pillars artifacts: `requirements/PRRD.md` (project rules) + the 4 kanban zones `tasks/ proposals/ refused/ archived/`.
- **hooks/** — a `Stop` hook (`scripts/amaa_stop_check.py`) that blocks exit until design work is complete (modern `args` exec form).
- **scripts/** — the design/lifecycle/github/publish tooling; `publish.py` is the CPV-canonical strict pipeline (no-skip, process-ancestry pre-push guard).
- Memory: AMAA uses the GLOBAL janitor memory system (see the project `CLAUDE.md` "## Memory"); it ships NO per-plugin memory-recall/write skills.

## Applies to
- (component/aspect pages radiate here as written — wire the reciprocal `## Governed by` on each)

## See also
- (lateral links to other functionality hubs, once they exist)

## Notes and lessons learned
