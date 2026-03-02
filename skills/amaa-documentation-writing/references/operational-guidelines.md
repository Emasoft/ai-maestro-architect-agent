# Operational Guidelines

Guidelines for document creation, updates, organization, and version control.

---

## Table of Contents

- 1. When to Create New Documents
- 2. When to Update Existing Documents
- 3. Document Organization
- 4. Version Control
- 5. Troubleshooting

---

## 1. When to Create New Documents

Create new documentation when:

| Trigger | Document Type |
|---------|---------------|
| New feature or module is planned | Module Specification |
| Architectural decision is made | ADR |
| New process or workflow is established | Process Documentation |
| Knowledge gap is identified during development | FAQ / Guide |
| Post-mortem analysis is completed | Lessons Learned |

---

## 2. When to Update Existing Documents

Update documentation when:

| Trigger | Action |
|---------|--------|
| Implementation reveals spec inaccuracies | Correct spec to match reality |
| Architecture changes impact existing docs | Update all affected documents |
| User feedback identifies confusion | Clarify and add examples |
| New edge cases are discovered | Add to error handling section |
| Technology upgrades change behavior | Update configuration and examples |

---

## 3. Document Organization

### Folder Structure

```
docs/
  README.md                  # Main index
  module-specs/              # Module specifications
  api-contracts/             # API documentation
  adrs/                      # Architecture Decision Records
  workflows/                 # Process documentation
  glossary.md                # Terminology definitions

docs_dev/
  requirements/              # User requirements
    USER_REQUIREMENTS.md     # Immutable user requirements
```

### Naming Conventions

| Document Type | Pattern | Example |
|---------------|---------|---------|
| Module Spec | `{module-name}.md` | `authentication.md` |
| API Contract | `{service}-endpoints.md` | `auth-endpoints.md` |
| ADR | `adr-{number}-{title}.md` | `adr-005-jwt-authentication.md` |
| Workflow | `{process-name}-workflow.md` | `deployment-workflow.md` |

### Best Practices

- Use hierarchical folder structure
- Name files descriptively (no abbreviations)
- Create index/README in each folder
- Tag documents with categories
- Maintain a global glossary

---

## 4. Version Control

### Commit Messages

```
docs: add authentication module specification

- Created module-specs/authentication.md
- Added API contract for auth endpoints
- Updated README with links
```

### Branching

- Use branches for major documentation overhauls
- Review documentation changes in PRs
- Keep changelog for major specification documents

### Tracking Changes

- All documentation in Git repository
- Commit messages explain what changed and why
- Include "Last Updated" timestamp in documents

---

## 5. Troubleshooting

### Issue: Documentation becomes inconsistent across files

**Solution**:
- Maintain a global glossary (`/docs/glossary.md`)
- Use find-and-replace for terminology updates
- Create documentation review checklist
- Use automated linting (e.g., vale, markdownlint)

### Issue: Specifications are too abstract for implementation

**Solution**:
- Add concrete code examples for every concept
- Include input/output examples
- Specify error conditions explicitly
- Provide decision trees for conditional logic

### Issue: Documentation becomes outdated quickly

**Solution**:
- Add "Last Updated" dates to all documents
- Schedule regular documentation audits
- Link documentation to code via comments
- Create documentation update checklist for code changes

### Issue: Too much documentation, hard to find information

**Solution**:
- Create layered documentation (overview -> details)
- Use descriptive file names and folder structure
- Maintain comprehensive README files
- Implement documentation search tool
