# Risk Identification: Discovering What Could Go Wrong

## Table of Contents

1. [What is Risk Identification?](#what-is-risk-identification)
2. [Risk Identification in Four Steps](#risk-identification-in-four-steps)
   - [Step 1: Discover All Risks](#step-1-discover-all-risks)
   - [Step 2: Assess Impact and Probability](#step-2-assess-impact-and-probability)
   - [Step 3: Plan Mitigation Strategies](#step-3-plan-mitigation-strategies)
   - [Step 4: Create Risk Register and Monitoring Plan](#step-4-create-risk-register-and-monitoring-plan)
3. [Risk Categories](#risk-categories)
4. [Risk Identification Checklist](#risk-identification-checklist)
5. [Common Mistakes in Risk Identification](#common-mistakes-in-risk-identification)
6. [Next Steps](#next-steps)

## What is Risk Identification?

Risk identification is the process of systematically discovering, analyzing, and planning for obstacles that could prevent successful execution of your plan.

**Input**: The completed architecture design from the previous phase

**Output**: A risk register containing:
- All identified risks
- Impact assessment for each risk
- Probability of occurrence
- Mitigation strategies
- Ownership and monitoring plans

## Risk Identification in Four Steps

### Step 1: Discover All Risks

Use systematic methods to uncover risks you might otherwise miss.

**Method 1: Architecture-Based Risk Discovery**
Review each component from your architecture design:
1. For each component, ask: "What could cause this component to fail?"
2. List all failure modes
3. For each failure mode, ask: "What impact would this failure have?"

**Example**:
```
Component: UserDatabase

Possible failures:
  1. Database server crashes
  2. Disk runs out of space
  3. Network connection to database is lost
  4. Malicious hacker gains access
  5. Queries become very slow under load
  6. Data corruption occurs
  7. Backups fail silently

For each failure, ask impact:
  1. Crash → Users cannot log in → Service unavailable
  2. Disk full → Cannot write new records → Application hangs
  3. Network lost → Timeouts on every query → All operations blocked
  4. Hack → Data stolen/modified → Security breach, legal liability
  5. Slow queries → UI becomes unresponsive → Poor user experience
  6. Corruption → Reports show wrong data → Business decisions based on false data
  7. Backup fails → Cannot recover from disasters → Data loss
```

**Method 2: Dependency-Based Risk Discovery**
Review your dependency graph:
1. For each dependency, ask: "What if this dependency fails or is unavailable?"
2. List cascade effects

**Example**:
```
AuthenticationMiddleware depends on:
  - AuthenticationTokenValidator

Question: What if validator is unavailable?
  → All authentication fails
  → No users can access system
  → System is down for all users

Question: What if validator becomes very slow?
  → Every request is delayed by validator latency
  → User experience degrades
  → Requests timeout
```

**Method 3: Phase-Based Risk Discovery**
Consider risks that emerge at different project phases:

1. **Pre-launch risks**:
   - Key person leaves
   - Requirements change
   - Dependencies are delayed
   - Budget is cut

2. **Launch risks**:
   - Too much load
   - Security breach
   - Data corruption
   - Third-party service outage

3. **Post-launch risks**:
   - Difficult to maintain
   - Cannot scale
   - Users cannot be migrated from old system
   - Performance degrades over time

**Method 4: Stakeholder-Based Risk Discovery**
Ask stakeholders: "What keeps you up at night about this project?"

Common stakeholder concerns:
- **Business stakeholders**: Budget overruns, scope creep, poor adoption
- **Technical stakeholders**: Technical debt, scalability, maintainability
- **Security stakeholders**: Data breaches, compliance violations
- **Operations stakeholders**: Monitoring gaps, insufficient alerting
- **Users**: Performance, reliability, data privacy

### Step 2: Assess Impact and Probability

For each risk, determine how serious it is.

**Impact Assessment Template**:
```
Risk: [Name]
Description: [Specific description of what could go wrong]

Impact: [Low / Medium / High / Critical]
  - What happens if this risk occurs?
  - Who is affected? (users, business, team, security, etc.)
  - How many people/systems are affected?
  - What is the financial impact?
  - What is the reputational impact?

Probability: [Low / Medium / High]
  - How likely is this to occur?
  - What indicators would show this is happening?
  - Have we seen this problem before?

Risk Score: [Impact] × [Probability] = [Priority]
  - Critical × High = URGENT (address immediately)
  - High × High = URGENT
  - High × Medium = IMPORTANT (address soon)
  - Medium × High = IMPORTANT
  - Medium × Medium = MONITOR (watch carefully)
  - Everything else = LOW (acknowledge but deprioritize)
```

**Example**:
```
Risk: Database Server Crash

Description: The production database server experiences hardware failure
or software crash, becoming unavailable to the application.

Impact: CRITICAL
  - All database operations fail
  - Application cannot serve any requests
  - All users are locked out
  - Lost transactions (if no backup)
  - Business cannot operate
  - Revenue is lost (significant business impact)

Probability: MEDIUM
  - Database is running on single server (no redundancy)
  - Server is 3 years old (end of typical lifecycle)
  - No automatic failover mechanism exists
  - We have not experienced this in our service history

Risk Score: CRITICAL × MEDIUM = URGENT
  - Must be addressed before launch
  - This is a showstopper risk
```

### Step 3: Plan Mitigation Strategies

For each risk, create a plan to reduce likelihood or impact.

**Mitigation Strategy Template**:
```
Risk: [Name]

Mitigation Strategy 1: [Strategy name]
  Type: [Prevent / Reduce / Transfer / Accept]

  Describe exactly what to do:
    1. [Specific action]
    2. [Specific action]
    3. [Specific action]

  Cost: [Resources required]
  Effectiveness: [How much does this reduce risk?]
  Owner: [Who is responsible for implementing this?]
  Priority: [How urgent is this mitigation?]

Mitigation Strategy 2: [Alternative strategy]
  ...

Mitigation Strategy 3: [Third strategy option]
  ...

Selected Strategy: [Which one we will use and why]
```

**Mitigation Types Explained**:

1. **Prevent**: Stop the risk from occurring
   - Example risk: "Hacker gains database access"
   - Prevention: Implement strong passwords, encryption, access controls
   - Effectiveness: Very high (if done correctly)
   - Cost: Medium to high

2. **Reduce**: Lower probability or impact
   - Example risk: "Database server crashes"
   - Reduction: Add monitoring, alerting, and automatic restart
   - Effectiveness: High (cannot prevent all crashes, but reduces impact)
   - Cost: Medium

3. **Transfer**: Move risk to someone else
   - Example risk: "Cloud provider outage"
   - Transfer: Buy provider insurance, use multi-provider architecture
   - Effectiveness: High (financial protection)
   - Cost: High (but predictable)

4. **Accept**: Acknowledge the risk and live with it
   - Example risk: "Junior developer makes mistakes"
   - Acceptance: Have code reviews, testing, monitoring
   - Effectiveness: Low (does not prevent the problem)
   - Cost: Must budget for recovery/remediation
   - Use when: Prevention is too expensive, impact is acceptable

**Concrete Example**:
```
Risk: Database Server Crash (CRITICAL × MEDIUM = URGENT)

Mitigation Strategy 1: Database Replication
  Type: Prevent/Reduce

  Exact steps:
    1. Set up second database server in different data center
    2. Configure primary-replica replication (synchronous)
    3. Set up automatic failover using heartbeat monitoring
    4. Test failover monthly with production data
    5. Document recovery procedures

  Cost: Moderate development effort + $200/month hosting
  Effectiveness: 95% (prevents single-server crashes)
  Owner: Infrastructure team
  Priority: CRITICAL - Must complete before launch

Selected Strategy: Database Replication
  Why: Highest effectiveness + acceptable cost + critical importance
  Implementation: Early phase, before production launch
  Success criteria: Automatic failover works without data loss
  Monitoring: Heartbeat every 10 seconds, alert on failures
```

### Step 4: Create Risk Register and Monitoring Plan

Consolidate all risks into a single document with tracking.

**Risk Register Format**:
```
| Risk ID | Risk Name | Description | Impact | Probability | Score | Mitigation Strategy | Owner | Priority | Status |
|---------|-----------|-------------|--------|-------------|-------|-------------------|-------|----------|--------|
| R-001 | DB Crash | Single DB server failure | CRITICAL | MEDIUM | URGENT | Implement replication | InfoSec | CRITICAL | In Progress |
| R-002 | DDoS Attack | Malicious traffic floods API | HIGH | LOW | IMPORTANT | Rate limiting, WAF | Security | HIGH | Planning |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Monitoring Plan**:
```
For each risk, define:
  - How will we know if this risk is happening? (indicators)
  - Who checks for these indicators? (owner)
  - How often do they check? (frequency)
  - What action to take if indicator appears? (response plan)

Example:
  Risk: Database performance degradation
  Indicator: Query response time > 500ms for more than 1 minute
  Owner: Database administrator
  Frequency: Continuous monitoring with automated alerts
  Response:
    1. Alert sent to on-call engineer
    2. Check for resource exhaustion (CPU, memory, disk)
    3. Analyze slow query log
    4. Kill long-running queries if necessary
    5. Scale database resources if needed
```

## Risk Categories

Organize risks into these categories:

1. **Technical Risks**: Related to technology, architecture, implementation
   - Database failures, network issues, integration problems
   - Performance degradation, scalability limits
   - Technical debt, security vulnerabilities

2. **Resource Risks**: Related to people and capabilities
   - Key person leaves (too much knowledge in one person)
   - Skills gaps (team lacks required expertise)
   - Scope uncertainty (requirements not fully understood)
   - Budget constraints (not enough money to do proper job)

3. **Business Risks**: Related to requirements and market
   - Requirements change mid-project
   - Customer cancels project
   - Market conditions shift
   - Competitor releases similar product
   - Adoption is lower than expected

4. **External Risks**: Related to dependencies and third parties
   - Third-party service is unavailable
   - API changes from provider
   - Library goes unmaintained
   - Cloud provider increases prices

5. **Security Risks**: Related to data and access
   - Data breach (hacker steals information)
   - Insider threat (employee misuses access)
   - Privacy violations (incorrect data handling)
   - Compliance violations (breaks regulations)

6. **Operational Risks**: Related to running the system
   - Unclear runbooks cause mistakes during incidents
   - No backups exist, data is lost
   - Difficult to maintain system after launch
   - Inadequate monitoring prevents quick detection

## Risk Identification Checklist

- ☐ All components have been reviewed for possible failures
- ☐ All dependencies have been assessed for cascade failures
- ☐ At least 15 distinct risks have been identified
- ☐ Each risk has impact, probability, and score assessed
- ☐ Each risk has at least one mitigation strategy defined
- ☐ Mitigation strategies have cost estimates and priority levels
- ☐ Risk ownership is assigned to specific people
- ☐ Monitoring/indicators are defined for each risk
- ☐ Risk register has been created and formatted
- ☐ Stakeholders have reviewed and accepted the risk register
- ☐ High-probability, high-impact risks have been prioritized in roadmap

## Common Mistakes in Risk Identification

1. **Only listing technical risks**: Include business, resource, and operational risks
2. **Vague risk descriptions**: "System might fail" is too vague. "Load balancer crashes under 10,000 concurrent users" is specific
3. **No mitigation plan**: Identifying risk without planning how to handle it is useless
4. **Setting unrealistic mitigation dates**: If risk is CRITICAL, mitigation cannot be "after launch"
5. **Ignoring cascade effects**: Assessing risks in isolation misses how one failure triggers others
6. **No monitoring**: You cannot manage what you do not measure
7. **No ownership**: Unowned risks are ignored

## Next Steps

Once your risk register is complete:
1. Have stakeholders review and approve the risk register
2. Prioritize high-impact mitigation work in your roadmap
3. Move to Roadmap Creation (`roadmap-creation.md`) with architecture and risks as inputs
4. Use the risk register to inform task priorities and sequencing

---

**Related**:
- `step-by-step-procedures.md` - context of full planning process
- `architecture-design.md` - input to risk identification
