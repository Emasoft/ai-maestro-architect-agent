---
name: amaa-design-management
description: "Use when creating, searching, or validating design documents. Trigger with document management or UUID generation request."
agent: amaa-architect-main-agent
context: fork
user-invocable: false
---

# Design Document Management

## Overview

Manages design documents in the `design/` directory. Covers creating documents from templates, searching with structured queries, and validating frontmatter compliance. Requires Python 3.10+.

## Prerequisites

- Python 3.10 or higher installed
- The `design/` directory structure exists in the project root
- Write access to the design document directories

## Instructions

1. Read UUID Specification to understand the GUUID format
2. Select document type from Document Types reference
3. Create document using `amaa_design_create.py`
4. Validate using `amaa_design_validate.py --all`
5. Search and retrieve using `amaa_design_search.py`

### Checklist

Copy this checklist and track your progress:

- [ ] Read UUID Specification reference to understand the GUUID format
- [ ] Review Document Types reference to select the appropriate type
- [ ] Create document: `python scripts/amaa_design_create.py --type <type> --title "<title>"`
- [ ] Verify document has proper UUID and frontmatter
- [ ] Search documents: `python scripts/amaa_design_search.py --type <type> --status <status>`
- [ ] Validate all: `python scripts/amaa_design_validate.py --all`
- [ ] Fix any validation errors; consult Troubleshooting if errors persist

## Reference Documents

| Document | Description |
|----------|-------------|
| [uuid-specification.md](references/uuid-specification.md) | 1 UUID Format Definition, 2 Date Component Requirements, 3 Sequence Number Rules, 4 Manual UUID Generation, 5 UUID Validation Rules, 6 UUID Parsing |
| [document-types.md](references/document-types.md) | 1 Type Selection Guide, 2 PDR Documents (pdr/), 3 Spec Documents (spec/), 4 Feature Documents (feature/), 5 Decision Documents (decision/), 6 Architecture Documents (architecture/), 7 Template Documents (template/), 8 Directory Structure |
| [creating-documents.md](references/creating-documents.md) | 1 Basic Document Creation, 2 Required Arguments, 3 Optional Fields (author, description), 4 Custom Filenames, 5 Post-Creation Validation, 6 Creation Error Handling, 7 Script Reference |
| [searching-documents.md](references/searching-documents.md) | 1 UUID Search, 2 Type Filter, 3 Status Filter, 4 Keyword Search, 5 Glob Pattern Search, 6 Combined Filters, 7 Empty Results Handling, 8 Output Formats, 9 Script Reference |

## Examples

```bash
# Create a PDR, then validate
python scripts/amaa_design_create.py --type pdr --title "Auth Redesign"
python scripts/amaa_design_validate.py --all
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| UUID generation fails | Date format or sequence conflict | Check date format YYYYMMDD, reset sequence |
| Document creation fails | Missing directory or permissions | Ensure `design/<type>/` exists with write access |
| Search returns no results | Wrong filters or empty directory | Verify type/status values, check directory has files |
| Validation: malformed frontmatter | Invalid YAML syntax | Fix YAML delimiters (`---`) and field formatting |
| Files in wrong directory | Manual file placement error | Move file to correct `design/<type>/` subdirectory |

## Resources

See Reference Documents table above.

## Output

| Output | Format | Example |
|--------|--------|---------|
| Created Document | Markdown file with UUID filename | `design/pdr/GUUID-20250129-0001-feature.md` |
| Search Results | JSON array or ASCII table | `[{"uuid": "GUUID-...", "title": "..."}]` |
| Validation Report | Error list with file paths and line numbers | `ERROR: doc.md:3 - Missing field 'uuid'` |
