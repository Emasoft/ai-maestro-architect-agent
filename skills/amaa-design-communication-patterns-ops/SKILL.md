---
name: amaa-design-communication-patterns-ops
description: "Use when handling edge cases or shared operations in architect communication. Trigger with communication ops request. Loaded by ai-maestro-architect-agent-main-agent"
context: fork
user-invocable: false
agent: ai-maestro-architect-agent-main-agent
---

# Design Communication Patterns (Operations)

## Overview

Operational procedures and edge case handling for architect inter-agent communication. Covers failure protocols, shared templates, constants, messaging, and schema validation.

## Prerequisites

- AI Maestro running and API accessible

## Instructions

1. Identify the operational procedure or edge case scenario
2. Consult the appropriate reference document
3. Follow the protocol steps as documented
4. Report outcome to orchestrator

## Checklist

Copy this checklist and track your progress:

- [ ] Identify needed operation or edge case
- [ ] Consult reference document
- [ ] Execute protocol steps

## Reference Documents

| Document | Content |
|----------|---------|
| [edge-case-protocols.md](references/edge-case-protocols.md) | AI Maestro Unavailable, GitHub Unavailable, Remote Agent Unresponsive, Requirements Ambiguity, API Research Failures, Design Conflicts, Planning Validation Failures |
| [op-load-shared-template.md](references/op-load-shared-template.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Template Placeholders, Error Handling |
| [op-access-shared-constants.md](references/op-access-shared-constants.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Available Constants, Error Handling |
| [op-send-ai-maestro-message.md](references/op-send-ai-maestro-message.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Message Types, Error Handling |
| [op-validate-with-schema.md](references/op-validate-with-schema.md) | When to Use, Prerequisites, Procedure, Checklist, Examples, Required Fields by Schema, Error Handling |

## Examples

Example: `Use edge-case-protocols.md when AI Maestro is offline to queue messages locally`

## Error Handling

| Issue | Fix |
|-------|-----|
| Reference not found | Verify file exists in `references/` |
| AI Maestro offline | Follow edge-case-protocols.md offline queue |

## Output

| Type | Description |
|------|-------------|
| Operational guidance | Step-by-step procedures for edge cases and shared operations |

## Resources

See Reference Documents table above.
