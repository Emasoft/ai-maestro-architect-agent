# Handoff Document Format


## Contents

- [Overview](#overview)
- [Handoff Validation Checklist](#handoff-validation-checklist)
  - [Validation Script](#validation-script)
- [Handoff Document Template](#handoff-document-template)
- [Executive Summary](#executive-summary)
- [Design Artifacts](#design-artifacts)
- [Implementation Sequence](#implementation-sequence)
  - [Phase 1: Foundation (Week 1)](#phase-1-foundation-week-1)
  - [Phase 2: Core Features (Week 2)](#phase-2-core-features-week-2)
  - [Phase 3: Integration (Week 3)](#phase-3-integration-week-3)
- [Risks and Mitigations](#risks-and-mitigations)
  - [High Priority](#high-priority)
  - [Medium Priority](#medium-priority)
  - [Low Priority](#low-priority)
- [Success Criteria for EOA](#success-criteria-for-eoa)
- [Open Questions](#open-questions)
- [Notes](#notes)
- [Template Field Guide](#template-field-guide)
  - [Executive Summary](#executive-summary)
  - [Design Artifacts](#design-artifacts)
  - [Implementation Sequence](#implementation-sequence)
  - [Risks and Mitigations](#risks-and-mitigations)
  - [Success Criteria for EOA](#success-criteria-for-eoa)
  - [Open Questions](#open-questions)
  - [Notes](#notes)

## Overview

**Location:** `docs_dev/design/handoffs/`

**Purpose:** Complete package of design artifacts for EOA to begin implementation.

**Naming Convention:** `handoff-{uuid}.md` (generate UUID with `uuidgen` command)

## Handoff Validation Checklist

**CRITICAL:** Before sending handoff to EOA/ECOS, verify ALL items:

- [ ] **All referenced files exist** - Every file path in handoff document is valid
- [ ] **All design artifacts complete** - No empty or placeholder documents
- [ ] **No placeholder [TBD] markers** - Search for "[TBD]", "[TODO]", "[PLACEHOLDER]"
- [ ] **Module specs have acceptance criteria** - Each module has testable success criteria
- [ ] **Risk register complete** - All identified risks have mitigations documented
- [ ] **UUID is unique** - Run `grep -r "handoff-{uuid}" docs_dev/` to verify no duplicates

### Validation Script

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

## Handoff Document Template

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

## Template Field Guide

### Executive Summary
- **What to include**: High-level description of what system does, key technologies chosen, major architectural components
- **Length**: 1-2 paragraphs maximum
- **Example**: "Designed a real-time notification system using WebSockets and Redis pub/sub. Major components include Node.js API server, Redis message broker, and React frontend. System handles 10K concurrent connections with sub-100ms latency."

### Design Artifacts
- **Purpose**: Complete list of all design documents produced
- **Format**: Bullet list with relative paths from project root
- **Include counts**: Show number of modules, ADRs, API research documents
- **Verify existence**: Every path must point to an existing file

### Implementation Sequence
- **Structure**: Organize into phases with clear dependencies
- **Phase naming**: Use descriptive names (Foundation, Core Features, Integration) with time estimates
- **Module references**: Link to specific module specification files
- **Success criteria**: Each phase must have measurable, testable outcomes
- **Dependencies**: Explicitly state which phases must complete before starting next

### Risks and Mitigations
- **Priority levels**: High/Medium/Low based on impact and likelihood
- **Format**: Risk description, mitigation strategy, owner team
- **Complete register**: All identified risks during design must be listed
- **Actionable mitigations**: Each mitigation must be specific and implementable

### Success Criteria for EOA
- **Format**: Checklist with measurable outcomes
- **Coverage**: Must cover all design artifacts and requirements
- **Testability**: Each criterion must be verifiable (tests pass, metrics met, etc.)
- **Completeness**: Reference all key design documents

### Open Questions
- **When to use**: Only if questions remain unresolved after design completion
- **Required fields**: Question text, escalation status, blocking status
- **Message tracking**: Include AI Maestro message ID for escalated questions
- **None case**: Explicitly state "None. All design decisions finalized." if no questions

### Notes
- **Purpose**: Additional context that doesn't fit other sections
- **Examples**: Special considerations, assumptions, deferred decisions, deployment notes
- **Optional**: Can be omitted if no additional context needed
