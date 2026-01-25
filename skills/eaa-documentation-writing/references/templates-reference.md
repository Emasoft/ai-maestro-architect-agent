# Document Templates Reference

Templates for module specifications, API contracts, and architecture decision records.

---

## Table of Contents

- 1. Module Specification Template
- 2. API Contract Template
- 3. Architecture Decision Record (ADR) Template
- 4. Input Format Examples

---

## 1. Module Specification Template

```markdown
# Module Name: [Module Name]

## Purpose
[One-sentence description of what this module does]

## Responsibilities
- [Responsibility 1]
- [Responsibility 2]

## Public Interface
### Functions
#### `functionName(param1, param2) -> ReturnType`
**Purpose**: [What this function does]
**Parameters**:
- `param1` (Type): [Description]
- `param2` (Type): [Description]
**Returns**: [Description of return value]
**Errors**: [List of possible errors]
**Example**:
```language
[Code example showing usage]
```

## Dependencies
- [Dependency 1]: [Why needed]

## Configuration
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| VAR_NAME | string | "default" | [Purpose] |

## Error Handling
- [Error scenario 1]: [How to handle]

## Testing Strategy
- [Test type 1]: [What to test]

## Performance Considerations
- [Consideration 1]: [Impact and mitigation]
```

---

## 2. API Contract Template

```markdown
# API Endpoint: [Method] /path/to/resource

## Description
[What this endpoint does]

## Authentication
**Required**: [Yes/No]
**Type**: [Bearer token / API key / etc.]

## Request
### Headers
- `Content-Type`: application/json
- `Authorization`: Bearer {token}

### Path Parameters
- `{id}` (UUID): [Description]

### Query Parameters
- `filter` (string, optional): [Description]

### Request Body
```json
{
  "field1": "string",
  "field2": 123
}
```

**Schema**:
- `field1` (string, required): [Description]
- `field2` (integer, optional): [Description]

## Response
### Success (200 OK)
```json
{
  "status": "success",
  "data": { }
}
```

### Error Responses
**400 Bad Request**: Invalid input
**401 Unauthorized**: Missing or invalid token
**404 Not Found**: Resource not found
**500 Internal Server Error**: Server error

## Rate Limiting
- **Limit**: 100 requests per minute
- **Headers**: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Examples
[Full request/response examples]
```

---

## 3. Architecture Decision Record (ADR) Template

```markdown
# ADR-001: [Decision Title]

**Date**: YYYY-MM-DD
**Status**: [Proposed / Accepted / Deprecated / Superseded]
**Deciders**: [Names/Roles]

## Context
[What is the issue we're facing?]

## Decision
[What decision did we make?]

## Rationale
[Why did we choose this option?]

## Consequences
### Positive
- [Benefit 1]

### Negative
- [Trade-off 1]

### Neutral
- [Impact 1]

## Alternatives Considered
### Option 1: [Name]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Rejected because**: [Reason]

## Implementation Notes
[Specific guidance for implementation]

## References
- [Link to related documents]
```

---

## 4. Input Format Examples

### Requirement Document Input

```markdown
**Feature**: User authentication system
**Scope**: Login, logout, session management
**Constraints**: Must use JWT, 15-minute session timeout
**Success Criteria**: 99.9% uptime, <200ms response time
```

### Orchestrator Prompt Input

```
Task: Document the API contract for the user authentication module
Context: RESTful API, JWT-based auth, PostgreSQL backend
Requirements: Include error codes, rate limiting, security headers
Output: API specification in OpenAPI 3.0 format (markdown)
```

### Decision Record Input

```
Decision: Use Redis for session storage
Rationale: Sub-millisecond latency, horizontal scaling support
Alternatives Considered: PostgreSQL sessions (slower), in-memory (no persistence)
Impact: Adds Redis as runtime dependency
```
