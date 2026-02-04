# GH CLI and GraphQL Scripts


## Contents

- [Table of Contents](#table-of-contents)
- [1. Repository Setup Script](#1-repository-setup-script)
  - [1.1 Branch Protection Configuration](#11-branch-protection-configuration)
  - [1.2 Security Settings](#12-security-settings)
  - [1.3 Merge Settings](#13-merge-settings)
- [2. GraphQL Queries](#2-graphql-queries)
  - [2.1 Get Workflow Runs Query](#21-get-workflow-runs-query)
  - [2.2 Get Repository Environments Query](#22-get-repository-environments-query)
  - [2.3 Get Pull Request Status Query](#23-get-pull-request-status-query)
- [3. Workflow Management Scripts](#3-workflow-management-scripts)
  - [3.1 Batch Workflow Operations](#31-batch-workflow-operations)
  - [3.2 Artifact Cleanup Script](#32-artifact-cleanup-script)
- [4. Secret Automation](#4-secret-automation)
  - [4.1 Bulk Secret Setup](#41-bulk-secret-setup)
  - [4.2 Secret Rotation Check](#42-secret-rotation-check)
- [Quick Reference](#quick-reference)

---

Reference scripts for repository configuration and management using GitHub CLI.

---

## Table of Contents

- 1. Repository Setup Script
  - 1.1 Branch protection configuration
  - 1.2 Security settings
  - 1.3 Merge settings
- 2. GraphQL Queries
  - 2.1 Get workflow runs query
  - 2.2 Get repository environments query
  - 2.3 Get pull request status query
- 3. Workflow Management Scripts
  - 3.1 Batch workflow operations
  - 3.2 Artifact cleanup script
- 4. Secret Automation
  - 4.1 Bulk secret setup
  - 4.2 Secret rotation check

---

## 1. Repository Setup Script

### 1.1 Branch Protection Configuration

```bash
#!/bin/bash
# setup_repo.sh - Configure repository settings via GH CLI

REPO="$1"

if [ -z "$REPO" ]; then
    echo "Usage: setup_repo.sh owner/repo"
    exit 1
fi

echo "Configuring repository: $REPO"

# Enable branch protection for main
gh api repos/$REPO/branches/main/protection -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["ci"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f restrictions=null

echo "✓ Branch protection enabled"
```

### 1.2 Security Settings

```bash
# Enable vulnerability alerts
gh api repos/$REPO/vulnerability-alerts -X PUT
echo "✓ Vulnerability alerts enabled"

# Enable automated security fixes
gh api repos/$REPO/automated-security-fixes -X PUT
echo "✓ Automated security fixes enabled"

# Enable secret scanning
gh api repos/$REPO -X PATCH \
  -f security_and_analysis='{"secret_scanning":{"status":"enabled"}}'
echo "✓ Secret scanning enabled"
```

### 1.3 Merge Settings

```bash
# Configure merge settings
gh api repos/$REPO -X PATCH \
  -f allow_squash_merge=true \
  -f allow_merge_commit=false \
  -f allow_rebase_merge=true \
  -f delete_branch_on_merge=true \
  -f allow_auto_merge=true

echo "✓ Merge settings configured"
echo "Repository $REPO configured successfully"
```

---

## 2. GraphQL Queries

### 2.1 Get Workflow Runs Query

```graphql
# get_workflow_runs.graphql
# Usage: gh api graphql -f query="$(cat get_workflow_runs.graphql)" -f owner=OWNER -f repo=REPO

query GetWorkflowRuns($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    actions {
      runs(first: 10, orderBy: {field: CREATED_AT, direction: DESC}) {
        nodes {
          id
          status
          conclusion
          createdAt
          updatedAt
          workflow {
            name
          }
          headBranch
          event
        }
        totalCount
      }
    }
  }
}
```

**CLI Usage**:
```bash
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    actions {
      runs(first: 10) {
        nodes {
          status
          conclusion
          workflow { name }
        }
      }
    }
  }
}' -f owner=Emasoft -f repo=my-repo
```

### 2.2 Get Repository Environments Query

```graphql
# get_environments.graphql
query GetEnvironments($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    environments(first: 10) {
      nodes {
        name
        protectionRules(first: 5) {
          nodes {
            ... on RequiredReviewers {
              reviewers {
                ... on User {
                  login
                }
                ... on Team {
                  name
                }
              }
            }
            ... on WaitTimer {
              waitTimer
            }
          }
        }
      }
    }
  }
}
```

### 2.3 Get Pull Request Status Query

```graphql
# get_pr_status.graphql
query GetPRStatus($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      title
      state
      mergeable
      reviewDecision
      commits(last: 1) {
        nodes {
          commit {
            statusCheckRollup {
              state
              contexts(first: 20) {
                nodes {
                  ... on CheckRun {
                    name
                    conclusion
                    status
                  }
                  ... on StatusContext {
                    context
                    state
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## 3. Workflow Management Scripts

### 3.1 Batch Workflow Operations

```bash
#!/bin/bash
# batch_workflow_ops.sh - Batch operations on workflow runs

REPO="$1"
ACTION="$2"  # cancel, rerun, delete

case "$ACTION" in
  cancel)
    # Cancel all in-progress runs
    gh run list --repo "$REPO" --status in_progress --json databaseId -q '.[].databaseId' | \
    while read run_id; do
      echo "Cancelling run $run_id"
      gh run cancel "$run_id" --repo "$REPO"
    done
    ;;

  rerun-failed)
    # Rerun all failed runs from last 24h
    gh run list --repo "$REPO" --status failure --json databaseId -q '.[].databaseId' | \
    while read run_id; do
      echo "Rerunning failed run $run_id"
      gh run rerun "$run_id" --repo "$REPO" --failed
    done
    ;;

  delete-old)
    # Delete runs older than 30 days (requires admin)
    CUTOFF=$(date -d "30 days ago" +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d)
    gh run list --repo "$REPO" --json databaseId,createdAt -q ".[] | select(.createdAt < \"$CUTOFF\") | .databaseId" | \
    while read run_id; do
      echo "Deleting old run $run_id"
      gh api repos/$REPO/actions/runs/$run_id -X DELETE
    done
    ;;

  *)
    echo "Usage: batch_workflow_ops.sh owner/repo [cancel|rerun-failed|delete-old]"
    exit 1
    ;;
esac
```

### 3.2 Artifact Cleanup Script

```bash
#!/bin/bash
# cleanup_artifacts.sh - Clean up old workflow artifacts

REPO="$1"
DAYS_OLD="${2:-7}"

echo "Cleaning artifacts older than $DAYS_OLD days from $REPO"

# Get artifacts older than specified days
gh api repos/$REPO/actions/artifacts --paginate -q ".artifacts[] | select(.expired == false) | .id" | \
while read artifact_id; do
  CREATED=$(gh api repos/$REPO/actions/artifacts/$artifact_id -q '.created_at')
  CUTOFF=$(date -d "$DAYS_OLD days ago" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -v-${DAYS_OLD}d +%Y-%m-%dT%H:%M:%SZ)

  if [[ "$CREATED" < "$CUTOFF" ]]; then
    echo "Deleting artifact $artifact_id (created: $CREATED)"
    gh api repos/$REPO/actions/artifacts/$artifact_id -X DELETE
  fi
done

echo "Cleanup complete"
```

---

## 4. Secret Automation

### 4.1 Bulk Secret Setup

```python
#!/usr/bin/env python3
"""
setup_secrets.py - Configure GitHub repository secrets

Usage:
    python setup_secrets.py --repo owner/repo --env-file .env.secrets
    python setup_secrets.py --repo owner/repo --platforms apple android
"""

import subprocess
import argparse
from pathlib import Path

REQUIRED_SECRETS = {
    'apple': [
        'APPLE_CERTIFICATE_BASE64',
        'APPLE_CERTIFICATE_PASSWORD',
        'APPLE_ID',
        'APPLE_TEAM_ID',
        'NOTARIZATION_PASSWORD',
    ],
    'android': [
        'ANDROID_KEYSTORE_BASE64',
        'KEYSTORE_PASSWORD',
        'KEY_ALIAS',
        'KEY_PASSWORD',
    ],
    'windows': [
        'WINDOWS_CERTIFICATE_BASE64',
        'WINDOWS_CERTIFICATE_PASSWORD',
    ],
    'npm': ['NPM_TOKEN'],
    'pypi': ['PYPI_API_TOKEN'],
    'docker': ['DOCKERHUB_USERNAME', 'DOCKERHUB_TOKEN'],
}

def set_secret(repo: str, name: str, value: str) -> bool:
    """Set a GitHub repository secret using gh CLI."""
    result = subprocess.run(
        ['gh', 'secret', 'set', name, '--repo', repo],
        input=value.encode(),
        capture_output=True
    )
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True, help='Repository in owner/repo format')
    parser.add_argument('--env-file', required=True, help='Path to .env secrets file')
    parser.add_argument('--platforms', nargs='+', default=['all'], help='Platforms to configure')
    args = parser.parse_args()

    # Load secrets from env file
    secrets = {}
    env_path = Path(args.env_file)
    if not env_path.exists():
        print(f"Error: {args.env_file} not found")
        return 1

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                secrets[key] = value

    # Set secrets for selected platforms
    platforms = args.platforms if 'all' not in args.platforms else REQUIRED_SECRETS.keys()

    for platform in platforms:
        print(f"\nConfiguring {platform} secrets:")
        for secret_name in REQUIRED_SECRETS.get(platform, []):
            if secret_name in secrets:
                success = set_secret(args.repo, secret_name, secrets[secret_name])
                status = "✓" if success else "✗"
                print(f"  {status} {secret_name}")
            else:
                print(f"  ⚠ {secret_name} (not in env file)")

    print("\nSecret setup complete")
    return 0

if __name__ == '__main__':
    exit(main())
```

### 4.2 Secret Rotation Check

```bash
#!/bin/bash
# check_secret_rotation.sh - Check if secrets need rotation

REPO="$1"

echo "Checking secret rotation status for $REPO"
echo "================================================"

# Get secret update timestamps
gh api repos/$REPO/actions/secrets --paginate -q '.secrets[] | "\(.name): \(.updated_at)"' | \
while IFS=: read name updated; do
  DAYS_OLD=$(( ($(date +%s) - $(date -d "$updated" +%s 2>/dev/null || date -jf "%Y-%m-%dT%H:%M:%SZ" "$updated" +%s)) / 86400 ))

  if [ $DAYS_OLD -gt 90 ]; then
    echo "⚠️  $name: $DAYS_OLD days old (ROTATION NEEDED)"
  elif [ $DAYS_OLD -gt 60 ]; then
    echo "🟡 $name: $DAYS_OLD days old (rotation soon)"
  else
    echo "✓  $name: $DAYS_OLD days old"
  fi
done
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `gh api repos/OWNER/REPO` | Get repository info |
| `gh api repos/OWNER/REPO/actions/runs` | List workflow runs |
| `gh api repos/OWNER/REPO/actions/secrets` | List secrets |
| `gh api graphql -f query=...` | Execute GraphQL query |
| `gh run list --repo OWNER/REPO` | List runs with CLI |
| `gh secret set NAME --repo OWNER/REPO` | Set secret |
