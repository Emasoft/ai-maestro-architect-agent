---
name: amaa-design-management
description: "Use when creating, searching, or validating design documents from templates in the design/ directory."
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

1. Read UUID Specification reference to understand the GUUID format
2. Review Document Types reference to select the appropriate type
3. Create document: `python scripts/amaa_design_create.py --type <type> --title "<title>"`
4. Verify document has proper UUID and frontmatter
5. Search documents: `python scripts/amaa_design_search.py --type <type> --status <status>`
6. Validate all: `python scripts/amaa_design_validate.py --all`
7. Fix any validation errors; consult Troubleshooting if errors persist

## Reference Documents

| Document | Description |
|----------|-------------|
| [uuid-specification.md](references/uuid-specification.md) | GUUID format and generation rules |
| [document-types.md](references/document-types.md) | Six document type categories and when to use each |
| [creating-documents.md](references/creating-documents.md) | Document creation workflow and templates |
| [searching-documents.md](references/searching-documents.md) | Query and filter documents by metadata/content |
| [validating-documents.md](references/validating-documents.md) | Frontmatter validation rules and fixes |
| [troubleshooting.md](references/troubleshooting.md) | Common issues and recovery procedures |
| [quick-reference.md](references/quick-reference.md) | Commands, status workflow, frontmatter fields, examples |

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

- [references/quick-reference.md](references/quick-reference.md) - Commands cheat sheet and examples
- [references/uuid-specification.md](references/uuid-specification.md) - GUUID format spec
- [references/document-types.md](references/document-types.md) - Document type guide
- [references/troubleshooting.md](references/troubleshooting.md) - Troubleshooting guide
