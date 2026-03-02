---
procedure: support-skill
workflow-instruction: support
---

# Operation: Create Configuration Template


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Identify Configuration Options](#step-1-identify-configuration-options)
  - [Step 2: Write Configuration Template](#step-2-write-configuration-template)
- [Environment Variables](#environment-variables)
  - [Required](#required)
  - [Optional](#optional)
- [Configuration Files](#configuration-files)
  - [Python (config.py)](#python-configpy)
  - [JavaScript (config.js)](#javascript-configjs)
- [Environment Templates](#environment-templates)
  - [Development (.env.development)](#development-envdevelopment)
  - [Staging (.env.staging)](#staging-envstaging)
  - [Production (.env.production)](#production-envproduction)
- [Docker Configuration](#docker-configuration)
  - [Dockerfile](#dockerfile)
  - [docker-compose.yml](#docker-composeyml)
- [Kubernetes Configuration](#kubernetes-configuration)
  - [ConfigMap](#configmap)
  - [Secret](#secret)
- [Security Guidelines](#security-guidelines)
  - [.gitignore](#gitignore)
- [Validation Script](#validation-script)
  - [Step 3: Save Document](#step-3-save-document)
- [Output](#output)
- [Verification Checklist](#verification-checklist)

## Purpose

Create a configuration template document that provides environment setup, configuration options, and deployment templates for different environments.

## When to Use

- Setting up API integration configuration
- Creating deployment documentation
- Providing environment templates

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Config options | Research findings | Yes |
| Environment variables | Research findings | Yes |
| Default values | Research findings | Yes |

## Procedure

### Step 1: Identify Configuration Options

Collect:
- Required environment variables
- Optional configuration settings
- Default values
- Environment-specific overrides

### Step 2: Write Configuration Template

Use this template:

```markdown
# <API-Name> Configuration Template

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `<API>_API_KEY` | API authentication key | `sk_live_xxx...` |
| `<API>_BASE_URL` | API base URL | `https://api.example.com` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `<API>_TIMEOUT` | Request timeout (seconds) | `30` |
| `<API>_RETRY_COUNT` | Max retry attempts | `3` |
| `<API>_LOG_LEVEL` | Logging level | `INFO` |

---

## Configuration Files

### Python (config.py)

```python
import os
from dataclasses import dataclass

@dataclass
class APIConfig:
    api_key: str
    base_url: str = "https://api.example.com"
    timeout: int = 30
    retry_count: int = 3
    log_level: str = "INFO"

    @classmethod
    def from_env(cls):
        return cls(
            api_key=os.environ["<API>_API_KEY"],
            base_url=os.environ.get("<API>_BASE_URL", cls.base_url),
            timeout=int(os.environ.get("<API>_TIMEOUT", cls.timeout)),
            retry_count=int(os.environ.get("<API>_RETRY_COUNT", cls.retry_count)),
            log_level=os.environ.get("<API>_LOG_LEVEL", cls.log_level),
        )
```

### JavaScript (config.js)

```javascript
const config = {
  apiKey: process.env.<API>_API_KEY,
  baseUrl: process.env.<API>_BASE_URL || 'https://api.example.com',
  timeout: parseInt(process.env.<API>_TIMEOUT) || 30000,
  retryCount: parseInt(process.env.<API>_RETRY_COUNT) || 3,
  logLevel: process.env.<API>_LOG_LEVEL || 'info',
};

module.exports = config;
```

---

## Environment Templates

### Development (.env.development)

```bash
# Development environment
<API>_API_KEY=sk_test_your_test_key
<API>_BASE_URL=https://api.example.com/sandbox
<API>_TIMEOUT=60
<API>_LOG_LEVEL=DEBUG
```

### Staging (.env.staging)

```bash
# Staging environment
<API>_API_KEY=sk_staging_your_staging_key
<API>_BASE_URL=https://api.example.com
<API>_TIMEOUT=30
<API>_LOG_LEVEL=INFO
```

### Production (.env.production)

```bash
# Production environment - USE SECRET MANAGER
# Do NOT store production keys in files
<API>_API_KEY=${SECRET_MANAGER_API_KEY}
<API>_BASE_URL=https://api.example.com
<API>_TIMEOUT=30
<API>_RETRY_COUNT=5
<API>_LOG_LEVEL=WARNING
```

---

## Docker Configuration

### Dockerfile

```dockerfile
ENV <API>_TIMEOUT=30
ENV <API>_RETRY_COUNT=3
ENV <API>_LOG_LEVEL=INFO
```

### docker-compose.yml

```yaml
services:
  app:
    environment:
      - <API>_API_KEY=${<API>_API_KEY}
      - <API>_BASE_URL=https://api.example.com
      - <API>_TIMEOUT=30
```

---

## Kubernetes Configuration

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: <api>-config
data:
  <API>_BASE_URL: "https://api.example.com"
  <API>_TIMEOUT: "30"
  <API>_RETRY_COUNT: "3"
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <api>-secrets
type: Opaque
data:
  <API>_API_KEY: <base64-encoded-key>
```

---

## Security Guidelines

1. **Never commit secrets** to version control
2. **Use .gitignore** for .env files
3. **Rotate keys regularly** (monthly recommended)
4. **Use secret managers** in production
5. **Audit access** to credentials

### .gitignore

```
.env
.env.local
.env.*.local
*.key
*.pem
secrets/
```

---

## Validation Script

```python
#!/usr/bin/env python3
"""Validate API configuration."""

import os
import sys

REQUIRED_VARS = ["<API>_API_KEY"]
OPTIONAL_VARS = ["<API>_BASE_URL", "<API>_TIMEOUT"]

def validate_config():
    missing = [var for var in REQUIRED_VARS if not os.environ.get(var)]
    if missing:
        print(f"ERROR: Missing required variables: {', '.join(missing)}")
        sys.exit(1)
    print("Configuration valid.")

if __name__ == "__main__":
    validate_config()
```
```

### Step 3: Save Document

Save to: `<output-dir>/<api-name>-config-template.md`

## Output

| File | Content |
|------|---------|
| `<api-name>-config-template.md` | Complete configuration template |

## Verification Checklist

- [ ] All required env vars documented
- [ ] Optional env vars with defaults listed
- [ ] Config file examples provided
- [ ] Environment templates included
- [ ] Docker/K8s examples provided
- [ ] Security guidelines included
- [ ] Validation script provided
