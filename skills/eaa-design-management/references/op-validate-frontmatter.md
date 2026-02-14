---
operation: validate-frontmatter
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-design-management
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Validate Document Frontmatter


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Understand Required Frontmatter](#step-1-understand-required-frontmatter)
  - [Step 2: Validate Single Document](#step-2-validate-single-document)
  - [Step 3: Validate All Documents](#step-3-validate-all-documents)
  - [Step 4: Interpret Validation Output](#step-4-interpret-validation-output)
  - [Step 5: Fix Validation Errors](#step-5-fix-validation-errors)
  - [Step 6: Verify Fixes](#step-6-verify-fixes)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Validate Single Document](#example-1-validate-single-document)
  - [Example 2: Validate All with Type Filter](#example-2-validate-all-with-type-filter)
  - [Example 3: JSON Output for CI/CD](#example-3-json-output-for-cicd)
  - [Example 4: Common Validation Errors and Fixes](#example-4-common-validation-errors-and-fixes)
- [Validation Rules](#validation-rules)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Checking a document for frontmatter compliance before review
- Validating all design documents as part of a quality check
- Troubleshooting document parsing issues
- Ensuring documents meet the required schema
- Running automated validation in CI/CD pipelines

## Prerequisites

- Python 3.10 or higher installed
- Access to the `scripts/eaa_design_validate.py` script
- Design documents exist in the `design/` directory structure
- Understanding of required frontmatter fields

## Procedure

### Step 1: Understand Required Frontmatter

All design documents must have these required fields:

```yaml
---
uuid: GUUID-YYYYMMDD-NNNN          # Required: Unique identifier
title: "Document Title"            # Required: Human-readable title
status: draft                      # Required: Current status
created: YYYY-MM-DD                # Required: Creation date
updated: YYYY-MM-DD                # Required: Last update date
---
```

**Optional fields:**
```yaml
---
type: pdr                          # Optional: Document type
author: "Author Name"              # Optional: Author
description: "Brief description"   # Optional: Summary
tags: [tag1, tag2]                 # Optional: Categorization
related: [GUUID-..., GUUID-...]    # Optional: Related documents
---
```

### Step 2: Validate Single Document

To validate a specific document:

```bash
python scripts/eaa_design_validate.py design/pdr/my-document.md
```

**Output on success:**
```
Validating: design/pdr/my-document.md
[PASS] Frontmatter present
[PASS] Required field: uuid
[PASS] Required field: title
[PASS] Required field: status
[PASS] Required field: created
[PASS] Required field: updated
[PASS] UUID format valid
[PASS] Date format valid (created)
[PASS] Date format valid (updated)

Validation passed: 0 errors, 0 warnings
```

### Step 3: Validate All Documents

To validate all documents in the design directory:

```bash
python scripts/eaa_design_validate.py --all
```

**Filter by type:**
```bash
python scripts/eaa_design_validate.py --all --type pdr
```

### Step 4: Interpret Validation Output

**Error levels:**
| Level | Meaning | Action Required |
|-------|---------|-----------------|
| ERROR | Critical issue | Must fix before proceeding |
| WARNING | Non-critical issue | Should fix, but not blocking |
| INFO | Informational | Optional improvement |

**Example output with errors:**
```
Validating: design/pdr/broken-document.md
[ERROR] Line 3: Missing required field 'uuid'
[ERROR] Line 5: Invalid date format for 'created': expected YYYY-MM-DD
[WARNING] Line 8: Empty 'author' field

Validation failed: 2 errors, 1 warning
```

### Step 5: Fix Validation Errors

Address each error in order:

1. **Missing required field**: Add the field to frontmatter
2. **Invalid date format**: Use YYYY-MM-DD format
3. **Invalid UUID format**: Regenerate using proper format
4. **Malformed YAML**: Fix syntax issues in frontmatter block

### Step 6: Verify Fixes

Re-run validation after fixing:

```bash
python scripts/eaa_design_validate.py design/pdr/fixed-document.md
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify document(s) to validate
- [ ] Run validation script
- [ ] Review all errors and warnings
- [ ] Fix ERROR level issues first
- [ ] Fix WARNING level issues
- [ ] Re-run validation to confirm fixes
- [ ] Document passes validation

## Examples

### Example 1: Validate Single Document

```bash
python scripts/eaa_design_validate.py design/pdr/GUUID-20260130-0001-auth-design.md

# Output:
# Validating: design/pdr/GUUID-20260130-0001-auth-design.md
# [PASS] Frontmatter present
# [PASS] Required field: uuid (GUUID-20260130-0001)
# [PASS] Required field: title (User Authentication Design)
# [PASS] Required field: status (draft)
# [PASS] Required field: created (2026-01-30)
# [PASS] Required field: updated (2026-01-30)
# [PASS] UUID format valid
# [PASS] Date formats valid
#
# Validation passed: 0 errors, 0 warnings
```

### Example 2: Validate All with Type Filter

```bash
python scripts/eaa_design_validate.py --all --type pdr --verbose

# Output:
# Scanning: design/pdr/
# Found: 5 documents
#
# [1/5] GUUID-20260128-0001-user-auth.md
#   [PASS] All checks passed
#
# [2/5] GUUID-20260129-0002-payment.md
#   [PASS] All checks passed
#
# [3/5] GUUID-20260130-0003-shipping.md
#   [ERROR] Missing required field: status
#   [WARNING] Empty description
#
# [4/5] GUUID-20260130-0004-notifications.md
#   [PASS] All checks passed
#
# [5/5] GUUID-20260130-0005-reporting.md
#   [PASS] All checks passed
#
# Summary: 5 files validated, 4 passed, 1 failed
# Errors: 1, Warnings: 1
```

### Example 3: JSON Output for CI/CD

```bash
python scripts/eaa_design_validate.py --all --format json

# Output:
# {
#   "total": 5,
#   "passed": 4,
#   "failed": 1,
#   "errors": [
#     {
#       "file": "design/pdr/GUUID-20260130-0003-shipping.md",
#       "line": 3,
#       "level": "ERROR",
#       "message": "Missing required field: status"
#     }
#   ],
#   "warnings": [
#     {
#       "file": "design/pdr/GUUID-20260130-0003-shipping.md",
#       "line": 7,
#       "level": "WARNING",
#       "message": "Empty description"
#     }
#   ]
# }
```

### Example 4: Common Validation Errors and Fixes

**Error: Missing required field**
```yaml
# Before (missing uuid)
---
title: "My Design"
status: draft
---

# After (uuid added)
---
uuid: GUUID-20260130-0001
title: "My Design"
status: draft
created: 2026-01-30
updated: 2026-01-30
---
```

**Error: Invalid date format**
```yaml
# Before (wrong format)
---
created: January 30, 2026
---

# After (correct format)
---
created: 2026-01-30
---
```

**Error: Invalid UUID format**
```yaml
# Before (wrong format)
---
uuid: 12345
---

# After (correct GUUID format)
---
uuid: GUUID-20260130-0001
---
```

## Validation Rules

| Rule | Check | Valid Example |
|------|-------|---------------|
| UUID format | GUUID-YYYYMMDD-NNNN | GUUID-20260130-0001 |
| Date format | YYYY-MM-DD | 2026-01-30 |
| Status values | draft, review, approved, implemented, deprecated, rejected | draft |
| Type values | pdr, spec, feature, decision, architecture, template | pdr |
| Tags format | YAML list | [auth, security] |
| Related format | YAML list of UUIDs | [GUUID-20260128-0001] |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No frontmatter found | Missing YAML block | Add frontmatter block between `---` delimiters |
| Malformed YAML | Syntax error in frontmatter | Check for indentation, colons, quotes |
| Invalid UUID format | UUID doesn't match pattern | Use GUUID-YYYYMMDD-NNNN format |
| Invalid date format | Date not YYYY-MM-DD | Use ISO date format |
| Unknown status value | Invalid status | Use: draft, review, approved, implemented, deprecated, rejected |
| File not found | Path incorrect | Verify file path and name |
| Encoding error | Non-UTF-8 encoding | Convert file to UTF-8 |

## Related Operations

- [op-create-document-from-template.md](op-create-document-from-template.md) - Create valid documents
- [op-search-design-documents.md](op-search-design-documents.md) - Find documents to validate
- [op-generate-guuid.md](op-generate-guuid.md) - Generate valid UUIDs
