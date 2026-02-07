---
operation: attach-design-to-issue
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-github-integration
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Attach Design Document to Existing GitHub Issue

## When to Use

Trigger this operation when:
- A GitHub issue already exists and you need to link a design document to it
- Design document was created after the issue was opened
- Multiple designs need to be linked to a single issue

## Prerequisites

- gh CLI installed and authenticated
- Design document exists with valid UUID in frontmatter
- Target GitHub issue exists
- Write access to the repository

## Procedure

### Step 1: Verify the Issue Exists

```bash
gh issue view 42
```

Confirm the issue number and title match your expectations.

### Step 2: Verify Design Document Has UUID

```bash
head -20 docs/design/specs/<design-file>.md
```

Look for `uuid:` field in frontmatter.

### Step 3: Attach the Design Document

```bash
python scripts/eaa_github_attach_document.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --issue 42
```

### Step 4: Verify Results

The script will:
1. Post design document content as issue comment
2. Update issue labels based on design status
3. Update design document with `related_issues: ["#42"]`

## Checklist

Copy this checklist and track your progress:

- [ ] Verify gh CLI is authenticated: `gh auth status`
- [ ] Verify issue exists: `gh issue view <N>`
- [ ] Record issue title and number for verification
- [ ] Verify design document has UUID in frontmatter
- [ ] Attach design: `python scripts/eaa_github_attach_document.py --uuid <UUID> --issue <N>`
- [ ] Verify comment was posted: `gh issue view <N> --comments`
- [ ] Verify labels updated on issue
- [ ] Verify design frontmatter updated with `related_issues`

## Examples

### Example: Attach Spec to Feature Request Issue

```bash
# Verify issue exists
gh issue view 42

# Output:
# Feature: Add OAuth2 Support
# State: OPEN
# Labels: feature, priority:high

# Attach the design document
python scripts/eaa_github_attach_document.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --issue 42

# Output:
# ATTACHED: Design to issue #42
# UPDATED: Labels [design, design:spec, status:draft, feature, priority:high]
```

### Example: Attach with Custom Comment Header

```bash
python scripts/eaa_github_attach_document.py \
  --uuid PROJ-SPEC-20250129-a1b2c3d4 \
  --issue 42 \
  --header "Revised Architecture Design (v2)"
```

This adds a custom header to distinguish from previous attachments.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ERROR: Issue #42 not found` | Issue does not exist or wrong number | Verify issue number with `gh issue list` |
| `ERROR: Document has no UUID` | Missing frontmatter | Run `eaa_design_uuid.py --file <path> --type SPEC` |
| `ERROR: gh CLI not authenticated` | No auth token | Run `gh auth login` |
| `ERROR: Permission denied` | No write access to repo | Request repository write access |
| `WARNING: Design already linked to #42` | Already attached | Use [op-sync-status-to-github.md](op-sync-status-to-github.md) to update status |

## Related Operations

- [op-create-issue-from-design.md](op-create-issue-from-design.md) - If no issue exists yet
- [op-sync-status-to-github.md](op-sync-status-to-github.md) - To sync status changes after attach
- [op-generate-design-uuid.md](op-generate-design-uuid.md) - If design has no UUID
- [op-verify-gh-cli-auth.md](op-verify-gh-cli-auth.md) - If authentication fails
