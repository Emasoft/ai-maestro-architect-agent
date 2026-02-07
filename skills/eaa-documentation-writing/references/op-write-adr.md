---
procedure: support-skill
workflow-instruction: support
---

# Operation: Write Architecture Decision Record (ADR)

## Purpose

Write an Architecture Decision Record (ADR) that documents a significant architecture decision, including context, decision, rationale, alternatives considered, and consequences.

## When to Use

- Recording a significant architecture decision
- Documenting technology selection
- Capturing design pattern choice
- Recording integration approach decision

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Decision context | Discussion/analysis | Yes |
| Decision statement | Resolution | Yes |
| Alternatives | Analysis | Yes |
| Rationale | Discussion | Yes |

## Procedure

### Step 1: Determine ADR Number

Check existing ADRs in `/docs/adrs/`:
```bash
ls /docs/adrs/ADR-*.md | tail -1
```

Use next sequential number (e.g., ADR-001, ADR-002).

### Step 2: Create ADR Document

Use this template:

```markdown
# ADR-<NNN>: <Decision Title>

**Status:** PROPOSED | ACCEPTED | SUPERSEDED | DEPRECATED
**Date:** YYYY-MM-DD
**Deciders:** <Names or roles involved>
**Supersedes:** ADR-XXX (if applicable)
**Superseded by:** ADR-YYY (if applicable)

---

## Context

<Describe the issue motivating this decision. What forces are at play? What is the problem we need to solve?>

### Background

<Additional context or history that helps understand the decision>

### Constraints

- <Constraint 1>
- <Constraint 2>

### Requirements

- <Requirement that must be met>
- <Another requirement>

---

## Decision

<State the decision clearly and concisely>

We will use **<chosen option>** because <primary reason>.

---

## Rationale

<Explain why this decision was made. What factors were most important?>

### Key Factors

1. **<Factor 1>**: <Why this mattered>
2. **<Factor 2>**: <Why this mattered>
3. **<Factor 3>**: <Why this mattered>

---

## Alternatives Considered

### Option 1: <Alternative Name>

**Description:** <Brief description>

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Why not chosen:** <Specific reason>

---

### Option 2: <Another Alternative>

**Description:** <Brief description>

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Why not chosen:** <Specific reason>

---

## Consequences

### Positive

- <Positive consequence 1>
- <Positive consequence 2>

### Negative

- <Negative consequence or trade-off 1>
- <Mitigation approach>

### Neutral

- <Neutral impact>

---

## Implementation Notes

<Any specific guidance for implementing this decision>

### Affected Components

- `component-1`: <How it's affected>
- `component-2`: <How it's affected>

### Migration Plan (if applicable)

1. <Step 1>
2. <Step 2>

---

## Related Decisions

- [ADR-XXX: Related Decision](ADR-XXX-related.md)

---

## References

- [External reference 1](url)
- [External reference 2](url)

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| YYYY-MM-DD | Name | Initial draft |
```

### Step 3: Apply Quality Check (6 C's)

- [ ] **Complete**: Context, decision, alternatives, consequences
- [ ] **Correct**: Decision matches actual implementation
- [ ] **Clear**: Decision statement unambiguous
- [ ] **Consistent**: Terminology matches project
- [ ] **Current**: Reflects current status
- [ ] **Connected**: Links to related ADRs

### Step 4: Save Document

Save to: `/docs/adrs/ADR-<NNN>-<title-slug>.md`

Filename format: `ADR-001-database-selection.md`

## Output

| File | Location |
|------|----------|
| Architecture Decision Record | `/docs/adrs/ADR-<NNN>-<title>.md` |

## Verification Checklist

- [ ] ADR number is sequential
- [ ] Status is set (PROPOSED initially)
- [ ] Context explains the problem
- [ ] Decision is clearly stated
- [ ] At least 2 alternatives documented
- [ ] Consequences listed (positive and negative)
- [ ] Related ADRs linked
- [ ] 6 C's quality check passed

## Example

```markdown
# ADR-005: Session Storage Selection

**Status:** ACCEPTED
**Date:** 2026-02-04
**Deciders:** Architecture Team

## Context

The application needs session storage for user authentication state. Sessions must be available across multiple application instances.

## Decision

We will use **Redis** for session storage.

## Rationale

Redis provides sub-millisecond latency, built-in TTL support, and horizontal scaling through Redis Cluster.

## Alternatives Considered

### Option 1: PostgreSQL
**Why not chosen:** Higher latency for session lookups (5-10ms vs <1ms)

### Option 2: In-memory
**Why not chosen:** No horizontal scaling, sessions lost on restart

## Consequences

### Positive
- Fast session access
- Easy horizontal scaling

### Negative
- Additional infrastructure to manage
- Mitigation: Use managed Redis service
```

## Error Handling

| Error | Solution |
|-------|----------|
| Duplicate ADR number | Check existing ADRs, use next available |
| Decision unclear | Restate as "We will..." statement |
| Missing alternatives | Document at least "do nothing" option |
