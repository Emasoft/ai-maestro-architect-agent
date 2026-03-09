# Quick Reference - Design Document Management

## Table of Contents

- [Quick Reference Commands](#quick-reference-commands)
- [Document Status Workflow](#document-status-workflow)
- [Frontmatter Reference](#frontmatter-reference)
- [Directory Structure](#directory-structure)
- [Extended Examples](#extended-examples)

## Quick Reference Commands

**Create documents:**
```bash
# Create a PDR
python scripts/amaa_design_create.py --type pdr --title "Feature Design"

# Create with author
python scripts/amaa_design_create.py --type feature --title "OAuth" --author "John"

# Create with custom filename
python scripts/amaa_design_create.py --type spec --title "API Spec" --filename "api-v2"
```

**Search documents:**
```bash
# Search by UUID
python scripts/amaa_design_search.py --uuid GUUID-20250129-0001

# Search by type and status
python scripts/amaa_design_search.py --type pdr --status approved

# Search by keyword
python scripts/amaa_design_search.py --keyword "authentication"

# Table output
python scripts/amaa_design_search.py --type feature --format table
```

**Validate documents:**
```bash
# Validate single file
python scripts/amaa_design_validate.py design/pdr/my-design.md

# Validate all documents
python scripts/amaa_design_validate.py --all

# Validate specific type
python scripts/amaa_design_validate.py --all --type pdr

# Verbose output with warnings
python scripts/amaa_design_validate.py --all --verbose --format text
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

## Extended Examples

### Example 1: Create a New PDR Document

```bash
python scripts/amaa_design_create.py --type pdr --title "User Authentication Redesign"
# Output: Created design/pdr/GUUID-20250129-0001-user-authentication-redesign.md
```

### Example 2: Search and Validate Documents

```bash
# Find all approved PDRs
python scripts/amaa_design_search.py --type pdr --status approved --format table

# Validate all documents for frontmatter compliance
python scripts/amaa_design_validate.py --all --verbose
```
