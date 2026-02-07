---
procedure: support-skill
workflow-instruction: support
---

# Operation: Research Python Library

## Purpose

Research and document a Python library, producing comprehensive documentation covering installation, usage, API reference, and integration patterns.

## When to Use

- Assigned to research a Python library for project use
- Evaluating library capabilities before adoption
- Creating library documentation for team reference

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Library name | Orchestrator assignment | Yes |
| Scope/focus area | Orchestrator assignment | Yes |
| PyPI package name | Research | Yes |

## Procedure

### Step 1: Acknowledge Assignment

Format: `[RESEARCH STARTED] <library-name> library - <scope>`

### Step 2: Locate Documentation Sources

Search order:
1. PyPI page (`https://pypi.org/project/<library-name>/`)
2. Official documentation site (usually linked from PyPI)
3. GitHub repository (README, docs/ folder)
4. Read the Docs page (if available)

### Step 3: Gather Core Information

Collect:
- Current version and Python compatibility
- Installation command (`pip install <name>`)
- Dependencies (direct and optional)
- Main modules and classes
- Common usage patterns
- Configuration options

### Step 4: Document Installation

Verify:
- [ ] pip install command confirmed working
- [ ] Python version requirements noted
- [ ] Optional dependencies documented
- [ ] Virtual environment setup noted

### Step 5: Document Key API

For main classes/functions:
- Import path
- Constructor/function signature
- Parameters with types and descriptions
- Return values
- Common usage examples
- Edge cases and limitations

### Step 6: Create Output Documents

Create all 5 documents:
1. `<library-name>-api-overview.md` - Overview and capabilities
2. `<library-name>-authentication.md` - Setup and credentials (if applicable)
3. `<library-name>-endpoints.md` - Key methods/classes reference
4. `<library-name>-integration.md` - Usage patterns and examples
5. `<library-name>-config-template.md` - Configuration options

### Step 7: Report Completion

Format: `[DONE] <library-name> library research complete`

## Output

| File | Content |
|------|---------|
| `<library-name>-api-overview.md` | Purpose, features, when to use |
| `<library-name>-authentication.md` | Setup, credentials if needed |
| `<library-name>-endpoints.md` | Key classes and methods |
| `<library-name>-integration.md` | Code examples, patterns |
| `<library-name>-config-template.md` | Configuration, environment setup |

## Verification Checklist

- [ ] PyPI page reviewed
- [ ] Official docs consulted
- [ ] Installation tested (or verified)
- [ ] Key API documented with examples
- [ ] All 5 output documents created
- [ ] Completion reported to orchestrator

## Example

```
Orchestrator: Research the requests library for HTTP calls
Agent: [RESEARCH STARTED] requests library - HTTP client scope

1. PyPI: https://pypi.org/project/requests/
2. Docs: https://docs.python-requests.org/
3. Key methods: get(), post(), put(), delete()
4. Auth options: Basic, Digest, OAuth
5. Created 5 documentation files

[DONE] requests library research complete
```

## Error Handling

| Error | Solution |
|-------|----------|
| Library not on PyPI | Check alternative sources (GitHub, conda) |
| Sparse documentation | Document from source code, note gaps |
| Version incompatibility | Document compatible Python versions |
