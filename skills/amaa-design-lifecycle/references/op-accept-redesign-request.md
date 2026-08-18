---
operation: accept-redesign-request
---

# Accept a Redesign Request (the redesign loop)

## Contents

- When to Use
- Prerequisites
- Procedure
- Checklist
- Related Operations
- Related Templates

## When to Use

A MEMBER surfaced a design problem *after* implementation started — through one
of the three dialog loops (task-comprehension handshake, in-dev issue dialog, or
pre-PR gate) — and ORCH relayed it to ARCH. Use this operation to decide what to
do with the surfaced issue and, when it is a genuine design flaw, to drive the
`IMPLEMENTED → REVIEW` redesign loop.

This is the ARCHITECT's half of the loop. The MEMBER never edits the design and
never improvises around the flaw; the issue comes to ARCH and ARCH owns the
design surface (single-writer-per-domain).

## Prerequisites

- The design document is currently in `IMPLEMENTED` (or `approved`).
- ORCH has relayed a concrete description of the surfaced issue (which
  requirement, assumption, interface, or sequencing step is wrong), per R6 v3
  (within-team ORCH↔ARCH is a direct edge; MANAGER is not in this loop).

## Procedure

### Step 1: Classify the surfaced issue

| Classification | Signal | Action |
|---|---|---|
| **Implementation question** | The design is sound; the MEMBER needs clarification on *how* | Answer in the dialog. **No state change.** |
| **Genuine design flaw** | A requirement/assumption/interface in the design is wrong or unbuildable | Drive the redesign loop (Step 2). |
| **Scope gap** | The design is correct but incomplete — a prerequisite (NPT) or effect (EHT) was missed | Author the missing TRDD(s); the parent may stay `IMPLEMENTED` if unblocked, else re-enter REVIEW. |

Only a genuine design flaw (or a scope gap that invalidates the current design)
re-enters REVIEW. Do not bounce the design to REVIEW for a question you can
answer in one message.

### Step 2: Re-enter REVIEW

```bash
python scripts/amaa_design_lifecycle.py --uuid <UUID> --transition REVIEW
# Output: State transitioned: IMPLEMENTED -> REVIEW (redesign loop)
```

Record in the design body WHY it re-entered REVIEW (which assumption was wrong)
so the revision history is auditable.

### Step 3: Revise in place OR split/group into new TRDDs

- **Revise in place** when the flaw is local: edit the design, then
  REVIEW → APPROVED → IMPLEMENTED again. Implementation resumes against the
  corrected design.
- **Split/group** when the flaw means the work should be re-decomposed: author
  the new TRDD(s) (1→N split or N→1 group per the TRDD rules), set this design's
  `superseded-by:`, and transition it to `superseded`. The new TRDDs enter their
  own lifecycle.

### Step 4: Notify ORCH the design is re-approved (or superseded)

Send the design-handoff / revision message back through ORCH so the MEMBER
implements against the corrected design. The MEMBER does NOT resume until ARCH
signals the redesign is complete.

## Checklist

- [ ] Issue classified (implementation question vs design flaw vs scope gap)
- [ ] If design flaw: re-entered REVIEW with a recorded reason
- [ ] Revised in place OR split/grouped into new TRDD(s)
- [ ] Re-approved (or marked superseded) and ORCH notified
- [ ] MEMBER unblocked against the corrected design

## Related Operations

- [op-manage-state-transitions.md](op-manage-state-transitions.md) - the `IMPLEMENTED → REVIEW` edge
- [op-submit-design-review.md](op-submit-design-review.md) - REVIEW mechanics
- [op-approve-design.md](op-approve-design.md) - re-approval after revision

## Related Templates

- [dialog-loop-comprehension-handshake.md](../templates/dialog-loop-comprehension-handshake.md)
- [dialog-loop-in-dev-issue.md](../templates/dialog-loop-in-dev-issue.md)
- [dialog-loop-pre-pr-gate.md](../templates/dialog-loop-pre-pr-gate.md)
