# Plan Verification Guide

## Table of Contents

1. [Overview](#overview)
2. [Part 1: Verification Patterns](plan-verification-guide-part1-verification-patterns.md)
   - Phase Completion Verification
     - Architecture Phase verification requirements
     - Risk Phase verification requirements
     - Roadmap Phase verification requirements
     - Implementation Phase verification requirements
   - Task Completion Criteria
     - Code Task verification requirements
     - Documentation Task verification requirements
     - Review Task verification requirements
     - Deploy Task verification requirements
3. [Part 2: Checklist Template & Task Tracker Integration](plan-verification-guide-part2-checklist-integration.md)
   - Verification Checklist Template (copy-paste ready)
   - Integration with Task Tracker
     - Automatic Status Updates and transitions
     - Verification Script Integration (YAML config)
     - Blocking Verification Failures and unblocking process
4. [Part 3: Examples](plan-verification-guide-part3-examples.md)
   - Example 1: Verifying a Code Implementation Task
   - Example 2: Verifying a Documentation Task
   - Example 3: Verifying a Multi-Step Task
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [Related Documentation](#related-documentation)

---

## Overview

This guide explains how to apply verification-patterns to validate plan step completion. Effective verification ensures that each phase of planning and implementation is properly completed before moving to the next step, preventing cascading failures and ensuring quality outcomes.

Verification is the bridge between planning and execution. Every task in a plan must have clear completion criteria that can be objectively verified using evidence-based methods.

**Document Structure**:
- **Part 1**: Defines verification patterns for each planning phase and task type
- **Part 2**: Provides a reusable checklist template and task tracker integration guidance
- **Part 3**: Contains complete, realistic examples you can adapt

---

## Best Practices

### 1. Verify Early and Often
- Don't wait until task completion to start verification planning
- Define verification criteria when creating the task
- Build verification scripts alongside implementation

### 2. Automate Verification
- Prefer automated verification over manual checks
- Use exit codes as primary verification signal
- Collect evidence artifacts automatically

### 3. Make Verification Reproducible
- Verification should produce same result when re-run
- Document exact verification commands
- Version-control verification scripts

### 4. Fail Fast on Verification Failures
- Don't proceed with failed verifications
- Block dependent tasks immediately
- Require explicit re-verification after fixes

### 5. Document Verification Evidence
- Store all evidence artifacts in version control
- Reference evidence in task tracker
- Maintain audit trail of verification history

---

## Troubleshooting

### Verification Script Returns Non-Zero Exit Code
**Problem**: Verification script fails with non-zero exit code, but manual check shows task is complete.

**Diagnosis**:
- Check script logs for specific failure reason
- Verify script has correct permissions and dependencies
- Confirm script is testing the right environment/target

**Solution**:
- Fix script bug if verification logic is wrong
- Update verification criteria if expectations changed
- Re-run verification after fix

### Evidence Collection Fails
**Problem**: Cannot collect required evidence artifacts (files don't exist, API unreachable, etc.)

**Diagnosis**:
- Check if task actually completed (evidence should exist)
- Verify evidence collection tools are installed
- Confirm correct paths/URLs for evidence

**Solution**:
- Complete task if not actually done
- Install missing verification tools
- Update evidence paths in verification config

### Verification Passes But Task is Incomplete
**Problem**: Verification reports PASSED, but manual inspection shows task is not complete.

**Diagnosis**:
- Verification criteria too weak (false positive)
- Wrong verification pattern for task type
- Evidence doesn't prove what's claimed

**Solution**:
- Strengthen verification requirements
- Add additional verification checks
- Change to more appropriate verification pattern
- Require human validation for critical tasks

### Circular Verification Dependencies
**Problem**: Task A verification depends on Task B, but Task B verification depends on Task A.

**Diagnosis**:
- Tasks are too coupled
- Verification dependencies mirror implementation dependencies incorrectly
- Need to break circular dependency

**Solution**:
- Refactor tasks to remove circular dependency
- Verify tasks in integration (both together) instead of separately
- Reorder task execution to break cycle

---

## Related Documentation

- **[plan-verification-guide-part1-verification-patterns.md](plan-verification-guide-part1-verification-patterns.md)**: Verification patterns for phases and task types
- **[plan-verification-guide-part2-checklist-integration.md](plan-verification-guide-part2-checklist-integration.md)**: Task tracker integration and checklist template
- **[plan-file-linking.md](plan-file-linking.md)**: Plan-to-GitHub linking for traceability
- **[planning-checklist.md](planning-checklist.md)**: Planning phase checklist

---

## Part Files

| Part | File | Content |
|------|------|---------|
| Part 1 | [plan-verification-guide-part1-verification-patterns.md](plan-verification-guide-part1-verification-patterns.md) | Verification patterns for phases and task types |
| Part 2 | [plan-verification-guide-part2-checklist-integration.md](plan-verification-guide-part2-checklist-integration.md) | Checklist template and task tracker integration |
| Part 3 | [plan-verification-guide-part3-examples.md](plan-verification-guide-part3-examples.md) | Complete worked examples |
