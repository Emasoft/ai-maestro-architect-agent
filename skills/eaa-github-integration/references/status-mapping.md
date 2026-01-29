# Status to Label Mapping Reference

## Table of Contents

- 1. Design Status Values
- 2. GitHub Label Mapping
- 3. Valid Status Transitions
- 4. Label Naming Convention
- 5. Automated Label Management
- 6. Manual Label Operations

---

## 1. Design Status Values

Design documents use these status values in frontmatter:

| Status | Description | Terminal? |
|--------|-------------|-----------|
| `draft` | Initial creation, work in progress | No |
| `review` | Under stakeholder review | No |
| `approved` | Approved for implementation | No |
| `implementing` | Being implemented | No |
| `implemented` | Implementation complete | No |
| `completed` | Full lifecycle complete | No |
| `deprecated` | No longer valid/used | Yes |
| `superseded` | Replaced by newer version | Yes |
| `archived` | Historical reference only | Yes |

---

## 2. GitHub Label Mapping

### Status Labels

| Design Status | GitHub Label | Label Color |
|---------------|--------------|-------------|
| `draft` | `status:draft` | `#FBCA04` (yellow) |
| `review` | `status:review` | `#C5DEF5` (light blue) |
| `approved` | `status:approved` | `#0E8A16` (green) |
| `implementing` | `status:implementing` | `#006B75` (teal) |
| `implemented` | `status:implemented` | `#0E8A16` (green) |
| `completed` | `status:completed` | `#0E8A16` (green) |
| `deprecated` | `status:deprecated` | `#D93F0B` (red) |
| `superseded` | `status:superseded` | `#D93F0B` (red) |
| `archived` | `status:archived` | `#5319E7` (purple) |

### Type Labels

| Document Type | GitHub Label | Label Color |
|---------------|--------------|-------------|
| `spec` | `design:spec` | `#1D76DB` (blue) |
| `plan` | `design:plan` | `#5319E7` (purple) |
| `adr` | `design:adr` | `#B60205` (dark red) |
| any | `design` | `#0052CC` (corporate blue) |

---

## 3. Valid Status Transitions

```
         +--> deprecated
         |
draft ---+--> review ----+--> approved ---+--> implementing ---+--> implemented
         |               |                |                    |
         |               |                +--> deprecated      +--> completed
         |               |                |                    |
         |               +--> draft       +--> superseded      +--> deprecated
         |                                                     |
         +--------------------------------------------------> superseded
```

### Transition Rules

| From | Allowed To |
|------|------------|
| `draft` | `review`, `deprecated` |
| `review` | `draft`, `approved`, `deprecated` |
| `approved` | `implementing`, `deprecated`, `superseded` |
| `implementing` | `implemented`, `deprecated`, `superseded` |
| `implemented` | `completed`, `deprecated`, `superseded` |
| `completed` | `archived`, `deprecated` |
| `deprecated` | (terminal) |
| `superseded` | (terminal) |
| `archived` | (terminal) |

---

## 4. Label Naming Convention

### Format

```
<category>:<value>
```

### Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| `status` | Lifecycle status | `status:draft`, `status:approved` |
| `design` | Document type | `design:spec`, `design:adr` |
| `priority` | Priority level | `priority:high`, `priority:low` |
| `module` | Module/component | `module:auth`, `module:api` |

### Rules

1. Use lowercase for all labels
2. Use colon `:` as separator
3. Use hyphen `-` for multi-word values
4. Keep labels under 50 characters

---

## 5. Automated Label Management

### Sync Behavior

When `eaa_github_sync_status.py` runs:

1. **Reads** current status from design document frontmatter
2. **Gets** current labels from GitHub issue
3. **Identifies** old status labels to remove
4. **Identifies** new status label to add
5. **Updates** issue labels via gh CLI

### Example

Document status changes from `draft` to `review`:

**Before sync**:
- Issue labels: `design`, `design:spec`, `status:draft`

**After sync**:
- Issue labels: `design`, `design:spec`, `status:review`

### Sync with Comment

```bash
python scripts/eaa_github_sync_status.py --uuid PROJ-SPEC-... --comment
```

Adds a comment like:

```markdown
## Design Status Update

**Status**: `review`
**Description**: Design is under review
**Design UUID**: `PROJ-SPEC-20250129-a1b2c3d4`
**Updated**: 2025-01-29 14:30

---
*Synchronized from design document*
```

---

## 6. Manual Label Operations

### Create All Labels

```bash
# Design category
gh label create "design" --color "0052CC" --description "Design documents"
gh label create "design:spec" --color "1D76DB" --description "Specification"
gh label create "design:plan" --color "5319E7" --description "Planning document"
gh label create "design:adr" --color "B60205" --description "Architecture Decision Record"

# Status category
gh label create "status:draft" --color "FBCA04" --description "Draft"
gh label create "status:review" --color "C5DEF5" --description "Under review"
gh label create "status:approved" --color "0E8A16" --description "Approved"
gh label create "status:implementing" --color "006B75" --description "Implementing"
gh label create "status:implemented" --color "0E8A16" --description "Implemented"
gh label create "status:completed" --color "0E8A16" --description "Completed"
gh label create "status:deprecated" --color "D93F0B" --description "Deprecated"
gh label create "status:superseded" --color "D93F0B" --description "Superseded"
gh label create "status:archived" --color "5319E7" --description "Archived"
```

### List Labels

```bash
gh label list
```

### Update Label

```bash
gh label edit "status:draft" --color "FFA500" --description "Work in progress"
```

### Delete Label

```bash
gh label delete "status:old" --yes
```

### Add Label to Issue

```bash
gh issue edit 42 --add-label "status:approved"
```

### Remove Label from Issue

```bash
gh issue edit 42 --remove-label "status:draft"
```
