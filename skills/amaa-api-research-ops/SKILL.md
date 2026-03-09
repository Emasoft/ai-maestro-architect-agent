---
name: amaa-api-research-ops
description: "Use when needing API research scenarios or collaboration patterns. Trigger with API research ops request."
context: fork
user-invocable: false
agent: amaa-api-researcher
---

# API Researcher Skill (Operations)

## Overview

Scenarios for researching REST, GraphQL, Python, and cloud APIs. Includes collaboration patterns with orchestrator and other agents, plus quick reference for workflows and communication formats.

## Prerequisites

- Completion of core API research skill setup

## Instructions

1. Select the appropriate research scenario for the API type
2. Follow the step-by-step approach for that scenario
3. Use collaboration patterns for orchestrator communication
4. Consult quick reference for output files and formats

## Checklist

Copy this checklist and track your progress:

- [ ] Identify API type (REST, GraphQL, Python library, cloud service)
- [ ] Follow scenario-specific research steps
- [ ] Use correct communication format for status updates
- [ ] Complete handoff protocol when research is done

## Reference Documents

| Document | Content |
|----------|---------|
| [research-scenarios.md](references/research-scenarios.md) | Scenario 1: Research REST API, Scenario 2: Research Python Library, Scenario 3: Research Cloud Service API, Scenario 4: Research GraphQL API, Types, Queries, Mutations |
| [collaboration-patterns.md](references/collaboration-patterns.md) | Integration with Orchestrator, Handling Blockers, Handoff Protocol, Collaboration with Other Agents, Best Practices |
| [quick-reference.md](references/quick-reference.md) | Research Output Files, Research Workflow, Communication Formats, Extended Examples |

## Examples

Example: `Research REST API - WebSearch for docs, WebFetch API reference, document endpoints, identify auth method, check rate limits, create integration guide`

## Error Handling

| Issue | Fix |
|-------|-----|
| Scenario mismatch | Re-evaluate API type and switch scenario |
| Orchestrator unresponsive | Use [BLOCKED] format and wait |

## Output

| Type | Description |
|------|-------------|
| Scenario-guided research | Structured research following API-type-specific steps |
| Status reports | Formatted communication using standard patterns |

## Resources

See Reference Documents table above.
