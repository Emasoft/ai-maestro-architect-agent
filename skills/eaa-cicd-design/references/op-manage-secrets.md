---
procedure: support-skill
workflow-instruction: support
---

# Operation: Manage GitHub Secrets

## Purpose

Configure and manage GitHub secrets for secure credential storage and usage in workflows, including repository, environment, and organization secrets.

## When to Use

- Setting up secrets for a new repository
- Adding deployment credentials
- Managing environment-specific secrets
- Documenting secret requirements

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Secret name | Requirements | Yes |
| Secret value | Secure source | Yes |
| Secret scope | Requirements | Yes |

## Procedure

### Step 1: Determine Secret Scope

| Scope | Use Case | Access |
|-------|----------|--------|
| Repository | Project-specific credentials | All workflows in repo |
| Environment | Deployment-specific | Workflows targeting environment |
| Organization | Shared across repos | Selected repositories |

### Step 2: Create Secret via GitHub CLI

**Repository Secret:**
```bash
gh secret set SECRET_NAME --body "secret-value"
# Or from file
gh secret set SECRET_NAME < secret-file.txt
```

**Environment Secret:**
```bash
gh secret set SECRET_NAME --env production --body "secret-value"
```

**Organization Secret:**
```bash
gh secret set SECRET_NAME --org my-org --visibility selected --repos "repo1,repo2"
```

### Step 3: List Existing Secrets

```bash
# Repository secrets
gh secret list

# Environment secrets
gh secret list --env production

# Organization secrets
gh secret list --org my-org
```

### Step 4: Use Secrets in Workflows

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Use secret in env
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: ./deploy.sh

      - name: Use secret in input
        uses: some/action@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

### Step 5: Configure Environment Protection

For sensitive deployments:
1. Create environment in repository settings
2. Add required reviewers
3. Add wait timer (optional)
4. Add secret to environment

```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - name: Deploy
        env:
          PROD_KEY: ${{ secrets.PROD_API_KEY }}
        run: ./deploy.sh
```

### Step 6: Document Secret Requirements

Create `docs/SECRETS.md`:

```markdown
# Required Secrets

## Repository Secrets

| Secret | Purpose | How to Obtain |
|--------|---------|---------------|
| `API_KEY` | External API access | Get from dashboard |
| `NPM_TOKEN` | npm publishing | npm token create |

## Environment Secrets

### Production
| Secret | Purpose |
|--------|---------|
| `PROD_DATABASE_URL` | Production database |

### Staging
| Secret | Purpose |
|--------|---------|
| `STAGING_DATABASE_URL` | Staging database |
```

## Output

| File | Content |
|------|---------|
| `docs/SECRETS.md` | Secret documentation |
| Configured secrets | In GitHub settings |

## Verification Checklist

- [ ] Secret scope determined
- [ ] Secret created via gh CLI
- [ ] Secret referenced correctly in workflow
- [ ] Environment protection configured (if needed)
- [ ] Secret requirements documented
- [ ] Secrets never logged or exposed

## Example

```bash
# Set up secrets for a Python package release

# PyPI token
gh secret set PYPI_API_TOKEN --body "pypi-AgEIcH..."

# Test PyPI token (for staging)
gh secret set TEST_PYPI_TOKEN --env staging --body "pypi-AgEIcH..."

# Verify
gh secret list
```

Workflow usage:
```yaml
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish to PyPI
        env:
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          pip install build twine
          python -m build
          twine upload dist/*
```

## Error Handling

| Error | Solution |
|-------|----------|
| Secret not found | Check spelling, verify scope |
| Permission denied | Verify gh auth status |
| Secret masked as *** | Expected - GitHub hides secrets |
