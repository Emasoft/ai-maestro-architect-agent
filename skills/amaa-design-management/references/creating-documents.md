# Creating Documents

This document explains how to create new design documents using the `eia_design_create.py` script.

## Contents

- 3.1 Basic Document Creation
- 3.2 Required Arguments
- 3.3 Optional Fields (author, description)
- 3.4 Custom Filenames
- 3.5 Post-Creation Validation
- 3.6 Creation Error Handling
- 3.7 Script Reference

---

## 3.1 Basic Document Creation

The simplest way to create a design document:

```bash
python scripts/eia_design_create.py --type pdr --title "My Design Document"
```

**What happens:**
1. A unique UUID is generated (e.g., GUUID-20250129-0001)
2. The title is converted to a filename (my-design-document.md)
3. The file is created in the correct subdirectory (design/pdr/)
4. The template is populated with the title
5. The created document is validated

**Output (JSON format):**
```json
{
  "success": true,
  "file_path": "design/pdr/my-design-document.md",
  "uuid": "GUUID-20250129-0001",
  "title": "My Design Document",
  "type": "pdr",
  "status": "draft",
  "created": "2025-01-29",
  "validation": {
    "valid": true,
    "errors": [],
    "warnings": []
  }
}
```

---

## 3.2 Required Arguments

Two arguments are always required:

| Argument | Description | Example |
|----------|-------------|---------|
| `--type` | Document type (pdr, spec, feature, decision, architecture, template) | `--type feature` |
| `--title` | Document title (used in frontmatter and filename) | `--title "OAuth Support"` |

**Examples for each type:**

```bash
# Product Design Review
python scripts/eia_design_create.py --type pdr --title "User Authentication System"

# Technical Specification
python scripts/eia_design_create.py --type spec --title "REST API v2 Specification"

# Feature Document
python scripts/eia_design_create.py --type feature --title "OAuth Login Feature"

# Architecture Decision Record
python scripts/eia_design_create.py --type decision --title "Use PostgreSQL for Primary Database"

# Architecture Document
python scripts/eia_design_create.py --type architecture --title "Payment Processing Architecture"

# Template
python scripts/eia_design_create.py --type template --title "Sprint Retrospective Template"
```

---

## 3.3 Optional Fields

### Author

Add an author name to the frontmatter:

```bash
python scripts/eia_design_create.py \
  --type pdr \
  --title "Authentication System" \
  --author "John Smith"
```

**Resulting frontmatter:**
```yaml
---
uuid: GUUID-20250129-0001
title: "Authentication System"
type: pdr
status: draft
created: 2025-01-29
updated: 2025-01-29
author: "John Smith"
---
```

### Description

Add a brief description:

```bash
python scripts/eia_design_create.py \
  --type decision \
  --title "Database Selection" \
  --description "ADR for choosing between PostgreSQL and MongoDB"
```

**Resulting frontmatter:**
```yaml
---
uuid: GUUID-20250129-0002
title: "Database Selection"
type: decision
status: draft
created: 2025-01-29
updated: 2025-01-29
description: "ADR for choosing between PostgreSQL and MongoDB"
---
```

### Combining Options

All optional fields can be combined:

```bash
python scripts/eia_design_create.py \
  --type feature \
  --title "OAuth 2.0 Integration" \
  --author "Jane Doe" \
  --description "Implement OAuth 2.0 login with Google and GitHub providers"
```

---

## 3.4 Custom Filenames

By default, the filename is derived from the title. Use `--filename` to override:

```bash
python scripts/eia_design_create.py \
  --type spec \
  --title "REST API Version 2.0 Specification" \
  --filename "api-v2-spec"
```

**Result:**
- File created at: `design/spec/api-v2-spec.md`
- Title in frontmatter: "REST API Version 2.0 Specification"

**Filename rules:**
1. Converted to lowercase
2. Non-alphanumeric characters replaced with hyphens
3. Leading/trailing hyphens removed
4. Multiple hyphens collapsed to single hyphen

**Examples:**
| Input | Resulting Filename |
|-------|-------------------|
| "API v2 Spec" | api-v2-spec.md |
| "OAuth 2.0" | oauth-2-0.md |
| "  My Document  " | my-document.md |
| "Test---Doc" | test-doc.md |

---

## 3.5 Post-Creation Validation

Every created document is automatically validated. The validation result is included in the output:

```json
{
  "success": true,
  "validation": {
    "valid": true,
    "errors": [],
    "warnings": []
  }
}
```

**If validation fails:**
```json
{
  "success": false,
  "validation": {
    "valid": false,
    "errors": ["Missing required field: uuid"],
    "warnings": []
  }
}
```

**Manual validation:**
```bash
# Validate the created file
python scripts/eia_design_validate.py design/pdr/my-document.md
```

---

## 3.6 Creation Error Handling

### File Already Exists

If a file with the generated name already exists, the script appends the UUID sequence number:

```bash
# First creation
python scripts/eia_design_create.py --type pdr --title "My Design"
# Creates: design/pdr/my-design.md

# Second creation with same title
python scripts/eia_design_create.py --type pdr --title "My Design"
# Creates: design/pdr/my-design-0002.md
```

### Invalid Type

```bash
python scripts/eia_design_create.py --type invalid --title "Test"
```

**Output:**
```json
{
  "success": false,
  "error": "Invalid type 'invalid'. Valid types: pdr, spec, feature, decision, architecture, template"
}
```

### Permission Errors

If the script cannot write to the design directory:

```json
{
  "success": false,
  "error": "Failed to write file: [Errno 13] Permission denied: 'design/pdr/my-doc.md'"
}
```

**Solution:**
```bash
# Check directory permissions
ls -la design/

# Fix permissions if needed
chmod 755 design/pdr/
```

### Empty Title

```bash
python scripts/eia_design_create.py --type pdr --title ""
```

The script will generate a fallback filename using the UUID sequence number.

---

## 3.7 Script Reference

### Full Command Syntax

```bash
python scripts/eia_design_create.py \
  --type TYPE \
  --title TITLE \
  [--author AUTHOR] \
  [--description DESCRIPTION] \
  [--filename FILENAME] \
  [--design-dir PATH] \
  [--format {json,text}]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--type` | Yes | Document type: pdr, spec, feature, decision, architecture, template |
| `--title` | Yes | Document title (appears in frontmatter) |
| `--author` | No | Author name |
| `--description` | No | Brief description |
| `--filename` | No | Custom filename (without .md extension) |
| `--design-dir` | No | Path to design directory (default: ../design from script) |
| `--format` | No | Output format: json (default) or text |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Document created successfully |
| 1 | Creation failed |

### Examples

```bash
# Minimal creation
python scripts/eia_design_create.py --type pdr --title "Auth System"

# With all options
python scripts/eia_design_create.py \
  --type feature \
  --title "OAuth Support" \
  --author "Dev Team" \
  --description "OAuth 2.0 with multiple providers" \
  --filename "oauth-v2" \
  --format text

# Custom design directory
python scripts/eia_design_create.py \
  --type spec \
  --title "API Spec" \
  --design-dir /path/to/project/design
```

---

## See Also

- [Document Types](document-types.md) - Which type to choose for your document
- [UUID Specification](uuid-specification.md) - How UUIDs are generated
- [Validating Documents](validating-documents.md) - How to validate created documents
