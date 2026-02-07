---
procedure: support-skill
workflow-instruction: support
---

# Operation: Archive Valuable Prototype

## Purpose

Archive a prototype from an experiment that has value for future reference, reuse, or as a starting point for implementation.

## When to Use

- Experiment produced useful code worth preserving
- Prototype could be basis for implementation
- Code demonstrates a technique worth documenting

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Experiment results | REPORT.md | Yes |
| Source code | Experiment scripts | Yes |
| Archive decision | Analysis | Yes |

## Procedure

### Step 1: Evaluate Archive Criteria

Archive if ANY of these are true:
- [ ] Code implements a verified claim successfully
- [ ] Code demonstrates a non-obvious technique
- [ ] Code could be starting point for production implementation
- [ ] Code has educational value for team
- [ ] Code solves a problem likely to recur

Do NOT archive if:
- [ ] All approaches failed
- [ ] Code is trivial/obvious
- [ ] Better implementations exist
- [ ] Code has no reuse potential

### Step 2: Create Archive Directory

```bash
CLAIM_NAME="redis-caching"
ARCHIVE_DIR="prototypes/${CLAIM_NAME}"

mkdir -p "${ARCHIVE_DIR}/src"
mkdir -p "${ARCHIVE_DIR}/tests"
mkdir -p "${ARCHIVE_DIR}/docs"
```

### Step 3: Copy Valuable Code

```bash
# Copy only the valuable approach(es)
cp experiments/${CLAIM_NAME}/scripts/approach_b.py prototypes/${CLAIM_NAME}/src/
cp experiments/${CLAIM_NAME}/requirements.txt prototypes/${CLAIM_NAME}/

# Copy tests if any
cp experiments/${CLAIM_NAME}/tests/*.py prototypes/${CLAIM_NAME}/tests/

# Copy relevant documentation
cp experiments/${CLAIM_NAME}/REPORT.md prototypes/${CLAIM_NAME}/docs/EXPERIMENT_REPORT.md
```

### Step 4: Create README

Create `prototypes/<claim-name>/README.md`:

```markdown
# Prototype: <Claim Name>

**Source Experiment:** experiments/<claim-name>
**Date Archived:** YYYY-MM-DD
**Status:** <VERIFIED|PARTIALLY VERIFIED>

---

## Purpose

<Why this prototype was archived and what value it provides>

## Background

<Brief summary of the experiment and findings>

### Experiment Summary

- **Claim:** "<original claim>"
- **Result:** <VERIFIED/PARTIALLY VERIFIED>
- **Key Finding:** <main takeaway>

---

## What This Prototype Does

<Description of the prototype's functionality>

### Key Features

- <Feature 1>
- <Feature 2>
- <Feature 3>

---

## How to Use

### Prerequisites

- Python 3.12+
- <Other requirements>

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from src.approach_b import <main_function>

result = <main_function>(params)
```

### Example

```python
# Complete working example
```

---

## File Structure

```
prototypes/<claim-name>/
├── README.md           # This file
├── requirements.txt    # Dependencies
├── src/
│   └── approach_b.py   # Main implementation
├── tests/
│   └── test_approach.py
└── docs/
    └── EXPERIMENT_REPORT.md  # Full experiment report
```

---

## Limitations

<What this prototype does NOT do or handle>

- <Limitation 1>
- <Limitation 2>

---

## When to Use This

Use this prototype when:
- <Scenario 1>
- <Scenario 2>

Do NOT use when:
- <Anti-scenario 1>
- <Anti-scenario 2>

---

## Adapting for Production

If using this prototype as a basis for production code:

### Required Changes

1. <Change 1> - <why needed>
2. <Change 2> - <why needed>

### Recommended Enhancements

1. <Enhancement 1>
2. <Enhancement 2>

---

## Related Resources

- [Original Experiment Report](docs/EXPERIMENT_REPORT.md)
- [Related Prototype](../other-prototype/)
- [External Reference](url)

---

## Maintainer

<Name/Team>

## License

<License or "Internal use only">
```

### Step 5: Clean Up Code

Before archiving, clean the code:

```python
# Remove debug statements
# Remove unused imports
# Add docstrings
# Format with ruff
```

```bash
cd prototypes/${CLAIM_NAME}
ruff format src/
ruff check src/ --fix
```

### Step 6: Add Tests (if missing)

```python
# prototypes/<claim-name>/tests/test_approach.py

import pytest
from src.approach_b import main_function

def test_basic_functionality():
    """Test that the main function works as expected."""
    result = main_function(input_data)
    assert result == expected_output

def test_edge_case():
    """Test edge case handling."""
    result = main_function(edge_case_data)
    assert result is not None
```

### Step 7: Verify Archive Works

```bash
cd prototypes/${CLAIM_NAME}

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Verify example from README works
python -c "from src.approach_b import main_function; print(main_function(test_data))"
```

## Output

| File | Content |
|------|---------|
| `prototypes/<claim>/README.md` | Documentation |
| `prototypes/<claim>/src/` | Cleaned source code |
| `prototypes/<claim>/tests/` | Test files |
| `prototypes/<claim>/docs/` | Experiment report |

## Verification Checklist

- [ ] Archive criteria met
- [ ] Directory structure created
- [ ] Valuable code copied
- [ ] Code cleaned and formatted
- [ ] README created with usage instructions
- [ ] Tests added and passing
- [ ] Example verified working
- [ ] Experiment report linked

## Example

```
prototypes/redis-caching/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── redis_cache.py
├── tests/
│   └── test_redis_cache.py
└── docs/
    └── EXPERIMENT_REPORT.md
```

## Error Handling

| Error | Solution |
|-------|----------|
| Code doesn't run standalone | Add missing imports and dependencies |
| Tests fail in archive | Fix tests or document known issues |
| README unclear | Get feedback, improve examples |
