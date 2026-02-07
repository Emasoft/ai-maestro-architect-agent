---
operation: archive-design
procedure: proc-handle-feedback
workflow-instruction: Step 15 - Design Archival
parent-skill: eaa-design-lifecycle
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Complete and Archive Design

## When to Use

Use this operation when:
- All requirements from the design have been implemented
- Implementation has been verified and tested
- The design document needs to be archived for historical reference
- The project or feature is complete

## Prerequisites

- Design document is in IMPLEMENTING or COMPLETED state
- All implementation tasks are complete
- Verification testing has passed
- No outstanding deviations require resolution

## Procedure

### Step 1: Verify All Requirements Implemented

Check that every requirement in the design has been implemented:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action verify-completion
```

This checks:
- All requirements have linked artifacts
- All tasks are marked complete
- No blocking issues remain

### Step 2: Update State to COMPLETED

Transition the design from IMPLEMENTING to COMPLETED:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition COMPLETED
```

### Step 3: Create Completion Report

Generate a final report documenting the implementation:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action create-completion-report
```

The report includes:
- Requirements coverage summary
- Deviations summary
- Implementation timeline
- Lessons learned

### Step 4: Archive to Historical Folder

Move the design document to the archive:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --action archive
```

This:
- Moves the document to `docs_dev/design/completed/`
- Updates the design index with archived status
- Preserves all history and metadata

### Step 5: Update Design Index

Ensure the design index reflects the archived status:

```bash
python scripts/eaa_design_lifecycle.py --uuid <UUID> --transition ARCHIVED
```

### Step 6: Final State - ARCHIVED

The design is now in terminal ARCHIVED state. It serves as:
- Historical reference
- Template for similar future designs
- Documentation for maintenance teams

## Checklist

Copy this checklist and track your progress:

- [ ] Verify all requirements are implemented
- [ ] Confirm all tasks are complete
- [ ] Run final verification: `--action verify-completion`
- [ ] Transition to COMPLETED state
- [ ] Generate completion report
- [ ] Review completion report with stakeholders
- [ ] Archive design document to `completed/` folder
- [ ] Transition to ARCHIVED state
- [ ] Update design index
- [ ] Notify stakeholders of completion

## Examples

### Example: Archive Authentication Design

```bash
# Step 1: Verify completion
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action verify-completion
# Output:
# Completion Verification: design-auth-20260130-abc123
# Requirements: 4/4 implemented (100%)
# Tasks: 4/4 complete (100%)
# Deviations: 2 documented and approved
# Status: READY FOR COMPLETION

# Step 2: Transition to COMPLETED
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --transition COMPLETED
# Output: State transitioned: IMPLEMENTING -> COMPLETED

# Step 3: Create completion report
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action create-completion-report
# Output: Completion report saved to docs_dev/design/completed/design-auth-20260130-abc123-report.md

# Step 4: Archive
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --action archive
# Output: Design archived to docs_dev/design/completed/design-auth-20260130-abc123.md

# Step 5: Final state
python scripts/eaa_design_lifecycle.py --uuid design-auth-20260130-abc123 --transition ARCHIVED
# Output: State transitioned: COMPLETED -> ARCHIVED (terminal state)
```

### Example: Completion Report Format

```markdown
# Design Completion Report

**Design UUID:** design-auth-20260130-abc123
**Title:** User Authentication System Design
**Completed:** 2026-02-20

## Summary

The user authentication system design has been fully implemented. All 4 requirements
have been satisfied with 2 documented deviations.

## Requirements Coverage

| Requirement | Status | Artifact |
|-------------|--------|----------|
| REQ-AUTH-001 | Complete | src/auth/service.py |
| REQ-AUTH-002 | Complete | src/auth/token_manager.py |
| REQ-AUTH-003 | Complete | src/auth/password.py |
| REQ-AUTH-004 | Complete | src/auth/service.py |

## Deviations Summary

| # | Description | Impact |
|---|-------------|--------|
| 1 | Added rate limiting | Low |
| 2 | Token expiry reduced | Low |

## Timeline

- **Design Created:** 2026-01-30
- **Review Completed:** 2026-02-05
- **Approved:** 2026-02-05
- **Implementation Started:** 2026-02-06
- **Implementation Completed:** 2026-02-18
- **Archived:** 2026-02-20

Total Duration: 21 days

## Lessons Learned

1. Rate limiting should be considered in initial design
2. Security team should review designs earlier in process
3. Module breakdown was accurate - implementation followed design closely
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Verification failed | Outstanding requirements | Complete all requirements before archival |
| Incomplete tasks | Tasks still in progress | Finish all implementation tasks |
| Invalid state transition | Design not in IMPLEMENTING state | Must be IMPLEMENTING before COMPLETED |
| Archive failed | Permission denied | Check write access to completed/ directory |
| Report generation failed | Missing data | Ensure all tracking data is present |

## Related Operations

- [op-track-implementation.md](op-track-implementation.md) - Previous step in workflow
- [op-manage-state-transitions.md](op-manage-state-transitions.md) - State transition rules
- [op-create-design-document.md](op-create-design-document.md) - Start new design cycle
