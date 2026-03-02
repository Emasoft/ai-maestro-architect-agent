---
operation: access-shared-constants
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-design-communication-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Access Shared Constants


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Import Required Constants](#step-1-import-required-constants)
  - [Step 2: Use Constants in Validation](#step-2-use-constants-in-validation)
  - [Step 3: Use Constants in Configuration](#step-3-use-constants-in-configuration)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Validate Design Document Status](#example-validate-design-document-status)
  - [Example: Validate Design Type](#example-validate-design-type)
  - [Example: Use Priority Levels](#example-use-priority-levels)
- [Available Constants](#available-constants)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Trigger this operation when:
- Need standard status values for design documents
- Validating input against allowed values
- Using consistent configuration across skills
- Referencing priority levels, timeouts, or other standard values

## Prerequisites

- eaa-design-communication-patterns skill directory accessible
- Python environment configured with eaa_shared module in path
- Constants defined in `constants/` subdirectory

## Procedure

### Step 1: Import Required Constants

```python
from eaa_shared.constants import (
    VALID_STATUSES,
    PRIORITY_LEVELS,
    DEFAULT_TIMEOUT,
    DESIGN_TYPES,
    MESSAGE_TYPES
)
```

### Step 2: Use Constants in Validation

```python
# Validate a status value
if status not in VALID_STATUSES:
    raise ValueError(f"Invalid status: {status}. Must be one of: {VALID_STATUSES}")
```

### Step 3: Use Constants in Configuration

```python
# Use default timeout
timeout = kwargs.get("timeout", DEFAULT_TIMEOUT)

# Use priority levels
priority = PRIORITY_LEVELS["high"]
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify which constants are needed
- [ ] Verify eaa-design-communication-patterns is in Python path
- [ ] Import constants from `eaa_shared.constants`
- [ ] Use constants in validation logic
- [ ] Do NOT hardcode values that exist as constants
- [ ] Update usage if constants change in future versions

## Examples

### Example: Validate Design Document Status

```python
from eaa_shared.constants import VALID_STATUSES

def validate_design_status(status: str) -> bool:
    """Validate that status is an allowed value."""
    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. "
            f"Must be one of: {', '.join(VALID_STATUSES)}"
        )
    return True

# Usage
validate_design_status("draft")      # OK
validate_design_status("approved")   # OK
validate_design_status("invalid")    # Raises ValueError
```

### Example: Validate Design Type

```python
from eaa_shared.constants import DESIGN_TYPES

def create_design(doc_type: str, title: str):
    """Create a design document of specified type."""
    if doc_type not in DESIGN_TYPES:
        raise ValueError(
            f"Invalid design type '{doc_type}'. "
            f"Must be one of: {', '.join(DESIGN_TYPES)}"
        )

    # Proceed with creation...
    print(f"Creating {doc_type}: {title}")

# Valid types: SPEC, ADR, RFC, GUIDE, PLAN
create_design("SPEC", "Auth Service")  # OK
create_design("ADR", "Database Choice")  # OK
```

### Example: Use Priority Levels

```python
from eaa_shared.constants import PRIORITY_LEVELS

def send_notification(message: str, priority: str = "normal"):
    """Send notification with specified priority."""
    if priority not in PRIORITY_LEVELS:
        priority = "normal"

    priority_value = PRIORITY_LEVELS[priority]

    # Use numeric value for sorting/comparison
    print(f"Sending message (priority {priority_value}): {message}")

# Priority levels: urgent=1, high=2, normal=3, low=4
send_notification("Design approved", priority="high")
```

## Available Constants

| Constant | Type | Values | Purpose |
|----------|------|--------|---------|
| `VALID_STATUSES` | Set[str] | draft, review, approved, implementing, completed, deprecated | Valid design document statuses |
| `DESIGN_TYPES` | Set[str] | SPEC, ADR, RFC, GUIDE, PLAN | Valid design document types |
| `PRIORITY_LEVELS` | Dict[str, int] | urgent=1, high=2, normal=3, low=4 | AI Maestro message priorities |
| `MESSAGE_TYPES` | Set[str] | request, response, notification, handoff | AI Maestro message types |
| `DEFAULT_TIMEOUT` | int | 30 | Default operation timeout in seconds |
| `MAX_RETRIES` | int | 3 | Maximum retry attempts |
| `POLL_INTERVAL` | int | 5 | Default polling interval in seconds |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ModuleNotFoundError: eaa_shared` | Module not in path | Add eaa-design-communication-patterns to Python path |
| `ImportError: cannot import CONSTANT` | Constant not defined | Check constant name spelling; verify version |
| `KeyError` on dict constant | Invalid key used | Use only documented keys |
| `TypeError: unhashable type` | Using list instead of set | Use `in` operator, not index |

## Related Operations

- [op-load-shared-template.md](op-load-shared-template.md) - Use templates that reference constants
- [op-validate-with-schema.md](op-validate-with-schema.md) - Schemas reference these constants
- [op-send-ai-maestro-message.md](op-send-ai-maestro-message.md) - Uses PRIORITY_LEVELS and MESSAGE_TYPES
