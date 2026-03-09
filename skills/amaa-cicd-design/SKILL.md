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
| [github-actions.md](references/github-actions.md) | Use Cases (Quick Reference), Overview, Part 1: Workflow Basics and Runners, Part 2: Matrix Builds, Secrets, and Conditionals, Part 3: Reusable Workflows and Releases, Part 4: Debugging and Common Patterns, Quick Command Reference |
| [cross-platform-builds.md](references/cross-platform-builds.md) | Use Cases (Quick Reference), Overview, Runner Matrix, Multi-Platform CI Workflow, Build Optimization, Checklist |
| [secret-management.md](references/secret-management.md) | Use Cases (Quick Reference), Overview, Secret Hierarchy, Required Secrets by Platform, Using Secrets in Workflows, Security Best Practices, Debugging Secret Issues, Checklist |
| [tdd-enforcement.md](references/tdd-enforcement.md) | Use Cases (Quick Reference), Overview, Core Principles, Coverage Requirements, Complete TDD Workflow, Test Skipping Policy, Mutation Testing, Debug Script, Checklist |
| [release-automation.md](references/release-automation.md) | Use Cases (Quick Reference), Overview, Part Files, Release Pipeline Stages, Semantic Versioning, Version Bumping Automation, Changelog Generation, Checklist |
| [release-automation-part1-complete-workflow.md](references/release-automation-part1-complete-workflow.md) | Table of Contents, Tag-Triggered Release |
| [release-automation-part2-platform-publishing.md](references/release-automation-part2-platform-publishing.md) | Table of Contents, Platform-Specific Publishing, Debug Script |
| [devops-debugging.md](references/devops-debugging.md) | Table of Contents, Debug Script Template, Common Debugging Commands, Troubleshooting Common Issues, Debug Workflow Checklist |
| [gh-cli-scripts.md](references/gh-cli-scripts.md) | Table of Contents, Repository Setup Script, GraphQL Queries, Workflow Management Scripts, Secret Automation, Quick Reference |
| [platform-test-protocols.md](references/platform-test-protocols.md) | Table of Contents, Language-Specific Test Commands, Cross-Platform Test Matrix, Coverage Configuration, Performance Testing, Test Protocol Checklist |
| [github-actions-templates.md](references/github-actions-templates.md) | Table of Contents, Multi-Platform CI Workflow Template, Release Workflow Template, Security Scanning Workflow, GitHub Runners Matrix, Workflow Types Reference |
| [quick-reference-tables.md](references/quick-reference-tables.md) | GitHub Runners Matrix, Workflow Templates, Required Secrets per Platform, TDD Enforcement Rules, Recommended Pipeline Stages, Debug Scripts, Handoff Protocol, Competency Index |
| [error-handling-examples.md](references/error-handling-examples.md) | Error Handling, Examples |

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
