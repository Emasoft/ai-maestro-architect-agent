---
name: amaa-documentation-writing
description: "Use when writing module specs, API contracts, ADRs, or feature docs. Trigger with documentation writing or spec creation request."
context: fork
agent: amaa-documentation-writer
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
3. Create document structure using appropriate template from templates-reference.md
4. Write core content following quality-standards.md
5. Add cross-references to related documents
6. Perform quality check against 6 C's (Complete, Correct, Clear, Consistent, Current, Connected)
7. Commit document and report completion

## Reference Documents

| File | Description |
|------|-------------|
| templates-reference.md | Document templates and formats |
| quality-standards.md | Quality criteria and examples |
| writing-workflow.md | Step-by-step writing process |
| operational-guidelines.md | Document lifecycle rules |
| agent-interactions.md | Agent handoff protocols |
| op-write-module-spec.md | Module spec operation |
| op-write-api-contract.md | API contract operation |
| op-write-adr.md | ADR writing operation |
| op-write-feature-spec.md | Feature spec operation |
| op-write-process-doc.md | Process doc operation |
| op-quality-check-6c.md | Quality check operation |

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

See **Reference Documents** table above for all reference files and their contents.
