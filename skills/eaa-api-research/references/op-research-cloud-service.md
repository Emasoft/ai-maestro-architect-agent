---
procedure: support-skill
workflow-instruction: support
---

# Operation: Research Cloud Service API

## Purpose

Research and document a cloud service API (AWS, GCP, Azure, etc.), producing comprehensive documentation covering service overview, authentication, SDK usage, and integration patterns.

## When to Use

- Assigned to research a cloud service for integration
- Evaluating cloud service capabilities
- Creating documentation for cloud service adoption

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Service name | Orchestrator assignment | Yes |
| Cloud provider | Orchestrator or research | Yes |
| Use case scope | Orchestrator assignment | Yes |

## Procedure

### Step 1: Acknowledge Assignment

Format: `[RESEARCH STARTED] <provider> <service-name> - <scope>`

### Step 2: Locate Documentation Sources

Search order:
1. Official service documentation (AWS docs, GCP docs, Azure docs)
2. SDK documentation (boto3, google-cloud-*, azure-*)
3. API reference
4. Service-specific tutorials

### Step 3: Gather Core Information

Collect:
- Service purpose and capabilities
- Authentication methods (IAM roles, service accounts, managed identity)
- SDK packages and CLI tools
- Pricing model and free tier limits
- Regional availability
- Quotas and limits

### Step 4: Document Authentication

Verify:
- [ ] Auth method identified (IAM, service account, managed identity)
- [ ] Credential setup documented
- [ ] Required permissions/roles listed
- [ ] Local development setup noted
- [ ] Production deployment setup noted

### Step 5: Document Service Operations

For key operations:
- SDK method or API endpoint
- Required permissions
- Input parameters
- Response format
- Error handling
- Cost implications

### Step 6: Create Output Documents

Create all 5 documents:
1. `<service-name>-api-overview.md` - Service capabilities, use cases
2. `<service-name>-authentication.md` - IAM/credential setup
3. `<service-name>-endpoints.md` - API/SDK operations reference
4. `<service-name>-integration.md` - Integration patterns, code samples
5. `<service-name>-config-template.md` - Environment configuration

### Step 7: Report Completion

Format: `[DONE] <provider> <service-name> research complete`

## Output

| File | Content |
|------|---------|
| `<service-name>-api-overview.md` | Service description, features, limits |
| `<service-name>-authentication.md` | IAM/credential configuration |
| `<service-name>-endpoints.md` | API operations and SDK methods |
| `<service-name>-integration.md` | Code examples for common tasks |
| `<service-name>-config-template.md` | Environment variables, config files |

## Verification Checklist

- [ ] Official docs consulted
- [ ] Authentication documented for local and production
- [ ] Key operations documented with permissions
- [ ] Pricing and limits noted
- [ ] All 5 output documents created
- [ ] Completion reported to orchestrator

## Example

```
Orchestrator: Research AWS S3 for file storage
Agent: [RESEARCH STARTED] AWS S3 - file storage scope

1. Docs: https://docs.aws.amazon.com/s3/
2. SDK: boto3 (s3 client and resource)
3. Auth: IAM roles, access keys
4. Operations: put_object, get_object, list_objects
5. Created 5 documentation files

[DONE] AWS S3 research complete
```

## Error Handling

| Error | Solution |
|-------|----------|
| Service not available in region | Document regional availability |
| Complex IAM requirements | Document step-by-step permission setup |
| SDK version differences | Note version-specific behavior |
