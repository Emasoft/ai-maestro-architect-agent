# Quick Reference

## Table of Contents

- Research Output Files
- Research Workflow
- Communication Formats
- Extended Examples

## Research Output Files

| File | Template | Purpose |
|------|----------|---------|
| `<library>-api-overview.md` | output-templates | High-level API description |
| `<library>-authentication.md` | output-templates | Auth setup and security |
| `<library>-endpoints.md` | output-templates | Endpoint reference |
| `<library>-integration.md` | output-templates | Integration guide |
| `<library>-config-template.md` | output-templates | Configuration options |

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
