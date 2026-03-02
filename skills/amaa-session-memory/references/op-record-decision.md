---
procedure: support-skill
workflow-instruction: support
---

# Operation: Record Architecture Decision


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Determine ADR Number](#step-1-determine-adr-number)
  - [Step 2: Create ADR File](#step-2-create-adr-file)
- [Status](#status)
- [Context](#context)
  - [Background](#background)
  - [Constraints Considered](#constraints-considered)
- [Decision](#decision)
- [Rationale](#rationale)
  - [Key Factors](#key-factors)
- [Alternatives Considered](#alternatives-considered)
  - [Option 1: <Alternative>](#option-1-alternative)
  - [Option 2: <Alternative>](#option-2-alternative)
- [Consequences](#consequences)
  - [Positive](#positive)
  - [Negative](#negative)
- [Implementation Impact](#implementation-impact)
  - [Affected Components](#affected-components)
  - [Required Actions](#required-actions)
- [Related](#related)
  - [Step 3: Update Design Index](#step-3-update-design-index)
  - [Step 4: Update Session State](#step-4-update-session-state)
  - [Step 5: Link Related Artifacts](#step-5-link-related-artifacts)
  - [Step 6: Report Decision Recorded](#step-6-report-decision-recorded)
- [Decision Recorded](#decision-recorded)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example](#example)
- [Status](#status)
- [Context](#context)
- [Decision](#decision)
- [Rationale](#rationale)
- [Alternatives Considered](#alternatives-considered)
  - [Option 1: PostgreSQL](#option-1-postgresql)
  - [Option 2: In-memory](#option-2-in-memory)
- [Consequences](#consequences)
  - [Positive](#positive)
  - [Negative](#negative)
- [Error Handling](#error-handling)

## Purpose

Create an Architecture Decision Record (ADR) when a significant architecture decision is made, ensuring the decision and its rationale are preserved.

## When to Use

- Architecture decision finalized
- Technology selection made
- Design pattern chosen
- Integration approach decided

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Decision statement | Discussion | Yes |
| Rationale | Analysis | Yes |
| Alternatives | Evaluation | Yes |
| Impact scope | Analysis | Yes |

## Procedure

### Step 1: Determine ADR Number

```bash
# Get next ADR number
DECISIONS_DIR="docs_dev/design/decisions"
mkdir -p "$DECISIONS_DIR"

LAST_ADR=$(ls "$DECISIONS_DIR"/ADR-*.md 2>/dev/null | sort -V | tail -1 | grep -oE 'ADR-[0-9]+')
if [ -z "$LAST_ADR" ]; then
    NEXT_NUM="001"
else
    CURRENT_NUM=$(echo "$LAST_ADR" | grep -oE '[0-9]+')
    NEXT_NUM=$(printf "%03d" $((10#$CURRENT_NUM + 1)))
fi

echo "Next ADR: ADR-$NEXT_NUM"
```

### Step 2: Create ADR File

Create `docs_dev/design/decisions/ADR-NNN-<title-slug>.md`:

```markdown
---
id: ADR-<NNN>
title: <Decision Title>
status: PROPOSED
date: YYYY-MM-DD
deciders: <Names/Roles>
---

# ADR-<NNN>: <Decision Title>

## Status

PROPOSED

## Context

<What issue motivates this decision? What forces are at play?>

### Background

<Additional context>

### Constraints Considered

- CON-XXX: <relevant constraint>
- CON-YYY: <relevant constraint>

## Decision

We will use **<chosen option>** because <primary reason>.

## Rationale

<Why this decision was made>

### Key Factors

1. **<Factor 1>**: <explanation>
2. **<Factor 2>**: <explanation>
3. **<Factor 3>**: <explanation>

## Alternatives Considered

### Option 1: <Alternative>

**Pros:**
- <pro>

**Cons:**
- <con>

**Why not chosen:** <reason>

### Option 2: <Alternative>

<Same structure>

## Consequences

### Positive

- <positive consequence>

### Negative

- <negative consequence or trade-off>
- **Mitigation:** <how to address>

## Implementation Impact

### Affected Components

- `<component>`: <how affected>

### Required Actions

1. <action item>
2. <action item>

## Related

- [ADR-XXX](ADR-XXX-related.md) - Related decision
- [CON-XXX](../constraints.md#con-xxx) - Relevant constraint
```

### Step 3: Update Design Index

```python
def add_decision_to_index(decision: dict):
    """Add new decision to design index."""
    import json

    index_path = "docs_dev/design/index.json"

    # Load existing index
    with open(index_path) as f:
        index = json.load(f)

    # Add decision
    index["decisions"].append({
        "id": decision["id"],
        "title": decision["title"],
        "status": decision["status"],
        "file": f"decisions/{decision['filename']}"
    })

    # Update timestamp
    index["last_updated"] = datetime.now().isoformat()

    # Save index
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
```

### Step 4: Update Session State

```python
def update_session_after_decision(session_state: dict, decision_id: str):
    """Update session state after recording a decision."""
    session_state["last_activity"] = "architecture_decision_made"
    session_state["last_updated"] = datetime.now().isoformat()
    session_state["decisions_count"] += 1

    save_session_state(session_state)
```

### Step 5: Link Related Artifacts

If this decision resolves an open question:
```python
def resolve_question(question_id: str, decision_id: str):
    """Mark an open question as resolved by a decision."""
    # Update open-questions.md
    # Change status from OPEN to RESOLVED
    # Add reference to resolving decision
```

### Step 6: Report Decision Recorded

```markdown
## Decision Recorded

**ID:** ADR-005
**Title:** Session Storage Selection
**Status:** PROPOSED

**File:** docs_dev/design/decisions/ADR-005-session-storage.md

**Index Updated:** Yes
**Session State Updated:** Yes

**Current State:**
- Decisions: 5 (was 4)
- Open Questions: 1 resolved
```

## Output

| File | Content |
|------|---------|
| `docs_dev/design/decisions/ADR-NNN-*.md` | Decision record |
| `docs_dev/design/index.json` | Updated index |
| `.claude/eaa-session-state.local.md` | Updated session state |

## Verification Checklist

- [ ] ADR number is sequential
- [ ] ADR file created
- [ ] All required sections filled
- [ ] Alternatives documented (at least 2)
- [ ] Consequences listed
- [ ] Index updated
- [ ] Session state updated
- [ ] Related artifacts linked

## Example

```markdown
# ADR-005: Session Storage Selection

## Status
PROPOSED

## Context
The application needs session storage for user authentication state.

## Decision
We will use **Redis** for session storage.

## Rationale
Redis provides sub-millisecond latency and built-in TTL support.

## Alternatives Considered

### Option 1: PostgreSQL
**Why not chosen:** Higher latency for session lookups

### Option 2: In-memory
**Why not chosen:** No horizontal scaling

## Consequences

### Positive
- Fast session access

### Negative
- Additional infrastructure
- **Mitigation:** Use managed Redis service
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Duplicate ADR number | Race condition | Check again, use higher number |
| Index update fails | File locked | Retry after delay |
| Missing rationale | Incomplete input | Cannot proceed - rationale required |
