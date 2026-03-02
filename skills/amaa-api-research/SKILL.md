---
name: amaa-api-research
description: Use when researching external APIs, libraries, and services. Creates standardized documentation with authentication, endpoints, and integration guides.
context: fork
user-invocable: false
---

# API Researcher Skill

## Overview

Structured workflow for investigating external APIs, libraries, and services. Produces standardized documentation including overviews, authentication guides, endpoint references, and integration instructions.

## Prerequisites

- Web access for documentation lookup
- Write access to documentation output directories
- Familiarity with REST, GraphQL, Python libraries, npm packages, or cloud APIs

## Instructions

1. Receive research assignment from orchestrator with library name and scope
2. Gather information from official documentation sources
3. Create all five standard document types using templates
4. Report completion with minimal report format

### Checklist

- [ ] Receive assignment with library name and scope
- [ ] Acknowledge: `[RESEARCH STARTED] <library> API - <scope>`
- [ ] Consult official docs, GitHub repo, API explorer
- [ ] Verify: auth method, endpoints, rate limits, error codes
- [ ] Create all 5 document types (see Output table)
- [ ] Report: `[DONE] <library> API research complete`

## Reference Documents

| Document | Description |
|----------|-------------|
| [research-procedure.md](references/research-procedure.md) | Step-by-step research workflow |
| [output-templates.md](references/output-templates.md) | All 5 documentation templates |
| [tools-reference.md](references/tools-reference.md) | Available tools and usage |
| [research-scenarios.md](references/research-scenarios.md) | REST, Python, Cloud, GraphQL patterns |
| [collaboration-patterns.md](references/collaboration-patterns.md) | Agent interaction and handoff protocols |
| [quick-reference.md](references/quick-reference.md) | TOC, workflow tables, communication formats |

## Examples

```
Orchestrator: Research the Stripe API for payment processing
Agent: [RESEARCH STARTED] Stripe API - payment processing scope

1. Consult official docs at https://stripe.com/docs/api
2. Document authentication (API keys, webhooks)
3. List key endpoints (charges, customers, subscriptions)
4. Create integration guide with code samples

Output: stripe-api-overview.md, stripe-authentication.md,
        stripe-endpoints.md, stripe-integration.md,
        stripe-config-template.md

[DONE] Stripe API research complete
```

## Error Handling

| Error | Solution |
|-------|----------|
| Documentation not found | Report blocker, suggest alternatives |
| API deprecated | Document deprecation, find replacement |
| Multiple versions | Document both, recommend latest |
| Rate limit hit | Wait, retry, use cached versions |

## Output

| Output Type | Description |
|-------------|-------------|
| API Overview | High-level API description with key features |
| Authentication Guide | Auth setup, security, credential management |
| Endpoints Reference | Endpoint docs with parameters and examples |
| Integration Guide | Step-by-step instructions with code samples |
| Configuration Template | Config options and environment setup |

## Resources

- [research-procedure.md](references/research-procedure.md) - Full research workflow
- [output-templates.md](references/output-templates.md) - Documentation templates
- [quick-reference.md](references/quick-reference.md) - Tables, formats, extended examples
