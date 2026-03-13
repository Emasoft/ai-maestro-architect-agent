---
name: amaa-planning-patterns-ops
description: "Use when enforcing plans, verifying requirements, or linking to GitHub. Trigger with planning ops request."
context: fork
user-invocable: false
agent: ai-maestro-architect-agent-main-agent
---

# Planning Patterns Operations

## Overview

Operational procedures for enforcing, validating, and linking planning outputs. Covers enforcement mechanisms, scripts, TDD integration, requirement immutability, plan verification, and GitHub issue linking.

## Prerequisites

- Completed planning phases from amaa-planning-patterns core skill

## Instructions

1. Run enforcement checks using validate_plan.py and thresholds.py
2. Apply TDD planning principles to implementation tasks
3. Verify plan completeness using the plan verification guide
4. Link all plans to GitHub issues per plan-file-linking requirements

## Checklist

Copy this checklist and track your progress:

- [ ] Run plan validation and fix issues
- [ ] Apply TDD planning to code tasks
- [ ] Verify requirement immutability compliance
- [ ] Complete plan verification checklist
- [ ] Link plans to GitHub issues

## Reference Documents

| Document | Content |
|----------|---------|
| [enforcement-mechanisms.md](references/enforcement-mechanisms.md) | Overview of Enforcement, Plan Validation Script (validate_plan.py), Shared Thresholds Module (thresholds.py), Handoff Protocols, Integration Workflow |
| [scripts-reference.md](references/scripts-reference.md) | Universal Analysis Scripts, Core Planning Scripts, Template Generation Scripts, Analysis Scripts, Task Tracker Scripts |
| [tdd-planning.md](references/tdd-planning.md) | TDD Planning Principles, TDD Phase Planning, TDD Task Template Extension, TDD Verification Checklist, Integration with Planning Phases |
| [requirement-immutability.md](references/requirement-immutability.md) | Planning Phase Requirement Check, Plan Structure Requirements, Forbidden Planning Actions, Correct Planning Approach |
| [plan-verification-guide.md](references/plan-verification-guide.md) | Overview, Part 1: Verification Patterns, Part 2: Checklist Template & Task Tracker Integration, Part 3: Examples, Best Practices, Troubleshooting, Related Documentation |
| [plan-file-linking.md](references/plan-file-linking.md) | Purpose, Linking Requirements, Overview, Implementation Plan, Sub-Plans, Plan File Naming Convention, Automatic Linking |

## Examples

Example: `"Validate plan and link to GH-42"` triggers enforcement checks and GitHub linking.

## Error Handling

| Issue | Fix |
|-------|-----|
| Validation failing | Run `validate_plan.py --verbose` |
| Missing plan links | Check plan-file-linking requirements |
| TDD steps skipped | Review tdd-planning checklist |

## Output

| Type | Description |
|------|-------------|
| Validation report | Plan quality assessment |
| Linked plans | Plans connected to GitHub issues |

## Resources

See Reference Documents table above.
