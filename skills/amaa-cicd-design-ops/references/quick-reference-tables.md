# CI/CD Design - Quick Reference Tables

## Table of Contents

- GitHub Runners Matrix
- Workflow Templates
- Required Secrets per Platform
- TDD Enforcement Rules
- Recommended Pipeline Stages
- Debug Scripts
- Handoff Protocol

## GitHub Runners Matrix

| Platform | Runner | Architecture | Free Tier |
|----------|--------|--------------|-----------|
| macOS | `macos-14` | ARM64 (M1) | 2000 min/month |
| macOS | `macos-13` | x86_64 | 2000 min/month |
| Windows | `windows-latest` | x86_64 | 2000 min/month |
| Linux | `ubuntu-latest` | x86_64 | 2000 min/month |

## Workflow Templates

| Template | Purpose |
|----------|---------|
| `templates/ci-multi-platform.yml` | Multi-platform CI |
| `templates/release-github.yml` | GitHub Release |
| `templates/security-scan.yml` | Security scanning |
| `templates/docs-generate.yml` | Documentation |

## Required Secrets per Platform

| Platform | Secrets |
|----------|---------|
| Apple | `APPLE_CERTIFICATE`, `APPLE_ID`, `NOTARIZATION_PASSWORD` |
| Windows | `WINDOWS_CERTIFICATE`, `WINDOWS_CERTIFICATE_PASSWORD` |
| Android | `ANDROID_KEYSTORE`, `KEYSTORE_PASSWORD` |
| npm | `NPM_TOKEN` |
| PyPI | `PYPI_API_TOKEN` |

## TDD Enforcement Rules

Every pipeline MUST:
1. Run tests before build
2. Fail if coverage < 80%
3. Block PR merge if tests fail
4. Run tests on all target platforms
5. No test skipping without documented reason

## Recommended Pipeline Stages

```yaml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
jobs:
  lint-format:        # Stage 1: Quality checks
  type-check:         # Stage 2: Type safety
  test-matrix:        # Stage 3: Tests on all platforms
  build-matrix:       # Stage 4: Build artifacts
  release:            # Stage 5: Release (tags only)
```

## Debug Scripts

| Script | Purpose |
|--------|---------|
| `scripts/debug_workflow.py` | Simulate workflow locally |
| `scripts/validate_yaml.py` | Validate workflow syntax |
| `scripts/setup_secrets.py` | Configure GitHub secrets |
| `scripts/list_runners.py` | List available runners |

## Handoff Protocol

### From Modularizer Expert
Receive:
- Module list with platform targets
- Build system requirements
- Test matrix requirements

### Output
Provide:
- Complete `.github/workflows/` directory
- Secret management documentation
- Debug scripts for each workflow
- Release checklist

## Competency Index

### GitHub Actions Workflows
- Workflow triggers -> [github-actions.md](github-actions.md) (section: Workflow Structure)
- Runner selection -> [github-actions.md](github-actions.md) (section: Runners)
- Matrix builds -> [github-actions.md](github-actions.md) (section: Matrix Builds)
- Secrets usage -> [github-actions.md](github-actions.md) (section: Secrets)
- Conditional execution -> [github-actions.md](github-actions.md) (section: Conditional Execution)
- Data passing between jobs -> [github-actions.md](github-actions.md) (section: Outputs and Dependencies)
- Reusable workflows -> [github-actions.md](github-actions.md) (section: Reusable Workflows)
- Release workflows -> [github-actions.md](github-actions.md) (section: Release Workflow)
- Debugging -> [github-actions.md](github-actions.md) (section: Debugging)

### Cross-Platform Build Automation
- Runner selection -> [cross-platform-builds.md](cross-platform-builds.md) (section: Runner Matrix)
- Free tier limits -> [cross-platform-builds.md](cross-platform-builds.md) (section: Free Tier Minutes)
- Multi-platform CI -> [cross-platform-builds.md](cross-platform-builds.md) (section: Multi-Platform CI Workflow)
- Matrix configuration -> [cross-platform-builds.md](cross-platform-builds.md) (section: Complete Matrix Build)
- Platform-specific steps -> [cross-platform-builds.md](cross-platform-builds.md) (section: Platform-Specific Jobs)

### Secret Management
- Secret hierarchy -> [secret-management.md](secret-management.md) (section: Secret Hierarchy)
- Creating secrets via CLI -> [secret-management.md](secret-management.md) (section: Creating Secrets)
- Secrets in workflows -> [secret-management.md](secret-management.md) (section: Using Secrets in Workflows)
- Environment secrets -> [secret-management.md](secret-management.md) (section: Environment Secrets)

### TDD Enforcement
- Core principles -> [tdd-enforcement.md](tdd-enforcement.md) (section: Core Principles)
- Coverage thresholds -> [tdd-enforcement.md](tdd-enforcement.md) (section: Coverage Requirements)
- Python coverage -> [tdd-enforcement.md](tdd-enforcement.md) (section: Python pytest-cov)
- Rust coverage -> [tdd-enforcement.md](tdd-enforcement.md) (section: Rust cargo-tarpaulin)
- TypeScript/JS coverage -> [tdd-enforcement.md](tdd-enforcement.md) (section: TypeScript/JavaScript vitest)
- Go coverage -> [tdd-enforcement.md](tdd-enforcement.md) (section: Go go test)
- Branch protection -> [tdd-enforcement.md](tdd-enforcement.md) (section: Branch Protection Rules)

### Release Automation
- Pipeline stages -> [release-automation.md](release-automation.md) (section: Release Pipeline Stages)
- Semantic versioning -> [release-automation.md](release-automation.md) (section: Semantic Versioning)
- Version bumping -> [release-automation.md](release-automation.md) (section: Version Bumping Automation)
- Changelog generation -> [release-automation.md](release-automation.md) (section: Changelog Generation)
- Complete workflow -> [release-automation-part1-complete-workflow.md](release-automation-part1-complete-workflow.md)
- Platform publishing -> [release-automation-part2-platform-publishing.md](release-automation-part2-platform-publishing.md)
