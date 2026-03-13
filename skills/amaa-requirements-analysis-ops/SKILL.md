---
name: amaa-requirements-analysis-ops
description: "Use when troubleshooting requirements analysis or needing quick reference. Trigger with requirements ops request."
context: fork
user-invocable: false
agent: ai-maestro-architect-agent-main-agent
---

# Requirements Analysis Operations

## Overview

Covers troubleshooting, quick reference tables, utility scripts, and extended examples for the planning phase. Use when debugging planning commands, looking up status/priority values, or running utility scripts.

## Prerequisites

- Planning phase initialized via `/amaa-start-planning`

## Instructions

1. Diagnose planning command failures using troubleshooting reference
2. Look up command syntax, status values, and priority values in quick reference
3. Run utility scripts for plan validation and export
4. Follow extended examples for complex planning workflows

## Checklist

Copy this checklist and track your progress:

- [ ] Identify the planning issue or command failure
- [ ] Consult troubleshooting reference for resolution
- [ ] Run prerequisite check script if needed
- [ ] Verify resolution by checking plan state file

## Reference Documents

| Document | Content |
|----------|---------|
| [troubleshooting.md](references/troubleshooting.md) | When /amaa-start-planning fails, When Checking Planning Status Shows Errors, When /amaa-add-requirement fails, When /amaa-modify-requirement fails, When /amaa-remove-requirement fails, When Plan Approval Fails, State file corruption recovery |
| [quick-reference-and-scripts.md](references/quick-reference-and-scripts.md) | Command Quick Reference, Status Values, Priority Values, Modifiable Fields, Utility Scripts, Complete Planning Workflow Example, Requirement Analysis Scripts |
| [extended-examples-and-resources.md](references/extended-examples-and-resources.md) | Error Handling Details, Extended Examples, Resources, Command Output Reference |

## Examples

Example: `python3 scripts/check_plan_prerequisites.py --fix-suggestions` to diagnose and fix plan approval failures.

## Error Handling

| Issue | Fix |
|-------|-----|
| State file parse error | Check YAML syntax, restore from backup |
| gh CLI auth failed | Run `gh auth login` |
| Module has GitHub Issue | Close issue first or use `--force` |

## Output

| Type | Description |
|------|-------------|
| Diagnostic info | Troubleshooting steps and resolution |
| Script output | Plan validation results and export files |

## Resources

See Reference Documents table above.
