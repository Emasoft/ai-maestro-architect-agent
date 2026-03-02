# Workflow Checklists

## Contents

- [1. Introduction](#1-introduction)
- [2. Checklist: Requirements Analysis](#2-checklist-requirements-analysis)
- [3. Checklist: Design Phase](#3-checklist-design-phase)
- [4. Checklist: Handoff Preparation](#4-checklist-handoff-preparation)

---

## 1. Introduction

Use these checklists to ensure nothing is missed. Update task status in AI Maestro messages to ECOS.

---

## 2. Checklist: Requirements Analysis

**Phase:** Receive and analyze user requirements

- [ ] **Receive requirements from ECOS** (via AI Maestro message)
- [ ] **Read FULL_PROJECT_WORKFLOW.md** to understand project context
- [ ] **Extract user requirements** (exact quotes, no paraphrasing)
- [ ] **Document in USER_REQUIREMENTS.md** with sections:
  - [ ] Functional requirements (what system must do)
  - [ ] Non-functional requirements (performance, security, scale)
  - [ ] Constraints (budget, timeline, technology)
  - [ ] Success metrics (how to measure success)
- [ ] **Identify ambiguities** (requirements that can be interpreted multiple ways)
- [ ] **Check feasibility** of each requirement (can it be built with available resources?)
- [ ] **Request clarifications** if needed (send AI Maestro message to ECOS)
- [ ] **Wait for clarifications** (do NOT proceed if requirements unclear)
- [ ] **Log in requirements-log.md** (timestamp, requirements received, clarifications requested)
- [ ] **Verify RULE 14 compliance** (requirements are immutable, no changes without user approval)

**Output:** `docs_dev/design/USER_REQUIREMENTS.md`, `docs_dev/design/requirements-log.md`

**Next:** Proceed to Design Phase only after all requirements clear

---

## 3. Checklist: Design Phase

**Phase:** Create architecture and technical specifications

- [ ] **Create architecture.md skeleton** with sections:
  - [ ] System overview
  - [ ] Component breakdown
  - [ ] Data models
  - [ ] Integration points
  - [ ] Technology stack
  - [ ] Deployment architecture
- [ ] **Identify external APIs** (list all third-party services needed)
- [ ] **Spawn eaa-api-researcher** for each external API (if 3+ endpoints or complex auth)
- [ ] **Wait for API research results** (do NOT proceed until research complete)
- [ ] **Design system components** (clear boundaries, responsibilities)
- [ ] **Define component interactions** (APIs, events, data flows)
- [ ] **Create data models** (schemas, relationships, constraints)
- [ ] **Document integration points** (external APIs, webhooks, queues)
- [ ] **Select technology stack** (languages, frameworks, databases with versions)
- [ ] **Create Mermaid diagrams** (system architecture, data flow, deployment)
- [ ] **Make architectural decisions** (for significant choices, create ADRs)
- [ ] **Document non-functional requirements** (performance, security, scalability)
- [ ] **Spawn eaa-modularizer-expert** for module breakdown (if 5+ responsibilities)
- [ ] **Wait for modularization results** (do NOT proceed until complete)
- [ ] **Review all design artifacts** (ensure completeness, clarity, consistency)
- [ ] **Verify RULE 14 compliance** (design implements ALL user requirements, no omissions)

**Output:** `docs_dev/design/architecture.md`, `docs_dev/design/data-models.md`, `docs_dev/design/adrs/`, `docs_dev/design/api-research/`, `docs_dev/design/modules/`

**Next:** Proceed to Handoff Preparation

---

## 4. Checklist: Handoff Preparation

**Phase:** Prepare complete handoff package for EOA

- [ ] **Verify all design artifacts complete:**
  - [ ] USER_REQUIREMENTS.md exists and complete
  - [ ] architecture.md exists and complete (with diagrams)
  - [ ] data-models.md exists and complete
  - [ ] integration-points.md exists and complete
  - [ ] api-research/ directory complete (all APIs researched)
  - [ ] modules/ directory complete (all modules specified)
  - [ ] adrs/ directory complete (all decisions documented)
- [ ] **Create implementation sequence** (which modules to build first, dependency order)
- [ ] **Identify risks** (technical, resource, dependency risks)
- [ ] **Document mitigation strategies** (for each identified risk)
- [ ] **Define success criteria for EOA** (how to verify implementation is correct)
- [ ] **Resolve or escalate open questions** (do NOT handoff with unresolved questions)
- [ ] **Create handoff-{uuid}.md** with sections:
  - [ ] Executive summary (what was designed)
  - [ ] File paths (all design artifacts)
  - [ ] Implementation sequence (order of module development)
  - [ ] Risks and mitigations
  - [ ] Success criteria
  - [ ] Open questions (if any, with escalation status)
- [ ] **Self-review using Success Criteria section** (verify all criteria met)
- [ ] **Send AI Maestro message to ECOS** (design complete, ready for handoff)

**Output:** `docs_dev/design/handoff-{uuid}.md`

**Next:** Wait for ECOS to route handoff to EOA
