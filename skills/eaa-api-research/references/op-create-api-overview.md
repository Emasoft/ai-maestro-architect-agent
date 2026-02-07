---
procedure: support-skill
workflow-instruction: support
---

# Operation: Create API Overview Document

## Purpose

Create a high-level API overview document that describes the API's purpose, key features, capabilities, and when to use it.

## When to Use

- Starting API research documentation
- Creating reference documentation for a new API
- Providing team overview of API capabilities

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| API name | Research data | Yes |
| API purpose | Research findings | Yes |
| Key features | Research findings | Yes |
| Official docs URL | Research | Yes |

## Procedure

### Step 1: Gather Overview Information

From research, collect:
- API name and provider
- Primary purpose/problem it solves
- Key features (5-10 main capabilities)
- Target use cases
- Limitations and constraints
- Pricing model (if applicable)

### Step 2: Write Overview Document

Use this template:

```markdown
# <API-Name> API Overview

## What is <API-Name>?

<1-2 paragraph description of what the API does and who provides it>

## Key Features

| Feature | Description |
|---------|-------------|
| <feature-1> | <what it enables> |
| <feature-2> | <what it enables> |
| ... | ... |

## Use Cases

- **<use-case-1>**: <brief description>
- **<use-case-2>**: <brief description>
- **<use-case-3>**: <brief description>

## Quick Facts

| Property | Value |
|----------|-------|
| Type | <REST/GraphQL/SOAP/etc.> |
| Base URL | <base-url> |
| Auth Method | <auth-type> |
| Rate Limit | <limit> |
| Pricing | <pricing-model> |

## When to Use

Use this API when:
- <scenario-1>
- <scenario-2>

Do NOT use this API when:
- <anti-scenario-1>
- <anti-scenario-2>

## Related Documents

- [Authentication Guide](<api-name>-authentication.md)
- [Endpoints Reference](<api-name>-endpoints.md)
- [Integration Guide](<api-name>-integration.md)
- [Configuration Template](<api-name>-config-template.md)

## Official Resources

- [Official Documentation](<url>)
- [API Reference](<url>)
- [Status Page](<url>)
```

### Step 3: Save Document

Save to: `<output-dir>/<api-name>-api-overview.md`

## Output

| File | Content |
|------|---------|
| `<api-name>-api-overview.md` | High-level API description |

## Verification Checklist

- [ ] API purpose clearly stated
- [ ] Key features listed (5-10)
- [ ] Use cases documented
- [ ] Quick facts table complete
- [ ] When to use/not use guidance provided
- [ ] Links to related documents added
- [ ] Official resource links included

## Example

```markdown
# Stripe API Overview

## What is Stripe?

Stripe is a payment processing API that enables businesses to accept
payments online. It provides a complete payment infrastructure including
card processing, subscriptions, invoicing, and fraud prevention.

## Key Features

| Feature | Description |
|---------|-------------|
| Card Payments | Process credit/debit card payments |
| Subscriptions | Manage recurring billing |
| Invoicing | Create and send invoices |
| Fraud Protection | ML-based fraud detection |
| Multi-currency | Support 135+ currencies |
```
