---
name: eaa-documentation-writer
description: Use when writing module specs, API contracts, ADRs, or feature specs. Follows 6 C's quality framework. Trigger with technical documentation requests for modules or architecture.
version: 1.0.0
license: Apache-2.0
compatibility: Works with any codebase. Outputs to standardized documentation directories (/docs/module-specs/, /docs/api-contracts/, /docs/adrs/). Requires AI Maestro installed.
metadata:
  author: Emasoft
  triggers: "Create technical documentation for a module, Write API contract documentation, Document architecture decisions (ADR), Create feature specifications"
context: fork
---

# Documentation Writer Skill

## Overview

Technical documentation creation skill for the Documentation Writer Agent. This skill provides templates, quality standards, and workflows for producing module specifications, API contracts, architecture decision records (ADRs), and feature specifications.

## Prerequisites

- Access to documentation output directories (`/docs/module-specs/`, `/docs/api-contracts/`, `/docs/adrs/`)
- Understanding of the 6 C's quality framework
- Read access to source code for reference

## Instructions

1. Receive and parse documentation assignment
2. Gather context from existing code and specifications
3. Create document structure using appropriate template
4. Write core content following quality standards
5. Add cross-references to related documents
6. Perform quality check against 6 C's
7. Commit and report completion

## Output

| Artifact | Location | Format | Contains |
|----------|----------|--------|----------|
| Module Specification | `/docs/module-specs/<module-name>.md` | Markdown | Purpose, interfaces, dependencies, configuration |
| API Contract | `/docs/api-contracts/<api-name>.md` | Markdown | Endpoints, request/response schemas, authentication |
| Architecture Decision Record | `/docs/adrs/ADR-<NNN>-<title>.md` | Markdown | Context, decision, consequences, alternatives |
| Feature Specification | `/docs_dev/requirements/<feature-name>.md` | Markdown | User stories, requirements, acceptance criteria |
| Process Documentation | `/docs/workflows/<process-name>.md` | Markdown | Workflow steps, responsibilities, tooling |

---

## Table of Contents

- 1. Document Templates
- 2. Quality Standards
- 3. Writing Workflow
- 4. Operational Guidelines
- 5. Agent Interactions

---

## Quick Reference

### Document Types

| Type | Template | Purpose |
|------|----------|---------|
| Module Specification | [templates-reference.md](references/templates-reference.md) | Technical spec for implementation |
| API Contract | [templates-reference.md](references/templates-reference.md) | Endpoint documentation |
| ADR | [templates-reference.md](references/templates-reference.md) | Architecture decisions |
| Feature Specification | [templates-reference.md](references/templates-reference.md) | User stories and requirements |

### Output Locations

| Document Type | Directory |
|---------------|-----------|
| Module Specs | `/docs/module-specs/` |
| API Contracts | `/docs/api-contracts/` |
| ADRs | `/docs/adrs/` |
| User Requirements | `/docs_dev/requirements/` |
| Process Docs | `/docs/workflows/` |

### Quality Checklist

Copy this checklist and track your progress:

- [ ] Receive and parse documentation assignment
- [ ] Gather context from existing code and specifications
- [ ] Create document structure using appropriate template
- [ ] Write core content following quality standards
- [ ] Add cross-references to related documents
- [ ] Perform quality check against 6 C's:
  - [ ] Complete - all aspects covered
  - [ ] Correct - technically accurate
  - [ ] Clear - unambiguous language
  - [ ] Consistent - same terminology throughout
  - [ ] Current - reflects latest decisions
  - [ ] Connected - cross-references to related docs
- [ ] Commit document to appropriate location
- [ ] Report completion to orchestrator

---

## Reference Documents

### Templates Reference
For all document templates, see: [templates-reference.md](references/templates-reference.md)
- 1. Module Specification Template
- 2. API Contract Template
- 3. Architecture Decision Record (ADR) Template
- 4. Input Format Examples

### Quality Standards
For documentation quality criteria, see: [quality-standards.md](references/quality-standards.md)
- 1. Documentation Quality Criteria
  - 1.1 Must Be (6 C's)
  - 1.2 Must Include
  - 1.3 Must Avoid
- 2. Feature Specification Example

### Writing Workflow
For step-by-step procedure, see: [writing-workflow.md](references/writing-workflow.md)
- 1. Step 1: Receive and Parse Assignment
- 2. Step 2: Gather Context
- 3. Step 3: Create Document Structure
- 4. Step 4: Write Core Content
- 5. Step 5: Add Cross-References
- 6. Step 6: Quality Check
- 7. Step 7: Commit and Report

### Operational Guidelines
For document management, see: [operational-guidelines.md](references/operational-guidelines.md)
- 1. When to Create New Documents
- 2. When to Update Existing Documents
- 3. Document Organization
- 4. Version Control
- 5. Troubleshooting

### Agent Interactions
For agent coordination, see: [agent-interactions.md](references/agent-interactions.md)
- 1. Upstream Agents (Receive Input From)
- 2. Downstream Agents (Provide Output To)
- 3. Peer Agents (Bidirectional)
- 4. Handoff Protocol

---

## IRON RULE

**This skill is for DOCUMENTATION ONLY. NEVER write source code.**

All code examples in documentation are illustrative only.

## Examples

### Example 1: Write Module Specification

```
Assignment: Document the auth-service module

1. Read existing auth-service code
2. Use Module Specification template
3. Document:
   - Purpose and responsibilities
   - Public interfaces
   - Dependencies
   - Configuration options
4. Quality check: Complete, Correct, Clear, Consistent, Current, Connected
5. Output: /docs/module-specs/auth-service.md
```

### Example 2: Create Architecture Decision Record

```
Assignment: Document decision to use PostgreSQL

1. Use ADR template
2. Document:
   - Context: Database selection needed
   - Decision: PostgreSQL chosen
   - Consequences: Pros and cons
   - Alternatives considered
3. Output: /docs/adrs/ADR-001-database-selection.md
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Missing context | Source code unavailable | Request access from orchestrator |
| Template not found | Template file missing | Use templates-reference.md |
| Quality check failed | 6 C's not met | Revise content, recheck each criterion |
| Cross-reference broken | Linked doc moved/deleted | Update link or remove reference |
| Duplicate ADR number | Numbering conflict | Check existing ADRs, use next available |

## Resources

- [templates-reference.md](references/templates-reference.md) - All document templates
- [quality-standards.md](references/quality-standards.md) - Documentation quality criteria
- [writing-workflow.md](references/writing-workflow.md) - Step-by-step procedure
- [operational-guidelines.md](references/operational-guidelines.md) - Document management
- [agent-interactions.md](references/agent-interactions.md) - Agent coordination
