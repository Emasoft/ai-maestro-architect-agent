---
name: eaa-api-researcher
description: Use when investigating external APIs, libraries, and services. Creates standardized API documentation with auth and endpoints. Trigger with API research or library investigation requests.
version: 1.0.0
license: Apache-2.0
compatibility: Requires web access for documentation lookup. Works with REST APIs, GraphQL APIs, Python libraries, npm packages, and cloud service APIs. Requires AI Maestro installed.
metadata:
  author: Emasoft
  triggers: "User asks to research an API or library, Need to understand authentication for external service, Orchestrator needs API documentation before implementation, Integration with third-party service required"
context: fork
workflow-instruction: "Step 7"
procedure: "proc-create-design"
---

# API Researcher Skill

## Overview

Comprehensive API research and documentation skill for the API Researcher Agent. This skill provides structured workflows for investigating external APIs, libraries, and services, producing standardized documentation that includes overviews, authentication guides, endpoint references, and integration instructions.

## Prerequisites

- Web access for documentation lookup
- Write access to documentation output directories
- Familiarity with REST APIs, GraphQL APIs, Python libraries, npm packages, or cloud service APIs

## Instructions

1. Receive research assignment from orchestrator with library name and scope
2. Gather information from official documentation sources
3. Create all five standard document types using templates
4. Report completion with minimal report format

### Checklist

Copy this checklist and track your progress:

- [ ] Receive research assignment with library name and scope
- [ ] Acknowledge assignment in format: `[RESEARCH STARTED] <library> API - <scope>`
- [ ] Consult official documentation sources (in order: official docs, GitHub repo, API explorer)
- [ ] Verify information: auth method, endpoints, rate limits, error codes
- [ ] Create API Overview Document
- [ ] Create Authentication Guide
- [ ] Create Endpoints Reference
- [ ] Create Integration Guide
- [ ] Create Configuration Template
- [ ] Report completion: `[DONE] <library> API research complete`

## Output

| Output Type | Description |
|-------------|-------------|
| API Overview Document | High-level API description with key features and capabilities |
| Authentication Guide | Auth setup, security requirements, and credential management |
| Endpoints Reference | Comprehensive endpoint documentation with parameters and examples |
| Integration Guide | Step-by-step integration instructions with code samples |
| Configuration Template | Configuration options and environment setup |

---

## Table of Contents

### Research Procedures
For the step-by-step research workflow, see [research-procedure.md](references/research-procedure.md):
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
For all documentation templates, see [output-templates.md](references/output-templates.md):
- 1. API Overview Document Template
- 2. Authentication Guide Template
- 3. Endpoints Reference Template
- 4. Integration Guide Template
- 5. Configuration Template

### Tools Reference
For available tools and usage, see [tools-reference.md](references/tools-reference.md):
- 1. Read Tool - for local files
- 2. WebFetch Tool - for online documentation
- 3. WebSearch Tool - for finding resources
- 4. Write Tool - for documentation output
- 5. Glob/Grep Tools - for finding existing code

### Research Scenarios
For common research patterns, see [research-scenarios.md](references/research-scenarios.md):
- 1. Scenario 1: Research REST API
- 2. Scenario 2: Research Python Library
- 3. Scenario 3: Research Cloud Service API
- 4. Scenario 4: Research GraphQL API

### Collaboration Patterns
For interaction with other agents, see [collaboration-patterns.md](references/collaboration-patterns.md):
- 1. Integration with Orchestrator
  - 1.1 Receiving Tasks
  - 1.2 Reporting Progress
  - 1.3 Delivering Results
- 2. Handling Blockers
  - 2.1 Documentation Not Found
  - 2.2 API Deprecated
  - 2.3 Multiple Versions
- 3. Handoff Protocol
  - 3.1 Handoff Report Format
  - 3.2 Return to Orchestrator
- 4. Collaboration with Other Agents
  - 4.1 With Code-Writer Agent
  - 4.2 With Documentation-Writer Agent
  - 4.3 With Requirements-Analyst Agent
- 5. Best Practices

---

## Quick Reference

### Research Output Files

| File | Template | Purpose |
|------|----------|---------|
| `<library>-api-overview.md` | [output-templates.md](references/output-templates.md) | High-level API description |
| `<library>-authentication.md` | [output-templates.md](references/output-templates.md) | Auth setup and security |
| `<library>-endpoints.md` | [output-templates.md](references/output-templates.md) | Endpoint reference |
| `<library>-integration.md` | [output-templates.md](references/output-templates.md) | Integration guide |
| `<library>-config-template.md` | [output-templates.md](references/output-templates.md) | Configuration options |

### Research Workflow

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Understand Requirements | Library name, scope, context clear |
| 2 | Gather Information | Official docs, auth, endpoints, rate limits found |
| 3 | Document Findings | All 5 document types created |
| 4 | Report to Orchestrator | Minimal report with file list sent |

### Communication Formats

| Situation | Format |
|-----------|--------|
| Start | `[RESEARCH STARTED] <library> API - <scope>` |
| Progress | `[PROGRESS] <library> API - Phase: <phase>` |
| Blocked | `[BLOCKED] <library> API - Issue: <issue>` |
| Complete | `[DONE] <library> API research complete` |

## Examples

### Example 1: Research a REST API

```
Orchestrator: Research the Stripe API for payment processing
Agent: [RESEARCH STARTED] Stripe API - payment processing scope

1. Consult official docs at https://stripe.com/docs/api
2. Document authentication (API keys, webhooks)
3. List key endpoints (charges, customers, subscriptions)
4. Create integration guide with code samples

Output files:
- stripe-api-overview.md
- stripe-authentication.md
- stripe-endpoints.md
- stripe-integration.md
- stripe-config-template.md

[DONE] Stripe API research complete
```

### Example 2: Research a Python Library

```
Orchestrator: Research the requests library for HTTP calls
Agent: [RESEARCH STARTED] requests library - HTTP client scope

1. Read PyPI page and official docs
2. Document installation and basic usage
3. List key methods (get, post, put, delete)
4. Create integration examples

[DONE] requests library research complete
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Documentation not found | API has no public docs | Report blocker to orchestrator, suggest alternatives |
| API deprecated | Service is sunset | Document deprecation, find replacement API |
| Multiple versions | API has breaking changes | Document both versions, recommend latest |
| Rate limit hit | Too many doc requests | Wait and retry, use cached versions |
| Authentication unclear | Docs incomplete | Experiment with API, document findings |

## Resources

- [research-procedure.md](references/research-procedure.md) - Step-by-step research workflow
- [output-templates.md](references/output-templates.md) - All documentation templates
- [tools-reference.md](references/tools-reference.md) - Available tools and usage
- [research-scenarios.md](references/research-scenarios.md) - Common research patterns
- [collaboration-patterns.md](references/collaboration-patterns.md) - Agent interaction patterns
