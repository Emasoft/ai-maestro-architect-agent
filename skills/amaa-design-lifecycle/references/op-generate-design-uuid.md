---
operation: generate-design-uuid
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-design-lifecycle
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Generate Design UUID


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Understand the UUID Format](#step-1-understand-the-uuid-format)
  - [Step 2: Generate UUID Using Script](#step-2-generate-uuid-using-script)
  - [Step 3: Verify UUID Uniqueness](#step-3-verify-uuid-uniqueness)
  - [Step 4: Manual UUID Generation (Fallback)](#step-4-manual-uuid-generation-fallback)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Generate Design UUID](#example-generate-design-uuid)
  - [Example: UUID in Document Frontmatter](#example-uuid-in-document-frontmatter)
  - [Example: UUID in Design Index](#example-uuid-in-design-index)
- [UUID Format Rules](#uuid-format-rules)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Creating a new design document that needs a unique identifier
- Registering a design in the design index
- Linking design documents to implementation artifacts
- Ensuring traceability from requirements to implementation

## Prerequisites

- Python 3.8+ installed
- Access to the UUID generation script at `scripts/eaa_design_uuid.py`
- Understanding of the UUID format requirements

## Procedure

### Step 1: Understand the UUID Format

Design UUIDs follow the pattern:

```
<type>-<feature-slug>-<YYYYMMDD>-<unique-id>
```

Components:
- **type**: Document type (design, pdr, spec, feature, decision, architecture)
- **feature-slug**: Kebab-case name describing the feature
- **YYYYMMDD**: Creation date in ISO format
- **unique-id**: 6-character alphanumeric unique identifier

Example: `design-user-authentication-20260130-7f3a2b`

### Step 2: Generate UUID Using Script

Use the generation script to create a unique identifier:

```bash
python scripts/eaa_design_uuid.py --type design
```

For a specific feature name:

```bash
python scripts/eaa_design_uuid.py --type design --name "user-authentication"
```

### Step 3: Verify UUID Uniqueness

The script automatically checks uniqueness against the design index:

```bash
python scripts/eaa_design_uuid.py --type design --verify
```

### Step 4: Manual UUID Generation (Fallback)

If the script is unavailable, generate manually:

1. Determine the type: `design`
2. Create the feature slug: lowercase, kebab-case, no special characters
3. Get today's date: `YYYYMMDD` format
4. Generate unique suffix: 6 random alphanumeric characters

```bash
# Manual generation example
DATE=$(date +%Y%m%d)
SUFFIX=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-z0-9' | head -c 6)
echo "design-feature-name-${DATE}-${SUFFIX}"
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify the document type (design, pdr, spec, etc.)
- [ ] Determine the feature name for the slug
- [ ] Run UUID generation script
- [ ] Verify UUID is unique in design index
- [ ] Record UUID in design document frontmatter
- [ ] Register UUID in design index

## Examples

### Example: Generate Design UUID

```bash
# Basic generation
python scripts/eaa_design_uuid.py --type design
# Output: design-20260130-abc123

# With feature name
python scripts/eaa_design_uuid.py --type design --name "payment-gateway"
# Output: design-payment-gateway-20260130-def456

# For a PDR document
python scripts/eaa_design_uuid.py --type pdr --name "api-v2-migration"
# Output: pdr-api-v2-migration-20260130-ghi789

# Verify uniqueness
python scripts/eaa_design_uuid.py --type design --name "payment-gateway" --verify
# Output: UUID is unique. Ready to use.
```

### Example: UUID in Document Frontmatter

```yaml
---
uuid: design-payment-gateway-20260130-def456
title: "Payment Gateway Integration Design"
status: draft
created: 2026-01-30
updated: 2026-01-30
---
```

### Example: UUID in Design Index

```json
{
  "designs": [
    {
      "uuid": "design-payment-gateway-20260130-def456",
      "title": "Payment Gateway Integration Design",
      "status": "draft",
      "created": "2026-01-30",
      "path": "docs_dev/design/design-payment-gateway-20260130-def456.md"
    }
  ]
}
```

## UUID Format Rules

| Rule | Description | Valid Example | Invalid Example |
|------|-------------|---------------|-----------------|
| Type prefix | Must be valid document type | `design-...` | `random-...` |
| Feature slug | Lowercase, kebab-case | `user-auth` | `UserAuth`, `user_auth` |
| Date format | YYYYMMDD | `20260130` | `2026-01-30`, `01302026` |
| Unique suffix | 6 alphanumeric | `abc123` | `abc`, `abcdefgh` |
| No spaces | Entire UUID has no spaces | `design-api-20260130-abc123` | `design api 20260130 abc123` |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Script not found | Missing eaa_design_uuid.py | Check script path; restore from backup |
| UUID collision | Generated UUID already exists | Regenerate with different suffix |
| Invalid type | Unknown document type | Use valid type: design, pdr, spec, feature, decision, architecture |
| Invalid characters | Special characters in feature name | Use only lowercase letters, numbers, hyphens |
| Index not found | design/requirements/index.json missing | Create index file first |

## Related Operations

- [op-create-design-document.md](op-create-design-document.md) - Uses UUID during document creation
- [op-manage-state-transitions.md](op-manage-state-transitions.md) - UUID required for state management
