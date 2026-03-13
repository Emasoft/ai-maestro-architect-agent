---
name: amaa-cicd-design-ops
description: "Use when debugging CI/CD, scripting with GH CLI, or referencing templates. Trigger with CI/CD ops or debugging request."
context: fork
user-invocable: false
agent: ai-maestro-architect-agent-main-agent
---

# DevOps Expert Skill (Operations)

## Overview

Debugging, scripting, testing protocols, workflow templates, and quick reference for CI/CD operations.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated

## Instructions

1. Identify the operational issue (debugging, testing, scripting, or template selection)
2. Consult the relevant reference document for patterns and commands
3. Apply templates or scripts to your workflow configuration
4. Validate using debug checklists and test protocols

## Checklist

Copy this checklist and track your progress:

- [ ] Debug workflow issues using debug scripts and commands
- [ ] Configure test protocols for target platforms and languages
- [ ] Apply workflow templates for CI, release, or security scanning

## Reference Documents

| Document | Content |
|----------|---------|
| [devops-debugging.md](references/devops-debugging.md) | Debug Script Template, Common Debugging Commands, Troubleshooting Common Issues, Debug Workflow Checklist |
| [gh-cli-scripts.md](references/gh-cli-scripts.md) | Repository Setup Script, GraphQL Queries, Workflow Management Scripts, Secret Automation, Quick Reference |
| [platform-test-protocols.md](references/platform-test-protocols.md) | Language-Specific Test Commands, Cross-Platform Test Matrix, Coverage Configuration, Performance Testing, Test Protocol Checklist |
| [github-actions-templates.md](references/github-actions-templates.md) | Multi-Platform CI Workflow Template, Release Workflow Template, Security Scanning Workflow, GitHub Runners Matrix, Workflow Types Reference |
| [quick-reference-tables.md](references/quick-reference-tables.md) | GitHub Runners Matrix, Workflow Templates, Required Secrets per Platform, TDD Enforcement Rules, Recommended Pipeline Stages, Debug Scripts, Handoff Protocol |
| [error-handling-examples.md](references/error-handling-examples.md) | Error Handling, Examples |

## Examples

Example: `actionlint .github/workflows/ci.yml` to validate workflow syntax locally

## Error Handling

| Issue | Fix |
|-------|-----|
| Debug script fails | Check `act` and `actionlint` are installed |
| Test matrix mismatch | Verify runner availability and OS compatibility |

## Output

| Type | Description |
|------|-------------|
| Debug reports | Workflow validation and troubleshooting results |
| Test configs | Platform-specific test and coverage configurations |

## Resources

See Reference Documents table above.
