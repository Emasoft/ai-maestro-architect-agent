# Design States

## Table of Contents

- State Definitions
- The redesign loop (mid-dev re-entry)

## State Definitions

| State | Description | Transitions |
|-------|-------------|-------------|
| DRAFT | Initial creation | -> REVIEW |
| REVIEW | Under review | -> APPROVED / -> DRAFT |
| APPROVED | Ready for implementation | -> IMPLEMENTING |
| IMPLEMENTING | Being implemented | -> COMPLETED / -> REVIEW (mid-dev redesign) |
| COMPLETED | Fully implemented | -> ARCHIVED |
| ARCHIVED | Historical reference | (terminal) |

## The redesign loop (mid-dev re-entry)

`IMPLEMENTING -> REVIEW` is the **redesign loop**. It exists so that when a
design flaw surfaces *after* implementation has started — during the
task-comprehension handshake, the in-dev issue dialog, or the pre-PR gate —
the ARCHITECT can pull the design back into REVIEW, revise it (or split/group
it into new TRDDs), and re-approve, instead of letting the team silently
improvise around the flaw. Without this edge the design state machine is a
one-way street and the dialog loops have nowhere to send a surfaced design
problem.

Who triggers it: ORCH relays a MEMBER-surfaced design issue to ARCH (R6 v3 —
within-team ORCH↔ARCH is a direct edge). ARCH decides whether the issue is a
genuine design flaw (→ re-enter REVIEW) or an implementation question (→ answer
in the dialog, no state change).
