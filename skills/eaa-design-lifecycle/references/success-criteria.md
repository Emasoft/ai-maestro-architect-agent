# Success Criteria

## Table of Contents

1. [Overview](#overview)
2. [Requirements Captured](#requirements-captured)
3. [Architecture Designed](#architecture-designed)
4. [APIs Researched](#apis-researched)
5. [Modules Specified](#modules-specified)
6. [Handoff Prepared](#handoff-prepared)

---

## Overview

Every architecture phase has specific completion criteria. Use these to self-verify before handoff.

---

## Requirements Captured

### Criteria

- [ ] All user requirements extracted (verbatim quotes in USER_REQUIREMENTS.md)
- [ ] Ambiguities identified and logged
- [ ] Clarification requests sent to ECOS (if needed)
- [ ] Functional requirements separated from non-functional
- [ ] Constraints documented (technical, budget, timeline, resources)
- [ ] Dependencies identified (internal systems, external APIs, team skills)
- [ ] Success metrics defined (performance, scale, availability)

### Evidence Files

- `docs_dev/design/USER_REQUIREMENTS.md`
- `docs_dev/design/requirements-log.md` (with timestamp entries)
- `docs_dev/design/clarifications/` (if any)

### Self-Check Question

"Can EOA implement this without asking me what the user wanted?"

---

## Architecture Designed

### Criteria

- [ ] System components identified with clear boundaries
- [ ] Component interactions defined (APIs, events, data flows)
- [ ] Technology stack specified (languages, frameworks, databases with versions)
- [ ] Data models designed (schemas, relationships, constraints)
- [ ] Integration points documented (external APIs, webhooks, queues)
- [ ] Non-functional requirements addressed (performance, security, scalability)
- [ ] Architectural decisions recorded in ADRs (for significant choices)
- [ ] Deployment architecture specified (hosting, CI/CD, monitoring)

### Evidence Files

- `docs_dev/design/architecture.md` (with Mermaid diagrams)
- `docs_dev/design/adrs/` (for key decisions)
- `docs_dev/design/data-models.md`
- `docs_dev/design/integration-points.md`

### Self-Check Question

"Can a new developer understand the system from these documents alone?"

---

## APIs Researched

### Criteria

- [ ] All external APIs identified and validated
- [ ] Authentication methods documented (API keys, OAuth2, JWT)
- [ ] Rate limits and quotas documented
- [ ] Error handling strategies defined (retries, fallbacks, circuit breakers)
- [ ] Cost estimates calculated (per request, monthly projections)
- [ ] API stability assessed (versioning, deprecation policies)
- [ ] Alternatives considered and compared (if applicable)
- [ ] Integration risks identified (downtime, breaking changes)

### Evidence Files

- `docs_dev/design/api-research/` (one file per API)
- `docs_dev/design/api-comparison.md` (if multiple options)

### Self-Check Question

"Can EOA integrate this API without further research?"

---

## Modules Specified

### Criteria

- [ ] Each module has single responsibility
- [ ] Module boundaries clear (inputs, outputs, side effects)
- [ ] Dependencies between modules explicit (dependency graph)
- [ ] Implementation order defined (foundation → features → integration)
- [ ] Test strategy per module (unit, integration, e2e)
- [ ] Acceptance criteria defined (what "done" means)
- [ ] Estimated scope (files, LOC, complexity: Simple/Medium/Complex)

### Evidence Files

- `docs_dev/design/modules/` (one file per module)
- `docs_dev/design/module-dependency-graph.md` (Mermaid graph)

### Self-Check Question

"Can each module be implemented and tested independently?"

---

## Handoff Prepared

### Criteria

- [ ] All design artifacts complete and reviewed
- [ ] Implementation sequence defined (which modules first)
- [ ] Risks identified and mitigation strategies documented
- [ ] Open questions resolved or escalated
- [ ] Handoff document created with all file paths
- [ ] Success criteria defined for EOA (how to know implementation is correct)

### Evidence Files

- `docs_dev/design/handoff-{uuid}.md`
