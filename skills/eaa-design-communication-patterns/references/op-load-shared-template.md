---
operation: load-shared-template
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-design-communication-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Load and Use Shared Templates

## When to Use

Trigger this operation when:
- Creating a new design document that should follow standard format
- Needing consistent document structure across the project
- Generating reports, plans, or specifications from templates

## Prerequisites

- eaa-design-communication-patterns skill directory accessible
- Template exists in `templates/` subdirectory
- Python environment configured with eaa_shared module in path

## Procedure

### Step 1: Identify Required Template

Available templates in `templates/` directory:
- `design-document` - Standard design document structure
- `adr-template` - Architecture Decision Record
- `rfc-template` - Request for Comments
- `implementation-plan` - Implementation plan structure
- `review-checklist` - Design review checklist

### Step 2: Load the Template

```python
from eaa_shared.templates import load_template

template = load_template("design-document")
```

### Step 3: Fill Template with Data

```python
filled = template.format(
    title="My Design",
    author="Agent",
    date="2026-01-30",
    status="draft",
    overview="Design overview text here"
)
```

### Step 4: Write to File or Use Output

```python
# Write to file
with open("docs/design/specs/new-design.md", "w") as f:
    f.write(filled)

# Or return as string for further processing
print(filled)
```

## Checklist

Copy this checklist and track your progress:

- [ ] Identify the template needed (design-document, adr, rfc, etc.)
- [ ] Verify template exists: check `templates/` directory
- [ ] Ensure eaa-design-communication-patterns is in Python path
- [ ] Import `load_template` from `eaa_shared.templates`
- [ ] Load the template by name
- [ ] Identify ALL required placeholders in template
- [ ] Prepare values for each placeholder
- [ ] Call `template.format()` with all required values
- [ ] Verify output is complete (no unfilled placeholders)
- [ ] Write output to file or use as needed

## Examples

### Example: Create New Design Document

```python
from eaa_shared.templates import load_template
from datetime import datetime

# Load the design document template
template = load_template("design-document")

# Fill with data
document = template.format(
    title="Authentication Service Architecture",
    author="eaa-architect-main-agent",
    date=datetime.now().strftime("%Y-%m-%d"),
    status="draft",
    overview="This document describes the authentication service architecture.",
    requirements="- OAuth2 support\n- JWT tokens\n- Session management",
    design="The service will use a modular design with...",
    risks="- Complexity of OAuth2 flows\n- Token security"
)

# Write to file
with open("docs/design/specs/auth-service.md", "w") as f:
    f.write(document)

print("Created: docs/design/specs/auth-service.md")
```

### Example: Create ADR from Template

```python
from eaa_shared.templates import load_template

template = load_template("adr-template")

adr = template.format(
    adr_number="001",
    title="Use PostgreSQL for Primary Database",
    date="2026-01-30",
    status="Proposed",
    context="We need a reliable relational database for our application.",
    decision="We will use PostgreSQL 15 as our primary database.",
    consequences="- Need PostgreSQL expertise\n- Good performance for our use case",
    alternatives="- MySQL: Less feature-rich\n- MongoDB: Not suitable for relational data"
)

with open("docs/design/adrs/adr-001.md", "w") as f:
    f.write(adr)
```

## Template Placeholders

Each template has specific placeholders. Common ones include:

| Placeholder | Required | Description |
|-------------|----------|-------------|
| `{title}` | Yes | Document title |
| `{author}` | Yes | Author name or agent ID |
| `{date}` | Yes | Creation date (YYYY-MM-DD) |
| `{status}` | Yes | Document status (draft, review, approved) |
| `{overview}` | Varies | Document overview/summary |
| `{requirements}` | Varies | Requirements section content |
| `{design}` | Varies | Design details |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `ModuleNotFoundError: eaa_shared` | Module not in path | Add eaa-design-communication-patterns to Python path |
| `KeyError: template_name` | Template not found | Verify template exists in `templates/` directory |
| `KeyError: placeholder` | Missing format argument | Provide all required placeholders to `format()` |
| `ValueError: incomplete format` | Unfilled placeholders | Check for typos in placeholder names |
| `FileNotFoundError` | Templates directory missing | Verify skill directory structure |

## Related Operations

- [op-access-shared-constants.md](op-access-shared-constants.md) - Access configuration values
- [op-validate-with-schema.md](op-validate-with-schema.md) - Validate filled template output
