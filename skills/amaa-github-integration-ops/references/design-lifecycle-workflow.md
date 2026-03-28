---
topic: design-lifecycle-workflow
parent-skill: amaa-github-integration
---

# Design Lifecycle Workflow


## Table of Contents

- Steps
- Full Example

Recommended end-to-end workflow integrating design documents with GitHub issues.

## Steps

### 1. Create Design Document

```bash
python scripts/amaa_design_uuid.py --file docs/design/specs/new-feature.md --type SPEC
```

### 2. Create GitHub Issue

```bash
python scripts/amaa_github_issue_create.py --uuid PROJ-SPEC-...
```

### 3. Design Review (status: draft -> review)

```bash
python scripts/amaa_design_transition.py --uuid PROJ-SPEC-... --status review
python scripts/amaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
```

### 4. Design Approved (status: review -> approved)

```bash
python scripts/amaa_design_transition.py --uuid PROJ-SPEC-... --status approved
python scripts/amaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
```

### 5. Implementation Complete (close issue)

```bash
python scripts/amaa_design_transition.py --uuid PROJ-SPEC-... --status completed
python scripts/amaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
gh issue close <issue-number> --comment "Design implemented" --repo "$OWNER_REPO"
```

## Full Example

```bash
# Step 1: Create design with UUID
python scripts/amaa_design_uuid.py --file docs/design/specs/new-feature.md --type SPEC

# Step 2: Create GitHub issue
python scripts/amaa_github_issue_create.py --uuid PROJ-SPEC-...

# Step 3: Transition to review
python scripts/amaa_design_transition.py --uuid PROJ-SPEC-... --status review
python scripts/amaa_github_sync_status.py --uuid PROJ-SPEC-... --comment

# Step 4: Approve design
python scripts/amaa_design_transition.py --uuid PROJ-SPEC-... --status approved
python scripts/amaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
```
