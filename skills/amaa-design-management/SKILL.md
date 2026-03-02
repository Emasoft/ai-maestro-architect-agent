---
name: amaa-design-management
description: "Use when creating, searching, or validating design documents. Trigger with document management or UUID generation request."
agent: amaa-main
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
| [uuid-specification.md](references/uuid-specification.md) | GUUID format and rules (1 UUID Format Definition, 2 Date Component Requirements) |
| [document-types.md](references/document-types.md) | Document types (1 Type Selection Guide, 2 PDR Documents (pdr/)) |
| [creating-documents.md](references/creating-documents.md) | Creation workflow (1 Basic Document Creation, 2 Required Arguments) |
| [searching-documents.md](references/searching-documents.md) | Query and filter (1 UUID Search, 2 Type Filter) |
| [validating-documents.md](references/validating-documents.md) | Validation rules (1 Single File Validation, 2 Bulk Validation) |
| [troubleshooting.md](references/troubleshooting.md) | Recovery procedures (1 UUID Generation Issues, 2 Creation Failures) |
| [quick-reference.md](references/quick-reference.md) | Commands and reference (Quick Reference Commands, Document Status Workflow, Frontmatter Reference) |

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

## Output

| Output | Format | Example |
|--------|--------|---------|
| Created Document | Markdown file with UUID filename | `design/pdr/GUUID-20250129-0001-feature.md` |
| Search Results | JSON array or ASCII table | `[{"uuid": "GUUID-...", "title": "..."}]` |
| Validation Report | Error list with file paths and line numbers | `ERROR: doc.md:3 - Missing field 'uuid'` |

## Resources

- [references/quick-reference.md](references/quick-reference.md) - Commands cheat sheet and examples (Quick Reference Commands, Document Status Workflow, Frontmatter Reference, Directory Structure, Extended Examples)
- [references/uuid-specification.md](references/uuid-specification.md) - GUUID format spec (1 UUID Format Definition, 2 Date Component Requirements)
- [references/document-types.md](references/document-types.md) - Document type guide (1 Type Selection Guide, 2 PDR Documents (pdr/))
- [references/troubleshooting.md](references/troubleshooting.md) - Troubleshooting guide (1 UUID Generation Issues, 2 Creation Failures)
