---
name: amaa-label-taxonomy
description: "Use when managing GitHub labels for the Architect Agent: component, effort, type, and priority labels. Trigger with label management or taxonomy request."
context: fork
agent: ai-maestro-architect-agent-main-agent
user-invocable: false
---

# AMAA Label Taxonomy

## Overview

Provides the label taxonomy for the Architect Agent (AMAA) role. AMAA recommends `component:*` labels, validates `effort:*` estimates, and may suggest `type:*` changes based on architecture analysis. Each role plugin has its own label-taxonomy skill.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Active issue number for architecture work
- Familiarity with AMAA role (see AGENT_OPERATIONS.md)

## Checklist

Copy this checklist and track your progress:

- [ ] Analyze requirements to identify affected components
- [ ] Review `priority:*` labels to scope design constraints
- [ ] Validate `effort:*` against design complexity
- [ ] Recommend `component:*` labels from module breakdown
- [ ] Create sub-issues with `type:*`, `component:*`, `status:backlog`
- [ ] Update effort label if architecture reveals mismatch
- [ ] Ensure all labels set before handoff to AMOA

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
| [label-taxonomy-details.md](references/label-taxonomy-details.md) | Component Labels (`component:*`), Kanban Columns (Canonical 5-Column System), Type Labels AMAA Clarifies, Priority Labels (`priority:*`) - Read by AMAA, Effort Labels (`effort:*`) - Validated by AMAA, Architecture-to-Labels Mapping, Architecture Breakdown |
| [examples-extended.md](references/examples-extended.md) | Extended examples with bash commands (Example 1: Adding Component Labels After Architecture Analysis, Example 2: Validating Effort Estimate, Example 3: Creating Component-Specific Sub-Issues, Example 4: Architecture Decision Record (ADR)) |
| [op-add-component-labels.md](references/op-add-component-labels.md) | Purpose, When to Use, Prerequisites, Procedure, Example, Component Label Reference, Error Handling |

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
