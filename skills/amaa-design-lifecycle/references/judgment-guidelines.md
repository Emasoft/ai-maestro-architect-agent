# Design Judgment Guidelines

## Contents

- [1. When to research external APIs instead of using existing documentation](#1-when-to-research-external-apis-instead-of-using-existing-documentation)
  - [1.1 Research External APIs when](#11-research-external-apis-when)
  - [1.2 Use Existing Docs when](#12-use-existing-docs-when)
  - [1.3 Spawn eaa-api-researcher for](#13-spawn-eaa-api-researcher-for)
- [2. When to create an ADR instead of just documenting the decision](#2-when-to-create-an-adr-instead-of-just-documenting-the-decision)
  - [2.1 Create ADR (Architecture Decision Record) when](#21-create-adr-architecture-decision-record-when)
  - [2.2 Just Document in architecture.md when](#22-just-document-in-architecturemd-when)
  - [2.3 ADR Template Location](#23-adr-template-location)
- [3. When to modularize a system instead of keeping it simple](#3-when-to-modularize-a-system-instead-of-keeping-it-simple)
  - [3.1 Spawn eaa-modularizer-expert when](#31-spawn-eaa-modularizer-expert-when)
  - [3.2 Keep Simple (single module) when](#32-keep-simple-single-module-when)
  - [3.3 Modularization Threshold](#33-modularization-threshold)
- [4. When to escalate unclear requirements to ECOS for clarification](#4-when-to-escalate-unclear-requirements-to-ecos-for-clarification)
  - [4.1 Escalate immediately when](#41-escalate-immediately-when)
  - [4.2 Escalation Format](#42-escalation-format)

---

## 1. When to research external APIs instead of using existing documentation

As the Architect, you make daily decisions about depth and scope when dealing with external APIs. Here's when to apply judgment:

### 1.1 Research External APIs when

- API documentation is incomplete or outdated
- Integration requirements are complex (auth, rate limits, webhooks)
- Multiple API options exist and need comparison
- API version changes may affect architecture
- Cost/performance trade-offs need analysis

### 1.2 Use Existing Docs when

- Standard, well-documented APIs (Stripe, AWS, GitHub)
- Internal APIs with up-to-date documentation
- Simple integration (single endpoint, basic auth)
- API already validated by team in previous projects

### 1.3 Spawn eaa-api-researcher for

- 3+ endpoints to integrate
- Complex authentication flows (OAuth2, JWT, custom)
- Rate limiting strategies needed
- Error handling patterns must be defined
- Cost estimation required

---

## 2. When to create an ADR instead of just documenting the decision

### 2.1 Create ADR (Architecture Decision Record) when

- Decision affects multiple modules or teams
- Trade-offs involve significant cost/performance/complexity
- Alternative approaches were seriously considered
- Decision may be questioned or revisited later
- Regulatory/compliance concerns are involved
- Third-party dependencies are chosen

### 2.2 Just Document in architecture.md when

- Standard pattern application (e.g., using REST for API)
- Team convention being followed
- Obvious technical choice (e.g., using SQLite for local dev)
- Implementation detail (e.g., specific library version)

### 2.3 ADR Template Location

`docs_dev/design/adrs/`

---

## 3. When to modularize a system instead of keeping it simple

### 3.1 Spawn eaa-modularizer-expert when

- System has 5+ distinct responsibilities
- Multiple teams will work on different parts
- Components may be replaced independently
- Clear domain boundaries exist
- Parallel development is needed
- Reusability across projects is expected

### 3.2 Keep Simple (single module) when

- Single responsibility
- Small codebase (<1000 lines)
- Single developer/team
- Prototype or proof-of-concept
- Short-lived tool or script

### 3.3 Modularization Threshold

If architecture.md grows beyond 500 lines, consider modularization.

---

## 4. When to escalate unclear requirements to ECOS for clarification

### 4.1 Escalate immediately when

- User requirements conflict with each other
- Technical constraints make requirement infeasible
- Scope exceeds project resources by >30%
- Security/compliance requirements unclear
- External dependencies have unknown availability
- Budget constraints conflict with requirements

### 4.2 Escalation Format

Send AI Maestro message with `priority: "urgent"`, include specific questions, and BLOCK progress until clarification received.
