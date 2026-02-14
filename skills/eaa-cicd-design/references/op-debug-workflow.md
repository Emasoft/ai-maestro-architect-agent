---
procedure: support-skill
workflow-instruction: support
---

# Operation: Debug Failing GitHub Actions Workflow


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Review Workflow Logs](#step-1-review-workflow-logs)
  - [Step 2: Enable Debug Logging](#step-2-enable-debug-logging)
  - [Step 3: Add Debug Steps](#step-3-add-debug-steps)
  - [Step 4: Use tmate for Interactive Debugging](#step-4-use-tmate-for-interactive-debugging)
  - [Step 5: Compare Local vs CI Environment](#step-5-compare-local-vs-ci-environment)
  - [Step 6: Common Fix Patterns](#step-6-common-fix-patterns)
  - [Step 7: Create Local Reproduction](#step-7-create-local-reproduction)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example Debug Session](#example-debug-session)
- [Error Handling](#error-handling)

## Purpose

Diagnose and fix failing GitHub Actions workflows using debugging techniques, logging, and local reproduction.

## When to Use

- Workflow fails with unclear error
- Tests pass locally but fail in CI
- Need to understand workflow execution
- Troubleshooting intermittent failures

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Workflow run URL | GitHub Actions | Yes |
| Error message | Workflow logs | Yes |
| Local test results | Local execution | Helpful |

## Procedure

### Step 1: Review Workflow Logs

1. Go to Actions tab in repository
2. Click on failed workflow run
3. Expand failed job
4. Read error messages in red

Key log areas:
- Setup steps (checkout, setup-python, etc.)
- Dependency installation
- Test execution
- Build steps

### Step 2: Enable Debug Logging

Add to workflow for more output:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

Or set repository secrets:
- `ACTIONS_STEP_DEBUG` = `true`
- `ACTIONS_RUNNER_DEBUG` = `true`

### Step 3: Add Debug Steps

```yaml
steps:
  - name: Debug - List files
    run: ls -la

  - name: Debug - Show environment
    run: env | sort

  - name: Debug - Show disk space
    run: df -h

  - name: Debug - Show memory
    run: free -m || vm_stat  # Linux || macOS

  - name: Debug - Show Python packages
    run: pip list
```

### Step 4: Use tmate for Interactive Debugging

```yaml
- name: Setup tmate session
  if: failure()
  uses: mxschmitt/action-tmate@v3
  with:
    limit-access-to-actor: true
```

This provides SSH access to the runner when the workflow fails.

### Step 5: Compare Local vs CI Environment

Check for differences:
- OS version
- Tool versions
- Environment variables
- File permissions
- Network access

```yaml
- name: Show environment info
  run: |
    echo "OS: $(uname -a)"
    echo "Python: $(python --version)"
    echo "Node: $(node --version || echo 'N/A')"
    echo "PWD: $(pwd)"
    echo "User: $(whoami)"
```

### Step 6: Common Fix Patterns

**Dependency issues:**
```yaml
- name: Clear cache and reinstall
  run: |
    rm -rf node_modules package-lock.json
    npm install
```

**Path issues (Windows):**
```yaml
- name: Run script
  shell: bash  # Use bash on Windows too
  run: ./script.sh
```

**Permission issues:**
```yaml
- name: Fix permissions
  run: chmod +x ./scripts/*.sh
```

**Timing issues:**
```yaml
- name: Wait for service
  run: |
    for i in {1..30}; do
      curl -s http://localhost:8080/health && break
      sleep 1
    done
```

### Step 7: Create Local Reproduction

```bash
# Use act to run workflows locally
brew install act  # macOS
act -j test       # Run specific job
act --list        # List available jobs
```

## Output

| Artifact | Content |
|----------|---------|
| Debug logs | Enhanced logging output |
| Fixed workflow | Working workflow file |
| Debug script | `scripts/debug_workflow.py` |

## Verification Checklist

- [ ] Workflow logs reviewed
- [ ] Error message understood
- [ ] Debug logging enabled
- [ ] Environment differences checked
- [ ] Fix applied
- [ ] Workflow passes after fix
- [ ] Debug code removed

## Example Debug Session

```yaml
# Before: failing workflow
- name: Run tests
  run: pytest  # Fails with "Module not found"

# After: fixed workflow
- name: Install package
  run: pip install -e ".[test]"  # Was missing!

- name: Run tests
  run: pytest
```

## Error Handling

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| "Module not found" | Dependencies not installed | Check pip install step |
| "Permission denied" | Script not executable | Add `chmod +x` step |
| "Connection refused" | Service not ready | Add wait/retry logic |
| "Timeout" | Slow operation | Increase timeout value |
| "Out of disk space" | Artifacts too large | Clean up or use larger runner |
