---
name: amaa-requirements-analysis
description: "Use when managing requirements, initializing plans, or approving transitions. Trigger with requirements analysis or plan initialization request."
agent: amaa-architect-main-agent
user-invocable: false
context: fork
---

# Requirements Analysis Skill

## Overview

Handles all planning phase commands for the Architect Agent. The planning phase gathers requirements, defines modules, and creates the implementation plan before code is written.

## Prerequisites

- Python 3.8+
- GitHub CLI (`gh`) authenticated for issue creation
- Write access to `.claude/` directory

## Checklist

Copy this checklist and track your progress:

- [ ] Start planning session with goal description
- [ ] Add all required requirements
- [ ] Add all modules with criteria and priority
- [ ] Track progress by reviewing state file
- [ ] Modify requirements as needed
- [ ] Mark all sections and modules as complete
- [ ] Begin orchestration

## Instructions

1. Start planning: `/amaa-start-planning "goal description"`
2. Add requirements: `/amaa-add-requirement requirement "Name"`
3. Add modules: `/amaa-add-requirement module "name" --criteria "..." --priority high`
4. Track progress: review `.claude/orchestrator-plan-phase.local.md`
5. Modify as needed: `/amaa-modify-requirement requirement "Name" --status complete`
6. Mark all sections and modules complete when plan is ready
7. Begin orchestration phase

## Reference Documents

| Document | Content |
|----------|---------|
| start-planning-procedure.md | Planning session setup and initialization |
| requirement-management.md | Add, modify, and remove requirements |
| plan-approval-transition.md | Plan approval and GitHub issue creation |
| state-file-format.md | State file schema and field definitions |
| troubleshooting.md | Common errors and recovery steps |
| quick-reference-and-scripts.md | Command reference and utility scripts |
| extended-examples-and-resources.md | Extended examples and output reference |

## Examples

```bash
/amaa-start-planning "Build a REST API for user management"
/amaa-add-requirement module "user-crud" --criteria "CRUD operations" --priority critical
/amaa-modify-requirement requirement "Functional Requirements" --status complete
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| State file not found | Planning not started | Run `/amaa-start-planning` first |
| Approval prerequisites failed | Incomplete requirements | Mark all sections complete |
| Module has GitHub Issue | Cannot remove linked module | Use `--force` or close issue first |
| gh CLI auth failed | Not logged in | Run `gh auth login` |

## Resources

- quick-reference-and-scripts.md - Command reference and utility scripts

## Output

| Command | Output |
|---------|--------|
| `/amaa-start-planning` | Creates plan state file and locks goal |
| `/amaa-modify-requirement` | Updates requirement/module status, criteria, priority |
