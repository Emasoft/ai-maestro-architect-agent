---
name: amaa-cicd-design
description: "Use when designing CI/CD pipelines, GitHub Actions workflows, cross-platform builds, and release automation."
context: fork
user-invocable: false
agent: amaa-main
---

# DevOps Expert Skill

## Overview

Design and configure CI/CD pipelines, GitHub Actions workflows, cross-platform build automation, secret management, and release processes. This skill produces workflow YAML files, configuration, and documentation -- it never executes code directly.

## Prerequisites

- GitHub Actions access on target repository
- GitHub CLI (`gh`) installed and authenticated
- Access to required secrets (API keys, certificates)

## Instructions

1. Review project requirements and target platforms
2. Define workflow triggers and select GitHub runners
3. Configure secret management via `gh` CLI
4. Set up TDD enforcement with coverage thresholds (>= 80%)
5. Create multi-platform CI workflow with matrix builds
6. Set up release automation workflow
7. Add debug/validation scripts and document setup
8. Test workflows on all target platforms

## Reference Documents

| Document | Content |
|----------|---------|
| [github-actions.md](references/github-actions.md) | Workflow structure, runners, matrix builds, secrets, reusable workflows |
| [cross-platform-builds.md](references/cross-platform-builds.md) | Runner matrix, free tier, multi-platform CI, platform-specific jobs |
| [secret-management.md](references/secret-management.md) | Secret hierarchy, creating/using secrets, environment secrets |
| [tdd-enforcement.md](references/tdd-enforcement.md) | Coverage requirements, per-language config, branch protection |
| [release-automation.md](references/release-automation.md) | Pipeline stages, semantic versioning, changelog generation |
| [release-automation-part1-complete-workflow.md](references/release-automation-part1-complete-workflow.md) | Complete release workflow |
| [release-automation-part2-platform-publishing.md](references/release-automation-part2-platform-publishing.md) | Platform-specific publishing |
| [devops-debugging.md](references/devops-debugging.md) | Debugging techniques and troubleshooting |
| [gh-cli-scripts.md](references/gh-cli-scripts.md) | GitHub CLI script recipes |
| [platform-test-protocols.md](references/platform-test-protocols.md) | Platform-specific test protocols |
| [github-actions-templates.md](references/github-actions-templates.md) | Ready-to-use workflow templates |
| [quick-reference-tables.md](references/quick-reference-tables.md) | Runners, secrets, scripts, competency index |
| [error-handling-examples.md](references/error-handling-examples.md) | Common errors and workflow examples |

## Examples

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
      - run: pytest --cov=src tests/
```

## Error Handling

| Issue | Cause | Fix |
|-------|-------|-----|
| CI fails, local passes | Environment differences | Check env vars, dependency versions, path case sensitivity |
| Workflow not triggering | YAML error or filter mismatch | Validate YAML, check branch/path filters, verify Actions enabled |
| Secrets unavailable | Scope or name mismatch | Verify exact name, correct scope, fork limitations |
| Deployment timeout | Network or config issues | Increase timeout, check connectivity, verify credentials |

See [error-handling-examples.md](references/error-handling-examples.md) for detailed solutions.

## Output

| Output Type | Description |
|-------------|-------------|
| Workflow YAML | `.github/workflows/` directory with CI/CD files |
| Secret Docs | Instructions for configuring secrets via `gh` CLI |
| Debug Scripts | Workflow validation and local debugging scripts |
| Release Checklist | Step-by-step release process guide |

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Semantic Versioning](https://semver.org/)
