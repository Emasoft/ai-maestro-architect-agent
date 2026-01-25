# Agent Interactions

How the Documentation Writer Agent interacts with other agents in the Architect Agent system.

---

## Table of Contents

- 1. Upstream Agents (Receive Input From)
- 2. Downstream Agents (Provide Output To)
- 3. Peer Agents (Bidirectional)
- 4. Handoff Protocol

---

## 1. Upstream Agents (Receive Input From)

### Team Orchestrator
- **Receives**: High-level project goals, milestone definitions, feature breakdowns
- **Provides**: Project documentation structure, milestone tracking documents
- **Handoff Format**: Structured task assignments with context and deliverables

### Modularizer Expert
- **Receives**: Module decomposition, platform requirements, dependency graphs
- **Provides**: Formal specifications ready for implementation
- **Handoff Format**: Module specifications with platform targets and build system design

### DevOps Expert
- **Receives**: CI/CD requirements, platform targets
- **Provides**: Pipeline documentation, workflow configurations
- **Handoff Format**: GitHub Actions workflows, secret management docs

### Planner
- **Receives**: Implementation plans, task sequences, resource allocations
- **Provides**: Process documentation, workflow guides
- **Handoff Format**: Planning documents with timelines and dependencies

### API Researcher
- **Receives**: API research findings, usage patterns, integration notes
- **Provides**: Consolidated API reference documentation
- **Handoff Format**: Research reports with code examples

---

## 2. Downstream Agents (Provide Output To)

### Remote Developer Agents (via AI Maestro)
- **Provides**: Module specifications, interface contracts, implementation guidelines
- **Format**: Markdown specs with code examples and acceptance criteria
- **Enables**: Remote agents implement modules independently via AI Maestro messaging

### Integration Verifier
- **Provides**: Integration test specifications, expected behaviors
- **Format**: Test scenario descriptions, success criteria
- **Enables**: Automated verification of integration points

### PR Evaluator
- **Provides**: Compliance checklists, documentation standards
- **Format**: Evaluation criteria, required documentation sections
- **Enables**: Consistent PR evaluation against standards

### Report Generator
- **Provides**: Documentation templates, style guides
- **Format**: Markdown templates with placeholders
- **Enables**: Consistent report formatting

---

## 3. Peer Agents (Bidirectional)

### Checklist Compiler
- **Exchange**: Documentation quality checklists <-> Checklist formatting standards
- **Purpose**: Ensure documentation meets quality gates

### GitHub Sync Agent
- **Exchange**: Documentation files <-> Repository structure requirements
- **Purpose**: Maintain documentation in version control

---

## 4. Handoff Protocol

### Receiving Assignments from Orchestrator

```markdown
**Task**: Document the authentication module specification
**Context**: JWT-based auth, 15-min sessions, Redis storage
**Inputs**: Module decomposition from Modularizer Expert
**Deliverables**:
  - Module specification (module-specs/authentication.md)
  - API contract (api-contracts/auth-endpoints.md)
  - ADR for JWT decision (adrs/adr-005-jwt-authentication.md)
**Dependencies**: Await API Researcher findings on JWT libraries
```

### Delivering Completed Documentation

```markdown
**Deliverable**: Authentication Module Documentation
**Files Created**:
  - `/docs/module-specs/authentication.md` (2,450 words, 15 code examples)
  - `/docs/api-contracts/auth-endpoints.md` (1,200 words, OpenAPI 3.0 format)
  - `/docs/adrs/adr-005-jwt-authentication.md` (800 words)
**Cross-References Added**:
  - Updated `/docs/README.md` with new links
  - Referenced in `/docs/architecture/system-overview.md`
**Review Status**: Ready for Team Orchestrator review
**Next Steps**: Await approval, then send specs to Remote Developer Agents via AI Maestro
```
