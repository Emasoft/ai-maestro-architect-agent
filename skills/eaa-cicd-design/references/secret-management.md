# Secret Management


## Contents

- [Use Cases (Quick Reference)](#use-cases-quick-reference)
- [Overview](#overview)
- [Secret Hierarchy](#secret-hierarchy)
  - [Levels of Secrets](#levels-of-secrets)
  - [Creating Secrets](#creating-secrets)
    - [Via GitHub CLI](#via-github-cli)
    - [Via GitHub UI](#via-github-ui)
- [Required Secrets by Platform](#required-secrets-by-platform)
  - [Apple (macOS/iOS)](#apple-macosios)
  - [Windows](#windows)
  - [Android](#android)
  - [Package Registries](#package-registries)
  - [Cloud Providers](#cloud-providers)
- [Using Secrets in Workflows](#using-secrets-in-workflows)
  - [Basic Usage](#basic-usage)
  - [Environment Secrets](#environment-secrets)
  - [Environment Protection Rules](#environment-protection-rules)
- [Security Best Practices](#security-best-practices)
  - [Never Log Secrets](#never-log-secrets)
  - [Limit Secret Exposure](#limit-secret-exposure)
  - [Use OIDC Instead of Long-Lived Secrets](#use-oidc-instead-of-long-lived-secrets)
  - [Rotate Secrets Regularly](#rotate-secrets-regularly)
- [Debugging Secret Issues](#debugging-secret-issues)
  - [Common Problems](#common-problems)
  - [Debug Script](#debug-script)
- [Checklist](#checklist)

---

## Use Cases (Quick Reference)

- When you need to decide which secret level to use → [Secret Hierarchy](#secret-hierarchy)
- When you need to create secrets via GitHub CLI → [Creating Secrets](#creating-secrets)
- When you need to use secrets in workflows → [Using Secrets in Workflows](#using-secrets-in-workflows)
- When you need to handle environment-specific secrets → [Environment Secrets](#environment-secrets)
- When you need to manage organization-wide secrets → [Secret Hierarchy](#secret-hierarchy)
- When you need to secure sensitive files (certificates, keys) → [Creating Secrets](#creating-secrets)
- When you need to follow security best practices → [Security Best Practices](#security-best-practices)
- When you need to debug secret-related failures → [Debugging Secret Issues](#debugging-secret-issues)

## Overview

Proper secret management is critical for CI/CD security. This reference covers the hierarchy of secrets in GitHub Actions and best practices for handling sensitive data.

## Secret Hierarchy

### Levels of Secrets

```
Organization Secrets
    └── Repository Secrets
            └── Environment Secrets
```

| Level | Scope | Use Case |
|-------|-------|----------|
| Organization | All repos in org | Shared API keys, org-wide credentials |
| Repository | Single repo | Project-specific secrets |
| Environment | Specific environment | Production vs staging credentials |

### Creating Secrets

#### Via GitHub CLI

```bash
# Repository secret
gh secret set API_KEY --body "your-api-key"

# From file
gh secret set CERTIFICATE < certificate.p12

# Environment secret
gh secret set DATABASE_URL --env production

# Organization secret
gh secret set ORG_API_KEY --org myorg

# List secrets
gh secret list
gh secret list --env production
```

#### Via GitHub UI

1. Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Enter name and value
4. Click "Add secret"

## Required Secrets by Platform

### Apple (macOS/iOS)

| Secret Name | Description | How to Obtain |
|-------------|-------------|---------------|
| `APPLE_CERTIFICATE` | Base64 P12 certificate | Export from Keychain Access |
| `APPLE_CERTIFICATE_PASSWORD` | Certificate password | Set during export |
| `APPLE_ID` | Apple ID email | developer.apple.com |
| `NOTARIZATION_PASSWORD` | App-specific password | appleid.apple.com |
| `APPLE_TEAM_ID` | Team ID | developer.apple.com |
| `PROVISIONING_PROFILE` | Base64 provisioning profile | developer.apple.com |

**Encoding certificate**:
```bash
base64 -i certificate.p12 | pbcopy  # macOS
base64 certificate.p12 > cert.txt   # Linux
```

**Setting secrets**:
```bash
cat certificate.p12 | base64 | gh secret set APPLE_CERTIFICATE
gh secret set APPLE_CERTIFICATE_PASSWORD --body "your-password"
gh secret set APPLE_ID --body "your@email.com"
gh secret set NOTARIZATION_PASSWORD --body "xxxx-xxxx-xxxx-xxxx"
gh secret set APPLE_TEAM_ID --body "XXXXXXXXXX"
```

### Windows

| Secret Name | Description | How to Obtain |
|-------------|-------------|---------------|
| `WINDOWS_CERTIFICATE` | Base64 PFX certificate | Certificate Authority |
| `WINDOWS_CERTIFICATE_PASSWORD` | Certificate password | Set during creation |
| `AZURE_TENANT_ID` | Azure AD tenant | Azure Portal |
| `AZURE_CLIENT_ID` | Service principal ID | Azure Portal |
| `AZURE_CLIENT_SECRET` | Service principal secret | Azure Portal |

**Setting secrets**:
```bash
cat certificate.pfx | base64 | gh secret set WINDOWS_CERTIFICATE
gh secret set WINDOWS_CERTIFICATE_PASSWORD --body "your-password"
```

### Android

| Secret Name | Description | How to Obtain |
|-------------|-------------|---------------|
| `ANDROID_KEYSTORE` | Base64 keystore | `keytool -genkey` |
| `KEYSTORE_PASSWORD` | Keystore password | Set during creation |
| `KEY_ALIAS` | Key alias name | Set during creation |
| `KEY_PASSWORD` | Key password | Set during creation |
| `PLAY_STORE_CREDENTIALS` | Service account JSON | Google Play Console |

**Creating keystore**:
```bash
keytool -genkey -v \
  -keystore release.keystore \
  -alias myapp \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# Encode and set
cat release.keystore | base64 | gh secret set ANDROID_KEYSTORE
gh secret set KEYSTORE_PASSWORD --body "your-password"
gh secret set KEY_ALIAS --body "myapp"
gh secret set KEY_PASSWORD --body "your-key-password"
```

### Package Registries

| Secret Name | Description | How to Obtain |
|-------------|-------------|---------------|
| `NPM_TOKEN` | npm access token | npm.js/settings/tokens |
| `PYPI_API_TOKEN` | PyPI API token | pypi.org/manage/account |
| `CRATES_IO_TOKEN` | crates.io token | crates.io/settings/tokens |
| `DOCKERHUB_USERNAME` | Docker Hub username | hub.docker.com |
| `DOCKERHUB_TOKEN` | Docker Hub access token | hub.docker.com/settings/security |
| `NUGET_API_KEY` | NuGet API key | nuget.org/account/apikeys |

### Cloud Providers

| Provider | Secrets Needed |
|----------|---------------|
| AWS | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` |
| GCP | `GCP_SA_KEY` (service account JSON) |
| Azure | `AZURE_CREDENTIALS` (service principal JSON) |

## Using Secrets in Workflows

### Basic Usage

```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: ./deploy.sh

  - name: Docker Login
    uses: docker/login-action@v3
    with:
      username: ${{ secrets.DOCKERHUB_USERNAME }}
      password: ${{ secrets.DOCKERHUB_TOKEN }}
```

### Environment Secrets

```yaml
jobs:
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}  # staging-specific
        run: ./deploy.sh staging

  deploy-production:
    environment: production
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}  # production-specific
        run: ./deploy.sh production
```

### Environment Protection Rules

Configure in Repository → Settings → Environments:

| Rule | Purpose |
|------|---------|
| Required reviewers | Manual approval before deploy |
| Wait timer | Delay deployment (e.g., 30 minutes) |
| Deployment branches | Restrict which branches can deploy |

```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://myapp.com
    runs-on: ubuntu-latest
    # Will wait for approval if required reviewers configured
```

## Security Best Practices

### Never Log Secrets

```yaml
# BAD - secret visible in logs
- run: echo "Key is ${{ secrets.API_KEY }}"

# GOOD - secrets are masked
- run: ./script.sh
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

### Limit Secret Exposure

```yaml
# BAD - secret available to all steps
env:
  API_KEY: ${{ secrets.API_KEY }}

jobs:
  build:
    steps:
      - run: something  # Has access to API_KEY

# GOOD - secret only where needed
jobs:
  build:
    steps:
      - run: something  # No access to API_KEY

      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}  # Only this step
        run: ./deploy.sh
```

### Use OIDC Instead of Long-Lived Secrets

```yaml
# AWS with OIDC (no secrets needed!)
jobs:
  deploy:
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActions
          aws-region: us-east-1

      - run: aws s3 sync dist/ s3://my-bucket/
```

### Rotate Secrets Regularly

```bash
# Script to check secret age
#!/bin/bash
REPO="owner/repo"

# Get secrets list with dates
gh api "repos/$REPO/actions/secrets" \
  --jq '.secrets[] | "\(.name): \(.updated_at)"'
```

## Debugging Secret Issues

### Common Problems

| Issue | Cause | Solution |
|-------|-------|----------|
| Secret is empty | Wrong secret name | Check spelling, case-sensitive |
| Secret not found | Wrong scope | Check repo vs org vs environment |
| Access denied | Permissions | Check GITHUB_TOKEN permissions |
| Masked as *** | GitHub auto-masking | Expected behavior for security |

### Debug Script

```python
#!/usr/bin/env python3
"""
Debug script for GitHub Actions secret configuration.
Run locally to verify secrets are configured correctly.
"""
import subprocess
import json
import sys

def check_secrets(repo: str) -> dict:
    """Check which secrets are configured."""
    result = subprocess.run(
        ["gh", "secret", "list", "-R", repo, "--json", "name"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return {}

    secrets = json.loads(result.stdout)
    return {s["name"] for s in secrets}

def check_environments(repo: str) -> list:
    """List configured environments."""
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/environments"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return []

    data = json.loads(result.stdout)
    return [env["name"] for env in data.get("environments", [])]

def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else None
    if not repo:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner"],
            capture_output=True,
            text=True,
        )
        repo = json.loads(result.stdout)["nameWithOwner"]

    print(f"Checking secrets for: {repo}")
    print("=" * 50)

    # Required secrets per platform
    required = {
        "Apple": ["APPLE_CERTIFICATE", "APPLE_CERTIFICATE_PASSWORD", "APPLE_ID", "NOTARIZATION_PASSWORD"],
        "Windows": ["WINDOWS_CERTIFICATE", "WINDOWS_CERTIFICATE_PASSWORD"],
        "Android": ["ANDROID_KEYSTORE", "KEYSTORE_PASSWORD", "KEY_ALIAS", "KEY_PASSWORD"],
        "npm": ["NPM_TOKEN"],
        "PyPI": ["PYPI_API_TOKEN"],
    }

    configured = check_secrets(repo)
    print(f"\nConfigured secrets: {len(configured)}")

    for platform, secrets in required.items():
        missing = [s for s in secrets if s not in configured]
        if missing:
            print(f"\n{platform} - MISSING:")
            for s in missing:
                print(f"  - {s}")
        else:
            print(f"\n{platform} - OK")

    envs = check_environments(repo)
    if envs:
        print(f"\nEnvironments: {', '.join(envs)}")

if __name__ == "__main__":
    main()
```

## Checklist

- [ ] All required platform secrets configured
- [ ] Secrets use minimum required scope
- [ ] Environment secrets separate staging/production
- [ ] Protection rules configured for production
- [ ] OIDC used where possible (AWS, GCP, Azure)
- [ ] Secrets rotated periodically
- [ ] No secrets logged or exposed in outputs
- [ ] Debug script verified configuration
