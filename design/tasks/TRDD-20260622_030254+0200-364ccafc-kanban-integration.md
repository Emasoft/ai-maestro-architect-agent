---
trdd-id: 364ccafc-fc24-4e60-8915-fd1478ff60f3
title: AI Maestro Kanban Integration — architect creates the epic + child task tree from a design doc
column: dev
created: 2026-06-22T03:02:54+0200
updated: 2026-06-22T11:00:35+0200
current-owner: amaa
assignee: amaa
priority: 3
severity: MEDIUM
effort: L
labels: [kanban, ai-maestro, integration, design-handoff]
task-type: feature
parent-trdd: null
npt: []
eht: []
blocked-by: []
supersedes: []
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
merge-strategy: squash
test-requirements: [unit, integration]
audit-requirements: []
review-requirements: [human-review]
runtime-targets: [macos, linux]
impacts: [public-api]
attempts: 0
last-test-result: not-run
external-refs: ["github.com/Emasoft/ai-maestro-architect-agent/issues/7", "github.com/Emasoft/ai-maestro/issues/43"]
---

# TRDD-364ccafc — AI Maestro Kanban Integration (architect#7)

**Filename:** `design/tasks/TRDD-20260622_030254+0200-364ccafc-kanban-integration.md`
**Tracks:** ai-maestro-architect-agent#7

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-06-22

**What this is:** implement architect#7 — when AMAA finalizes a design doc, it (1) creates an `epic` kanban task on AI-Maestro carrying the design + its first-level child tasks, (2) puts the `aimaestro_task_id` in the AMP design-handoff so the orchestrator links design→task, (3) can read-only query the epic's children for progress, (4) resolves the handoff recipient dynamically (no hardcoded names).

**Unblock context (2026-06-22):** the `amp-kanban-create-task` frozen verb gained the relationship flags (`--parent`/`--npt`/`--eht`/`--supersedes`/`--relevant-rules`/`--severity`/`--effort`/`--release-via`/`--task-type epic`) — deployed 2026-06-20 21:29, verified by reading the deployed 328-line script. So the epic→child TREE is now expressible via R23. See the USER-scope memory note `reference_kanban_task_creation_contract` ([^5] there).

**Per-part implementability (verified 2026-06-22):**
- **Part 1 (epic + children):** DOABLE. `amp-kanban-create-task "Design: <proj>" --task-type epic --labels design,epic` then children with `--parent <epicId>`. GAP: no `--attachments` flag → interim: design-doc path in `--description`/a label. (Residual CLI gap #1.)
- **Part 2 (aimaestro_task_id in handoff):** DOABLE — architect-side. Add the field to the design-handoff template in `skills/amaa-design-communication-patterns/references/ai-maestro-message-templates.md` (+ the `-ops` mirror).
- **Part 3 (progress query):** DOABLE via workaround. `amp-kanban-list` emits the full task JSON (`jq '.'`); filter client-side on `parentTask == <epicId>`. GAP: no `--parent` server filter. (Residual CLI gap #2.)
- **Part 4 (dynamic orchestrator lookup):** LARGELY ALREADY DONE. `op-send-ai-maestro-message.md` already resolves recipients via `amp-team-members --team <teamId>` (pick the chief-of-staff / orchestrator by governance title). The `ecos`/`orchestrator-master` grep hits live in UNRELATED files (planning-patterns publishing docs, label-taxonomy ADR op, infra scripts) — NOT the handoff path. → VERIFY those are not live recipients; clean any stray ones.

**PHASE 1 PROGRESS (2026-06-22):**
- **Part 2 — DONE (architect-side).** `aimaestro_task_id` added as an additive, backward-compatible top-level key, now CONSISTENT across ALL copies: canonical templates (§1.3 + §1.4), the examples file, and session-memory `record-keeping-formats.md` — every JSON block re-validated (parses). op-send references the canonical (no change). Example value `PVTI_…` (a live github-project id, per F3). The cross-plugin read-side (AMOA must READ the field) remains an EHT.
- **Part 4 — DONE (verify-only).** No hardcoded `ecos`/`orchestrator-master` recipient exists in the design-comms skills; dynamic `amp-team-members --team` resolution is already present in the skill + `-ops` + the templates file. No code change needed.
- **Template duplication (verified, refined):** op-send (×2, skill + `-ops`) REFERENCES the canonical templates file (line 145 "Full message template reference"), so **Part 2 is FUNCTIONAL** through that pointer — those are NOT duplicates. The only true content-copies of the §1.3/§1.4 template are TWO: `ai-maestro-message-examples.md` (a design_complete example, line 59) and session-memory `record-keeping-formats.md` (a near-verbatim §1.3+§1.4 copy, lines 393/419). Both now carry the field too (propagated 2026-06-22, all JSON re-validated); canonical (`ai-maestro-message-templates.md`) remains authoritative.

**PHASE 2/3 PROGRESS (2026-06-22):** BOTH ops AUTHORED in both locations (skill + `-ops` twin) — `op-create-kanban-epic.md` (Part 1: epic + `--parent` children) and `op-query-kanban-progress.md` (Part 3: `amp-kanban-list` + client-side `parentTask` filter), matching the op-* format with full error-handling tables.

**INTEGRATION DONE (2026-06-22):** wired into `amaa-design-lifecycle/references/procedures.md` — PROCEDURE 3 (Approve) step 3 creates the kanban epic+children (op-create-kanban-epic), step 4's handoff carries `aimaestro_task_id`; PROCEDURE 4 (Track) step 1 queries progress (op-query-kanban-progress). [CORRECTED: the hook is PROCEDURE 3/4 — approve→handoff→track — NOT PROCEDURE 5 (complete+archive, which is post-implementation). My earlier "PROCEDURE 5" was wrong; verified by reading procedures.md.]

**NEXT ACTION (Phase 4, doable HERE):** (a) a lightweight anti-drift test — assert the ops' documented `amp-kanban-create-task`/`amp-kanban-list` flags exist in the deployed verbs' `--help` (catches doc↔verb drift; the ops are markdown, so there is no code to unit-test, and the live round-trip is deployment-time); (b) update the architecture wikimem with the kanban-integration; (c) file the 2 ai-maestro CLI Method-1 follow-ups (`--attachments` on create, `--parent` on list). DEPLOYMENT-time / post-ship: LIVE round-trip (Phase 0), orchestrator read-side issue, optional secondary-copy consolidation.

**Phase 0 (round-trip persistence NPT) — DEFERRED (not blocking Phase 1), 2026-06-22.** Server is UP (HTTP 401 = auth-gated, `localhost:23000`), BUT `amp-kanban-list` errors `Multiple AMP agents found — use --id <uuid>`: this host has DOZENS of registered agents (all display as `ai-maestro@emasoft.aimaestro.local`, plus `scen018-*`/`scen020-*` scenario-test leftovers), so the architect's OWN uuid + team can't be cleanly resolved for a NON-POLLUTING round-trip. **ROOT CAUSE (verified read-only 2026-06-22):** this session has NO AMP agent binding — no `$AID`/`$AMP_*` env var, no `AMP_CONFIG` config.json, `~/.ai-maestro/` empty. It is a DEV session working ON the plugin, NOT a registered fleet architect agent with a team; the host's many `…aimaestro.local` agents are other sessions / scenario-tests. **Implication:** the LIVE round-trip + Parts 1/3 LIVE operation cannot run from this dev session at all — they are **DEPLOYMENT-time** (a real AMCOS-spawned architect agent + team verifies them). **What IS doable here (so Phase 2 is NOT blocked):** author the ops (the exact CLI command construction) + **contract-test the command strings** (assert the right `amp-kanban-create-task …` / `amp-kanban-list …` invocation is built — no live server needed). Risk the round-trip guards is LOW: the 2026-06-21 F3 relaxed the relationship-field Zod to accept live `PVTI_`/`TRDD-` ids, so `parentTask`/`npt`/`eht` are wired through persistence. Phase 0 gates Parts 1 + 3 **LIVE use** only — NOT Phase 1, NOT the op-authoring + contract-tests.

**Load-bearing facts:**
- The architect's design-handoff lives in the `amaa-design-communication-patterns` skill (+ its `-ops` twin) — `ai-maestro-message-templates.md` (templates) + `op-send-ai-maestro-message.md` (the send op, already dynamic-recipient).
- Design lifecycle state machine: `scripts/amaa_design_lifecycle.py` + the `amaa-design-lifecycle` skill — the epic-creation hook fires on design-doc COMPLETION.
- Frozen verbs (R23, never raw `/api/*`): `amp-kanban-create-task`, `amp-kanban-list`, `amp-team-members` (all `~/.local/bin/*.sh`).

**SUPERSEDED — do NOT carry forward:**
- ✗ "architect#7 is fully implementable / no gaps remain" (my 2026-06-22 #7 comment overstated it) — TWO residual CLI gaps remain (attachments-on-create, parent-filter-on-list); both have architect-side workarounds, so #7 is actionable, just not gap-free.
- ✗ "part 4 needs to replace hardcoded ecos/orchestrator-master in the handoff" — the handoff ALREADY uses dynamic `amp-team-members` lookup; part 4 is mostly verify+cleanup, not a rewrite.

**Durable artifacts to read before acting:**
- ai-maestro-architect-agent#7 (acceptance criteria, 4 parts) · ai-maestro#43 (the CLI-verb work)
- USER memory `reference_kanban_task_creation_contract` (the field contract + [^1]..[^5] lessons)

## Problem (from architect#7)

AMAA produces design docs handed to the orchestrator via AMP, but does not create AI-Maestro kanban tasks, so there is no design-doc → task → GitHub-issue traceability and the architect cannot see implementation progress. Target flow: *design doc → architect creates an `epic` task (+ first-level children) → AMP handoff carries the `aimaestro_task_id` → orchestrator expands the epic → architect queries progress.*

## Design

All board access goes through the **R23 frozen verbs** (`amp-kanban-create-task`, `amp-kanban-list`, `amp-team-members`), never raw `/api/*` — consistent with the plugin's `decouple-api-to-cli` invariant.

### Part 1 — create the epic + first-level children on design completion
On `amaa_design_lifecycle` reaching design-complete, create:
```
EPIC=$(amp-kanban-create-task "Design: <project>" --task-type epic \
  --labels design,epic --description "<design-doc relpath> — <1-line summary>" \
  --status backburner | jq -r '.id // .task.id')
# one child per first-level NPT/EHT/sub-task the design identified:
amp-kanban-create-task "<child subject>" --parent "$EPIC" --task-type <feature|bugfix|...> \
  --labels <...> [--npt <ids>] [--eht <ids>] --status backburner
```
Capture the epic id for Part 2. (Attachment of the design-doc FILE awaits the `--attachments` verb gap; interim = description/label pointer.)

### Part 2 — aimaestro_task_id in the AMP design-handoff
Add `aimaestro_task_id: <epic-uuid>` (+ optional `aimaestro_child_task_ids`) to the design-handoff template so the orchestrator links the doc to the epic. Edit `ai-maestro-message-templates.md` and the `op-send-ai-maestro-message` op (both the skill and `-ops` copies — keep them in parity).

### Part 3 — read-only progress query
A new op `op-query-kanban-progress`: `amp-kanban-list --team <id>` then `jq '[.[] | select(.parentTask=="<epicId>")]'` to show child statuses across the 14-stage pipeline. Replace with `amp-kanban-list --parent <epicId>` once that flag ships.

### Part 4 — dynamic recipient (verify + cleanup)
Confirm the handoff send-op resolves the orchestrator via `amp-team-members --team <id>` (it does today). Audit the `ecos`/`orchestrator-master` occurrences; if any is a live recipient, switch it to the dynamic lookup; otherwise leave/clean the doc examples.

## Residual CLI-verb gaps (core's domain — file Method-1 on ai-maestro)
1. `amp-kanban-create-task --attachments "<path>,<path>"` — to attach the design doc to the epic (server persists `attachments` already; the verb doesn't expose it). Workaround now: description/label pointer.
2. `amp-kanban-list --parent <taskId>` — server-side child filter for Part 3. Workaround now: list-all + client-side `parentTask` jq filter.
Both are nice-to-haves with working architect-side fallbacks → they do NOT block #7. File one ai-maestro issue citing #43 as the sibling CLI follow-up.

## NPT (necessary prerequisite — Phase 0)
- **Round-trip persistence verification** of `parentTask`/`npt`/`eht` (create→read-back), per the [^3] "accepts ≠ persists" trap. Blocked if no live server/test team — then flag and pause Part 1/3 build.

## EHT (effects handling — post-conditions)
- **Cross-plugin read-side (orchestrator/AMOA):** the architect SENDS `aimaestro_task_id`; AMOA must READ it to attach its child breakdown under the epic. Architect cannot edit the orchestrator plugin (Method-1 boundary) → file an issue on `ai-maestro-orchestrator-agent` (its #7-equivalent) once the architect side ships.
- **(DONE by propagation 2026-06-22)** the 2 secondary copies (`ai-maestro-message-examples.md` + session-memory `record-keeping-formats.md`) now carry `aimaestro_task_id`, consistent with canonical. OPTIONAL future cleanup: replace their inline template with a pointer to the canonical templates file (true one-source-of-truth, as op-send already does) — low priority.
- Update `amaa-design-lifecycle` + the architecture wikimem to document the new epic-creation step.
- Tests for the epic-creation + progress-query ops (mock-free against a live test team where possible; otherwise contract tests on the command construction).

## Phased plan (≤5 files/phase) — concrete (2026-06-22)
- **Phase 0 (NPT) — DEPLOYMENT-TIME, not runnable here:** live round-trip verify of `parentTask`/`npt`/`eht` persistence. This dev session has no AMP agent binding, so a real AMCOS-spawned architect+team verifies it. Gates Parts 1/3 LIVE use, NOT the build.
- **Phase 1 — ✅ DONE:** Part 2 (handoff `aimaestro_task_id`, consistent across all template copies) + Part 4 (dynamic recipient, already done).
- **Phase 2 — Part 1 epic-creation (DOABLE HERE, build NEXT):** author `op-create-kanban-epic.md` in `skills/amaa-design-communication-patterns-ops/references/` **and** its twin `skills/amaa-design-communication-patterns/references/` (both skills carry each op-*). Match the op-* format: `---\noperation: create-kanban-epic\n---` + sections *When to Use / Prerequisites / Procedure / Checklist / Examples / Error Handling* (template: `op-send-ai-maestro-message.md`). Procedure: `EPIC=$(amp-kanban-create-task "Design: <proj>" --task-type epic --labels design,epic --description "<doc relpath> — <summary>" | jq -r '.id // .task.id')` → first-level children via `--parent "$EPIC"`. Wire into the design-lifecycle APPROVE→handoff step (`amaa-design-lifecycle` PROCEDURE 3 in `references/procedures.md`, NOT 5): create the epic at approval, BEFORE the handoff, and feed its id to Part 2's `aimaestro_task_id`.
- **Phase 3 — Part 3 progress-query:** author `op-query-kanban-progress.md` (+ twin, same format): `amp-kanban-list` → `jq '[.[] | select(.parentTask=="<epicId>")]'` (client-side filter; `--parent` server-filter is the upstream nice-to-have). + file the 2 ai-maestro CLI Method-1 follow-ups (`--attachments` on create, `--parent` on list).
- **Phase 4 — tests + docs + ship:** contract tests asserting the BUILT command strings (no live server); update the architecture wikimem; then publish + file the orchestrator read-side Method-1 issue (EHT).

## Affected files
- `skills/amaa-design-communication-patterns{,-ops}/references/ai-maestro-message-templates.md`, `op-send-ai-maestro-message.md`
- `skills/amaa-design-lifecycle{,-ops}/...` + `scripts/amaa_design_lifecycle.py`
- new ops: `op-create-kanban-epic.md`, `op-query-kanban-progress.md`
- tests under the plugin's test suite

## Approval log
- 2026-06-22T03:02:54+0200 — Authored as Tier-0 (architect's own in-scope task on its own plugin; no baseline/governance/cross-project deviation). `column: dev`, assignee amaa.
