---
name: op-validate-effort-estimate
description: Operation procedure for validating and adjusting effort estimates based on architecture analysis.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Validate Effort Estimate

## Purpose

Validate that the issue's effort label matches the actual complexity revealed by architecture analysis. Recommend adjustments if needed.

## When to Use

- After completing architecture breakdown
- When design reveals more complexity than initially estimated
- During architecture handoff to EOA

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Issue number to validate
- Completed architecture analysis with component count

## Procedure

### Step 1: Check Current Effort Label

```bash
CURRENT_EFFORT=$(gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name | select(startswith("effort:"))')
echo "Current effort: $CURRENT_EFFORT"
```

### Step 2: Count Affected Components

From architecture analysis, count components:

| Component Count | Recommended Effort |
|-----------------|-------------------|
| 1 component, clear pattern | `effort:s` (small) |
| 2-3 components, existing patterns | `effort:m` (medium) |
| Multiple components, new patterns | `effort:l` (large) |
| System-wide, new architecture | `effort:xl` (extra-large) |

### Step 3: Compare Current vs Recommended

```bash
# Example: 3 components found, current is effort:s
COMPONENT_COUNT=3
CURRENT="effort:s"

if [ $COMPONENT_COUNT -gt 2 ] && [ "$CURRENT" = "effort:s" ]; then
  RECOMMENDED="effort:m"
  echo "Recommend upgrade: $CURRENT -> $RECOMMENDED"
fi
```

### Step 4: Document Recommendation in Comment

```bash
gh issue comment $ISSUE_NUMBER --body "## Effort Validation

**Current:** \`$CURRENT_EFFORT\`
**Recommended:** \`$RECOMMENDED_EFFORT\`

**Rationale:** Architecture analysis reveals $COMPONENT_COUNT components affected:
- component:api
- component:database
- component:auth

This complexity suggests \`$RECOMMENDED_EFFORT\` is more appropriate."
```

### Step 5: Update Effort Label (if change needed)

```bash
gh issue edit $ISSUE_NUMBER --remove-label "$CURRENT_EFFORT" --add-label "$RECOMMENDED_EFFORT"
```

### Step 6: Verify Update

```bash
gh issue view $ISSUE_NUMBER --json labels --jq '.labels[].name | select(startswith("effort:"))'
```

## Example

**Scenario:** Issue #123 labeled `effort:s` but architecture reveals 3 components.

```bash
# Step 1: Check current effort
CURRENT=$(gh issue view 123 --json labels --jq '.labels[].name | select(startswith("effort:"))')
echo "Current: $CURRENT"
# Output: effort:s

# Step 2: Comment with recommendation
gh issue comment 123 --body "## Effort Validation

**Current:** \`effort:s\`
**Recommended:** \`effort:m\`

**Rationale:** Architecture analysis suggests effort:m due to 3 components affected (API, DB, Auth). Original estimate was for single-component change."

# Step 3: Update effort
gh issue edit 123 --remove-label "effort:s" --add-label "effort:m"

# Step 4: Verify
gh issue view 123 --json labels --jq '.labels[].name | select(startswith("effort:"))'
# Output: effort:m
```

## Effort Guidelines

| Effort | Time Estimate | Typical Scope |
|--------|---------------|---------------|
| `effort:s` | 1-2 hours | Single file, clear change |
| `effort:m` | 2-8 hours | Multiple files, one component |
| `effort:l` | 1-3 days | Multiple components, integration |
| `effort:xl` | 1+ week | System-wide, new architecture |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No effort label found | Never assigned | Recommend appropriate effort based on analysis |
| Multiple effort labels | Data error | Remove all, add single correct label |
| EOA rejects change | Disagreement on estimate | Document rationale, defer to EOA decision |

## Notes

- EAA recommends effort changes but EOA has final authority
- Document all rationale in issue comments for transparency
- Consider both technical complexity and unknowns/risks
