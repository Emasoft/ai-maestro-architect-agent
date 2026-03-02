---
procedure: support-skill
workflow-instruction: support
---

# Operation: Record Open Question


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Ensure Open Questions File Exists](#step-1-ensure-open-questions-file-exists)
- [Open Questions](#open-questions)
- [Resolved Questions](#resolved-questions)
  - [Step 2: Determine Question ID](#step-2-determine-question-id)
  - [Step 3: Classify Question Type](#step-3-classify-question-type)
  - [Step 4: Add Open Question Entry](#step-4-add-open-question-entry)
  - [OQ-<NNN>: <Question Title>](#oq-nnn-question-title)
  - [Step 5: Update Design Index](#step-5-update-design-index)
  - [Step 6: Update Session State](#step-6-update-session-state)
  - [Step 7: Report Question Recorded](#step-7-report-question-recorded)
- [Open Question Recorded](#open-question-recorded)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Resolving a Question](#resolving-a-question)
- [Example](#example)
  - [OQ-003: Payment Processor Selection](#oq-003-payment-processor-selection)
- [Error Handling](#error-handling)

## Purpose

Record an unresolved question that arises during design work, tracking what decisions are blocked and who should resolve it.

## When to Use

- Design question cannot be answered immediately
- Decision requires external input
- Trade-off needs stakeholder decision
- Technical investigation needed

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Question statement | Discussion | Yes |
| Blocking | Analysis | Yes |
| Suggested owner | Context | Yes |

## Procedure

### Step 1: Ensure Open Questions File Exists

```bash
QUESTIONS_FILE="docs_dev/design/open-questions.md"

if [ ! -f "$QUESTIONS_FILE" ]; then
    cat > "$QUESTIONS_FILE" << 'EOF'
# Open Questions Registry

This document tracks unresolved design questions.

---

## Open Questions

<!-- Questions pending resolution -->

---

## Resolved Questions

<!-- Questions that have been answered -->

EOF
fi
```

### Step 2: Determine Question ID

```bash
# Get next question number
LAST_OQ=$(grep -oE 'OQ-[0-9]+' "$QUESTIONS_FILE" | sort -V | tail -1)
if [ -z "$LAST_OQ" ]; then
    NEXT_NUM="001"
else
    CURRENT_NUM=$(echo "$LAST_OQ" | grep -oE '[0-9]+')
    NEXT_NUM=$(printf "%03d" $((10#$CURRENT_NUM + 1)))
fi

echo "Next Question: OQ-$NEXT_NUM"
```

### Step 3: Classify Question Type

| Type | Description |
|------|-------------|
| **Technical** | Requires technical investigation |
| **Business** | Requires business decision |
| **Resource** | Requires resource allocation |
| **External** | Requires external input |

### Step 4: Add Open Question Entry

Add to Open Questions section in `docs_dev/design/open-questions.md`:

```markdown
### OQ-<NNN>: <Question Title>

**Status:** OPEN | IN_PROGRESS | RESOLVED
**Type:** <Technical|Business|Resource|External>
**Owner:** <Who should resolve>
**Priority:** <High|Medium|Low>
**Date Opened:** YYYY-MM-DD
**Target Resolution:** YYYY-MM-DD (if known)

#### Question

<Clear statement of what needs to be decided>

#### Context

<Background information relevant to answering the question>

#### Blocking

**Blocked Decisions:**
- ADR-XXX: <Decision that cannot proceed>

**Blocked Components:**
- `<component>`: <why blocked>

#### Options Being Considered

1. **Option A:** <description>
   - Pros: <advantages>
   - Cons: <disadvantages>

2. **Option B:** <description>
   - Pros: <advantages>
   - Cons: <disadvantages>

#### Information Needed

- <What information would help answer this>
- <Who might have the answer>

#### Resolution (when resolved)

**Date Resolved:** YYYY-MM-DD
**Decision:** <What was decided>
**Resolved By:** <Who made the decision>
**Resolving ADR:** [ADR-XXX](decisions/ADR-XXX-*.md)

---
```

### Step 5: Update Design Index

```python
def add_question_to_index(question: dict):
    """Add open question to design index."""
    import json

    index_path = "docs_dev/design/index.json"

    with open(index_path) as f:
        index = json.load(f)

    index["open_questions"].append({
        "id": question["id"],
        "statement": question["statement"],
        "status": "OPEN",
        "owner": question["owner"],
        "file": f"open-questions.md#oq-{question['id'].split('-')[1].lower()}"
    })

    index["last_updated"] = datetime.now().isoformat()

    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
```

### Step 6: Update Session State

```python
def update_session_after_question(session_state: dict, question_id: str):
    """Update session state after recording an open question."""
    session_state["last_activity"] = "open_question_identified"
    session_state["last_updated"] = datetime.now().isoformat()
    session_state["open_questions_count"] += 1

    save_session_state(session_state)
```

### Step 7: Report Question Recorded

```markdown
## Open Question Recorded

**ID:** OQ-003
**Question:** Which payment processor should we integrate?
**Owner:** Product Team
**Priority:** High

**File Updated:** docs_dev/design/open-questions.md
**Index Updated:** Yes
**Session State Updated:** Yes

**Current State:**
- Open Questions: 3 (was 2)

**Blocking:**
- ADR-007: Payment Integration (cannot proceed)
- payment-service component (blocked)
```

## Output

| File | Content |
|------|---------|
| `docs_dev/design/open-questions.md` | Updated questions registry |
| `docs_dev/design/index.json` | Updated index |
| `.claude/eaa-session-state.local.md` | Updated session state |

## Verification Checklist

- [ ] Question ID assigned
- [ ] Question clearly stated
- [ ] Owner identified
- [ ] Priority assigned
- [ ] Blocking items documented
- [ ] Options listed (if known)
- [ ] open-questions.md updated
- [ ] Index updated
- [ ] Session state updated

## Resolving a Question

When a question is resolved:

```python
def resolve_question(question_id: str, decision: str, resolved_by: str, adr_id: str = None):
    """Mark an open question as resolved."""
    # 1. Update status in open-questions.md to RESOLVED
    # 2. Add resolution details
    # 3. Move to Resolved Questions section
    # 4. Update index status
    # 5. Decrement open_questions_count in session state
```

## Example

```markdown
### OQ-003: Payment Processor Selection

**Status:** OPEN
**Type:** Business
**Owner:** Product Team
**Priority:** High
**Date Opened:** 2026-02-05
**Target Resolution:** 2026-02-12

#### Question

Which payment processor should we integrate: Stripe, Square, or Adyen?

#### Context

We need to process payments in USD and EUR. Transaction volume expected to be 10,000/month initially.

#### Blocking

**Blocked Decisions:**
- ADR-007: Payment Integration

**Blocked Components:**
- `payment-service`: Cannot implement without processor selection

#### Options Being Considered

1. **Stripe:**
   - Pros: Best docs, team familiarity
   - Cons: Higher fees for EU transactions

2. **Adyen:**
   - Pros: Lower EU fees
   - Cons: More complex integration

#### Information Needed

- Final pricing from each vendor
- EU transaction volume estimates
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No clear owner | Shared responsibility | Assign primary and backup |
| Blocking unclear | Need more analysis | Document "TBD" and update |
| Duplicate question | Already asked | Reference existing or clarify difference |
