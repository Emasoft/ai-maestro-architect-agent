---
operation: create-document-from-template
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-design-management
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Create Document from Template

## When to Use

Use this operation when:
- Creating a new design document of any type (PDR, spec, feature, etc.)
- Initializing a document with proper structure and frontmatter
- Ensuring consistency across design documents
- Starting a new design effort that needs formal documentation

## Prerequisites

- Python 3.10 or higher installed
- Access to the `scripts/eaa_design_create.py` script
- Write access to the `design/` directory structure
- Understanding of the document type you need to create

## Procedure

### Step 1: Select Document Type

Choose the appropriate document type for your needs.

| Type | Use Case | Directory |
|------|----------|-----------|
| `pdr` | Product Design Review - comprehensive feature designs | `design/pdr/` |
| `spec` | Technical Specification - detailed technical documentation | `design/spec/` |
| `feature` | Feature Document - user-facing feature descriptions | `design/feature/` |
| `decision` | Architecture Decision Record - decision documentation | `design/decision/` |
| `architecture` | System Architecture - high-level system design | `design/architecture/` |
| `template` | Reusable Template - document templates | `design/template/` |

### Step 2: Run Creation Script

Execute the document creation script with required arguments:

```bash
python scripts/eaa_design_create.py --type <type> --title "<title>"
```

**Required arguments:**
- `--type`: Document type (pdr, spec, feature, decision, architecture, template)
- `--title`: Document title in quotes

**Optional arguments:**
- `--author`: Author name
- `--description`: Brief description
- `--filename`: Custom filename (instead of auto-generated)

### Step 3: Verify Created Document

Check that the document was created with proper structure:

```bash
# List the created file
ls -la design/<type>/

# Check frontmatter
head -20 design/<type>/<filename>.md
```

### Step 4: Populate Document Content

Open the created document and fill in the template sections:

1. Complete all required frontmatter fields
2. Fill in the document body sections
3. Add diagrams or references as needed
4. Update the `updated` field when making changes

### Step 5: Validate Document

Run validation to ensure compliance:

```bash
python scripts/eaa_design_validate.py design/<type>/<filename>.md
```

## Checklist

Copy this checklist and track your progress:

- [ ] Select appropriate document type
- [ ] Prepare title and optional metadata
- [ ] Run creation script with required arguments
- [ ] Verify file was created in correct directory
- [ ] Check frontmatter is properly populated
- [ ] Fill in all template sections
- [ ] Run validation to check compliance
- [ ] Fix any validation errors

## Examples

### Example 1: Create a PDR Document

```bash
# Create a Product Design Review for user authentication
python scripts/eaa_design_create.py --type pdr --title "User Authentication System Design"

# Output:
# Created: design/pdr/GUUID-20260130-0001-user-authentication-system-design.md
# UUID: GUUID-20260130-0001
# Type: pdr
# Status: draft
```

### Example 2: Create with All Options

```bash
# Create a spec with author and description
python scripts/eaa_design_create.py \
  --type spec \
  --title "REST API Specification v2" \
  --author "API Team" \
  --description "Detailed specification for the v2 REST API endpoints"

# Output:
# Created: design/spec/GUUID-20260130-0002-rest-api-specification-v2.md
```

### Example 3: Create with Custom Filename

```bash
# Create a decision record with custom filename
python scripts/eaa_design_create.py \
  --type decision \
  --title "Database Selection" \
  --filename "adr-001-database-selection"

# Output:
# Created: design/decision/adr-001-database-selection.md
```

### Example 4: Expected Frontmatter Output

After creation, the document will have this frontmatter:

```yaml
---
uuid: GUUID-20260130-0001
title: "User Authentication System Design"
status: draft
created: 2026-01-30
updated: 2026-01-30
type: pdr
author: ""
description: ""
tags: []
related: []
---

# User Authentication System Design

## Overview
[Describe the purpose and scope of this design]

## Background
[Provide context and background information]

## Requirements
[List the requirements this design addresses]

## Proposed Design
[Describe the proposed design in detail]

## Alternatives Considered
[Document alternatives that were considered]

## Implementation Plan
[Outline the implementation approach]

## References
[List related documents and resources]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Script not found | Missing eaa_design_create.py | Verify script path: `scripts/eaa_design_create.py` |
| Invalid document type | Unsupported type specified | Use valid type: pdr, spec, feature, decision, architecture, template |
| Permission denied | No write access to design directory | Check directory permissions |
| UUID generation failed | System issue | Retry or generate UUID manually |
| Directory not found | Missing design subdirectory | Create directory: `mkdir -p design/<type>/` |
| Title empty | No title provided | Provide `--title "Your Title"` argument |

## Related Operations

- [op-generate-guuid.md](op-generate-guuid.md) - UUID generation details
- [op-validate-frontmatter.md](op-validate-frontmatter.md) - Validate created document
- [op-search-design-documents.md](op-search-design-documents.md) - Find existing documents
