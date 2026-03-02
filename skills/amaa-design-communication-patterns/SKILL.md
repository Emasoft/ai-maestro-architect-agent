---
name: amaa-design-communication-patterns
description: "Use when implementing inter-agent communication, messaging protocols, or design document standards."
context: fork
agent: amaa-planner
user-invocable: false
---

# Design Communication Patterns Skill

## Overview

Centralizes communication patterns, messaging protocols, and design document standards for all Architect Agent skills. Requires AI Maestro installed and running.

## Prerequisites

- AI Maestro running and API accessible
- Reference documents present in `references/` directory
- Proper agent naming convention (domain-subdomain-name)

## Instructions

1. Identify the communication pattern or protocol needed
2. Consult the appropriate reference document in `references/`
3. Follow the protocol as documented
4. Do not duplicate protocol definitions in individual skills

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

- **Send message**: Use templates from [ai-maestro-message-templates.md](references/ai-maestro-message-templates.md) with the AI Maestro API
- **Route incoming message**: Follow [message-response-decision-tree.md](references/message-response-decision-tree.md)
- **Complete task**: Verify with [task-completion-checklist.md](references/task-completion-checklist.md)

## Error Handling

| Error | Solution |
|-------|----------|
| Reference not found | Verify file exists in `references/` |
| Message delivery failed | Ensure AI Maestro API is reachable |
| Handoff rejected | See [edge-case-protocols.md](references/edge-case-protocols.md) |

## Output

Protocol guidance, message templates, decision trees, and checklists as Markdown reference docs.

## Resources

- amaa-design-lifecycle - Skill lifecycle management
- amaa-requirements-analysis - Requirements documentation
- amaa-planning-patterns - Planning and design patterns
