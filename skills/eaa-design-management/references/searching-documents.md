# Searching Documents

This document explains how to search design documents using the `eia_design_search.py` script.

## Contents

- 4.1 UUID Search
- 4.2 Type Filter
- 4.3 Status Filter
- 4.4 Keyword Search
- 4.5 Glob Pattern Search
- 4.6 Combined Filters
- 4.7 Empty Results Handling
- 4.8 Output Formats
- 4.9 Script Reference

---

## 4.1 UUID Search

Search for a specific document by its UUID:

```bash
python scripts/eia_design_search.py --uuid GUUID-20250129-0001
```

**Output:**
```json
{
  "results": [
    {
      "file_path": "design/pdr/auth-system.md",
      "uuid": "GUUID-20250129-0001",
      "title": "Authentication System Design",
      "type": "pdr",
      "status": "approved",
      "created": "2025-01-29",
      "updated": "2025-01-29"
    }
  ],
  "total": 1,
  "search_params": {
    "uuid": "GUUID-20250129-0001",
    "type": null,
    "status": null,
    "keyword": null,
    "pattern": null
  }
}
```

**Invalid UUID format:**
```bash
python scripts/eia_design_search.py --uuid invalid-uuid
```

```json
{
  "error": "Invalid UUID format: invalid-uuid. Expected: GUUID-YYYYMMDD-NNNN",
  "results": [],
  "total": 0,
  "search_params": {...}
}
```

---

## 4.2 Type Filter

Search for all documents of a specific type:

```bash
python scripts/eia_design_search.py --type pdr
```

**Output:**
```json
{
  "results": [
    {
      "file_path": "design/pdr/auth-system.md",
      "uuid": "GUUID-20250129-0001",
      "title": "Authentication System Design",
      "type": "pdr",
      "status": "approved",
      "created": "2025-01-29",
      "updated": "2025-01-29"
    },
    {
      "file_path": "design/pdr/database-migration.md",
      "uuid": "GUUID-20250128-0003",
      "title": "Database Migration Plan",
      "type": "pdr",
      "status": "draft",
      "created": "2025-01-28",
      "updated": "2025-01-29"
    }
  ],
  "total": 2,
  "search_params": {...}
}
```

**Valid type values:**
- `pdr` - Product Design Reviews
- `spec` - Technical Specifications
- `feature` - Feature Documents
- `decision` - Architecture Decision Records
- `architecture` - Architecture Documents
- `template` - Document Templates

---

## 4.3 Status Filter

Search for documents with a specific status:

```bash
python scripts/eia_design_search.py --status approved
```

**Valid status values:**
- `draft` - Initial creation, work in progress
- `review` - Under review by stakeholders
- `approved` - Approved for implementation
- `implemented` - Implementation complete
- `deprecated` - No longer current
- `rejected` - Not approved for implementation

**Example: Find all draft documents:**
```bash
python scripts/eia_design_search.py --status draft
```

**Example: Find deprecated documents:**
```bash
python scripts/eia_design_search.py --status deprecated
```

---

## 4.4 Keyword Search

Search for documents containing a keyword in title or content:

```bash
python scripts/eia_design_search.py --keyword "authentication"
```

**Search behavior:**
- Case-insensitive search
- Searches both title and full document content
- Partial word matching (e.g., "auth" matches "authentication")

**Examples:**
```bash
# Search for OAuth-related documents
python scripts/eia_design_search.py --keyword "oauth"

# Search for API-related documents
python scripts/eia_design_search.py --keyword "api"

# Search for specific technology
python scripts/eia_design_search.py --keyword "postgresql"
```

---

## 4.5 Glob Pattern Search

Use glob patterns to search specific files or directories:

```bash
# All files in pdr/ directory
python scripts/eia_design_search.py --pattern "pdr/*.md"

# All files recursively in design/
python scripts/eia_design_search.py --pattern "**/*.md"

# Files starting with "api-"
python scripts/eia_design_search.py --pattern "**/api-*.md"

# Files in specific subdirectory
python scripts/eia_design_search.py --pattern "spec/v2/*.md"
```

**Common patterns:**
| Pattern | Matches |
|---------|---------|
| `*.md` | All .md files in design root |
| `**/*.md` | All .md files recursively |
| `pdr/*.md` | All .md files in pdr/ only |
| `**/auth*.md` | All .md files starting with "auth" |
| `feature/202501*.md` | Feature docs created in Jan 2025 |

---

## 4.6 Combined Filters

Combine multiple filters to narrow results:

```bash
# PDR documents that are approved
python scripts/eia_design_search.py --type pdr --status approved

# Draft features containing "api"
python scripts/eia_design_search.py --type feature --status draft --keyword "api"

# Approved specs in specific directory
python scripts/eia_design_search.py --pattern "spec/v2/*.md" --status approved
```

**Filter logic:**
- All filters are combined with AND logic
- A document must match ALL specified filters to be included
- Unspecified filters are ignored (no filtering on that attribute)

**Examples:**
```bash
# Find all approved PDRs about authentication
python scripts/eia_design_search.py \
  --type pdr \
  --status approved \
  --keyword "authentication"

# Find draft decision records
python scripts/eia_design_search.py \
  --type decision \
  --status draft
```

---

## 4.7 Empty Results Handling

When no documents match the search criteria:

```json
{
  "results": [],
  "total": 0,
  "search_params": {
    "uuid": null,
    "type": "pdr",
    "status": "approved",
    "keyword": "nonexistent",
    "pattern": null
  }
}
```

**Table format output:**
```
No documents found matching criteria.
```

**Common causes of empty results:**
1. **Typo in keyword** - Check spelling
2. **Wrong type** - Verify document is in the expected type directory
3. **Wrong status** - Document may have different status
4. **Pattern too specific** - Try broader glob pattern
5. **Design directory empty** - No documents created yet

**Debugging empty results:**
```bash
# List all documents (no filters)
python scripts/eia_design_search.py

# Check if type directory has documents
ls design/pdr/

# Try broader search
python scripts/eia_design_search.py --pattern "**/*.md"
```

---

## 4.8 Output Formats

### JSON Format (Default)

```bash
python scripts/eia_design_search.py --type pdr --format json
```

**Output structure:**
```json
{
  "results": [...],
  "total": 5,
  "search_params": {...}
}
```

### Table Format

```bash
python scripts/eia_design_search.py --type pdr --format table
```

**Output:**
```
UUID                   Type         Status       Title                                    Updated
----------------------------------------------------------------------------------------------------
GUUID-20250129-0001    pdr          approved     Authentication System Design             2025-01-29
GUUID-20250128-0003    pdr          draft        Database Migration Plan                  2025-01-29

Total: 2 document(s)
```

---

## 4.9 Script Reference

### Full Command Syntax

```bash
python scripts/eia_design_search.py \
  [--uuid UUID] \
  [--type TYPE] \
  [--status STATUS] \
  [--keyword KEYWORD] \
  [--pattern PATTERN] \
  [--design-dir PATH] \
  [--format {json,table}]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `--uuid` | Exact UUID to match (GUUID-YYYYMMDD-NNNN format) |
| `--type` | Document type filter (pdr, spec, feature, decision, architecture, template) |
| `--status` | Status filter (draft, review, approved, implemented, deprecated, rejected) |
| `--keyword` | Search in title and content (case-insensitive) |
| `--pattern` | Glob pattern for file matching (relative to design root) |
| `--design-dir` | Path to design directory (default: ../design from script) |
| `--format` | Output format: json (default) or table |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Search completed (even if no results) |
| 1 | Search error (invalid arguments, missing directory) |

### Result Sorting

Results are sorted by `updated` date in descending order (most recently updated first).

---

## See Also

- [UUID Specification](uuid-specification.md) - UUID format for searching by UUID
- [Document Types](document-types.md) - Valid type values
- [Validating Documents](validating-documents.md) - Finding and fixing invalid documents
