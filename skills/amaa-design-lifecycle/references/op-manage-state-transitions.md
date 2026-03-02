---
operation: manage-state-transitions
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-design-lifecycle
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Manage Design State Transitions


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Understand the State Machine](#step-1-understand-the-state-machine)
  - [Step 2: Check Current State](#step-2-check-current-state)
  - [Step 3: Validate Proposed Transition](#step-3-validate-proposed-transition)
  - [Step 4: Execute State Transition](#step-4-execute-state-transition)
  - [Step 5: Verify Transition Success](#step-5-verify-transition-success)
- [State Transition Rules](#state-transition-rules)
  - [DRAFT to REVIEW](#draft-to-review)
  - [REVIEW to APPROVED](#review-to-approved)
  - [REVIEW to DRAFT (Revision)](#review-to-draft-revision)
  - [APPROVED to IMPLEMENTING](#approved-to-implementing)
  - [IMPLEMENTING to COMPLETED](#implementing-to-completed)
  - [COMPLETED to ARCHIVED](#completed-to-archived)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Full Lifecycle Transitions](#example-full-lifecycle-transitions)
  - [Example: Revision After Review](#example-revision-after-review)
  - [Example: Invalid Transition Error](#example-invalid-transition-error)
- [State Transition Matrix](#state-transition-matrix)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Changing the status of a design document
- Validating a proposed state transition
- Understanding the design workflow and allowed transitions
- Troubleshooting invalid state transition errors

## Prerequisites

- Understanding of design lifecycle states
- Design document with valid UUID
- Access to state transition scripts

## Procedure

### Step 1: Understand the State Machine

Design documents follow this state machine:

```
DRAFT → REVIEW → APPROVED → IMPLEMENTING → COMPLETED → ARCHIVED
         ↓
        DRAFT (revision)
```

**State Definitions:**

| State | Description | Allowed Transitions |
|-------|-------------|---------------------|
| DRAFT | Initial creation, work in progress | REVIEW |
| REVIEW | Under review by stakeholders | APPROVED, DRAFT |
| APPROVED | Ready for implementation | IMPLEMENTING |
| IMPLEMENTING | Being implemented | COMPLETED |
| COMPLETED | Fully implemented | ARCHIVED |
| ARCHIVED | Historical reference (terminal) | None |

### Step 2: Check Current State

Before transitioning, verify the current state:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action check-state
```

### Step 3: Validate Proposed Transition

Check if a transition is valid:

```bash
python scripts/eaa_design_transition.py --uuid <UUID> --from <CURRENT> --to <TARGET> --validate
```

### Step 4: Execute State Transition

Perform the transition:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition <TARGET_STATE>
```

The script:
1. Validates the transition is legal
2. Checks prerequisites for the target state
3. Updates the frontmatter
4. Updates the design index
5. Records the transition timestamp

### Step 5: Verify Transition Success

Confirm the state change:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action check-state
```

## State Transition Rules

### DRAFT to REVIEW

**Prerequisites:**
- All required sections completed
- Completeness checklist passed

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition REVIEW
```

### REVIEW to APPROVED

**Prerequisites:**
- All review comments resolved
- At least one reviewer approval

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition APPROVED
```

### REVIEW to DRAFT (Revision)

**When to use:** Design needs significant changes based on review feedback.

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition DRAFT
```

### APPROVED to IMPLEMENTING

**Prerequisites:**
- Implementation tasks created
- Resources allocated

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition IMPLEMENTING
```

### IMPLEMENTING to COMPLETED

**Prerequisites:**
- All tasks complete
- All requirements implemented
- Testing passed

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition COMPLETED
```

### COMPLETED to ARCHIVED

**Prerequisites:**
- Completion report generated
- Stakeholders notified

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition ARCHIVED
```

## Checklist

Copy this checklist and track your progress:

- [ ] Check current state before transition
- [ ] Validate transition prerequisites
- [ ] Run transition validation: `--validate`
- [ ] Execute transition command
- [ ] Verify new state in frontmatter
- [ ] Verify new state in design index
- [ ] Document transition in history

## Examples

### Example: Full Lifecycle Transitions

```bash
# Create new design - starts in DRAFT
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --action check-state
# Output: Current state: DRAFT

# Complete draft, submit for review
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition REVIEW
# Output: State transitioned: DRAFT -> REVIEW

# After review approval
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition APPROVED
# Output: State transitioned: REVIEW -> APPROVED

# Begin implementation
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition IMPLEMENTING
# Output: State transitioned: APPROVED -> IMPLEMENTING

# Implementation complete
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition COMPLETED
# Output: State transitioned: IMPLEMENTING -> COMPLETED

# Archive for history
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition ARCHIVED
# Output: State transitioned: COMPLETED -> ARCHIVED (terminal state)
```

### Example: Revision After Review

```bash
# Design is in REVIEW but needs major changes
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --action check-state
# Output: Current state: REVIEW

# Return to DRAFT for revision
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition DRAFT
# Output: State transitioned: REVIEW -> DRAFT (revision)

# Make changes, then resubmit
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition REVIEW
# Output: State transitioned: DRAFT -> REVIEW
```

### Example: Invalid Transition Error

```bash
# Attempt invalid transition: DRAFT -> APPROVED (skipping REVIEW)
python scripts/eaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition APPROVED
# Output: ERROR: Invalid state transition
# Cannot transition from DRAFT to APPROVED
# Valid transitions from DRAFT: REVIEW
```

## State Transition Matrix

| From State | To DRAFT | To REVIEW | To APPROVED | To IMPLEMENTING | To COMPLETED | To ARCHIVED |
|------------|----------|-----------|-------------|-----------------|--------------|-------------|
| DRAFT | - | YES | NO | NO | NO | NO |
| REVIEW | YES | - | YES | NO | NO | NO |
| APPROVED | NO | NO | - | YES | NO | NO |
| IMPLEMENTING | NO | NO | NO | - | YES | NO |
| COMPLETED | NO | NO | NO | NO | - | YES |
| ARCHIVED | NO | NO | NO | NO | NO | - |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Invalid state transition | Attempted illegal transition | Check transition matrix for valid transitions |
| Prerequisites not met | Missing requirements for target state | Complete prerequisites before transitioning |
| UUID not found | Design not in index | Register design in index first |
| State mismatch | Frontmatter differs from index | Sync frontmatter with index |
| Already in target state | No-op transition | No action needed |

## Related Operations

- [op-create-design-document.md](op-create-design-document.md) - Initial DRAFT state
- [op-submit-design-review.md](op-submit-design-review.md) - DRAFT to REVIEW
- [op-approve-design.md](op-approve-design.md) - REVIEW to APPROVED
- [op-track-implementation.md](op-track-implementation.md) - APPROVED to IMPLEMENTING
- [op-archive-design.md](op-archive-design.md) - COMPLETED to ARCHIVED
