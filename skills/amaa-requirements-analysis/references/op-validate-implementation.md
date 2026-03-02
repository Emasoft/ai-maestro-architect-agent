---
operation: validate-implementation
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Validate Implementation Operation


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Identify Implementation to Validate](#step-1-identify-implementation-to-validate)
  - [Step 2: Execute Validate Command](#step-2-execute-validate-command)
  - [Step 3: Review Validation Report](#step-3-review-validation-report)
  - [Step 4: Address Gaps](#step-4-address-gaps)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Validating a Module Implementation](#example-validating-a-module-implementation)
  - [Example: Generated Validation Report](#example-generated-validation-report)
- [Validation Details](#validation-details)
- [Results Summary](#results-summary)
- [Detailed Results](#detailed-results)
  - [REQ-F001: User Login](#req-f001-user-login)
  - [REQ-F002: Password Reset](#req-f002-password-reset)
  - [REQ-F003: Two-Factor Authentication](#req-f003-two-factor-authentication)
  - [REQ-NF001: Response Time](#req-nf001-response-time)
- [Next Steps](#next-steps)
  - [Example: Validation with Failures](#example-validation-with-failures)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Verifying implementation meets user requirements
- Conducting requirement traceability checks
- Preparing for module completion sign-off
- Auditing compliance with original requirements
- Generating validation reports for stakeholders

This operation supports RULE 14 by ensuring implementations match original requirements.

## Prerequisites

- [ ] Requirements tracking initialized
- [ ] Implementation code/artifacts available
- [ ] USER_REQUIREMENTS.md documented
- [ ] Module to validate identified

## Procedure

### Step 1: Identify Implementation to Validate

Determine which module or implementation path to validate.

### Step 2: Execute Validate Command

```bash
python3 scripts/eaa_requirement_analysis.py validate \
  --project-root . \
  --implementation path/to/module/or/code
```

### Step 3: Review Validation Report

```bash
cat docs_dev/requirements/validations/validation-YYYYMMDD-HHMMSS.md
```

### Step 4: Address Gaps

If validation fails:
1. Identify missing requirements
2. Update implementation OR
3. Report requirement issue if requirement is infeasible

## Checklist

Copy this checklist and track your progress:

- [ ] Identify implementation to validate
- [ ] Ensure USER_REQUIREMENTS.md is current
- [ ] Execute validate command
- [ ] Review validation report
- [ ] Address any gaps or failures
- [ ] Re-validate after fixes
- [ ] Archive validation report

## Examples

### Example: Validating a Module Implementation

```bash
python3 scripts/eaa_requirement_analysis.py validate \
  --project-root . \
  --implementation src/auth/

# Expected output:
# Validating implementation: src/auth/
# Against requirements: USER_REQUIREMENTS.md
#
# Validation Results:
# +-----------------+----------+----------------------------------+
# | Requirement     | Status   | Notes                            |
# +-----------------+----------+----------------------------------+
# | REQ-F001        | PASS     | User login implemented           |
# | REQ-F002        | PASS     | Password reset implemented       |
# | REQ-F003        | PARTIAL  | 2FA not yet complete            |
# | REQ-NF001       | PASS     | Performance within threshold     |
# +-----------------+----------+----------------------------------+
#
# Summary: 3/4 PASS, 1/4 PARTIAL
#
# Report saved: docs_dev/requirements/validations/validation-20260115-143022.md
```

### Example: Generated Validation Report

```markdown
# Implementation Validation Report

## Validation Details
- **Date**: 2026-01-15T14:30:22
- **Implementation**: src/auth/
- **Requirements Source**: USER_REQUIREMENTS.md
- **Validator**: eaa_requirement_analysis.py

## Results Summary
- **Total Requirements**: 4
- **Passed**: 3 (75%)
- **Partial**: 1 (25%)
- **Failed**: 0 (0%)

## Detailed Results

### REQ-F001: User Login
- **Status**: PASS
- **Original Requirement**: "Allow users to login with email and password"
- **Implementation**: `src/auth/login.py`
- **Evidence**: Unit tests passing, integration test confirms functionality

### REQ-F002: Password Reset
- **Status**: PASS
- **Original Requirement**: "Support password reset via email link"
- **Implementation**: `src/auth/password_reset.py`
- **Evidence**: Email sending confirmed, token validation working

### REQ-F003: Two-Factor Authentication
- **Status**: PARTIAL
- **Original Requirement**: "Support 2FA with TOTP"
- **Implementation**: `src/auth/2fa.py` (incomplete)
- **Gap**: TOTP verification not implemented
- **Estimated Completion**: 2 hours

### REQ-NF001: Response Time
- **Status**: PASS
- **Original Requirement**: "API responses under 200ms"
- **Evidence**: Load test results show avg 85ms, p99 150ms

## Next Steps
1. Complete REQ-F003 implementation
2. Re-run validation
3. Proceed to module completion
```

### Example: Validation with Failures

```bash
python3 scripts/eaa_requirement_analysis.py validate \
  --project-root . \
  --implementation src/api/

# Output showing failures:
# Validation Results:
# +-----------------+----------+----------------------------------+
# | Requirement     | Status   | Notes                            |
# +-----------------+----------+----------------------------------+
# | REQ-F010        | FAIL     | Endpoint not found               |
# | REQ-F011        | PASS     | Data export working              |
# | REQ-NF005       | FAIL     | Security scan found issues       |
# +-----------------+----------+----------------------------------+
#
# VALIDATION FAILED: 2 requirements not met
#
# Action Required:
# - Fix failing requirements before marking module complete
# - Or report requirement issue if requirement is infeasible
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Validations folder not found | Tracking not initialized | Run init operation first |
| Implementation path not found | Invalid path | Verify implementation path exists |
| USER_REQUIREMENTS.md not found | Requirements not documented | Create USER_REQUIREMENTS.md first |
| Script not found | Plugin not loaded | Verify plugin is enabled |

## Related Operations

- [op-init-requirements-tracking.md](op-init-requirements-tracking.md) - Initialize tracking first
- [op-report-requirement-issue.md](op-report-requirement-issue.md) - Report infeasible requirements
- [op-approve-plan.md](op-approve-plan.md) - Approve plan before validation
