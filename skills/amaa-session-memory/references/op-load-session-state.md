---
procedure: support-skill
workflow-instruction: support
---

# Operation: Load Session State on Start


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Check for Existing Session State](#step-1-check-for-existing-session-state)
  - [Step 2: Read Session State File](#step-2-read-session-state-file)
- [Current Focus](#current-focus)
- [Recent Decisions](#recent-decisions)
- [Active Constraints](#active-constraints)
- [Open Questions](#open-questions)
  - [Step 3: Load Design Index](#step-3-load-design-index)
  - [Step 4: Check for Recent Handoffs](#step-4-check-for-recent-handoffs)
  - [Step 5: Report Loaded Context](#step-5-report-loaded-context)
- [Session Context Loaded](#session-context-loaded)
  - [Design State](#design-state)
  - [Current Focus](#current-focus)
  - [Recommended Next Action](#recommended-next-action)
  - [Files Loaded](#files-loaded)
  - [Step 6: Initialize Fresh Session (if no state)](#step-6-initialize-fresh-session-if-no-state)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example](#example)
- [Error Handling](#error-handling)

## Purpose

Load existing session state and design context when starting a new session, enabling continuity from previous work.

## When to Use

- At the beginning of every design session
- When resuming work after a break
- When context needs to be restored

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state file | `.claude/eaa-session-state.local.md` | If exists |
| Design index | `docs_dev/design/index.json` | If exists |
| Handoff documents | `docs_dev/design/handoffs/` | If exists |

## Procedure

### Step 1: Check for Existing Session State

```bash
SESSION_STATE_FILE=".claude/eaa-session-state.local.md"

if [ -f "$SESSION_STATE_FILE" ]; then
    echo "Found existing session state"
else
    echo "No existing session state found - starting fresh"
fi
```

### Step 2: Read Session State File

If session state exists, parse the YAML frontmatter and content:

```markdown
---
session_id: eaa-session-20260203-091500
project: project-name
design_id: design-payments-xyz789
phase: architecture
last_activity: architecture_decision_made
last_updated: 2026-02-03T09:15:00Z
decisions_count: 4
constraints_count: 6
open_questions_count: 2
---

## Current Focus

<Description of current work focus>

## Recent Decisions

- ADR-003: Selected PostgreSQL for data storage
- ADR-004: Chose microservices architecture

## Active Constraints

- CON-005: Must support offline mode
- CON-006: Maximum 100ms response time

## Open Questions

- OQ-001: Payment processor selection (OPEN)
- OQ-002: Notification service choice (OPEN)
```

### Step 3: Load Design Index

```python
# Load design index for quick lookup
import json

def load_design_index():
    """Load the design index for quick artifact lookup."""
    index_path = "docs_dev/design/index.json"

    try:
        with open(index_path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "decisions": [],
            "patterns": [],
            "constraints": [],
            "open_questions": [],
            "last_updated": None
        }
```

Index structure:
```json
{
  "decisions": [
    {"id": "ADR-001", "title": "Database Selection", "status": "ACCEPTED", "file": "decisions/ADR-001-database-selection.md"},
    {"id": "ADR-002", "title": "API Design", "status": "ACCEPTED", "file": "decisions/ADR-002-api-design.md"}
  ],
  "patterns": [
    {"name": "Repository Pattern", "applied_to": "data-layer", "file": "patterns.md#repository"}
  ],
  "constraints": [
    {"id": "CON-001", "statement": "Must support offline mode", "file": "constraints.md#con-001"}
  ],
  "open_questions": [
    {"id": "OQ-001", "statement": "Payment processor?", "status": "OPEN", "file": "open-questions.md#oq-001"}
  ],
  "last_updated": "2026-02-03T09:15:00Z"
}
```

### Step 4: Check for Recent Handoffs

```bash
# Check for handoff documents
HANDOFF_DIR="docs_dev/design/handoffs"

if [ -d "$HANDOFF_DIR" ]; then
    LATEST_HANDOFF=$(ls -t "$HANDOFF_DIR"/*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_HANDOFF" ]; then
        echo "Found latest handoff: $LATEST_HANDOFF"
    fi
fi
```

### Step 5: Report Loaded Context

Generate summary for the session:

```markdown
## Session Context Loaded

**Session ID:** eaa-session-20260203-091500
**Project:** project-name
**Last Activity:** 2026-02-03T09:15:00Z

### Design State

| Category | Count | Status |
|----------|-------|--------|
| Decisions | 4 | All ACCEPTED |
| Patterns | 2 | Applied |
| Constraints | 6 | Active |
| Open Questions | 2 | 2 OPEN |

### Current Focus

Architecture phase - Payment module design

### Recommended Next Action

Resolve OQ-001: Payment processor selection

### Files Loaded

- `.claude/eaa-session-state.local.md`
- `docs_dev/design/index.json`
- `docs_dev/design/handoffs/handoff-20260203-090000.md`
```

### Step 6: Initialize Fresh Session (if no state)

If no session state exists:

```python
def initialize_session():
    """Initialize a new session state."""
    import datetime

    session_id = f"eaa-session-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    session_state = {
        "session_id": session_id,
        "project": None,  # Set when design work begins
        "design_id": None,
        "phase": "pre-design",
        "last_activity": "session_started",
        "last_updated": datetime.datetime.now().isoformat(),
        "decisions_count": 0,
        "constraints_count": 0,
        "open_questions_count": 0
    }

    return session_state
```

## Output

| Artifact | Content |
|----------|---------|
| Loaded context | Session state in memory |
| Context summary | Report of loaded state |

## Verification Checklist

- [ ] Session state file checked
- [ ] Session state loaded (if exists)
- [ ] Design index loaded (if exists)
- [ ] Handoff documents checked
- [ ] Context summary reported
- [ ] Ready for design work

## Example

```
EAA: Checking for existing session state...
Found: .claude/eaa-session-state.local.md

Session ID: eaa-session-20260203-091500
Last Activity: architecture_decision_made
Decisions: 4
Constraints: 6
Open Questions: 2

Loading design index...
Index loaded: 4 decisions, 2 patterns, 6 constraints, 2 open questions

Context retrieved. Active design: design-payments-xyz789
Current phase: architecture
Next recommended action: Resolve OQ-002 (Payment processor selection)

Ready to continue design work.
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Session state corrupted | Invalid YAML | Rebuild from design index |
| Design index missing | Never created | Initialize empty index |
| Handoff reference invalid | File moved/deleted | Rebuild from available files |
