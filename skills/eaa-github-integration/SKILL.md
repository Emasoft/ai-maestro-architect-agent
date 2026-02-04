---
name: eaa-github-integration
description: Use when linking design documents to GitHub issues. Creates issues from designs and syncs status. Trigger with GitHub issue linking or design traceability requests.
version: 1.0.0
compatibility: Requires AI Maestro installed.
context: fork
agent: eaa-planner
user-invocable: true
triggers:
  - when creating GitHub issues from design documents
  - when attaching design documents to existing issues
  - when synchronizing design status with GitHub issues
  - when tracking design-to-issue relationships
---

# GitHub Integration Skill

## Overview

Link design documents to GitHub issues for complete traceability. Create issues from designs, attach designs to existing issues, and keep status synchronized between design document status and GitHub issue labels.

## Prerequisites

- gh CLI installed and authenticated (`gh auth status` returns success)
- Current directory within a GitHub repository
- Design documents with valid UUID in frontmatter
- Write access to the repository

## Instructions

1. Verify gh CLI is authenticated
2. Verify design document has UUID in frontmatter
3. Use appropriate procedure:
   - PROCEDURE 1: Create issue from design document
   - PROCEDURE 2: Attach design to existing issue
   - PROCEDURE 3: Synchronize status to GitHub
4. Verify results and update design frontmatter

### Checklist

Copy this checklist and track your progress:

- [ ] Verify gh CLI is installed (`gh --version`)
- [ ] Verify gh CLI is authenticated (`gh auth status`)
- [ ] Verify current directory is within a GitHub repository
- [ ] Verify design document has UUID in frontmatter
- [ ] Choose operation: Create Issue / Attach to Issue / Sync Status
- [ ] For Create Issue:
  - [ ] Run dry-run first: `python scripts/eaa_github_issue_create.py --uuid <UUID> --dry-run`
  - [ ] Create issue: `python scripts/eaa_github_issue_create.py --uuid <UUID>`
  - [ ] Verify issue created and design frontmatter updated
- [ ] For Attach to Issue:
  - [ ] Verify issue exists: `gh issue view <N>`
  - [ ] Attach design: `python scripts/eaa_github_attach_document.py --uuid <UUID> --issue <N>`
  - [ ] Verify comment posted and labels updated
- [ ] For Sync Status:
  - [ ] Run sync: `python scripts/eaa_github_sync_status.py --uuid <UUID>`
  - [ ] Verify labels updated to match design status

---

## Table of Contents

### Core Procedures
- 1. PROCEDURE: Create Issue from Design Document
- 2. PROCEDURE: Attach Design to Existing Issue
- 3. PROCEDURE: Synchronize Status to GitHub

### Edge Cases
- 4. EDGE CASE: Issue Already Exists
- 5. EDGE CASE: Design Has No UUID
- 6. EDGE CASE: gh CLI Not Available

### Reference Documentation
For detailed troubleshooting, see [troubleshooting.md](references/troubleshooting.md):
- Common errors and solutions
- gh CLI authentication issues
- Label creation problems

For status mapping reference, see [status-mapping.md](references/status-mapping.md):
- Design status to GitHub label mapping
- Valid status transitions
- Label naming conventions

---

## Quick Reference

### Scripts Location

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/eaa_github_issue_create.py` | Create issue from design | `--uuid <UUID>` |
| `scripts/eaa_github_attach_document.py` | Attach design to issue | `--uuid <UUID> --issue <N>` |
| `scripts/eaa_github_sync_status.py` | Sync status to issue | `--uuid <UUID>` |

### Status to Label Mapping

| Design Status | GitHub Label |
|---------------|--------------|
| draft | `status:draft` |
| review | `status:review` |
| approved | `status:approved` |
| implementing | `status:implementing` |
| completed | `status:completed` |
| deprecated | `status:deprecated` |

---

## 1. PROCEDURE: Create Issue from Design Document

Use this when you have a design document and need to create a corresponding GitHub issue.

### Prerequisites

1. Design document must have valid UUID in frontmatter
2. gh CLI must be installed and authenticated
3. Current directory must be within a GitHub repository

### Step-by-Step

**Step 1: Verify Prerequisites**

```bash
# Check gh CLI is authenticated
gh auth status

# Verify design document exists and has UUID
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --dry-run
```

**Step 2: Create the Issue**

```bash
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4
```

**Step 3: Verify Results**

The script will:
1. Extract title, type, status from design frontmatter
2. Generate issue title with type prefix: `[SPEC] Design Title`
3. Add labels: `design`, `design:spec`, `status:draft`
4. Include overview section in issue body
5. Update design document with `related_issues: ["#123"]`

### Expected Output

```
CREATED: https://github.com/owner/repo/issues/123
UPDATED: docs/design/specs/auth-service.md with issue #123
```

---

## 2. PROCEDURE: Attach Design to Existing Issue

Use this when a GitHub issue already exists and you need to link a design document to it.

### Prerequisites

1. Design document must have valid UUID
2. GitHub issue must exist
3. gh CLI must be authenticated

### Step-by-Step

**Step 1: Verify the Issue Exists**

```bash
gh issue view 42
```

**Step 2: Attach the Design Document**

```bash
python scripts/eaa_github_attach_document.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --issue 42
```

**Step 3: Verify Results**

The script will:
1. Post design document content as issue comment
2. Update issue labels based on design status
3. Update design document with `related_issues: ["#42"]`

### Custom Comment Header

```bash
python scripts/eaa_github_attach_document.py --uuid PROJ-SPEC-... --issue 42 --header "Revised Architecture Design"
```

---

## 3. PROCEDURE: Synchronize Status to GitHub

Use this when design status changes and GitHub issue labels need updating.

### Single Document Sync

```bash
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-20250129-a1b2c3d4
```

### With Status Change Comment

```bash
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
```

### Batch Sync All Linked Documents

```bash
python scripts/eaa_github_sync_status.py --all
```

### Expected Behavior

1. Reads current status from design document frontmatter
2. Gets current labels from linked GitHub issue(s)
3. Removes old status labels (e.g., `status:draft`)
4. Adds new status label (e.g., `status:approved`)
5. Optionally adds status change comment

---

## 4. EDGE CASE: Issue Already Exists

**Situation**: Design document already has `related_issues` in frontmatter.

**Detection**: Script shows warning:
```
WARNING: Document already linked to issues: ["#42"]
```

**Resolution Options**:

1. **Attach to existing issue instead**:
   ```bash
   python scripts/eaa_github_attach_document.py --uuid PROJ-SPEC-... --issue 42
   ```

2. **Sync status to existing issue**:
   ```bash
   python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-...
   ```

3. **Create additional issue anyway** (if truly needed):
   - Manually create issue via `gh issue create`
   - Manually update design document frontmatter

---

## 5. EDGE CASE: Design Has No UUID

**Situation**: Design document does not have `uuid` field in frontmatter.

**Detection**: Script shows error:
```
ERROR: Document has no UUID in frontmatter: docs/design/specs/auth.md
```

**Resolution**:

1. **Generate UUID for the document**:
   ```bash
   python scripts/eaa_design_uuid.py --file docs/design/specs/auth.md --type SPEC
   ```

2. **Verify UUID was added**:
   ```bash
   head -20 docs/design/specs/auth.md
   ```

3. **Retry the GitHub integration**:
   ```bash
   python scripts/eaa_github_issue_create.py --uuid <new-uuid>
   ```

---

## 6. EDGE CASE: gh CLI Not Available

**Situation**: gh CLI is not installed or not authenticated.

**Detection**: Script shows error:
```
ERROR: gh CLI not found. Install from https://cli.github.com/
```
or
```
ERROR: gh CLI not authenticated. Run: gh auth login
```

**Resolution**:

1. **Install gh CLI**:
   ```bash
   # macOS
   brew install gh

   # Ubuntu/Debian
   sudo apt install gh

   # Windows
   winget install GitHub.cli
   ```

2. **Authenticate gh CLI**:
   ```bash
   gh auth login
   ```

3. **Verify authentication**:
   ```bash
   gh auth status
   ```

4. **Retry the operation**

---

## Monitoring GitHub Project Changes

### GitHub Project Kanban Monitoring

During active design work, monitor the GitHub Project board for external changes that may affect your work.

**Poll Interval:** Every 5 minutes during active work sessions

**What to Monitor:**
- Card movements (status changes)
- New comments on linked issues
- Label changes
- Assignment changes
- Milestone updates

**Monitoring Command:**
```bash
# List all items in the project board
gh project item-list --owner Emasoft --format json

# Get specific project items with details
gh project item-list --owner Emasoft --project [PROJECT_NUMBER] --format json | jq '.items[] | {title, status, updatedAt}'

# Check for items updated in last 5 minutes
gh project item-list --owner Emasoft --format json | jq --arg cutoff "$(date -v-5M -u +%Y-%m-%dT%H:%M:%SZ)" '.items[] | select(.updatedAt > $cutoff)'
```

**Actions on External Change Detection:**

1. **On card movement detected:**
   ```bash
   # Notify EOA about status change
   curl -X POST "http://localhost:23000/api/messages" \
     -H "Content-Type: application/json" \
     -d '{
       "from": "eaa-architect-main-agent",
       "to": "ecos",
       "subject": "GitHub Project Change Detected",
       "priority": "normal",
       "content": {
         "type": "project_sync",
         "message": "Card [CARD_TITLE] moved from [OLD_STATUS] to [NEW_STATUS]. Updating local design state."
       }
     }'
   ```

2. **Update local design document state** to match GitHub Project status

3. **Log change** in `docs_dev/design/project-sync-log.md`

**Sync Log Format:**
```markdown
## [TIMESTAMP]
- Card: [CARD_TITLE]
- Change: [OLD_STATUS] -> [NEW_STATUS]
- Source: GitHub Project external update
- Action: Updated local design state
- Notified: EOA via AI Maestro
```

---

## Integration with Design Lifecycle

### Recommended Workflow

1. **Create Design Document**
   ```bash
   python scripts/eaa_design_uuid.py --file docs/design/specs/new-feature.md --type SPEC
   ```

2. **Create GitHub Issue**
   ```bash
   python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-...
   ```

3. **Design Review** (status: draft -> review)
   ```bash
   python scripts/eaa_design_transition.py --uuid PROJ-SPEC-... --status review
   python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
   ```

4. **Design Approved** (status: review -> approved)
   ```bash
   python scripts/eaa_design_transition.py --uuid PROJ-SPEC-... --status approved
   python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
   ```

5. **Implementation Complete** (close issue)
   ```bash
   python scripts/eaa_design_transition.py --uuid PROJ-SPEC-... --status completed
   python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
   gh issue close <issue-number> --comment "Design implemented"
   ```

---

## Output

Each GitHub integration operation produces specific outputs that confirm successful execution:

| Operation | Output Type | Example | Description |
|-----------|-------------|---------|-------------|
| Create Issue from Design | GitHub issue URL + local file update | `CREATED: https://github.com/owner/repo/issues/123`<br>`UPDATED: docs/design/specs/auth-service.md with issue #123` | Creates new GitHub issue and updates design frontmatter with `related_issues` |
| Attach Design to Issue | Issue comment + label update | `ATTACHED: Design to issue #42`<br>`UPDATED: Labels [design, design:spec, status:draft]` | Adds design content as comment and syncs labels |
| Sync Status | Label change confirmation | `SYNCED: Issue #42 labels updated`<br>`REMOVED: status:draft`<br>`ADDED: status:approved` | Updates issue labels to match design status |
| Dry Run | Validation report | `DRY-RUN: Would create issue with title "[SPEC] Auth Service"`<br>`DRY-RUN: Would add labels: design, design:spec, status:draft` | Shows what would happen without making changes |
| Error | Error message + cause | `ERROR: gh CLI not authenticated. Run: gh auth login` | Describes the problem and recommended fix |

### Output File Modifications

| Modified File | Field Updated | Purpose |
|---------------|---------------|---------|
| Design document frontmatter | `related_issues: ["#123"]` | Links design to GitHub issue(s) |
| Design document frontmatter | `status: approved` | Updated by transition (synced to GitHub) |
| GitHub issue | Labels: `design`, `design:spec`, `status:*` | Tracks design type and current status |
| GitHub issue | Comments | Contains design document content snapshots |

---

## Examples

### Example 1: Create Issue from Design

```bash
# Verify prerequisites
gh auth status
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4 --dry-run

# Create the issue
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-20250129-a1b2c3d4

# Expected output:
# CREATED: https://github.com/owner/repo/issues/123
# UPDATED: docs/design/specs/auth-service.md with issue #123
```

### Example 2: Full Design-to-Implementation Workflow

```bash
# Step 1: Create design with UUID
python scripts/eaa_design_uuid.py --file docs/design/specs/new-feature.md --type SPEC

# Step 2: Create GitHub issue
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-...

# Step 3: Transition to review
python scripts/eaa_design_transition.py --uuid PROJ-SPEC-... --status review
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment

# Step 4: Approve design
python scripts/eaa_design_transition.py --uuid PROJ-SPEC-... --status approved
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| gh CLI not found | Not installed | Install via `brew install gh` or equivalent |
| gh CLI not authenticated | No auth token | Run `gh auth login` |
| Document has no UUID | Missing frontmatter | Run `eaa_design_uuid.py --file <path>` |
| Issue already exists | Duplicate creation attempt | Use attach or sync instead |
| Label creation failed | Missing permissions | Create labels manually or request access |

## Resources

- [troubleshooting.md](references/troubleshooting.md) - Common errors and solutions
- [status-mapping.md](references/status-mapping.md) - Design status to GitHub label mapping
- `scripts/eaa_github_issue_create.py` - Create issue from design
- `scripts/eaa_github_attach_document.py` - Attach design to issue
- `scripts/eaa_github_sync_status.py` - Sync status to issue
- eaa-design-lifecycle - Design document state management
- eaa-requirements-analysis - Requirements extraction and tracking
- eaa-planning-patterns - Implementation planning from designs
