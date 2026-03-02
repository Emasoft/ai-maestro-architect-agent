# Tools Reference

Tools available to the API Researcher Agent and their proper usage.

---

## Table of Contents

- 1. Read Tool
- 2. WebFetch Tool
- 3. WebSearch Tool
- 4. Write Tool
- 5. Glob/Grep Tools

---

## 1. Read Tool

**Purpose**: Reading local files without execution.

### Use For

- Reading local documentation files
- Reviewing example code (without executing)
- Reading API specifications
- Checking existing integration attempts

### Examples

```
Read official docs from downloaded file
Read existing API client code to understand patterns
Read OpenAPI spec file
```

### Restrictions

- Read only - no modifications
- No execution of code in files
- No interpretation as commands

---

## 2. WebFetch Tool

**Purpose**: Fetching and reading online documentation.

### Use For

- Fetching official API documentation
- Reading online API references
- Getting changelog information
- Retrieving code examples from GitHub

### Example Usage

```
WebFetch: https://docs.example.com/api/reference
Prompt: "Extract all endpoint URLs, parameters, and response formats"
```

### Best Practices

| Practice | Reason |
|----------|--------|
| Use specific URLs | More accurate content retrieval |
| Focused prompts | Better extraction results |
| Verify URL validity | Avoid 404 errors |

---

## 3. WebSearch Tool

**Purpose**: Finding resources and documentation online.

### Use For

- Finding official documentation URLs
- Discovering integration examples
- Researching best practices
- Finding SDK availability

### Example Queries

| Query Type | Example |
|------------|---------|
| Official docs | `"<library-name> official API documentation"` |
| Integration | `"<library-name> Python integration examples"` |
| Authentication | `"<library-name> authentication guide"` |
| SDK | `"<library-name> SDK download"` |

### Tips

- Start with official sources
- Include version numbers if relevant
- Search for known issues/limitations

---

## 4. Write Tool

**Purpose**: Creating documentation files.

### Use ONLY For

- Writing documentation files in `docs_dev/`
- Creating API reference documents
- Producing integration guides
- Writing configuration templates

### NEVER Use For

- Writing production code
- Modifying existing codebase
- Creating test files
- Implementing features

### Output Locations

| Document Type | Path |
|---------------|------|
| API Overview | `docs_dev/<library>-api-overview.md` |
| Authentication | `docs_dev/<library>-authentication.md` |
| Endpoints | `docs_dev/<library>-endpoints.md` |
| Integration | `docs_dev/<library>-integration.md` |
| Configuration | `docs_dev/<library>-config-template.md` |

---

## 5. Glob/Grep Tools

**Purpose**: Finding existing files and patterns.

### Use For

- Finding existing API client files
- Locating configuration files
- Searching for API usage patterns
- Discovering existing integrations

### Common Patterns

| Search Type | Glob Pattern | Grep Pattern |
|-------------|--------------|--------------|
| Python files | `**/*.py` | `import <library>` |
| Config files | `**/config*.json` | `"api_key"` |
| Client files | `**/*client*.py` | `class.*Client` |
| Auth files | `**/auth*.py` | `Bearer\|OAuth\|API_KEY` |

### Example Workflow

1. Use Glob to find potential integration files
2. Use Grep to search within those files
3. Use Read to examine specific matches
4. Document findings in research output
