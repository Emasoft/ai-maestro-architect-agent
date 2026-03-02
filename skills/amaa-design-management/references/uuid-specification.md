# UUID Format Specification

This document defines the GUUID (Global Unique Identifier for Design Documents) format used to uniquely identify design documents across the entire codebase.

## Contents

- 1.1 UUID Format Definition
- 1.2 Date Component Requirements
- 1.3 Sequence Number Rules
- 1.4 Manual UUID Generation
- 1.5 UUID Validation Rules
- 1.6 UUID Parsing

---

## 1.1 UUID Format Definition

The GUUID format follows this pattern:

```
GUUID-YYYYMMDD-NNNN
```

**Components:**
- `GUUID` - Fixed prefix identifying this as a design document UUID
- `YYYYMMDD` - Date of document creation (8 digits)
- `NNNN` - Sequence number for that day (4 digits, zero-padded)

**Examples:**
```
GUUID-20250129-0001  (First document on January 29, 2025)
GUUID-20250129-0002  (Second document on January 29, 2025)
GUUID-20250130-0001  (First document on January 30, 2025)
```

---

## 1.2 Date Component Requirements

The date component (`YYYYMMDD`) must be:

1. **Valid calendar date**: The date must represent a real calendar date
   - Year: 2000-2099 (reasonable range for documents)
   - Month: 01-12
   - Day: 01-31 (must be valid for the month)

2. **Creation date**: The date should match when the document was created, not when it was modified

3. **ISO format without separators**: No hyphens or slashes in the date

**Valid dates:**
```
20250129  (January 29, 2025)
20251231  (December 31, 2025)
20260101  (January 1, 2026)
```

**Invalid dates:**
```
2025-01-29  (Contains hyphens)
25012025    (Wrong order)
20251301    (Invalid month 13)
20250230    (February 30 does not exist)
```

---

## 1.3 Sequence Number Rules

The sequence number (`NNNN`) follows these rules:

1. **Zero-padded to 4 digits**: Always 4 digits (0001, 0042, 0999)
2. **Starts at 0001**: First document of the day is 0001, not 0000
3. **Increments per day**: Resets to 0001 on each new day
4. **Maximum 9999**: Supports up to 9999 documents per day

**Automatic generation:**
The `eia_design_create.py` script automatically finds the highest existing sequence number for the current date and increments it.

**Example sequence:**
```
GUUID-20250129-0001  (Created at 09:00)
GUUID-20250129-0002  (Created at 10:30)
GUUID-20250129-0003  (Created at 14:15)
GUUID-20250130-0001  (Next day, reset to 0001)
```

---

## 1.4 Manual UUID Generation

While automatic generation is preferred, you may need to create a UUID manually in some cases:

**Step 1: Determine the date**
```bash
date +%Y%m%d
# Output: 20250129
```

**Step 2: Find the highest existing sequence**
```bash
# Search for existing UUIDs with today's date
python scripts/eia_design_search.py --pattern "**/*.md" --format table | grep "GUUID-20250129"
```

**Step 3: Increment and format**
If the highest existing is GUUID-20250129-0005, use GUUID-20250129-0006.

**Step 4: Verify uniqueness**
```bash
python scripts/eia_design_search.py --uuid GUUID-20250129-0006
# Should return 0 results
```

---

## 1.5 UUID Validation Rules

A valid UUID must satisfy ALL of these conditions:

| Rule | Description | Example (Valid) | Example (Invalid) |
|------|-------------|-----------------|-------------------|
| Prefix | Must start with "GUUID-" | GUUID-20250129-0001 | UUID-20250129-0001 |
| Date length | Date must be 8 digits | GUUID-20250129-0001 | GUUID-2025129-0001 |
| Date format | Must be YYYYMMDD | GUUID-20250129-0001 | GUUID-29012025-0001 |
| Valid date | Must be real calendar date | GUUID-20250228-0001 | GUUID-20250230-0001 |
| Sequence length | Must be 4 digits | GUUID-20250129-0001 | GUUID-20250129-1 |
| Sequence range | Must be 0001-9999 | GUUID-20250129-0001 | GUUID-20250129-0000 |
| Separators | Must have exactly 2 hyphens | GUUID-20250129-0001 | GUUID20250129-0001 |

**Validation regex pattern:**
```python
import re
UUID_PATTERN = re.compile(r"^GUUID-(\d{4})(\d{2})(\d{2})-(\d{4})$")

def is_valid_uuid(uuid_string):
    match = UUID_PATTERN.match(uuid_string)
    if not match:
        return False
    year, month, day, seq = match.groups()
    month, day, seq = int(month), int(day), int(seq)
    return 1 <= month <= 12 and 1 <= day <= 31 and seq >= 1
```

---

## 1.6 UUID Parsing

To extract components from a UUID:

**Python example:**
```python
import re

def parse_uuid(uuid_string):
    """Parse a GUUID into its components.

    Returns dict with year, month, day, sequence, or None if invalid.
    """
    pattern = re.compile(r"^GUUID-(\d{4})(\d{2})(\d{2})-(\d{4})$")
    match = pattern.match(uuid_string)
    if not match:
        return None

    return {
        "year": int(match.group(1)),
        "month": int(match.group(2)),
        "day": int(match.group(3)),
        "sequence": int(match.group(4)),
        "date": f"{match.group(1)}-{match.group(2)}-{match.group(3)}",
    }

# Example usage
result = parse_uuid("GUUID-20250129-0042")
# result = {"year": 2025, "month": 1, "day": 29, "sequence": 42, "date": "2025-01-29"}
```

**Bash example:**
```bash
UUID="GUUID-20250129-0042"
YEAR="${UUID:6:4}"    # 2025
MONTH="${UUID:10:2}"  # 01
DAY="${UUID:12:2}"    # 29
SEQ="${UUID:15:4}"    # 0042
```

---

## See Also

- [Creating Documents](creating-documents.md) - How to create documents with automatic UUID generation
- [Validating Documents](validating-documents.md) - How to validate UUID format in existing documents
