# Research Procedure

Step-by-step procedure for conducting API research.

---

## Table of Contents

- 1. Step 1: Understand Requirements
- 2. Step 2: Gather Information
- 3. Step 3: Document Findings
- 4. Step 4: Report to Orchestrator

---

## 1. Step 1: Understand Requirements

### Input from Orchestrator

| Field | Description |
|-------|-------------|
| Library/service name | The API or library to research |
| Specific functionality | What features need to be documented |
| Integration context | How it will be used in the project |
| Constraints | Rate limits, auth methods, etc. |

### Acknowledgment Format

```markdown
[RESEARCH STARTED] <library-name> API - <specific-functionality>
- Target: <service/library>
- Scope: <what needs to be researched>
- Output: <deliverable type>
```

### Verification Checklist

- [ ] Library/service name is clearly identified
- [ ] Specific API functionality scope is understood
- [ ] Integration context is documented
- [ ] Any constraints are noted
- [ ] Acknowledgment message sent to orchestrator

---

## 2. Step 2: Gather Information

### Sources to Consult (in order)

#### 2.1 Official Documentation

- Use WebFetch to read official docs
- Look for API reference sections
- Find authentication guides
- Check for SDK documentation

#### 2.2 API Specifications

- OpenAPI/Swagger specs
- GraphQL schemas
- REST API documentation
- gRPC proto files

#### 2.3 Code Examples

- Official example repositories
- Community examples (GitHub)
- Stack Overflow patterns
- Integration tutorials

#### 2.4 Version Information

- Current stable version
- Breaking changes between versions
- Deprecation notices
- Migration guides

### Information Verification Checklist

- [ ] Official documentation URL found and verified
- [ ] Authentication method identified
- [ ] Base URL/endpoint structure documented
- [ ] Required parameters cataloged
- [ ] Response formats documented
- [ ] Error codes and handling noted
- [ ] Rate limits identified
- [ ] SDK availability checked
- [ ] Code examples reviewed
- [ ] Best practices gathered

---

## 3. Step 3: Document Findings

### Document Types to Create

| Document | Location | Content |
|----------|----------|---------|
| API Overview | `docs_dev/<library>-api-overview.md` | Capabilities, limitations, pricing |
| Authentication Guide | `docs_dev/<library>-authentication.md` | Setup, flow, security |
| Endpoints Reference | `docs_dev/<library>-endpoints.md` | All endpoints with params |
| Integration Guide | `docs_dev/<library>-integration.md` | Step-by-step integration |
| Configuration Template | `docs_dev/<library>-config-template.md` | Env vars, config options |

### Verification Checklist

- [ ] API Overview Document created with all required sections
- [ ] Authentication Guide completed with step-by-step setup
- [ ] Endpoints Reference includes all relevant endpoints
- [ ] Integration Guide provides clear implementation pathway
- [ ] Configuration Template includes all necessary options
- [ ] All documents follow standard templates
- [ ] Documents are saved in `docs_dev/` directory

---

## 4. Step 4: Report to Orchestrator

### Minimal Report Format

```markdown
[DONE] <library-name> API research complete
- Docs: docs_dev/<library>-*.md (5 files)
- Key finding: <one critical insight>
- Ready for: implementation by code-writer agent
```

### Verification Checklist

- [ ] All documentation files created
- [ ] File count matches deliverables
- [ ] Key findings summarized in one line
- [ ] Critical insights highlighted
- [ ] Next steps clearly identified
- [ ] Minimal report sent to orchestrator
