# Plan Verification Guide - Part 2: Checklist Template & Task Tracker Integration

## Table of Contents

1. [Verification Checklist Template](#verification-checklist-template)
2. [Integration with Task Tracker](#integration-with-task-tracker)
   - [Automatic Status Updates](#automatic-status-updates)
   - [Verification Script Integration](#verification-script-integration)
   - [Blocking Verification Failures](#blocking-verification-failures)

---

## Verification Checklist Template

Use this template for every task to ensure consistent verification:

```markdown
## Task: {task-name}

### Task Description
{Brief description of what this task accomplishes}

### Verification Requirements
- [ ] Primary evidence: {type} - {what it proves}
- [ ] Secondary evidence: {type} - {additional validation}
- [ ] Exit code check: {script or command to run}
- [ ] Human validation: {what requires manual review}

### Pre-verification Checklist
- [ ] All dependencies completed and verified
- [ ] Required resources available
- [ ] Test environment prepared
- [ ] Verification tools installed

### Evidence Collected

**Evidence 1: {evidence-type}**
- Source: {where evidence was collected}
- Timestamp: {when collected}
- Result: {what it shows}
- File/Link: {reference to evidence artifact}

**Evidence 2: {evidence-type}**
- Source: {where evidence was collected}
- Timestamp: {when collected}
- Result: {what it shows}
- File/Link: {reference to evidence artifact}

**Evidence 3: {evidence-type}** (if applicable)
- Source: {where evidence was collected}
- Timestamp: {when collected}
- Result: {what it shows}
- File/Link: {reference to evidence artifact}

### Exit Code Verification
```bash
# Command executed
{command}

# Exit code
{exit-code}

# Interpretation
{what this exit code means}
```

### Verification Result
- **Status**: PASSED / FAILED / BLOCKED
- **Verified by**: {agent-name or human-name}
- **Timestamp**: {ISO-8601 timestamp}
- **Confidence**: HIGH / MEDIUM / LOW
- **Notes**: {any additional context or caveats}

### Failure Analysis (if FAILED)
- **Failure mode**: {what went wrong}
- **Root cause**: {why it failed}
- **Remediation plan**: {what needs to be done}
- **Retry conditions**: {when to retry verification}

### Dependencies Unblocked (if PASSED)
- {list of tasks that can now proceed}
- {tasks that were waiting on this verification}
```

---

## Integration with Task Tracker

### Automatic Status Updates

Verification results should automatically update task tracker status:

**Status transitions on verification PASS**:
- `in-progress` → `verify-ready` (task implementation complete, awaiting verification)
- `verify-ready` → `verified` (verification passed)
- `verified` → `completed` (all dependencies verified, task fully complete)

**Status transitions on verification FAIL**:
- `verify-ready` → `in-progress` (verification failed, needs rework)
- `blocked` → `in-progress` (blocking issue resolved, can retry)

**Status transitions on verification BLOCKED**:
- `verify-ready` → `blocked` (cannot verify due to external dependency)

### Verification Script Integration

Task tracker should support verification script fields:

```yaml
task:
  id: "TASK-123"
  name: "Implement user authentication"
  status: "verify-ready"
  verification:
    script: "tests/verify_auth.sh"
    required_exit_code: 0
    evidence_artifacts:
      - "test-results/auth-tests.xml"
      - "coverage/auth-coverage.html"
    approver: "security-team"
```

When verification runs:
1. Execute `verification.script`
2. Check exit code matches `required_exit_code`
3. Collect `evidence_artifacts`
4. Request approval from `approver` if specified
5. Update task status based on results

### Blocking Verification Failures

**Critical verification failures should block dependent tasks**:

```
Task A (FAILED verification)
  ↓ blocks
Task B (cannot start)
  ↓ blocks
Task C (cannot start)
```

**Blocking behavior**:
- Tasks with failed verification cannot transition to `completed`
- Dependent tasks cannot start until blocker is `verified`
- Task tracker shows blocked dependency chain
- Notifications sent to task owners and blockers

**Unblocking process**:
1. Fix root cause of verification failure
2. Re-run verification
3. On PASS, automatically unblock dependent tasks
4. Notify previously blocked task owners

---

**Navigation**: [Back to Index](plan-verification-guide.md) | [Previous: Verification Patterns](plan-verification-guide-part1-verification-patterns.md) | [Next: Examples](plan-verification-guide-part3-examples.md)
