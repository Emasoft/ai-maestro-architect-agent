---
procedure: support-skill
workflow-instruction: support
---

# Operation: Set Up CI/CD Pipeline


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Analyze Project Requirements](#step-1-analyze-project-requirements)
  - [Step 2: Create Workflow Directory](#step-2-create-workflow-directory)
  - [Step 3: Design Pipeline Stages](#step-3-design-pipeline-stages)
  - [Step 4: Create Main CI Workflow](#step-4-create-main-ci-workflow)
  - [Step 5: Configure Branch Protection](#step-5-configure-branch-protection)
  - [Step 6: Document the Pipeline](#step-6-document-the-pipeline)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example](#example)
- [Error Handling](#error-handling)

## Purpose

Set up a complete CI/CD pipeline from scratch for a new project, including workflow triggers, test stages, build stages, and deployment configuration.

## When to Use

- Starting CI/CD for a new project
- Migrating from another CI system to GitHub Actions
- Rebuilding pipeline from scratch

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Project type | Project analysis | Yes |
| Target platforms | Requirements | Yes |
| Test framework | Project config | Yes |
| Deployment targets | Requirements | Yes |

## Procedure

### Step 1: Analyze Project Requirements

Determine:
- Programming language(s)
- Build tools (npm, pip, cargo, etc.)
- Test framework (pytest, jest, etc.)
- Target platforms (Linux, macOS, Windows)
- Deployment targets (PyPI, npm, GitHub Releases)

### Step 2: Create Workflow Directory

```bash
mkdir -p .github/workflows
```

### Step 3: Design Pipeline Stages

Standard pipeline structure:

```
Stage 1: lint-format      # Code quality checks
Stage 2: type-check       # Type safety (if applicable)
Stage 3: test-matrix      # Tests on all platforms
Stage 4: build-matrix     # Build artifacts
Stage 5: release          # Release (tags only)
```

### Step 4: Create Main CI Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint-format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up environment
        # Language-specific setup
      - name: Lint and format check
        run: |
          # Linting commands

  test:
    needs: lint-format
    strategy:
      matrix:
        os: [ubuntu-latest]
        # Add other platforms as needed
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          # Test commands

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: |
          # Build commands
```

### Step 5: Configure Branch Protection

Require status checks:
- lint-format
- test
- build (for main branch)

### Step 6: Document the Pipeline

Create `.github/PIPELINE.md` documenting:
- Pipeline stages
- Triggers
- Required secrets
- How to extend

## Output

| File | Content |
|------|---------|
| `.github/workflows/ci.yml` | Main CI workflow |
| `.github/PIPELINE.md` | Pipeline documentation |

## Verification Checklist

- [ ] Project requirements analyzed
- [ ] Workflow directory created
- [ ] CI workflow file created
- [ ] All stages defined (lint, test, build)
- [ ] Branch protection configured
- [ ] Pipeline documented

## Example

```yaml
# Python project CI pipeline
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check src/

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e ".[test]"
      - run: pytest --cov=src tests/
```

## Error Handling

| Error | Solution |
|-------|----------|
| Workflow syntax error | Validate YAML with `actionlint` |
| Jobs not running | Check trigger conditions |
| Permission denied | Verify repository settings |
