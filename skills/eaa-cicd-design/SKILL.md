---
name: eaa-cicd-design
description: "Use when designing CI/CD workflows and DevOps architecture. Trigger with CI/CD pipeline or GitHub Actions design requests."
version: 1.0.0
license: Apache-2.0
compatibility: Requires GitHub Actions, GitHub CLI (gh), and understanding of CI/CD concepts. Supports macOS, Windows, Linux, iOS, Android build automation. Requires AI Maestro installed.
metadata:
  author: Anthropic
context: fork
agent: eaa-main
---

# DevOps Expert Skill

## Overview

Design and configure CI/CD pipelines, GitHub Actions workflows, cross-platform build automation, secret management, and release processes.

## Prerequisites

- GitHub Actions access on target repository
- GitHub CLI (gh) installed and authenticated
- Understanding of CI/CD concepts
- Access to required secrets (API keys, certificates)

## Output

| Output Type | Description |
|-------------|-------------|
| GitHub Actions Workflows | Complete `.github/workflows/` directory with YAML files |
| Secret Management Documentation | Instructions for configuring secrets via gh CLI |
| Debug Scripts | Python scripts for workflow validation and local debugging |
| Release Checklist | Step-by-step guide for release process |
| Pipeline Configurations | CI/CD configurations for multi-platform builds |

## Instructions

1. Setting up CI/CD pipelines for new projects
2. Configuring GitHub Actions workflows
3. Managing secrets across environments
4. Automating multi-platform releases
5. Debugging failing workflows
6. Enforcing TDD in pipelines

## Checklist

Copy this checklist and track your progress:

- [ ] Review project requirements and target platforms
- [ ] Define workflow triggers (push, PR, tags)
- [ ] Select appropriate GitHub runners for each platform
- [ ] Configure secret management (API keys, certificates)
- [ ] Set up TDD enforcement with coverage thresholds
- [ ] Create multi-platform CI workflow YAML
- [ ] Configure matrix builds for cross-platform testing
- [ ] Set up release automation workflow
- [ ] Add debug scripts for local workflow simulation
- [ ] Validate YAML syntax and workflow structure
- [ ] Document secret setup instructions
- [ ] Create release checklist
- [ ] Test workflows on all target platforms
- [ ] Configure branch protection rules

## Core Competencies

### 1. GitHub Actions Workflows ([references/github-actions.md](references/github-actions.md))

- When you need to define workflow triggers → [Workflow Structure](references/github-actions.md#workflow-structure)
- When you need to choose the right runner → [Runners](references/github-actions.md#runners)
- When you need to build on multiple platforms → [Matrix Builds](references/github-actions.md#matrix-builds)
- When you need to use secrets securely → [Secrets](references/github-actions.md#secrets)
- When you need conditional execution logic → [Conditional Execution](references/github-actions.md#conditional-execution)
- When you need to pass data between jobs → [Outputs and Dependencies](references/github-actions.md#outputs-and-dependencies)
- When you need to reuse workflow code → [Reusable Workflows](references/github-actions.md#reusable-workflows)
- When you need to create releases → [Release Workflow](references/github-actions.md#release-workflow)
- When you need to debug failing workflows → [Debugging](references/github-actions.md#debugging)

### 2. Cross-Platform Build Automation ([references/cross-platform-builds.md](references/cross-platform-builds.md))

- When you need to choose runners for your target platforms → [Runner Matrix](references/cross-platform-builds.md#runner-matrix)
- When you need to check free tier minute limits → [Free Tier Minutes](references/cross-platform-builds.md#free-tier-minutes)
- When you need to configure a multi-platform CI workflow → [Multi-Platform CI Workflow](references/cross-platform-builds.md#multi-platform-ci-workflow)
- When you need to set up matrix builds with platform-specific configuration → [Complete Matrix Build](references/cross-platform-builds.md#complete-matrix-build)
- When you need to handle platform-specific build steps → [Platform-Specific Jobs](references/cross-platform-builds.md#platform-specific-jobs)

### 3. Secret Management ([references/secret-management.md](references/secret-management.md))

- When you need to decide which secret level to use → [Secret Hierarchy](references/secret-management.md#secret-hierarchy)
- When you need to create secrets via GitHub CLI → [Creating Secrets](references/secret-management.md#creating-secrets)
- When you need to use secrets in workflows → [Using Secrets in Workflows](references/secret-management.md#using-secrets-in-workflows)
- When you need to handle environment-specific secrets → [Environment Secrets](references/secret-management.md#environment-secrets)
- When you need to manage organization-wide secrets → [Organization Secrets](references/secret-management.md#secret-hierarchy)
- When you need to secure sensitive files (certificates, keys) → [Creating Secrets](references/secret-management.md#creating-secrets)

### 4. TDD Enforcement ([references/tdd-enforcement.md](references/tdd-enforcement.md))

- When you need to understand TDD principles → [Core Principles](references/tdd-enforcement.md#core-principles)
- When you need to set coverage thresholds for your project → [Coverage Requirements](references/tdd-enforcement.md#coverage-requirements)
- When you need to configure coverage for Python → [Python (pytest-cov)](references/tdd-enforcement.md#python-pytest-cov)
- When you need to configure coverage for Rust → [Rust (cargo-tarpaulin)](references/tdd-enforcement.md#rust-cargo-tarpaulin)
- When you need to configure coverage for TypeScript/JavaScript → [TypeScript/JavaScript (vitest)](references/tdd-enforcement.md#typescriptjavascript-vitest)
- When you need to configure coverage for Go → [Go (go test)](references/tdd-enforcement.md#go-go-test)
- When you need to implement branch protection rules → [Branch Protection Rules](references/tdd-enforcement.md#branch-protection-rules)

### 5. Release Automation ([references/release-automation.md](references/release-automation.md))

- When you need to understand the release workflow stages → [Release Pipeline Stages](references/release-automation.md#release-pipeline-stages)
- When you need to implement semantic versioning → [Semantic Versioning](references/release-automation.md#semantic-versioning)
- When you need to automatically bump versions → [Version Bumping Automation](references/release-automation.md#version-bumping-automation)
- When you need to generate changelogs → [Changelog Generation](references/release-automation.md#changelog-generation)
- When you need to create a complete release workflow → [Complete Release Workflow](references/release-automation.md#complete-release-workflow)
- When you need to publish to package registries → [Platform-Specific Publishing](references/release-automation.md#platform-specific-publishing)

## Quick Reference

### GitHub Runners Matrix

| Platform | Runner | Architecture | Free Tier |
|----------|--------|--------------|-----------|
| macOS | `macos-14` | ARM64 (M1) | 2000 min/month |
| macOS | `macos-13` | x86_64 | 2000 min/month |
| Windows | `windows-latest` | x86_64 | 2000 min/month |
| Linux | `ubuntu-latest` | x86_64 | 2000 min/month |

### Workflow Templates

| Template | Purpose |
|----------|---------|
| `templates/ci-multi-platform.yml` | Multi-platform CI |
| `templates/release-github.yml` | GitHub Release |
| `templates/security-scan.yml` | Security scanning |
| `templates/docs-generate.yml` | Documentation |

### Required Secrets per Platform

| Platform | Secrets |
|----------|---------|
| Apple | `APPLE_CERTIFICATE`, `APPLE_ID`, `NOTARIZATION_PASSWORD` |
| Windows | `WINDOWS_CERTIFICATE`, `WINDOWS_CERTIFICATE_PASSWORD` |
| Android | `ANDROID_KEYSTORE`, `KEYSTORE_PASSWORD` |
| npm | `NPM_TOKEN` |
| PyPI | `PYPI_API_TOKEN` |

## TDD Enforcement Rules

```yaml
# Every pipeline MUST:
1. Run tests before build
2. Fail if coverage < 80%
3. Block PR merge if tests fail
4. Run tests on all target platforms
5. No test skipping without documented reason
```

## Workflow Structure

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

Every workflow should have a debug script:

| Script | Purpose |
|--------|---------|
| `scripts/debug_workflow.py` | Simulate workflow locally |
| `scripts/validate_yaml.py` | Validate workflow syntax |
| `scripts/setup_secrets.py` | Configure GitHub secrets |

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

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/debug_workflow.py` | Debug workflow locally |
| `scripts/validate_yaml.py` | Validate YAML syntax |
| `scripts/setup_secrets.py` | Configure secrets via gh CLI |
| `scripts/list_runners.py` | List available runners |

## IRON RULE

This skill NEVER executes code. All outputs are:
- GitHub Actions workflow files (YAML)
- Configuration files
- Documentation (Markdown)
- Script templates (for manual execution)

Actual pipeline execution happens on GitHub Actions runners.

## Examples

### Example 1: Multi-Platform CI Workflow

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest --cov=src tests/
```

### Example 2: Release Workflow

```yaml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and publish
        run: |
          python -m build
          twine upload dist/*
        env:
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

---

## Error Handling

### Issue: CI pipeline fails but tests pass locally

**Cause**: Environment differences between local and CI.

**Solution**:
1. Check CI environment variables vs local
2. Verify dependency versions match (package-lock.json, pyproject.toml)
3. Check for filesystem path differences (case sensitivity)
4. Review CI logs for environment-specific errors

### Issue: Docker build fails in CI but works locally

**Cause**: Docker cache differences or missing dependencies.

**Solution**:
1. Add `--no-cache` to CI docker build to eliminate cache issues
2. Check base image availability in CI environment
3. Verify all required files are in Docker context (not gitignored)
4. Check CI runner has sufficient disk space

### Issue: Deployment script times out

**Cause**: Network issues or slow operations not properly configured.

**Solution**:
1. Increase timeout values in deployment configuration
2. Check network connectivity between CI and deployment target
3. Verify credentials/tokens haven't expired
4. Split large deployments into smaller steps

### Issue: GitHub Actions workflow not triggering

**Cause**: YAML syntax error or trigger condition not met.

**Solution**:
1. Validate YAML syntax with online validator
2. Check branch/path filters match actual changes
3. Verify workflow file is in `.github/workflows/`
4. Check repository Actions settings are enabled

### Issue: Secrets not available in workflow

**Cause**: Secret scope incorrect or name mismatch.

**Solution**:
1. Verify secret name matches exactly (case-sensitive)
2. Check secret is set at correct scope (repo/org/environment)
3. For forks, secrets are not available by default
4. Use `${{ secrets.SECRET_NAME }}` syntax

---

## Resources

- [github-actions.md](references/github-actions.md) - Workflow structure and features
- [cross-platform-builds.md](references/cross-platform-builds.md) - Multi-platform CI setup
- [secret-management.md](references/secret-management.md) - Secret hierarchy and usage
- [tdd-enforcement.md](references/tdd-enforcement.md) - Test coverage requirements
- [release-automation.md](references/release-automation.md) - Release pipeline stages
- `templates/ci-multi-platform.yml` - Multi-platform CI template
- `templates/release-github.yml` - GitHub release template
- `templates/security-scan.yml` - Security scanning template
