# GitHub Actions Part 4: Debugging and Common Patterns


## Contents

- [Debugging](#debugging)
  - [Debug Logging](#debug-logging)
  - [SSH into Runner](#ssh-into-runner)
  - [Local Testing with act](#local-testing-with-act)
- [Common Patterns](#common-patterns)
  - [Monorepo Path Filtering](#monorepo-path-filtering)
  - [Scheduled Jobs](#scheduled-jobs)
  - [Manual Workflow with Inputs](#manual-workflow-with-inputs)
- [Checklist](#checklist)

---

## Debugging

### Debug Logging
```yaml
# Enable debug logging in workflow
env:
  ACTIONS_RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

### SSH into Runner
```yaml
- name: Setup tmate session
  if: failure()
  uses: mxschmitt/action-tmate@v3
  with:
    limit-access-to-actor: true
```

### Local Testing with act
```bash
# Install act
brew install act

# Run workflow locally
act push

# Run specific job
act -j build

# Use secrets
act -s MY_SECRET=value

# List workflows
act -l
```

## Common Patterns

### Monorepo Path Filtering
```yaml
on:
  push:
    paths:
      - 'packages/frontend/**'
      - 'packages/shared/**'
    paths-ignore:
      - '**/*.md'
      - '.github/**'
```

### Scheduled Jobs
```yaml
on:
  schedule:
    - cron: '0 6 * * *'    # Daily at 6am UTC
    - cron: '0 0 * * 0'    # Weekly Sunday midnight
```

### Manual Workflow with Inputs
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options:
          - staging
          - production
      dry_run:
        description: 'Dry run (no actual deploy)'
        required: false
        type: boolean
        default: true
```

## Checklist

- [ ] Workflow triggers defined correctly
- [ ] Matrix covers all target platforms
- [ ] Secrets configured in repository
- [ ] Permissions minimized
- [ ] Actions pinned to specific versions
- [ ] Cache configured for dependencies
- [ ] Artifacts uploaded/downloaded as needed
- [ ] Release workflow creates proper artifacts

---
Back to [GitHub Actions Reference](github-actions.md)
