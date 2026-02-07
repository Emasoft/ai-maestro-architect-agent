---
procedure: support-skill
workflow-instruction: support
---

# Operation: Create Integration Guide

## Purpose

Create a step-by-step integration guide with code examples showing how to integrate the API into a project, including setup, common operations, and error handling.

## When to Use

- Providing implementation guidance
- Creating developer onboarding documentation
- Documenting integration patterns

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| API details | Research findings | Yes |
| SDK/client libraries | Research findings | Yes |
| Common use cases | Research findings | Yes |

## Procedure

### Step 1: Identify Integration Approach

Options:
- Official SDK (preferred if available)
- HTTP client (requests, axios, etc.)
- Generated client from OpenAPI spec

### Step 2: Write Integration Guide

Use this template:

```markdown
# <API-Name> Integration Guide

## Prerequisites

- <Language> version <X.X> or higher
- <API-Name> account with API credentials
- <Any other requirements>

## Installation

### Option 1: Official SDK (Recommended)

```bash
# Python
pip install <sdk-package>

# JavaScript
npm install <sdk-package>
```

### Option 2: Direct HTTP

Use your preferred HTTP client (requests, axios, etc.)

---

## Quick Start

### Step 1: Set Up Credentials

```python
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

### Step 2: Initialize Client

```python
from <sdk> import Client

client = Client(api_key=API_KEY)
```

### Step 3: Make Your First Request

```python
# Example: List resources
resources = client.resources.list(limit=10)
for resource in resources:
    print(f"ID: {resource.id}, Name: {resource.name}")
```

---

## Common Operations

### Operation 1: <Common Task>

<Description of what this operation does>

```python
# Full example with error handling
def <operation_name>(<parameters>):
    try:
        result = client.<method>(<params>)
        return result
    except APIError as e:
        logger.error(f"API error: {e}")
        raise
```

**Example Usage**:

```python
result = <operation_name>(<example_params>)
print(result)
```

---

### Operation 2: <Another Common Task>

<Description>

```python
# Code example
```

---

## Error Handling

### SDK Exceptions

| Exception | Cause | Handling |
|-----------|-------|----------|
| `AuthError` | Invalid credentials | Check API key |
| `RateLimitError` | Too many requests | Implement backoff |
| `NotFoundError` | Resource not found | Verify resource ID |
| `APIError` | General API error | Log and retry |

### Retry Pattern

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff()
def fetch_data():
    return client.data.get()
```

---

## Best Practices

1. **Use environment variables** for credentials
2. **Implement retry logic** for transient failures
3. **Handle rate limits** with exponential backoff
4. **Log API calls** for debugging
5. **Validate inputs** before API calls
6. **Use pagination** for large result sets

---

## Testing Your Integration

### Unit Tests

```python
from unittest.mock import patch

def test_fetch_resource():
    with patch("client.resources.get") as mock_get:
        mock_get.return_value = {"id": "123", "name": "Test"}
        result = fetch_resource("123")
        assert result["id"] == "123"
```

### Integration Tests

```python
# Use test/sandbox credentials
import os
os.environ["API_KEY"] = "test_key_xxx"

def test_real_api_call():
    client = Client(api_key=os.environ["API_KEY"])
    result = client.resources.list(limit=1)
    assert len(result) >= 0
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection timeout | Check network, increase timeout |
| SSL certificate error | Update certificates |
| Encoding issues | Ensure UTF-8 encoding |
| Unexpected response | Check API version compatibility |
```

### Step 3: Save Document

Save to: `<output-dir>/<api-name>-integration.md`

## Output

| File | Content |
|------|---------|
| `<api-name>-integration.md` | Complete integration guide |

## Verification Checklist

- [ ] Prerequisites listed
- [ ] Installation instructions provided
- [ ] Quick start with working example
- [ ] Common operations documented
- [ ] Error handling patterns shown
- [ ] Best practices included
- [ ] Testing guidance provided
- [ ] Troubleshooting section included
