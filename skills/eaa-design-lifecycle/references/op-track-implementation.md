---
operation: track-implementation
procedure: proc-handle-feedback
workflow-instruction: Step 15 - Implementation Tracking
parent-skill: eaa-design-lifecycle
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Track Implementation


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Update State to IMPLEMENTING](#step-1-update-state-to-implementing)
  - [Step 2: Monitor Implementation Progress](#step-2-monitor-implementation-progress)
  - [Step 3: Update Design if Changes Needed](#step-3-update-design-if-changes-needed)
  - [Step 4: Maintain Requirements Traceability](#step-4-maintain-requirements-traceability)
  - [Step 5: Document Deviations](#step-5-document-deviations)
  - [Step 6: Generate Progress Report](#step-6-generate-progress-report)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Track Authentication System Implementation](#example-track-authentication-system-implementation)
  - [Example: Deviation Record Format](#example-deviation-record-format)
- [Implementation Deviations](#implementation-deviations)
  - [Deviation 1](#deviation-1)
  - [Deviation 2](#deviation-2)
  - [Example: Traceability Matrix](#example-traceability-matrix)
- [Requirements Traceability](#requirements-traceability)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- A design has been approved and implementation has started
- You need to monitor progress of implementation tasks
- The design needs updates based on implementation findings
- Requirements traceability needs to be maintained
- Deviations from the design need to be documented

## Prerequisites

- Design document is in APPROVED or IMPLEMENTING state
- Implementation tasks have been created and linked
- Access to GitHub Issues or task tracking system
- Understanding of the design's module breakdown

## Procedure

### Step 1: Update State to IMPLEMENTING

When implementation begins, transition the design state:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition IMPLEMENTING
```

### Step 2: Monitor Implementation Progress

Track the status of implementation tasks:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action check-progress
```

This shows:
- Tasks completed vs total
- Percentage complete
- Blocked tasks
- Overdue tasks

### Step 3: Update Design if Changes Needed

If implementation reveals necessary changes to the design:

1. Document the change reason
2. Update the design document
3. Record the deviation

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action record-deviation \
  --reason "API endpoint structure changed for performance" \
  --section "API Specifications"
```

### Step 4: Maintain Requirements Traceability

Link requirements to implementation artifacts:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action update-traceability \
  --requirement "REQ-AUTH-001" \
  --artifact "src/auth/service.py"
```

### Step 5: Document Deviations

When implementation deviates from the design, document it:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action document-deviation \
  --description "Changed token expiry from 1 hour to 30 minutes" \
  --reason "Security requirement update from security team" \
  --impact "Minor - configuration change only"
```

### Step 6: Generate Progress Report

Create a status report for stakeholders:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action generate-report
```

## Checklist

Copy this checklist and track your progress:

- [ ] Transition state to IMPLEMENTING when work begins
- [ ] Monitor task completion progress weekly
- [ ] Document any design deviations immediately
- [ ] Update requirements traceability matrix
- [ ] Generate progress reports for stakeholders
- [ ] Review blocked tasks and escalate if needed
- [ ] Verify implementation matches design intent
- [ ] Update design document with implementation learnings

## Examples

### Example: Track Authentication System Implementation

```bash
# Step 1: Begin implementation
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --transition IMPLEMENTING
# Output: State transitioned: APPROVED -> IMPLEMENTING

# Step 2: Check progress (weekly)
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action check-progress
# Output:
# Implementation Progress: design-auth-20260130-abc123
# Tasks: 3/4 complete (75%)
# - [x] auth-service module
# - [x] user-store module
# - [x] token-manager module
# - [ ] Integration testing (IN PROGRESS)
# Blocked: 0
# Overdue: 0

# Step 3: Record a deviation
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action record-deviation \
  --reason "Added rate limiting to auth endpoints" \
  --section "API Specifications"
# Output: Deviation recorded in design history

# Step 4: Update traceability
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action update-traceability \
  --requirement "REQ-AUTH-001" \
  --artifact "src/auth/service.py:authenticate()"
# Output: Traceability updated: REQ-AUTH-001 -> src/auth/service.py:authenticate()
```

### Example: Deviation Record Format

```markdown
## Implementation Deviations

### Deviation 1
**Date:** 2026-02-10
**Section:** API Specifications
**Description:** Added rate limiting to authentication endpoints
**Reason:** Security team requirement after initial design
**Impact:** Low - additive change, no breaking changes
**Approved By:** SecurityLead

### Deviation 2
**Date:** 2026-02-12
**Section:** Token Management
**Description:** Token expiry changed from 1 hour to 30 minutes
**Reason:** Corporate security policy update
**Impact:** Low - configuration change
**Approved By:** SecurityLead
```

### Example: Traceability Matrix

```markdown
## Requirements Traceability

| Requirement ID | Requirement | Implementation Artifact | Status |
|----------------|-------------|------------------------|--------|
| REQ-AUTH-001 | User login | src/auth/service.py:authenticate() | Complete |
| REQ-AUTH-002 | Token refresh | src/auth/token_manager.py:refresh() | Complete |
| REQ-AUTH-003 | Password reset | src/auth/password.py:reset() | In Progress |
| REQ-AUTH-004 | Session logout | src/auth/service.py:logout() | Complete |
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Invalid state transition | Design not in APPROVED state | Must be APPROVED before IMPLEMENTING |
| Progress check failed | No linked tasks found | Create and link implementation tasks first |
| Traceability update failed | Invalid requirement ID | Verify requirement exists in requirements document |
| Deviation not recorded | Missing required fields | Provide description, reason, and section |
| Report generation failed | No progress data | Ensure tasks are linked and have status updates |

## Related Operations

- [op-approve-design.md](op-approve-design.md) - Previous step in workflow
- [op-archive-design.md](op-archive-design.md) - Next step after completion
- [op-manage-state-transitions.md](op-manage-state-transitions.md) - State transition rules
