---
operation: approve-design
procedure: proc-approve-design
workflow-instruction: Step 9 - Design Approval
parent-skill: eaa-design-lifecycle
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Approve Design

## When to Use

Use this operation when:
- A design document has been reviewed and all comments resolved
- Reviewers have signed off on the design
- The design is ready to be approved for implementation

## Prerequisites

- Design document is in REVIEW state
- All review comments have been addressed and resolved
- At least one reviewer has approved the design
- No blocking issues remain open

## Procedure

### Step 1: Verify All Review Comments Resolved

Check that all review comments have been addressed:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action check-review-status
```

Expected output: "All review comments resolved. Ready for approval."

### Step 2: Collect Reviewer Approvals

Verify that reviewers have approved:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action list-approvals
```

At minimum, require approval from:
- Technical lead or architect
- Domain expert (if applicable)

### Step 3: Update State to APPROVED

Transition the design from REVIEW to APPROVED:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition APPROVED
```

This command:
- Validates all comments are resolved
- Validates at least one approval exists
- Updates the frontmatter status field
- Records the approval timestamp and approvers

### Step 4: Create Implementation Tasks

Generate GitHub Issues or task entries for implementation:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action create-implementation-tasks
```

This creates tasks based on the module breakdown in the design document.

### Step 5: Notify Implementers

Alert the implementation team that the design is approved and ready:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action notify-implementers
```

### Step 6: Link to GitHub Issues

Associate the design with GitHub Issues for traceability:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action link-github-issues \
  --issues "123,124,125"
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify all review comments are resolved
- [ ] Confirm reviewer approvals (minimum 1 required)
- [ ] Check no blocking issues remain
- [ ] Transition state to APPROVED: `--transition APPROVED`
- [ ] Verify state change in frontmatter and index
- [ ] Create implementation tasks from design modules
- [ ] Link to relevant GitHub Issues
- [ ] Notify implementation team
- [ ] Document approval in design history

## Examples

### Example: Approve Authentication Design

```bash
# Step 1: Check review status
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action check-review-status
# Output: All 5 review comments resolved. Ready for approval.

# Step 2: List approvals
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action list-approvals
# Output:
# Approvals:
# - SecurityLead: APPROVED (2026-02-04)
# - BackendLead: APPROVED (2026-02-05)

# Step 3: Transition to APPROVED
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --transition APPROVED
# Output: State transitioned: REVIEW -> APPROVED

# Step 4: Create implementation tasks
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action create-implementation-tasks
# Output:
# Created 4 implementation tasks:
# - Task 1: Implement auth-service module
# - Task 2: Implement user-store module
# - Task 3: Implement token-manager module
# - Task 4: Integration testing

# Step 5: Link to GitHub Issues
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action link-github-issues \
  --issues "156,157,158,159"
# Output: Linked design to GitHub Issues #156, #157, #158, #159
```

### Example: Approval Record in Design Document

After approval, the design document should include:

```markdown
## Approval Record

**Status:** APPROVED
**Approval Date:** 2026-02-05

### Approvers
| Reviewer | Decision | Date | Comments |
|----------|----------|------|----------|
| SecurityLead | APPROVED | 2026-02-04 | Security considerations adequately addressed |
| BackendLead | APPROVED | 2026-02-05 | Architecture aligns with backend standards |

### Linked Issues
- #156 - Implement auth-service module
- #157 - Implement user-store module
- #158 - Implement token-manager module
- #159 - Integration testing
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Unresolved comments | Not all review comments addressed | Resolve all comments before approval |
| No approvals found | No reviewer has approved | Obtain at least one reviewer approval |
| Invalid state transition | Design not in REVIEW state | Can only transition to APPROVED from REVIEW |
| Task creation failed | Module breakdown missing | Ensure design has module breakdown section |
| GitHub linking failed | Invalid issue numbers | Verify issue numbers exist in repository |

## Related Operations

- [op-submit-design-review.md](op-submit-design-review.md) - Previous step in workflow
- [op-track-implementation.md](op-track-implementation.md) - Next step after approval
- [op-manage-state-transitions.md](op-manage-state-transitions.md) - State transition rules
