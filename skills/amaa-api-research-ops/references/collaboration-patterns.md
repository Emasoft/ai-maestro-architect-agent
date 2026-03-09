# Collaboration Patterns

Patterns for interacting with the orchestrator and other agents.

---

## Table of Contents

- 1. Integration with Orchestrator
- 2. Handling Blockers
- 3. Handoff Protocol
- 4. Collaboration with Other Agents
- 5. Best Practices

---

## 1. Integration with Orchestrator

### 1.1 Receiving Tasks

**Orchestrator Request Format:**

```markdown
Task: Research <library-name> API for <functionality>
Scope: <what specifically needs to be documented>
Context: <how this will be used in the project>
Deliverables: <specific documentation needed>
```

**Your Acknowledgment:**

```markdown
[ACKNOWLEDGED] <library-name> API research
- Starting with: official documentation
- Will produce: <list of deliverables>
```

### 1.2 Reporting Progress

Use minimal updates to avoid consuming orchestrator context:

```markdown
[PROGRESS] <library-name> API
- Phase: <current phase>
- Found: <key discovery>
```

### 1.3 Delivering Results

**Final Report Format:**

```markdown
[DONE] <library-name> API research complete
- Documentation: docs_dev/<library>-*.md (<count> files)
- Key insight: <most important finding in one line>
- Authentication: <method identified>
- Rate limits: <critical limit info>
- Ready for: code implementation
- Recommendation: <any critical advice>
```

**Attach file list:**

```
Created:
- docs_dev/<library>-api-overview.md
- docs_dev/<library>-authentication.md
- docs_dev/<library>-endpoints.md
- docs_dev/<library>-integration.md
- docs_dev/<library>-config-template.md
```

---

## 2. Handling Blockers

### 2.1 Documentation Not Found

```markdown
[BLOCKED] <library-name> API research
- Issue: Official documentation not accessible
- Attempted: <sources tried>
- Need: Human to provide documentation URL or access
- Alternatives explored: <what else was tried>
```

### 2.2 API Deprecated

```markdown
[ALERT] <library-name> API is deprecated
- Status: Deprecated as of <date>
- Replacement: <recommended alternative>
- Migration guide: <URL if available>
- Recommendation: Switch to <alternative>
```

### 2.3 Multiple Versions

```markdown
[QUESTION] <library-name> has multiple API versions
- Found: v1, v2, v3
- Latest: v3
- Most stable: v2
- Question: Which version should I document?
- Recommendation: <your assessment>
```

---

## 3. Handoff Protocol

### 3.1 Handoff Report Format

```markdown
[DONE] <library-name> API research complete

**Documentation Created:**
- docs_dev/<library>-api-overview.md
- docs_dev/<library>-authentication.md
- docs_dev/<library>-endpoints.md
- docs_dev/<library>-integration.md
- docs_dev/<library>-config-template.md

**Key Findings:**
- Authentication: <method>
- Rate Limits: <critical limits>
- Key Insight: <most important discovery>

**Ready For:**
- Implementation by code-writer agent
- Integration by feature-builder agent

**Recommendations:**
- <any critical advice or warnings>

**Blockers/Issues:**
- <list any issues encountered, or "None">
```

### 3.2 Return to Orchestrator

Once handoff report is sent:

| Action | Status |
|--------|--------|
| Await further instructions | Required |
| Be ready to clarify questions | Required |
| Begin implementation work | PROHIBITED |
| Create code files | PROHIBITED |
| Remain available for follow-up | Required |

---

## 4. Collaboration with Other Agents

### 4.1 With Code-Writer Agent

| You Provide | They Implement |
|-------------|----------------|
| API documentation | Actual code |
| Integration guide | API client |
| Configuration template | Error handling |
| Authentication details | Tests |

### 4.2 With Documentation-Writer Agent

| You Provide | They Create |
|-------------|-------------|
| Technical API details | User-facing documentation |
| Integration patterns | Tutorials |
| Configuration options | How-to guides |
| - | Public API docs |

### 4.3 With Requirements-Analyst Agent

| You Provide | They Decide |
|-------------|-------------|
| API capabilities | Whether to use this API |
| Limitations | Alternative options |
| Feasibility assessment | Requirements fit |

---

## 5. Best Practices

### 5.1 Always Cite Sources

- Include URLs to official documentation
- Note version numbers
- Date your research

### 5.2 Be Thorough but Concise

- Document all essential information
- Avoid unnecessary verbosity
- Use templates for consistency

### 5.3 Stay Current

- Check for latest API version
- Note deprecations
- Include migration guides

### 5.4 Think Like an Implementer

- What would a developer need to know?
- What configurations are required?
- What errors might occur?

### 5.5 Document the Unknown

- If something is unclear, note it
- Suggest where to find more info
- Flag areas needing human verification

### 5.6 Organize Systematically

- Use consistent file naming
- Follow template structures
- Create indexes when needed

### 5.7 Never Assume

- Verify everything
- Use official sources
- Don't guess at behavior
