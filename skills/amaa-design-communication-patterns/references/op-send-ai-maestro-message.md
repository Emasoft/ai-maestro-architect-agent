---
operation: send-ai-maestro-message
procedure: proc-submit-design
workflow-instruction: Step 8 - Design Submission
parent-skill: eaa-design-communication-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Send AI Maestro Inter-Agent Message


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Determine Message Parameters](#step-1-determine-message-parameters)
  - [Step 2: Send the Message](#step-2-send-the-message)
  - [Step 3: Verify Delivery](#step-3-verify-delivery)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: Notify Orchestrator of Design Completion](#example-notify-orchestrator-of-design-completion)
  - [Example: Request Code Review from Integrator](#example-request-code-review-from-integrator)
  - [Example: Handoff Work to Implementation Agent](#example-handoff-work-to-implementation-agent)
  - [Example: Urgent Escalation](#example-urgent-escalation)
- [Message Types](#message-types)
- [Priority Levels](#priority-levels)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Trigger this operation when:
- Notifying other agents about design completion or changes
- Requesting assistance from specialized agents
- Reporting status updates to the orchestrator
- Handing off work to another agent
- Escalating issues that require human attention

## Prerequisites

- AI Maestro service running
- Knowledge of target agent session name
- Understanding of message types and priorities
- The `agent-messaging` skill available

## Procedure

### Step 1: Determine Message Parameters

Identify:
- **Target agent**: Full session name (e.g., `orchestrator-master`, `helper-agent-generic`)
- **Message type**: request, response, notification, or handoff
- **Priority**: urgent, high, normal, or low
- **Subject**: Brief summary
- **Message content**: Details

### Step 2: Send the Message

Send a message using the `agent-messaging` skill with:
- **Recipient**: `<target-agent>`
- **Subject**: `<subject>`
- **Priority**: `<priority>`
- **Content**: `{"type": "<message-type>", "message": "<message-text>"}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

### Step 3: Verify Delivery

The `agent-messaging` skill will return a delivery confirmation with a message ID upon success.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify target agent full session name
- [ ] Determine appropriate priority level
- [ ] Determine message type (request/response/notification/handoff)
- [ ] Compose clear, concise subject line
- [ ] Write message content with all necessary details
- [ ] Verify AI Maestro is running
- [ ] Send message using the `agent-messaging` skill
- [ ] Verify delivery in response
- [ ] If urgent, consider following up if no response within timeout

## Examples

### Example: Notify Orchestrator of Design Completion

Send a message using the `agent-messaging` skill with:
- **Recipient**: `orchestrator-master`
- **Subject**: `Design Document Completed: Auth Service`
- **Priority**: `normal`
- **Content**: `{"type": "notification", "message": "Design document PROJ-SPEC-20250129-a1b2c3d4 completed and ready for review. Location: docs/design/specs/auth-service.md. Status: draft -> review."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

### Example: Request Code Review from Integrator

Send a message using the `agent-messaging` skill with:
- **Recipient**: `eia-integrator-main-agent`
- **Subject**: `Review Request: Auth Service Design`
- **Priority**: `high`
- **Content**: `{"type": "request", "message": "Please review design document at docs/design/specs/auth-service.md. Focus areas: security requirements, API contracts. GitHub issue: #123."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

### Example: Handoff Work to Implementation Agent

Send a message using the `agent-messaging` skill with:
- **Recipient**: `helper-agent-generic`
- **Subject**: `Handoff: Implement Auth Service per Design`
- **Priority**: `normal`
- **Content**: `{"type": "handoff", "message": "Design approved. Please implement according to docs/design/specs/auth-service.md. Key requirements: 1) OAuth2 flow implementation, 2) JWT token generation, 3) Session management. GitHub issue: #123."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

### Example: Urgent Escalation

Send a message using the `agent-messaging` skill with:
- **Recipient**: `orchestrator-master`
- **Subject**: `URGENT: Design Conflict Detected`
- **Priority**: `urgent`
- **Content**: `{"type": "notification", "message": "Conflicting requirements detected between auth-service.md and user-service.md. Cannot proceed without clarification. Blocking issue: Both define conflicting session handling strategies."}`
- **Verify**: Confirm the message was delivered by checking the `agent-messaging` skill send confirmation.

## Message Types

| Type | Purpose | Expected Response |
|------|---------|-------------------|
| `request` | Asking for action/information | Response message expected |
| `response` | Reply to a request | None (completes exchange) |
| `notification` | Informational update | None required |
| `handoff` | Transferring work ownership | Acknowledgment expected |

## Priority Levels

| Priority | Use Case | Expected Handling |
|----------|----------|-------------------|
| `urgent` | Blocking issues, critical failures | Immediate attention |
| `high` | Important updates, time-sensitive | Handle within current task |
| `normal` | Standard notifications | Handle when convenient |
| `low` | Non-critical information | Handle when idle |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Connection refused` | AI Maestro not running | Start AI Maestro service |
| `404 Not Found` | Wrong endpoint | Use `/api/messages` |
| `400 Bad Request` | Malformed JSON | Check JSON syntax |
| `422 Invalid agent` | Target agent not registered | Verify agent session name |
| `500 Server Error` | AI Maestro internal error | Check AI Maestro logs |

## Related Operations

- [op-access-shared-constants.md](op-access-shared-constants.md) - PRIORITY_LEVELS and MESSAGE_TYPES constants
- [ai-maestro-message-templates.md](ai-maestro-message-templates.md) - Full message template reference
- [message-response-decision-tree.md](message-response-decision-tree.md) - How to handle responses
