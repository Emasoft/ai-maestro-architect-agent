---
operation: search-design-documents
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-design-management
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Search Design Documents


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Determine Search Criteria](#step-1-determine-search-criteria)
  - [Step 2: Execute Search](#step-2-execute-search)
  - [Step 3: Interpret Results](#step-3-interpret-results)
  - [Step 4: Combine Filters](#step-4-combine-filters)
  - [Step 5: Handle Empty Results](#step-5-handle-empty-results)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Find All PDRs in Review](#example-1-find-all-pdrs-in-review)
  - [Example 2: Search by Keyword](#example-2-search-by-keyword)
  - [Example 3: Find Specific Document by UUID](#example-3-find-specific-document-by-uuid)
  - [Example 4: Combined Filter Search](#example-4-combined-filter-search)
  - [Example 5: List All Documents of a Type](#example-5-list-all-documents-of-a-type)
- [Search Result Fields](#search-result-fields)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Looking for existing design documents by type, status, or content
- Finding related documents before creating a new design
- Auditing design documents for a specific project area
- Generating reports on design document status
- Verifying no duplicate designs exist

## Prerequisites

- Python 3.10 or higher installed
- Access to the `scripts/eaa_design_search.py` script
- Design documents exist in the `design/` directory structure
- Understanding of frontmatter fields for filtering

## Procedure

### Step 1: Determine Search Criteria

Identify what you're searching for:

| Filter | Use Case | Example |
|--------|----------|---------|
| `--uuid` | Find specific document by UUID | `GUUID-20260130-0001` |
| `--type` | Filter by document type | `pdr`, `spec`, `feature` |
| `--status` | Filter by document status | `draft`, `review`, `approved` |
| `--keyword` | Search document content | `authentication`, `api` |
| `--author` | Filter by author | `Alice`, `API Team` |

### Step 2: Execute Search

Run the search script with your criteria:

```bash
python scripts/eaa_design_search.py [options]
```

**Search by UUID:**
```bash
python scripts/eaa_design_search.py --uuid GUUID-20260130-0001
```

**Search by type and status:**
```bash
python scripts/eaa_design_search.py --type pdr --status approved
```

**Search by keyword:**
```bash
python scripts/eaa_design_search.py --keyword "authentication"
```

### Step 3: Interpret Results

Results can be displayed in two formats:

**JSON format (default):**
```bash
python scripts/eaa_design_search.py --type pdr --format json
```

**Table format:**
```bash
python scripts/eaa_design_search.py --type pdr --format table
```

### Step 4: Combine Filters

Combine multiple filters for precise results:

```bash
python scripts/eaa_design_search.py \
  --type spec \
  --status approved \
  --keyword "api"
```

### Step 5: Handle Empty Results

If no results are found:
1. Verify the search criteria are correct
2. Check if documents exist with different status/type
3. Try broader search terms
4. Verify the design directory path

## Checklist

Copy this checklist and track your progress:

- [ ] Identify search criteria (type, status, keyword, etc.)
- [ ] Run search command with appropriate filters
- [ ] Choose output format (json or table)
- [ ] Review search results
- [ ] If empty, broaden search criteria
- [ ] Note relevant document UUIDs for reference

## Examples

### Example 1: Find All PDRs in Review

```bash
python scripts/eaa_design_search.py --type pdr --status review --format table

# Output:
# +---------------------+----------------------------------+--------+------------+
# | UUID                | Title                            | Status | Created    |
# +---------------------+----------------------------------+--------+------------+
# | GUUID-20260128-0001 | User Authentication Design       | review | 2026-01-28 |
# | GUUID-20260129-0002 | Payment Integration Design       | review | 2026-01-29 |
# +---------------------+----------------------------------+--------+------------+
# Found: 2 documents
```

### Example 2: Search by Keyword

```bash
python scripts/eaa_design_search.py --keyword "oauth" --format json

# Output:
# [
#   {
#     "uuid": "GUUID-20260128-0001",
#     "title": "User Authentication Design",
#     "status": "review",
#     "type": "pdr",
#     "path": "design/pdr/GUUID-20260128-0001-user-authentication-design.md",
#     "matches": ["OAuth integration for social login", "OAuth provider configuration"]
#   }
# ]
```

### Example 3: Find Specific Document by UUID

```bash
python scripts/eaa_design_search.py --uuid GUUID-20260128-0001 --format json

# Output:
# {
#   "uuid": "GUUID-20260128-0001",
#   "title": "User Authentication Design",
#   "status": "review",
#   "type": "pdr",
#   "created": "2026-01-28",
#   "updated": "2026-01-30",
#   "author": "Alice",
#   "path": "design/pdr/GUUID-20260128-0001-user-authentication-design.md"
# }
```

### Example 4: Combined Filter Search

```bash
python scripts/eaa_design_search.py \
  --type spec \
  --status approved \
  --keyword "rest api" \
  --format table

# Output:
# +---------------------+----------------------------------+----------+------------+
# | UUID                | Title                            | Status   | Created    |
# +---------------------+----------------------------------+----------+------------+
# | GUUID-20260115-0003 | REST API Specification v1        | approved | 2026-01-15 |
# +---------------------+----------------------------------+----------+------------+
# Found: 1 document
```

### Example 5: List All Documents of a Type

```bash
python scripts/eaa_design_search.py --type decision --format table

# Output:
# +---------------------+----------------------------------+----------+------------+
# | UUID                | Title                            | Status   | Created    |
# +---------------------+----------------------------------+----------+------------+
# | GUUID-20260110-0001 | ADR-001: Database Selection      | approved | 2026-01-10 |
# | GUUID-20260112-0002 | ADR-002: Caching Strategy        | approved | 2026-01-12 |
# | GUUID-20260120-0003 | ADR-003: Auth Provider           | draft    | 2026-01-20 |
# +---------------------+----------------------------------+----------+------------+
# Found: 3 documents
```

## Search Result Fields

| Field | Description |
|-------|-------------|
| `uuid` | Unique identifier for the document |
| `title` | Document title |
| `status` | Current status (draft, review, approved, etc.) |
| `type` | Document type (pdr, spec, feature, etc.) |
| `created` | Creation date |
| `updated` | Last modification date |
| `author` | Document author |
| `path` | Full path to the document file |
| `matches` | Content snippets matching keyword (keyword search only) |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No results found | No documents match criteria | Broaden search, check criteria spelling |
| Invalid type | Unknown document type | Use valid type: pdr, spec, feature, decision, architecture, template |
| Invalid status | Unknown status value | Use valid status: draft, review, approved, implemented, deprecated, rejected |
| Directory not found | Design directory missing | Verify `design/` directory exists |
| Malformed frontmatter | Document has invalid YAML | Run validation on documents first |
| Script not found | Missing search script | Verify script path: `scripts/eaa_design_search.py` |

## Related Operations

- [op-create-document-from-template.md](op-create-document-from-template.md) - Create new documents
- [op-validate-frontmatter.md](op-validate-frontmatter.md) - Validate document structure
- [op-generate-guuid.md](op-generate-guuid.md) - Understand UUID format
