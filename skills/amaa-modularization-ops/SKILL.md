---
name: amaa-modularization-ops
description: "Use when analyzing dependencies, planning migration, or testing modules. Trigger with modularization ops request. Loaded by ai-maestro-architect-agent-main-agent"
context: fork
user-invocable: false
agent: ai-maestro-architect-agent-main-agent
---

# Modularization Operations

## Overview

Covers dependency management, monolith decomposition via the Strangler Fig pattern, and testing strategies for modular systems.

## Prerequisites

- Modular architecture defined (see amaa-modularization core skill)

## Instructions

1. **Analyze Dependencies** - Graph module dependencies, detect circulars, apply injection
2. **Plan Migration** - Use Strangler pattern for incremental monolith decomposition
3. **Design Tests** - Build testing pyramid with unit, contract, and integration tests
4. **Validate** - Verify isolation, coupling metrics, and deployment independence

## Checklist

Copy this checklist and track your progress:

- [ ] Graph all module dependencies and identify direction violations
- [ ] Detect and resolve circular dependencies
- [ ] Plan strangler fig migration steps for monolith features
- [ ] Implement unit tests per module with proper mocking
- [ ] Add contract tests between module boundaries
- [ ] Run integration tests for cross-module flows

## Reference Documents

| Document | Contents |
|----------|----------|
| [dependency-analysis.md](references/dependency-analysis.md) | Overview, The Dependency Problem, Dependency Direction Rules, Visualizing Dependencies, The Shared Code Problem, Circular Dependency Detection and Resolution, Dependency Injection |
| [strangler-pattern.md](references/strangler-pattern.md) | Overview, Why Strangler Pattern?, The Strangler Fig Pattern, Step-by-Step Monolith Decomposition, Extraction Candidate: [Feature Name], Dealing with Dependencies, Example: Extracting Authentication |
| [module-testing.md](references/module-testing.md) | Overview, Testing Pyramid for Modular Systems, Unit Testing Modules, Mocking Module Dependencies, Contract Testing, Integration Testing, Test Doubles Taxonomy |

## Examples

Example: `Resolve circular dependency between OrderModule and InventoryModule by extracting shared StockInterface`

## Error Handling

| Problem | Solution |
|---------|----------|
| Circular dependency | Extract shared interface or invert dependency |
| Cannot test in isolation | Apply DIP, inject dependencies |
| Shared code causes ripple changes | Reduce shared surface, consider duplication |

## Output

| Phase | Artifact |
|-------|----------|
| Dependencies | Dependency graph with direction analysis |
| Migration | Strangler pattern extraction plan |
| Testing | Test strategy with coverage targets |

## Resources

See Reference Documents table above.
