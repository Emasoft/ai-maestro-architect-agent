---
name: amaa-requirements-analysis
description: "Use when managing requirements, initializing plans, or approving transitions. Trigger with requirements analysis or plan initialization request."
user-invocable: false
context: fork
---

# Planning Commands Skill

## Overview

Handles all planning phase commands for the Architect Agent. The planning phase gathers requirements, defines modules, and creates the implementation plan before code is written.

## Prerequisites

- Python 3.8+ with PyYAML installed
- GitHub CLI (`gh`) authenticated for issue creation
- Write access to `.claude/` directory

## Checklist

Copy this checklist and track your progress:

- [ ] Start planning session with goal description
- [ ] Add all required requirements
- [ ] Add all modules with criteria and priority
- [ ] Track progress with planning-status
- [ ] Modify requirements as needed
- [ ] Approve the plan
- [ ] Begin orchestration

## Instructions

1. Start planning: `/start-planning "goal description"`
2. Add requirements: `/add-requirement requirement "Name"`
3. Add modules: `/add-requirement module "name" --criteria "..." --priority high`
4. Track progress: `/planning-status`
5. Modify as needed: `/modify-requirement requirement "Name" --status complete`
6. Approve plan: `/approve-plan`
7. Begin orchestration: `/start-orchestration`

## Reference Documents

| Document | Content |
|----------|---------|
| [start-planning-procedure](references/start-planning-procedure.md) | `/start-planning` command (1 When to use /start-planning command, 2 Prerequisites before starting planning) |
| [requirement-management](references/requirement-management.md) | Add/modify/remove requirements (1 When to add a new requirement section, 2 When to add a new module) |
| [plan-approval-transition](references/plan-approval-transition.md) | Approval validation (1 When to approve the plan, 2 Prerequisites for plan approval) |
| [state-file-format](references/state-file-format.md) | State file schema (1 Plan phase state file location and purpose, 2 YAML frontmatter structure) |
| [troubleshooting](references/troubleshooting.md) | Common issues and recovery (1 When /start-planning fails, 2 When /planning-status shows errors) |
| [quick-reference-and-scripts](references/quick-reference-and-scripts.md) | Command table, status/priority values, utility scripts |
| [extended-examples-and-resources](references/extended-examples-and-resources.md) | Extended examples and command output reference |

## Examples

```bash
/start-planning "Build a REST API for user management"
/add-requirement module "user-crud" --criteria "CRUD operations" --priority critical
/modify-requirement requirement "Functional Requirements" --status complete
/planning-status --verbose
/approve-plan
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| State file not found | Planning not started | Run `/start-planning` first |
| Approval prerequisites failed | Incomplete requirements | Mark all sections complete |
| Module has GitHub Issue | Cannot remove linked module | Use `--force` or close issue first |
| gh CLI auth failed | Not logged in | Run `gh auth login` |

## Output

| Command | Output |
|---------|--------|
| `/planning-status` | Formatted table: phase status, requirements progress, modules |
| `/approve-plan` | Transition summary with created GitHub Issue URLs |

## Resources

- [requirement-management.md](references/requirement-management.md) - Core requirement operations (1 When to add a new requirement section, 2 When to add a new module)
- [plan-approval-transition.md](references/plan-approval-transition.md) - Approval workflow (1 When to approve the plan, 2 Prerequisites for plan approval)
- [quick-reference-and-scripts.md](references/quick-reference-and-scripts.md) - Quick ref and utility scripts (Command Quick Reference, Status Values, Priority Values, Modifiable Fields, Utility Scripts)
- [extended-examples-and-resources.md](references/extended-examples-and-resources.md) - Extended examples
