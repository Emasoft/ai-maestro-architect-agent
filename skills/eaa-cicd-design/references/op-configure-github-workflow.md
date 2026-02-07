---
procedure: support-skill
workflow-instruction: support
---

# Operation: Configure GitHub Actions Workflow

## Purpose

Configure a GitHub Actions workflow with proper triggers, jobs, steps, and dependencies for a specific use case.

## When to Use

- Creating a new workflow file
- Modifying existing workflow configuration
- Setting up specific workflow triggers

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Workflow purpose | Requirements | Yes |
| Trigger events | Requirements | Yes |
| Jobs needed | Design | Yes |

## Procedure

### Step 1: Define Workflow Triggers

Available triggers:

```yaml
on:
  # Push and PR triggers
  push:
    branches: [main, develop]
    paths: ['src/**', 'tests/**']  # Optional path filter
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

  # Tag triggers (for releases)
  push:
    tags: ['v*']

  # Scheduled triggers
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

  # Manual triggers
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
```

### Step 2: Select Runner

| Platform | Runner |
|----------|--------|
| Linux x64 | `ubuntu-latest` |
| macOS ARM | `macos-14` |
| macOS x64 | `macos-13` |
| Windows | `windows-latest` |

### Step 3: Define Jobs Structure

```yaml
jobs:
  job-1:
    runs-on: ubuntu-latest
    outputs:
      result: ${{ steps.step-id.outputs.value }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Step with output
        id: step-id
        run: echo "value=result" >> $GITHUB_OUTPUT

  job-2:
    needs: job-1  # Dependency
    runs-on: ubuntu-latest
    steps:
      - name: Use output from job-1
        run: echo "${{ needs.job-1.outputs.result }}"
```

### Step 4: Configure Conditional Execution

```yaml
steps:
  - name: Only on main branch
    if: github.ref == 'refs/heads/main'
    run: echo "On main"

  - name: Only on tags
    if: startsWith(github.ref, 'refs/tags/')
    run: echo "On tag"

  - name: Only on success
    if: success()
    run: echo "Previous steps succeeded"

  - name: Always run
    if: always()
    run: echo "Cleanup"
```

### Step 5: Add Environment and Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    env:
      NODE_ENV: production
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: ./deploy.sh
```

### Step 6: Save Workflow File

Save to `.github/workflows/<workflow-name>.yml`

## Output

| File | Content |
|------|---------|
| `.github/workflows/<name>.yml` | Complete workflow configuration |

## Verification Checklist

- [ ] Triggers match requirements
- [ ] Correct runners selected
- [ ] Job dependencies defined
- [ ] Conditionals properly configured
- [ ] Secrets referenced (not hardcoded)
- [ ] YAML syntax valid

## Example

```yaml
name: Build and Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Test
        run: npm test
```

## Error Handling

| Error | Solution |
|-------|----------|
| Invalid YAML | Use YAML linter, check indentation |
| Job not triggered | Verify trigger conditions and branch names |
| Action not found | Check action name and version |
