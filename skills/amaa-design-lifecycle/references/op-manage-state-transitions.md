---
operation: manage-state-transitions
---

# Manage Design State Transitions




## Contents

- When to Use
- Prerequisites
- Procedure
- State Transition Rules
- Checklist
- Examples
- Error Handling

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
DRAFT → REVIEW → APPROVED → IMPLEMENTED
  │        │         │           │
  ▼        ▼         ▼           ▼
DEPRECATED (terminal, from DRAFT/REVIEW/APPROVED/IMPLEMENTED)
                      │           │
                      ▼           ▼
              SUPERSEDED (terminal, from APPROVED/IMPLEMENTED)

REVIEW ◄──────────────────────────┘  (mid-dev redesign loop: IMPLEMENTED → REVIEW)

IMPLEMENTED / DEPRECATED / SUPERSEDED ──(archive subcommand)──► ARCHIVED (terminal)
```

**State Definitions:**

| State | Description | Allowed Transitions |
|-------|-------------|---------------------|
| DRAFT | Initial creation, work in progress | REVIEW, DEPRECATED |
| REVIEW | Under review by stakeholders | DRAFT, APPROVED, DEPRECATED |
| APPROVED | Ready for implementation | IMPLEMENTED, DEPRECATED, SUPERSEDED |
| IMPLEMENTED | Fully implemented | REVIEW (redesign loop), DEPRECATED, SUPERSEDED |
| DEPRECATED | No longer relevant (terminal) | None |
| SUPERSEDED | Replaced by another design (terminal) | None |
| ARCHIVED | Historical reference (terminal) | None |

**ARCHIVED is reached only via the `archive` subcommand** (`amaa_design_lifecycle.py
archive`), never via `--transition`, and only from IMPLEMENTED, DEPRECATED, or
SUPERSEDED (or `--force` to override). It has no edge in the transition table above
because it is not part of the ordinary transition machine — the archive subcommand
is its own guarded entry point that also moves the file.

**The redesign loop (`IMPLEMENTED → REVIEW`)** is the re-entry edge that makes
mid-dev redesign possible. When a design flaw surfaces *after* implementation
starts — through the task-comprehension handshake, the in-dev issue dialog, or
the pre-PR gate — ORCH relays it to ARCH (R6 v3 direct edge), and ARCH pulls the
design back to REVIEW to revise it (or split/group it into new TRDDs) rather than
letting the team improvise around the flaw. Without this edge the dialog loops
have nowhere to route a surfaced design problem.

### Step 2: Check Current State

Before transitioning, verify the current state:

```bash
python scripts/amaa_design_lifecycle.py --uuid <UUID> --action check-state
```

### Step 3: Validate Proposed Transition

Check if a transition is valid:

```bash
python scripts/amaa_design_transition.py --uuid <UUID> --from <CURRENT> --to <TARGET> --validate
```

### Step 4: Execute State Transition

Perform the transition:

```bash
python scripts/amaa_design_lifecycle.py --uuid <UUID> --transition <TARGET_STATE>
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
python scripts/amaa_design_lifecycle.py --uuid <UUID> --action check-state
```

## State Transition Rules

### DRAFT to REVIEW

**Prerequisites:**
- All required sections completed
- Completeness checklist passed

```bash
python scripts/amaa_design_lifecycle.py --uuid <UUID> --transition REVIEW
```

### REVIEW to APPROVED

**Prerequisites:**
- All review comments resolved
- At least one reviewer approval

```bash
python scripts/amaa_design_lifecycle.py --uuid <UUID> --transition APPROVED
```

### REVIEW to DRAFT (Revision)

**When to use:** Design needs significant changes based on review feedback.

```bash
python scripts/amaa_design_lifecycle.py --uuid <UUID> --transition DRAFT
```

### APPROVED to IMPLEMENTED

**Prerequisites:**
- Implementation tasks created
- Resources allocated
- All requirements implemented, testing passed

```bash
python scripts/amaa_design_lifecycle.py --uuid <UUID> --transition IMPLEMENTED
```

### IMPLEMENTED to REVIEW (Redesign loop)

**When to use:** A design flaw surfaced *after* implementation started — raised
by a MEMBER during the task-comprehension handshake, the in-dev issue dialog, or
the pre-PR gate, and relayed to ARCH by ORCH. The design must be revised before
implementation can correctly continue.

**Prerequisites:**
- ARCH has confirmed the surfaced issue is a genuine design flaw (not an
  implementation question answerable in the dialog without a state change).
- The redesign intent is recorded (which requirement/assumption was wrong).

**On re-entry, ARCH either:**
- revises this design in place (then REVIEW → APPROVED → IMPLEMENTED again), or
- splits/groups it into new TRDDs (this design may become `SUPERSEDED`).

```bash
python scripts/amaa_design_lifecycle.py --uuid <UUID> --transition REVIEW
```

### IMPLEMENTED to ARCHIVED (archive subcommand)

**Prerequisites:**
- Completion report generated
- Stakeholders notified
- Only reachable via the `archive` subcommand — not `--transition` — from
  IMPLEMENTED, DEPRECATED, or SUPERSEDED (or `--force` to override)

```bash
python scripts/amaa_design_lifecycle.py archive --uuid <UUID>
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
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --action check-state
# Output: Current state: DRAFT

# Complete draft, submit for review
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition REVIEW
# Output: State transitioned: DRAFT -> REVIEW

# After review approval
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition APPROVED
# Output: State transitioned: REVIEW -> APPROVED

# Begin implementation
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition IMPLEMENTED
# Output: State transitioned: APPROVED -> IMPLEMENTED

# Archive for history (archive subcommand, not --transition)
python scripts/amaa_design_lifecycle.py archive --uuid design-api-20260130-abc123
# Output: State transitioned: IMPLEMENTED -> ARCHIVED (terminal state)
```

### Example: Revision After Review

```bash
# Design is in REVIEW but needs major changes
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --action check-state
# Output: Current state: REVIEW

# Return to DRAFT for revision
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition DRAFT
# Output: State transitioned: REVIEW -> DRAFT (revision)

# Make changes, then resubmit
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition REVIEW
# Output: State transitioned: DRAFT -> REVIEW
```

### Example: Mid-dev Redesign (the redesign loop)

```bash
# Design is IMPLEMENTED; a MEMBER surfaced a design flaw via ORCH
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --action check-state
# Output: Current state: IMPLEMENTED

# Pull the design back to REVIEW to redesign
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition REVIEW
# Output: State transitioned: IMPLEMENTED -> REVIEW (redesign loop)

# Revise the design, re-approve, resume implementation
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition APPROVED
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition IMPLEMENTED
```

### Example: Invalid Transition Error

```bash
# Attempt invalid transition: DRAFT -> APPROVED (skipping REVIEW)
python scripts/amaa_design_lifecycle.py --uuid design-api-20260130-abc123 --transition APPROVED
# Output: ERROR: Invalid state transition
# Cannot transition from DRAFT to APPROVED
# Valid transitions from DRAFT: REVIEW
```

## State Transition Matrix

| From State | To DRAFT | To REVIEW | To APPROVED | To IMPLEMENTED | To DEPRECATED | To SUPERSEDED | To ARCHIVED |
|------------|----------|-----------|-------------|-----------------|----------------|----------------|-------------|
| DRAFT | - | YES | NO | NO | YES | NO | NO |
| REVIEW | YES | - | YES | NO | YES | NO | NO |
| APPROVED | NO | NO | - | YES | YES | YES | NO |
| IMPLEMENTED | NO | YES | NO | - | YES | YES | archive-only |
| DEPRECATED | NO | NO | NO | NO | - | NO | archive-only |
| SUPERSEDED | NO | NO | NO | NO | NO | - | archive-only |
| ARCHIVED | NO | NO | NO | NO | NO | NO | - |

`IMPLEMENTED → REVIEW` is the redesign-loop re-entry edge (see the rule above).
`archive-only` means the transition is reachable exclusively through the
`archive` subcommand (or `--force`), never through `--transition`.

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
- [op-track-implementation.md](op-track-implementation.md) - APPROVED to IMPLEMENTED
- [op-accept-redesign-request.md](op-accept-redesign-request.md) - IMPLEMENTED to REVIEW (redesign loop)
- [op-archive-design.md](op-archive-design.md) - IMPLEMENTED/DEPRECATED/SUPERSEDED to ARCHIVED
