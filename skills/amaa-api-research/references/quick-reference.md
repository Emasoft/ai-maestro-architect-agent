# Quick Reference

## Table of Contents

### Research Procedures
For the step-by-step research workflow, see [research-procedure.md](research-procedure.md):
- 1. Step 1: Understand Requirements
  - 1.1 Input from Orchestrator
  - 1.2 Acknowledgment Format
  - 1.3 Verification Checklist
- 2. Step 2: Gather Information
  - 2.1 Sources to Consult (in order)
  - 2.2 Information Verification Checklist
- 3. Step 3: Document Findings
  - 3.1 Document Types to Create
  - 3.2 Verification Checklist
- 4. Step 4: Report to Orchestrator
  - 4.1 Minimal Report Format
  - 4.2 Verification Checklist

### Output Templates
For all documentation templates, see [output-templates.md](output-templates.md):
- 1. API Overview Document Template
- 2. Authentication Guide Template
- 3. Endpoints Reference Template
- 4. Integration Guide Template
- 5. Configuration Template

### Tools Reference
For available tools and usage, see [tools-reference.md](tools-reference.md):
- 1. Read Tool - for local files
- 2. WebFetch Tool - for online documentation
- 3. WebSearch Tool - for finding resources
- 4. Write Tool - for documentation output
- 5. Glob/Grep Tools - for finding existing code

### Research Scenarios
For common research patterns, see [research-scenarios.md](research-scenarios.md):
- 1. Scenario 1: Research REST API
- 2. Scenario 2: Research Python Library
- 3. Scenario 3: Research Cloud Service API
- 4. Scenario 4: Research GraphQL API

### Collaboration Patterns
For interaction with other agents, see [collaboration-patterns.md](collaboration-patterns.md):
- 1. Integration with Orchestrator
- 2. Handling Blockers
- 3. Handoff Protocol
- 4. Collaboration with Other Agents
- 5. Best Practices

## Research Output Files

| File | Template | Purpose |
|------|----------|---------|
| `<library>-api-overview.md` | [output-templates.md](output-templates.md) | High-level API description |
| `<library>-authentication.md` | [output-templates.md](output-templates.md) | Auth setup and security |
| `<library>-endpoints.md` | [output-templates.md](output-templates.md) | Endpoint reference |
| `<library>-integration.md` | [output-templates.md](output-templates.md) | Integration guide |
| `<library>-config-template.md` | [output-templates.md](output-templates.md) | Configuration options |

## Research Workflow

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Understand Requirements | Library name, scope, context clear |
| 2 | Gather Information | Official docs, auth, endpoints, rate limits found |
| 3 | Document Findings | All 5 document types created |
| 4 | Report to Orchestrator | Minimal report with file list sent |

## Communication Formats

| Situation | Format |
|-----------|--------|
| Start | `[RESEARCH STARTED] <library> API - <scope>` |
| Progress | `[PROGRESS] <library> API - Phase: <phase>` |
| Blocked | `[BLOCKED] <library> API - Issue: <issue>` |
| Complete | `[DONE] <library> API research complete` |

## Extended Examples

### Example: Research a Python Library

```
Orchestrator: Research the requests library for HTTP calls
Agent: [RESEARCH STARTED] requests library - HTTP client scope

1. Read PyPI page and official docs
2. Document installation and basic usage
3. List key methods (get, post, put, delete)
4. Create integration examples

[DONE] requests library research complete
```
