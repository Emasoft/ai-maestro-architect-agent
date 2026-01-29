# GitHub Integration Troubleshooting

## Table of Contents

- 1. gh CLI Errors
  - 1.1 CLI not found
  - 1.2 Authentication failed
  - 1.3 Permission denied
- 2. Document Errors
  - 2.1 Document not found
  - 2.2 No UUID in frontmatter
  - 2.3 Invalid frontmatter format
- 3. Issue Errors
  - 3.1 Issue not found
  - 3.2 Label creation failed
  - 3.3 Comment failed
- 4. Sync Errors
  - 4.1 No linked issues
  - 4.2 Status label conflict
  - 4.3 Batch sync failures

---

## 1. gh CLI Errors

### 1.1 CLI not found

**Error**:
```
ERROR: gh CLI not found. Install from https://cli.github.com/
```

**Cause**: GitHub CLI is not installed or not in PATH.

**Solution**:

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Fedora
sudo dnf install gh

# Windows
winget install GitHub.cli
```

Verify installation:
```bash
which gh
gh --version
```

---

### 1.2 Authentication failed

**Error**:
```
ERROR: gh CLI not authenticated. Run: gh auth login
```

**Cause**: gh CLI is installed but not logged in.

**Solution**:

```bash
# Interactive login
gh auth login

# Select:
# - GitHub.com
# - HTTPS
# - Login with browser
```

Verify authentication:
```bash
gh auth status
```

---

### 1.3 Permission denied

**Error**:
```
ERROR: Failed to create issue: HTTP 403: ...
```

**Cause**: Authenticated user lacks permission to create issues in the repository.

**Solution**:

1. Verify you have write access to the repository
2. Check repository settings for issue creation permissions
3. If using a token, ensure it has `repo` scope

```bash
# Check current authentication scope
gh auth status

# Re-authenticate with correct scope
gh auth login --scopes repo
```

---

## 2. Document Errors

### 2.1 Document not found

**Error**:
```
ERROR: Document not found with UUID: PROJ-SPEC-20250129-a1b2c3d4
```

**Cause**: No document with matching UUID exists in the design root.

**Solution**:

1. List all UUIDs to find the correct one:
   ```bash
   python scripts/eaa_design_uuid.py --list
   ```

2. Check the design root path:
   ```bash
   cat .claude/architect/patterns.md | grep design_root
   ```

3. Search for partial UUID:
   ```bash
   grep -r "a1b2c3d4" docs/design/
   ```

---

### 2.2 No UUID in frontmatter

**Error**:
```
ERROR: Document has no UUID in frontmatter: docs/design/specs/auth.md
```

**Cause**: Document exists but lacks UUID field.

**Solution**:

```bash
# Add UUID to the document
python scripts/eaa_design_uuid.py --file docs/design/specs/auth.md --type SPEC
```

---

### 2.3 Invalid frontmatter format

**Error**:
```
ERROR: Document has no frontmatter: docs/design/specs/auth.md
```

**Cause**: Document does not start with `---` YAML frontmatter block.

**Solution**:

Add frontmatter to the document:

```markdown
---
uuid: PROJ-SPEC-20250129-a1b2c3d4
title: "Authentication Service Design"
type: spec
status: draft
created: 2025-01-29
---

# Authentication Service Design
...
```

Or use the UUID script to add it automatically:
```bash
python scripts/eaa_design_uuid.py --file docs/design/specs/auth.md --type SPEC
```

---

## 3. Issue Errors

### 3.1 Issue not found

**Error**:
```
ERROR: Issue #42 not found
```

**Cause**: The specified issue number does not exist.

**Solution**:

1. Verify the issue exists:
   ```bash
   gh issue view 42
   ```

2. Check you're in the correct repository:
   ```bash
   gh repo view
   ```

3. List recent issues:
   ```bash
   gh issue list
   ```

---

### 3.2 Label creation failed

**Error**:
```
WARNING: Failed to add labels: label "design:spec" not found
```

**Cause**: The label does not exist in the repository.

**Solution**:

Create the missing labels:

```bash
# Create design labels
gh label create "design" --color "0052CC" --description "Design documents"
gh label create "design:spec" --color "1D76DB" --description "Specification documents"
gh label create "design:plan" --color "5319E7" --description "Planning documents"
gh label create "design:adr" --color "B60205" --description "Architecture Decision Records"

# Create status labels
gh label create "status:draft" --color "FBCA04" --description "Draft status"
gh label create "status:review" --color "C5DEF5" --description "Under review"
gh label create "status:approved" --color "0E8A16" --description "Approved"
gh label create "status:implementing" --color "006B75" --description "Being implemented"
gh label create "status:completed" --color "0E8A16" --description "Completed"
gh label create "status:deprecated" --color "D93F0B" --description "Deprecated"
```

---

### 3.3 Comment failed

**Error**:
```
WARNING: Failed to add comment to #42: HTTP 422: ...
```

**Cause**: Comment body is too long or contains invalid characters.

**Solution**:

The scripts automatically truncate long content. If you still get this error:

1. Check for special characters in the document
2. Try attaching a shorter document
3. Use dry-run to preview the comment:
   ```bash
   python scripts/eaa_github_attach_document.py --uuid PROJ-SPEC-... --issue 42 --dry-run
   ```

---

## 4. Sync Errors

### 4.1 No linked issues

**Error**:
```
ERROR: Document has no linked issues. Use --issue to specify one.
```

**Cause**: Document frontmatter does not have `related_issues` field.

**Solution**:

Either specify the issue explicitly:
```bash
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --issue 42
```

Or first create/attach to an issue:
```bash
python scripts/eaa_github_issue_create.py --uuid PROJ-SPEC-...
```

---

### 4.2 Status label conflict

**Symptom**: Multiple status labels appear on the issue.

**Cause**: Label removal failed or manual label editing.

**Solution**:

1. Manually clean up labels:
   ```bash
   gh issue edit 42 --remove-label "status:draft,status:review"
   gh issue edit 42 --add-label "status:approved"
   ```

2. Re-run sync:
   ```bash
   python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-...
   ```

---

### 4.3 Batch sync failures

**Error**:
```
Synced 3 issue(s)
WARNING: Failed to sync issue #45
```

**Cause**: One or more issues in batch sync failed.

**Solution**:

1. Run sync individually for failed issues:
   ```bash
   python scripts/eaa_github_sync_status.py --uuid <failed-uuid> --dry-run
   ```

2. Check specific issue:
   ```bash
   gh issue view 45
   ```

3. Verify the issue exists and you have permission to edit it
