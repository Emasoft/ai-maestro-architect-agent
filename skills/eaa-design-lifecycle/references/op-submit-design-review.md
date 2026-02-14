---
operation: submit-design-review
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Review Submission
parent-skill: eaa-design-lifecycle
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Submit Design for Review


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Validate Completeness Checklist](#step-1-validate-completeness-checklist)
  - [Step 2: Update State to REVIEW](#step-2-update-state-to-review)
  - [Step 3: Create Review Request](#step-3-create-review-request)
  - [Step 4: Assign Reviewers](#step-4-assign-reviewers)
  - [Step 5: Track Review Comments](#step-5-track-review-comments)
  - [Step 6: Notify Reviewers](#step-6-notify-reviewers)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Submit Authentication Design for Review](#example-submit-authentication-design-for-review)
  - [Example: Review Request Format](#example-review-request-format)
- [Review Request](#review-request)
  - [Reviewers](#reviewers)
  - [Review Focus Areas](#review-focus-areas)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- A design document in DRAFT state is ready for stakeholder review
- All required sections of the design have been completed
- The design is ready to be evaluated by reviewers

## Prerequisites

- Design document exists in DRAFT state
- Design document UUID is registered in the design index
- All required sections of the design template are completed
- Completeness checklist has been validated

## Procedure

### Step 1: Validate Completeness Checklist

Before submission, verify all required sections are complete:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action validate-completeness
```

Required sections:
- Overview / Problem Statement
- Requirements Summary
- Proposed Architecture
- Component Breakdown
- Risk Assessment

### Step 2: Update State to REVIEW

Transition the design from DRAFT to REVIEW state:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition REVIEW
```

This command:
- Validates the transition is legal (DRAFT -> REVIEW is valid)
- Updates the frontmatter status field
- Updates the design index
- Records the transition timestamp

### Step 3: Create Review Request

Document the review request with scope and timeline:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action create-review-request \
  --scope "Full design review" \
  --deadline "2026-02-05"
```

### Step 4: Assign Reviewers

Specify who should review the design:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action assign-reviewers \
  --reviewers "Alice,Bob,Charlie"
```

### Step 5: Track Review Comments

Set up tracking for review comments. Comments can be added to the design document itself or tracked separately:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action init-review-tracking
```

### Step 6: Notify Reviewers

Send notifications to assigned reviewers that the design is ready for review.

## Checklist

Copy this checklist and track your progress:

- [ ] Run completeness validation: `--action validate-completeness`
- [ ] Verify all required sections are filled
- [ ] Transition state to REVIEW: `--transition REVIEW`
- [ ] Confirm state change in frontmatter
- [ ] Create review request with scope and deadline
- [ ] Assign at least 2 reviewers
- [ ] Initialize review tracking
- [ ] Send notifications to reviewers
- [ ] Document submission date in design history

## Examples

### Example: Submit Authentication Design for Review

```bash
# Step 1: Validate completeness
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action validate-completeness
# Output: Completeness check passed. 8/8 required sections complete.

# Step 2: Transition to REVIEW
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --transition REVIEW
# Output: State transitioned: DRAFT -> REVIEW

# Step 3: Create review request
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action create-review-request \
  --scope "Full architecture review" \
  --deadline "2026-02-07"
# Output: Review request created. Deadline: 2026-02-07

# Step 4: Assign reviewers
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action assign-reviewers \
  --reviewers "SecurityLead,BackendLead"
# Output: Assigned 2 reviewers to design
```

### Example: Review Request Format

The review request is documented in the design file or a separate review file:

```markdown
## Review Request

**Design UUID:** design-auth-20260130-abc123
**Submitted:** 2026-01-30
**Deadline:** 2026-02-07
**Scope:** Full architecture review

### Reviewers
- [ ] SecurityLead - Pending
- [ ] BackendLead - Pending

### Review Focus Areas
1. Security considerations for OAuth2 flow
2. Token storage and rotation strategy
3. API endpoint design
4. Error handling patterns
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Completeness check failed | Missing required sections | Complete all required sections before submission |
| Invalid state transition | Design not in DRAFT state | Can only transition to REVIEW from DRAFT |
| UUID not found | Design not registered in index | Register design first using `--action register` |
| No reviewers specified | Missing reviewer assignment | Assign at least one reviewer before proceeding |
| Deadline in past | Invalid deadline date | Specify a future date for review deadline |

## Related Operations

- [op-create-design-document.md](op-create-design-document.md) - Previous step in workflow
- [op-approve-design.md](op-approve-design.md) - Next step after review completion
- [op-manage-state-transitions.md](op-manage-state-transitions.md) - State transition rules
