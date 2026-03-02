# Debugging GitHub Actions Workflows


## Contents

- [Table of Contents](#table-of-contents)
- [1. Debug Script Template](#1-debug-script-template)
  - [1.1 WorkflowDebugger Class Implementation](#11-workflowdebugger-class-implementation)
- [2. Common Debugging Commands](#2-common-debugging-commands)
  - [2.1 Syntax Validation with actionlint](#21-syntax-validation-with-actionlint)
  - [2.2 Local Execution with act](#22-local-execution-with-act)
  - [2.3 Run Logs and Artifact Management](#23-run-logs-and-artifact-management)
  - [2.4 Secret Management Commands](#24-secret-management-commands)
- [3. Troubleshooting Common Issues](#3-troubleshooting-common-issues)
  - [3.1 Matrix Expansion Failures](#31-matrix-expansion-failures)
  - [3.2 Secret Exposure Risks](#32-secret-exposure-risks)
  - [3.3 Runner Availability Issues](#33-runner-availability-issues)
- [Debug Workflow Checklist](#debug-workflow-checklist)

---

Reference guide for debugging CI/CD pipelines locally and in GitHub Actions.

---

## Table of Contents

- 1. Debug Script Template
  - 1.1 WorkflowDebugger class implementation
  - 1.2 Job listing and validation
  - 1.3 Local step simulation
- 2. Common Debugging Commands
  - 2.1 Syntax validation with actionlint
  - 2.2 Local execution with act
  - 2.3 Run logs and artifact management
  - 2.4 Secret management commands
- 3. Troubleshooting Common Issues
  - 3.1 Matrix expansion failures
  - 3.2 Secret exposure risks
  - 3.3 Runner availability issues

---

## 1. Debug Script Template

Every workflow should have a corresponding debug script for local testing.

### 1.1 WorkflowDebugger Class Implementation

```python
#!/usr/bin/env python3
"""
debug_workflow.py - Debug GitHub Actions workflow locally

Usage:
    python debug_workflow.py --workflow ci.yml --job test-matrix
    python debug_workflow.py --workflow release.yml --dry-run
"""

from pathlib import Path
import subprocess
import yaml
import argparse

class WorkflowDebugger:
    """Debug GitHub Actions workflows locally."""

    def __init__(self, workflow_path: Path):
        self.workflow_path = workflow_path
        self.workflow = self._load_workflow()

    def _load_workflow(self) -> dict:
        """Load and parse workflow YAML."""
        with open(self.workflow_path) as f:
            return yaml.safe_load(f)

    def list_jobs(self) -> list[str]:
        """List all jobs in the workflow."""
        return list(self.workflow.get('jobs', {}).keys())

    def validate_syntax(self) -> bool:
        """Validate workflow YAML syntax."""
        # Use actionlint if available
        result = subprocess.run(
            ['actionlint', str(self.workflow_path)],
            capture_output=True
        )
        return result.returncode == 0

    def simulate_job(self, job_name: str, dry_run: bool = True) -> None:
        """Simulate running a job locally."""
        job = self.workflow['jobs'].get(job_name)
        if not job:
            raise ValueError(f"Job {job_name} not found")

        for step in job.get('steps', []):
            step_name = step.get('name', 'Unnamed step')
            if dry_run:
                print(f"[DRY RUN] Would execute: {step_name}")
            else:
                self._execute_step(step)

    def _execute_step(self, step: dict) -> None:
        """Execute a workflow step locally."""
        if 'run' in step:
            subprocess.run(step['run'], shell=True, check=True)
        elif 'uses' in step:
            print(f"[SKIP] Action: {step['uses']}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workflow', required=True)
    parser.add_argument('--job', default=None)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--list-jobs', action='store_true')
    parser.add_argument('--validate', action='store_true')
    args = parser.parse_args()

    debugger = WorkflowDebugger(Path('.github/workflows') / args.workflow)

    if args.validate:
        valid = debugger.validate_syntax()
        print(f"Workflow valid: {valid}")
    elif args.list_jobs:
        for job in debugger.list_jobs():
            print(f"  - {job}")
    elif args.job:
        debugger.simulate_job(args.job, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
```

---

## 2. Common Debugging Commands

### 2.1 Syntax Validation with actionlint

```bash
# Validate single workflow
actionlint .github/workflows/ci.yml

# Validate all workflows
actionlint .github/workflows/*.yml

# Install actionlint
brew install actionlint  # macOS
go install github.com/rhysd/actionlint/cmd/actionlint@latest  # Go
```

### 2.2 Local Execution with act

```bash
# Run specific job locally
act -j build --secret-file .env.secrets

# Run with specific event
act push -j test-matrix

# List available jobs
act -l

# Run with custom platform
act -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest

# Install act
brew install act  # macOS
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux
```

### 2.3 Run Logs and Artifact Management

```bash
# View workflow run logs
gh run view --log

# View specific job logs
gh run view <run-id> --job <job-id> --log

# Re-run failed workflow
gh run rerun <run-id> --failed

# Re-run all jobs
gh run rerun <run-id>

# Download workflow artifacts
gh run download <run-id>

# Download specific artifact
gh run download <run-id> --name <artifact-name>

# List workflow runs
gh run list --workflow ci.yml

# Watch workflow in progress
gh run watch <run-id>
```

### 2.4 Secret Management Commands

```bash
# View secret configuration (names only, not values)
gh secret list

# Set repository secret
gh secret set SECRET_NAME < secret.txt

# Set secret from prompt
gh secret set SECRET_NAME

# Delete secret
gh secret delete SECRET_NAME

# Set environment secret
gh secret set SECRET_NAME --env production

# Set organization secret
gh secret set SECRET_NAME --org my-org
```

---

## 3. Troubleshooting Common Issues

### 3.1 Matrix Expansion Failures

**Problem**: Matrix combinations exceed limits or produce invalid combinations.

**Solution**:
```yaml
# Use exclude to remove invalid combinations
strategy:
  matrix:
    os: [ubuntu-latest, macos-14, windows-latest]
    node: [18, 20]
    exclude:
      - os: windows-latest
        node: 18

# Use include for specific combinations
strategy:
  matrix:
    include:
      - os: ubuntu-latest
        node: 20
        coverage: true
      - os: macos-14
        node: 20
        coverage: false
```

### 3.2 Secret Exposure Risks

**Problem**: Secrets appearing in logs.

**Solution**:
```yaml
# GitHub auto-masks secrets, but avoid echo
- name: Use secret safely
  run: |
    # DON'T do this:
    # echo ${{ secrets.MY_SECRET }}

    # DO this:
    curl -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" https://api.example.com
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}

# Use add-mask for dynamic secrets
- name: Mask dynamic value
  run: |
    SECRET_VALUE=$(generate-secret)
    echo "::add-mask::$SECRET_VALUE"
    echo "Secret is now masked in logs"
```

### 3.3 Runner Availability Issues

**Problem**: Jobs stuck waiting for runners.

**Solution**:
```yaml
# Check runner availability before using
jobs:
  check-runners:
    runs-on: ubuntu-latest
    outputs:
      has-macos: ${{ steps.check.outputs.macos }}
    steps:
      - id: check
        run: echo "macos=true" >> $GITHUB_OUTPUT

  macos-job:
    needs: check-runners
    if: needs.check-runners.outputs.has-macos == 'true'
    runs-on: macos-14

# Use fallback runners
jobs:
  build:
    runs-on: ${{ matrix.runner }}
    strategy:
      matrix:
        include:
          - runner: macos-14
            fallback: macos-13
```

---

## Debug Workflow Checklist

- [ ] Validate YAML syntax with actionlint
- [ ] Test locally with act before pushing
- [ ] Check secret names match workflow references
- [ ] Verify matrix combinations are valid
- [ ] Confirm runner types are available
- [ ] Review logs for masked secrets
- [ ] Test failure scenarios
