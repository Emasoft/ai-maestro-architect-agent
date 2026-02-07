---
operation: generate-guuid
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-design-management
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Generate GUUID

## When to Use

Use this operation when:
- Creating a new design document that needs a unique identifier
- Understanding the GUUID format used in design documents
- Manually generating a UUID when automation is unavailable
- Verifying that an existing UUID follows the correct format
- Troubleshooting UUID-related validation errors

## Prerequisites

- Understanding of the GUUID format specification
- Access to current date in ISO format
- Ability to generate or obtain unique sequence numbers

## Procedure

### Step 1: Understand GUUID Format

GUUID stands for "Globalized Unique Universal Identifier" and follows this format:

```
GUUID-YYYYMMDD-NNNN
```

**Components:**

| Component | Description | Example |
|-----------|-------------|---------|
| `GUUID` | Fixed prefix | GUUID |
| `YYYYMMDD` | Creation date in ISO format | 20260130 |
| `NNNN` | 4-digit sequence number | 0001 |

**Full example:** `GUUID-20260130-0001`

### Step 2: Generate Using Script (Recommended)

Use the automated generation script:

```bash
python scripts/eaa_design_uuid.py
```

**Output:**
```
Generated UUID: GUUID-20260130-0001
Date: 2026-01-30
Sequence: 0001
Unique: Yes (verified against existing documents)
```

### Step 3: Manual Generation (Fallback)

If the script is unavailable, generate manually:

1. **Get today's date in YYYYMMDD format:**
   ```bash
   date +%Y%m%d
   # Output: 20260130
   ```

2. **Determine sequence number:**
   - Check existing documents for today's date
   - Use the next available number (0001, 0002, etc.)
   - If first document today, use 0001

3. **Combine components:**
   ```
   GUUID-20260130-0001
   ```

### Step 4: Verify Uniqueness

Before using the UUID, verify it doesn't already exist:

```bash
python scripts/eaa_design_search.py --uuid GUUID-20260130-0001
```

If found, increment the sequence number.

### Step 5: Apply UUID to Document

Add the UUID to your document's frontmatter:

```yaml
---
uuid: GUUID-20260130-0001
title: "Your Document Title"
status: draft
created: 2026-01-30
updated: 2026-01-30
---
```

## GUUID Format Rules

| Rule | Description | Valid | Invalid |
|------|-------------|-------|---------|
| Prefix | Must be "GUUID" | GUUID-... | UUID-..., ID-... |
| Date format | YYYYMMDD with no separators | 20260130 | 2026-01-30, 01/30/2026 |
| Sequence | 4 digits, zero-padded | 0001, 0123 | 1, 001, 12345 |
| Separator | Single hyphen between components | GUUID-DATE-SEQ | GUUID_DATE_SEQ |
| Case | Uppercase prefix, lowercase for extensions | GUUID-20260130-0001 | guuid-20260130-0001 |

## Checklist

Copy this checklist and track your progress:

- [ ] Determine if automated or manual generation needed
- [ ] Get today's date in YYYYMMDD format
- [ ] Check existing UUIDs for today to find next sequence
- [ ] Generate UUID in GUUID-YYYYMMDD-NNNN format
- [ ] Verify UUID is unique (search existing documents)
- [ ] Apply UUID to document frontmatter
- [ ] Validate document passes UUID format check

## Examples

### Example 1: Generate First UUID of the Day

```bash
# Check what exists today
python scripts/eaa_design_search.py --uuid "GUUID-20260130"
# Output: No documents found

# Generate new UUID
python scripts/eaa_design_uuid.py
# Output: GUUID-20260130-0001
```

### Example 2: Generate Subsequent UUID

```bash
# Check what exists today
python scripts/eaa_design_search.py --uuid "GUUID-20260130" --format table
# Output:
# +---------------------+----------------------+--------+
# | UUID                | Title                | Status |
# +---------------------+----------------------+--------+
# | GUUID-20260130-0001 | Auth Design          | draft  |
# | GUUID-20260130-0002 | API Spec             | draft  |
# +---------------------+----------------------+--------+

# Next available: GUUID-20260130-0003
python scripts/eaa_design_uuid.py
# Output: GUUID-20260130-0003
```

### Example 3: Manual Generation

```bash
# Step 1: Get date
DATE=$(date +%Y%m%d)
echo $DATE
# Output: 20260130

# Step 2: Find next sequence
ls design/*/GUUID-${DATE}* 2>/dev/null | wc -l
# Output: 2 (so next is 0003)

# Step 3: Format sequence
SEQ=$(printf "%04d" 3)
echo $SEQ
# Output: 0003

# Step 4: Combine
echo "GUUID-${DATE}-${SEQ}"
# Output: GUUID-20260130-0003
```

### Example 4: UUID in Document Context

```yaml
---
uuid: GUUID-20260130-0001
title: "User Authentication System Design"
status: draft
created: 2026-01-30
updated: 2026-01-30
type: pdr
author: "Architecture Team"
description: "Design document for the new authentication system"
tags: [authentication, security, oauth]
related: []
---

# User Authentication System Design

## Overview
This document describes the design for the user authentication system...
```

### Example 5: UUID Filename Convention

When using UUID in filenames, append a slug version of the title:

```
GUUID-20260130-0001-user-authentication-system-design.md
```

**Format:** `{UUID}-{title-slug}.md`

**Slug rules:**
- Lowercase
- Spaces replaced with hyphens
- Special characters removed
- Truncated to reasonable length

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| UUID already exists | Sequence number conflict | Increment sequence number |
| Invalid date format | Wrong date in UUID | Use YYYYMMDD format |
| Invalid sequence | Sequence not 4 digits | Zero-pad to 4 digits |
| Wrong prefix | Not using GUUID | Start with "GUUID-" |
| Future date | Date is in the future | Use current date only |
| Script failed | Python environment issue | Use manual generation method |

## Related Operations

- [op-create-document-from-template.md](op-create-document-from-template.md) - Uses GUUID when creating documents
- [op-validate-frontmatter.md](op-validate-frontmatter.md) - Validates UUID format
- [op-search-design-documents.md](op-search-design-documents.md) - Search by UUID
