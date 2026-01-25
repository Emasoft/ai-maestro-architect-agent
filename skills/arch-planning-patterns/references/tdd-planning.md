# Test-Driven Development (TDD) Planning Requirements

## Table of Contents

- 1. TDD Planning Principles
  - 1.1 Test strategy first - Defining tests before implementation
  - 1.2 TDD phases in timeline - Including RED-GREEN-REFACTOR in task breakdown
  - 1.3 Commit pattern - TDD-specific commit messages
- 2. TDD Phase Planning
  - 2.1 RED phase planning questions
  - 2.2 GREEN phase planning questions
  - 2.3 REFACTOR phase planning questions
- 3. TDD Task Template Extension
  - 3.1 Tests to write section
  - 3.2 Implementation scope section
  - 3.3 Refactoring candidates section
- 4. TDD Verification Checklist
  - 4.1 Pre-completion verification items
- 5. Integration with Planning Phases
  - 5.1 TDD in Architecture Design
  - 5.2 TDD in Risk Identification
  - 5.3 TDD in Roadmap Creation
  - 5.4 TDD in Implementation Planning

---

## 1. TDD Planning Principles

When planning code implementation tasks, incorporate Test-Driven Development methodology into your planning documents.

### 1.1 Test Strategy First

Define what tests will be written before implementation:
- Specify test types (unit, integration, end-to-end)
- Define test coverage goals (minimum % coverage)
- Identify edge cases and error conditions to test
- Document test data requirements

### 1.2 TDD Phases in Timeline

Include RED-GREEN-REFACTOR cycle in task breakdown:
- **RED Phase**: Write failing tests that define expected behavior
- **GREEN Phase**: Write minimum code to pass tests
- **REFACTOR Phase**: Improve code quality while maintaining passing tests

### 1.3 Commit Pattern

Require TDD-specific commit messages:
- RED: `test: add failing test for [behavior]`
- GREEN: `feat: implement [feature] to pass tests`
- REFACTOR: `refactor: improve [component] while maintaining tests`

---

## 2. TDD Phase Planning

| Phase | Planning Question | Output Required |
|-------|-------------------|-----------------|
| RED | What behavior needs testing? | Test specification with expected outcomes |
| GREEN | What's the minimum implementation? | Implementation scope limited to test requirements |
| REFACTOR | What can be improved? | Refactoring candidates (must have tests) |

### 2.1 RED Phase Planning Questions

- What is the expected behavior?
- What inputs does the function accept?
- What outputs should it produce?
- What error conditions exist?
- What edge cases need coverage?

### 2.2 GREEN Phase Planning Questions

- What is the minimum code to pass the test?
- What dependencies are required?
- What is out of scope for this phase?

### 2.3 REFACTOR Phase Planning Questions

- What code duplication exists?
- What naming can be improved?
- What performance optimizations are possible (with test coverage)?
- What design patterns apply?

---

## 3. TDD Task Template Extension

When creating tasks in implementation planning, include this TDD section:

```markdown
## TDD Plan for Task [ID]

### Tests to Write (RED Phase)
1. Test: [behavior description] - Expected: [outcome]
2. Test: [error condition] - Expected: [error response]
3. Test: [edge case] - Expected: [handling behavior]

### Implementation Scope (GREEN Phase)
- Minimum code needed to pass tests
- No additional features beyond test requirements
- Focus on passing tests, not perfection

### Refactoring Candidates (REFACTOR Phase)
- Code duplication to extract
- Naming improvements
- Performance optimizations (only if tests exist)
- Design pattern applications
```

---

## 4. TDD Verification Checklist

Before marking implementation task complete:

- [ ] Tests written before implementation code
- [ ] All tests fail initially (RED phase verified)
- [ ] Implementation makes tests pass (GREEN phase verified)
- [ ] Code refactored with tests still passing (REFACTOR phase verified)
- [ ] Test coverage meets defined threshold
- [ ] Commit messages follow TDD pattern
- [ ] No untested code paths in critical logic

---

## 5. Integration with Planning Phases

### 5.1 TDD in Architecture Design

Define testability requirements:
- Identify components that need dependency injection for testing
- Plan test doubles (mocks, stubs, fakes) for external dependencies
- Design interfaces for test isolation

### 5.2 TDD in Risk Identification

Include testing risks:

| Risk | Mitigation |
|------|------------|
| Insufficient test coverage | Enforce coverage thresholds in CI |
| Slow tests blocking development | Separate fast/slow test suites |
| Flaky tests | Test stability verification in code review |

### 5.3 TDD in Roadmap Creation

Allocate time for TDD:
- Add buffer time for test writing (typically 30-50% of implementation time)
- Schedule refactoring phases after GREEN phase completion
- Plan test infrastructure setup in early phases

### 5.4 TDD in Implementation Planning

Enforce TDD workflow:
- Each task includes test specification
- Task dependencies account for test-first approach
- Code review criteria include TDD compliance

See `implementation-planning.md` for detailed TDD task breakdown examples.
