# Research Scenarios

Common API research scenarios and step-by-step approaches.

---

## Table of Contents

- 1. Scenario 1: Research REST API
- 2. Scenario 2: Research Python Library
- 3. Scenario 3: Research Cloud Service API
- 4. Scenario 4: Research GraphQL API

---

## 1. Scenario 1: Research REST API

### When to Use

- Researching any REST-based web API
- Standard HTTP endpoints with JSON/XML responses
- Public or authenticated APIs

### Step-by-Step

| Step | Action | Tool |
|------|--------|------|
| 1 | WebSearch for official documentation | WebSearch |
| 2 | WebFetch the API reference page | WebFetch |
| 3 | Document all endpoints with parameters | Write |
| 4 | Identify authentication method | WebFetch |
| 5 | Check for rate limits | WebFetch |
| 6 | Create integration guide | Write |
| 7 | Provide configuration template | Write |

### Key Information to Gather

- Base URL and versioning scheme
- Authentication method (API key, OAuth, JWT)
- All endpoint paths and HTTP methods
- Request/response formats
- Rate limits and quotas
- Error codes and meanings

---

## 2. Scenario 2: Research Python Library

### When to Use

- Researching Python packages from PyPI
- SDK libraries for services
- Utility libraries

### Step-by-Step

| Step | Action | Tool |
|------|--------|------|
| 1 | WebFetch PyPI page for library | WebFetch |
| 2 | Read official documentation | WebFetch |
| 3 | Check GitHub for examples | WebSearch, WebFetch |
| 4 | Document main classes and methods | Write |
| 5 | Identify dependencies | WebFetch |
| 6 | Create usage guide | Write |
| 7 | Note version compatibility | WebFetch |

### Key Information to Gather

- Package name and installation command
- Python version compatibility
- Dependencies
- Main classes and methods
- Configuration options
- Common usage patterns

---

## 3. Scenario 3: Research Cloud Service API

### When to Use

- AWS, GCP, Azure services
- Other cloud provider APIs
- Managed service APIs

### Step-by-Step

| Step | Action | Tool |
|------|--------|------|
| 1 | WebFetch cloud provider documentation | WebFetch |
| 2 | Document service endpoints | Write |
| 3 | Identify authentication (IAM, API keys, etc.) | WebFetch |
| 4 | Note pricing/quotas | WebFetch |
| 5 | Document SDKs available | WebSearch |
| 6 | Create service-specific integration guide | Write |
| 7 | Provide infrastructure-as-code templates (reference only) | Write |

### Key Information to Gather

| Category | Details |
|----------|---------|
| Authentication | IAM roles, service accounts, API keys |
| Endpoints | Regional endpoints, global endpoints |
| Pricing | Free tier limits, per-request costs |
| SDKs | Official SDKs for each language |
| Quotas | Service limits, rate limits |
| IaC | Terraform/CloudFormation references |

---

## 4. Scenario 4: Research GraphQL API

### When to Use

- GraphQL-based APIs
- APIs with complex query capabilities
- Schema-driven APIs

### Step-by-Step

| Step | Action | Tool |
|------|--------|------|
| 1 | WebFetch GraphQL schema/documentation | WebFetch |
| 2 | Document queries and mutations | Write |
| 3 | Identify authentication method | WebFetch |
| 4 | Note schema structure | Write |
| 5 | Document variables and types | Write |
| 6 | Create query examples (non-executable) | Write |
| 7 | Provide integration patterns | Write |

### Key Information to Gather

- Schema types and relationships
- Available queries
- Available mutations
- Input types and validation
- Authentication headers
- Rate limiting/complexity limits
- Introspection availability

### GraphQL-Specific Documentation

```markdown
## Types
<List all relevant types with fields>

## Queries
<List all queries with parameters>

## Mutations
<List all mutations with parameters>

## Subscriptions (if available)
<List real-time subscription options>
```
