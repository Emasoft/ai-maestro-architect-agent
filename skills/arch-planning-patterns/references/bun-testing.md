# Bun Testing Reference Index

This reference is split into three parts for easier navigation and progressive discovery.

## Parts Overview

### Part 1: [Basics](bun-testing-basics.md)
**When to read:** When you need to understand Bun test fundamentals or write your first tests.

| Section | Use Case |
|---------|----------|
| What is Bun Test Runner | Understanding when and why to use Bun's test runner |
| Test Syntax and Structure | Writing test files, using describe/test/expect |
| Common Matchers | Choosing the right assertion for your test |
| CLI Options Reference | Running tests with different configurations |

### Part 2: [Lifecycle, Coverage, and CI](bun-testing-lifecycle-coverage.md)
**When to read:** When setting up test infrastructure, CI pipelines, or managing test state.

| Section | Use Case |
|---------|----------|
| Lifecycle Hooks | Setting up/tearing down resources before/after tests |
| Coverage Configuration | Generating and viewing code coverage reports |
| CI Integration | Setting up GitHub Actions, GitLab CI, or Jenkins |
| Package.json Scripts | Creating convenient npm/bun scripts for testing |

### Part 3: [Advanced Features and Troubleshooting](bun-testing-advanced-troubleshooting.md)
**When to read:** When you encounter issues or need advanced testing features.

| Section | Use Case |
|---------|----------|
| Per-Test Timeout | Handling slow tests individually |
| test.only / test.skip / test.todo | Focusing, skipping, or planning tests |
| Testing External Services | Best practices for real API/service tests |
| Troubleshooting | Fixing common test problems and CI failures |

---

## Quick Reference

| Task | File | Section |
|------|------|---------|
| Write first test | [basics](bun-testing-basics.md) | Test Syntax and Structure |
| Run tests with coverage | [basics](bun-testing-basics.md) | Coverage Mode |
| Set up database for tests | [lifecycle](bun-testing-lifecycle-coverage.md) | beforeAll Hook |
| Configure GitHub Actions | [lifecycle](bun-testing-lifecycle-coverage.md) | GitHub Actions Example |
| Debug test timeout | [troubleshooting](bun-testing-advanced-troubleshooting.md) | Test Timeout |
| Skip flaky test temporarily | [troubleshooting](bun-testing-advanced-troubleshooting.md) | Test.skip |
| Fix "tests not found" | [troubleshooting](bun-testing-advanced-troubleshooting.md) | Tests Not Found |
