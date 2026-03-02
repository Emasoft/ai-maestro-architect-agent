---
name: op-create-adr-issue
description: Operation procedure for creating Architecture Decision Record (ADR) issues.
workflow-instruction: "support"
procedure: "support-skill"
---

# Operation: Create ADR Issue


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Determine Next ADR Number](#step-1-determine-next-adr-number)
  - [Step 2: Prepare ADR Content](#step-2-prepare-adr-content)
  - [Step 3: Create ADR Issue](#step-3-create-adr-issue)
- [Status](#status)
- [Context](#context)
- [Decision Drivers](#decision-drivers)
- [Considered Options](#considered-options)
  - [Option 1: $OPTION_1_NAME](#option-1-option_1_name)
  - [Option 2: $OPTION_2_NAME](#option-2-option_2_name)
- [Decision](#decision)
- [Consequences](#consequences)
  - [Positive](#positive)
  - [Negative](#negative)
- [Related Issues](#related-issues)
  - [Step 4: Link to Related Issues](#step-4-link-to-related-issues)
  - [Step 5: Verify ADR Created](#step-5-verify-adr-created)
- [Example](#example)
- [Status](#status)
- [Context](#context)
- [Decision Drivers](#decision-drivers)
- [Considered Options](#considered-options)
  - [Option 1: PostgreSQL](#option-1-postgresql)
  - [Option 2: MongoDB](#option-2-mongodb)
- [Decision](#decision)
- [Consequences](#consequences)
  - [Positive](#positive)
  - [Negative](#negative)
- [Related Issues](#related-issues)
- [ADR Status Values](#adr-status-values)
- [Error Handling](#error-handling)
- [Notes](#notes)

## Purpose

Create a GitHub issue to track an Architecture Decision Record (ADR) when significant architectural decisions need documentation and discussion.

## When to Use

- When choosing between major technical alternatives
- When introducing new patterns or technologies
- When deprecating existing approaches
- When design decisions need stakeholder input

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Decision context and options identified
- Understanding of project's ADR numbering scheme

## Procedure

### Step 1: Determine Next ADR Number

```bash
# Find highest existing ADR number
LAST_ADR=$(gh issue list --search "ADR-" --json title --jq '[.[].title | capture("ADR-(?<num>[0-9]+)") | .num | tonumber] | max')
NEXT_ADR=$((LAST_ADR + 1))
echo "Next ADR: ADR-$(printf '%03d' $NEXT_ADR)"
```

### Step 2: Prepare ADR Content

ADR structure:
- **Title**: Decision summary
- **Context**: Why this decision is needed
- **Options**: Alternatives considered
- **Decision**: What was decided
- **Consequences**: Impact of the decision

### Step 3: Create ADR Issue

```bash
ADR_NUMBER=$(printf '%03d' $NEXT_ADR)

gh issue create \
  --title "[ADR-$ADR_NUMBER] $DECISION_TITLE" \
  --body "# ADR-$ADR_NUMBER: $DECISION_TITLE

## Status
PROPOSED

## Context
$CONTEXT_DESCRIPTION

## Decision Drivers
- Driver 1
- Driver 2

## Considered Options
### Option 1: $OPTION_1_NAME
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

### Option 2: $OPTION_2_NAME
**Pros:**
- Pro 1

**Cons:**
- Con 1

## Decision
$DECISION_STATEMENT

## Consequences
### Positive
- Consequence 1

### Negative
- Consequence 1

## Related Issues
- #$RELATED_ISSUE" \
  --label "type:docs" \
  --label "component:$AFFECTED_COMPONENT" \
  --label "priority:high"
```

### Step 4: Link to Related Issues

```bash
# Comment on related implementation issue
gh issue comment $RELATED_ISSUE --body "Related ADR: #$ADR_ISSUE_NUMBER

This implementation depends on the decision documented in [ADR-$ADR_NUMBER]."
```

### Step 5: Verify ADR Created

```bash
gh issue view $ADR_ISSUE_NUMBER
```

## Example

**Scenario:** Create ADR for choosing between PostgreSQL and MongoDB for user storage.

```bash
# Step 1: Find next ADR number
LAST_ADR=$(gh issue list --search "ADR-" --json title --jq '[.[].title | capture("ADR-(?<num>[0-9]+)") | .num | tonumber] | max // 0')
NEXT_ADR=$((LAST_ADR + 1))
ADR_NUMBER=$(printf '%03d' $NEXT_ADR)

# Step 2: Create ADR issue
gh issue create \
  --title "[ADR-$ADR_NUMBER] PostgreSQL vs MongoDB for user storage" \
  --body "# ADR-$ADR_NUMBER: PostgreSQL vs MongoDB for user storage

## Status
PROPOSED

## Context
The user authentication feature requires persistent storage for user credentials and session data. We need to decide which database technology to use.

## Decision Drivers
- ACID compliance requirements for auth data
- Team familiarity with technology
- Operational complexity
- Query patterns (mostly simple lookups)

## Considered Options

### Option 1: PostgreSQL
**Pros:**
- ACID compliant
- Team has experience
- Mature ecosystem
- Strong typing

**Cons:**
- Requires schema migrations
- More operational overhead than managed NoSQL

### Option 2: MongoDB
**Pros:**
- Flexible schema
- Easy to get started
- Good for rapid prototyping

**Cons:**
- Team less familiar
- ACID support only recent
- Different mental model

## Decision
Use PostgreSQL for user storage.

## Consequences
### Positive
- Consistent with existing services
- Leverage team expertise
- Strong data integrity

### Negative
- Need to manage migrations
- Schema changes require planning

## Related Issues
- #123 - User Authentication Epic" \
  --label "type:docs" \
  --label "component:database" \
  --label "priority:high"

# Link to epic
gh issue comment 123 --body "Related ADR: #$NEW_ADR_ISSUE

Database choice documented in ADR-$ADR_NUMBER."
```

## ADR Status Values

| Status | Meaning |
|--------|---------|
| PROPOSED | Decision under discussion |
| ACCEPTED | Decision approved |
| DEPRECATED | Decision superseded |
| SUPERSEDED | Replaced by newer ADR |

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Duplicate ADR number | Race condition | Re-query and increment |
| Missing context | Incomplete template | Fill all template sections |
| No component identified | Cross-cutting decision | Use `component:core` |

## Notes

- ADRs should be discussed before implementation begins
- Update ADR status as decision progresses
- Link ADRs to implementation issues for traceability
