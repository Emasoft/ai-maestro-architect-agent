---
name: dependency-analysis
description: Techniques for analyzing and managing module dependencies, including dependency direction rules, shared code strategies, circular dependency detection, and dependency injection patterns
version: 1.0.0
---

# Dependency Analysis and Management

## Table of Contents

- [Overview](#overview)
- [The Dependency Problem](#the-dependency-problem)
  - [What is a Dependency?](#what-is-a-dependency)
  - [Why Dependencies Matter](#why-dependencies-matter)
- [Dependency Direction Rules](#dependency-direction-rules)
  - [Rule 1: Stable Dependency Principle](#rule-1-stable-dependency-principle)
  - [Rule 2: Acyclic Dependency Principle](#rule-2-acyclic-dependency-principle)
  - [Rule 3: Dependency Inversion Principle](#rule-3-dependency-inversion-principle)
- [Visualizing Dependencies](#visualizing-dependencies)
  - [Dependency Graph](#dependency-graph)
  - [Tools for Dependency Analysis](#tools-for-dependency-analysis)
- [The Shared Code Problem](#the-shared-code-problem)
  - [Problem Statement](#problem-statement)
  - [Solution: Shared Module Guidelines](#solution-shared-module-guidelines)
  - [Shared Module Patterns](#shared-module-patterns)
- [Circular Dependency Detection and Resolution](#circular-dependency-detection-and-resolution)
  - [Detecting Circular Dependencies](#detecting-circular-dependencies)
  - [Resolution Strategies](#resolution-strategies)
- [Dependency Injection](#dependency-injection)
  - [What is Dependency Injection?](#what-is-dependency-injection)
  - [DI Benefits](#di-benefits)
  - [DI Patterns](#di-patterns)
  - [DI Containers](#di-containers)
- [Dependency Metrics](#dependency-metrics)
  - [Metrics to Track](#metrics-to-track)
  - [Measuring Coupling](#measuring-coupling)
- [Dependency Documentation](#dependency-documentation)
  - [Dependency Map](#dependency-map)
  - [Dependency Contract](#dependency-contract)
- [Anti-Patterns](#anti-patterns)
  - [Anti-Pattern 1: Tangled Dependencies](#anti-pattern-1-tangled-dependencies)
  - [Anti-Pattern 2: God Module](#anti-pattern-2-god-module)
  - [Anti-Pattern 3: Hidden Dependencies](#anti-pattern-3-hidden-dependencies)
  - [Anti-Pattern 4: Yo-Yo Problem](#anti-pattern-4-yo-yo-problem)
- [Summary](#summary)

## Overview

Module dependencies determine how modules interact and evolve. Proper dependency management is critical for maintaining modularity, testability, and independent evolution.

## The Dependency Problem

### What is a Dependency?

Module A depends on Module B when:
- A imports code from B
- A calls functions/methods in B
- A uses data structures defined in B
- A requires B to be present at runtime

**Example:**
```python
# OrderModule depends on CustomerModule
from customer_module import CustomerRepository

class OrderService:
    def __init__(self):
        self.customer_repo = CustomerRepository()  # Dependency!
```

### Why Dependencies Matter

| Issue | Cause | Impact |
|-------|-------|--------|
| Coupling | Too many dependencies | Changes ripple across modules |
| Testing | Concrete dependencies | Cannot test in isolation |
| Deployment | Tight dependencies | Must deploy modules together |
| Understanding | Complex dependency graph | Hard to understand system structure |
| Evolution | Circular dependencies | Cannot evolve modules independently |

## Dependency Direction Rules

### Rule 1: Stable Dependency Principle

**Modules should depend on modules more stable than themselves.**

Stability = Resistance to change

**Metrics:**
- **Afferent coupling (Ca):** Number of modules that depend on this module
- **Efferent coupling (Ce):** Number of modules this module depends on
- **Instability (I):** I = Ce / (Ca + Ce)
  - I = 0: Maximally stable (many dependents, no dependencies)
  - I = 1: Maximally unstable (no dependents, many dependencies)

**Example:**
```
UtilityModule (I=0.1, stable)
  ↑
  | depends on
  |
BusinessLogicModule (I=0.5, moderate)
  ↑
  | depends on
  |
UIModule (I=0.9, unstable)
```

**Why:** Unstable modules change frequently. If stable modules depend on unstable ones, changes ripple upward.

### Rule 2: Acyclic Dependency Principle

**The dependency graph must be a directed acyclic graph (DAG). No cycles allowed.**

**Bad (Circular Dependency):**
```
OrderModule → CustomerModule → OrderModule
(Order needs Customer, Customer needs Order)
```

**Good (Acyclic):**
```
OrderModule → CustomerModule
OrderModule → SharedTypesModule ← CustomerModule
(Both depend on shared types, no cycle)
```

### Rule 3: Dependency Inversion Principle

**High-level modules should not depend on low-level modules. Both should depend on abstractions.**

**Before (High-level depends on low-level):**
```
OrderService (high-level)
  ↓ depends on
PostgreSQLRepository (low-level)
```

**After (Both depend on abstraction):**
```
OrderService (high-level)
  ↓ depends on
RepositoryInterface (abstraction)
  ↑ implemented by
PostgreSQLRepository (low-level)
```

## Visualizing Dependencies

### Dependency Graph

Create a visual dependency graph to understand relationships:

```
Legend:
→ : depends on
--: associates with

Dependency Graph:

        WebAPI
          |
    ------+------
    |     |     |
    v     v     v
  Orders Users Products
    |           |
    v           v
 Payments    Inventory
    |           |
    +-----+-----+
          |
          v
      Database
```

### Tools for Dependency Analysis

| Language | Tools |
|----------|-------|
| Python | `pydeps`, `snakefood`, `pylint --generate-rcfile` |
| JavaScript | `madge`, `dependency-cruiser` |
| Java | `JDepend`, `Structure101` |
| C# | `NDepend` |
| Go | `go mod graph` |

**Example (Python):**
```bash
# Generate dependency graph
pydeps src/orders --show-deps --max-bacon=3

# Find circular dependencies
pydeps src/ --show-cycles
```

## The Shared Code Problem

### Problem Statement

When multiple modules need the same functionality, where should it live?

**Scenario:**
```
OrderModule needs validate_email()
CustomerModule needs validate_email()
```

**Options:**
1. Duplicate in both modules (bad: duplication)
2. OrderModule uses CustomerModule's version (bad: creates dependency)
3. Create SharedUtilitiesModule (good: dedicated module)

### Solution: Shared Module Guidelines

**When to Create Shared Module:**
- Code is used by 3+ modules
- Code is stable (changes infrequently)
- Code has no business logic (pure utilities)

**When NOT to Create Shared Module:**
- Code is used by only 1-2 modules → Keep local or duplicate
- Code changes frequently → Keep in owning module
- Code has business logic → Move to domain module

### Shared Module Patterns

#### Pattern 1: Utility Module

For generic utilities:

```python
# shared_utils module
def validate_email(email: str) -> bool:
    # Generic email validation
    pass

def format_currency(amount: Decimal) -> str:
    # Generic currency formatting
    pass
```

**Characteristics:**
- No business logic
- Pure functions
- Highly stable
- Many dependents

#### Pattern 2: Common Types Module

For shared data structures:

```python
# common_types module
@dataclass
class Address:
    street: str
    city: str
    postal_code: str
    country: str

@dataclass
class Money:
    amount: Decimal
    currency: str
```

**Characteristics:**
- Data structures only
- No behavior (or minimal)
- Used across modules
- Versioned carefully

#### Pattern 3: Integration Module

For external service clients:

```python
# payment_client module
class PaymentClient:
    def charge(amount: Money, payment_method: PaymentMethod) -> Result:
        # Calls external payment service
        pass
```

**Characteristics:**
- Encapsulates external service
- Multiple modules use same service
- Provides abstraction over third-party API

## Circular Dependency Detection and Resolution

### Detecting Circular Dependencies

**Manual Detection:**
1. Draw dependency graph
2. Follow arrows
3. If you return to starting node, cycle exists

**Automated Detection:**
```bash
# Python
pydeps src/ --show-cycles

# JavaScript
madge --circular src/

# Output:
Circular dependencies found:
orders → customers → orders
```

### Resolution Strategies

#### Strategy 1: Extract Shared Code

**Before:**
```
OrderModule → CustomerModule (to get customer data)
CustomerModule → OrderModule (to get order history)
```

**After:**
```
OrderModule → SharedTypes
CustomerModule → SharedTypes
(Both depend on shared types, no cycle)
```

#### Strategy 2: Dependency Inversion

**Before:**
```
OrderModule → CustomerModule
CustomerModule → OrderModule
```

**After:**
```
OrderModule → ICustomerService (interface)
CustomerModule implements ICustomerService
(OrderModule depends on interface, CustomerModule implements it)
```

#### Strategy 3: Event-Based Decoupling

**Before:**
```
OrderModule → CustomerModule (to notify of order)
CustomerModule → OrderModule (to check order status)
```

**After:**
```
OrderModule publishes OrderCreated event
CustomerModule subscribes to OrderCreated event
(No direct dependency, communicate via events)
```

#### Strategy 4: Introduce Mediator

**Before:**
```
ModuleA → ModuleB
ModuleB → ModuleA
```

**After:**
```
ModuleA → Mediator ← ModuleB
(Both depend on mediator, mediator coordinates)
```

## Dependency Injection

### What is Dependency Injection?

Instead of a module creating its dependencies, they are provided ("injected") from outside.

**Without DI (Hard-coded dependency):**
```python
class OrderService:
    def __init__(self):
        self.customer_repo = PostgreSQLCustomerRepository()  # Concrete dependency
```

**With DI (Injected dependency):**
```python
class OrderService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo  # Abstraction injected
```

### DI Benefits

| Benefit | Explanation |
|---------|-------------|
| Testability | Can inject mock dependencies for testing |
| Flexibility | Can swap implementations without changing code |
| Loose coupling | Modules depend on interfaces, not concrete classes |
| Configuration | Can configure dependencies externally |

### DI Patterns

#### Pattern 1: Constructor Injection

```python
class OrderService:
    def __init__(
        self,
        customer_repo: CustomerRepository,
        payment_service: PaymentService,
        email_service: EmailService
    ):
        self.customer_repo = customer_repo
        self.payment_service = payment_service
        self.email_service = email_service
```

**Pros:** Dependencies explicit, required at construction
**Cons:** Many dependencies = long constructor

#### Pattern 2: Property Injection

```python
class OrderService:
    customer_repo: CustomerRepository
    payment_service: PaymentService

    def set_customer_repo(self, repo: CustomerRepository):
        self.customer_repo = repo
```

**Pros:** Optional dependencies
**Cons:** Dependencies can be unset, less explicit

#### Pattern 3: Method Injection

```python
class OrderService:
    def create_order(
        self,
        customer_id: str,
        items: List[OrderItem],
        customer_repo: CustomerRepository  # Injected per method
    ):
        customer = customer_repo.get(customer_id)
        # ...
```

**Pros:** Dependencies scoped to method
**Cons:** Verbose, dependencies passed repeatedly

### DI Containers

DI containers automate dependency wiring:

```python
# Configure container
container = Container()
container.register(CustomerRepository, PostgreSQLCustomerRepository)
container.register(PaymentService, StripePaymentService)
container.register(OrderService)  # Dependencies auto-wired

# Resolve
order_service = container.resolve(OrderService)
# order_service.customer_repo is PostgreSQLCustomerRepository instance
# order_service.payment_service is StripePaymentService instance
```

## Dependency Metrics

### Metrics to Track

| Metric | Definition | Target |
|--------|------------|--------|
| Module coupling | Number of dependencies per module | < 7 |
| Circular dependencies | Number of dependency cycles | 0 |
| Dependency depth | Longest path in dependency graph | < 5 |
| Instability | Ce / (Ca + Ce) | Align with module role |
| Abstractness | Abstract types / Total types | High for stable modules |

### Measuring Coupling

```python
# Example: Calculate module coupling
def calculate_coupling(module):
    imports = count_imports(module)
    dependents = count_dependents(module)
    afferent = len(dependents)  # Ca
    efferent = len(imports)  # Ce
    instability = efferent / (afferent + efferent)  # I
    return {
        'afferent': afferent,
        'efferent': efferent,
        'instability': instability
    }
```

## Dependency Documentation

### Dependency Map

Document module dependencies explicitly:

```markdown
# OrderModule Dependencies

## Direct Dependencies
- CustomerModule: Get customer data (ICustomerRepository)
- PaymentModule: Process payments (IPaymentService)
- InventoryModule: Check stock (IInventoryService)

## Transitive Dependencies
- DatabaseModule (via CustomerModule)
- ConfigModule (via PaymentModule)

## Dependents (Modules that depend on us)
- WebAPIModule
- ReportingModule
```

### Dependency Contract

For each dependency, document the contract:

```markdown
# OrderModule depends on ICustomerRepository

## Why
Need to validate customer exists before creating order

## What
Interface: ICustomerRepository
Method: get_customer(customer_id: str) -> Optional[Customer]

## Stability
Customer module is highly stable (I=0.2)
Interface has not changed in 2 years

## Alternatives Considered
- Duplicate customer validation in OrderModule (rejected: duplication)
- Call CustomerModule's HTTP API (rejected: tight coupling)
- Use event sourcing (rejected: too complex)
```

## Anti-Patterns

### Anti-Pattern 1: Tangled Dependencies

**Problem:** Every module depends on every other module.

**Solution:** Apply layering, define dependency direction rules.

### Anti-Pattern 2: God Module

**Problem:** One module that every other module depends on.

**Solution:** Split god module into focused modules, apply SRP.

### Anti-Pattern 3: Hidden Dependencies

**Problem:** Module has dependencies not visible in its interface.

**Solution:** Make all dependencies explicit (constructor parameters, imports).

### Anti-Pattern 4: Yo-Yo Problem

**Problem:** Deep dependency chains force hopping through many modules.

**Solution:** Flatten dependency graph, introduce facades.

## Summary

**Key Principles:**
1. **Stable Dependency:** Depend on stable modules
2. **Acyclic Dependencies:** No circular dependencies
3. **Dependency Inversion:** Depend on abstractions

**Shared Code:**
- Create shared modules for utilities used by 3+ modules
- Keep shared modules stable and minimal
- Prefer duplication over wrong dependency

**Circular Dependencies:**
- Detect with tools (pydeps, madge)
- Resolve via extraction, inversion, events, or mediator

**Dependency Injection:**
- Inject dependencies (don't hard-code)
- Use constructor injection as default
- Consider DI containers for complex systems

**Metrics:**
- Track coupling, instability, depth
- Target: < 7 dependencies per module, 0 cycles

Good dependency management enables independent module evolution and maintains system modularity.
