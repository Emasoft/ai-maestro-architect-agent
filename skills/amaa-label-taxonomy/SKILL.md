---
name: amaa-label-taxonomy
description: "Use when managing GitHub labels for the Architect Agent: component, effort, type, and priority labels."
context: fork
user-invocable: false
---

# AMAA Label Taxonomy

## Overview

Provides the label taxonomy for the Architect Agent (AMAA) role. AMAA recommends `component:*` labels, validates `effort:*` estimates, and may suggest `type:*` changes based on architecture analysis. Each role plugin has its own label-taxonomy skill.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Active issue number for architecture work
- Familiarity with AMAA role (see AGENT_OPERATIONS.md)

## Instructions

1. Analyze requirements to identify affected components
2. Review `priority:*` labels to scope design constraints
3. Validate `effort:*` against design complexity
4. Recommend `component:*` labels from module breakdown
5. Create sub-issues with `type:*`, `component:*`, `status:backlog`
6. Update effort label if architecture reveals mismatch
7. Ensure all labels set before handoff to AMOA

## Reference Documents

| Document | Description |
|----------|-------------|
| [label-taxonomy-details.md](references/label-taxonomy-details.md) | Full label tables, kanban columns, commands, mapping rules |
| [examples-extended.md](references/examples-extended.md) | Extended examples with bash commands |
| [op-add-component-labels.md](references/op-add-component-labels.md) | Procedure: adding component labels |
| [op-validate-effort-estimate.md](references/op-validate-effort-estimate.md) | Procedure: validating effort estimates |
| [op-create-sub-issues.md](references/op-create-sub-issues.md) | Procedure: creating sub-issues |
| [op-create-adr-issue.md](references/op-create-adr-issue.md) | Procedure: creating ADR issues |

## Examples

```bash
# After architecture analysis of issue #123 (API + DB changes, effort upgrade)
gh issue edit 123 --add-label "component:api" --add-label "component:database"
gh issue edit 123 --remove-label "effort:s" --add-label "effort:m"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `label not found` | Label does not exist | Create via `gh label create` |
| `permission denied` | No write access | Verify GitHub token scopes |
| `issue not found` | Invalid issue number | Check with `gh issue list` |

## Output

| Output Type | Format |
|-------------|--------|
| Component recommendations | Issue comment listing affected components |
| Label updates | CLI stdout confirmation |
| Sub-issue creation | New issue URL |

## Resources

- **AGENT_OPERATIONS.md** - AMAA role definition
- **amaa-modularization** - Module breakdown procedures
- **references/** - Detailed taxonomy tables, commands, and examples
