---
operation: sync-status-to-github
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-github-integration
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Synchronize Design Status to GitHub Issue


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Verify Design Has Linked Issue](#step-1-verify-design-has-linked-issue)
  - [Step 2: Sync Single Document](#step-2-sync-single-document)
  - [Step 3: Verify Label Changes](#step-3-verify-label-changes)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Sync After Status Transition](#example-sync-after-status-transition)
  - [Example: Sync with Status Change Comment](#example-sync-with-status-change-comment)
  - [Example: Batch Sync All Linked Documents](#example-batch-sync-all-linked-documents)
- [Status to Label Mapping](#status-to-label-mapping)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Trigger this operation when:
- Design document status has changed (e.g., draft to review, review to approved)
- GitHub issue labels need to reflect current design state
- Performing batch sync of all linked documents

## Prerequisites

- gh CLI installed and authenticated
- Design document has `related_issues` field in frontmatter
- GitHub issue exists and is accessible
- Write access to the repository

## Procedure

### Step 1: Verify Design Has Linked Issue

```bash
head -30 docs/design/specs/<design-file>.md
```

Look for `related_issues: ["#42"]` in frontmatter.

### Step 2: Sync Single Document

```bash
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-20250129-a1b2c3d4
```

### Step 3: Verify Label Changes

```bash
gh issue view 42 --json labels
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify gh CLI is authenticated: `gh auth status`
- [ ] Verify design document has `related_issues` in frontmatter
- [ ] Note current design status (e.g., `status: approved`)
- [ ] Run sync: `python scripts/eaa_github_sync_status.py --uuid <UUID>`
- [ ] Verify labels updated: `gh issue view <N> --json labels`
- [ ] Optionally add status change comment: use `--comment` flag

## Examples

### Example: Sync After Status Transition

```bash
# Design was transitioned from draft to review
python scripts/eaa_design_transition.py --uuid PROJ-SPEC-... --status review

# Sync the status to GitHub
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-...

# Output:
# SYNCED: Issue #42 labels updated
# REMOVED: status:draft
# ADDED: status:review
```

### Example: Sync with Status Change Comment

```bash
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment

# Output:
# SYNCED: Issue #42 labels updated
# REMOVED: status:draft
# ADDED: status:approved
# COMMENTED: Status changed to approved
```

### Example: Batch Sync All Linked Documents

```bash
python scripts/eaa_github_sync_status.py --all

# Output:
# SYNCED: 5 documents
# - PROJ-SPEC-001: #42 (draft -> review)
# - PROJ-ADR-002: #45 (no change)
# - PROJ-SPEC-003: #51 (review -> approved)
# - PROJ-RFC-004: #53 (no change)
# - PROJ-ADR-005: #58 (draft -> review)
```

## Status to Label Mapping

| Design Status | GitHub Label |
|---------------|--------------|
| draft | `status:draft` |
| review | `status:review` |
| approved | `status:approved` |
| implementing | `status:implementing` |
| completed | `status:completed` |
| deprecated | `status:deprecated` |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ERROR: Document not linked to any issue` | No `related_issues` in frontmatter | Use [op-create-issue-from-design.md](op-create-issue-from-design.md) or [op-attach-design-to-issue.md](op-attach-design-to-issue.md) first |
| `ERROR: Issue #42 not found` | Issue was deleted or wrong number | Verify issue exists; update frontmatter if needed |
| `ERROR: gh CLI not authenticated` | No auth token | Run `gh auth login` |
| `ERROR: Label creation failed` | Missing permissions | Create labels manually or request access |
| `WARNING: No status change detected` | Status already matches | No action needed |

## Related Operations

- [op-create-issue-from-design.md](op-create-issue-from-design.md) - If design has no linked issue
- [op-attach-design-to-issue.md](op-attach-design-to-issue.md) - If design needs to be linked to existing issue
- [op-verify-gh-cli-auth.md](op-verify-gh-cli-auth.md) - If authentication fails
