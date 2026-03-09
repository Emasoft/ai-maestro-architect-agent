---
name: amaa-label-taxonomy-ops
description: "Use when validating effort estimates, creating sub-issues, or ADR issues. Trigger with label taxonomy ops request."
context: fork
user-invocable: false
agent: amaa-architect-main-agent
---

# AMAA Label Taxonomy (Operations)

## Overview

Operational procedures for the AMAA label taxonomy: validating effort estimates, creating component sub-issues from epics, and creating Architecture Decision Record (ADR) issues.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated

## Instructions

1. Validate effort labels against architecture complexity
2. Create component-specific sub-issues from epics
3. Create ADR issues for significant architectural decisions
4. Link all sub-issues and ADRs to parent issues

## Checklist

Copy this checklist and track your progress:

- [ ] Validate effort label matches architecture complexity
- [ ] Create sub-issues for each component identified
- [ ] Create ADR issues for significant decisions
- [ ] Link all created issues to parents

## Reference Documents

| Document | Content |
|----------|---------|
| [op-validate-effort-estimate.md](references/op-validate-effort-estimate.md) | Purpose, When to Use, Prerequisites, Procedure, Example, Effort Guidelines, Error Handling |
| [op-create-sub-issues.md](references/op-create-sub-issues.md) | Purpose, When to Use, Prerequisites, Procedure, Example, Description, Error Handling |
| [op-create-adr-issue.md](references/op-create-adr-issue.md) | Purpose, When to Use, Prerequisites, Procedure, Example, Status, Error Handling |

## Examples

Example: `gh issue edit 123 --remove-label "effort:s" --add-label "effort:m"` after architecture reveals higher complexity.

## Error Handling

| Issue | Fix |
|-------|-----|
| No effort label found | Recommend effort based on analysis |
| Duplicate ADR number | Re-query and increment |
| Too many sub-issues | Combine related tasks |

## Output

| Type | Description |
|------|-------------|
| Effort updates | CLI stdout confirmation |
| Sub-issue creation | New issue URLs |
| ADR issues | ADR issue URL with status |

## Resources

See Reference Documents table above.
