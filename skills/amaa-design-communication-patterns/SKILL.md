---
name: amaa-design-communication-patterns
description: "Use when implementing inter-agent communication, messaging protocols, or design document standards across Architect Agent skills."
version: 1.0.0
compatibility: Requires AI Maestro installed.
context: fork
agent: amaa-planner
user-invocable: false
workflow-instruction: "Step 8"
procedure: "proc-submit-design"
triggers:
  - when needing communication pattern guidance
  - when sending or handling inter-agent messages
  - when following design document protocols
---

# Design Communication Patterns Skill

## Overview

This skill provides reference documentation for communication patterns, inter-agent messaging protocols, and design document standards used across all Architect Agent skills. It centralizes protocol definitions and operational procedures so that other skills can follow consistent patterns for messaging, handoffs, and task completion.

## Prerequisites

- Access to the amaa-design-communication-patterns skill directory
- AI Maestro installed and running (for inter-agent messaging)
- Understanding of which reference documents are available

## Instructions

1. Identify the communication pattern or protocol you need guidance on
2. Consult the appropriate reference document in `references/`
3. Follow the protocol or pattern as documented
4. Do not duplicate protocol definitions in individual skills

### Checklist

Copy this checklist and track your progress:

- [ ] Identify the communication pattern or protocol needed
- [ ] Locate the relevant reference document in `references/`
- [ ] Read and understand the protocol requirements
- [ ] Follow the documented pattern in your skill implementation
- [ ] Verify compliance with the protocol
- [ ] Do NOT duplicate protocol definitions in your skill

## Reference Documents

All shared resources are reference documentation files located in the `references/` directory:

| Reference | Description |
|-----------|-------------|
| [ai-maestro-message-templates.md](references/ai-maestro-message-templates.md) | AI Maestro inter-agent message templates and examples |
| [message-response-decision-tree.md](references/message-response-decision-tree.md) | Decision tree for handling and routing AI Maestro messages by priority and type |
| [design-document-protocol.md](references/design-document-protocol.md) | Standards for creating, validating, and searching design documents in the design/ folder |
| [proactive-handoff-protocol.md](references/proactive-handoff-protocol.md) | Automatic handoff triggers and inter-agent work transfer procedures |
| [task-completion-checklist.md](references/task-completion-checklist.md) | Pre-completion verification checklist before reporting a task as done |
| [edge-case-protocols.md](references/edge-case-protocols.md) | Standardized protocols for handling failure scenarios and edge cases |
| [op-load-shared-template.md](references/op-load-shared-template.md) | Operational procedure for loading shared templates |
| [op-access-shared-constants.md](references/op-access-shared-constants.md) | Operational procedure for accessing shared constants |
| [op-send-ai-maestro-message.md](references/op-send-ai-maestro-message.md) | Operational procedure for sending AI Maestro messages |
| [op-validate-with-schema.md](references/op-validate-with-schema.md) | Operational procedure for validating documents with schemas |

## Examples

### Example 1: Sending an Inter-Agent Message

Consult [ai-maestro-message-templates.md](references/ai-maestro-message-templates.md) for the correct message format, then use the AI Maestro API:

```bash
curl -X POST "http://localhost:23000/api/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "target-agent-name",
    "subject": "Design review request",
    "priority": "normal",
    "content": {"type": "request", "message": "Please review the design document."}
  }'
```

### Example 2: Deciding How to Handle an Incoming Message

Consult [message-response-decision-tree.md](references/message-response-decision-tree.md) to determine the correct routing and response strategy based on message priority and type.

### Example 3: Completing a Task with Verification

Before reporting a task as done, follow the checklist in [task-completion-checklist.md](references/task-completion-checklist.md) to verify all completion criteria are met.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Reference not found | Path incorrect or file missing | Verify the reference file exists in `references/` |
| Protocol mismatch | Following outdated pattern | Re-read the latest version of the reference document |
| Message delivery failed | AI Maestro not running | Ensure AI Maestro is installed and the API is reachable |
| Handoff rejected | Target agent unavailable | Follow edge-case protocols in [edge-case-protocols.md](references/edge-case-protocols.md) |

## Output

| Output Type | Format | Description |
|-------------|--------|-------------|
| Protocol guidance | Markdown reference docs | Step-by-step procedures for communication patterns |
| Message templates | Markdown with examples | Ready-to-use inter-agent message formats |
| Decision trees | Markdown flowcharts | Routing logic for message handling |
| Checklists | Markdown checklists | Verification steps for task completion and handoffs |

## Resources

- `references/` - All reference documentation (10 files covering protocols, templates, decision trees, and operational procedures)
- amaa-design-lifecycle - Related skill that follows design document protocols defined here
- amaa-requirements-analysis - Related skill that follows validation protocols defined here
- amaa-planning-patterns - Related skill that follows planning patterns defined here
