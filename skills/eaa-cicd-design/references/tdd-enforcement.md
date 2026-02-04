# TDD Enforcement in CI/CD


## Contents

- [Use Cases (Quick Reference)](#use-cases-quick-reference)
- [Overview](#overview)
- [Core Principles](#core-principles)
  - [TDD Pipeline Rules](#tdd-pipeline-rules)
- [Coverage Requirements](#coverage-requirements)
  - [Minimum Thresholds](#minimum-thresholds)
  - [Coverage Configuration](#coverage-configuration)
    - [Rust (cargo-tarpaulin)](#rust-cargo-tarpaulin)
    - [Python (pytest-cov)](#python-pytest-cov)
    - [TypeScript/JavaScript (vitest)](#typescriptjavascript-vitest)
    - [Go (go test)](#go-go-test)
- [Complete TDD Workflow](#complete-tdd-workflow)
  - [Multi-Platform Test Matrix](#multi-platform-test-matrix)
  - [Branch Protection Rules](#branch-protection-rules)
- [Test Skipping Policy](#test-skipping-policy)
  - [When Skipping is Allowed](#when-skipping-is-allowed)
  - [CI Configuration for Ignored Tests](#ci-configuration-for-ignored-tests)
- [Mutation Testing](#mutation-testing)
  - [Why Mutation Testing?](#why-mutation-testing)
  - [Rust (cargo-mutants)](#rust-cargo-mutants)
- [Debug Script](#debug-script)
- [Checklist](#checklist)

---

## Use Cases (Quick Reference)

- When you need to understand TDD principles → [Core Principles](#core-principles)
- When you need to set coverage thresholds for your project → [Coverage Requirements](#coverage-requirements)
- When you need to configure coverage for Python → [Python (pytest-cov)](#python-pytest-cov)
- When you need to configure coverage for Rust → [Rust (cargo-tarpaulin)](#rust-cargo-tarpaulin)
- When you need to configure coverage for TypeScript/JavaScript → [TypeScript/JavaScript (vitest)](#typescriptjavascript-vitest)
- When you need to configure coverage for Go → [Go (go test)](#go-go-test)
- When you need to implement branch protection rules → [Branch Protection Rules](#branch-protection-rules)
- When you need to handle test skipping → [Test Skipping Policy](#test-skipping-policy)
- When you need mutation testing → [Mutation Testing](#mutation-testing)

## Overview

Test-Driven Development (TDD) enforcement ensures code quality through automated testing at every stage of the pipeline. No code reaches production without passing comprehensive tests.

## Core Principles

### TDD Pipeline Rules

```
1. Tests run BEFORE build
2. Build fails if tests fail
3. Build fails if coverage < threshold
4. No skipping tests without documented reason
5. All platforms must pass tests
6. PR cannot merge with failing tests
```

## Coverage Requirements

### Minimum Thresholds

| Project Type | Line Coverage | Branch Coverage |
|--------------|---------------|-----------------|
| Library | 80% | 70% |
| CLI Application | 75% | 65% |
| Web Application | 70% | 60% |
| Critical Infrastructure | 90% | 85% |

### Coverage Configuration

#### Rust (cargo-tarpaulin)

```yaml
- name: Run tests with coverage
  uses: actions-rs/tarpaulin@v0.1
  with:
    version: '0.27.0'
    args: '--all-features --workspace --out xml --fail-under 80'

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: cobertura.xml
    fail_ci_if_error: true
```

#### Python (pytest-cov)

```yaml
- name: Run tests with coverage
  run: |
    pytest tests/ \
      --cov=src \
      --cov-report=xml \
      --cov-report=term \
      --cov-fail-under=80

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: coverage.xml
```

#### TypeScript/JavaScript (vitest)

```yaml
- name: Run tests with coverage
  run: |
    pnpm test -- --coverage --coverage.thresholds.lines=80

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: coverage/lcov.info
```

#### Go (go test)

```yaml
- name: Run tests with coverage
  run: |
    go test -v -race -coverprofile=coverage.out -covermode=atomic ./...
    go tool cover -func=coverage.out | grep total | awk '{print $3}' | \
      sed 's/%//' | xargs -I {} test {} -ge 80 || exit 1

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: coverage.out
```

## Complete TDD Workflow

### Multi-Platform Test Matrix

```yaml
name: TDD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # Stage 1: Lint and format (fast feedback)
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt

      - name: Format check
        run: cargo fmt --all -- --check

      - name: Clippy
        run: cargo clippy --all-targets --all-features -- -D warnings

  # Stage 2: Type checking (if applicable)
  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: dtolnay/rust-toolchain@stable

      - name: Check
        run: cargo check --all-targets --all-features

  # Stage 3: Unit tests on all platforms
  test-unit:
    name: Unit Tests (${{ matrix.os }})
    needs: typecheck
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: dtolnay/rust-toolchain@stable

      - name: Cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry/
            ~/.cargo/git/
            target/
          key: ${{ runner.os }}-cargo-test-${{ hashFiles('**/Cargo.lock') }}

      - name: Run unit tests
        run: cargo test --lib --all-features
        env:
          RUST_BACKTRACE: 1

  # Stage 4: Integration tests
  test-integration:
    name: Integration Tests
    needs: test-unit
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: dtolnay/rust-toolchain@stable

      - name: Run integration tests
        run: cargo test --test '*' --all-features
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test

  # Stage 5: Coverage analysis
  coverage:
    name: Coverage Analysis
    needs: test-unit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: dtolnay/rust-toolchain@stable

      - name: Install tarpaulin
        run: cargo install cargo-tarpaulin

      - name: Generate coverage
        run: |
          cargo tarpaulin \
            --all-features \
            --workspace \
            --out xml \
            --out html \
            --fail-under 80

      - name: Upload to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: cobertura.xml
          fail_ci_if_error: true
          token: ${{ secrets.CODECOV_TOKEN }}

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: tarpaulin-report.html

  # Stage 6: Doc tests
  test-docs:
    name: Doc Tests
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: dtolnay/rust-toolchain@stable

      - name: Run doc tests
        run: cargo test --doc --all-features

  # Stage 7: Build only after ALL tests pass
  build:
    name: Build
    needs: [test-unit, test-integration, coverage, test-docs]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup
        uses: dtolnay/rust-toolchain@stable

      - name: Build release
        run: cargo build --release
```

### Branch Protection Rules

Configure in Repository → Settings → Branches → Add rule:

```yaml
Branch name pattern: main

Required status checks:
  - lint
  - typecheck
  - test-unit (ubuntu-latest)
  - test-unit (macos-14)
  - test-unit (windows-latest)
  - test-integration
  - coverage

Require branches to be up to date: true
Require conversation resolution: true
Require signed commits: false
Include administrators: true
```

## Test Skipping Policy

### When Skipping is Allowed

```rust
// ALLOWED: Platform-specific test
#[cfg(target_os = "macos")]
#[test]
fn test_macos_specific_feature() {
    // Only runs on macOS
}

// ALLOWED: Documented slow test
#[test]
#[ignore = "Requires external service - run with --ignored"]
fn test_with_external_api() {
    // Integration test requiring live API
}

// NOT ALLOWED: Skipping without reason
#[test]
#[ignore]  // BAD - no reason given
fn test_something() {
    // ???
}
```

### CI Configuration for Ignored Tests

```yaml
# Run fast tests in normal CI
- name: Run tests
  run: cargo test

# Run all tests including slow ones in nightly
- name: Run all tests (nightly)
  if: github.event_name == 'schedule'
  run: cargo test -- --include-ignored
```

## Mutation Testing

### Why Mutation Testing?

Coverage alone doesn't ensure test quality. Mutation testing verifies tests actually catch bugs.

### Rust (cargo-mutants)

```yaml
mutation-testing:
  name: Mutation Testing
  runs-on: ubuntu-latest
  if: github.event_name == 'schedule'  # Weekly
  steps:
    - uses: actions/checkout@v4

    - name: Setup
      uses: dtolnay/rust-toolchain@stable

    - name: Install cargo-mutants
      run: cargo install cargo-mutants

    - name: Run mutation tests
      run: |
        cargo mutants --timeout 300 -- --all-features

    - name: Upload results
      uses: actions/upload-artifact@v4
      with:
        name: mutation-report
        path: mutants.out/
```

## Debug Script

```python
#!/usr/bin/env python3
"""
Debug script for TDD pipeline failures.
Analyzes test results and coverage reports.
"""
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def analyze_coverage(coverage_file: Path) -> dict:
    """Parse coverage XML and return stats."""
    if not coverage_file.exists():
        return {"error": "Coverage file not found"}

    tree = ET.parse(coverage_file)
    root = tree.getroot()

    # Cobertura format
    if root.tag == "coverage":
        return {
            "line_rate": float(root.get("line-rate", 0)) * 100,
            "branch_rate": float(root.get("branch-rate", 0)) * 100,
            "lines_covered": int(root.get("lines-covered", 0)),
            "lines_valid": int(root.get("lines-valid", 0)),
        }

    return {"error": "Unknown coverage format"}


def analyze_test_results(test_output: str) -> dict:
    """Parse test output and return stats."""
    lines = test_output.split("\n")

    passed = 0
    failed = 0
    ignored = 0

    for line in lines:
        if "test result:" in line:
            # Example: test result: ok. 42 passed; 1 failed; 3 ignored
            parts = line.split()
            for i, part in enumerate(parts):
                if part == "passed;":
                    passed = int(parts[i - 1])
                elif part == "failed;":
                    failed = int(parts[i - 1])
                elif "ignored" in part:
                    ignored = int(parts[i - 1])

    return {
        "passed": passed,
        "failed": failed,
        "ignored": ignored,
        "total": passed + failed + ignored,
    }


def run_tests_verbose() -> tuple[int, str]:
    """Run tests with verbose output."""
    result = subprocess.run(
        ["cargo", "test", "--", "--nocapture"],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout + result.stderr


def main():
    print("TDD Pipeline Debug")
    print("=" * 50)

    # Run tests
    print("\nRunning tests...")
    code, output = run_tests_verbose()

    stats = analyze_test_results(output)
    print(f"\nTest Results:")
    print(f"  Passed:  {stats['passed']}")
    print(f"  Failed:  {stats['failed']}")
    print(f"  Ignored: {stats['ignored']}")

    if stats["failed"] > 0:
        print("\nFailed tests output:")
        print("-" * 40)
        # Extract failure details
        in_failure = False
        for line in output.split("\n"):
            if "FAILED" in line or "panicked" in line:
                in_failure = True
            if in_failure:
                print(line)
            if in_failure and line.strip() == "":
                in_failure = False

    # Check coverage
    coverage_file = Path("cobertura.xml")
    if coverage_file.exists():
        cov = analyze_coverage(coverage_file)
        print(f"\nCoverage:")
        print(f"  Line:   {cov.get('line_rate', 'N/A'):.1f}%")
        print(f"  Branch: {cov.get('branch_rate', 'N/A'):.1f}%")

        if cov.get("line_rate", 0) < 80:
            print("\n  WARNING: Coverage below 80% threshold!")

    return code


if __name__ == "__main__":
    sys.exit(main())
```

## Checklist

- [ ] Tests run before build in pipeline
- [ ] Coverage threshold configured (minimum 80%)
- [ ] All target platforms included in test matrix
- [ ] Branch protection requires passing tests
- [ ] Skipped tests have documented reasons
- [ ] Integration tests with real services
- [ ] Coverage reports uploaded to Codecov
- [ ] Mutation testing scheduled (weekly)
- [ ] Debug script available for failures
