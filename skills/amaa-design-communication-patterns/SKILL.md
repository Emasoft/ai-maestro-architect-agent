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

## Checklist

Copy this checklist and track your progress:

- [ ] Identify needed communication pattern
- [ ] Consult reference document
- [ ] Follow protocol as documented

## Reference Documents

All shared resources are reference documentation files located in the `references/` directory:

| Reference | Description |
|-----------|-------------|
| ai-maestro-message-templates.md | Message templates and ACK workflow |
| message-response-decision-tree.md | Priority triage and response routing |
| design-document-protocol.md | Document UUID, schema, and lifecycle |
| proactive-handoff-protocol.md | Handoff format, triggers, and rules |
| task-completion-checklist.md | Task verification and completion checks |
| edge-case-protocols.md | Offline, unresponsive, and conflict handling |
| op-load-shared-template.md | Load shared template procedure |
| op-access-shared-constants.md | Access shared constants procedure |
| op-send-ai-maestro-message.md | Send AI Maestro message procedure |
| op-validate-with-schema.md | Validate with schema procedure |

## Examples

Example: Use ai-maestro-message-templates.md for message templates.

## Error Handling

| Error | Solution |
|-------|----------|
| Reference not found | Verify file exists in `references/` |
| Message delivery failed | Ensure AI Maestro API is reachable |
| Handoff rejected | See edge-case-protocols.md for resolution steps |

## Output

Protocol guidance, message templates, decision trees, and checklists as Markdown reference docs.

## Resources

- amaa-design-lifecycle - Skill lifecycle management
- amaa-requirements-analysis - Requirements documentation
- amaa-planning-patterns - Planning and design patterns
