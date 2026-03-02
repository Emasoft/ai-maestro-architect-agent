# Document Types

This document describes the six document type categories used in the design/ directory hierarchy and when to use each type.

## Contents

- 2.1 Type Selection Guide
- 2.2 PDR Documents (pdr/)
- 2.3 Spec Documents (spec/)
- 2.4 Feature Documents (feature/)
- 2.5 Decision Documents (decision/)
- 2.6 Architecture Documents (architecture/)
- 2.7 Template Documents (template/)
- 2.8 Directory Structure

---

## 2.1 Type Selection Guide

Use this decision table to choose the correct document type:

| Your Goal | Document Type | Directory |
|-----------|---------------|-----------|
| Design a new product or major feature before implementation | **pdr** | design/pdr/ |
| Define detailed technical requirements and interfaces | **spec** | design/spec/ |
| Document a specific feature with user stories | **feature** | design/feature/ |
| Record a significant technical or architectural decision | **decision** | design/decision/ |
| Document high-level system architecture | **architecture** | design/architecture/ |
| Create a reusable document template | **template** | design/template/ |

**Quick selection questions:**

1. **Is this about WHY we chose something?** - Use `decision`
2. **Is this about HOW the system works at a high level?** - Use `architecture`
3. **Is this about WHAT we will build?** - Use `feature`
4. **Is this about detailed technical REQUIREMENTS?** - Use `spec`
5. **Is this a comprehensive DESIGN for review?** - Use `pdr`
6. **Is this a TEMPLATE for other documents?** - Use `template`

---

## 2.2 PDR Documents (pdr/)

**Full name:** Product Design Review

**Purpose:** Comprehensive design documents that go through formal review before implementation begins.

**When to use:**
- New products or major features
- Significant system changes
- Cross-team initiatives
- Features requiring stakeholder sign-off

**Required frontmatter:**
```yaml
---
uuid: GUUID-YYYYMMDD-NNNN
title: "PDR Title"
type: pdr
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Template sections:**
- Overview
- Problem Statement
- Proposed Solution
- Alternatives Considered
- Implementation Plan
- Success Metrics
- Open Questions

**Example titles:**
- "User Authentication System PDR"
- "Database Migration PDR"
- "Mobile App Redesign PDR"

---

## 2.3 Spec Documents (spec/)

**Full name:** Technical Specification

**Purpose:** Detailed technical requirements defining interfaces, behaviors, and constraints.

**When to use:**
- API definitions
- Protocol specifications
- Data format definitions
- Integration requirements
- System interfaces

**Required frontmatter:**
```yaml
---
uuid: GUUID-YYYYMMDD-NNNN
title: "Specification Title"
type: spec
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Template sections:**
- Purpose
- Scope
- Functional Requirements
- Non-Functional Requirements
- Interfaces (Input/Output)
- Constraints

**Example titles:**
- "REST API v2 Specification"
- "Event Message Format Specification"
- "Database Schema Specification"

---

## 2.4 Feature Documents (feature/)

**Full name:** Feature Document

**Purpose:** User-facing feature descriptions with user stories, design, and rollout plans.

**When to use:**
- New user-facing features
- Feature enhancements
- User experience changes
- Features with user stories

**Required frontmatter:**
```yaml
---
uuid: GUUID-YYYYMMDD-NNNN
title: "Feature Title"
type: feature
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Template sections:**
- Summary
- Motivation
- User Stories
- Design (Architecture, API Changes, Data Model)
- Testing Plan
- Rollout Plan

**Example titles:**
- "OAuth 2.0 Login Feature"
- "Dark Mode Feature"
- "Export to PDF Feature"

---

## 2.5 Decision Documents (decision/)

**Full name:** Architecture Decision Record (ADR)

**Purpose:** Record significant technical or architectural decisions with context and consequences.

**When to use:**
- Technology selection
- Architecture patterns
- Process changes
- Significant trade-offs
- Decisions that future developers should understand

**Required frontmatter:**
```yaml
---
uuid: GUUID-YYYYMMDD-NNNN
title: "Decision Title"
type: decision
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Template sections:**
- Status (Proposed/Accepted/Deprecated/Superseded)
- Context
- Decision
- Consequences (Positive/Negative)

**Example titles:**
- "Use PostgreSQL for Primary Database"
- "Adopt Microservices Architecture"
- "Switch to TypeScript"

---

## 2.6 Architecture Documents (architecture/)

**Full name:** Architecture Document

**Purpose:** High-level system architecture documentation showing components, data flows, and integrations.

**When to use:**
- System overview documentation
- Component architecture
- Integration architecture
- Security architecture
- Deployment architecture

**Required frontmatter:**
```yaml
---
uuid: GUUID-YYYYMMDD-NNNN
title: "Architecture Title"
type: architecture
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Template sections:**
- Overview
- Components
- Data Flow
- Dependencies
- Security Considerations
- Scalability
- Monitoring

**Example titles:**
- "Payment Processing Architecture"
- "Event-Driven Architecture"
- "Multi-Tenant Architecture"

---

## 2.7 Template Documents (template/)

**Full name:** Document Template

**Purpose:** Reusable templates for creating new documents of various types.

**When to use:**
- Creating standardized document formats
- Custom document types not covered by other categories
- Team-specific document templates

**Required frontmatter:**
```yaml
---
uuid: GUUID-YYYYMMDD-NNNN
title: "Template Title"
type: template
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Template sections:**
- Purpose
- Usage
- Sections (variable based on template purpose)

**Example titles:**
- "Sprint Retrospective Template"
- "Incident Report Template"
- "Meeting Notes Template"

---

## 2.8 Directory Structure

The design/ directory is organized by document type:

```
design/
  pdr/
    auth-system-design.md
    database-migration.md
  spec/
    rest-api-v2.md
    event-format.md
  feature/
    oauth-login.md
    dark-mode.md
  decision/
    use-postgresql.md
    adopt-typescript.md
  architecture/
    payment-processing.md
    event-driven.md
  template/
    retrospective.md
    incident-report.md
```

**Rules:**
1. Documents MUST be placed in the directory matching their `type` field
2. Filenames should be kebab-case (lowercase with hyphens)
3. All documents MUST have the `.md` extension
4. The `type` field in frontmatter should match the parent directory name

---

## See Also

- [Creating Documents](creating-documents.md) - How to create documents of each type
- [UUID Specification](uuid-specification.md) - UUID format used in all document types
