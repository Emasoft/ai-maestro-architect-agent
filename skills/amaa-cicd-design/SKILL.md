---
name: amaa-cicd-design
description: "Use when designing CI/CD pipelines, GitHub Actions, or release automation. Trigger with CI/CD design request or pipeline task."
context: fork
user-invocable: false
agent: amaa-main
---

# DevOps Expert Skill

## Overview

Design and configure CI/CD pipelines, GitHub Actions workflows, cross-platform builds, secret management, and release processes. Produces workflow YAML, configuration, and documentation -- never executes code directly.

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

## Checklist

Copy this checklist and track your progress:

- [ ] Review project requirements and target platforms
- [ ] Define workflow triggers and select GitHub runners
- [ ] Configure secret management via `gh` CLI
- [ ] Set up TDD enforcement with coverage thresholds (>= 80%)
- [ ] Create multi-platform CI workflow with matrix builds
- [ ] Set up release automation workflow
- [ ] Add debug/validation scripts and document setup
- [ ] Test workflows on all target platforms

## Reference Documents

| Document | Content |
|----------|---------|
| [github-actions.md](references/github-actions.md) | Workflows, runners, matrix builds (Use Cases, Overview, Workflow Structure, Runners) |
| [cross-platform-builds.md](references/cross-platform-builds.md) | Runner matrix, multi-platform CI (Use Cases, Overview, Runner Matrix) |
| [secret-management.md](references/secret-management.md) | Secret hierarchy, env secrets (Use Cases, Overview, Secret Hierarchy) |
| [tdd-enforcement.md](references/tdd-enforcement.md) | Coverage, branch protection (Use Cases, Core Principles, TDD Pipeline Rules) |
| [release-automation.md](references/release-automation.md) | Versioning, changelog (Use Cases, Overview, Complete Release Workflow) |
| [release-automation-part1-complete-workflow.md](references/release-automation-part1-complete-workflow.md) | Release workflow (Tag-Triggered Release) |
| [release-automation-part2-platform-publishing.md](references/release-automation-part2-platform-publishing.md) | Publishing (Platform-Specific Publishing, Homebrew, Docker Hub) |
| [devops-debugging.md](references/devops-debugging.md) | Debug tools (Debug Script Template, Common Debugging Commands) |
| [gh-cli-scripts.md](references/gh-cli-scripts.md) | CLI recipes (Repository Setup Script, Branch Protection Configuration) |
| [platform-test-protocols.md](references/platform-test-protocols.md) | Test protocols (Language-Specific Test Commands) |
| [github-actions-templates.md](references/github-actions-templates.md) | Templates (Multi-Platform CI Workflow Template, Release Workflow Template) |
| [quick-reference-tables.md](references/quick-reference-tables.md) | Quick reference tables (GitHub Runners Matrix, Workflow Templates, Required Secrets per Platform) |
| [error-handling-examples.md](references/error-handling-examples.md) | Error examples |

## Examples

```yaml
# Example: Multi-platform CI workflow trigger
on:
  push:
    branches: [main]
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
```

## Error Handling

| Issue | Cause | Fix |
|-------|-------|-----|
| CI fails, local passes | Environment differences | Check env vars, dependency versions, path sensitivity |
| Workflow not triggering | YAML error or filter mismatch | Validate YAML, check filters, verify Actions enabled |
| Secrets unavailable | Scope or name mismatch | Verify exact name, correct scope, fork limits |
| Deployment timeout | Network or config issues | Increase timeout, check connectivity, verify creds |

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
