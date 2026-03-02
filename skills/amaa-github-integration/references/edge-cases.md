---
topic: edge-cases
parent-skill: amaa-github-integration
---

# Edge Cases

## Issue Already Exists

**Situation**: Design document already has `related_issues` in frontmatter.

**Detection**: Script shows warning:
```
WARNING: Document already linked to issues: ["#42"]
```

**Resolution Options**:

1. **Attach to existing issue instead**:
   ```bash
   python scripts/amaa_github_attach_document.py --uuid PROJ-SPEC-... --issue 42
   ```

2. **Sync status to existing issue**:
   ```bash
   python scripts/amaa_github_sync_status.py --uuid PROJ-SPEC-...
   ```

3. **Create additional issue anyway** (if truly needed):
   - Manually create issue via `gh issue create`
   - Manually update design document frontmatter

---

## Design Has No UUID

**Situation**: Design document does not have `uuid` field in frontmatter.

**Detection**: Script shows error:
```
ERROR: Document has no UUID in frontmatter: docs/design/specs/auth.md
```

**Resolution**:

1. **Generate UUID for the document**:
   ```bash
   python scripts/amaa_design_uuid.py --file docs/design/specs/auth.md --type SPEC
   ```

2. **Verify UUID was added**:
   ```bash
   head -20 docs/design/specs/auth.md
   ```

3. **Retry the GitHub integration**:
   ```bash
   python scripts/amaa_github_issue_create.py --uuid <new-uuid>
   ```

---

## gh CLI Not Available

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
