---
procedure: support-skill
workflow-instruction: support
---

# Operation: Create Authentication Guide

## Purpose

Create a comprehensive authentication guide that documents how to authenticate with the API, including credential setup, token management, and security best practices.

## When to Use

- Documenting API authentication requirements
- Setting up secure API access
- Providing auth guidance for implementation teams

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Auth method | Research findings | Yes |
| Credential type | Research findings | Yes |
| Token format | Research findings | If token-based |
| Required scopes | Research findings | If OAuth |

## Procedure

### Step 1: Identify Authentication Type

Common types:
- API Key (header or query parameter)
- Bearer Token (JWT)
- OAuth 2.0 (various flows)
- Basic Auth (username/password)
- Certificate-based

### Step 2: Write Authentication Guide

Use this template:

```markdown
# <API-Name> Authentication Guide

## Authentication Method

<API-Name> uses **<auth-type>** authentication.

## Getting Credentials

### Step 1: Create Account

1. Go to <developer-portal-url>
2. Create an account or sign in
3. Navigate to API credentials section

### Step 2: Generate Credentials

1. Click "Create new API key" (or similar)
2. Select appropriate permissions/scopes
3. Copy and securely store the credentials

**Security Warning**: Never commit credentials to version control.

## Using Credentials

### Request Format

```bash
curl -X GET "https://api.example.com/endpoint" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Header Details

| Header | Value |
|--------|-------|
| `Authorization` | `Bearer <token>` |
| `Content-Type` | `application/json` |

## Token Management

### Token Expiration

<If applicable, describe token lifetime and refresh>

### Refresh Flow

<If applicable, describe how to refresh tokens>

```python
# Example refresh code
def refresh_token(refresh_token):
    response = requests.post(
        "https://api.example.com/oauth/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )
    return response.json()["access_token"]
```

## Security Best Practices

1. **Store credentials securely**: Use environment variables or secret managers
2. **Rotate credentials regularly**: Update keys periodically
3. **Use minimum permissions**: Request only needed scopes
4. **Never expose in client code**: Keep credentials server-side
5. **Monitor usage**: Watch for unauthorized access

## Environment Setup

### Development

```bash
export API_KEY="your-development-key"
```

### Production

Use a secret manager (AWS Secrets Manager, HashiCorp Vault, etc.)

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or missing credentials | Verify API key is correct |
| 403 Forbidden | Insufficient permissions | Check required scopes |
| Token expired | JWT past expiration | Refresh the token |
```

### Step 3: Save Document

Save to: `<output-dir>/<api-name>-authentication.md`

## Output

| File | Content |
|------|---------|
| `<api-name>-authentication.md` | Complete auth setup guide |

## Verification Checklist

- [ ] Auth type clearly identified
- [ ] Credential creation steps documented
- [ ] Request format with examples provided
- [ ] Token lifecycle documented (if applicable)
- [ ] Security best practices included
- [ ] Environment setup examples provided
- [ ] Troubleshooting section included

## Example

```markdown
# Stripe Authentication Guide

## Authentication Method

Stripe uses **API Key** authentication with secret keys.

## Getting Credentials

1. Sign in to Stripe Dashboard
2. Navigate to Developers > API keys
3. Copy your secret key (starts with sk_)

## Using Credentials

```bash
curl https://api.stripe.com/v1/charges \
  -u sk_test_YOUR_SECRET_KEY:
```
```
