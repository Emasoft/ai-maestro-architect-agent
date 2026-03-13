---
name: amaa-modularization
description: "Use when decomposing systems into modules with clear boundaries. Trigger with modularization or module boundary request."
context: fork
agent: ai-maestro-architect-agent-main-agent
user-invocable: false
---

# Modularization Skill

## Overview

Guides decomposition into modules with clear boundaries, minimal coupling, and high cohesion. Covers SOLID principles, boundary identification, API design, dependency management, and modularization validation.

## Prerequisites

- Project source code available for analysis

## Instructions

Use when starting new projects, refactoring monoliths, analyzing coupling, designing inter-module APIs, or planning microservices migration.

1. **Apply Principles** - Apply SOLID to guide decomposition
2. **Identify Boundaries** - Find natural module boundaries via domain mapping
3. **Design APIs** - Define interfaces and contracts between modules
4. **Manage Dependencies** - Graph dependencies, resolve circulars, extract shared code
5. **Validate** - Verify testability, coupling metrics, deployment independence

See [Detailed Procedures](./references/detailed-procedures.md) for the full phase checklist.

## Checklist

Copy this checklist and track your progress:

- [ ] Apply SOLID principles to guide decomposition
- [ ] Identify natural module boundaries via domain mapping
- [ ] Design interfaces and contracts between modules
- [ ] Graph dependencies and resolve circulars
- [ ] Extract shared code into dedicated modules
- [ ] Validate testability, coupling metrics, and deployment independence

## Reference Documents

| Document | Contents |
|----------|----------|
| [SOLID Principles](./references/solid-principles.md) | Overview, The Five SOLID Principles, Applying SOLID to Module Boundaries, Validation Checklist, Common Violations and Fixes, Summary |
| [Boundary Patterns](./references/boundary-patterns.md) | Overview, Core Principle, Step 1: Map Domain Concepts, Step 2: Identify Change Vectors, Step 3: Find Natural Seams, Step 4: Define Bounded Contexts, Step 5: Validate Boundaries |
| [API Design Guide](./references/api-design-guide.md) | Overview, Core API Design Principles, API Contract Templates, Versioning Strategy, Compatibility Rules, Data Transfer Objects (DTOs), Error Handling Contracts |
| [Detailed Procedures](./references/detailed-procedures.md) | What is a Module?, Why Modularization Matters, Detailed Phase Checklist, Examples, Troubleshooting, Next Steps |

## Examples

Example: `UserService (2000 LOC) → AuthModule, ProfileModule, RegistrationModule, PermissionsModule`

## Error Handling

| Problem | Solution |
|---------|----------|
| Module too large | Apply SRP, split by responsibility |
| Circular dependency | Extract shared interface or invert dependency |
| Cannot test in isolation | Apply DIP, inject dependencies |
| API breaks consumers | Implement semantic versioning |
| Shared code causes ripple changes | Reduce shared surface, consider duplication |

## Output

| Phase | Artifact |
|-------|----------|
| Principles | SOLID compliance assessment per module |
| Boundaries | Module boundary map with responsibilities |
| APIs | Interface definitions and contracts |
| Validation | Coupling/cohesion metrics and test strategy |

## Resources

See Reference Documents table above.
