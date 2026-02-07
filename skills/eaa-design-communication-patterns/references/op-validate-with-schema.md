---
operation: validate-with-schema
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-design-communication-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Validate with Shared Schema

## When to Use

Trigger this operation when:
- Validating a design document before submission
- Checking document structure conforms to requirements
- Verifying frontmatter fields are complete and correct
- Ensuring data integrity before GitHub integration

## Prerequisites

- eaa-design-communication-patterns skill directory accessible
- Python environment configured with eaa_shared module in path
- Schemas defined in `schemas/` subdirectory
- Document data in dict or YAML format

## Procedure

### Step 1: Import Schema Validation

```python
from eaa_shared.schemas import validate_design
```

### Step 2: Prepare Document Data

```python
# From YAML frontmatter or dict
document = {
    "title": "Auth Service Architecture",
    "uuid": "PROJ-SPEC-20250129-a1b2c3d4",
    "status": "draft",
    "author": "eaa-architect-main-agent",
    "type": "SPEC"
}
```

### Step 3: Run Validation

```python
errors = validate_design(document)
if errors:
    print(f"Validation failed: {errors}")
else:
    print("Document is valid")
```

### Step 4: Handle Validation Results

```python
if errors:
    for error in errors:
        print(f"  - {error}")
    raise ValueError("Document validation failed")
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify which schema applies (design, adr, rfc, etc.)
- [ ] Ensure eaa-design-communication-patterns is in Python path
- [ ] Import validation function from `eaa_shared.schemas`
- [ ] Parse document into dict format
- [ ] Run validation
- [ ] If errors exist, fix them before proceeding
- [ ] If no errors, proceed with operation

## Examples

### Example: Validate Design Document Before GitHub Issue Creation

```python
from eaa_shared.schemas import validate_design
import yaml

# Load document frontmatter
with open("docs/design/specs/auth-service.md", "r") as f:
    content = f.read()
    # Extract frontmatter between --- markers
    frontmatter = yaml.safe_load(content.split("---")[1])

# Validate
errors = validate_design(frontmatter)

if errors:
    print("Cannot create GitHub issue - document has errors:")
    for error in errors:
        print(f"  - {error}")
    exit(1)

# Proceed with GitHub issue creation
print("Document valid - creating GitHub issue...")
```

### Example: Validate with Specific Schema Type

```python
from eaa_shared.schemas import validate_adr, validate_rfc

# Validate ADR
adr_data = {
    "adr_number": "001",
    "title": "Use PostgreSQL",
    "status": "Proposed",
    "context": "Need a database",
    "decision": "Use PostgreSQL",
    "consequences": "Need expertise"
}

errors = validate_adr(adr_data)
if errors:
    print(f"ADR validation failed: {errors}")

# Validate RFC
rfc_data = {
    "rfc_number": "RFC-001",
    "title": "API v2 Design",
    "status": "Draft",
    "summary": "New API version"
}

errors = validate_rfc(rfc_data)
if errors:
    print(f"RFC validation failed: {errors}")
```

### Example: Batch Validate All Design Documents

```python
from pathlib import Path
from eaa_shared.schemas import validate_design
import yaml

design_dir = Path("docs/design/specs")
all_valid = True

for doc_path in design_dir.glob("*.md"):
    with open(doc_path, "r") as f:
        content = f.read()
        try:
            frontmatter = yaml.safe_load(content.split("---")[1])
            errors = validate_design(frontmatter)

            if errors:
                print(f"INVALID: {doc_path.name}")
                for error in errors:
                    print(f"  - {error}")
                all_valid = False
            else:
                print(f"VALID: {doc_path.name}")
        except Exception as e:
            print(f"ERROR parsing {doc_path.name}: {e}")
            all_valid = False

if all_valid:
    print("\nAll documents valid!")
else:
    print("\nSome documents have validation errors.")
```

## Required Fields by Schema

### Design Document Schema

| Field | Required | Type | Validation |
|-------|----------|------|------------|
| `title` | Yes | string | Non-empty |
| `uuid` | Yes | string | Matches UUID pattern |
| `status` | Yes | string | One of VALID_STATUSES |
| `author` | Yes | string | Non-empty |
| `type` | Yes | string | One of DESIGN_TYPES |
| `created` | No | string | ISO date format |
| `updated` | No | string | ISO date format |
| `related_issues` | No | list | List of issue references |

### ADR Schema

| Field | Required | Type | Validation |
|-------|----------|------|------------|
| `adr_number` | Yes | string | Numeric string |
| `title` | Yes | string | Non-empty |
| `status` | Yes | string | Proposed, Accepted, Deprecated, Superseded |
| `context` | Yes | string | Non-empty |
| `decision` | Yes | string | Non-empty |
| `consequences` | Yes | string | Non-empty |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ModuleNotFoundError: eaa_shared` | Module not in path | Add eaa-design-communication-patterns to Python path |
| `KeyError: missing required field` | Field not in document | Add the required field |
| `ValueError: invalid status` | Status not in allowed values | Use valid status from VALID_STATUSES |
| `ValueError: invalid UUID format` | UUID malformed | Generate new UUID with correct format |
| `yaml.YAMLError` | Malformed YAML | Fix YAML syntax in frontmatter |

## Related Operations

- [op-load-shared-template.md](op-load-shared-template.md) - Templates produce schema-valid output
- [op-access-shared-constants.md](op-access-shared-constants.md) - Constants define valid values
- [op-generate-design-uuid.md](../../../eaa-github-integration/references/op-generate-design-uuid.md) - Generate valid UUID
