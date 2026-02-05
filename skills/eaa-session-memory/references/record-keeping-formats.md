# Record-Keeping and Logging Formats

This document defines all standard formats for record-keeping, logging, and documentation in the EAA Architect workflow.

## Contents

1. [Requirements Log Format](#requirements-log-format)
2. [Design Artifacts Structure](#design-artifacts-structure)
3. [ADR Template](#adr-template)
4. [Handoff Document Template](#handoff-document-template)
5. [Handoff Validation Checklist](#handoff-validation-checklist)
6. [AI Maestro Message Formats](#ai-maestro-message-formats)
7. [File Organization Rules](#file-organization-rules)

---

## Requirements Log Format

**Location:** `docs_dev/design/requirements-log.md`

**Purpose:** Chronological record of all requirements received, clarifications requested, and decisions made.

**Template:**

```markdown
# Requirements Log

## [TIMESTAMP] - [PROJECT_NAME]

### Requirements Received
- Requirement 1: "[EXACT_USER_QUOTE]"
- Requirement 2: "[EXACT_USER_QUOTE]"
- ...

### Ambiguities Identified
- Ambiguity 1: "[SPECIFIC_QUESTION]" (Context: "[USER_QUOTE]")
- Ambiguity 2: "[SPECIFIC_QUESTION]" (Context: "[USER_QUOTE]")

### Clarifications Requested
- [TIMESTAMP]: Asked ECOS about [ISSUE] (Message ID: [MESSAGE_ID])
- [TIMESTAMP]: Received clarification: "[ECOS_RESPONSE]"

### Decisions Made
- Decision 1: "[DECISION]" (Rationale: "[REASON]")
- Decision 2: "[DECISION]" (Rationale: "[REASON]")

### Status
- [TIMESTAMP]: Requirements analysis complete
```

**Usage Rules:**
- Always use exact user quotes (no paraphrasing)
- Include timestamps for all entries (YYYY-MM-DD HH:MM:SS format)
- Reference AI Maestro message IDs for traceability
- Document rationale for every decision

---

## Design Artifacts Structure

**Location:** `docs_dev/design/`

**Directory Structure:**

```
docs_dev/design/
├── requirements-log.md         # Chronological requirements log
├── USER_REQUIREMENTS.md        # Extracted user requirements
├── architecture.md             # System architecture
├── data-models.md              # Database schemas, relationships
├── integration-points.md       # External APIs, webhooks, queues
├── module-dependency-graph.md  # Mermaid graph of module dependencies
├── handoff-{uuid}.md           # Handoff document to EOA
├── adrs/                       # Architecture Decision Records
│   ├── 001-database-choice.md
│   ├── 002-api-framework.md
│   └── ...
├── api-research/               # External API research
│   ├── stripe-api.md
│   ├── sendgrid-api.md
│   └── ...
├── modules/                    # Module specifications
│   ├── module-1-user-service.md
│   ├── module-2-payment-service.md
│   └── ...
├── clarifications/             # Clarification requests and responses
│   ├── 20260204-payment-flow.md
│   └── ...
└── blockers/                   # Blocker reports
    ├── 20260204-latency-requirement.md
    └── ...
```

**Naming Conventions:**
- **Logs/clarifications/blockers:** `YYYYMMDD-description.md` or `YYYYMMDD-HHMMSS-description.md`
- **Handoffs:** `handoff-{uuid}.md` (use `uuidgen` command)
- **ADRs:** `NNN-title.md` (sequential numbers: 001, 002, etc.)
- **Modules:** `module-N-name.md` (N = implementation order)
- **API research:** `{api-name}-api.md`

---

## ADR Template

**Location:** `docs_dev/design/adrs/NNN-title.md`

**Purpose:** Document significant architectural decisions with context, alternatives, and rationale.

**Template:**

```markdown
# ADR [NUMBER]: [TITLE]

**Date:** [YYYY-MM-DD]
**Status:** Proposed | Accepted | Deprecated | Superseded by [ADR-XXX]
**Deciders:** [Names/roles]
**Context:** [Project/module]

## Context
[What is the issue we're trying to solve? Include relevant background, constraints, requirements.]

## Decision
[What is the decision we've made? Be specific and concrete.]

## Alternatives Considered

### Alternative 1: [NAME]
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

### Alternative 2: [NAME]
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

## Rationale
[Why did we choose this decision over the alternatives? What trade-offs did we accept?]

## Consequences

### Positive
- Positive consequence 1
- Positive consequence 2

### Negative
- Negative consequence 1 (mitigation: [STRATEGY])
- Negative consequence 2 (mitigation: [STRATEGY])

### Neutral
- Neutral consequence 1
- Neutral consequence 2

## Related Decisions
- Related to [ADR-XXX]
- Supersedes [ADR-XXX]
- Superseded by [ADR-XXX]

## Notes
[Any additional context, references, or follow-up items.]
```

**When to Create ADR:**
- Decision affects multiple modules or teams
- Trade-offs involve significant cost/performance/complexity
- Alternative approaches were seriously considered
- Decision may be questioned or revisited later
- Regulatory/compliance concerns are involved
- Third-party dependencies are chosen

---

## Handoff Document Template

**Location:** `docs_dev/design/handoff-{uuid}.md`

**Purpose:** Complete package of design artifacts for EOA to begin implementation.

**Template:**

```markdown
# Design Handoff: [PROJECT_NAME]

**Date:** [YYYY-MM-DD HH:MM:SS]
**Project:** [PROJECT_NAME]
**Architect:** eaa-architect-main-agent
**Handoff ID:** [UUID]

## Executive Summary
[1-2 paragraphs: What was designed, key technologies, major components.]

## Design Artifacts
- Requirements: `docs_dev/design/USER_REQUIREMENTS.md`
- Architecture: `docs_dev/design/architecture.md`
- Data Models: `docs_dev/design/data-models.md`
- Integration Points: `docs_dev/design/integration-points.md`
- Module Specs: `docs_dev/design/modules/` (5 modules)
- ADRs: `docs_dev/design/adrs/` (3 decisions)
- API Research: `docs_dev/design/api-research/` (2 APIs)

## Implementation Sequence

### Phase 1: Foundation (Week 1)
**Modules:**
- Module 1: Database schema (docs_dev/design/modules/module-1-database.md)
- Module 2: Core models (docs_dev/design/modules/module-2-models.md)

**Dependencies:** None (start here)

**Success Criteria:**
- Database migrations run without errors
- Core models have 100% test coverage
- Models match data-models.md specification

### Phase 2: Core Features (Week 2)
**Modules:**
- Module 3: API service (docs_dev/design/modules/module-3-api.md)
- Module 4: Business logic (docs_dev/design/modules/module-4-logic.md)

**Dependencies:** Phase 1 complete

**Success Criteria:**
- All API endpoints respond with correct status codes
- Business logic passes all test scenarios
- Integration tests pass

### Phase 3: Integration (Week 3)
**Modules:**
- Module 5: External API integration (docs_dev/design/modules/module-5-integration.md)

**Dependencies:** Phase 2 complete

**Success Criteria:**
- External API calls succeed with proper error handling
- Webhook handlers process events correctly
- Rate limiting and retries working

## Risks and Mitigations

### High Priority
1. **Risk:** External API rate limits exceeded during peak traffic
   **Mitigation:** Implement request queue with backoff, cache responses for 5 minutes
   **Owner:** Backend team

### Medium Priority
2. **Risk:** Database query performance degrades with >100K records
   **Mitigation:** Add indexes on frequently queried columns (see data-models.md)
   **Owner:** Database team

### Low Priority
3. **Risk:** Frontend build size exceeds 1MB
   **Mitigation:** Use code splitting, lazy loading for non-critical components
   **Owner:** Frontend team

## Success Criteria for EOA
Implementation is complete when:
- [ ] All modules implemented per specifications in docs_dev/design/modules/
- [ ] All API endpoints match integration-points.md specification
- [ ] Database schema matches data-models.md
- [ ] All tests pass (unit, integration, e2e)
- [ ] Non-functional requirements met (performance, security, scalability from USER_REQUIREMENTS.md)
- [ ] External API integrations working (see api-research/)
- [ ] Deployment successful (see architecture.md deployment section)

## Open Questions
[List any unresolved questions. If ANY exist, escalation status must be included.]

1. **Question:** [QUESTION_TEXT]
   **Status:** Escalated to ECOS on [DATE] (Message ID: [ID])
   **Blocking:** [Yes/No]

2. **Question:** [QUESTION_TEXT]
   **Status:** Escalated to ECOS on [DATE] (Message ID: [ID])
   **Blocking:** [Yes/No]

[If no open questions: "None. All design decisions finalized."]

## Notes
[Any additional context for EOA.]
```

---

## Handoff Validation Checklist

**CRITICAL:** Before sending handoff to EOA/ECOS, verify ALL items:

- [ ] **All referenced files exist** - Every file path in handoff document is valid
- [ ] **All design artifacts complete** - No empty or placeholder documents
- [ ] **No placeholder [TBD] markers** - Search for "[TBD]", "[TODO]", "[PLACEHOLDER]"
- [ ] **Module specs have acceptance criteria** - Each module has testable success criteria
- [ ] **Risk register complete** - All identified risks have mitigations documented
- [ ] **UUID is unique** - Run `grep -r "handoff-{uuid}" docs_dev/` to verify no duplicates

**Validation Script:**

```bash
# Validate handoff before sending
HANDOFF_FILE="docs_dev/design/handoff-${UUID}.md"

# Check all file references exist
grep -oP 'docs_dev/[a-zA-Z0-9/_.-]+\.md' "$HANDOFF_FILE" | while read -r ref; do
  if [ ! -f "$ref" ]; then
    echo "ERROR: Missing file: $ref"
    exit 1
  fi
done

# Check for placeholder markers
if grep -qE '\[TBD\]|\[TODO\]|\[PLACEHOLDER\]' "$HANDOFF_FILE"; then
  echo "ERROR: Handoff contains placeholder markers"
  exit 1
fi

echo "Handoff validation passed"
```

**Do NOT send handoff if any validation fails. Fix issues first.**

---

## AI Maestro Message Formats

### 1. Acknowledgment of Design Request

**When:** ECOS assigns you a design task

**Format:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-architect-main-agent",
    "to": "ecos",
    "subject": "Design Request Acknowledged",
    "priority": "normal",
    "content": {
      "type": "acknowledgment",
      "message": "Design request received for [PROJECT_NAME]. Starting requirements analysis. ETA: [ESTIMATED_COMPLETION_TIME]."
    }
  }'
```

**Example:**
```json
{
  "from": "eaa-architect-main-agent",
  "to": "ecos",
  "subject": "Design Request Acknowledged",
  "priority": "normal",
  "content": {
    "type": "acknowledgment",
    "message": "Design request received for E-Commerce Product Catalog. Starting requirements analysis. ETA: 2 hours."
  }
}
```

### 2. Clarification Request

**When:** User requirements are ambiguous or conflicting

**Format:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-architect-main-agent",
    "to": "ecos",
    "subject": "Clarification Needed - [PROJECT_NAME]",
    "priority": "high",
    "content": {
      "type": "clarification_request",
      "message": "BLOCKING: Requirement ambiguity detected. Question: [SPECIFIC_QUESTION]. Context: [USER_REQUIREMENT_QUOTE]. Cannot proceed until clarified. Details: docs_dev/design/clarifications/[TIMESTAMP]-[ISSUE].md"
    }
  }'
```

**Example:**
```json
{
  "from": "eaa-architect-main-agent",
  "to": "ecos",
  "subject": "Clarification Needed - Payment Gateway Integration",
  "priority": "high",
  "content": {
    "type": "clarification_request",
    "message": "BLOCKING: Requirement ambiguity detected. Question: Should payment processing be synchronous or asynchronous? Context: User said 'fast payment processing' but also 'reliable with retries'. Synchronous = fast but no retries. Asynchronous = reliable retries but slower user feedback. Cannot proceed until clarified. Details: docs_dev/design/clarifications/20260204-payment-flow.md"
  }
}
```

### 3. Design Completion Report

**When:** All design artifacts ready, handoff prepared

**Format:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-architect-main-agent",
    "to": "ecos",
    "subject": "Design Complete - [PROJECT_NAME]",
    "priority": "normal",
    "content": {
      "type": "design_complete",
      "message": "[DONE] Design for [PROJECT_NAME] complete. Architecture: [BRIEF_SUMMARY]. Modules: [MODULE_COUNT]. Risks: [HIGH_COUNT]/[MEDIUM_COUNT]/[LOW_COUNT]. Handoff doc: docs_dev/design/handoff-[UUID].md. Ready for EOA assignment."
    }
  }'
```

**Example:**
```json
{
  "from": "eaa-architect-main-agent",
  "to": "ecos",
  "subject": "Design Complete - E-Commerce Product Catalog",
  "priority": "normal",
  "content": {
    "type": "design_complete",
    "message": "[DONE] Design for E-Commerce Product Catalog complete. Architecture: REST API + PostgreSQL + Redis cache + React frontend. Modules: 5 (product-service, inventory-service, search-service, cart-service, frontend). Risks: 1/3/2. Handoff doc: docs_dev/design/handoff-a7f8b2d4.md. Ready for EOA assignment."
  }
}
```

### 4. Handoff Ready

**When:** Design artifacts ready for implementation

**Format:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-architect-main-agent",
    "to": "ecos",
    "subject": "Handoff Ready - [PROJECT_NAME]",
    "priority": "normal",
    "content": {
      "type": "handoff",
      "message": "Design handoff ready for [PROJECT_NAME]. Implementation sequence: [PHASE_1] → [PHASE_2] → [PHASE_3]. Critical path: [TOP_3_ITEMS]. All artifacts in docs_dev/design/. Handoff doc: handoff-[UUID].md. Awaiting EOA assignment from ECOS."
    }
  }'
```

**Example:**
```json
{
  "from": "eaa-architect-main-agent",
  "to": "ecos",
  "subject": "Handoff Ready - Payment Gateway Integration",
  "priority": "normal",
  "content": {
    "type": "handoff",
    "message": "Design handoff ready for Payment Gateway Integration. Implementation sequence: Phase 1 (Database schema + Payment model) → Phase 2 (Stripe API integration) → Phase 3 (Webhook handlers + retry logic) → Phase 4 (Frontend payment form). Critical path: Stripe API credentials, webhook endpoint setup, PCI compliance review. All artifacts in docs_dev/design/. Handoff doc: handoff-c3e9f1a8.md. Awaiting EOA assignment from ECOS."
  }
}
```

### 5. Blocker Report

**When:** Cannot proceed due to missing information, infeasible requirement, or external dependency

**Format:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-architect-main-agent",
    "to": "ecos",
    "subject": "BLOCKED - [PROJECT_NAME]",
    "priority": "urgent",
    "content": {
      "type": "blocker",
      "message": "[BLOCKED] Design for [PROJECT_NAME]. Blocker: [SPECIFIC_ISSUE]. Impact: [IMPACT_DESCRIPTION]. Next: [WHAT_IS_NEEDED]. Details: docs_dev/design/blockers/[TIMESTAMP]-[ISSUE].md. Awaiting user decision."
    }
  }'
```

**Example:**
```json
{
  "from": "eaa-architect-main-agent",
  "to": "ecos",
  "subject": "BLOCKED - Real-Time Analytics Dashboard",
  "priority": "urgent",
  "content": {
    "type": "blocker",
    "message": "[BLOCKED] Design for Real-Time Analytics Dashboard. Blocker: User requires <100ms query latency for 1M+ records, but available database (PostgreSQL) cannot meet this requirement without significant infrastructure changes (distributed architecture, caching layer, query optimization). Impact: Cannot design system without clarifying performance vs. cost trade-off. Next: User must choose: (A) Relax latency requirement to <1s, (B) Increase budget for distributed architecture (Elasticsearch + Redis), or (C) Reduce dataset size via data retention policy. Details: docs_dev/design/blockers/20260204-latency-requirement.md. Awaiting user decision."
  }
}
```

### 6. ACK Protocol

**After sending any message:**

1. **Wait 30 seconds** for ACK response
2. **If no ACK received**, retry ONCE with same message
3. **If still no ACK**, escalate to orchestrator
4. **Do NOT proceed** with dependent operations until ACK received

**ACK Verification:**
```bash
curl -s "http://localhost:23000/api/messages?agent=eaa-architect-main-agent&action=list&status=unread" | jq '.messages[] | select(.subject | contains("ACK"))'
```

**Retry Format:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-architect-main-agent",
    "to": "[ORIGINAL_TARGET]",
    "subject": "[RETRY] [ORIGINAL_SUBJECT]",
    "priority": "high",
    "content": {
      "type": "retry",
      "message": "[ORIGINAL_MESSAGE] (Retry: No ACK received within 30s)"
    }
  }'
```

**Escalation Format:**
```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "eaa-architect-main-agent",
    "to": "ecos",
    "subject": "ACK Timeout Escalation",
    "priority": "urgent",
    "content": {
      "type": "escalation",
      "message": "ACK timeout from [TARGET]. Original message: [SUBJECT]. Sent: [TIMESTAMP]. Retry sent: [RETRY_TIMESTAMP]. Blocking operation: [BLOCKED_OPERATION]."
    }
  }'
```

---

## File Organization Rules

1. **Use timestamps in filenames** for logs and reports: `YYYYMMDD-HHMMSS-description.md`
2. **Use UUIDs for handoff documents** to avoid conflicts: `handoff-{uuidgen}.md`
3. **Keep design artifacts in docs_dev/design/** (never in project root or src/)
4. **Use subdirectories** for categories (adrs/, api-research/, modules/, clarifications/, blockers/)
5. **Never delete design artifacts** - they are historical record (rename to `*-archived.md` if obsolete)
6. **Reference file paths in messages** - never paste full content in AI Maestro messages

### Directory Creation Order

When starting a new project design:

```bash
# Create base design directory
mkdir -p docs_dev/design/{adrs,api-research,modules,clarifications,blockers}

# Initialize requirements log
touch docs_dev/design/requirements-log.md

# Create handoff directory (optional, handoffs can go in design root)
mkdir -p docs_dev/design/handoffs
```

### Archiving Obsolete Documents

When a design artifact becomes obsolete (not deleted, just superseded):

```bash
# Rename with -archived suffix
mv docs_dev/design/architecture.md docs_dev/design/architecture-archived-20260204.md

# Update references in handoff documents to point to new version
# Add note in new document explaining what changed
```

---

## Session State Tracking

### Current Work State Format

Track current work state in a session memory file (not part of permanent artifacts):

**Location:** `docs_dev/design/.eaa-session-state.json` (gitignored)

**Format:**
```json
{
  "project_name": "E-Commerce Product Catalog",
  "phase": "design|handoff_prep|blocked|waiting_clarification",
  "current_task": "API research for payment gateway",
  "blockers": [
    {
      "issue": "Payment flow unclear",
      "blocking_since": "2026-02-04T10:30:00Z",
      "escalated_to": "ecos",
      "message_id": "msg-12345"
    }
  ],
  "pending_clarifications": [
    {
      "question": "Sync vs async payment?",
      "asked_at": "2026-02-04T09:00:00Z",
      "target": "ecos"
    }
  ],
  "completed_artifacts": [
    "USER_REQUIREMENTS.md",
    "architecture.md",
    "data-models.md"
  ],
  "pending_artifacts": [
    "integration-points.md",
    "module-1-database.md"
  ],
  "sub_agents": [
    {
      "agent": "eaa-api-researcher",
      "task": "Research Stripe API",
      "status": "running",
      "started_at": "2026-02-04T11:00:00Z"
    }
  ]
}
```

**Usage:**
- Update after every major state change
- Read at session start to resume work
- Clear blockers list when resolved
- Track sub-agent spawns to avoid duplicate work

---

## Completion Verification Log

Before marking any phase complete, log verification:

**Location:** `docs_dev/design/phase-completion-log.md`

**Format:**
```markdown
# Phase Completion Log

## [YYYY-MM-DD HH:MM:SS] - Requirements Analysis Phase

**Phase:** Requirements Analysis
**Project:** [PROJECT_NAME]
**Status:** COMPLETE

### Checklist Verification
- [x] All user requirements extracted (verbatim quotes in USER_REQUIREMENTS.md)
- [x] Ambiguities identified and logged (2 ambiguities in requirements-log.md)
- [x] Clarification requests sent to ECOS (Message IDs: msg-123, msg-456)
- [x] Functional requirements separated from non-functional
- [x] Constraints documented (budget: $50K, timeline: 6 weeks, tech: Python/React)
- [x] Dependencies identified (Stripe API, PostgreSQL, AWS S3)
- [x] Success metrics defined (< 200ms API response, 99.9% uptime)

### Evidence Files
- docs_dev/design/USER_REQUIREMENTS.md (created, 1200 lines)
- docs_dev/design/requirements-log.md (updated, 3 entries)
- docs_dev/design/clarifications/20260204-payment-flow.md (created)

### Self-Check Result
✓ PASS: "Can EOA implement this without asking me what the user wanted?" - YES

### Next Phase
Design Phase (architecture.md, data models, API research)

---

## [YYYY-MM-DD HH:MM:SS] - Design Phase

**Phase:** Design Phase
**Project:** [PROJECT_NAME]
**Status:** COMPLETE

### Checklist Verification
- [x] System components identified with clear boundaries (5 components)
- [x] Component interactions defined (REST APIs, event bus)
- [x] Technology stack specified (Python 3.11, FastAPI, React 18, PostgreSQL 15)
- [x] Data models designed (12 tables, relationships documented)
- [x] Integration points documented (Stripe, SendGrid, AWS S3)
- [x] Non-functional requirements addressed (performance, security, scalability)
- [x] Architectural decisions recorded in ADRs (3 ADRs created)
- [x] Deployment architecture specified (Docker, AWS ECS, RDS)

### Evidence Files
- docs_dev/design/architecture.md (created, 2500 lines with 8 Mermaid diagrams)
- docs_dev/design/data-models.md (created, 800 lines)
- docs_dev/design/integration-points.md (created, 600 lines)
- docs_dev/design/adrs/001-database-choice.md (created)
- docs_dev/design/adrs/002-api-framework.md (created)
- docs_dev/design/adrs/003-payment-processor.md (created)
- docs_dev/design/api-research/stripe-api.md (created)
- docs_dev/design/api-research/sendgrid-api.md (created)

### Self-Check Result
✓ PASS: "Can a new developer understand the system from these documents alone?" - YES

### Next Phase
Handoff Preparation (module specs, handoff document)
```
