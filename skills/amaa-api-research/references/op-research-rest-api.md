---
procedure: support-skill
workflow-instruction: support
---

# Operation: Research REST API


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Acknowledge Assignment](#step-1-acknowledge-assignment)
  - [Step 2: Locate Official Documentation](#step-2-locate-official-documentation)
  - [Step 3: Gather Core Information](#step-3-gather-core-information)
  - [Step 4: Document Authentication](#step-4-document-authentication)
  - [Step 5: Document Endpoints](#step-5-document-endpoints)
  - [Step 6: Create Output Documents](#step-6-create-output-documents)
  - [Step 7: Report Completion](#step-7-report-completion)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example](#example)
- [Error Handling](#error-handling)

## Purpose

Research and document a REST API, producing comprehensive documentation covering overview, authentication, endpoints, integration, and configuration.

## When to Use

- Assigned to research a new REST API for integration
- Need to understand API capabilities before implementation
- Creating API documentation for team reference

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| API name | Orchestrator assignment | Yes |
| Scope | Orchestrator assignment | Yes |
| Official docs URL | Research or orchestrator | No |

## Procedure

### Step 1: Acknowledge Assignment

Format: `[RESEARCH STARTED] <api-name> API - <scope>`

### Step 2: Locate Official Documentation

Search order:
1. Official documentation site (e.g., `https://api.example.com/docs`)
2. GitHub repository documentation
3. API explorer/playground (if available)

### Step 3: Gather Core Information

Collect:
- Base URL and versioning scheme
- Authentication method (API key, OAuth, JWT, etc.)
- Rate limits and quotas
- Available endpoints grouped by resource
- Request/response formats (JSON, XML, etc.)
- Error code patterns

### Step 4: Document Authentication

Verify:
- [ ] Auth type identified (API key, OAuth2, JWT, etc.)
- [ ] Credential location documented (header, query, body)
- [ ] Token refresh mechanism (if applicable)
- [ ] Required scopes/permissions listed

### Step 5: Document Endpoints

For each endpoint:
- Method (GET, POST, PUT, DELETE, PATCH)
- Path with parameters
- Request headers required
- Request body schema
- Response schema
- Error responses
- Example request and response

### Step 6: Create Output Documents

Create all 5 documents:
1. `<api-name>-api-overview.md`
2. `<api-name>-authentication.md`
3. `<api-name>-endpoints.md`
4. `<api-name>-integration.md`
5. `<api-name>-config-template.md`

### Step 7: Report Completion

Format: `[DONE] <api-name> API research complete`

## Output

| File | Content |
|------|---------|
| `<api-name>-api-overview.md` | High-level description, key features, use cases |
| `<api-name>-authentication.md` | Auth setup, credentials, security |
| `<api-name>-endpoints.md` | Complete endpoint reference |
| `<api-name>-integration.md` | Step-by-step integration guide |
| `<api-name>-config-template.md` | Configuration options, environment variables |

## Verification Checklist

- [ ] Official documentation consulted
- [ ] Authentication method documented with examples
- [ ] All relevant endpoints documented
- [ ] Rate limits and error codes noted
- [ ] All 5 output documents created
- [ ] Completion reported to orchestrator

## Example

```
Orchestrator: Research the GitHub REST API for repository management
Agent: [RESEARCH STARTED] GitHub REST API - repository management scope

1. Consulted https://docs.github.com/en/rest
2. Auth: Personal access tokens or OAuth apps
3. Endpoints: repos/, issues/, pulls/, etc.
4. Created 5 documentation files

[DONE] GitHub REST API research complete
```

## Error Handling

| Error | Solution |
|-------|----------|
| No official docs found | Report blocker, suggest alternatives |
| Incomplete API documentation | Document what is available, note gaps |
| Deprecated endpoints | Note deprecation, document replacements |
