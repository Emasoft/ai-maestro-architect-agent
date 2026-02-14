---
operation: verify-gh-cli-auth
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-github-integration
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Verify gh CLI Authentication


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Verify gh CLI is Installed](#step-1-verify-gh-cli-is-installed)
  - [Step 2: Check Current Authentication Status](#step-2-check-current-authentication-status)
  - [Step 3: Authenticate (if needed)](#step-3-authenticate-if-needed)
  - [Step 4: Verify Repository Access](#step-4-verify-repository-access)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Fresh Installation and Authentication](#example-fresh-installation-and-authentication)
  - [Example: Re-authenticate After Token Expiry](#example-re-authenticate-after-token-expiry)
- [Installation Commands](#installation-commands)
  - [macOS](#macos)
  - [Ubuntu/Debian](#ubuntudebian)
  - [Windows](#windows)
- [Required Token Scopes](#required-token-scopes)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Trigger this operation when:
- Starting any GitHub integration operation
- Receiving "gh CLI not authenticated" error
- First-time setup of GitHub integration
- gh CLI returns permission errors

## Prerequisites

- gh CLI installed on the system
- Internet connectivity
- GitHub account with repository access

## Procedure

### Step 1: Verify gh CLI is Installed

```bash
gh --version
```

Expected output: `gh version X.X.X`

If not installed, proceed to installation.

### Step 2: Check Current Authentication Status

```bash
gh auth status
```

Expected output for authenticated user:
```
github.com
  ✓ Logged in to github.com as username
  ✓ Git operations for github.com configured to use https protocol.
  ✓ Token: gho_****
  ✓ Token scopes: gist, read:org, repo, workflow
```

### Step 3: Authenticate (if needed)

```bash
gh auth login
```

Follow the prompts:
1. Select `GitHub.com`
2. Select `HTTPS` protocol
3. Authenticate with browser or paste token
4. Verify with `gh auth status`

### Step 4: Verify Repository Access

```bash
gh repo view
```

Should display current repository information.

## Checklist

Copy this checklist and track your progress:

- [ ] Verify gh CLI is installed: `gh --version`
- [ ] If not installed, install gh CLI (see Installation section)
- [ ] Check auth status: `gh auth status`
- [ ] If not authenticated, run: `gh auth login`
- [ ] Verify repository access: `gh repo view`
- [ ] Verify token has required scopes: `repo`, `workflow` (optional: `read:org`)

## Examples

### Example: Fresh Installation and Authentication

```bash
# Check if installed
gh --version
# gh version 2.40.1

# Check auth status (not authenticated)
gh auth status
# You are not logged in.

# Login
gh auth login
# ? What account do you want to log into? GitHub.com
# ? What is your preferred protocol for Git operations on this host? HTTPS
# ? Authenticate Git with your GitHub credentials? Yes
# ? How would you like to authenticate GitHub CLI? Login with a web browser
#
# ! First copy your one-time code: XXXX-XXXX
# Press Enter to open github.com in your browser...

# After browser authentication
gh auth status
# github.com
#   ✓ Logged in to github.com as Emasoft
#   ✓ Git operations for github.com configured to use https protocol.
#   ✓ Token: gho_****
```

### Example: Re-authenticate After Token Expiry

```bash
# Check status shows expired or invalid token
gh auth status
# github.com
#   X Token is invalid

# Refresh authentication
gh auth refresh

# Or re-login
gh auth login
```

## Installation Commands

### macOS
```bash
brew install gh
```

### Ubuntu/Debian
```bash
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### Windows
```bash
winget install GitHub.cli
```

## Required Token Scopes

| Scope | Required | Purpose |
|-------|----------|---------|
| `repo` | Yes | Access to private/public repositories |
| `workflow` | Recommended | Trigger GitHub Actions |
| `read:org` | Optional | Read organization membership |
| `gist` | Optional | Create/manage gists |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `gh: command not found` | gh CLI not installed | Install using commands above |
| `You are not logged in` | No authentication | Run `gh auth login` |
| `Token is invalid` | Expired or revoked token | Run `gh auth refresh` or `gh auth login` |
| `HTTP 401: Bad credentials` | Token lacks permissions | Re-authenticate with required scopes |
| `HTTP 403: Forbidden` | No access to repository | Request repository access from owner |
| `HTTP 404: Not Found` | Repository does not exist | Verify repository URL and existence |

## Related Operations

- [op-create-issue-from-design.md](op-create-issue-from-design.md) - Requires gh auth
- [op-attach-design-to-issue.md](op-attach-design-to-issue.md) - Requires gh auth
- [op-sync-status-to-github.md](op-sync-status-to-github.md) - Requires gh auth
- [op-monitor-github-project.md](op-monitor-github-project.md) - Requires gh auth
