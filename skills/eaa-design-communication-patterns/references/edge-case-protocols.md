# Edge Case Protocols for Architect Agent

This document defines standardized protocols for handling edge cases and failure scenarios in the Architect Agent (eaa-) plugin.

## Table of Contents

- 1.0 AI Maestro Unavailable
  - 1.1 Detection Methods
  - 1.2 Response Workflow
  - 1.3 Fallback Design Delivery
- 2.0 GitHub Unavailable
  - 2.1 Detection Methods
  - 2.2 Response Workflow
  - 2.3 Design Document Caching
- 3.0 Remote Agent Timeout
  - 3.1 Detection Methods
  - 3.2 Research Agent Timeout
  - 3.3 Documentation Agent Timeout
- 4.0 Requirements Ambiguity
  - 4.1 Detection Methods
  - 4.2 Clarification Protocol
  - 4.3 Assumption Documentation
- 5.0 API Research Failures
  - 5.1 API Documentation Unavailable
  - 5.2 API Deprecated/Changed
  - 5.3 Rate Limits During Research
- 6.0 Design Conflicts
  - 6.1 Conflicting Requirements
  - 6.2 Technical Constraint Conflicts
  - 6.3 Stakeholder Disagreements
- 7.0 Planning Validation Failures
  - 7.1 Incomplete Module Specifications
  - 7.2 Circular Dependencies
  - 7.3 Infeasible Timelines

---

## 1.0 AI Maestro Unavailable

### 1.1 Detection Methods

The Architect uses AI Maestro to receive requirements from Assistant Manager and deliver designs. Detect unavailability through:

| Check | Command | Failure Indicator |
|-------|---------|-------------------|
| API Health | `curl -s "$AIMAESTRO_API/health"` | HTTP 503/504 or timeout |
| Connection Test | `curl -m 10 "$AIMAESTRO_API/api/messages?agent=$SESSION_NAME&action=unread-count"` | Connection timeout after 10 seconds |
| Agent Registry | `curl -s "$AIMAESTRO_API/api/agents"` | Registry unreachable |

### 1.2 Response Workflow

When AI Maestro is unavailable:

1. **Log the failure**:
   ```bash
   echo "$(date -Iseconds) | AIMAESTRO_UNAVAILABLE | $AIMAESTRO_API" >> .claude/logs/maestro-failures.log
   ```

2. **Queue outgoing messages**:
   ```bash
   mkdir -p .claude/queue/outbox
   cat > ".claude/queue/outbox/${RECIPIENT}-$(date +%s).json" <<EOF
   {
     "to": "${RECIPIENT}",
     "subject": "Design Delivery: ${PROJECT_NAME}",
     "priority": "high",
     "content": {"type": "design_delivery", "message": "Design complete. See handoff file."},
     "queued_at": "$(date -Iseconds)"
   }
   EOF
   ```

3. **Display warning**:
   ```
   WARNING: AI Maestro is unavailable.
   - Design documents saved locally
   - Handoff file created at: .claude/handoffs/design-{uuid}.md
   - Will notify Orchestrator when service recovers
   ```

4. **Use fallback delivery** (see 1.3)

5. **Retry every 5 minutes**
   - After 30 minutes, require user intervention

### 1.3 Fallback Design Delivery

When AI Maestro is down, deliver designs via:

| Priority | Method | Use Case |
|----------|--------|----------|
| 1st | GitHub Issue | Create design issue with full specification |
| 2nd | Handoff .md files | Store in shared directory |
| 3rd | Direct file creation | Create in Orchestrator's working directory |

**GitHub Issue Fallback Template**:
```markdown
## Design Delivery (AI Maestro Offline)

**Project**: ${PROJECT_NAME}
**Architect**: eaa-main
**Status**: Ready for Orchestration

### Design Documents
- Architecture: `.claude/design/${PROJECT_NAME}/architecture.md`
- Modules: `.claude/design/${PROJECT_NAME}/modules.md`
- Handoff: `.claude/handoffs/design-${UUID}.md`

### Summary
[High-level design summary]

### Next Steps
Orchestrator should pick up handoff file and begin module assignment.

---
*Note: AI Maestro unavailable. Manual handoff required.*
```

---

## 2.0 GitHub Unavailable

### 2.1 Detection Methods

| Check | Command | Failure Indicator |
|-------|---------|-------------------|
| API Status | `gh api rate_limit` | HTTP 5xx errors |
| Network | `gh repo view` | Network failure |
| Rate Limit | `gh api rate_limit --jq '.rate.remaining'` | Returns 0 |

### 2.2 Response Workflow

1. **Cache any GitHub data needed**:
   ```bash
   mkdir -p .claude/cache/github
   gh issue list --json number,title,body,labels > .claude/cache/github/issues.json
   echo "$(date -Iseconds)" > .claude/cache/github/cached_at
   ```

2. **Continue with local design work**:
   - Write design documents locally
   - Create architecture diagrams
   - Generate module specifications
   - Save all to `.claude/design/`

3. **Queue GitHub operations**:
   ```bash
   mkdir -p .claude/queue/github
   cat > ".claude/queue/github/op-$(date +%s).json" <<EOF
   {
     "operation": "issue_create",
     "title": "Design: ${PROJECT_NAME}",
     "body": "...",
     "labels": ["design", "architecture"],
     "queued_at": "$(date -Iseconds)"
   }
   EOF
   ```

4. **Notify user**:
   ```
   WARNING: GitHub is unavailable.
   - Design work continues locally
   - GitHub issue creation queued
   - Will sync when service recovers
   ```

5. **Retry every 10 minutes**

### 2.3 Design Document Caching

Maintain local design document repository:

| Document Type | Location | Format |
|---------------|----------|--------|
| Architecture | `.claude/design/{project}/architecture.md` | Markdown + Mermaid |
| Modules | `.claude/design/{project}/modules.md` | Structured Markdown |
| API Specs | `.claude/design/{project}/api-spec.md` | OpenAPI-like Markdown |
| Diagrams | `.claude/design/{project}/diagrams/` | Mermaid .mmd files |

---

## 3.0 Remote Agent Unresponsive

### 3.1 Detection Methods

AI agents collaborate asynchronously and may be hibernated for extended periods. Detection is based on **state**, not elapsed time.

| State | Detection | Priority |
|-------|-----------|----------|
| No ACK | Subagent has not acknowledged task | Normal |
| No Progress | Subagent acknowledged but no research/documentation progress | Normal |
| Stale | Subagent's last update predates significant events | High |
| Unresponsive | Multiple reminders sent without any response | Urgent |
| Offline | AI Maestro reports agent session terminated | Immediate |

### 3.2 Research Agent Unresponsive

When `eaa-api-researcher` is unresponsive:

1. **First Reminder (when state = No ACK or No Progress)**:
   ```bash
   curl -X POST "$AIMAESTRO_API/api/messages" \
     -d '{
       "to": "eaa-api-researcher",
       "subject": "Research Check: ${API_NAME}",
       "priority": "high",
       "content": {"type": "status_request", "message": "Please provide status update for ${API_NAME} research."}
     }'
   ```

2. **Wait 5 minutes**

3. **Urgent Reminder**: Note reassignment warning

4. **Reassign or proceed with cached data**:
   - Check for existing API documentation in cache
   - Search for alternative documentation sources
   - Document research as "PARTIAL - agent timeout"

5. **Proceed with assumptions** (document clearly):
   ```markdown
   ## API Research: ${API_NAME}

   **Status**: PARTIAL (Research agent timeout)

   ### Known Information
   - [Information from cache/prior knowledge]

   ### Assumptions Made
   - [ ] Assumption 1 - needs verification
   - [ ] Assumption 2 - needs verification

   ### Risks
   - Implementation may need adjustment when full API docs available
   ```

### 3.3 Documentation Agent Timeout

When `eaa-documentation-writer` times out:

1. **Follow escalation ladder** (same as 3.2)

2. **If unresolved, generate minimal documentation**:
   - Create stub documents with TODO markers
   - Include all technical details
   - Mark for later expansion

3. **Notify Orchestrator of partial delivery**:
   ```json
   {
     "status": "partial_delivery",
     "complete": ["architecture.md", "modules.md"],
     "incomplete": ["api-integration.md"],
     "reason": "documentation_agent_timeout"
   }
   ```

---

## 4.0 Requirements Ambiguity

### 4.1 Detection Methods

| Ambiguity Type | Detection Pattern |
|----------------|-------------------|
| Vague scope | "Handle X appropriately", "Support Y as needed" |
| Missing constraints | No performance/security requirements stated |
| Conflicting goals | "Fast AND thorough", "Simple AND comprehensive" |
| Undefined terms | Domain-specific terms without definition |
| Implicit assumptions | Requirements assume unstated context |

### 4.2 Clarification Protocol

1. **List all ambiguities**:
   ```
   REQUIREMENTS ANALYSIS - AMBIGUITIES DETECTED

   Vague Scope:
   1. "Handle errors appropriately" - Need specific error handling strategy
   2. "Support all common formats" - Need explicit format list

   Missing Constraints:
   1. No response time requirements specified
   2. No maximum resource usage defined

   Conflicting Goals:
   1. "Real-time processing" conflicts with "detailed logging"

   Undefined Terms:
   1. "Enterprise-grade" - Need specific criteria
   ```

2. **Generate clarification questions**:
   ```
   QUESTIONS FOR USER (via Assistant Manager):

   1. Error Handling:
      a) Should errors fail fast or attempt recovery?
      b) What should be logged vs displayed to user?

   2. Supported Formats:
      a) Please confirm: JSON, XML, CSV - any others?
      b) Should we support compressed formats?

   3. Performance:
      a) What is the acceptable response time? (<1s, <5s, <30s)
      b) Expected concurrent users?

   4. Clarify "Enterprise-grade":
      a) Does this require audit logging?
      b) Does this require multi-tenant support?
   ```

3. **Block design progression** until clarified

4. **Route questions to Assistant Manager** for user communication

### 4.3 Assumption Documentation

When user is unavailable and work must proceed:

1. **Document assumptions explicitly**:
   ```markdown
   ## Design Assumptions

   **WARNING**: The following assumptions were made due to unclear requirements.
   These MUST be verified before implementation.

   ### Assumption 1: Error Handling
   - **Assumed**: Fail-fast approach with detailed error messages
   - **Reason**: Most common pattern for developer tools
   - **Risk**: May need refactoring if recovery is required
   - **To Verify**: Confirm with user via Assistant Manager

   ### Assumption 2: Performance
   - **Assumed**: <5 second response time acceptable
   - **Reason**: No SLA specified, 5s is reasonable default
   - **Risk**: May need optimization if <1s required
   - **To Verify**: Get explicit performance requirements
   ```

2. **Mark design as PROVISIONAL**:
   ```json
   {
     "design_status": "PROVISIONAL",
     "assumptions_count": 3,
     "requires_verification": true,
     "verification_questions": [...]
   }
   ```

3. **Include assumption checklist in handoff**

---

## 5.0 API Research Failures

### 5.1 API Documentation Unavailable

**Detection**: Official docs return 404 or are significantly incomplete.

**Response Workflow**:

1. **Try alternative sources** (in order):
   | Source | Method |
   |--------|--------|
   | GitHub repo | Search for README, docs/, examples/ |
   | Stack Overflow | Search for API usage patterns |
   | DevDocs.io | Check for cached documentation |
   | Archive.org | Check for historical docs |

2. **If no docs found**:
   - Document API through experimentation (see `eaa-hypothesis-verification`)
   - Create minimal viable documentation from observed behavior
   - Mark integration as HIGH RISK

3. **Report to Assistant Manager**:
   ```
   API DOCUMENTATION ISSUE

   API: ${API_NAME}
   Issue: Official documentation unavailable

   Actions Taken:
   - Searched alternative sources: [list]
   - Created experimental documentation: [location]

   Recommendation:
   - Consider alternative API if available
   - OR proceed with high-risk integration
   - User decision required
   ```

### 5.2 API Deprecated/Changed

**Detection**: API returns deprecation warnings or behavior differs from docs.

**Response Workflow**:

1. **Identify changes**:
   ```markdown
   ## API Change Detection

   **API**: ${API_NAME}
   **Documented Version**: v2.1
   **Current Version**: v3.0

   ### Breaking Changes
   - Endpoint `/users` renamed to `/accounts`
   - Response format changed from XML to JSON
   - Authentication method changed

   ### Migration Required
   - [ ] Update endpoint URLs
   - [ ] Update response parsing
   - [ ] Update authentication
   ```

2. **Assess impact on design**:
   - Minor: Document and proceed
   - Major: Pause and report to user

3. **Update design to current API**

### 5.3 Rate Limits During Research

**Detection**: HTTP 429 or rate limit headers indicate exhaustion.

**Response Workflow**:

1. **Check rate limit status**:
   ```bash
   # Example for GitHub API
   gh api rate_limit --jq '.rate'
   ```

2. **If rate limited**:
   - Log the limit
   - Calculate reset time
   - Queue remaining research
   - Proceed with available information

3. **Notify user of delay**:
   ```
   RESEARCH DELAY: API Rate Limit

   API: ${API_NAME}
   Limit: 60 requests/hour
   Used: 60/60
   Reset: in 45 minutes

   Research is ${X}% complete.
   Will resume automatically after rate limit resets.
   ```

---

## 6.0 Design Conflicts

### 6.1 Conflicting Requirements

**Detection**: Requirements that cannot both be satisfied.

**Response Workflow**:

1. **Document the conflict**:
   ```markdown
   ## REQUIREMENT CONFLICT

   ### Requirement A
   "System must process requests in real-time (<100ms)"

   ### Requirement B
   "System must log all request details to external audit system"

   ### Conflict
   External audit logging adds 50-200ms latency, making real-time
   processing impossible.

   ### Options
   1. Async audit logging (satisfies A, weakens B)
   2. Accept higher latency (satisfies B, violates A)
   3. Local logging with async sync (compromise)
   ```

2. **Present options to user** via Assistant Manager

3. **Block design until resolved**

4. **Document resolution** for future reference

### 6.2 Technical Constraint Conflicts

**Detection**: Technical limitations prevent desired design.

**Response Workflow**:

1. **Document the constraint**:
   ```markdown
   ## TECHNICAL CONSTRAINT

   ### Desired Design
   Single binary deployment with no external dependencies

   ### Constraint
   Required library (OpenSSL) cannot be statically linked on target platform

   ### Impact
   - Binary will require OpenSSL runtime dependency
   - Deployment complexity increases

   ### Alternatives
   1. Use platform-native crypto (different API, more work)
   2. Accept OpenSSL dependency (simpler, external dependency)
   3. Bundle OpenSSL dynamically (larger binary, version management)
   ```

2. **Recommend solution with rationale**

3. **Get user approval before proceeding**

### 6.3 Stakeholder Disagreements

**Detection**: Different users/stakeholders provide conflicting direction.

**Response Workflow**:

1. **Document all positions**:
   ```markdown
   ## STAKEHOLDER CONFLICT

   ### Position A (User: Alice)
   "We need feature X implemented as top priority"

   ### Position B (User: Bob)
   "Feature X conflicts with our security requirements. Do Y instead."

   ### Analysis
   - Both positions have merit
   - Technical factors favor [analysis]
   - Business factors favor [analysis]
   ```

2. **Do not proceed** - escalate to Assistant Manager

3. **Request clear single decision-maker**

---

## 7.0 Planning Validation Failures

### 7.1 Incomplete Module Specifications

**Detection**: Module spec missing required fields.

| Required Field | Purpose |
|----------------|---------|
| `module_id` | Unique identifier |
| `description` | What the module does |
| `inputs` | What the module needs |
| `outputs` | What the module produces |
| `dependencies` | Other modules required |
| `success_criteria` | How to verify completion |

**Response Workflow**:

1. **List missing fields**:
   ```
   MODULE SPECIFICATION INCOMPLETE

   Module: auth-service

   Missing Fields:
   - [ ] success_criteria
   - [ ] inputs

   Cannot create handoff until specification is complete.
   ```

2. **Attempt to derive** from context if possible

3. **Request clarification** if cannot derive

### 7.2 Circular Dependencies

**Detection**: Module A depends on B, B depends on A.

**Response Workflow**:

1. **Visualize the cycle**:
   ```
   CIRCULAR DEPENDENCY DETECTED

   auth-service -> user-service -> permission-service -> auth-service
   ```

2. **Propose resolution**:
   - Identify the weakest dependency
   - Suggest interface extraction
   - Recommend module merge if appropriate

3. **Block handoff** until resolved

### 7.3 Infeasible Timelines

**Detection**: Estimated work exceeds available time/resources.

**Response Workflow**:

1. **Present the math**:
   ```markdown
   ## TIMELINE ANALYSIS

   ### Requested Deadline
   2 weeks (10 business days)

   ### Estimated Effort
   - Module A: 5 days
   - Module B: 4 days
   - Module C: 6 days
   - Integration: 3 days
   - Testing: 2 days
   **Total**: 20 days (with parallelization: 12 days minimum)

   ### Gap
   2 days over deadline even with maximum parallelization

   ### Options
   1. Extend deadline by 2 days
   2. Reduce scope (remove Module C)
   3. Add resources (parallel teams)
   4. Accept quality tradeoffs (reduce testing)
   ```

2. **Get user decision** before proceeding

3. **Document accepted tradeoffs**

---

## Emergency Recovery

If multiple edge cases compound:

1. **Save all design work locally**
2. **Create recovery checkpoint**:
   ```json
   {
     "checkpoint_type": "architect_emergency",
     "timestamp": "2025-01-29T15:00:00Z",
     "design_status": "IN_PROGRESS",
     "documents_saved": [...],
     "pending_clarifications": [...],
     "blocked_by": [...]
   }
   ```
3. **Notify Assistant Manager**
4. **Wait for user guidance**

Recovery checkpoint: `.claude/recovery/architect-checkpoint-{timestamp}.json`

---

## Related Documents

- **eaa-requirements-analysis** - Requirements patterns
- **eaa-api-research** (research-procedure.md reference) - API research
- **eaa-hypothesis-verification** - Testing assumptions
- **eaa-planning-patterns** (planning-checklist.md reference) - Planning validation
