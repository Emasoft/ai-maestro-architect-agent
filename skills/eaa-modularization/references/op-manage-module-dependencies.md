---
operation: manage-module-dependencies
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-modularization
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Manage Module Dependencies

## When to Use

Use this operation when:
- Analyzing dependencies between modules
- Detecting and resolving circular dependencies
- Extracting shared code to utility modules
- Defining dependency direction rules
- Planning dependency injection strategy
- Visualizing module relationships

## Prerequisites

- Module boundaries are defined
- Module interfaces are designed
- Understanding of data and control flow between modules
- Access to codebase for analysis (if existing system)

## Procedure

### Step 1: Create Module Dependency Graph

Map all dependencies between modules.

```bash
# Use tldr to analyze architecture
tldr arch src/

# Or manually document dependencies
```

**Dependency Graph Format:**
```markdown
## Module Dependency Graph

```
                    ┌─────────────────┐
                    │   API Gateway   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  AuthModule    │  │  OrderModule   │  │ CatalogModule  │
└────────┬───────┘  └───────┬────────┘  └────────────────┘
         │                  │                    │
         ▼                  ▼                    │
┌────────────────┐  ┌────────────────┐          │
│  UserModule    │  │ PaymentModule  │          │
└────────────────┘  └───────┬────────┘          │
                            │                    │
                            ▼                    ▼
                    ┌────────────────┐  ┌────────────────┐
                    │ External: Stripe│ │  Shared: Utils │
                    └────────────────┘  └────────────────┘
```

**Dependency Table:**
| Module | Depends On | Type |
|--------|------------|------|
| API Gateway | Auth, Order, Catalog | Control |
| AuthModule | UserModule | Data |
| OrderModule | PaymentModule, CatalogModule | Data |
| PaymentModule | External Stripe | External |
```

### Step 2: Identify Circular Dependencies

Check for modules that depend on each other.

**Detection Methods:**
```bash
# Using tldr
tldr arch src/ | grep -i circular

# Manual check: if A depends on B and B depends on A = circular
```

**Circular Dependency Example:**
```
OrderModule → InventoryModule → OrderModule
    ↑__________________________________|

Problem: Order needs inventory check, Inventory needs order info to update
```

**Resolution Strategies:**
| Strategy | When to Use |
|----------|-------------|
| Extract Interface | Both depend on abstraction instead of each other |
| Merge Modules | If truly coupled, make one module |
| Event-Based | Use async events instead of direct calls |
| Dependency Inversion | Introduce interface at boundary |

### Step 3: Extract Shared Code to Utility Modules

Identify code used by multiple modules.

**Shared Code Categories:**
| Category | Example | Module Name |
|----------|---------|-------------|
| Types/DTOs | Common data structures | SharedTypes |
| Utilities | Date formatting, validation | Utils |
| Infrastructure | Logging, config | Infrastructure |
| Constants | Error codes, status values | Constants |

**Rules for Shared Modules:**
1. Shared modules have NO business logic
2. Shared modules depend on NOTHING (except external libs)
3. Shared modules are stable and rarely change
4. Keep shared modules minimal

```markdown
## Shared Module Structure

```
shared/
├── types/           # Common interfaces and types
│   ├── user.ts
│   ├── order.ts
│   └── index.ts
├── utils/           # Pure utility functions
│   ├── date.ts
│   ├── validation.ts
│   └── index.ts
├── constants/       # Application constants
│   ├── errors.ts
│   └── status.ts
└── index.ts
```

**Rule:** If shared code grows business logic, it belongs in a business module.
```

### Step 4: Define Dependency Direction Rules

Establish rules for allowed dependencies.

**Layered Dependency Rules:**
```
┌─────────────────────────────────────────────┐
│              Presentation Layer              │  ← Can depend on Application
├─────────────────────────────────────────────┤
│              Application Layer               │  ← Can depend on Domain
├─────────────────────────────────────────────┤
│                Domain Layer                  │  ← Can depend on nothing
├─────────────────────────────────────────────┤
│            Infrastructure Layer              │  ← Can depend on Domain
└─────────────────────────────────────────────┘
```

**Module Dependency Rules:**
| Rule | Description |
|------|-------------|
| No Upward Dependencies | Lower layers cannot depend on upper |
| No Circular Dependencies | A→B→A is forbidden |
| Depend on Abstractions | Depend on interfaces, not implementations |
| Stable Dependencies | Depend on modules that change less |

### Step 5: Plan Dependency Injection Strategy

Define how dependencies will be provided to modules.

**DI Patterns:**
| Pattern | Description | Use When |
|---------|-------------|----------|
| Constructor Injection | Pass dependencies in constructor | Always preferred |
| Property Injection | Set via property | Optional dependencies |
| Method Injection | Pass per-method call | Varying dependencies |
| Service Locator | Lookup from registry | Last resort |

**DI Container Setup:**
```typescript
// Container configuration
container.register('IUserRepository', PostgresUserRepository);
container.register('IAuthService', AuthService);
container.register('ITokenGenerator', JwtTokenGenerator);

// Usage
const authService = container.resolve<IAuthService>('IAuthService');
```

## Checklist

Copy this checklist and track your progress:

- [ ] **Dependency Graph**
  - [ ] List all modules
  - [ ] Map dependencies between modules
  - [ ] Create visual dependency graph
  - [ ] Create dependency table
- [ ] **Circular Dependency Check**
  - [ ] Identify all cycles in dependency graph
  - [ ] Choose resolution strategy for each cycle
  - [ ] Plan refactoring to break cycles
- [ ] **Shared Code Extraction**
  - [ ] Identify code used by multiple modules
  - [ ] Categorize shared code (types, utils, infra)
  - [ ] Create shared modules
  - [ ] Ensure shared modules have no business logic
- [ ] **Dependency Direction Rules**
  - [ ] Define layer hierarchy
  - [ ] Document allowed dependencies per layer
  - [ ] Add linting/tooling to enforce rules
- [ ] **Dependency Injection**
  - [ ] Choose DI pattern (constructor preferred)
  - [ ] Define interface for each dependency
  - [ ] Configure DI container
  - [ ] Test with mock implementations

## Examples

### Example: Breaking Circular Dependency

**Problem:**
```
OrderModule depends on InventoryModule
InventoryModule depends on OrderModule

Order needs: checkAvailability(productId)
Inventory needs: getOrdersForProduct(productId) for forecasting
```

**Solution: Extract Interface**
```typescript
// shared/interfaces/IInventoryChecker.ts
interface IInventoryChecker {
  checkAvailability(productId: string, quantity: number): Promise<boolean>;
}

// shared/interfaces/IOrderProvider.ts
interface IOrderProvider {
  getOrdersForProduct(productId: string): Promise<Order[]>;
}

// Now both modules depend on interfaces, not each other
// OrderModule implements IOrderProvider
// InventoryModule implements IInventoryChecker
// Each can be injected with the other's interface
```

**After:**
```
OrderModule → IInventoryChecker (interface)
InventoryModule → IOrderProvider (interface)

No circular dependency - both depend on abstractions
```

### Example: Dependency Graph Documentation

```markdown
# Module Dependencies: E-Commerce Platform

## Dependency Graph

```
Level 0 (Entry Points):
  └── WebAPI, AdminAPI, WebhookHandler

Level 1 (Application Services):
  └── OrderService, ProductService, CustomerService

Level 2 (Domain Services):
  └── PricingService, InventoryService, ShippingCalculator

Level 3 (Infrastructure):
  └── Database, Cache, MessageQueue, ExternalAPIs

Level 4 (Shared):
  └── Types, Utils, Constants
```

## Dependency Rules

1. Level N can only depend on Level N+1 or lower
2. No dependencies within same level (horizontal)
3. Level 4 (Shared) can depend on nothing
4. External dependencies isolated in Level 3

## Allowed Dependencies Matrix

| Module | Can Depend On |
|--------|---------------|
| WebAPI | OrderService, ProductService, CustomerService, Shared |
| OrderService | PricingService, InventoryService, ShippingCalculator, Database, Shared |
| PricingService | Database, Cache, Shared |
| Database | Shared |
| Shared | (nothing) |
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Circular dependency detected | Modules depend on each other | Extract interface, use events, or merge |
| Shared module has business logic | Over-extraction to shared | Move logic to appropriate business module |
| Too many dependencies | Module doing too much | Split module, apply SRP |
| Upward dependency | Lower layer depends on upper | Invert dependency using interface |
| Hard to test | Dependencies not injectable | Apply DIP, use constructor injection |

## Related Operations

- [op-identify-module-boundaries.md](op-identify-module-boundaries.md) - Define modules first
- [op-design-module-apis.md](op-design-module-apis.md) - Design interfaces for dependencies
- [op-apply-solid-principles.md](op-apply-solid-principles.md) - Apply DIP
- [op-detect-circular-dependencies.md](op-detect-circular-dependencies.md) - Detailed cycle detection
