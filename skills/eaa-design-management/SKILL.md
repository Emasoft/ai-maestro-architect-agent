---
name: eaa-design-management
description: "Use when managing design documents. Trigger with design search, validation, or creation requests."
version: 1.0.0
license: Apache-2.0
compatibility: Requires Python 3.10 or higher. Requires AI Maestro installed.
metadata:
  author: Emasoft
agent: eaa-main
context: fork
workflow-instruction: "Step 7"
procedure: "proc-create-design"
---

# Design Document Management

## Overview

This skill provides comprehensive tooling for managing design documents in the `design/` directory hierarchy. It covers creating documents from templates, searching with structured queries, and validating frontmatter compliance.

## Prerequisites

Before using this skill, ensure:
1. Python 3.10 or higher is installed
2. The `design/` directory structure exists in the project root
3. Write access to the design document directories

## Instructions

1. Read the UUID Specification reference to understand the GUUID format
2. Review the Document Types reference to select the appropriate document type for your needs
3. Use the Creating Documents reference to create new design documents with proper frontmatter
4. Use the Searching Documents reference to query and filter existing documents by metadata or content
5. Use the Validating Documents reference to ensure all documents meet frontmatter compliance requirements
6. Consult the Troubleshooting reference if you encounter errors or validation issues

### Checklist

Copy this checklist and track your progress:

- [ ] Read UUID Specification reference (understand GUUID format)
- [ ] Review Document Types reference (select appropriate type: pdr, spec, feature, decision, architecture, template)
- [ ] Create design document using `python scripts/eaa_design_create.py --type <type> --title "<title>"`
- [ ] Verify document was created with proper UUID and frontmatter
- [ ] Search existing documents if needed: `python scripts/eaa_design_search.py --type <type> --status <status>`
- [ ] Validate all documents: `python scripts/eaa_design_validate.py --all`
- [ ] Fix any validation errors reported
- [ ] Consult Troubleshooting reference if errors persist

## Output

| Output Type | Description | Example |
|-------------|-------------|---------|
| Created Document | New markdown file with UUID-based filename and populated frontmatter | `design/pdr/GUUID-20250129-0001-feature-name.md` |
| Search Results JSON | JSON array of matching documents with metadata | `[{"uuid": "GUUID-...", "title": "...", "status": "..."}]` |
| Search Results Table | Human-readable table of matching documents | ASCII table with columns for UUID, Title, Status, Type |
| Validation Report | List of errors and warnings with file paths and line numbers | `ERROR: design/pdr/doc.md:3 - Missing required field 'uuid'` |
| Validation Summary | Count of files validated, errors found, and overall status | `Validated 42 files: 40 passed, 2 failed` |

## Quick Start

**Create a new design document (30 seconds):**
```bash
python scripts/eaa_design_create.py --type pdr --title "My Feature Design"
```

**Search existing documents:**
```bash
python scripts/eaa_design_search.py --type pdr --status approved
```

**Validate all documents:**
```bash
python scripts/eaa_design_validate.py --all
```

## Core Workflow Sequence

This skill teaches design document management in the following order:

1. **UUID Specification** - Understand the GUUID format for unique identification
2. **Document Types** - Learn the six document type categories
3. **Creating Documents** - Use templates to create new documents
4. **Searching Documents** - Query documents by metadata and content
5. **Validating Documents** - Ensure frontmatter compliance
6. **Troubleshooting** - Handle common issues and edge cases

## Reference Documentation Structure

Each reference document focuses on a specific aspect of design management. Read them in order for initial learning, or jump directly to the relevant section when you need specific information.

---

## UUID Format Specification

**Reference:** [references/uuid-specification.md](references/uuid-specification.md)

**Use-Case TOC:**
- When you need to understand the UUID format - UUID Format Definition
- When you need to generate a UUID manually - Manual UUID Generation
- When you need to verify UUID validity - UUID Validation Rules
- When parsing UUIDs from documents - UUID Parsing

**What you will learn:**
- The GUUID-YYYYMMDD-NNNN format specification
- Date component requirements (YYYYMMDD)
- Sequence number rules (NNNN)
- Uniqueness guarantees within a day
- Manual vs automatic UUID generation

---

## Document Types

**Reference:** [references/document-types.md](references/document-types.md)

**Use-Case TOC:**
- When you need to choose a document type - Type Selection Guide
- When creating a Product Design Review - PDR Documents
- When writing technical specifications - Spec Documents
- When documenting features - Feature Documents
- When recording architecture decisions - Decision Documents
- When documenting system architecture - Architecture Documents
- When creating reusable templates - Template Documents

**What you will learn:**
- The six document type categories (pdr, spec, feature, decision, architecture, template)
- When to use each document type
- Directory structure organization
- Type-specific frontmatter fields

---

## Creating Documents

**Reference:** [references/creating-documents.md](references/creating-documents.md)

**Use-Case TOC:**
- When creating a new design document - Basic Document Creation
- When you need a specific author or description - Optional Fields
- When you want a custom filename - Custom Filenames
- When validation fails after creation - Post-Creation Validation
- When the script reports an error - Creation Error Handling

**What you will learn:**
- Using `eaa_design_create.py` with required arguments
- Specifying optional metadata (author, description)
- Automatic UUID generation
- Template population
- File placement in correct subdirectory
- Post-creation validation

---

## Searching Documents

**Reference:** [references/searching-documents.md](references/searching-documents.md)

**Use-Case TOC:**
- When searching by UUID - UUID Search
- When filtering by document type - Type Filter
- When filtering by status - Status Filter
- When searching document content - Keyword Search
- When using file patterns - Glob Pattern Search
- When combining multiple filters - Combined Filters
- When no results are returned - Empty Results Handling

**What you will learn:**
- Using `eaa_design_search.py` with different filters
- Combining multiple search criteria
- Output formats (JSON and table)
- Handling empty results
- Interpreting search results

---

## Validating Documents

**Reference:** [references/validating-documents.md](references/validating-documents.md)

**Use-Case TOC:**
- When validating a single document - Single File Validation
- When validating all documents - Bulk Validation
- When validation reports errors - Understanding Errors
- When validation reports warnings - Understanding Warnings
- When fixing validation issues - Error Resolution

**What you will learn:**
- Using `eaa_design_validate.py` for single and bulk validation
- Required frontmatter fields
- Error messages and line numbers
- Warning vs error severity
- Fixing common validation issues

---

## Error Handling

**Reference:** [references/troubleshooting.md](references/troubleshooting.md)

**Use-Case TOC:**
- If UUID generation fails - UUID Generation Issues
- If document creation fails - Creation Failures
- If search returns no results - Search Issues
- If validation reports malformed frontmatter - Frontmatter Parsing Issues
- If files are in wrong directories - Directory Structure Issues

**What you will learn:**
- Diagnosing common failure modes
- Fixing malformed frontmatter
- Handling file permission issues
- Resolving encoding problems
- Recovery procedures

---

## Quick Reference Commands

**Create documents:**
```bash
# Create a PDR
python scripts/eaa_design_create.py --type pdr --title "Feature Design"

# Create with author
python scripts/eaa_design_create.py --type feature --title "OAuth" --author "John"

# Create with custom filename
python scripts/eaa_design_create.py --type spec --title "API Spec" --filename "api-v2"
```

**Search documents:**
```bash
# Search by UUID
python scripts/eaa_design_search.py --uuid GUUID-20250129-0001

# Search by type and status
python scripts/eaa_design_search.py --type pdr --status approved

# Search by keyword
python scripts/eaa_design_search.py --keyword "authentication"

# Table output
python scripts/eaa_design_search.py --type feature --format table
```

**Validate documents:**
```bash
# Validate single file
python scripts/eaa_design_validate.py design/pdr/my-design.md

# Validate all documents
python scripts/eaa_design_validate.py --all

# Validate specific type
python scripts/eaa_design_validate.py --all --type pdr

# Verbose output with warnings
python scripts/eaa_design_validate.py --all --verbose --format text
```

## Document Status Workflow

| Status | Meaning | Next Steps |
|--------|---------|------------|
| `draft` | Initial creation, work in progress | Complete content, request review |
| `review` | Under review by stakeholders | Address feedback, approve or revise |
| `approved` | Approved for implementation | Begin implementation |
| `implemented` | Implementation complete | Monitor, update if needed |
| `deprecated` | No longer current | Reference replacement document |
| `rejected` | Not approved for implementation | Document reasons, archive |

## Frontmatter Reference

**Required fields:**
```yaml
---
uuid: GUUID-20250129-0001
title: "Document Title"
status: draft
created: 2025-01-29
updated: 2025-01-29
---
```

**Optional fields:**
```yaml
---
type: pdr
author: "Author Name"
description: "Brief description"
tags: [api, security, v2]
related: [GUUID-20250128-0003, GUUID-20250127-0001]
---
```

## Directory Structure

```
design/
  pdr/           - Product Design Reviews
  spec/          - Technical Specifications
  feature/       - Feature Documents
  decision/      - Architecture Decision Records
  architecture/  - System Architecture Documents
  template/      - Reusable Templates
```

## Examples

### Example 1: Create a New PDR Document

```bash
# Create a Product Design Review document
python scripts/eaa_design_create.py --type pdr --title "User Authentication Redesign"

# Output: Created design/pdr/GUUID-20250129-0001-user-authentication-redesign.md
```

### Example 2: Search and Validate Documents

```bash
# Find all approved PDRs
python scripts/eaa_design_search.py --type pdr --status approved --format table

# Validate all documents for frontmatter compliance
python scripts/eaa_design_validate.py --all --verbose
```

## Resources

- [references/uuid-specification.md](references/uuid-specification.md) - GUUID format and generation
- [references/document-types.md](references/document-types.md) - Six document type categories
- [references/creating-documents.md](references/creating-documents.md) - Document creation workflow
- [references/searching-documents.md](references/searching-documents.md) - Query and filter documents
- [references/validating-documents.md](references/validating-documents.md) - Frontmatter validation
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and fixes

---

**Skill Version:** 1.0.0
**Last Updated:** 2025-01-29
**Maintainer:** Skill Development Team
