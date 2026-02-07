# AI Maestro Message Templates for EAA

This document provides all message templates and format examples for the Emasoft Architect Agent (EAA) to communicate via AI Maestro using the `agent-messaging` skill.

## Contents

- **1.1** Sending acknowledgment when receiving a design request from ECOS
- **1.2** Requesting clarification from ECOS for ambiguous requirements
- **1.3** Reporting design completion to ECOS
- **1.4** Notifying ECOS that handoff document is ready for EOA
- **1.5** Reporting blocker that prevents design progress
- **1.6** Verifying ACK receipt after sending a message
- **1.7** Retrying message when ACK not received within 30 seconds
- **1.8** Escalating to ECOS when ACK timeout occurs after retry

---

## 1.1 Sending Acknowledgment When Receiving Design Request from ECOS

**Use Case:** ECOS assigns you a design task via AI Maestro. You must acknowledge receipt and provide an ETA.

Send a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `Design Request Acknowledged`
- **Priority**: `normal`
- **Content**: `{"type": "acknowledgment", "message": "Design request received for [PROJECT_NAME]. Starting requirements analysis. ETA: [ESTIMATED_COMPLETION_TIME]."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Example Content:**
```json
{
  "type": "acknowledgment",
  "message": "Design request received for E-Commerce Product Catalog. Starting requirements analysis. ETA: 2 hours."
}
```

---

## 1.2 Requesting Clarification from ECOS for Ambiguous Requirements

**Use Case:** User requirements are ambiguous, conflicting, or unclear. You cannot proceed until clarification is received.

Send a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `Clarification Needed - [PROJECT_NAME]`
- **Priority**: `high`
- **Content**: `{"type": "clarification_request", "message": "BLOCKING: Requirement ambiguity detected. Question: [SPECIFIC_QUESTION]. Context: [USER_REQUIREMENT_QUOTE]. Cannot proceed until clarified. Details: docs_dev/design/clarifications/[TIMESTAMP]-[ISSUE].md"}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Example Content:**
```json
{
  "type": "clarification_request",
  "message": "BLOCKING: Requirement ambiguity detected. Question: Should payment processing be synchronous or asynchronous? Context: User said 'fast payment processing' but also 'reliable with retries'. Synchronous = fast but no retries. Asynchronous = reliable retries but slower user feedback. Cannot proceed until clarified. Details: docs_dev/design/clarifications/20260204-payment-flow.md"
}
```

---

## 1.3 Reporting Design Completion to ECOS

**Use Case:** All design artifacts are complete, and handoff document is prepared. You are ready for ECOS to assign the work to EOA.

Send a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `Design Complete - [PROJECT_NAME]`
- **Priority**: `normal`
- **Content**: `{"type": "design_complete", "message": "[DONE] Design for [PROJECT_NAME] complete. Architecture: [BRIEF_SUMMARY]. Modules: [MODULE_COUNT]. Risks: [HIGH_COUNT]/[MEDIUM_COUNT]/[LOW_COUNT]. Handoff doc: docs_dev/design/handoff-[UUID].md. Ready for EOA assignment."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Example Content:**
```json
{
  "type": "design_complete",
  "message": "[DONE] Design for E-Commerce Product Catalog complete. Architecture: REST API + PostgreSQL + Redis cache + React frontend. Modules: 5 (product-service, inventory-service, search-service, cart-service, frontend). Risks: 1/3/2. Handoff doc: docs_dev/design/handoff-a7f8b2d4.md. Ready for EOA assignment."
}
```

---

## 1.4 Notifying ECOS That Handoff Document is Ready for EOA

**Use Case:** Design artifacts are complete and packaged in a handoff document. You are notifying ECOS that the handoff is ready for EOA assignment.

Send a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `Handoff Ready - [PROJECT_NAME]`
- **Priority**: `normal`
- **Content**: `{"type": "handoff", "message": "Design handoff ready for [PROJECT_NAME]. Implementation sequence: [PHASE_1] -> [PHASE_2] -> [PHASE_3]. Critical path: [TOP_3_ITEMS]. All artifacts in docs_dev/design/. Handoff doc: handoff-[UUID].md. Awaiting EOA assignment from ECOS."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Example Content:**
```json
{
  "type": "handoff",
  "message": "Design handoff ready for Payment Gateway Integration. Implementation sequence: Phase 1 (Database schema + Payment model) -> Phase 2 (Stripe API integration) -> Phase 3 (Webhook handlers + retry logic) -> Phase 4 (Frontend payment form). Critical path: Stripe API credentials, webhook endpoint setup, PCI compliance review. All artifacts in docs_dev/design/. Handoff doc: handoff-c3e9f1a8.md. Awaiting EOA assignment from ECOS."
}
```

---

## 1.5 Reporting Blocker That Prevents Design Progress

**Use Case:** You cannot proceed due to missing information, infeasible requirement, or external dependency. You must escalate to ECOS for user decision.

Send a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `BLOCKED - [PROJECT_NAME]`
- **Priority**: `urgent`
- **Content**: `{"type": "blocker", "message": "[BLOCKED] Design for [PROJECT_NAME]. Blocker: [SPECIFIC_ISSUE]. Impact: [IMPACT_DESCRIPTION]. Next: [WHAT_IS_NEEDED]. Details: docs_dev/design/blockers/[TIMESTAMP]-[ISSUE].md. Awaiting user decision."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Example Content:**
```json
{
  "type": "blocker",
  "message": "[BLOCKED] Design for Real-Time Analytics Dashboard. Blocker: User requires <100ms query latency for 1M+ records, but available database (PostgreSQL) cannot meet this requirement without significant infrastructure changes (distributed architecture, caching layer, query optimization). Impact: Cannot design system without clarifying performance vs. cost trade-off. Next: User must choose: (A) Relax latency requirement to <1s, (B) Increase budget for distributed architecture (Elasticsearch + Redis), or (C) Reduce dataset size via data retention policy. Details: docs_dev/design/blockers/20260204-latency-requirement.md. Awaiting user decision."
}
```

---

## 1.6 Verifying ACK Receipt After Sending a Message

**Use Case:** After sending any AI Maestro message, you must verify that an ACK (acknowledgment) was received within 30 seconds.

Check your inbox using the `agent-messaging` skill. Filter for messages with subjects containing "ACK".

**Workflow:**
1. Send AI Maestro message using the `agent-messaging` skill
2. Wait 30 seconds
3. Check your inbox using the `agent-messaging` skill for ACK messages
4. If ACK received: Proceed with next operation
5. If NO ACK received: Proceed to **1.7 (Retry)**

---

## 1.7 Retrying Message When ACK Not Received Within 30 Seconds

**Use Case:** You sent a message but did not receive ACK within 30 seconds. You must retry ONCE before escalating.

Send a message using the `agent-messaging` skill with:
- **Recipient**: `[ORIGINAL_TARGET]`
- **Subject**: `[RETRY] [ORIGINAL_SUBJECT]`
- **Priority**: `high`
- **Content**: `{"type": "retry", "message": "[ORIGINAL_MESSAGE] (Retry: No ACK received within 30s)"}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Workflow After Retry:**
1. Send retry message using the `agent-messaging` skill
2. Wait another 30 seconds
3. Check inbox for ACK (see **1.6**)
4. If ACK received: Proceed with next operation
5. If STILL NO ACK: Proceed to **1.8 (Escalate)**

---

## 1.8 Escalating to ECOS When ACK Timeout Occurs After Retry

**Use Case:** You sent a message, retried after 30 seconds, and STILL received no ACK after another 30 seconds. You must escalate to ECOS.

Send a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `ACK Timeout Escalation`
- **Priority**: `urgent`
- **Content**: `{"type": "escalation", "message": "ACK timeout from [TARGET]. Original message: [SUBJECT]. Sent: [TIMESTAMP]. Retry sent: [RETRY_TIMESTAMP]. Blocking operation: [BLOCKED_OPERATION]."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Example Content:**
```json
{
  "type": "escalation",
  "message": "ACK timeout from eaa-api-researcher. Original message: API Research Request - Stripe Integration. Sent: 2026-02-05 14:30:00. Retry sent: 2026-02-05 14:30:30. Blocking operation: Cannot finalize architecture without Stripe API research results."
}
```

---

## AI Maestro ACK Protocol Summary

**Complete workflow for reliable message delivery:**

1. **Send message** using the `agent-messaging` skill (see sections 1.1-1.5)
2. **Wait 30 seconds**
3. **Verify ACK** (see section 1.6)
4. **If no ACK**: Retry ONCE (see section 1.7)
5. **Wait 30 seconds again**
6. **Verify ACK again** (see section 1.6)
7. **If still no ACK**: Escalate to ECOS (see section 1.8)
8. **Do NOT proceed** with dependent operations until ACK received

**CRITICAL:** Never proceed with operations that depend on the message being received until ACK is confirmed!

---

## Message Field Reference

All AI Maestro messages use this JSON structure:

```json
{
  "from": "<your-agent-name>",       // Required: Your agent identifier
  "to": "<target-agent-name>",       // Required: Target agent identifier
  "subject": "<message-subject>",    // Required: Brief subject line
  "priority": "<priority-level>",    // Required: "normal", "high", or "urgent"
  "content": {                       // Required: Message content object
    "type": "<message-type>",        // Required: Message classification
    "message": "<message-text>"      // Required: Actual message content
  }
}
```

**Valid Priority Levels:**
- `"normal"` - Standard messages (acknowledgments, status updates, completion reports)
- `"high"` - Important messages requiring attention (clarification requests, retries)
- `"urgent"` - Critical messages requiring immediate action (blockers, escalations, ACK timeouts)

**Common Message Types:**
- `"acknowledgment"` - Confirming receipt of a message or task
- `"clarification_request"` - Requesting additional information
- `"design_complete"` - Reporting design completion
- `"handoff"` - Notifying handoff readiness
- `"blocker"` - Reporting blocking issue
- `"retry"` - Retrying a previous message
- `"escalation"` - Escalating an issue to higher authority

---

## Example: Complete Message Send and Verify Workflow

**Step 1:** Send a design completion message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `Design Complete - User Authentication System`
- **Priority**: `normal`
- **Content**: `{"type": "design_complete", "message": "[DONE] Design for User Authentication System complete. Architecture: FastAPI + PostgreSQL + JWT auth + bcrypt hashing. Modules: 3 (auth-service, user-service, session-service). Risks: 0/2/1. Handoff doc: docs_dev/design/handoff-f4e8a9b1.md. Ready for EOA assignment."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Step 2:** Wait 30 seconds.

**Step 3:** Check your inbox using the `agent-messaging` skill. Filter for messages with subjects containing "ACK".

**Step 4:** If ACK received, proceed with next operation.

**Step 5 (if no ACK):** Retry by sending a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `[RETRY] Design Complete - User Authentication System`
- **Priority**: `high`
- **Content**: `{"type": "retry", "message": "[DONE] Design for User Authentication System complete. Architecture: FastAPI + PostgreSQL + JWT auth + bcrypt hashing. Modules: 3 (auth-service, user-service, session-service). Risks: 0/2/1. Handoff doc: docs_dev/design/handoff-f4e8a9b1.md. Ready for EOA assignment. (Retry: No ACK received within 30s)"}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

**Step 6:** Wait 30 seconds again.

**Step 7:** Check your inbox using the `agent-messaging` skill for ACK messages again.

**Step 8 (if still no ACK):** Escalate by sending a message using the `agent-messaging` skill with:
- **Recipient**: `ecos`
- **Subject**: `ACK Timeout Escalation`
- **Priority**: `urgent`
- **Content**: `{"type": "escalation", "message": "ACK timeout from ecos. Original message: Design Complete - User Authentication System. Sent: 2026-02-05 15:00:00. Retry sent: 2026-02-05 15:00:30. Blocking operation: Cannot proceed to next design task without confirmation that handoff was received."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

Then wait for manual intervention from ECOS.
