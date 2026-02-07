---
procedure: support-skill
workflow-instruction: support
---

# Operation: Write API Contract Document

## Purpose

Write a comprehensive API contract document that defines endpoint specifications, request/response schemas, authentication, and versioning for internal or external APIs.

## When to Use

- Designing a new API before implementation
- Documenting an existing API
- Defining contract between services

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| API name | Assignment | Yes |
| API purpose | Design or analysis | Yes |
| Endpoints | Design or existing code | Yes |

## Procedure

### Step 1: Gather API Information

Collect:
- API purpose and scope
- Base URL and versioning scheme
- Authentication requirements
- Available endpoints
- Request/response schemas
- Error response formats

### Step 2: Create API Contract Document

Use this template:

```markdown
# <API-Name> API Contract

**Version:** 1.0.0
**Status:** Draft | Review | Approved | Deprecated
**Last Updated:** YYYY-MM-DD

---

## Overview

### Purpose

<Description of what this API provides and who uses it>

### Base URL

| Environment | URL |
|-------------|-----|
| Production | `https://api.example.com/v1` |
| Staging | `https://api.staging.example.com/v1` |

### Versioning

This API uses URL path versioning. Breaking changes increment the major version.

---

## Authentication

### Method

<Bearer Token | API Key | OAuth 2.0>

### Header Format

```
Authorization: Bearer <token>
```

### Required Scopes

| Scope | Description |
|-------|-------------|
| `read:resources` | Read access to resources |
| `write:resources` | Write access to resources |

---

## Endpoints

### Resource: <Resource-Name>

#### List Resources

**Endpoint:** `GET /resources`

**Description:** Retrieves a paginated list of resources.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max items (default: 20, max: 100) |
| `offset` | integer | No | Items to skip (default: 0) |
| `filter` | string | No | Filter expression |

**Request Example:**

```bash
curl -X GET "https://api.example.com/v1/resources?limit=10" \
  -H "Authorization: Bearer TOKEN"
```

**Response Schema:**

```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "created_at": "ISO8601 datetime",
      "updated_at": "ISO8601 datetime"
    }
  ],
  "meta": {
    "total": "integer",
    "limit": "integer",
    "offset": "integer"
  }
}
```

**Response Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 500 | Internal Server Error |

---

#### Get Resource

**Endpoint:** `GET /resources/{id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Resource identifier |

**Response Schema:**

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "ISO8601 datetime",
  "updated_at": "ISO8601 datetime"
}
```

---

#### Create Resource

**Endpoint:** `POST /resources`

**Request Body:**

```json
{
  "name": "string (required)",
  "description": "string (optional)"
}
```

**Response:** Returns created resource with status 201.

---

#### Update Resource

**Endpoint:** `PUT /resources/{id}`

**Request Body:**

```json
{
  "name": "string",
  "description": "string"
}
```

**Response:** Returns updated resource with status 200.

---

#### Delete Resource

**Endpoint:** `DELETE /resources/{id}`

**Response:** Empty body with status 204.

---

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": {
      "field": "Additional context"
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Malformed request body |
| `UNAUTHORIZED` | 401 | Invalid or missing credentials |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Rate Limiting

| Tier | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 60 | 1,000 |
| Pro | 600 | 50,000 |
| Enterprise | 6,000 | Unlimited |

Rate limit headers:
- `X-RateLimit-Limit`: Max requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Unix timestamp of reset

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |
```

### Step 3: Apply Quality Check (6 C's)

- [ ] **Complete**: All endpoints documented
- [ ] **Correct**: Schemas match implementation
- [ ] **Clear**: Unambiguous parameter descriptions
- [ ] **Consistent**: Same formats throughout
- [ ] **Current**: Reflects current API version
- [ ] **Connected**: Links to related docs

### Step 4: Save Document

Save to: `/docs/api-contracts/<api-name>.md`

## Output

| File | Location |
|------|----------|
| API contract | `/docs/api-contracts/<api-name>.md` |

## Verification Checklist

- [ ] Base URL documented
- [ ] Authentication explained
- [ ] All endpoints documented
- [ ] Request/response schemas complete
- [ ] Error formats defined
- [ ] Rate limits documented
- [ ] 6 C's quality check passed

## Error Handling

| Error | Solution |
|-------|----------|
| Schema incomplete | Review implementation or OpenAPI spec |
| Versioning unclear | Consult with API owner |
| Missing error codes | Review error handling in code |
