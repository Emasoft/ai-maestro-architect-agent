---
name: amaa-documentation-writing-ops
description: "Use when writing API contracts, ADRs, feature specs, or quality checks. Trigger with documentation ops request."
context: fork
user-invocable: false
agent: amaa-documentation-writer
---

# Documentation Writer Operations

## Overview

Operational procedures for writing API contracts, ADRs, feature specifications, process documentation, and performing 6 C's quality checks.

## Prerequisites

- Access to output directories (`/docs/`, `/docs_dev/requirements/`)

## Instructions

1. Identify the document type requested (API contract, ADR, feature spec, process doc)
2. Follow the corresponding operation procedure from reference documents
3. Apply 6 C's quality check using op-quality-check-6c.md
4. Commit document and report completion

## Checklist

Copy this checklist and track your progress:
- [ ] Identify document type and select operation procedure
- [ ] Gather required inputs per the operation
- [ ] Write document following the operation template
- [ ] Apply 6 C's quality check
- [ ] Commit and report

## Reference Documents

| Document | Content |
|----------|---------|
| [op-write-api-contract.md](references/op-write-api-contract.md) | Purpose, When to Use, Inputs, Procedure, Overview, Authentication, Error Handling |
| [op-write-adr.md](references/op-write-adr.md) | Purpose, When to Use, Inputs, Procedure, Example, Context, Error Handling |
| [op-write-feature-spec.md](references/op-write-feature-spec.md) | Purpose, When to Use, Inputs, Procedure, Overview, User Stories, Error Handling |
| [op-write-process-doc.md](references/op-write-process-doc.md) | Purpose, When to Use, Inputs, Procedure, Overview, Roles and Responsibilities, Error Handling |
| [op-quality-check-6c.md](references/op-quality-check-6c.md) | Purpose, When to Use, Inputs, Procedure, Summary, Issues Found, Error Handling |

## Examples

Example: `"Write an ADR for switching from REST to GraphQL"` produces `/docs/adrs/ADR-042-graphql-migration.md`

Example: `"Create API contract for /api/users"` produces `/docs/api-contracts/users-api.md`

## Error Handling

| Issue | Fix |
|-------|-----|
| Missing context | Request source access from orchestrator |
| Quality check failed | Revise content, recheck 6 C's |

## Output

| Type | Description |
|------|-------------|
| API Contract | `/docs/api-contracts/<api-name>.md` |
| ADR | `/docs/adrs/ADR-<NNN>-<title>.md` |
| Feature Spec | `/docs_dev/requirements/<feature-name>.md` |
| Process Doc | `/docs/workflows/<process-name>.md` |

## Resources

See Reference Documents table above.
