---
name: architecture
description: "how does ai-maestro-architect-agent (AMAA) work — the ARCHITECT role plugin: overview, the main parts (agents, skills, design pipeline, hooks), where the key pieces live"
ocd: 2026-06-16
lmd: 2026-06-22
metadata:
  node_type: memory
  type: project
  tier: hub
  functionality: architecture
  globs: ["agents/**", "skills/**", "scripts/**", "commands/**", "hooks/**", "lib/**"]
---
ai-maestro-architect-agent (AMAA) is the **ARCHITECT** role plugin of the AI Maestro fleet: one architect per project, owning technical architecture design, requirements analysis, API research, the design-document lifecycle, and complete implementation handoffs to the orchestrator. It does not write production code — it produces specifications and design artifacts.

## Parts map
- **agents/** — the main agent (`ai-maestro-architect-agent-main-agent`) + LOCAL HELPER sub-agents (documentation-writer, modularizer-expert, planner, api-researcher, cicd-designer). Sub-agents are AMP-restricted (only the main agent messages other agents). Each agent's `model:` is a **deliberate alias** (`opus`; `sonnet` for the cheaper planner) — not a pinned deprecated model ID.[^1]
- **skills/** — the `amaa-*` capability skills: design-lifecycle, design-management, requirements-analysis, planning-patterns, cicd-design, hypothesis-verification, github-integration, session-memory (transcript/session restore — distinct from the wiki memory). The design state machine + redesign loop live in `scripts/amaa_design_lifecycle.py`.
- **design/** — the 3-pillars artifacts: `requirements/PRRD.md` (project rules) + the 4 kanban zones `tasks/ proposals/ refused/ archived/`.
- **hooks/** — a `Stop` hook (`scripts/amaa_stop_check.py`) that blocks exit until design work is complete (modern `args` exec form).
- **scripts/** — the design/lifecycle/github/publish tooling; `publish.py` is the CPV-canonical strict pipeline (no-skip, process-ancestry pre-push guard). This plugin is the CPV **`remote-validation` profile** (de-vendored validators, drives the remote `cpv-remote-validate --strict` gate); `plugin.json` declares its by-design canon divergences via `cpv.pipeline.intentional_divergence` — **never run CPV `--force-templates` here, it damages the profile.**[^2]
- Memory: AMAA uses the GLOBAL janitor memory system (see the project `CLAUDE.md` "## Memory"); it ships NO per-plugin memory-recall/write skills.

## Applies to
- [[decouple-api-to-cli]] — skills call the frozen CLI verbs (`amp-*`, `aimaestro-*.sh`), never raw `/api/*` routes.

## See also
- (lateral links to other functionality hubs, once they exist)

## Notes and lessons learned
[^1]: [ocd:2026-06-20 lmd:2026-06-20] Claude Code changelog audit (through **2.1.183**) vs this plugin (2026-06-20): **NO required update.** The 6 agent `model:` fields are bare aliases (`opus` ×5, `sonnet` ×1) that auto-resolve to the current generation — NOT pinned deprecated IDs — so the 2.1.183 "deprecated/auto-updated model" warning (which targets pinned *old* IDs in agent frontmatter) does not apply, and a "CPV best-practice: omit `model:`" or "changelog update" pass must NOT strip them: doing so would silently change each sub-agent's model tier (the planner is on `sonnet` on purpose, for cheaper planning). Also verified current: `hooks/hooks.json` is the modern Stop-only `args`-exec form whose `amaa_stop_check.py` reads stdin JSON (the live hook contract); no `.mcp.json` is shipped (MCP-config changelog items N/A). Every other plugin-relevant changelog item is ADDITIVE/optional, not breaking — candidate future enhancements (not adopted): Stop/SubagentStop `hookSpecificOutput.additionalContext` (2.1.x), skill/command `disallowed-tools` frontmatter, the `MessageDisplay` hook event, `plugin.json` `defaultEnabled`. Lesson: a "read the changelog and update the plugin" request usually resolves to a VERIFICATION (most CC entries are runtime/TUI fixes); audit `model:`-frontmatter / `hooks.json` shape / `.mcp.json` against the relevant subset and report "current" rather than inventing churn.
[^2]: [ocd:2026-06-22 lmd:2026-06-22] CPV canonical-pipeline upgrade (architect#23 / fleet ai-maestro#44), shipped v2.10.2 (commit `b0b735d`). This plugin is the CPV **`remote-validation` profile** by design: it de-vendored the CPV validators, `publish.py`/CI drive the REMOTE `cpv-remote-validate --strict` gate, and `.githooks/pre-push` is a process-ancestry gate (a stronger alternative to the env-var gate). Old CPV 2.137.0's `standardize --fix --force-templates` DAMAGED it (re-vendored publish.py 62→73KB, re-created `cpv_network_resilience.py`, added a competing env-gate pre-push, downgraded `notify-marketplace.yml`) — sandbox-proven, then reverted. The correct upgrade with CPV ≥ 2.143.0 (profile-aware): declare each by-design-divergent shared-canon file in `plugin.json` → `cpv.pipeline.intentional_divergence` (a SELECTOR not a suppressor, TRDD-02e1672b — drift becomes an auditable INFO, never silenced, and `--force-templates` skips it). The 2 residual `RC-PIPELINE-DRIFT-001` WARNINGs (`publish.py` by-design, `notify-marketplace.yml` ahead-of-canon) are advisory + non-blocking + EXPECTED. Lesson: NEVER run CPV `--force-templates` on this plugin; bring it to canon by editing `intentional_divergence` in the manifest and let `--strict` (0 C/M/MI/N + advisory WARNINGs only) be the gate.
