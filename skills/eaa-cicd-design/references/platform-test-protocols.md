# Platform Test Protocols


## Contents

- [Table of Contents](#table-of-contents)
- [1. Language-Specific Test Commands](#1-language-specific-test-commands)
  - [1.1 Python Testing with pytest](#11-python-testing-with-pytest)
  - [1.2 TypeScript/JavaScript Testing with Vitest](#12-typescriptjavascript-testing-with-vitest)
  - [1.3 Rust Testing with cargo](#13-rust-testing-with-cargo)
  - [1.4 Swift Testing with XCTest](#14-swift-testing-with-xctest)
  - [1.5 C#/.NET Testing with xUnit](#15-cnet-testing-with-xunit)
  - [1.6 Kotlin/JVM Testing with JUnit](#16-kotlinjvm-testing-with-junit)
  - [1.7 Go Testing](#17-go-testing)
- [2. Cross-Platform Test Matrix](#2-cross-platform-test-matrix)
  - [2.1 Core Library Tests (All Platforms)](#21-core-library-tests-all-platforms)
  - [2.2 Platform-Specific UI Tests](#22-platform-specific-ui-tests)
- [3. Coverage Configuration](#3-coverage-configuration)
  - [3.1 Coverage Tools by Language](#31-coverage-tools-by-language)
  - [3.2 Codecov Integration](#32-codecov-integration)
- [4. Performance Testing](#4-performance-testing)
  - [4.1 Benchmark Configurations](#41-benchmark-configurations)
  - [4.2 Regression Detection](#42-regression-detection)
- [Test Protocol Checklist](#test-protocol-checklist)

---

Reference for language-specific and cross-platform testing configurations.

---

## Table of Contents

- 1. Language-Specific Test Commands
  - 1.1 Python testing with pytest
  - 1.2 TypeScript/JavaScript testing with Vitest
  - 1.3 Rust testing with cargo
  - 1.4 Swift testing with XCTest
  - 1.5 C#/.NET testing with xUnit
  - 1.6 Kotlin/JVM testing with JUnit
  - 1.7 Go testing
- 2. Cross-Platform Test Matrix
  - 2.1 Core library tests (all platforms)
  - 2.2 Platform-specific UI tests
- 3. Coverage Configuration
  - 3.1 Coverage tools by language
  - 3.2 Codecov integration
- 4. Performance Testing
  - 4.1 Benchmark configurations
  - 4.2 Regression detection

---

## 1. Language-Specific Test Commands

### 1.1 Python Testing with pytest

```bash
# Basic test run
pytest tests/

# With coverage
pytest --cov=src --cov-report=xml --cov-report=html tests/

# Verbose with long tracebacks
pytest -v --tb=long tests/

# Run specific markers
pytest -m "not slow" tests/

# Parallel execution
pytest -n auto tests/

# JUnit XML output for CI
pytest --junitxml=test-results.xml tests/
```

**Coverage Tool**: coverage.py / pytest-cov

### 1.2 TypeScript/JavaScript Testing with Vitest

```bash
# Basic test run
vitest run

# With coverage
vitest run --coverage

# Watch mode
vitest

# UI mode
vitest --ui

# Specific files
vitest run src/utils
```

**Coverage Tool**: c8 / istanbul

### 1.3 Rust Testing with cargo

```bash
# Basic test run
cargo test

# With output
cargo test -- --nocapture

# Release mode tests
cargo test --release

# Specific test
cargo test test_name

# Documentation tests
cargo test --doc

# All features
cargo test --all-features
```

**Coverage Tool**: cargo-tarpaulin, cargo-llvm-cov

```bash
# Install tarpaulin
cargo install cargo-tarpaulin

# Run with coverage
cargo tarpaulin --out Xml --out Html
```

### 1.4 Swift Testing with XCTest

```bash
# macOS tests
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=macOS'

# iOS Simulator tests
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 15'

# With result bundle
xcodebuild test \
  -scheme MyApp \
  -resultBundlePath TestResults.xcresult
```

**Coverage Tool**: xcov, xccov

```bash
# Extract coverage from xcresult
xcrun xccov view --report TestResults.xcresult
```

### 1.5 C#/.NET Testing with xUnit

```bash
# Basic test run
dotnet test

# With coverage
dotnet test --collect:"XPlat Code Coverage"

# Specific project
dotnet test MyApp.Tests/MyApp.Tests.csproj

# Verbosity
dotnet test --verbosity detailed

# Filter tests
dotnet test --filter "FullyQualifiedName~UnitTests"
```

**Coverage Tool**: coverlet

### 1.6 Kotlin/JVM Testing with JUnit

```bash
# Gradle test
./gradlew test

# With coverage report
./gradlew test jacocoTestReport

# Specific tests
./gradlew test --tests "com.example.MyTest"

# Parallel execution
./gradlew test --parallel
```

**Coverage Tool**: JaCoCo

### 1.7 Go Testing

```bash
# Basic test run
go test ./...

# With coverage
go test -coverprofile=coverage.out ./...

# Coverage HTML report
go tool cover -html=coverage.out -o coverage.html

# Race detection
go test -race ./...

# Verbose
go test -v ./...

# Benchmarks
go test -bench=. ./...
```

**Coverage Tool**: built-in

---

## 2. Cross-Platform Test Matrix

### 2.1 Core Library Tests (All Platforms)

```yaml
test-matrix:
  strategy:
    fail-fast: false
    matrix:
      include:
        # Core library tests - run on all platforms
        - name: core-linux
          runner: ubuntu-latest
          test-command: cargo test --package core

        - name: core-macos
          runner: macos-14
          test-command: cargo test --package core

        - name: core-windows
          runner: windows-latest
          test-command: cargo test --package core
```

### 2.2 Platform-Specific UI Tests

```yaml
test-matrix:
  strategy:
    matrix:
      include:
        # macOS UI tests
        - name: macos-ui
          runner: macos-14
          test-command: xcodebuild test -scheme MacApp -destination 'platform=macOS'

        # iOS Simulator tests
        - name: ios-ui
          runner: macos-14
          test-command: xcodebuild test -scheme iOSApp -destination 'platform=iOS Simulator,name=iPhone 15'

        # Windows UI tests
        - name: windows-ui
          runner: windows-latest
          test-command: dotnet test WindowsApp.Tests

        # Android Instrumented tests
        - name: android-ui
          runner: ubuntu-latest
          test-command: ./gradlew connectedAndroidTest

        # Web E2E tests
        - name: web-e2e
          runner: ubuntu-latest
          test-command: pnpm test:e2e
```

---

## 3. Coverage Configuration

### 3.1 Coverage Tools by Language

| Language | Test Framework | Command | Coverage Tool |
|----------|---------------|---------|---------------|
| Python | pytest | `pytest --cov=src --cov-report=xml` | coverage.py |
| TypeScript | Vitest | `vitest run --coverage` | c8/istanbul |
| Rust | cargo | `cargo tarpaulin --out Xml` | cargo-tarpaulin |
| Swift | XCTest | `xcodebuild test` + xcov | xcov/xccov |
| C# | xUnit | `dotnet test --collect:"XPlat Code Coverage"` | coverlet |
| Kotlin | JUnit | `./gradlew test jacocoTestReport` | JaCoCo |
| Go | go test | `go test -coverprofile=coverage.out ./...` | built-in |

### 3.2 Codecov Integration

```yaml
# codecov.yml - Coverage requirements
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%
        informational: false
    patch:
      default:
        target: 90%
        informational: false

parsers:
  gcov:
    branch_detection:
      conditional: yes
      loop: yes
      method: no
      macro: no

comment:
  layout: "reach,diff,flags,files"
  behavior: default
  require_changes: true
  require_base: false
  require_head: true

flags:
  python:
    paths:
      - src/
    carryforward: true

  typescript:
    paths:
      - packages/
    carryforward: true
```

**GitHub Actions Integration**:

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    files: ./coverage.xml
    flags: ${{ matrix.platform }}
    fail_ci_if_error: true
```

---

## 4. Performance Testing

### 4.1 Benchmark Configurations

**Python (pytest-benchmark)**:
```python
def test_performance(benchmark):
    result = benchmark(my_function, arg1, arg2)
    assert result is not None
```

```bash
pytest tests/benchmarks/ --benchmark-json=benchmark.json
```

**Rust (criterion)**:
```rust
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_function(c: &mut Criterion) {
    c.bench_function("my_function", |b| b.iter(|| my_function()));
}

criterion_group!(benches, bench_function);
criterion_main!(benches);
```

**Go**:
```go
func BenchmarkMyFunction(b *testing.B) {
    for i := 0; i < b.N; i++ {
        myFunction()
    }
}
```

### 4.2 Regression Detection

```yaml
# In CI workflow
- name: Run benchmarks
  run: |
    pytest tests/benchmarks/ --benchmark-json=current.json

- name: Compare with baseline
  run: |
    if [ -f baseline.json ]; then
      pytest-benchmark compare baseline.json current.json --csv=comparison.csv
      # Fail if >10% regression
      python scripts/check_regression.py comparison.csv --threshold 10
    fi

- name: Update baseline (on main only)
  if: github.ref == 'refs/heads/main'
  run: |
    cp current.json baseline.json
    git add baseline.json
    git commit -m "Update benchmark baseline" || true
```

---

## Test Protocol Checklist

- [ ] All languages have test commands documented
- [ ] Coverage tools configured for each language
- [ ] Cross-platform matrix covers all targets
- [ ] UI tests run on appropriate runners
- [ ] Codecov thresholds configured
- [ ] Performance benchmarks established
- [ ] Regression detection in place
