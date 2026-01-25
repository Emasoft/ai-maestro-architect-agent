# Output Templates

Templates for API research documentation deliverables.

---

## Table of Contents

- 1. API Overview Document
- 2. Authentication Guide
- 3. Endpoints Reference
- 4. Integration Guide
- 5. Configuration Template

---

## 1. API Overview Document

**Filename**: `docs_dev/<library>-api-overview.md`

```markdown
# <Library/Service> API Overview

## Description
<What this API does>

## Official Resources
- Documentation: <URL>
- API Reference: <URL>
- GitHub: <URL>
- Version researched: <version>

## Capabilities
<What can be done with this API>

## Limitations
- Rate limits: <details>
- Quotas: <details>
- Restrictions: <details>

## Authentication Required
<Type: API key, OAuth, JWT, etc.>

## Pricing/Costs
<Free tier, paid tiers, rate limits>

## Recommended For
<Use cases where this API excels>

## Not Recommended For
<Use cases where alternatives are better>
```

---

## 2. Authentication Guide

**Filename**: `docs_dev/<library>-authentication.md`

```markdown
# <Library/Service> Authentication Guide

## Authentication Method
<API Key | OAuth 2.0 | JWT | Basic Auth | etc.>

## Step-by-Step Setup

### 1. Obtain Credentials
<How to get API key/credentials>

### 2. Configuration
<Where to store credentials (env vars, config files)>

### 3. Authentication Flow
<Detailed steps for authenticating>

### 4. Token Refresh (if applicable)
<How to handle token expiration>

## Security Best Practices
- Never hardcode credentials
- Use environment variables
- Rotate keys regularly
- Monitor for leaks

## Example Configuration
\`\`\`json
{
  "api_key": "YOUR_API_KEY_HERE",
  "api_secret": "YOUR_SECRET_HERE"
}
\`\`\`

## Common Authentication Errors
<List common errors and solutions>
```

---

## 3. Endpoints Reference

**Filename**: `docs_dev/<library>-endpoints.md`

```markdown
# <Library/Service> Endpoints Reference

## Base URL
`https://api.example.com/v1`

## Endpoints

### GET /resource
**Purpose:** <What this endpoint does>

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | <description> |
| param2 | integer | No | <description> |

**Response:**
\`\`\`json
{
  "status": "success",
  "data": {
    "id": 123,
    "name": "example"
  }
}
\`\`\`

**Error Codes:**
- 400: Bad Request - <when this occurs>
- 401: Unauthorized - <when this occurs>
- 429: Rate Limited - <when this occurs>

**Rate Limit:** <requests per minute/hour>

---

### POST /resource
<Same structure as above>

---

## Common Request Headers
\`\`\`
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
Accept: application/json
\`\`\`

## Pagination
<How pagination works if applicable>

## Filtering/Sorting
<How to filter or sort results if applicable>
```

---

## 4. Integration Guide

**Filename**: `docs_dev/<library>-integration.md`

```markdown
# <Library/Service> Integration Guide

## Overview
<High-level integration strategy>

## Prerequisites
- <Dependency 1>
- <Dependency 2>
- Account/credentials required

## Integration Steps

### Step 1: Install Dependencies
\`\`\`bash
# Dependencies needed (DO NOT EXECUTE - for reference only)
pip install <package>
\`\`\`

### Step 2: Configuration
<What configuration files need to be created>

### Step 3: Initialize Client
<Pseudocode or description of initialization>

### Step 4: Make Requests
<Patterns for making API requests>

### Step 5: Handle Responses
<How to parse and use responses>

### Step 6: Error Handling
<Recommended error handling patterns>

## Common Integration Patterns

### Pattern 1: <Pattern Name>
<When to use this pattern>
<Pseudocode/description>

### Pattern 2: <Pattern Name>
<When to use this pattern>
<Pseudocode/description>

## Best Practices
1. <Practice 1>
2. <Practice 2>
3. <Practice 3>

## Troubleshooting
<Common issues and solutions>

## Next Steps
<What to do after integration is complete>
```

---

## 5. Configuration Template

**Filename**: `docs_dev/<library>-config-template.md`

```markdown
# <Library/Service> Configuration Template

## Environment Variables

\`\`\`bash
# Required
LIBRARY_API_KEY=your_api_key_here
LIBRARY_API_SECRET=your_secret_here

# Optional
LIBRARY_BASE_URL=https://api.example.com/v1
LIBRARY_TIMEOUT=30
LIBRARY_RETRY_ATTEMPTS=3
\`\`\`

## Configuration File

\`\`\`json
{
  "api": {
    "base_url": "https://api.example.com/v1",
    "timeout": 30,
    "retry": {
      "attempts": 3,
      "backoff": "exponential"
    }
  },
  "authentication": {
    "type": "api_key",
    "key_location": "env:LIBRARY_API_KEY"
  },
  "features": {
    "enable_caching": true,
    "cache_ttl": 3600
  }
}
\`\`\`

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| base_url | string | <default> | API base URL |
| timeout | integer | 30 | Request timeout in seconds |
| retry_attempts | integer | 3 | Number of retry attempts |

## Validation Checklist
- [ ] All required credentials provided
- [ ] Base URL is correct for environment
- [ ] Timeout values are reasonable
- [ ] Retry logic configured
- [ ] Error handling enabled
```
