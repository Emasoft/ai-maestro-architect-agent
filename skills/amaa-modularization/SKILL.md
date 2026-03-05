---
name: amaa-modularization
description: "Use when decomposing systems into modules with clear boundaries. Trigger with modularization or module boundary request."
context: fork
agent: amaa-modularizer-expert
user-invocable: false
---

# Modularization Skill

## Overview

Guides architects in decomposing systems into well-defined modules with clear boundaries, minimal coupling, and high cohesion. Covers SOLID principle application, boundary identification, API design between modules, dependency management, and validation of modularization quality.

## Prerequisites

- Understanding of the system's functional requirements
- Access to existing codebase (if refactoring)
- Knowledge of domain concepts and bounded contexts

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
| [SOLID Principles](./references/solid-principles.md) | SRP, ISP, DIP application guidance (Overview, The Five SOLID Principles, Single Responsibility Principle, Open/Closed Principle, Liskov Substitution Principle) |
| [Boundary Patterns](./references/boundary-patterns.md) | Domain mapping, change vectors, bounded contexts (Overview, Core Principle, Map Domain Concepts, Domain-Driven Design Approach, Entity Relationship Analysis) |
| [API Design Guide](./references/api-design-guide.md) | Interface design, contracts, versioning (Overview, Core API Design Principles, Minimal Surface Area, Stable Contracts, Clear Semantics) |
| [Dependency Analysis](./references/dependency-analysis.md) | Dependency graphs, shared code strategies (Overview, The Dependency Problem, What is a Dependency, Why Dependencies Matter, Dependency Direction Rules) |
| [Strangler Pattern](./references/strangler-pattern.md) | Monolith decomposition approach (Overview, Why Strangler Pattern, The Big Rewrite Problem, Strangler Pattern Benefits, The Strangler Fig Pattern) |
| [Module Testing](./references/module-testing.md) | Testing strategies for modular systems (Overview, Testing Pyramid for Modular Systems, Unit Testing Modules, Unit Test Definition, Unit Test Example) |
| [Detailed Procedures](./references/detailed-procedures.md) | Full checklist, examples, troubleshooting (What is a Module?, Why Modularization Matters, Detailed Phase Checklist) |

## Examples

```
Before: UserService (2000 LOC monolith)
After:  AuthenticationModule, UserProfileModule,
        RegistrationModule, PermissionsModule,
        UserReportingModule
```

See [Detailed Procedures](./references/detailed-procedures.md) for full examples (What is a Module?, Why Modularization Matters, Detailed Phase Checklist).

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

- [SOLID Principles Reference](./references/solid-principles.md) (Overview, The Five SOLID Principles, Single Responsibility Principle)
- [Boundary Patterns](./references/boundary-patterns.md) (Overview, Core Principle, Map Domain Concepts)
- [Strangler Pattern](./references/strangler-pattern.md) (Overview, Why Strangler Pattern, The Strangler Fig Pattern)
- [Module Testing Guide](./references/module-testing.md) (Overview, Testing Pyramid, Unit Testing Modules)
