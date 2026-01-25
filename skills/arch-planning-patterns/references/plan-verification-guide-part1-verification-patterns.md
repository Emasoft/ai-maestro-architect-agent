# Plan Verification Guide - Part 1: Verification Patterns

## Table of Contents

1. [Mapping Verification Patterns to Plan Steps](#mapping-verification-patterns-to-plan-steps)
   - [Phase Completion Verification](#phase-completion-verification)
   - [Task Completion Criteria](#task-completion-criteria)

---

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

---

**Navigation**: [Back to Index](plan-verification-guide.md) | [Next: Checklist & Integration](plan-verification-guide-part2-checklist-integration.md)
