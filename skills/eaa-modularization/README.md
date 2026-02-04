# EAA Modularization Skill

## Purpose

This skill teaches the Emasoft Architect Agent (EAA) how to decompose systems into well-defined modules with clear boundaries, minimal coupling, and high cohesion.

## Contents

```
eaa-modularization/
  SKILL.md              # Main skill document with modularization principles
  README.md             # This file
  references/           # Detailed reference documents (to be populated)
```

## When to Use

Use this skill when:
- Designing a new system and need to plan module structure
- Breaking up a monolithic application
- Analyzing existing code for coupling/cohesion issues
- Designing APIs between system components
- Deciding where to place shared functionality
- Evaluating module boundaries for microservices migration

## Key Topics Covered

1. **SOLID Principles for Modules**
   - Single Responsibility Principle
   - Interface Segregation Principle
   - Dependency Inversion Principle

2. **Module Quality Metrics**
   - High Cohesion
   - Low Coupling

3. **Boundary Identification**
   - Domain concept mapping
   - Change vector analysis
   - Bounded context definition

4. **API Design**
   - Interface contracts
   - Versioning strategies
   - Error handling

5. **Dependency Management**
   - Dependency graphs
   - Circular dependency resolution
   - Shared code strategies

6. **Monolith Decomposition**
   - Strangler fig pattern
   - Incremental extraction

7. **Testing**
   - Module isolation testing
   - Contract testing
   - Mocking strategies

## Related Skills

- `eaa-planning-patterns` - Planning integration
- `eaa-design-lifecycle` - Design document management
- `eaa-requirements-analysis` - Requirements gathering
