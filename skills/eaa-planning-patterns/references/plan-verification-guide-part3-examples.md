# Plan Verification Guide - Part 3: Examples

## Table of Contents

1. [Example 1: Verifying a Code Implementation Task](#example-1-verifying-a-code-implementation-task)
2. [Example 2: Verifying a Documentation Task](#example-2-verifying-a-documentation-task)
3. [Example 3: Verifying a Multi-Step Task](#example-3-verifying-a-multi-step-task)

---

## Example 1: Verifying a Code Implementation Task

**Task**: Implement password reset functionality

**Verification checklist**:

```markdown
## Task: Implement password reset functionality

### Task Description
Add password reset flow with email verification and secure token generation

### Verification Requirements
- [ ] Primary evidence: Test suite exit code - proves functionality works
- [ ] Secondary evidence: Code coverage report - proves adequate testing
- [ ] Exit code check: `pytest tests/test_password_reset.py`
- [ ] Human validation: Security review by @security-team

### Pre-verification Checklist
- [x] All dependencies completed and verified
- [x] Required resources available (test email server)
- [x] Test environment prepared (staging DB populated)
- [x] Verification tools installed (pytest, coverage)

### Evidence Collected

**Evidence 1: Test Results**
- Source: pytest execution on staging
- Timestamp: 2026-01-01T00:15:30Z
- Result: All 24 tests passed
- File/Link: `test-results/password-reset-2026-01-01.xml`

**Evidence 2: Coverage Report**
- Source: coverage.py analysis
- Timestamp: 2026-01-01T00:15:35Z
- Result: 94% coverage on auth module
- File/Link: `coverage/auth-module.html`

**Evidence 3: Security Review**
- Source: GitHub PR #456 review
- Timestamp: 2026-01-01T00:20:00Z
- Result: Approved with minor suggestions
- File/Link: https://github.com/org/repo/pull/456#review-12345

### Exit Code Verification
```bash
# Command executed
pytest tests/test_password_reset.py --cov=src/auth --cov-report=html

# Exit code
0

# Interpretation
All tests passed, no failures or errors
```

### Verification Result
- **Status**: PASSED
- **Verified by**: build-agent-07
- **Timestamp**: 2026-01-01T00:20:05Z
- **Confidence**: HIGH
- **Notes**: Security team suggested rate limiting on reset endpoint, tracked in TASK-457

### Dependencies Unblocked
- TASK-457: Add rate limiting to password reset
- TASK-458: Update password reset documentation
- TASK-459: Deploy password reset to production
```

---

## Example 2: Verifying a Documentation Task

**Task**: Write API integration guide

**Verification checklist**:

```markdown
## Task: Write API integration guide

### Task Description
Create comprehensive guide for integrating with our REST API, including authentication, rate limits, and examples

### Verification Requirements
- [ ] Primary evidence: File existence - proves doc was created
- [ ] Secondary evidence: Link validation - proves all links work
- [ ] Exit code check: `markdown-link-check docs/api-integration.md`
- [ ] Human validation: Technical writer review

### Pre-verification Checklist
- [x] All dependencies completed and verified
- [x] Required resources available (API specs, examples)
- [x] Test environment prepared (N/A for docs)
- [x] Verification tools installed (markdown-link-check, vale)

### Evidence Collected

**Evidence 1: File Creation**
- Source: Filesystem check
- Timestamp: 2026-01-01T00:10:00Z
- Result: File exists at docs/api-integration.md
- File/Link: `docs/api-integration.md` (3,421 bytes)

**Evidence 2: Link Validation**
- Source: markdown-link-check tool
- Timestamp: 2026-01-01T00:10:15Z
- Result: 23/23 links valid
- File/Link: `validation/link-check-2026-01-01.log`

**Evidence 3: Grammar Check**
- Source: vale linter
- Timestamp: 2026-01-01T00:10:20Z
- Result: 0 errors, 2 warnings (accepted)
- File/Link: `validation/vale-2026-01-01.log`

**Evidence 4: Technical Review**
- Source: Docs team review
- Timestamp: 2026-01-01T00:25:00Z
- Result: Approved
- File/Link: Internal review doc #789

### Exit Code Verification
```bash
# Command executed
markdown-link-check docs/api-integration.md

# Exit code
0

# Interpretation
All hyperlinks in document are valid and reachable
```

### Verification Result
- **Status**: PASSED
- **Verified by**: docs-review-agent
- **Timestamp**: 2026-01-01T00:25:10Z
- **Confidence**: HIGH
- **Notes**: None

### Dependencies Unblocked
- TASK-560: Publish API integration guide to public docs
- TASK-561: Add guide link to API homepage
```

---

## Example 3: Verifying a Multi-Step Task

**Task**: Migrate database from PostgreSQL 14 to 16

**Verification checklist**:

```markdown
## Task: Migrate database from PostgreSQL 14 to 16

### Task Description
Perform in-place upgrade of production PostgreSQL database from version 14.x to 16.x with zero data loss

### Verification Requirements
- [ ] Primary evidence: Migration script exit code - proves migration succeeded
- [ ] Secondary evidence: Data integrity checks - proves no data corruption
- [ ] Exit code check: `./scripts/verify-migration.sh`
- [ ] Human validation: DBA approval of migration results

### Pre-verification Checklist
- [x] All dependencies completed and verified
- [x] Required resources available (backup verified, downtime window approved)
- [x] Test environment prepared (migration tested on staging)
- [x] Verification tools installed (pg_dump, migration scripts)

### Evidence Collected

**Evidence 1: Migration Script Execution**
- Source: Production migration script
- Timestamp: 2026-01-01T02:00:00Z
- Result: Migration completed successfully
- File/Link: `logs/migration-2026-01-01-02-00.log`

**Evidence 2: Data Integrity Check**
- Source: Row count and checksum validation
- Timestamp: 2026-01-01T02:15:00Z
- Result: All tables match, checksums identical
- File/Link: `validation/data-integrity-2026-01-01.csv`

**Evidence 3: Application Health Check**
- Source: Application smoke tests
- Timestamp: 2026-01-01T02:20:00Z
- Result: All queries executing correctly
- File/Link: `test-results/post-migration-smoke.xml`

**Evidence 4: Performance Baseline**
- Source: Query performance comparison
- Timestamp: 2026-01-01T02:30:00Z
- Result: Performance improved 12% on average
- File/Link: `benchmarks/pg16-vs-pg14.html`

**Evidence 5: DBA Review**
- Source: Senior DBA final approval
- Timestamp: 2026-01-01T02:45:00Z
- Result: Approved, rollback no longer needed
- File/Link: Approval email thread

### Exit Code Verification
```bash
# Command executed
./scripts/verify-migration.sh --full-check

# Exit code
0

# Interpretation
Migration verification passed all checks:
- Database version: 16.1 ✓
- Row counts match: 100% ✓
- Checksums match: 100% ✓
- Indexes rebuilt: ✓
- Foreign keys valid: ✓
```

### Verification Result
- **Status**: PASSED
- **Verified by**: migration-orchestrator-agent + DBA-team
- **Timestamp**: 2026-01-01T02:45:30Z
- **Confidence**: HIGH
- **Notes**: Rollback window closed, pg14 instance can be decommissioned

### Dependencies Unblocked
- TASK-670: Decommission PostgreSQL 14 instance
- TASK-671: Update monitoring for PG16 metrics
- TASK-672: Document PG16 migration lessons learned
```

---

**Navigation**: [Back to Index](plan-verification-guide.md) | [Previous: Checklist & Integration](plan-verification-guide-part2-checklist-integration.md)
