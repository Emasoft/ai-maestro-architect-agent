---
procedure: support-skill
workflow-instruction: support
---

# Operation: Resume from Handoff Document

## Purpose

Restore session context from a handoff document, enabling seamless continuation of design work from a previous session.

## When to Use

- Starting new session after context clear
- Resuming work after break
- Taking over from another agent's session
- Recovering from interrupted session

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Handoff document | `docs_dev/design/handoffs/` | Yes |
| Session state | `.claude/` | If exists |
| Design index | `docs_dev/design/` | Yes |

## Procedure

### Step 1: Locate Handoff Document

```bash
HANDOFF_DIR="docs_dev/design/handoffs"

# Find most recent handoff
LATEST_HANDOFF=$(ls -t "$HANDOFF_DIR"/*.md 2>/dev/null | head -1)

if [ -z "$LATEST_HANDOFF" ]; then
    echo "No handoff documents found"
    exit 1
fi

echo "Found handoff: $LATEST_HANDOFF"
```

Or use specific handoff:
```bash
HANDOFF_FILE="docs_dev/design/handoffs/handoff-20260205-143022.md"
```

### Step 2: Parse Handoff Document

Extract key sections:
- Session Summary (project, design ID)
- Decisions Made
- Open Questions
- Current Work State
- Resume Instructions

```python
def parse_handoff(handoff_path: str) -> dict:
    """Parse handoff document into structured data."""
    with open(handoff_path) as f:
        content = f.read()

    # Extract sections
    handoff = {
        "type": extract_field(content, "Type"),
        "created": extract_field(content, "Created"),
        "session_id": extract_field(content, "Session ID"),
        "project": extract_section(content, "Project"),
        "decisions": extract_table(content, "Decisions Made"),
        "open_questions": extract_table(content, "Open Questions"),
        "current_focus": extract_section(content, "Current Work State"),
        "next_steps": extract_list(content, "Next Steps"),
        "files_modified": extract_table(content, "Files Modified")
    }

    return handoff
```

### Step 3: Verify Referenced Files Exist

```bash
# Check all referenced files exist
while read -r file; do
    if [ ! -f "$file" ]; then
        echo "WARNING: Referenced file missing: $file"
    fi
done < <(grep -oE 'docs_dev/[^ )]+' "$LATEST_HANDOFF")
```

### Step 4: Load Design Index

```python
def load_design_index():
    """Load current design index."""
    index_path = "docs_dev/design/index.json"

    with open(index_path) as f:
        return json.load(f)
```

Verify index matches handoff:
- Decision count matches
- Constraint count matches
- Open questions count matches

### Step 5: Create New Session State

```python
def create_session_from_handoff(handoff: dict) -> dict:
    """Create new session state from handoff."""
    import datetime

    session_id = f"eaa-session-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    session_state = {
        "session_id": session_id,
        "project": handoff["project"],
        "design_id": handoff.get("design_id"),
        "phase": handoff.get("phase", "architecture"),
        "last_activity": "resumed_from_handoff",
        "last_updated": datetime.datetime.now().isoformat(),
        "resumed_from": handoff["session_id"],
        "handoff_file": handoff["source_file"],
        "decisions_count": len(handoff["decisions"]),
        "constraints_count": count_from_index("constraints"),
        "open_questions_count": len([q for q in handoff["open_questions"] if q["status"] == "OPEN"])
    }

    save_session_state(session_state)
    return session_state
```

### Step 6: Review Open Questions

```markdown
## Open Questions Requiring Attention

| ID | Question | Owner | Blocking | Priority |
|----|----------|-------|----------|----------|
| OQ-003 | Payment processor? | Product | ADR-007 | High |

**Recommendation:** Resolve OQ-003 before continuing with payment module design.
```

### Step 7: Report Resume Complete

```markdown
## Session Resumed from Handoff

**Handoff File:** docs_dev/design/handoffs/handoff-20260205-143022.md
**Handoff Type:** context_clear
**Original Session:** eaa-session-20260205-120000
**New Session:** eaa-session-20260205-150000

### Context Restored

| Category | Count | Status |
|----------|-------|--------|
| Decisions | 6 | 6 ACCEPTED |
| Patterns | 3 | Applied |
| Constraints | 7 | Active |
| Open Questions | 2 | 2 OPEN |

### Current State

**Project:** payment-system
**Phase:** architecture
**Focus:** Payment module design

### Blocking Items

- OQ-003: Payment processor selection (blocks ADR-007)

### Recommended Next Action

Review OQ-003 options and make selection decision.

### Files Available

- Design index loaded: `docs_dev/design/index.json`
- Decisions: `docs_dev/design/decisions/`
- Patterns: `docs_dev/design/patterns.md`
- Constraints: `docs_dev/design/constraints.md`

---

Ready to continue design work.
```

## Output

| File | Content |
|------|---------|
| `.claude/eaa-session-state.local.md` | New session state |
| Console output | Resume summary |

## Verification Checklist

- [ ] Handoff document located
- [ ] Handoff parsed successfully
- [ ] Referenced files verified
- [ ] Design index loaded
- [ ] Counts match handoff
- [ ] New session state created
- [ ] Open questions reviewed
- [ ] Resume summary provided

## Quick Resume Commands

```bash
# Find and display latest handoff
cat $(ls -t docs_dev/design/handoffs/*.md | head -1)

# Check design index status
cat docs_dev/design/index.json | jq '{
  decisions: .decisions | length,
  patterns: .patterns | length,
  constraints: .constraints | length,
  open_questions: .open_questions | length
}'

# List open questions
grep -A 5 "^### OQ-" docs_dev/design/open-questions.md | grep "OPEN"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Handoff not found | Wrong path or deleted | Check handoffs directory |
| Files missing | Deleted after handoff | Rebuild from available data |
| Count mismatch | Changes after handoff | Use design index as source of truth |
| Corrupted handoff | Bad format | Parse what's readable, note gaps |
