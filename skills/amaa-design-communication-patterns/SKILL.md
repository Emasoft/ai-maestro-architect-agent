---
name: amaa-design-communication-patterns
description: "Use when implementing inter-agent messaging or design document protocols. Trigger with communication pattern or messaging request."
context: fork
agent: amaa-architect-main-agent
user-invocable: false
---

# Design Communication Patterns Skill

## Overview

Centralizes communication patterns, messaging protocols, and design document standards. Requires AI Maestro running.

## Prerequisites

- AI Maestro running and API accessible
- Reference documents present in `references/` directory
- Proper agent naming convention (domain-subdomain-name)

## Instructions

1. Identify the communication pattern or protocol needed
2. Consult the appropriate reference document in `references/`
3. Follow the protocol as documented
4. Do not duplicate protocol definitions in individual skills

Copy this checklist and track your progress:
- [ ] Identified the communication pattern or protocol needed
- [ ] Consulted the appropriate reference document in `references/`
- [ ] Followed the protocol as documented
- [ ] Verified no duplicate protocol definitions in individual skills

## Reference Documents

All shared resources are reference documentation files located in the `references/` directory:

| Reference | Description |
|-----------|-------------|
| [ai-maestro-message-templates.md](references/ai-maestro-message-templates.md) | AI Maestro message templates (**1.1** Sending acknowledgment when receiving a design request from AMCOS, **1.2** Requesting clarification from AMCOS for ambiguous requirements) |
| [message-response-decision-tree.md](references/message-response-decision-tree.md) | Decision tree for routing messages (Step 1: Priority Triage, Step 2: Message Type Routing, Step 3: Response Actions) |
| [design-document-protocol.md](references/design-document-protocol.md) | Standards for creating, validating, and searching design documents in the design/ folder (Document UUID Format, Required Frontmatter Schema, Document Lifecycle, Validation Procedures) |
| [proactive-handoff-protocol.md](references/proactive-handoff-protocol.md) | Automatic handoff triggers and inter-agent work transfer procedures (Standard Handoff Format, Automatic Handoff Triggers, Mandatory Handoff Sections, Proactive Writing Rules, Handoff Quality Checklist) |
| [task-completion-checklist.md](references/task-completion-checklist.md) | Pre-completion checklist (Before Reporting Task Complete, Acceptance Criteria Met, Quality Gates Passed) |
| [edge-case-protocols.md](references/edge-case-protocols.md) | Failure scenario protocols (0 AI Maestro Unavailable, 1 Detection Methods, 2 Response Workflow) |
| [op-load-shared-template.md](references/op-load-shared-template.md) | Operational procedure for loading shared templates (When to Use, Prerequisites, Procedure) |
| [op-access-shared-constants.md](references/op-access-shared-constants.md) | Operational procedure for accessing shared constants (When to Use, Prerequisites, Procedure) |
| [op-send-ai-maestro-message.md](references/op-send-ai-maestro-message.md) | Operational procedure for sending AI Maestro messages (When to Use, Prerequisites, Procedure) |
| [op-validate-with-schema.md](references/op-validate-with-schema.md) | Operational procedure for validating documents with schemas (When to Use, Prerequisites, Procedure) |

## Examples

- **Send message**: Use templates from [ai-maestro-message-templates.md](references/ai-maestro-message-templates.md) (**1.1** Sending acknowledgment when receiving a design request from AMCOS, **1.2** Requesting clarification from AMCOS for ambiguous requirements)
- **Route incoming message**: Follow [message-response-decision-tree.md](references/message-response-decision-tree.md) (Step 1: Priority Triage, Step 2: Message Type Routing)
- **Complete task**: Verify with [task-completion-checklist.md](references/task-completion-checklist.md) (Before Reporting Task Complete, Acceptance Criteria Met)

Send an AI Maestro message using the curl API:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "target-agent-name",
    "subject": "Design document ready for review",
    "priority": "normal",
    "content": {"type": "notification", "message": "Handoff doc written to docs_dev/handoffs/handoff-abc123.md"}
  }'
```

## Error Handling

| Error | Solution |
|-------|----------|
| Reference not found | Verify file exists in `references/` |
| Message delivery failed | Ensure AI Maestro API is reachable |
| Handoff rejected | See [edge-case-protocols.md](references/edge-case-protocols.md) (0 AI Maestro Unavailable, 1 Detection Methods) |

## Output

Protocol guidance, message templates, decision trees, and checklists as Markdown reference docs.

## Resources

- amaa-design-lifecycle - Skill lifecycle management
- amaa-requirements-analysis - Requirements documentation
- amaa-planning-patterns - Planning and design patterns
