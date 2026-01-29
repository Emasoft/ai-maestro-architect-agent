# GitHub Integration Skill

Link design documents to GitHub issues for complete traceability and status synchronization.

## When to Use

- Creating a GitHub issue from a design document
- Attaching a design document to an existing issue
- Synchronizing design status changes with GitHub labels
- Tracking design-to-issue relationships

## Features

| Feature | Description |
|---------|-------------|
| Issue creation | Create GitHub issues from design documents with proper labels |
| Document attachment | Post design content as issue comments |
| Status sync | Keep GitHub labels synchronized with design status |
| Batch operations | Sync all linked documents at once |

## Scripts

| Script | Purpose |
|--------|---------|
| `eaa_github_issue_create.py` | Create GitHub issue from design document |
| `eaa_github_attach_document.py` | Attach design to existing issue |
| `eaa_github_sync_status.py` | Sync status to GitHub labels |

## Quick Start

Read [SKILL.md](SKILL.md) for the full workflow. Key procedures:

1. **Create issue**: Extract design metadata, create issue, link back to document
2. **Attach document**: Post design content to existing issue
3. **Sync status**: Update GitHub labels when design status changes

## Requirements

- gh CLI installed and authenticated (`gh auth login`)
- Design documents with valid UUID in frontmatter
- Current directory within a GitHub repository

## License

Apache-2.0
