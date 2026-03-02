---
procedure: support-skill
workflow-instruction: support
---

# Operation: Record Discovered Constraint


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Ensure Constraints File Exists](#step-1-ensure-constraints-file-exists)
- [Active Constraints](#active-constraints)
- [Resolved Constraints](#resolved-constraints)
  - [Step 2: Determine Constraint ID](#step-2-determine-constraint-id)
  - [Step 3: Classify Constraint Type](#step-3-classify-constraint-type)
  - [Step 4: Add Constraint Entry](#step-4-add-constraint-entry)
  - [CON-<NNN>: <Constraint Title>](#con-nnn-constraint-title)
  - [Step 5: Update Design Index](#step-5-update-design-index)
  - [Step 6: Update Session State](#step-6-update-session-state)
  - [Step 7: Report Constraint Recorded](#step-7-report-constraint-recorded)
- [Constraint Recorded](#constraint-recorded)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example](#example)
  - [CON-007: Response Time Limit](#con-007-response-time-limit)
- [Error Handling](#error-handling)

## Purpose

Record when a constraint is discovered during design analysis, ensuring the constraint and its impact are documented and tracked.

## When to Use

- Technical constraint discovered
- Business constraint identified
- Resource constraint recognized
- Regulatory requirement surfaced

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Constraint statement | Discovery | Yes |
| Source | Origin | Yes |
| Impact | Analysis | Yes |

## Procedure

### Step 1: Ensure Constraints File Exists

```bash
CONSTRAINTS_FILE="docs_dev/design/constraints.md"

if [ ! -f "$CONSTRAINTS_FILE" ]; then
    cat > "$CONSTRAINTS_FILE" << 'EOF'
# Constraints Registry

This document tracks constraints discovered during design analysis.

---

## Active Constraints

<!-- Constraints are listed below with their IDs -->

---

## Resolved Constraints

<!-- Constraints that have been addressed or are no longer applicable -->

EOF
fi
```

### Step 2: Determine Constraint ID

```bash
# Get next constraint number
LAST_CON=$(grep -oE 'CON-[0-9]+' "$CONSTRAINTS_FILE" | sort -V | tail -1)
if [ -z "$LAST_CON" ]; then
    NEXT_NUM="001"
else
    CURRENT_NUM=$(echo "$LAST_CON" | grep -oE '[0-9]+')
    NEXT_NUM=$(printf "%03d" $((10#$CURRENT_NUM + 1)))
fi

echo "Next Constraint: CON-$NEXT_NUM"
```

### Step 3: Classify Constraint Type

| Type | Description | Examples |
|------|-------------|----------|
| **Technical** | System/technology limitations | "Max 100ms response time" |
| **Business** | Organizational requirements | "Cannot use cloud outside EU" |
| **Resource** | Team/budget limitations | "Team has no Go experience" |
| **Regulatory** | Legal/compliance requirements | "Must comply with GDPR" |
| **Temporal** | Time-based constraints | "Must launch by Q2" |

### Step 4: Add Constraint Entry

Add to Active Constraints section in `docs_dev/design/constraints.md`:

```markdown
### CON-<NNN>: <Constraint Title>

**Type:** <Technical|Business|Resource|Regulatory|Temporal>
**Source:** <Where discovered: user, research, dependency, regulation>
**Status:** ACTIVE
**Date Discovered:** YYYY-MM-DD

#### Constraint Statement

<Clear statement of what is constrained>

#### Impact

**Affected Decisions:**
- [ADR-XXX](decisions/ADR-XXX-*.md) - How this decision is affected

**Affected Components:**
- `<component>`: <how affected>

#### Mitigation

<How the constraint is being addressed>

#### Validation

<How to verify the constraint is being met>

---
```

### Step 5: Update Design Index

```python
def add_constraint_to_index(constraint: dict):
    """Add constraint to design index."""
    import json

    index_path = "docs_dev/design/index.json"

    with open(index_path) as f:
        index = json.load(f)

    index["constraints"].append({
        "id": constraint["id"],
        "statement": constraint["statement"],
        "type": constraint["type"],
        "status": "ACTIVE",
        "file": f"constraints.md#con-{constraint['id'].split('-')[1].lower()}"
    })

    index["last_updated"] = datetime.now().isoformat()

    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
```

### Step 6: Update Session State

```python
def update_session_after_constraint(session_state: dict, constraint_id: str):
    """Update session state after recording a constraint."""
    session_state["last_activity"] = "constraint_discovered"
    session_state["last_updated"] = datetime.now().isoformat()
    session_state["constraints_count"] += 1

    save_session_state(session_state)
```

### Step 7: Report Constraint Recorded

```markdown
## Constraint Recorded

**ID:** CON-007
**Type:** Technical
**Statement:** API response time must not exceed 100ms at 95th percentile

**File Updated:** docs_dev/design/constraints.md
**Index Updated:** Yes
**Session State Updated:** Yes

**Current State:**
- Active Constraints: 7 (was 6)

**Affected Decisions to Review:**
- ADR-003: Database Selection (may need caching layer)
```

## Output

| File | Content |
|------|---------|
| `docs_dev/design/constraints.md` | Updated constraints registry |
| `docs_dev/design/index.json` | Updated index |
| `.claude/eaa-session-state.local.md` | Updated session state |

## Verification Checklist

- [ ] Constraint ID assigned
- [ ] Type classified
- [ ] Source documented
- [ ] Statement is clear and measurable
- [ ] Impact identified
- [ ] Mitigation approach noted
- [ ] constraints.md updated
- [ ] Index updated
- [ ] Session state updated
- [ ] Affected decisions flagged

## Example

```markdown
### CON-007: Response Time Limit

**Type:** Technical
**Source:** Performance requirements document
**Status:** ACTIVE
**Date Discovered:** 2026-02-05

#### Constraint Statement

API response time must not exceed 100ms at the 95th percentile under normal load conditions (1000 concurrent users).

#### Impact

**Affected Decisions:**
- [ADR-003](decisions/ADR-003-database.md) - May require read replicas
- [ADR-005](decisions/ADR-005-caching.md) - Caching layer required

**Affected Components:**
- `api-gateway`: Must implement response time tracking
- `database-layer`: Query optimization required

#### Mitigation

1. Implement Redis caching for frequently accessed data
2. Use read replicas for query distribution
3. Implement request timeout at 95ms to fail fast

#### Validation

- APM monitoring configured to alert on p95 > 100ms
- Load tests run with 1000 concurrent users before each release
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Duplicate constraint | Already recorded | Merge or reference existing |
| ID conflict | Concurrent recording | Check again, use higher number |
| Impact unclear | Need more analysis | Mark as needs review |
