---
procedure: support-skill
workflow-instruction: support
---

# Operation: Write Module Specification


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Gather Module Information](#step-1-gather-module-information)
  - [Step 2: Create Module Specification Document](#step-2-create-module-specification-document)
- [Overview](#overview)
  - [Purpose](#purpose)
  - [Responsibilities](#responsibilities)
  - [Non-Responsibilities](#non-responsibilities)
- [Public Interface](#public-interface)
  - [Classes](#classes)
  - [Functions](#functions)
- [Dependencies](#dependencies)
  - [Internal Dependencies](#internal-dependencies)
  - [External Dependencies](#external-dependencies)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Configuration File](#configuration-file)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)
  - [Basic Usage](#basic-usage)
  - [Advanced Usage](#advanced-usage)
- [Performance Considerations](#performance-considerations)
- [Related Modules](#related-modules)
  - [Step 3: Apply Quality Check (6 C's)](#step-3-apply-quality-check-6-cs)
  - [Step 4: Save Document](#step-4-save-document)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Error Handling](#error-handling)

## Purpose

Write a comprehensive module specification document that describes a module's purpose, interfaces, dependencies, configuration, and implementation details.

## When to Use

- Documenting a new module before implementation
- Creating reference documentation for existing modules
- Updating module documentation after changes

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Module name | Assignment | Yes |
| Module purpose | Analysis or assignment | Yes |
| Source code | Repository | If existing |

## Procedure

### Step 1: Gather Module Information

Collect from source code or design:
- Module purpose and responsibilities
- Public interfaces (classes, functions, APIs)
- Dependencies (internal and external)
- Configuration options
- Error handling patterns
- Performance characteristics

### Step 2: Create Module Specification Document

Use this template:

```markdown
# <Module-Name> Module Specification

## Overview

### Purpose

<1-2 paragraphs describing what this module does and why it exists>

### Responsibilities

- <responsibility-1>
- <responsibility-2>
- <responsibility-3>

### Non-Responsibilities

- <what this module does NOT do>

---

## Public Interface

### Classes

#### `ClassName`

<Description of the class>

**Constructor:**
```python
def __init__(self, param1: Type, param2: Type = default) -> None:
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param1` | `Type` | Yes | Description |
| `param2` | `Type` | No | Description (default: value) |

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `method_name` | `arg: Type` | `ReturnType` | What it does |

### Functions

#### `function_name(param1: Type) -> ReturnType`

<Description of the function>

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `param1` | `Type` | Description |

**Returns:** `ReturnType` - Description

**Raises:**
| Exception | Condition |
|-----------|-----------|
| `ValueError` | When param1 is invalid |

---

## Dependencies

### Internal Dependencies

| Module | Purpose |
|--------|---------|
| `module.submodule` | What this module provides |

### External Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `package-name` | `>=1.0.0` | What it's used for |

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MODULE_SETTING` | No | `value` | What it controls |

### Configuration File

```yaml
module_name:
  setting1: value
  setting2: value
```

---

## Error Handling

| Error | Condition | Handling |
|-------|-----------|----------|
| `ModuleError` | When X happens | How to handle |

---

## Usage Examples

### Basic Usage

```python
from module import ClassName

instance = ClassName(param1=value)
result = instance.method()
```

### Advanced Usage

```python
# Advanced example with configuration
```

---

## Performance Considerations

- <Performance note 1>
- <Performance note 2>

---

## Related Modules

- [Related Module 1](related-module-1.md)
- [Related Module 2](related-module-2.md)
```

### Step 3: Apply Quality Check (6 C's)

- [ ] **Complete**: All interfaces documented
- [ ] **Correct**: Matches actual implementation
- [ ] **Clear**: No ambiguous language
- [ ] **Consistent**: Same terminology throughout
- [ ] **Current**: Reflects latest version
- [ ] **Connected**: Links to related docs

### Step 4: Save Document

Save to: `/docs/module-specs/<module-name>.md`

## Output

| File | Location |
|------|----------|
| Module specification | `/docs/module-specs/<module-name>.md` |

## Verification Checklist

- [ ] Purpose clearly stated
- [ ] All public interfaces documented
- [ ] Dependencies listed
- [ ] Configuration documented
- [ ] Error handling explained
- [ ] Usage examples provided
- [ ] 6 C's quality check passed

## Error Handling

| Error | Solution |
|-------|----------|
| Source code unavailable | Request access from orchestrator |
| Interface changes frequently | Note version, add change log |
| Missing dependency info | Check requirements.txt/pyproject.toml |
