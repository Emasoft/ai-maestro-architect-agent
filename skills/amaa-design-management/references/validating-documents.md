# Validating Documents

This document explains how to validate design documents using the `eia_design_validate.py` script.

## Contents

- 5.1 Single File Validation
- 5.2 Bulk Validation
- 5.3 Understanding Errors
- 5.4 Understanding Warnings
- 5.5 Error Resolution
- 5.6 Required Frontmatter Fields
- 5.7 Script Reference

---

## 5.1 Single File Validation

Validate a specific document:

```bash
python scripts/eia_design_validate.py design/pdr/auth-system.md
```

**Output (JSON format):**
```json
{
  "valid": true,
  "file_path": "design/pdr/auth-system.md",
  "errors": [],
  "warnings": []
}
```

**Output (text format with --format text):**
```
[VALID] design/pdr/auth-system.md
```

**Invalid document example:**
```json
{
  "valid": false,
  "file_path": "design/pdr/broken-doc.md",
  "errors": [
    "Frontmatter: Missing required field 'uuid'",
    "Line 5: Invalid status 'pending'. Valid values: draft, review, approved, implemented, deprecated, rejected"
  ],
  "warnings": [
    "Frontmatter: Missing recommended field 'description'"
  ]
}
```

---

## 5.2 Bulk Validation

### Validate All Documents

```bash
python scripts/eia_design_validate.py --all
```

**Output:**
```json
{
  "valid": false,
  "results": [
    {"valid": true, "file_path": "design/pdr/auth-system.md", "errors": [], "warnings": []},
    {"valid": false, "file_path": "design/pdr/broken.md", "errors": ["..."], "warnings": []}
  ],
  "summary": {
    "total": 10,
    "valid": 8,
    "invalid": 2,
    "total_errors": 3,
    "total_warnings": 5
  }
}
```

### Validate by Type

```bash
# Validate all PDR documents
python scripts/eia_design_validate.py --all --type pdr

# Validate all specifications
python scripts/eia_design_validate.py --all --type spec
```

### Verbose Text Output

```bash
python scripts/eia_design_validate.py --all --format text --verbose
```

**Output:**
```
Design Document Validation Summary
==================================================
Total documents: 10
Valid: 8
Invalid: 2
Total errors: 3
Total warnings: 5

[INVALID] design/pdr/broken.md
  ERROR: Frontmatter: Missing required field 'uuid'
  ERROR: Line 5: Invalid status 'pending'
  WARNING: Frontmatter: Missing recommended field 'description'

[VALID] design/pdr/auth-system.md
  WARNING: Frontmatter: Missing recommended field 'author'
```

---

## 5.3 Understanding Errors

Errors indicate problems that MUST be fixed. The document will not pass validation until all errors are resolved.

### Common Error Types

| Error | Cause | Fix |
|-------|-------|-----|
| Missing frontmatter opening delimiter | File doesn't start with `---` | Add `---` as first line |
| Missing closing delimiter | No second `---` after frontmatter | Add closing `---` |
| Missing required field 'X' | Required field not in frontmatter | Add the missing field |
| Invalid UUID format | UUID doesn't match GUUID-YYYYMMDD-NNNN | Fix UUID format |
| Invalid status 'X' | Status not in allowed values | Use valid status value |
| Invalid created/updated format | Date not YYYY-MM-DD | Fix date format |

### Error Message Format

Errors include line numbers when possible:

```
Line 3: Invalid UUID format 'bad-uuid'. Expected: GUUID-YYYYMMDD-NNNN
Frontmatter: Missing required field 'title'
```

- `Line N:` - Error on specific line
- `Frontmatter:` - Error in frontmatter section (line unknown)

---

## 5.4 Understanding Warnings

Warnings indicate potential issues that don't prevent validation from passing.

### Common Warning Types

| Warning | Cause | Recommendation |
|---------|-------|----------------|
| Missing recommended field 'X' | Optional but recommended field missing | Add for completeness |
| Type 'X' does not match folder 'Y' | Frontmatter type differs from directory | Align type with directory |
| File does not have .md extension | Wrong file extension | Rename to .md |

### When to Address Warnings

- **Before review**: Fix warnings before submitting for review
- **For completeness**: Add recommended fields for documentation quality
- **Type mismatch**: Fix immediately to maintain organization

---

## 5.5 Error Resolution

### Missing Frontmatter

**Error:**
```
Line 1: Missing frontmatter opening delimiter '---'
```

**Fix:** Add complete frontmatter at the start of the file:

```yaml
---
uuid: GUUID-20250129-0001
title: "Document Title"
status: draft
created: 2025-01-29
updated: 2025-01-29
---
```

### Invalid UUID

**Error:**
```
Line 2: Invalid UUID format 'uuid-123'. Expected: GUUID-YYYYMMDD-NNNN
```

**Fix:** Replace with valid GUUID format:

```yaml
# Wrong
uuid: uuid-123

# Correct
uuid: GUUID-20250129-0001
```

### Invalid Status

**Error:**
```
Line 4: Invalid status 'pending'. Valid values: draft, review, approved, implemented, deprecated, rejected
```

**Fix:** Use a valid status value:

```yaml
# Wrong
status: pending

# Correct
status: draft
```

### Invalid Date Format

**Error:**
```
Line 5: Invalid created format '01/29/2025'. Expected: YYYY-MM-DD
```

**Fix:** Use ISO date format:

```yaml
# Wrong
created: 01/29/2025

# Correct
created: 2025-01-29
```

### Missing Required Fields

**Error:**
```
Frontmatter: Missing required field 'title'
```

**Fix:** Add all required fields:

```yaml
---
uuid: GUUID-20250129-0001
title: "My Document Title"    # Add this
status: draft
created: 2025-01-29
updated: 2025-01-29
---
```

---

## 5.6 Required Frontmatter Fields

Every design document MUST have these fields:

| Field | Format | Example |
|-------|--------|---------|
| `uuid` | GUUID-YYYYMMDD-NNNN | `GUUID-20250129-0001` |
| `title` | Quoted string | `"Authentication Design"` |
| `status` | draft\|review\|approved\|implemented\|deprecated\|rejected | `draft` |
| `created` | YYYY-MM-DD | `2025-01-29` |
| `updated` | YYYY-MM-DD | `2025-01-29` |

**Minimal valid frontmatter:**
```yaml
---
uuid: GUUID-20250129-0001
title: "Document Title"
status: draft
created: 2025-01-29
updated: 2025-01-29
---
```

**Recommended additional fields:**
```yaml
---
uuid: GUUID-20250129-0001
title: "Document Title"
type: pdr
status: draft
created: 2025-01-29
updated: 2025-01-29
author: "Author Name"
description: "Brief description of the document"
---
```

---

## 5.7 Script Reference

### Full Command Syntax

```bash
python scripts/eia_design_validate.py FILE
python scripts/eia_design_validate.py --all [--type TYPE]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `FILE` | Path to document to validate (single file mode) |
| `--all` | Validate all documents in design directory |
| `--type` | Filter by type when using --all |
| `--design-dir` | Path to design directory (default: ../design from script) |
| `--format` | Output format: json (default) or text |
| `--verbose` | Show warnings in text output |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validated documents are valid |
| 1 | One or more documents have errors |

### Examples

```bash
# Validate single file
python scripts/eia_design_validate.py design/pdr/auth.md

# Validate all with text output
python scripts/eia_design_validate.py --all --format text

# Validate all PDRs with verbose output
python scripts/eia_design_validate.py --all --type pdr --verbose --format text

# Validate with custom design directory
python scripts/eia_design_validate.py --all --design-dir /path/to/design
```

---

## See Also

- [Creating Documents](creating-documents.md) - Create documents with valid frontmatter
- [UUID Specification](uuid-specification.md) - UUID format requirements
- [Troubleshooting](troubleshooting.md) - Common validation issues
