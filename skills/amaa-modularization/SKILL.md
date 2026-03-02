---
name: eaa-modularization
description: Use when designing modular systems, breaking up monoliths, or defining module boundaries and APIs. Trigger with modularization requests, system decomposition, or coupling analysis.
version: 1.0.0
license: Apache-2.0
compatibility: Requires AI Maestro installed.
context: fork
agent: eaa-main
user-invocable: false
workflow-instruction: "Steps 7, 10"
procedure: "proc-create-design, proc-decompose-design"
triggers:
  - when decomposing a system into modules
  - when identifying module boundaries
  - when designing inter-module APIs
  - when breaking up monolithic code
  - when analyzing coupling and cohesion
  - when managing shared code between modules
---

# Modularization Skill

## Overview

This skill teaches architects how to decompose systems into well-defined modules with clear boundaries, minimal coupling, and high cohesion. Proper modularization is the foundation of maintainable, scalable, and testable software systems.

**What is a Module?**

A module is a self-contained unit of code that:
- Has a single, well-defined responsibility
- Exposes a clear public interface (API)
- Hides its internal implementation details
- Can be developed, tested, and deployed independently
- Has explicit dependencies on other modules

**Why Modularization Matters:**

| Benefit | Explanation |
|---------|-------------|
| Maintainability | Changes to one module do not ripple through the entire system |
| Testability | Modules can be tested in isolation with mocked dependencies |
| Scalability | Teams can work on different modules in parallel |
| Reusability | Well-designed modules can be reused across projects |
| Understandability | Smaller modules are easier to comprehend than monolithic code |

## Prerequisites

- Understanding of the system's functional requirements
- Access to existing codebase (if refactoring)
- Knowledge of domain concepts and bounded contexts
- Familiarity with dependency analysis tools

## Instructions

Use this skill when:
- Starting a new project and need to plan its structure
- Refactoring a monolithic application into modules
- Analyzing existing code for coupling problems
- Designing APIs between system components
- Deciding where to place shared functionality
- Evaluating module boundaries for a microservices migration

**Execute these phases in order:**

1. **Principle Application** - Apply SOLID principles to guide decomposition
2. **Boundary Identification** - Find natural module boundaries
3. **API Design** - Define interfaces between modules
4. **Dependency Management** - Manage module dependencies and shared code
5. **Validation** - Verify modularization quality

### Checklist

Copy this checklist and track your progress:

- [ ] **Phase 1: Apply Modularization Principles**
  - [ ] Review Single Responsibility Principle for each proposed module
  - [ ] Apply Interface Segregation to module APIs
  - [ ] Apply Dependency Inversion between modules
  - [ ] Evaluate cohesion within each module
  - [ ] Evaluate coupling between modules
- [ ] **Phase 2: Identify Module Boundaries**
  - [ ] Map domain concepts to potential modules
  - [ ] Identify change vectors (things that change together)
  - [ ] Find natural seams in the codebase
  - [ ] Define bounded contexts
  - [ ] Validate boundary decisions with stakeholders
- [ ] **Phase 3: Design Module APIs**
  - [ ] Define public interface for each module
  - [ ] Document API contracts
  - [ ] Design data transfer objects (DTOs)
  - [ ] Plan versioning strategy
  - [ ] Define error handling contracts
- [ ] **Phase 4: Manage Dependencies**
  - [ ] Create module dependency graph
  - [ ] Identify circular dependencies
  - [ ] Extract shared code to utility modules
  - [ ] Define dependency direction rules
  - [ ] Plan dependency injection strategy
- [ ] **Phase 5: Validate and Refine**
  - [ ] Verify modules can be tested independently
  - [ ] Check for hidden coupling
  - [ ] Validate deployment independence
  - [ ] Review with development team

## Output

| Phase | Output Artifact | Contents |
|-------|-----------------|----------|
| Principle Application | Principle analysis document | SOLID compliance assessment for each module |
| Boundary Identification | Module boundary map | Modules, responsibilities, bounded contexts |
| API Design | API specification | Interface definitions, contracts, DTOs |
| Dependency Management | Dependency graph | Module relationships, shared code strategy |
| Validation | Quality report | Coupling metrics, cohesion scores, test strategy |

## Core Modularization Principles

For detailed principles, see [references/solid-principles.md](references/solid-principles.md):
- 1. Single Responsibility Principle (SRP) - One reason to change
- 2. Interface Segregation Principle (ISP) - Small, focused interfaces
- 3. Dependency Inversion Principle (DIP) - Depend on abstractions
- 4. High Cohesion - Related elements together
- 5. Low Coupling - Minimal inter-module dependencies

## Module Boundary Identification

For detailed boundary identification, see [references/boundary-patterns.md](references/boundary-patterns.md):
- Step 1: Map Domain Concepts
- Step 2: Identify Change Vectors
- Step 3: Find Natural Seams
- Step 4: Define Bounded Contexts
- Step 5: Validate Boundaries

## API Design Between Modules

For detailed API design, see [references/api-design-guide.md](references/api-design-guide.md):
- API Design Principles (Minimal Surface, Versioning, Compatibility)
- API Contract Templates
- Versioning Strategy
- Error Handling Contracts

## Shared Code Management

For shared code strategies, see [references/dependency-analysis.md](references/dependency-analysis.md):
- The Shared Code Problem
- Shared Module Guidelines
- Dependency Direction Rules
- Circular Dependency Detection

## Breaking Up Monoliths

For monolith decomposition, see [references/strangler-pattern.md](references/strangler-pattern.md):
- The Strangler Fig Pattern
- Step-by-Step Monolith Decomposition
- Module Dependency Graphs
- Detecting Circular Dependencies

## Module Testing

For testing strategies, see [references/module-testing.md](references/module-testing.md):
- Testing Strategies by Scope
- Module Testing Pattern
- Mocking Module Dependencies
- Contract Testing

## Error Handling

| Problem | Cause | Solution |
|---------|-------|----------|
| Module too large | Multiple responsibilities | Apply SRP - split into focused modules |
| Circular dependency detected | Modules depend on each other | Extract common code or invert dependency |
| Cannot test module in isolation | Hidden dependencies | Apply DIP - inject dependencies |
| API breaks consumers | Missing versioning | Implement semantic versioning |
| Shared module causes ripple changes | Too much shared code | Reduce shared code surface, consider duplication |
| Unclear module boundaries | No bounded context analysis | Map domain concepts, identify change vectors |
| High coupling detected | Direct concrete dependencies | Introduce interfaces, reduce API surface |
| Low cohesion in module | Unrelated functionality | Move unrelated code to appropriate modules |

## Examples

### Example 1: E-Commerce Modularization

```
Domain Analysis:
- Products, Orders, Customers, Payments, Shipping

Module Breakdown:
1. ProductCatalog Module
   - Product CRUD
   - Category management
   - Search/filtering

2. OrderManagement Module
   - Order creation/cancellation
   - Order status tracking
   - Order history

3. CustomerModule
   - Customer profiles
   - Authentication
   - Address management

4. PaymentModule
   - Payment processing
   - Refunds
   - Payment methods

5. ShippingModule
   - Shipping rate calculation
   - Label generation
   - Tracking

6. InventoryModule
   - Stock levels
   - Reservations
   - Reorder alerts

Dependency Graph:
  WebAPI
    |
    +-> ProductCatalog
    +-> OrderManagement --> PaymentModule
    |                  |-> ShippingModule
    |                  +-> InventoryModule
    +-> CustomerModule
```

### Example 2: Breaking Up User Monolith

```
Before (Monolith):
UserService (2000 lines)
  - registerUser()
  - authenticateUser()
  - resetPassword()
  - updateProfile()
  - uploadAvatar()
  - sendVerificationEmail()
  - checkPermissions()
  - generateUserReport()

After (Modules):
1. AuthenticationModule
   - authenticateUser()
   - resetPassword()

2. UserProfileModule
   - updateProfile()
   - uploadAvatar()

3. RegistrationModule
   - registerUser()
   - sendVerificationEmail()

4. PermissionsModule
   - checkPermissions()

5. UserReportingModule
   - generateUserReport()
```

## Resources

| Resource | Use When |
|----------|----------|
| [SOLID Principles Reference](./references/solid-principles.md) | Applying design principles |
| [Boundary Patterns](./references/boundary-patterns.md) | Identifying module boundaries |
| [API Design Guide](./references/api-design-guide.md) | Designing module interfaces |
| [Dependency Analysis](./references/dependency-analysis.md) | Analyzing and visualizing dependencies |
| [Strangler Pattern](./references/strangler-pattern.md) | Breaking up monoliths gradually |
| [Module Testing Guide](./references/module-testing.md) | Testing modular systems |

## Summary

| Phase | Purpose | Key Output |
|-------|---------|------------|
| Principle Application | Apply SOLID to guide design | Principle compliance checklist |
| Boundary Identification | Find natural module boundaries | Module boundary map |
| API Design | Define module interfaces | API contracts |
| Dependency Management | Manage relationships | Dependency graph |
| Validation | Verify quality | Coupling/cohesion metrics |

**Key Principles:**

1. **Single Responsibility** - One reason to change per module
2. **Interface Segregation** - Small, focused interfaces
3. **Dependency Inversion** - Depend on abstractions
4. **High Cohesion** - Related elements together
5. **Low Coupling** - Minimal inter-module dependencies

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Circular dependency detected | Modules depend on each other bidirectionally | Use `tldr arch` to visualize layers, extract shared interface to utility module, apply Dependency Inversion Principle |
| Module boundaries unclear | Insufficient domain analysis or overlapping responsibilities | Review `boundary-patterns.md`, map domain concepts again, identify change vectors, redefine bounded contexts |
| Cannot test module in isolation | Hidden dependencies or tight coupling | Apply Dependency Injection, create interface abstractions, use mocking framework for dependencies |
| API breaking consumer modules | Missing versioning strategy or backward compatibility | Implement semantic versioning, add deprecation warnings before removal, maintain parallel versions during transition |
| High coupling metrics | Direct concrete dependencies between modules | Introduce interface abstractions, reduce API surface area, review `api-design-guide.md` for minimal surface pattern |
| Module too large (>500 LOC) | Multiple responsibilities violating SRP | Split by responsibility using `solid-principles.md`, create sub-modules with focused interfaces |
| Shared module causes ripple changes | Over-shared code between modules | Review `dependency-analysis.md`, reduce shared surface, consider strategic duplication over coupling |
| Deployment dependencies blocking independence | Runtime coupling or database sharing | Plan strangler pattern migration using `strangler-pattern.md`, introduce service boundaries, separate databases |

## Next Steps

1. Read core principles section thoroughly
2. Inventory your current system or planned system
3. Map domain concepts to candidate modules
4. Identify change vectors and bounded contexts
5. Validate boundaries with stakeholders
6. Design APIs between modules
7. Create dependency graph
8. Plan extraction sequence (for monoliths)
9. Implement module tests
10. Iterate and refine boundaries as needed

---

**Final Note:** Perfect modularization is achieved iteratively. Start with clear principles, make reasonable boundary decisions, and refine as you learn more about the system's actual behavior and change patterns.
