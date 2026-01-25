# Plan Verification Guide - Part 1: Patterns and Integration

## Table of Contents

1. [Overview](#overview)
2. [Mapping Verification Patterns to Plan Steps](#mapping-verification-patterns-to-plan-steps)
   - [Phase Completion Verification](#phase-completion-verification)
   - [Task Completion Criteria](#task-completion-criteria)
3. [Verification Checklist Template](#verification-checklist-template)
4. [Integration with Task Tracker](#integration-with-task-tracker)
   - [Automatic Status Updates](#automatic-status-updates)
   - [Verification Script Integration](#verification-script-integration)
   - [Blocking Verification Failures](#blocking-verification-failures)

---

**Related Parts:**
- [Part 2: Checklist Integration](plan-verification-guide-part2-checklist-integration.md)
- [Part 3: Examples](plan-verification-guide-part3-examples.md)
- [Index](plan-verification-guide.md)

---

## Overview

This guide explains how to apply verification-patterns to validate plan step completion. Effective verification ensures that each phase of planning and implementation is properly completed before moving to the next step, preventing cascading failures and ensuring quality outcomes.

Verification is the bridge between planning and execution. Every task in a plan must have clear completion criteria that can be objectively verified using evidence-based methods.

## Mapping Verification Patterns to Plan Steps

### Phase Completion Verification

Each planning phase requires specific verification patterns to ensure proper completion:

#### Architecture Phase
- **Primary pattern**: Evidence-based verification for design decisions
- **What to verify**: Design documents exist, diagrams are complete, technical decisions are documented
- **Evidence required**: Architecture diagrams (SVG/PNG), design decision records (ADR format), component specifications
- **Verification method**: File existence + content review + stakeholder approval

#### Risk Phase
- **Primary pattern**: Integration verification for risk mitigation tests
- **What to verify**: Each identified risk has mitigation strategy, critical risks have tested mitigation
- **Evidence required**: Risk register with mitigations, test results for high-priority risks
- **Verification method**: Risk coverage analysis + mitigation test exit codes

#### Roadmap Phase
- **Primary pattern**: Consistency verification for timeline validation
- **What to verify**: Milestones are achievable, dependencies are properly sequenced, timeline is realistic
- **Evidence required**: Dependency graph, milestone definitions, resource allocation plan
- **Verification method**: Dependency analysis + timeline feasibility check + resource validation

#### Implementation Phase
- **Primary pattern**: Exit-code verification for code changes
- **What to verify**: Code changes pass tests, meet quality standards, are properly documented
- **Evidence required**: Test results (exit code 0), code review approval, updated documentation
- **Verification method**: Automated tests + linting + code review + documentation checks

### Task Completion Criteria

Each task type requires specific verification approaches to confirm completion:

#### Code Task
**Verification requirements**:
- Exit code from automated tests (must be 0)
- Evidence of test coverage (minimum threshold met)
- Code review approval (GitHub PR approval or equivalent)
- Linting/formatting checks passed

**Verification steps**:
1. Run test suite: `pytest tests/` or equivalent
2. Check coverage: `coverage report --fail-under=80`
3. Verify code review: Check PR approval status
4. Run linters: `ruff check`, `mypy`, etc.

**Completion criteria**: All verifications PASSED

#### Documentation Task
**Verification requirements**:
- Evidence of file creation (file exists at expected path)
- Content completeness (all required sections present)
- Link validation (all internal/external links work)
- Spelling/grammar check passed

**Verification steps**:
1. Verify file exists: `test -f path/to/doc.md`
2. Check required sections: Parse markdown headers
3. Validate links: Use link checker tool
4. Grammar check: Run automated grammar validator

**Completion criteria**: File exists, sections complete, links valid

#### Review Task
**Verification requirements**:
- Approval evidence (GitHub review, comment, or explicit approval)
- All review comments addressed
- Changes requested are implemented

**Verification steps**:
1. Check review status via API or UI
2. Verify all comment threads resolved
3. Confirm approver has proper authority

**Completion criteria**: Approved by authorized reviewer

#### Deploy Task
**Verification requirements**:
- Exit code from deploy script (must be 0)
- Health check endpoint responding
- Smoke tests passing in target environment
- Rollback plan verified

**Verification steps**:
1. Execute deploy script: `./deploy.sh production`
2. Health check: `curl -f https://app.example.com/health`
3. Run smoke tests: `pytest tests/smoke/`
4. Verify rollback: Check rollback script exists and is tested

**Completion criteria**: Deploy successful, health checks pass, smoke tests pass

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

**Continue to:** [Part 2: Checklist Integration](plan-verification-guide-part2-checklist-integration.md)
