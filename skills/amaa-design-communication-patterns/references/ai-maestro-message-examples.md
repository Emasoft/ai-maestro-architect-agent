# AI Maestro Message Examples

Concrete JSON examples showing the structure of messages sent through the `agent-messaging` skill.

> **Note**: These structures show conceptual message content. Use the `agent-messaging` skill to send messages — it handles the exact API format automatically.

## Example 1: Design Request Acknowledgment

When AMCOS assigns a design task:

```json
{
  "from": "amaa-architect-main-agent",
  "to": "amcos",
  "subject": "Design Request Acknowledged",
  "priority": "normal",
  "content": {
    "type": "acknowledgment",
    "message": "Design request received for E-Commerce Product Catalog. Starting requirements analysis. ETA: 2 hours."
  }
}
```

## Example 2: Clarification Request (Blocking)

When requirements are ambiguous or conflicting:

```json
{
  "from": "amaa-architect-main-agent",
  "to": "amcos",
  "subject": "Clarification Needed - Payment Gateway Integration",
  "priority": "high",
  "content": {
    "type": "clarification_request",
    "message": "BLOCKING: Requirement ambiguity detected. Question: Should payment processing be synchronous or asynchronous? Context: User said 'fast payment processing' but also 'reliable with retries'. Synchronous = fast but no retries. Asynchronous = reliable retries but slower user feedback. Cannot proceed until clarified. Details: docs_dev/design/clarifications/20260204-payment-flow.md"
  }
}
```

## Example 3: Design Completion Report

When all design artifacts are ready:

```json
{
  "from": "amaa-architect-main-agent",
  "to": "amcos",
  "subject": "Design Complete - E-Commerce Product Catalog",
  "priority": "normal",
  "content": {
    "type": "design_complete",
    "message": "[DONE] Design for E-Commerce Product Catalog complete. Architecture: REST API + PostgreSQL + Redis cache + React frontend. Modules: 5 (product-service, inventory-service, search-service, cart-service, frontend). Risks: 1/3/2. Handoff doc: docs_dev/design/handoff-a7f8b2d4.md. Ready for AMOA assignment."
  }
}
```
