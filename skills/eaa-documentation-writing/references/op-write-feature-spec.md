---
procedure: support-skill
workflow-instruction: support
---

# Operation: Write Feature Specification

## Purpose

Write a feature specification document that defines user stories, functional requirements, acceptance criteria, and implementation guidance for a new feature.

## When to Use

- Specifying a new feature before development
- Documenting feature requirements for implementation team
- Creating acceptance criteria for testing

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Feature name | Assignment | Yes |
| User stories | Requirements | Yes |
| Acceptance criteria | Stakeholders | Yes |

## Procedure

### Step 1: Gather Feature Information

Collect:
- Feature name and description
- User stories (who, what, why)
- Functional requirements
- Non-functional requirements
- Acceptance criteria
- Dependencies and constraints

### Step 2: Create Feature Specification Document

Use this template:

```markdown
# Feature Specification: <Feature Name>

**Version:** 1.0
**Status:** Draft | Review | Approved | In Development | Complete
**Owner:** <Name/Role>
**Last Updated:** YYYY-MM-DD

---

## Overview

### Problem Statement

<What problem does this feature solve? Why is it needed?>

### Proposed Solution

<High-level description of the solution>

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| <metric-1> | <target> | <how to measure> |

---

## User Stories

### US-001: <Story Title>

**As a** <user type>
**I want** <goal>
**So that** <benefit>

**Priority:** High | Medium | Low
**Estimation:** <story points or t-shirt size>

**Acceptance Criteria:**
- [ ] Given <context>, when <action>, then <outcome>
- [ ] Given <context>, when <action>, then <outcome>

---

### US-002: <Story Title>

**As a** <user type>
**I want** <goal>
**So that** <benefit>

**Priority:** <priority>

**Acceptance Criteria:**
- [ ] <criterion>
- [ ] <criterion>

---

## Functional Requirements

### FR-001: <Requirement Title>

**Description:** <Detailed description>

**Inputs:**
- <input 1>
- <input 2>

**Processing:**
- <step 1>
- <step 2>

**Outputs:**
- <output 1>

**Business Rules:**
- <rule 1>
- <rule 2>

---

### FR-002: <Requirement Title>

<Same structure as above>

---

## Non-Functional Requirements

### Performance

| Requirement | Target |
|-------------|--------|
| Response time | < 200ms for 95th percentile |
| Throughput | 1000 requests/second |

### Security

- <Security requirement 1>
- <Security requirement 2>

### Accessibility

- <Accessibility requirement>

### Scalability

- <Scalability requirement>

---

## User Interface

### Mockups

<Include wireframes or links to design files>

### User Flow

1. User navigates to <page>
2. User performs <action>
3. System displays <result>

---

## Technical Considerations

### Architecture Impact

<How does this feature affect system architecture?>

### Database Changes

| Table | Change | Description |
|-------|--------|-------------|
| `table_name` | Add column | New field for feature |

### API Changes

| Endpoint | Method | Change |
|----------|--------|--------|
| `/api/resource` | POST | New endpoint |

### Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| `package` | `^1.0.0` | Required for X |

---

## Testing Strategy

### Unit Tests

- <Unit test scenario 1>
- <Unit test scenario 2>

### Integration Tests

- <Integration test scenario>

### End-to-End Tests

- <E2E test scenario>

---

## Rollout Plan

### Phase 1: Internal Testing

- Duration: <time>
- Audience: <internal team>

### Phase 2: Beta Release

- Duration: <time>
- Audience: <beta users>

### Phase 3: General Availability

- Launch date: <date>
- Announcement: <channel>

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| <risk> | High/Med/Low | High/Med/Low | <mitigation> |

---

## Open Questions

- [ ] <Question 1>
- [ ] <Question 2>

---

## References

- [Related Feature Spec](link)
- [Design Document](link)
- [ADR](link)
```

### Step 3: Apply Quality Check (6 C's)

- [ ] **Complete**: All user stories and requirements included
- [ ] **Correct**: Requirements match stakeholder needs
- [ ] **Clear**: Acceptance criteria unambiguous
- [ ] **Consistent**: Terminology matches project
- [ ] **Current**: Reflects latest decisions
- [ ] **Connected**: Links to related docs

### Step 4: Save Document

Save to: `/docs_dev/requirements/<feature-name>.md`

## Output

| File | Location |
|------|----------|
| Feature specification | `/docs_dev/requirements/<feature-name>.md` |

## Verification Checklist

- [ ] Problem statement defined
- [ ] User stories with acceptance criteria
- [ ] Functional requirements listed
- [ ] Non-functional requirements included
- [ ] Technical considerations documented
- [ ] Testing strategy outlined
- [ ] Risks identified
- [ ] 6 C's quality check passed

## Error Handling

| Error | Solution |
|-------|----------|
| Unclear requirements | Schedule stakeholder clarification |
| Missing acceptance criteria | Cannot proceed - criteria required |
| Conflicting requirements | Escalate to product owner |
