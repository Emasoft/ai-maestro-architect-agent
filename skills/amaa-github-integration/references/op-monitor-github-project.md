---
operation: monitor-github-project
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-github-integration
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Monitor GitHub Project Kanban Board


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: List All Project Items](#step-1-list-all-project-items)
  - [Step 2: Get Specific Project Items with Details](#step-2-get-specific-project-items-with-details)
  - [Step 3: Check for Recent Updates](#step-3-check-for-recent-updates)
  - [Step 4: On External Change Detection](#step-4-on-external-change-detection)
  - [Step 5: Update Local Design State](#step-5-update-local-design-state)
  - [Step 6: Log the Change](#step-6-log-the-change)
- [[TIMESTAMP]](#timestamp)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Detect Card Movement](#example-detect-card-movement)
  - [Example: Automated Polling Script](#example-automated-polling-script)
- [What to Monitor](#what-to-monitor)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Trigger this operation when:
- During active design work sessions (poll every 5 minutes)
- Need to detect external changes to project board
- Synchronizing local design state with GitHub Project status
- Tracking card movements, comments, and label changes

## Prerequisites

- gh CLI installed and authenticated
- GitHub Project exists and is accessible
- Knowledge of the project owner and project number
- AI Maestro running (for notifications)

## Procedure

### Step 1: List All Project Items

```bash
gh project item-list --owner Emasoft --format json
```

### Step 2: Get Specific Project Items with Details

```bash
gh project item-list --owner Emasoft --project [PROJECT_NUMBER] --format json | jq '.items[] | {title, status, updatedAt}'
```

### Step 3: Check for Recent Updates

```bash
# Items updated in last 5 minutes
gh project item-list --owner Emasoft --format json | jq --arg cutoff "$(date -v-5M -u +%Y-%m-%dT%H:%M:%SZ)" '.items[] | select(.updatedAt > $cutoff)'
```

### Step 4: On External Change Detection

When changes are detected, notify EOA (Emasoft Orchestrator Agent). Send a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `GitHub Project Change Detected`
- **Priority**: `normal`
- **Content**: `{"type": "project_sync", "message": "Card [CARD_TITLE] moved from [OLD_STATUS] to [NEW_STATUS]. Updating local design state."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

### Step 5: Update Local Design State

Match the GitHub Project status to local design document status.

### Step 6: Log the Change

Append to `docs_dev/design/project-sync-log.md`:

```markdown
## [TIMESTAMP]
- Card: [CARD_TITLE]
- Change: [OLD_STATUS] -> [NEW_STATUS]
- Source: GitHub Project external update
- Action: Updated local design state
- Notified: EOA via AI Maestro
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify gh CLI is authenticated: `gh auth status`
- [ ] Identify project owner and number
- [ ] Fetch current project items
- [ ] Check for items updated since last poll
- [ ] For each changed item:
  - [ ] Identify the change type (status, labels, assignment)
  - [ ] Notify EOA via AI Maestro
  - [ ] Update local design document state
  - [ ] Log change to project-sync-log.md
- [ ] Schedule next poll (5 minutes)

## Examples

### Example: Detect Card Movement

```bash
# Poll for updates
gh project item-list --owner Emasoft --format json | jq '.items[] | {title, status, updatedAt}'

# Output:
# {
#   "title": "Auth Service Design",
#   "status": "AI Review",
#   "updatedAt": "2025-01-29T15:30:00Z"
# }

# Previous status was "Draft" - movement detected!
# Notify EOA using the `agent-messaging` skill with:
# - Recipient: `ecos`
# - Subject: `GitHub Project Change Detected`
# - Priority: `normal`
# - Content: `{"type": "project_sync", "message": "Card Auth Service Design moved from Draft to AI Review. Updating local design state."}`
# - Verify: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.
```

### Example: Automated Polling Script

```bash
#!/bin/bash
# Run every 5 minutes during active work

LAST_CHECK=$(cat /tmp/gh-project-last-check 2>/dev/null || echo "1970-01-01T00:00:00Z")

UPDATES=$(gh project item-list --owner Emasoft --format json | \
  jq --arg cutoff "$LAST_CHECK" '[.items[] | select(.updatedAt > $cutoff)]')

if [ "$(echo "$UPDATES" | jq 'length')" -gt 0 ]; then
  echo "Changes detected since $LAST_CHECK"
  echo "$UPDATES" | jq '.'
  # Process updates...
fi

date -u +%Y-%m-%dT%H:%M:%SZ > /tmp/gh-project-last-check
```

## What to Monitor

| Change Type | Detection Method | Action |
|-------------|------------------|--------|
| Card movement (status) | `status` field differs | Update local design status, notify EOA |
| New comments | Check issue comments API | Review and respond if needed |
| Label changes | `labels` field differs | Sync labels to local design |
| Assignment changes | `assignees` field differs | Update design assignee field |
| Milestone updates | `milestone` field differs | Update design milestone field |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ERROR: Project not found` | Wrong owner or project number | Verify with `gh project list --owner <owner>` |
| `ERROR: gh CLI not authenticated` | No auth token | Run `gh auth login` |
| `ERROR: AI Maestro not responding` | Service not running | Start AI Maestro or log change only |
| `ERROR: jq command not found` | jq not installed | Install via `brew install jq` |
| `WARNING: No updates found` | No recent changes | Normal - continue polling |

## Related Operations

- [op-sync-status-to-github.md](op-sync-status-to-github.md) - Push local status changes to GitHub
- [op-verify-gh-cli-auth.md](op-verify-gh-cli-auth.md) - If authentication fails
