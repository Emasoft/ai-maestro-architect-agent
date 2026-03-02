---
name: amaa-documentation-writing
description: "Use when writing module specs, API contracts, ADRs, or feature specs following the 6 C's quality framework."
context: fork
user-invocable: false
---

# Documentation Writer Skill

## Overview

Technical documentation creation skill for the Documentation Writer Agent. Provides templates, quality standards, and workflows for producing module specifications, API contracts, architecture decision records (ADRs), and feature specifications. **This skill is for DOCUMENTATION ONLY -- never write source code.**

## Prerequisites

- Access to output directories (`/docs/module-specs/`, `/docs/api-contracts/`, `/docs/adrs/`)
- Read access to source code for reference

## Instructions

1. Receive and parse documentation assignment
2. Gather context from existing code and specifications
3. Create document structure using appropriate template from [templates-reference.md](references/templates-reference.md)
4. Write core content following [quality standards](references/quality-standards.md)
5. Add cross-references to related documents
6. Perform quality check against 6 C's (Complete, Correct, Clear, Consistent, Current, Connected)
7. Commit document and report completion

## Reference Documents

| Document | Path | Contents |
|----------|------|----------|
| Templates | [templates-reference.md](references/templates-reference.md) | Module spec, API contract, ADR, feature spec templates |
| Quality Standards | [quality-standards.md](references/quality-standards.md) | 6 C's criteria, must-include/must-avoid rules |
| Writing Workflow | [writing-workflow.md](references/writing-workflow.md) | Step-by-step procedure for each document type |
| Operational Guidelines | [operational-guidelines.md](references/operational-guidelines.md) | When to create/update docs, versioning, troubleshooting |
| Agent Interactions | [agent-interactions.md](references/agent-interactions.md) | Upstream/downstream agents, handoff protocol |
| Op: Module Spec | [op-write-module-spec.md](references/op-write-module-spec.md) | Detailed module spec writing procedure |
| Op: API Contract | [op-write-api-contract.md](references/op-write-api-contract.md) | Detailed API contract writing procedure |
| Op: ADR | [op-write-adr.md](references/op-write-adr.md) | Detailed ADR writing procedure |
| Op: Feature Spec | [op-write-feature-spec.md](references/op-write-feature-spec.md) | Detailed feature spec writing procedure |
| Op: Process Doc | [op-write-process-doc.md](references/op-write-process-doc.md) | Detailed process doc writing procedure |
| Op: Quality Check | [op-quality-check-6c.md](references/op-quality-check-6c.md) | 6 C's quality check procedure |

## Examples

Document auth-service module: Read code → Use Module Specification template → Write purpose, interfaces, dependencies → Quality check 6 C's → Output to `/docs/module-specs/auth-service.md`

## Error Handling

| Error | Solution |
|-------|----------|
| Missing context | Request source access from orchestrator |
| Template not found | Use templates-reference.md |
| Quality check failed | Revise content, recheck each 6 C's criterion |
| Cross-reference broken | Update link or remove reference |

## Output

| Artifact | Location |
|----------|----------|
| Module Specification | `/docs/module-specs/<module-name>.md` |
| API Contract | `/docs/api-contracts/<api-name>.md` |
| ADR | `/docs/adrs/ADR-<NNN>-<title>.md` |
| Feature Specification | `/docs_dev/requirements/<feature-name>.md` |

## Resources

- [templates-reference.md](references/templates-reference.md) - All document templates
- [quality-standards.md](references/quality-standards.md) - Quality criteria
- [writing-workflow.md](references/writing-workflow.md) - Step-by-step procedure
- [agent-interactions.md](references/agent-interactions.md) - Agent coordination
