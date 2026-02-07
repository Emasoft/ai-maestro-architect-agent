---
procedure: support-skill
workflow-instruction: support
---

# Operation: Create Endpoints Reference

## Purpose

Create a comprehensive endpoints reference document that documents all API endpoints with methods, parameters, request/response formats, and examples.

## When to Use

- Documenting API endpoint details
- Creating implementation reference
- Providing complete API operation catalog

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Endpoint list | Research findings | Yes |
| Request schemas | Research findings | Yes |
| Response schemas | Research findings | Yes |
| Error codes | Research findings | Yes |

## Procedure

### Step 1: Organize Endpoints by Resource

Group endpoints by logical resource:
- Users: /users, /users/{id}
- Products: /products, /products/{id}
- Orders: /orders, /orders/{id}

### Step 2: Write Endpoints Reference

Use this template:

```markdown
# <API-Name> Endpoints Reference

## Base URL

```
https://api.example.com/v1
```

## Authentication

All endpoints require authentication. See [Authentication Guide](<api>-authentication.md).

---

## <Resource-1>

### List <Resource-1>

Retrieves a list of <resource-1> items.

**Endpoint**: `GET /<resource-1>`

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max items to return (default: 20) |
| `offset` | integer | No | Number of items to skip |
| `filter` | string | No | Filter criteria |

**Request Example**:

```bash
curl -X GET "https://api.example.com/v1/<resource-1>?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response Example**:

```json
{
  "data": [
    {
      "id": "abc123",
      "name": "Example Item",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "total": 100,
    "limit": 10,
    "offset": 0
  }
}
```

**Response Codes**:

| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 500 | Server error |

---

### Get <Resource-1> by ID

Retrieves a single <resource-1> by its ID.

**Endpoint**: `GET /<resource-1>/{id}`

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | The <resource-1> ID |

**Request Example**:

```bash
curl -X GET "https://api.example.com/v1/<resource-1>/abc123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response Example**:

```json
{
  "id": "abc123",
  "name": "Example Item",
  "description": "Detailed description",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T08:00:00Z"
}
```

---

### Create <Resource-1>

Creates a new <resource-1>.

**Endpoint**: `POST /<resource-1>`

**Request Body**:

```json
{
  "name": "New Item",
  "description": "Item description"
}
```

**Request Body Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Item name |
| `description` | string | No | Item description |

**Response**: Returns the created item with status 201.

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Malformed request |
| `UNAUTHORIZED` | 401 | Invalid credentials |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMITED` | 429 | Too many requests |
| `SERVER_ERROR` | 500 | Internal error |
```

### Step 3: Save Document

Save to: `<output-dir>/<api-name>-endpoints.md`

## Output

| File | Content |
|------|---------|
| `<api-name>-endpoints.md` | Complete endpoint reference |

## Verification Checklist

- [ ] All endpoints documented
- [ ] Methods (GET, POST, PUT, DELETE) specified
- [ ] Parameters documented with types
- [ ] Request examples provided
- [ ] Response examples provided
- [ ] Error codes documented
- [ ] Rate limits noted (if applicable)
