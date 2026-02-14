---
operation: identify-risks
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-planning-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Identify Risks


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Discover All Risks](#step-1-discover-all-risks)
  - [Step 2: Assess Impact and Probability](#step-2-assess-impact-and-probability)
  - [Step 3: Prioritize Risks](#step-3-prioritize-risks)
  - [Step 4: Plan Mitigation Strategies](#step-4-plan-mitigation-strategies)
  - [Step 5: Create Risk Register](#step-5-create-risk-register)
- [Risk Register](#risk-register)
  - [Step 6: Define Monitoring Plan](#step-6-define-monitoring-plan)
- [Risk Monitoring](#risk-monitoring)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Authentication System Risks](#example-authentication-system-risks)
- [Identified Risks](#identified-risks)
  - [Technical Risks](#technical-risks)
  - [Resource Risks](#resource-risks)
- [Risk Matrix](#risk-matrix)
- [Top Risks Summary](#top-risks-summary)
  - [Example: Risk Register Template](#example-risk-register-template)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Architecture design is complete and needs risk assessment
- Starting a project with unknown technical challenges
- Evaluating third-party dependencies or integrations
- Planning for failure modes and recovery strategies
- Creating mitigation plans for potential obstacles

## Prerequisites

- Completed architecture design document
- Understanding of technical constraints
- Knowledge of organizational limitations (time, budget, skills)
- Access to stakeholders for impact assessment

## Procedure

### Step 1: Discover All Risks

Systematically identify risks across multiple categories.

**Risk Categories:**

| Category | Examples |
|----------|----------|
| Technical | Unproven technology, scalability limits, integration complexity |
| Schedule | Dependencies on external teams, underestimated effort |
| Resource | Key person dependency, skill gaps, budget constraints |
| External | Vendor stability, API changes, regulatory requirements |
| Scope | Unclear requirements, scope creep, changing priorities |

**Discovery techniques:**
- Review architecture document for complexity points
- Interview stakeholders about concerns
- Review similar past projects for issues encountered
- Analyze third-party dependencies

### Step 2: Assess Impact and Probability

Rate each risk on two dimensions:

**Impact Scale:**
| Rating | Impact | Description |
|--------|--------|-------------|
| 4 | CRITICAL | Project failure, major financial loss |
| 3 | HIGH | Significant delay, budget overrun |
| 2 | MEDIUM | Moderate delay, workaround needed |
| 1 | LOW | Minor inconvenience, easily resolved |

**Probability Scale:**
| Rating | Probability | Description |
|--------|-------------|-------------|
| 4 | CERTAIN | Will happen (>90%) |
| 3 | LIKELY | Probably will happen (60-90%) |
| 2 | POSSIBLE | Might happen (30-60%) |
| 1 | UNLIKELY | Probably won't happen (<30%) |

**Risk Score:**
```
Risk Score = Impact x Probability
```

### Step 3: Prioritize Risks

Sort risks by risk score:

| Priority | Score Range | Action |
|----------|-------------|--------|
| CRITICAL | 12-16 | Immediate mitigation required |
| HIGH | 6-11 | Active mitigation plan |
| MEDIUM | 3-5 | Monitor and prepare |
| LOW | 1-2 | Accept and document |

### Step 4: Plan Mitigation Strategies

For each high-priority risk, define mitigation strategies:

**Mitigation Types:**
| Type | Description |
|------|-------------|
| Avoid | Change plan to eliminate risk |
| Reduce | Take actions to lower probability or impact |
| Transfer | Move risk to third party (insurance, contracts) |
| Accept | Acknowledge risk and prepare contingency |

### Step 5: Create Risk Register

Document all risks in a structured register:

```markdown
## Risk Register

| ID | Risk | Category | Impact | Probability | Score | Priority | Mitigation | Owner |
|----|------|----------|--------|-------------|-------|----------|------------|-------|
| R1 | OAuth provider rate limits | Technical | 3 | 2 | 6 | HIGH | Implement caching | DevLead |
| R2 | Key developer leaves | Resource | 4 | 1 | 4 | MEDIUM | Cross-training | PM |
```

### Step 6: Define Monitoring Plan

Specify how risks will be monitored:

```markdown
## Risk Monitoring

| Risk ID | Trigger | Monitor Frequency | Escalation |
|---------|---------|-------------------|------------|
| R1 | API errors > 5% | Daily | Escalate to architect |
| R2 | Resignation notice | Immediate | Escalate to PM |
```

## Checklist

Copy this checklist and track your progress:

- [ ] Review architecture for complexity points
- [ ] Identify technical risks
- [ ] Identify schedule risks
- [ ] Identify resource risks
- [ ] Identify external risks
- [ ] Identify scope risks
- [ ] Assess impact for each risk (1-4)
- [ ] Assess probability for each risk (1-4)
- [ ] Calculate risk scores
- [ ] Prioritize risks by score
- [ ] Define mitigation for CRITICAL risks
- [ ] Define mitigation for HIGH risks
- [ ] Create risk register
- [ ] Define monitoring plan
- [ ] Assign risk owners

## Examples

### Example: Authentication System Risks

```markdown
# Risk Assessment: Authentication System

## Identified Risks

### Technical Risks

**R1: OAuth Provider Rate Limits**
- Description: Third-party OAuth provider may rate-limit our requests during peak traffic
- Category: Technical
- Impact: HIGH (3) - Users unable to login
- Probability: POSSIBLE (2) - Peak traffic is 10x normal
- Score: 6 (HIGH)
- Mitigation: Implement token caching, prepare fallback OAuth provider
- Owner: Backend Lead
- Status: Monitoring

**R2: Token Storage Security Breach**
- Description: Tokens stored insecurely could be compromised
- Category: Technical
- Impact: CRITICAL (4) - Data breach, compliance violation
- Probability: UNLIKELY (1) - We follow security best practices
- Score: 4 (MEDIUM)
- Mitigation: Encrypt tokens at rest, implement rotation
- Owner: Security Lead
- Status: Mitigated

### Resource Risks

**R3: Single Senior Developer on Auth**
- Description: Only one developer has deep auth expertise
- Category: Resource
- Impact: HIGH (3) - Major delays if unavailable
- Probability: UNLIKELY (1) - No indication of departure
- Score: 3 (MEDIUM)
- Mitigation: Cross-training sessions, documentation
- Owner: Tech Lead
- Status: In Progress

## Risk Matrix

           | Low (1) | Medium (2) | High (3) | Critical (4)
-----------|---------|------------|----------|-------------
Certain(4) |    4    |     8      |    12    |     16
Likely (3) |    3    |     6      |     9    |     12
Possible(2)|    2    |     4      |     6    |      8
Unlikely(1)|    1    |     2      |   R2,R3  |      4

## Top Risks Summary

1. **R1 - OAuth Rate Limits** (Score: 6)
   - Action: Implement caching layer by Week 2

2. **R2 - Token Security** (Score: 4)
   - Action: Security review complete by Week 1
```

### Example: Risk Register Template

```markdown
| ID | Risk | Category | Impact | Probability | Score | Priority | Mitigation | Owner | Status |
|----|------|----------|--------|-------------|-------|----------|------------|-------|--------|
| R1 | OAuth rate limits | Technical | 3 | 2 | 6 | HIGH | Caching + fallback | BackendLead | Open |
| R2 | Token security | Technical | 4 | 1 | 4 | MEDIUM | Encryption | SecurityLead | Mitigated |
| R3 | Single point of failure | Resource | 3 | 1 | 3 | MEDIUM | Cross-training | TechLead | In Progress |
| R4 | API deprecation | External | 2 | 2 | 4 | MEDIUM | Version monitoring | DevOps | Monitoring |
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Risks not specific enough | Generic risk descriptions | Rewrite with specific scenarios |
| All risks marked HIGH | Assessment bias | Re-calibrate using examples |
| No mitigation defined | Incomplete analysis | Define at least one mitigation per HIGH risk |
| Risks not updated | Stale register | Schedule weekly risk review |
| Missing risk categories | Narrow focus | Use category checklist systematically |

## Related Operations

- [op-design-architecture.md](op-design-architecture.md) - Architecture informs risk analysis
- [op-create-roadmap.md](op-create-roadmap.md) - Risks influence roadmap sequencing
- [op-plan-implementation.md](op-plan-implementation.md) - Tasks include risk mitigation activities
