---
name: ao-documentation-writer
description: Technical documentation creation skill for writing module specifications, API contracts, architecture decision records (ADRs), and feature specifications. Follows the 6 C's quality framework.
license: Apache-2.0
compatibility: Works with any codebase. Outputs to standardized documentation directories (/docs/module-specs/, /docs/api-contracts/, /docs/adrs/).
metadata:
  author: Anthropic
  version: 1.0.0
  triggers:
    - Create technical documentation for a module
    - Write API contract documentation
    - Document architecture decisions (ADR)
    - Create feature specifications
context: fork
---

# Documentation Writer Skill

Technical documentation creation skill for the Documentation Writer Agent.

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

- [ ] Complete - all aspects covered
- [ ] Correct - technically accurate
- [ ] Clear - unambiguous language
- [ ] Consistent - same terminology throughout
- [ ] Current - reflects latest decisions
- [ ] Connected - cross-references to related docs

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
