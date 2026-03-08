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
| [ai-maestro-message-templates.md](references/ai-maestro-message-templates.md) | 1.1 Sending Acknowledgment When Receiving Design Request from AMCOS, 1.2 Requesting Clarification from AMCOS for Ambiguous Requirements, 1.3 Reporting Design Completion to AMCOS, 1.4 Notifying AMCOS That Handoff Document is Ready for AMOA, 1.5 Reporting Blocker That Prevents Design Progress, 1.6 Verifying ACK Receipt After Sending a Message, Example: Complete Message Send and Verify Workflow |
| [message-response-decision-tree.md](references/message-response-decision-tree.md) | Step 1: Priority Triage, Step 2: Message Type Routing, Step 3: Response Actions, Step 4: ACK Protocol |
| [design-document-protocol.md](references/design-document-protocol.md) | Document UUID Format (GUUID), Required Frontmatter Schema, Document Lifecycle, Validation Procedures, Search Procedures, GitHub Integration, Edge Cases and Error Handling, File Naming Convention, Cross-Plugin Protocol, Quick Reference |
| [proactive-handoff-protocol.md](references/proactive-handoff-protocol.md) | Standard Handoff Format, Automatic Handoff Triggers, Handoff Document Location, Mandatory Handoff Sections, Context, Progress, Current State, Blockers (if any), Next Steps, References, Proactive Writing Rules, Handoff Quality Checklist |
| [task-completion-checklist.md](references/task-completion-checklist.md) | Before Reporting Task Complete, Verification Loop, Common Traps (Architect-Specific), Completion Report Format, Pre-Completion Checklist for Architects, When to Escalate vs Complete |
| [edge-case-protocols.md](references/edge-case-protocols.md) | 1.0 AI Maestro Unavailable, Design Delivery (AI Maestro Offline), 2.0 GitHub Unavailable, 3.0 Remote Agent Unresponsive, 4.0 Requirements Ambiguity, 5.0 API Research Failures, 6.0 Design Conflicts |
| [op-load-shared-template.md](references/op-load-shared-template.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Template Placeholders, Error Handling, Related Operations |
| [op-access-shared-constants.md](references/op-access-shared-constants.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Available Constants, Error Handling, Related Operations |
| [op-send-ai-maestro-message.md](references/op-send-ai-maestro-message.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Message Types, Priority Levels, Error Handling, Related Operations |
| [op-validate-with-schema.md](references/op-validate-with-schema.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Required Fields by Schema, Error Handling, Related Operations |

## Examples

Use ai-maestro-message-templates.md for message templates.

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
