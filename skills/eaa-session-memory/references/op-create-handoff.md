---
procedure: support-skill
workflow-instruction: support
---

# Operation: Create Session Handoff Document

## Purpose

Create a handoff document that captures complete session context for continuity, enabling a future session (or another agent) to resume work without loss of context.

## When to Use

- Context window approaching limit
- Session ending intentionally
- Transitioning to implementation
- Major design milestone reached
- Significant time gap expected

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Session state | Current session | Yes |
| Design index | Files | Yes |
| Current focus | Context | Yes |

## Procedure

### Step 1: Determine Handoff Type

| Type | Purpose | Target |
|------|---------|--------|
| `session_continuity` | Continue design work | Future EAA session |
| `orchestrator_handoff` | Design complete | EOA (via EAMA) |
| `context_clear` | Preserve before reset | Future EAA session |

### Step 2: Create Handoff Directory

```bash
HANDOFF_DIR="docs_dev/design/handoffs"
mkdir -p "$HANDOFF_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
HANDOFF_FILE="${HANDOFF_DIR}/handoff-${TIMESTAMP}.md"
```

### Step 3: Gather Session Context

Collect from current session:
- Session ID and duration
- Decisions made this session
- Patterns applied
- Constraints discovered
- Questions opened/resolved
- Files modified
- Current work state

### Step 4: Create Handoff Document

```markdown
# Design Session Handoff

**Type:** <session_continuity|orchestrator_handoff|context_clear>
**Created:** YYYY-MM-DD HH:MM:SS
**Session ID:** <session-id>

---

## Session Summary

**Project:** <project-name>
**Design ID:** <design-id>
**Duration:** <start-time> to <end-time>
**Primary Focus:** <what was being worked on>

---

## Decisions Made This Session

| ADR | Title | Status |
|-----|-------|--------|
| ADR-005 | Session Storage | ACCEPTED |
| ADR-006 | API Gateway | PROPOSED |

### Key Decision Details

**ADR-005: Session Storage**
- Selected Redis for session storage
- Rationale: Sub-ms latency, built-in TTL
- Impact: Requires Redis infrastructure

---

## Patterns Applied This Session

| Pattern | Applied To |
|---------|------------|
| Repository | data-access-layer |
| Circuit Breaker | external-api-calls |

---

## Constraints Active

| ID | Statement | Type |
|----|-----------|------|
| CON-001 | Max 100ms response time | Technical |
| CON-002 | GDPR compliance required | Regulatory |

---

## Open Questions

### Pending Resolution

| ID | Question | Owner | Blocking |
|----|----------|-------|----------|
| OQ-003 | Payment processor? | Product | ADR-007 |

### Resolved This Session

| ID | Question | Resolution |
|----|----------|------------|
| OQ-001 | Database choice | ADR-003: PostgreSQL |

---

## Current Work State

### Active Design Focus

<Description of what is currently being designed>

### In Progress

- [ ] <Task in progress>
- [ ] <Task in progress>

### Next Steps

1. <Immediate next action>
2. <Following action>
3. <Following action>

---

## Files Modified This Session

| File | Change |
|------|--------|
| `docs_dev/design/decisions/ADR-005-*.md` | Created |
| `docs_dev/design/patterns.md` | Updated |
| `docs_dev/design/constraints.md` | Updated |

---

## Design Artifacts Summary

| Artifact Type | Count | Location |
|---------------|-------|----------|
| Decisions | 6 | `docs_dev/design/decisions/` |
| Patterns | 3 | `docs_dev/design/patterns.md` |
| Constraints | 7 | `docs_dev/design/constraints.md` |
| Open Questions | 2 | `docs_dev/design/open-questions.md` |

---

## Resume Instructions

### For Future EAA Session

1. Load this handoff document
2. Read current session state from `.claude/eaa-session-state.local.md`
3. Load design index from `docs_dev/design/index.json`
4. Review open questions for blocking items
5. Continue from "Next Steps" above

### Context to Restore

```
Project: <project-name>
Design Phase: architecture
Current Focus: <current focus>
Blocking: OQ-003 (payment processor)
```

### Immediate Priority

<What should be addressed first in next session>

---

## Handoff Validation

- [ ] All decisions documented
- [ ] All constraints recorded
- [ ] Open questions current
- [ ] Files list complete
- [ ] Resume instructions clear
```

### Step 5: Update Session State with Handoff Reference

```python
def update_session_with_handoff(session_state: dict, handoff_file: str):
    """Record handoff in session state."""
    session_state["last_activity"] = "handoff_created"
    session_state["last_updated"] = datetime.now().isoformat()
    session_state["last_handoff"] = handoff_file

    save_session_state(session_state)
```

### Step 6: Report Handoff Created

```markdown
## Handoff Document Created

**File:** docs_dev/design/handoffs/handoff-20260205-143022.md
**Type:** context_clear

**Content Summary:**
- Decisions: 2 recorded
- Patterns: 2 applied
- Constraints: 7 active
- Open Questions: 2 pending

**Session State Updated:** Yes

**To Resume:**
Read handoff document at docs_dev/design/handoffs/handoff-20260205-143022.md

Ready for context clear.
```

## Output

| File | Content |
|------|---------|
| `docs_dev/design/handoffs/handoff-*.md` | Complete handoff document |
| `.claude/eaa-session-state.local.md` | Updated with handoff reference |

## Verification Checklist

- [ ] Handoff type determined
- [ ] Session context gathered
- [ ] Decisions documented
- [ ] Patterns listed
- [ ] Constraints current
- [ ] Open questions listed
- [ ] Files modified listed
- [ ] Resume instructions clear
- [ ] Session state updated

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Incomplete context | Missing files | Gather what's available, note gaps |
| Large handoff | Much activity | Focus on changes this session |
| Handoff dir missing | First handoff | Create directory |
