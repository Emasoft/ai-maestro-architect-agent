---
procedure: support-skill
workflow-instruction: support
---

# Operation: Research GraphQL API


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Acknowledge Assignment](#step-1-acknowledge-assignment)
  - [Step 2: Locate Documentation Sources](#step-2-locate-documentation-sources)
  - [Step 3: Gather Core Information](#step-3-gather-core-information)
  - [Step 4: Document Authentication](#step-4-document-authentication)
  - [Step 5: Explore Schema via Introspection](#step-5-explore-schema-via-introspection)
  - [Step 6: Create Output Documents](#step-6-create-output-documents)
  - [Step 7: Report Completion](#step-7-report-completion)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example](#example)
- [Error Handling](#error-handling)

## Purpose

Research and document a GraphQL API, producing comprehensive documentation covering schema, queries, mutations, subscriptions, and integration patterns.

## When to Use

- Assigned to research a GraphQL API for integration
- Need to understand GraphQL schema before implementation
- Creating GraphQL API documentation for team reference

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| API name | Orchestrator assignment | Yes |
| Scope | Orchestrator assignment | Yes |
| GraphQL endpoint | Research or orchestrator | Yes |

## Procedure

### Step 1: Acknowledge Assignment

Format: `[RESEARCH STARTED] <api-name> GraphQL API - <scope>`

### Step 2: Locate Documentation Sources

Search order:
1. Official API documentation
2. GraphQL playground/explorer (introspection)
3. GitHub repository (if open source)
4. Schema documentation (if available)

### Step 3: Gather Core Information

Collect:
- GraphQL endpoint URL
- Authentication method
- Available queries
- Available mutations
- Available subscriptions (if any)
- Custom scalar types
- Rate limits

### Step 4: Document Authentication

Verify:
- [ ] Auth method identified (Bearer token, API key, etc.)
- [ ] Header format documented
- [ ] Token refresh mechanism (if applicable)
- [ ] Permission/scope requirements noted

### Step 5: Explore Schema via Introspection

Run introspection query:
```graphql
{
  __schema {
    types { name kind }
    queryType { fields { name } }
    mutationType { fields { name } }
  }
}
```

Document:
- Types and their fields
- Query operations
- Mutation operations
- Input types
- Enum types

### Step 6: Create Output Documents

Create all 5 documents:
1. `<api-name>-api-overview.md` - API overview, schema summary
2. `<api-name>-authentication.md` - Auth setup for GraphQL
3. `<api-name>-endpoints.md` - Queries, mutations, subscriptions
4. `<api-name>-integration.md` - Client setup, query patterns
5. `<api-name>-config-template.md` - Configuration, environment

### Step 7: Report Completion

Format: `[DONE] <api-name> GraphQL API research complete`

## Output

| File | Content |
|------|---------|
| `<api-name>-api-overview.md` | Schema overview, type system |
| `<api-name>-authentication.md` | Auth configuration |
| `<api-name>-endpoints.md` | Query/mutation/subscription reference |
| `<api-name>-integration.md` | Client libraries, example queries |
| `<api-name>-config-template.md` | Endpoint configuration |

## Verification Checklist

- [ ] GraphQL endpoint URL confirmed
- [ ] Introspection performed (if enabled)
- [ ] Authentication documented
- [ ] Key queries and mutations documented
- [ ] All 5 output documents created
- [ ] Completion reported to orchestrator

## Example

```
Orchestrator: Research the GitHub GraphQL API for repository data
Agent: [RESEARCH STARTED] GitHub GraphQL API - repository data scope

1. Endpoint: https://api.github.com/graphql
2. Auth: Bearer token (personal access token)
3. Introspection: schema explored
4. Key queries: repository, viewer, organization
5. Created 5 documentation files

[DONE] GitHub GraphQL API research complete
```

## Error Handling

| Error | Solution |
|-------|----------|
| Introspection disabled | Use official schema docs |
| Complex nested types | Document incrementally by use case |
| Missing documentation | Document from playground exploration |
