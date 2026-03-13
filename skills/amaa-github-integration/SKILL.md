---
name: amaa-github-integration
description: Use when syncing designs to GitHub issues or managing project boards. Trigger with GitHub integration or issue sync request.
context: fork
agent: ai-maestro-architect-agent-main-agent
user-invocable: true
---

# GitHub Integration Skill

## Overview

Link design documents to GitHub issues for complete traceability. Create issues from designs, attach designs to existing issues, and keep status synchronized between design document status and GitHub issue labels.

## Prerequisites

- gh CLI installed and authenticated (`gh auth status`)
- Current directory within a GitHub repository
- Design documents with valid UUID in frontmatter

## Instructions

1. Verify gh CLI is authenticated: `gh auth status`
2. Verify design document has UUID in frontmatter
3. Choose and execute the appropriate operation:
   - **Create issue**: `python scripts/amaa_github_issue_create.py --uuid <UUID>`
   - **Attach to issue**: `python scripts/amaa_github_attach_document.py --uuid <UUID> --issue <N>`
   - **Sync status**: `python scripts/amaa_github_sync_status.py --uuid <UUID>`
4. Use `--dry-run` flag on create to preview before executing
5. Verify results and confirm design frontmatter was updated
6. For batch sync of all linked documents: `--all` flag on sync script
7. Monitor GitHub Project board for external changes (see monitoring ref)

## Checklist

Copy this checklist and track your progress:

- [ ] Verify gh CLI is installed and authenticated
- [ ] Confirm design document has valid UUID in frontmatter
- [ ] Choose the correct operation (create, attach, or sync)
- [ ] Run with `--dry-run` flag to preview before executing
- [ ] Execute the chosen operation
- [ ] Verify design frontmatter was updated with results
- [ ] Confirm GitHub issue reflects the expected state

## Reference Documents

| Document | Description |
|----------|-------------|
| [op-create-issue-from-design.md](references/op-create-issue-from-design.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling, Related Operations |
| [op-attach-design-to-issue.md](references/op-attach-design-to-issue.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Error Handling, Related Operations |
| [op-sync-status-to-github.md](references/op-sync-status-to-github.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Status to Label Mapping, Error Handling, Related Operations |
| [op-monitor-github-project.md](references/op-monitor-github-project.md) | When to Use, Prerequisites, Procedure, [[TIMESTAMP]](#timestamp), Checklist, Examples, What to Monitor, Error Handling, Related Operations |
| [op-generate-design-uuid.md](references/op-generate-design-uuid.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, UUID Format, Error Handling, Related Operations |

## Examples

```bash
# Create issue from design (dry-run first)
python scripts/amaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --dry-run
python scripts/amaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4
# Output: CREATED: https://github.com/owner/repo/issues/123
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| gh CLI not found | Not installed | `brew install gh` |
| gh not authenticated | No auth token | `gh auth login` |
| Document has no UUID | Missing frontmatter | Run `amaa_design_uuid.py` |
| Issue already exists | Duplicate attempt | Use attach or sync instead |
| Label creation failed | Missing permissions | Create labels manually |

## Output

| Operation | Output |
|-----------|--------|
| Create Issue | GitHub issue URL + design frontmatter updated with `related_issues` |
| Attach Design | Comment posted on issue + labels updated |
| Sync Status | Old status label removed, new label added |
| Dry Run | Preview of what would happen without changes |

## Resources

See Reference Documents table above.
