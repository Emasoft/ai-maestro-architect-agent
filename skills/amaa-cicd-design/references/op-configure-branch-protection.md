---
procedure: support-skill
workflow-instruction: support
---

# Operation: Configure Branch Protection Rules


## Contents

- Purpose
- When to Use
- Inputs
- Procedure
- Protected Branches
- Example
- Error Handling

## Purpose

Set up branch protection rules to enforce code review, status checks, and merge requirements for protected branches.

## When to Use

- Setting up protection for main/develop branches
- Enforcing PR reviews before merge
- Requiring CI checks to pass

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Branch name | Repository structure | Yes |
| Required checks | CI workflow | Yes |
| Review requirements | Team policy | Yes |

## Procedure

### Step 1: Identify Protection Requirements

Common requirements:
- Required reviewers (1-2 approvals)
- Required status checks (CI jobs)
- Up-to-date branches before merge
- Signed commits
- Linear history (no merge commits)

### Step 2: Configure via GitHub CLI

> The ratified ai-maestro baseline omits `required_linear_history` and sets `required_approving_review_count` to 0 (GitHub forbids self-approval) — deviate only with MANAGER approval.

```bash
# Enable branch protection with all common settings
gh api -X PUT repos/{owner}/{repo}/branches/main/protection \
  -f required_status_checks='{"strict":true,"checks":[{"context":"test"},{"context":"lint"}]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":false,"required_approving_review_count":0}' \
  -f restrictions=null \
  -f allow_force_pushes=false \
  -f allow_deletions=false
```

### Step 3: Configure via GitHub UI

1. Go to Settings > Branches
2. Click "Add branch protection rule"
3. Enter branch name pattern: `main`
4. Configure settings:

| Setting | Recommended |
|---------|-------------|
| Require a pull request before merging | Yes |
| Require approvals | 0 (solo owner; GitHub forbids self-approval) or 1+ (team) |
| Dismiss stale reviews | Yes |
| Require status checks to pass | Yes |
| Require branches to be up to date | Yes |
| Require signed commits | Optional |
| Require linear history | NOT part of the ratified baseline — enable only on a team's own decision |
| Include administrators | Yes (for strict enforcement) |
| Allow force pushes | No |
| Allow deletions | No |

### Step 4: Add Required Status Checks

List available checks:
```bash
gh api repos/{owner}/{repo}/commits/{sha}/check-runs --jq '.check_runs[].name'
```

Add checks to protection:
```bash
gh api -X PATCH repos/{owner}/{repo}/branches/main/protection/required_status_checks \
  -f strict=true \
  -f checks='[{"context":"test"},{"context":"lint"},{"context":"build"}]'
```

### Step 5: Configure CODEOWNERS

Create `.github/CODEOWNERS`:

```
# Default owners for everything
*       @team-lead @senior-dev

# Specific paths
/src/core/   @core-team
/docs/       @docs-team
/.github/    @devops-team
```

### Step 6: Document Branch Strategy

Create `docs/BRANCHING.md`:

```markdown
# Branch Strategy

## Protected Branches

| Branch | Protection | Purpose |
|--------|------------|---------|
| `main` | Full | Production code |
| `develop` | Partial | Integration branch |

## Merge Requirements

- All PRs require 1 approval
- CI must pass (test, lint, build)
- Branch must be up to date with target

## Workflow

1. Create feature branch from `develop`
2. Make changes and push
3. Open PR to `develop`
4. Get review and CI approval
5. Merge (squash recommended)
```

## Output

| Artifact | Content |
|----------|---------|
| Branch protection | Configured in GitHub |
| `.github/CODEOWNERS` | Code ownership rules |
| `docs/BRANCHING.md` | Branch strategy documentation |

## Verification Checklist

- [ ] Branch protection enabled
- [ ] Required reviewers configured
- [ ] Status checks added
- [ ] CODEOWNERS file created
- [ ] Force push disabled
- [ ] Admins included in enforcement
- [ ] Documentation updated

## Example

```bash
# Complete branch protection setup script

REPO="owner/repo"
BRANCH="main"

# Set protection rules
gh api -X PUT "repos/${REPO}/branches/${BRANCH}/protection" \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "checks": [
      {"context": "test"},
      {"context": "lint"},
      {"context": "build"}
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 0
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF

echo "Branch protection configured for ${BRANCH}"
```

## Error Handling

| Error | Solution |
|-------|----------|
| "Resource not accessible" | Check repository admin permissions |
| "Required check not found" | Run workflow first to register check |
| "Cannot enable without checks" | Add at least one workflow check |
