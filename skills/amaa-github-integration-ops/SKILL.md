---
name: amaa-github-integration-ops
description: "Use when troubleshooting GitHub integration or managing edge cases. Trigger with GitHub ops request."
context: fork
user-invocable: false
agent: amaa-architect-main-agent
---

# GitHub Integration Operations

## Overview

Operational references for GitHub integration: CLI authentication, edge case handling, status-to-label mapping, troubleshooting, and design lifecycle workflow.

## Prerequisites

- Core GitHub integration skill (`amaa-github-integration`) understood

## Instructions

1. Verify gh CLI auth using the verification procedure reference
2. Handle edge cases (duplicate issues, missing UUIDs, CLI unavailable)
3. Use status mapping to manage design-to-label synchronization
4. Follow troubleshooting guide for CLI, document, issue, or sync errors

## Checklist

Copy this checklist and track your progress:

- [ ] Verify gh CLI is installed and authenticated
- [ ] Review edge cases relevant to current operation
- [ ] Confirm status-to-label mapping is correct
- [ ] Follow lifecycle workflow for end-to-end integration

## Reference Documents

| Document | Content |
|----------|---------|
| [op-verify-gh-cli-auth.md](references/op-verify-gh-cli-auth.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Installation Commands, Required Token Scopes, Error Handling, Related Operations |
| [edge-cases.md](references/edge-cases.md) | Issue Already Exists, Design Has No UUID, gh CLI Not Available |
| [status-mapping.md](references/status-mapping.md) | Design Status Values, GitHub Label Mapping, Valid Status Transitions, Label Naming Convention, Automated Label Management, Manual Label Operations |
| [troubleshooting.md](references/troubleshooting.md) | gh CLI Errors, Document Errors, Issue Errors, Sync Errors |
| [design-lifecycle-workflow.md](references/design-lifecycle-workflow.md) | Steps, Full Example |

## Examples

Example: `gh auth status` to verify authentication before any GitHub operation

## Error Handling

| Issue | Fix |
|-------|-----|
| gh CLI not found | `brew install gh` |
| Token expired | `gh auth refresh` |
| Status label conflict | Remove old labels manually, re-run sync |

## Output

| Type | Description |
|------|-------------|
| Auth verification | Confirmation of gh CLI authentication status |
| Sync result | Labels updated on GitHub issues |

## Resources

See Reference Documents table above.
