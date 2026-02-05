---
name: eaa-design-communication-patterns
description: Use when accessing shared utilities, templates, and constants across Architect Agent skills. Trigger with shared template access or common utility imports.
version: 1.0.0
compatibility: Requires AI Maestro installed.
context: fork
agent: eaa-planner
user-invocable: false
triggers:
  - when needing shared templates
  - when accessing common utilities
  - when using shared constants
---

# Shared Resources Skill

## Overview

This skill provides shared utilities, templates, and constants used across all Architect Agent skills. It ensures consistent behavior and reduces duplication by centralizing common resources.

## Prerequisites

- Access to the eaa-design-communication-patterns skill directory
- Understanding of which resources are available
- Other eaa-* skills that depend on shared resources

## Instructions

1. Check if the resource you need exists in this shared skill
2. Import or reference the shared resource in your skill
3. Follow any usage guidelines specified for each resource type
4. Do not duplicate shared resources in individual skills

### Checklist

Copy this checklist and track your progress:

- [ ] Identify the resource type needed (Template/Script/Constant/Schema)
- [ ] Check if resource exists in eaa-design-communication-patterns skill directory
- [ ] Verify eaa-design-communication-patterns is in Python path (if using scripts)
- [ ] Import or reference the shared resource
- [ ] Follow usage guidelines for the resource type
- [ ] Test that the resource works correctly
- [ ] Do NOT duplicate the resource in your skill

## Shared Resource Types

| Type | Location | Purpose |
|------|----------|---------|
| Templates | `templates/` | Reusable document templates |
| Scripts | `scripts/` | Common utility scripts |
| Constants | `constants/` | Shared configuration values |
| Schemas | `schemas/` | JSON/YAML validation schemas |

## Examples

### Example 1: Using a Shared Template

```python
# In another skill's script
from eaa_shared.templates import load_template

template = load_template("design-document")
filled = template.format(
    title="My Design",
    author="Agent",
    date="2026-01-30"
)
```

### Example 2: Accessing Shared Constants

```python
# In another skill's script
from eaa_shared.constants import (
    VALID_STATUSES,
    PRIORITY_LEVELS,
    DEFAULT_TIMEOUT
)

if status not in VALID_STATUSES:
    raise ValueError(f"Invalid status: {status}")
```

### Example 3: Using Shared Schema Validation

```python
# Validate a design document
from eaa_shared.schemas import validate_design

errors = validate_design(document)
if errors:
    print(f"Validation failed: {errors}")
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Resource not found | Path incorrect | Check resource exists in shared skill |
| Import failed | Module not in path | Ensure eaa-design-communication-patterns is in Python path |
| Schema validation error | Document malformed | Fix document according to schema |
| Template placeholder missing | Incomplete format call | Provide all required placeholders |
| Version mismatch | Outdated shared resource | Update eaa-design-communication-patterns to latest version |

## Output

| Output Type | Format | Description |
|-------------|--------|-------------|
| Templates | Markdown/Text | Filled document templates ready for use |
| Constants | Python variables | Configuration values and enums |
| Validation Results | Boolean/List | Schema validation pass/fail with error details |
| Utility Functions | Python callables | Reusable helper functions |

## References

Detailed reference documentation for communication patterns:

| Reference | Description |
|-----------|-------------|
| [ai-maestro-message-templates.md](references/ai-maestro-message-templates.md) | AI Maestro inter-agent message templates and examples |

## Resources

- `templates/` - Reusable document templates
- `scripts/` - Common utility scripts
- `constants/` - Shared configuration values
- `schemas/` - JSON/YAML validation schemas
- eaa-design-lifecycle - Uses shared design templates
- eaa-requirements-analysis - Uses shared validation schemas
- eaa-planning-patterns - Uses shared planning templates
