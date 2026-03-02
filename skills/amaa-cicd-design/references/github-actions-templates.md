# GitHub Actions Workflow Templates


## Contents

- [Table of Contents](#table-of-contents)
- [1. Multi-Platform CI Workflow Template](#1-multi-platform-ci-workflow-template)
- [2. Release Workflow Template](#2-release-workflow-template)
- [3. Security Scanning Workflow](#3-security-scanning-workflow)
- [GitHub Runners Matrix](#github-runners-matrix)
- [Workflow Types Reference](#workflow-types-reference)

---

Reference templates for CI/CD pipelines used by the DevOps Expert Agent.

---

## Table of Contents

- 1. Multi-Platform CI Workflow Template
  - 1.1 Lint & Format Job
  - 1.2 Type Checking Job
  - 1.3 Test Matrix Job
  - 1.4 Build Matrix Job
- 2. Release Workflow Template
  - 2.1 Tag Validation
  - 2.2 Multi-Platform Build
  - 2.3 Create GitHub Release
  - 2.4 Publish to Platforms (npm, PyPI)
- 3. Security Scanning Workflow
  - 3.1 Dependency Vulnerabilities (npm, pip, cargo audit)
  - 3.2 Code Analysis (CodeQL, Semgrep)
  - 3.3 Secret Detection (TruffleHog)

---

## 1. Multi-Platform CI Workflow Template

```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint-format:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup toolchain
        # Platform-specific setup
      - name: Run linters
        # Linting commands
      - name: Check formatting
        # Format check commands

  type-check:
    name: Type Checking
    runs-on: ubuntu-latest
    needs: lint-format
    steps:
      - uses: actions/checkout@v4
      - name: Type check
        # Type checking commands

  test-matrix:
    name: Test (${{ matrix.platform }})
    needs: type-check
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: macos
            runner: macos-14
          - platform: windows
            runner: windows-latest
          - platform: linux
            runner: ubuntu-latest
          - platform: web
            runner: ubuntu-latest
    runs-on: ${{ matrix.runner }}
    steps:
      - uses: actions/checkout@v4
      - name: Setup platform
        # Platform-specific setup
      - name: Run tests
        # Platform-specific test commands
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          flags: ${{ matrix.platform }}

  build-matrix:
    name: Build (${{ matrix.platform }})
    needs: test-matrix
    strategy:
      matrix:
        include:
          - platform: macos
            runner: macos-14
          - platform: windows
            runner: windows-latest
          - platform: linux
            runner: ubuntu-latest
    runs-on: ${{ matrix.runner }}
    steps:
      - uses: actions/checkout@v4
      - name: Build
        # Platform-specific build commands
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.platform }}
          path: dist/
```

---

## 2. Release Workflow Template

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write
  packages: write

jobs:
  validate-tag:
    name: Validate Tag
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - name: Extract version
        id: version
        run: echo "version=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

  build-all-platforms:
    name: Build (${{ matrix.platform }})
    needs: validate-tag
    strategy:
      matrix:
        include:
          - platform: macos-arm64
            runner: macos-14
          - platform: macos-x64
            runner: macos-13
          - platform: windows-x64
            runner: windows-latest
          - platform: linux-x64
            runner: ubuntu-latest
          - platform: linux-arm64
            runner: ubuntu-24.04-arm
    runs-on: ${{ matrix.runner }}
    steps:
      - uses: actions/checkout@v4
      - name: Build release
        # Build commands
      - name: Sign artifacts
        # Signing commands (platform-specific)
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: release-${{ matrix.platform }}
          path: dist/

  create-release:
    name: Create GitHub Release
    needs: build-all-platforms
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/
      - name: Create release
        uses: softprops/action-gh-release@v1
        with:
          files: artifacts/**/*
          generate_release_notes: true

  publish-platforms:
    name: Publish to Platforms
    needs: create-release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish to npm
        if: hashFiles('package.json') != ''
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
      - name: Publish to PyPI
        if: hashFiles('pyproject.toml') != '' || hashFiles('setup.py') != ''
        run: |
          pip install build twine
          python -m build
          python -m twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

---

## 3. Security Scanning Workflow

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6am

jobs:
  dependency-scan:
    name: Dependency Vulnerabilities
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run npm audit
        if: hashFiles('package.json') != ''
        run: npm audit --audit-level=moderate
      - name: Run pip audit
        if: hashFiles('requirements.txt') != '' || hashFiles('pyproject.toml') != ''
        run: |
          pip install pip-audit
          pip-audit
      - name: Run cargo audit
        if: hashFiles('Cargo.toml') != ''
        run: |
          cargo install cargo-audit
          cargo audit

  code-scan:
    name: Code Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run CodeQL
        uses: github/codeql-action/analyze@v3
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1

  secret-scan:
    name: Secret Detection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified
```

---

## GitHub Runners Matrix

| Platform | Runner | Architecture | Notes |
|----------|--------|--------------|-------|
| macOS | `macos-14` | ARM64 (M1) | Free tier: 2000 min/month |
| macOS | `macos-13` | x86_64 | Legacy Intel support |
| Windows | `windows-latest` | x86_64 | Free tier: 2000 min/month |
| Linux | `ubuntu-latest` | x86_64 | Free tier: 2000 min/month |
| Linux ARM | `ubuntu-24.04-arm` | ARM64 | Limited availability |

---

## Workflow Types Reference

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | push, pull_request | Continuous Integration |
| `release.yml` | tag push | Release automation |
| `nightly.yml` | schedule | Nightly builds and tests |
| `platform-*.yml` | workflow_call | Platform-specific builds |
| `security.yml` | push, schedule | Security scanning |
| `docs.yml` | push to main | Documentation generation |
