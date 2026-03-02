# GitHub Actions Reference


## Contents

- [Use Cases (Quick Reference)](#use-cases-quick-reference)
- [Overview](#overview)
- [Part 1: Workflow Basics and Runners](#part-1-workflow-basics-and-runners)
  - [Workflow Structure](#workflow-structure)
  - [Runners](#runners)
  - [Common Actions](#common-actions)
- [Part 2: Matrix Builds, Secrets, and Conditionals](#part-2-matrix-builds-secrets-and-conditionals)
  - [Matrix Builds](#matrix-builds)
  - [Secrets](#secrets)
  - [Conditional Execution](#conditional-execution)
  - [Outputs and Dependencies](#outputs-and-dependencies)
- [Part 3: Reusable Workflows and Releases](#part-3-reusable-workflows-and-releases)
  - [Reusable Workflows](#reusable-workflows)
  - [Release Workflow](#release-workflow)
  - [Publish to Package Registries](#publish-to-package-registries)
  - [Security Best Practices](#security-best-practices)
- [Part 4: Debugging and Common Patterns](#part-4-debugging-and-common-patterns)
  - [Debugging](#debugging)
  - [Common Patterns](#common-patterns)
  - [Checklist](#checklist)
- [Quick Command Reference](#quick-command-reference)

---

## Use Cases (Quick Reference)

- When you need to define workflow triggers → [Part 1: Workflow Basics](github-actions-part1-workflow-basics.md)
- When you need to choose the right runner → [Part 1: Workflow Basics](github-actions-part1-workflow-basics.md)
- When you need to build on multiple platforms → [Part 2: Matrix Builds](github-actions-part2-matrix-secrets.md)
- When you need to use secrets securely → [Part 2: Secrets](github-actions-part2-matrix-secrets.md)
- When you need conditional execution logic → [Part 2: Conditional Execution](github-actions-part2-matrix-secrets.md)
- When you need to pass data between jobs → [Part 2: Outputs and Dependencies](github-actions-part2-matrix-secrets.md)
- When you need to reuse workflow code → [Part 3: Reusable Workflows](github-actions-part3-reusable-release.md)
- When you need to create releases → [Part 3: Release Workflow](github-actions-part3-reusable-release.md)
- When you need to debug failing workflows → [Part 4: Debugging](github-actions-part4-debugging-patterns.md)
- When you need to test workflows locally → [Part 4: Debugging](github-actions-part4-debugging-patterns.md) (act section)
- When you need to cache dependencies → [Part 1: Common Actions](github-actions-part1-workflow-basics.md) (cache section)
- When you need to publish packages → [Part 3: Release Workflow](github-actions-part3-reusable-release.md) (publish section)

## Overview

GitHub Actions is the CI/CD platform integrated with GitHub. Workflows are defined in YAML files in `.github/workflows/`.

---

## Part 1: Workflow Basics and Runners

**File**: [github-actions-part1-workflow-basics.md](github-actions-part1-workflow-basics.md)

### Workflow Structure

Defining triggers (push, pull_request, schedule, workflow_dispatch), setting concurrency to prevent duplicate runs, global environment variables, job and step definitions.

See [github-actions-part1-workflow-basics.md](github-actions-part1-workflow-basics.md) for full details.

### Runners

GitHub-hosted runners table (ubuntu, macos, windows), free tier limits by account type, self-hosted runner configuration.

See [github-actions-part1-workflow-basics.md](github-actions-part1-workflow-basics.md) for full details.

### Common Actions

Checkout action with submodules, cache action for dependencies, upload/download artifacts, setup tools (Node.js, Python, Rust, Go, Java, .NET).

See [github-actions-part1-workflow-basics.md](github-actions-part1-workflow-basics.md) for full details.

---

## Part 2: Matrix Builds, Secrets, and Conditionals

**File**: [github-actions-part2-matrix-secrets.md](github-actions-part2-matrix-secrets.md)

### Matrix Builds

Basic matrix with fail-fast option, complex matrix with include/exclude.

See [github-actions-part2-matrix-secrets.md](github-actions-part2-matrix-secrets.md) for full details.

### Secrets

Using secrets in workflows, environment-specific secrets, setting secrets via gh CLI.

See [github-actions-part2-matrix-secrets.md](github-actions-part2-matrix-secrets.md) for full details.

### Conditional Execution

Job conditions (branch, tag checks), step conditions (event type, matrix values), conditional expressions (always, failure, success, cancelled).

See [github-actions-part2-matrix-secrets.md](github-actions-part2-matrix-secrets.md) for full details.

### Outputs and Dependencies

Job outputs and needs, step outputs with GITHUB_OUTPUT.

See [github-actions-part2-matrix-secrets.md](github-actions-part2-matrix-secrets.md) for full details.

---

## Part 3: Reusable Workflows and Releases

**File**: [github-actions-part3-reusable-release.md](github-actions-part3-reusable-release.md)

### Reusable Workflows

Defining reusable workflow with workflow_call, inputs and secrets for reusable workflows, calling reusable workflows.

See [github-actions-part3-reusable-release.md](github-actions-part3-reusable-release.md) for full details.

### Release Workflow

Creating GitHub releases with softprops/action-gh-release, downloading artifacts for release.

See [github-actions-part3-reusable-release.md](github-actions-part3-reusable-release.md) for full details.

### Publish to Package Registries

npm, PyPI, Crates.io, Docker Hub publishing workflows.

See [github-actions-part3-reusable-release.md](github-actions-part3-reusable-release.md) for full details.

### Security Best Practices

Minimal permissions configuration, pinning action versions to SHA, dependency review action.

See [github-actions-part3-reusable-release.md](github-actions-part3-reusable-release.md) for full details.

---

## Part 4: Debugging and Common Patterns

**File**: [github-actions-part4-debugging-patterns.md](github-actions-part4-debugging-patterns.md)

### Debugging

Enabling debug logging (ACTIONS_RUNNER_DEBUG, ACTIONS_STEP_DEBUG), SSH into runner with tmate, local testing with act.

See [github-actions-part4-debugging-patterns.md](github-actions-part4-debugging-patterns.md) for full details.

### Common Patterns

Monorepo path filtering, scheduled jobs with cron, manual workflow with inputs (workflow_dispatch).

See [github-actions-part4-debugging-patterns.md](github-actions-part4-debugging-patterns.md) for full details.

### Checklist

Workflow validation checklist.

See [github-actions-part4-debugging-patterns.md](github-actions-part4-debugging-patterns.md) for full details.

---

## Quick Command Reference

```bash
# Install act for local testing
brew install act

# Run workflow locally
act push

# Run specific job
act -j build

# Set repository secret
gh secret set API_KEY < api_key.txt

# List secrets
gh secret list
```
