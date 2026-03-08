---
name: amaa-cicd-design
description: "Use when designing CI/CD pipelines, GitHub Actions, or release automation. Trigger with CI/CD design request or pipeline task."
context: fork
user-invocable: false
agent: amaa-cicd-designer
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

- [ ] Define triggers and runners
- [ ] Configure secrets and TDD
- [ ] Create CI and release workflows

## Reference Documents

| Document | Content |
|----------|---------|
| github-actions.md | Workflow basics, matrix builds, reusable workflows |
| cross-platform-builds.md | Runner matrix, multi-platform CI, optimization |
| secret-management.md | Secret hierarchy, per-platform secrets, security |
| tdd-enforcement.md | Coverage requirements, TDD workflow, mutation testing |
| release-automation.md | Release pipeline, semver, changelog generation |
| release-automation-part1-complete-workflow.md | Tag-triggered release workflow |
| release-automation-part2-platform-publishing.md | Platform publishing, debug script |
| devops-debugging.md | Debug templates, troubleshooting, common commands |
| gh-cli-scripts.md | Repo setup, GraphQL, workflow and secret scripts |
| platform-test-protocols.md | Test commands, cross-platform matrix, coverage |
| github-actions-templates.md | CI/release/security workflow templates |
| quick-reference-tables.md | Runners, secrets, pipelines, debug quick-ref |
| error-handling-examples.md | Error handling patterns and examples |

## Error Handling

| Issue | Cause | Fix |
|-------|-------|-----|
| CI fails, local passes | Environment differences | Check env vars, dependency versions, path sensitivity |
| Workflow not triggering | YAML error or filter mismatch | Validate YAML, check filters, verify Actions enabled |
| Secrets unavailable | Scope or name mismatch | Verify exact name, correct scope, fork limits |
| Deployment timeout | Network or config issues | Increase timeout, check connectivity, verify creds |

## Examples

Example: `matrix: os: [ubuntu-latest, macos-latest, windows-latest]`

## Output

| Output Type | Description |
|-------------|-------------|
| Workflow YAML | `.github/workflows/` directory with CI/CD files |
| Secret Docs | Instructions for configuring secrets via `gh` CLI |
| Debug Scripts | Workflow validation and local debugging scripts |
| Release Checklist | Step-by-step release process guide |

## Resources

See Reference Documents table above.
