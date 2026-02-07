---
procedure: support-skill
workflow-instruction: support
---

# Operation: Classify Verification Result

## Purpose

Classify the experiment result as VERIFIED, UNVERIFIED, or PARTIALLY VERIFIED based on evidence and define the conditions under which each classification applies.

## When to Use

- After analyzing experiment results
- Before finalizing the report
- When making recommendations

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Experiment results | Analysis | Yes |
| Original claim | Hypothesis | Yes |
| Statistical analysis | Execution | Yes |

## Procedure

### Step 1: Review Classification Definitions

| Status | Definition | Safe to Rely On? |
|--------|------------|------------------|
| **VERIFIED** | Claim experimentally confirmed under tested conditions | YES |
| **UNVERIFIED** | Claim tested but failed to match expected outcomes | NO (dangerous) |
| **PARTIALLY VERIFIED** | Claim true under specific conditions only | YES (with conditions) |
| **TBV** | Not yet tested (initial state) | NO (unknown risk) |

### Step 2: Apply Classification Criteria

**VERIFIED if ALL of these are true:**
- [ ] Results match claimed behavior within acceptable margin
- [ ] Results are consistent across multiple runs
- [ ] Statistical significance confirmed (p < 0.05)
- [ ] No major confounding factors identified
- [ ] Results reproducible

**UNVERIFIED if ANY of these are true:**
- [ ] Results contradict claimed behavior
- [ ] Claimed benefits not observed
- [ ] Results show opposite effect
- [ ] Implementation fails to work as described

**PARTIALLY VERIFIED if:**
- [ ] Claim true under some conditions but not others
- [ ] Claim true with specific configuration
- [ ] Claim true for certain data sizes/types
- [ ] Edge cases fail but common cases pass

### Step 3: Document Classification Decision

```markdown
## Classification Decision

### Final Status: <STATUS>

### Evidence Summary

| Criterion | Result | Notes |
|-----------|--------|-------|
| Matches claimed behavior | YES/NO | <details> |
| Consistent results | YES/NO | <variance notes> |
| Statistical significance | YES/NO | p = <value> |
| No confounding factors | YES/NO | <factors identified> |

### Decision Rationale

<2-3 paragraphs explaining why this classification was chosen>

### Confidence Level

| Level | Meaning |
|-------|---------|
| HIGH | Strong evidence, multiple confirming tests |
| MEDIUM | Good evidence, some uncertainty |
| LOW | Limited evidence, more testing recommended |

**Confidence:** <HIGH/MEDIUM/LOW>
```

### Step 4: Document Conditions (if PARTIALLY VERIFIED)

```markdown
## Conditions for Validity

### The claim IS valid when:
- <Specific condition 1>
  - Evidence: <reference to data>
- <Specific condition 2>
  - Evidence: <reference to data>

### The claim is NOT valid when:
- <Specific condition 1>
  - Evidence: <reference to data>
- <Specific condition 2>
  - Evidence: <reference to data>

### Boundary Conditions

| Parameter | Valid Range | Invalid Range |
|-----------|-------------|---------------|
| Data size | > 10,000 items | < 10,000 items |
| Concurrency | > 10 threads | Single thread |
| Network latency | < 1ms | > 10ms |
```

### Step 5: Create Status Badge

For documentation:

```markdown
![Status: VERIFIED](https://img.shields.io/badge/Status-VERIFIED-green)
![Status: UNVERIFIED](https://img.shields.io/badge/Status-UNVERIFIED-red)
![Status: PARTIALLY_VERIFIED](https://img.shields.io/badge/Status-PARTIALLY_VERIFIED-yellow)
```

### Step 6: Define Implications

```markdown
## Implications

### If relying on this claim:

**VERIFIED:**
- Safe to proceed with implementation
- Document as verified with experiment reference

**UNVERIFIED:**
- Do NOT rely on this claim
- Seek alternative approaches
- Document failure to prevent others from repeating

**PARTIALLY VERIFIED:**
- Safe to use ONLY under documented conditions
- Implement runtime checks for conditions
- Document limitations clearly
```

## Output

| Artifact | Content |
|----------|---------|
| Classification section in REPORT.md | Status and rationale |
| Conditions document | If PARTIALLY VERIFIED |

## Verification Checklist

- [ ] All criteria evaluated
- [ ] Evidence cited for each criterion
- [ ] Status selected
- [ ] Rationale documented
- [ ] Confidence level assigned
- [ ] Conditions documented (if applicable)
- [ ] Implications stated

## Example

```markdown
## Classification Decision

### Final Status: PARTIALLY VERIFIED

### Evidence Summary

| Criterion | Result | Notes |
|-----------|--------|-------|
| Matches claimed behavior | PARTIAL | Only true at scale |
| Consistent results | YES | CV < 10% |
| Statistical significance | YES | p = 0.003 |
| No confounding factors | YES | Controlled environment |

### Decision Rationale

The claim that "Redis is faster for caching" is PARTIALLY VERIFIED. Our experiments show that for data sets under 1000 items, in-memory dict outperforms Redis due to network overhead. However, for data sets over 10,000 items with multiple concurrent clients, Redis provides significantly better performance due to its optimized data structures and connection pooling.

### Confidence: HIGH

Strong evidence from 5 independent runs with consistent results.

## Conditions for Validity

### Valid when:
- Data set size > 10,000 items
- Multiple concurrent clients (> 5)
- Network latency < 5ms

### Not valid when:
- Single client access pattern
- Small data sets (< 1000 items)
- High network latency (> 50ms)
```

## Error Handling

| Error | Solution |
|-------|----------|
| Cannot determine status | Gather more evidence or classify as TBV |
| Contradictory evidence | Document both, classify as PARTIALLY VERIFIED |
| Edge cases unclear | Document known cases, note gaps |
