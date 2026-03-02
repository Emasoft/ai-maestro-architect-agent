---
operation: create-issue-from-design
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-github-integration
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Create GitHub Issue from Design Document


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Verify gh CLI Authentication](#step-1-verify-gh-cli-authentication)
  - [Step 2: Verify Design Document Has UUID](#step-2-verify-design-document-has-uuid)
  - [Step 3: Run Dry-Run First](#step-3-run-dry-run-first)
  - [Step 4: Create the Issue](#step-4-create-the-issue)
  - [Step 5: Verify Results](#step-5-verify-results)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Create Issue for Auth Service Spec](#example-create-issue-for-auth-service-spec)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Trigger this operation when:
- A new design document has been created and needs GitHub tracking
- Design document has a valid UUID in frontmatter
- No GitHub issue exists yet for this design

## Prerequisites

- gh CLI installed and authenticated (`gh auth status` returns success)
- Current directory within a GitHub repository
- Design document exists with valid UUID in frontmatter
- Write access to the repository

## Procedure

### Step 1: Verify gh CLI Authentication

```bash
gh auth status
```

Expected output contains: `Logged in to github.com`

### Step 2: Verify Design Document Has UUID

```bash
head -20 docs/design/specs/<design-file>.md
```

Look for `uuid:` field in frontmatter.

### Step 3: Run Dry-Run First

Always run dry-run before creating the actual issue:

```bash
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --dry-run
```

Expected output:
```
DRY-RUN: Would create issue with title "[SPEC] Design Title"
DRY-RUN: Would add labels: design, design:spec, status:draft
```

### Step 4: Create the Issue

```bash
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4
```

### Step 5: Verify Results

The script will:
1. Extract title, type, status from design frontmatter
2. Generate issue title with type prefix: `[SPEC] Design Title`
3. Add labels: `design`, `design:spec`, `status:draft`
4. Include overview section in issue body
5. Update design document with `related_issues: ["#123"]`

## Checklist

Copy this checklist and track your progress:

- [ ] Verify gh CLI is installed: `gh --version`
- [ ] Verify gh CLI is authenticated: `gh auth status`
- [ ] Verify current directory is a GitHub repository: `git remote -v`
- [ ] Verify design document has UUID in frontmatter
- [ ] Run dry-run: `python scripts/eaa_github_issue_create.py --uuid <UUID> --dry-run`
- [ ] Review dry-run output for correctness
- [ ] Create issue: `python scripts/eaa_github_issue_create.py --uuid <UUID>`
- [ ] Verify issue was created: check URL in output
- [ ] Verify design frontmatter updated with `related_issues`

## Examples

### Example: Create Issue for Auth Service Spec

```bash
# Dry-run first
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --dry-run

# Output:
# DRY-RUN: Would create issue with title "[SPEC] Auth Service Architecture"
# DRY-RUN: Would add labels: design, design:spec, status:draft

# Create the issue
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4

# Output:
# CREATED: https://github.com/owner/repo/issues/123
# UPDATED: docs/design/specs/auth-service.md with issue #123
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ERROR: gh CLI not found` | gh CLI not installed | Install via `brew install gh` (macOS) or `apt install gh` (Linux) |
| `ERROR: gh CLI not authenticated` | No auth token | Run `gh auth login` |
| `ERROR: Document has no UUID` | Missing frontmatter | Run `eaa_design_uuid.py --file <path> --type SPEC` |
| `WARNING: Document already linked to issues` | Issue already exists | Use [op-attach-design-to-issue.md](op-attach-design-to-issue.md) or [op-sync-status-to-github.md](op-sync-status-to-github.md) instead |
| `ERROR: Repository not found` | Not in git repo | Navigate to repository root |

## Related Operations

- [op-generate-design-uuid.md](op-generate-design-uuid.md) - If design has no UUID
- [op-attach-design-to-issue.md](op-attach-design-to-issue.md) - If issue already exists
- [op-sync-status-to-github.md](op-sync-status-to-github.md) - To sync status changes
- [op-verify-gh-cli-auth.md](op-verify-gh-cli-auth.md) - If authentication fails
