---
operation: query-kanban-progress
---

# Query AI Maestro Kanban Progress (read-only)

## Contents

- When to Use
- Prerequisites
- Procedure
- Checklist
- Examples
- Error Handling
- Related Operations

## When to Use

Trigger this operation when the architect wants to SEE how the orchestrator (AMOA) broke down a design epic and track implementation progress — read-only visibility into an epic's child tasks across the 14-stage pipeline. Use it after handing off a design (with its `aimaestro_task_id` epic), during IMPLEMENTING / tracking, or before a redesign decision.

This is READ-ONLY: it never creates, moves, or closes tasks.

## Prerequisites

- AI Maestro service running and this session a registered fleet agent with a team (see op-create-kanban-epic Prerequisites; a dev session with no agent binding cannot run it live — TRDD-364ccafc Phase 0).
- The epic task id (`aimaestro_task_id`) captured when the epic was created (op-create-kanban-epic).
- The frozen verb `amp-kanban-list` on PATH (R23 — never a raw `/api/*` call) and `jq`.

## Procedure

### Step 1: List the team's tasks and filter to the epic's children

`amp-kanban-list` returns the team's tasks as JSON. Filter client-side by `parentTask` (the verb has no `--parent` server filter yet — tracked upstream):

```bash
EPIC="<aimaestro_task_id>"
amp-kanban-list | jq --arg e "$EPIC" \
  '[.[] | select(.parentTask == $e) | {id, subject, status, taskType, assigneeAgentId}]'
```

### Step 2: Summarize progress by status

```bash
amp-kanban-list | jq --arg e "$EPIC" \
  '[.[] | select(.parentTask == $e)] | group_by(.status) | map({status: .[0].status, count: length})'
```

A child in `complete` / `published` / `live` is done; `blocked` / `failed` needs attention; the rest are in flight across the 14-stage pipeline.

## Checklist

- [ ] Have the epic id from the handoff (`aimaestro_task_id`)
- [ ] Listed the team's tasks (read-only)
- [ ] Filtered to children where `parentTask == <epicId>`
- [ ] Reviewed child statuses across the 14-stage pipeline
- [ ] Did NOT mutate any task (this operation is read-only)

## Examples

### Example: progress of an e-commerce design epic

```bash
EPIC="PVTI_laDOABcd1234"
amp-kanban-list | jq --arg e "$EPIC" '[.[] | select(.parentTask == $e) | {subject, status}]'
# → [{"subject":"Implement product-service","status":"dev"},
#    {"subject":"Implement frontend","status":"backburner"}, ...]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Multiple AMP agents found. Use --id <uuid>` | Not a single bound fleet agent | Pass `--id <architect-uuid>`; dev-session-only symptom |
| empty result for a known epic | `parentTask` not populated on the children (server didn't persist the link) | Verify TRDD-364ccafc Phase 0; confirm the children were created with `--parent` |
| `Connection refused` / HTTP 000 | AI Maestro not running | Start the service (default `localhost:23000`) |
| no `parentTask` field on returned tasks | server build predates the relationship persistence | Confirm the server has the 2026-06-21 extended-task-model landing |

## Related Operations

- [op-create-kanban-epic.md](op-create-kanban-epic.md) - create the epic + children this op reads
- [op-send-ai-maestro-message.md](op-send-ai-maestro-message.md) - the handoff that carried the epic's `aimaestro_task_id`
