---
name: amaa-documentation-writing
description: "Use when writing module specs, API contracts, ADRs, or feature docs. Trigger with documentation writing or spec creation request."
context: fork
user-invocable: false
---

# Documentation Writer Skill

## Overview

Technical documentation creation for module specs, API contracts, ADRs, and feature specs. **DOCUMENTATION ONLY -- never write source code.**

## Checklist

Copy this checklist and track your progress:
- [ ] Receive and parse documentation assignment
- [ ] Gather context from existing code and specifications
- [ ] Select appropriate template from templates-reference.md
- [ ] Write core content following quality standards
- [ ] Add cross-references to related documents
- [ ] Perform 6 C's quality check (Complete, Correct, Clear, Consistent, Current, Connected)
- [ ] Commit document and report completion

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
| Templates | [templates-reference.md](references/templates-reference.md) | Templates (Module Specification Template, API Contract Template, ADR Template, Input Format Examples) |
| Quality Standards | [quality-standards.md](references/quality-standards.md) | 6 C's rules (Documentation Quality Criteria, Must Be 6 C's, Must Include, Must Avoid, Feature Specification Example) |
| Writing Workflow | [writing-workflow.md](references/writing-workflow.md) | Procedure (Step 1: Receive and Parse Assignment, Step 2: Gather Context, Step 3: Create Document Structure) |
| Operational Guidelines | [operational-guidelines.md](references/operational-guidelines.md) | Ops (When to Create New Documents, When to Update Existing, Document Organization, Version Control, Troubleshooting) |
| Agent Interactions | [agent-interactions.md](references/agent-interactions.md) | Coordination (Upstream Agents, Downstream Agents, Peer Agents, Handoff Protocol) |
| Op: Module Spec | [op-write-module-spec.md](references/op-write-module-spec.md) | Detailed module spec writing procedure |
| Op: API Contract | [op-write-api-contract.md](references/op-write-api-contract.md) | Detailed API contract writing procedure |
| Op: ADR | [op-write-adr.md](references/op-write-adr.md) | Detailed ADR writing procedure |
| Op: Feature Spec | [op-write-feature-spec.md](references/op-write-feature-spec.md) | Detailed feature spec writing procedure |
| Op: Process Doc | [op-write-process-doc.md](references/op-write-process-doc.md) | Detailed process doc writing procedure |
| Op: Quality Check | [op-quality-check-6c.md](references/op-quality-check-6c.md) | 6 C's quality check procedure |

## Examples

```
input: "Document the auth-service module"
output: /docs/module-specs/auth-service.md (purpose, interfaces, dependencies, 6 C's verified)

input: "Write an ADR for switching from REST to GraphQL"
output: /docs/adrs/ADR-042-graphql-migration.md (context, decision, consequences)

input: "Create API contract for /api/users endpoint"
output: /docs/api-contracts/users-api.md (endpoints, request/response schemas, error codes)
```

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

- [templates-reference.md](references/templates-reference.md) (Module Specification Template, API Contract Template, ADR Template, Input Format Examples)
- [quality-standards.md](references/quality-standards.md) (Documentation Quality Criteria, Must Be 6 C's, Must Include, Must Avoid, Feature Specification Example)
- [writing-workflow.md](references/writing-workflow.md) (Step 1: Receive and Parse Assignment, Step 2: Gather Context, Step 3: Create Document Structure)
- [agent-interactions.md](references/agent-interactions.md) (Upstream Agents (Receive Input From), Downstream Agents (Provide Output To), Peer Agents (Bidirectional))
