---
operation: generate-design-uuid
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-github-integration
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Generate UUID for Design Document


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Verify Document Lacks UUID](#step-1-verify-document-lacks-uuid)
  - [Step 2: Generate UUID](#step-2-generate-uuid)
  - [Step 3: Verify UUID Was Added](#step-3-verify-uuid-was-added)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Generate UUID for New Spec](#example-generate-uuid-for-new-spec)
  - [Example: Different Document Types](#example-different-document-types)
- [UUID Format](#uuid-format)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Trigger this operation when:
- Creating a new design document that needs GitHub integration
- Existing design document lacks UUID in frontmatter
- GitHub integration scripts report "Document has no UUID" error

## Prerequisites

- Design document file exists
- Write access to the design document
- Knowledge of the design document type (SPEC, ADR, RFC, etc.)

## Procedure

### Step 1: Verify Document Lacks UUID

```bash
head -20 docs/design/specs/<design-file>.md
```

Check if frontmatter already contains `uuid:` field.

### Step 2: Generate UUID

```bash
python scripts/eaa_design_uuid.py --file docs/design/specs/auth-service.md --type SPEC
```

Document types:
- `SPEC` - Specification document
- `ADR` - Architecture Decision Record
- `RFC` - Request for Comments
- `GUIDE` - Implementation guide
- `PLAN` - Project plan

### Step 3: Verify UUID Was Added

```bash
head -20 docs/design/specs/auth-service.md
```

Expected frontmatter now includes:
```yaml
uuid: PROJ-SPEC-20250129-a1b2c3d4
```

## Checklist

Copy this checklist and track your progress:

- [ ] Verify document exists at specified path
- [ ] Check if document already has UUID: `head -20 <file>`
- [ ] If UUID exists, skip this operation
- [ ] Determine document type: SPEC, ADR, RFC, GUIDE, or PLAN
- [ ] Generate UUID: `python scripts/eaa_design_uuid.py --file <path> --type <TYPE>`
- [ ] Verify UUID was added to frontmatter
- [ ] Proceed with GitHub integration operations

## Examples

### Example: Generate UUID for New Spec

```bash
# Check current frontmatter
head -20 docs/design/specs/auth-service.md

# Output:
# ---
# title: Auth Service Architecture
# status: draft
# author: architect-agent
# ---

# Generate UUID
python scripts/eaa_design_uuid.py --file docs/design/specs/auth-service.md --type SPEC

# Output:
# GENERATED: UUID PROJ-SPEC-20250129-a1b2c3d4
# UPDATED: docs/design/specs/auth-service.md

# Verify
head -20 docs/design/specs/auth-service.md

# Output:
# ---
# title: Auth Service Architecture
# uuid: PROJ-SPEC-20250129-a1b2c3d4
# status: draft
# author: architect-agent
# ---
```

### Example: Different Document Types

```bash
# ADR (Architecture Decision Record)
python scripts/eaa_design_uuid.py --file docs/design/adrs/adr-001.md --type ADR
# Generated: PROJ-ADR-20250129-b2c3d4e5

# RFC (Request for Comments)
python scripts/eaa_design_uuid.py --file docs/design/rfcs/rfc-api-v2.md --type RFC
# Generated: PROJ-RFC-20250129-c3d4e5f6
```

## UUID Format

The generated UUID follows this pattern:
```
PROJ-<TYPE>-<DATE>-<RANDOM>
```

Where:
- `PROJ` - Project identifier (configurable)
- `TYPE` - Document type (SPEC, ADR, RFC, GUIDE, PLAN)
- `DATE` - Creation date in YYYYMMDD format
- `RANDOM` - 8-character random hex string

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ERROR: File not found` | Path does not exist | Verify file path |
| `ERROR: Invalid document type` | Unknown type specified | Use one of: SPEC, ADR, RFC, GUIDE, PLAN |
| `WARNING: Document already has UUID` | UUID already exists | No action needed; use existing UUID |
| `ERROR: Cannot write to file` | Permission denied | Check file permissions |
| `ERROR: No frontmatter found` | Missing YAML block | Add `---` delimiters at top of file |

## Related Operations

- [op-create-issue-from-design.md](op-create-issue-from-design.md) - After generating UUID, create GitHub issue
- [op-attach-design-to-issue.md](op-attach-design-to-issue.md) - After generating UUID, attach to existing issue
