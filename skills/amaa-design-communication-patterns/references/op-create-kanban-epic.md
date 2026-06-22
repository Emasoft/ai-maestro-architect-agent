---
operation: create-kanban-epic
---

# Create AI Maestro Kanban Epic Task

## Contents

- When to Use
- Prerequisites
- Procedure
- Checklist
- Examples
- Error Handling
- Related Operations

## When to Use

Trigger this operation when a design document reaches COMPLETED in the design lifecycle and is about to be handed off to AMOA. The architect creates ONE `epic` task on the AI Maestro kanban representing the whole design, then (optionally) the first-level child tasks it has already identified (modules, NPTs, EHTs). The epic's id is carried in the design-handoff message as `aimaestro_task_id` (see op-send-ai-maestro-message and ai-maestro-message-templates §1.3/§1.4), giving design-doc → epic → child-task → GitHub-issue traceability.

Do NOT use this for status changes (use amp-kanban-move / amp-task-done) or for flat non-epic tasks.

## Prerequisites

- AI Maestro service running AND this session registered as a fleet agent with a team (a real AMCOS-spawned architect session). `amp-kanban-create-task` resolves the team from the agent registration, or pass `--team <teamId>`. A dev session with no agent binding cannot run this live (see TRDD-364ccafc Phase 0).
- The design document is COMPLETE (lifecycle state COMPLETED) with its handoff doc written.
- The frozen verb `amp-kanban-create-task` on PATH (R23 — never a raw `/api/*` call) and `jq` to capture the returned id.

## Procedure

### Step 1: Create the epic task

Create one `epic` task for the design. Put the design-doc path + a one-line summary in the description (the verb has no `--attachments` flag yet — tracked upstream):

```bash
EPIC=$(amp-kanban-create-task "Design: <PROJECT_NAME>" \
  --task-type epic \
  --labels design,epic \
  --description "<docs_dev/design/handoff-<UUID>.md> — <one-line design summary>" \
  --status backburner \
  | jq -r '.id // .task.id // empty')
[ -n "$EPIC" ] || { echo "ERROR: epic id not returned by amp-kanban-create-task" >&2; exit 1; }
```

### Step 2: Create the first-level child tasks (optional)

For each first-level task the design identified, create a child linked to the epic via `--parent`:

```bash
amp-kanban-create-task "<child subject>" \
  --parent "$EPIC" \
  --task-type <feature|bugfix|refactor|infra|docs> \
  --labels <area> \
  --status backburner
```

Use `--npt "<id1>,<id2>"` / `--eht "<id1>,<id2>"` when a child is a necessary-prerequisite / effects-handling task of another.

### Step 3: Carry the epic id into the handoff

Pass `$EPIC` as `aimaestro_task_id` in the design-handoff message (op-send-ai-maestro-message, content per ai-maestro-message-templates §1.3 design_complete / §1.4 handoff). This is what links the design doc to the kanban epic for AMOA.

## Checklist

- [ ] Design lifecycle state is COMPLETED and the handoff doc exists
- [ ] Created exactly ONE `epic` task ("Design: <project>") with labels design,epic
- [ ] Captured the returned epic id (non-empty)
- [ ] Created the first-level child tasks with `--parent <epicId>` (if any identified)
- [ ] Passed the epic id as `aimaestro_task_id` in the design-handoff message
- [ ] (Deployment) verified the children read back under the epic (parentTask round-trips) — TRDD-364ccafc Phase 0

## Examples

### Example: Epic + 3 module children for an e-commerce design

```bash
EPIC=$(amp-kanban-create-task "Design: E-Commerce Product Catalog" \
  --task-type epic --labels design,epic \
  --description "docs_dev/design/handoff-a7f8b2d4.md — REST API + PostgreSQL + Redis + React, 5 modules" \
  --status backburner | jq -r '.id // .task.id')

amp-kanban-create-task "Implement product-service" --parent "$EPIC" --task-type feature --labels backend  --status backburner
amp-kanban-create-task "Implement search-service"  --parent "$EPIC" --task-type feature --labels backend  --status backburner
amp-kanban-create-task "Implement frontend"        --parent "$EPIC" --task-type feature --labels frontend --status backburner
# then send the design-handoff with "aimaestro_task_id": "$EPIC"
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Multiple AMP agents found. Use --id <uuid>` | Host has several registered agents; this session isn't a single bound fleet agent | Pass `--id <this-architect-agent-uuid>`; in a real fleet session the agent is bound, so this is a dev-session-only symptom |
| epic id empty after Step 1 | create returned an unexpected JSON shape | Inspect the raw `amp-kanban-create-task` output; adjust the `jq` path |
| `Connection refused` / HTTP 000 | AI Maestro not running | Start the AI Maestro service (default `localhost:23000`) |
| child not under epic on read-back | `parentTask` not persisted server-side | Verify against TRDD-364ccafc Phase 0 (deployment-time round-trip); file upstream if it regresses |
| unknown flag rejected | deployed verb predates the relationship flags | Re-check the deployed `amp-kanban-create-task --help` (relationship flags landed 2026-06-20) |

## Related Operations

- [op-send-ai-maestro-message.md](op-send-ai-maestro-message.md) - send the design-handoff carrying `aimaestro_task_id`
- [op-query-kanban-progress.md](op-query-kanban-progress.md) - read the epic's child tasks for progress
- [ai-maestro-message-templates.md](ai-maestro-message-templates.md) - §1.3/§1.4 handoff templates with `aimaestro_task_id`
