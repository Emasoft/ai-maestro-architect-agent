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
| [start-planning-procedure](references/start-planning-procedure.md) | 1 When to use /amaa-start-planning command, 2 Prerequisites before starting planning, 3 Command syntax and arguments, 4 What the command creates, 5 Post-initialization steps, 6 Example workflow after starting planning |
| [requirement-management](references/requirement-management.md) | 1 When to add a new requirement section, 2 When to add a new module, 3 Add requirement syntax and arguments, 4 When to modify existing requirements, 5 Modify requirement syntax and arguments, 6 When to remove requirements, 7 Remove requirement syntax and restrictions, 8 State file changes after operations, 9 Common operation examples |
| [plan-approval-transition](references/plan-approval-transition.md) | 1 When to approve the plan, 2 Prerequisites for plan approval, 3 Approve plan syntax and options, 4 Validation checks performed, 5 GitHub Issue creation process, Module: {module_name}, 8 Approval workflow example |
| [state-file-format](references/state-file-format.md) | 1 Plan phase state file location and purpose, 2 YAML frontmatter structure, 3 Field definitions and allowed values, 4 Requirements sections schema, 5 Modules schema, 6 Exit criteria schema, 7 Reading and parsing the state file, 8 State file lifecycle |
| [troubleshooting](references/troubleshooting.md) | 1 When /amaa-start-planning fails, 2 When checking planning status shows errors, 3 When /amaa-add-requirement fails, 4 When /amaa-modify-requirement fails, 5 When /amaa-remove-requirement fails, 6 When plan approval fails, 7 State file corruption recovery, 8 GitHub Issue creation problems, 9 Exit blocking issues |
| [quick-reference-and-scripts](references/quick-reference-and-scripts.md) | Command Quick Reference, Status Values, Priority Values, Modifiable Fields, Utility Scripts, Complete Planning Workflow Example, Requirement Analysis Scripts |
| [extended-examples-and-resources](references/extended-examples-and-resources.md) | Error Handling Details, Extended Examples, Resources, Command Output Reference |

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

- [quick-reference-and-scripts](references/quick-reference-and-scripts.md) - Command Quick Reference, Status Values, Priority Values, Modifiable Fields, Utility Scripts, Complete Planning Workflow Example, Requirement Analysis Scripts

## Output

| Command | Output |
|---------|--------|
| `/amaa-start-planning` | Creates plan state file and locks goal |
| `/amaa-modify-requirement` | Updates requirement/module status, criteria, priority |
