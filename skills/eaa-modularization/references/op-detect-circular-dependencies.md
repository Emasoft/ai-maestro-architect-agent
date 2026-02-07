---
operation: detect-circular-dependencies
procedure: proc-decompose-design
workflow-instruction: Step 10 - Design Decomposition
parent-skill: eaa-modularization
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Detect Circular Dependencies

## When to Use

Use this operation when:
- Analyzing existing codebase for architectural issues
- Validating module design before implementation
- Troubleshooting build or runtime dependency issues
- Preparing for monolith decomposition
- Reviewing architecture for coupling problems

## Prerequisites

- Access to codebase source files
- Understanding of module structure
- Tools for dependency analysis (tldr, imports analysis)

## Procedure

### Step 1: Build Import/Dependency Graph

Analyze all imports and dependencies in the codebase.

```bash
# Using tldr to analyze architecture layers
tldr arch src/

# Analyze imports for a specific file
tldr imports src/modules/order/service.ts

# Find all files that import a module
tldr importers "OrderService" src/
```

**Manual Analysis:**
```markdown
## Import Analysis

### OrderModule imports:
- PaymentModule
- InventoryModule
- CustomerModule
- Shared/Types

### PaymentModule imports:
- OrderModule        ← POTENTIAL CYCLE
- Shared/Types

### InventoryModule imports:
- ProductModule
- Shared/Types
```

### Step 2: Identify Cycles

Look for import chains that form loops.

**Cycle Detection Algorithm:**
1. Start from each module
2. Follow its dependencies
3. Track visited modules
4. If you visit a module twice, you found a cycle

**Common Cycle Patterns:**

| Pattern | Description | Example |
|---------|-------------|---------|
| Direct Cycle | A → B → A | Order → Payment → Order |
| Indirect Cycle | A → B → C → A | Order → Inventory → Shipping → Order |
| Self Reference | A → A | Module importing itself (rare) |

```markdown
## Detected Cycles

### Cycle 1: Order ↔ Payment
```
OrderModule
    ↓ imports PaymentService for payment processing
PaymentModule
    ↓ imports OrderService for order lookups
OrderModule (CYCLE)
```

### Cycle 2: Inventory → Shipping → Inventory
```
InventoryModule
    ↓ imports ShippingCalculator for weight-based stock
ShippingModule
    ↓ imports InventoryChecker for availability
InventoryModule (CYCLE)
```
```

### Step 3: Classify Cycle Severity

Not all cycles are equally problematic.

| Severity | Description | Action |
|----------|-------------|--------|
| Critical | Prevents compilation/startup | Must fix immediately |
| High | Causes tight coupling, testing issues | Fix in current sprint |
| Medium | Code organization problem | Plan to fix |
| Low | Minor coupling, isolated impact | Document and monitor |

**Assessment Criteria:**
- Does the cycle cross bounded contexts? (Critical)
- Does the cycle prevent testing? (High)
- Does the cycle cause ripple effects on change? (Medium)
- Is the cycle contained within a logical unit? (Low)

### Step 4: Determine Root Cause

Understand why the cycle exists.

**Common Root Causes:**

| Cause | Pattern | Solution |
|-------|---------|----------|
| Feature Envy | Module A uses too much of Module B | Move behavior to appropriate module |
| Shared Mutant | Both modules modify shared state | Extract shared state to third module |
| Callback Hell | A calls B which calls back to A | Use events or extract interface |
| Bidirectional Lookup | Both modules need to query each other | Extract query interface |
| Layering Violation | Lower layer depends on upper layer | Apply Dependency Inversion |

### Step 5: Plan Resolution

Choose appropriate resolution strategy.

**Resolution Strategies:**

**Strategy 1: Extract Interface**
```
Before:
  OrderModule → PaymentModule → OrderModule

After:
  OrderModule → IPaymentProcessor (interface)
  PaymentModule implements IPaymentProcessor
  PaymentModule → IOrderProvider (interface)
  OrderModule implements IOrderProvider
```

**Strategy 2: Extract Shared Module**
```
Before:
  ModuleA → ModuleB → ModuleA (sharing data)

After:
  ModuleA → SharedDataModule
  ModuleB → SharedDataModule
```

**Strategy 3: Use Events**
```
Before:
  Order creates payment → Payment updates order (cycle)

After:
  Order creates payment → Payment emits PaymentCompleted event
  Order listens to PaymentCompleted event (no direct dependency)
```

**Strategy 4: Merge Modules**
```
Before:
  TightlyCoupledModuleA ↔ TightlyCoupledModuleB

After:
  MergedModule (if they truly belong together)
```

## Checklist

Copy this checklist and track your progress:

- [ ] **Build Dependency Graph**
  - [ ] Analyze all module imports
  - [ ] Create visual dependency graph
  - [ ] Document all dependencies
- [ ] **Detect Cycles**
  - [ ] Run cycle detection on graph
  - [ ] List all detected cycles
  - [ ] Trace each cycle path
- [ ] **Classify Severity**
  - [ ] Rate each cycle (Critical/High/Medium/Low)
  - [ ] Prioritize by severity
  - [ ] Document impact of each cycle
- [ ] **Determine Root Cause**
  - [ ] Analyze why each cycle exists
  - [ ] Identify the root cause pattern
  - [ ] Document findings
- [ ] **Plan Resolution**
  - [ ] Choose strategy for each cycle
  - [ ] Document proposed changes
  - [ ] Create implementation tasks

## Examples

### Example: Detecting and Resolving Order-Payment Cycle

```markdown
# Cycle Analysis: Order ↔ Payment

## Detection

**Import Analysis:**
```
// order/service.ts
import { PaymentService } from '../payment/service';
// Uses: processPayment(orderId, amount)

// payment/service.ts
import { OrderService } from '../order/service';
// Uses: getOrderTotal(orderId), updateOrderPaymentStatus(orderId)
```

**Cycle Path:**
OrderModule → PaymentModule → OrderModule

## Severity: HIGH
- Prevents independent testing
- Changes to Order affect Payment and vice versa
- Cannot deploy modules independently

## Root Cause: Bidirectional Data Access
- Order needs to initiate payment
- Payment needs to read order total and update order status

## Resolution: Extract Interfaces + Events

**Step 1: Extract IOrderProvider interface**
```typescript
// shared/interfaces/IOrderProvider.ts
interface IOrderProvider {
  getOrderTotal(orderId: string): Promise<number>;
}
```

**Step 2: Order implements IOrderProvider**
```typescript
// order/service.ts
class OrderService implements IOrderProvider {
  async getOrderTotal(orderId: string): Promise<number> { ... }
}
```

**Step 3: Payment depends on interface, not module**
```typescript
// payment/service.ts
class PaymentService {
  constructor(private orderProvider: IOrderProvider) {}

  async processPayment(orderId: string) {
    const total = await this.orderProvider.getOrderTotal(orderId);
    // process payment
    // emit event instead of calling back to Order
    this.eventBus.emit('PaymentCompleted', { orderId, status: 'success' });
  }
}
```

**Step 4: Order listens to events**
```typescript
// order/service.ts
class OrderService {
  constructor(private eventBus: IEventBus) {
    this.eventBus.on('PaymentCompleted', this.handlePaymentCompleted);
  }

  private handlePaymentCompleted = async (event: PaymentEvent) => {
    await this.updateOrderPaymentStatus(event.orderId, event.status);
  }
}
```

## After Resolution

```
OrderModule → IOrderProvider (interface)
           → EventBus (infrastructure)

PaymentModule → IOrderProvider (interface)
             → EventBus (infrastructure)

No direct dependency between Order and Payment!
```
```

### Example: Cycle Detection Report

```markdown
# Circular Dependency Report

## Summary
- Total modules analyzed: 12
- Cycles detected: 3
- Critical: 1
- High: 1
- Medium: 1

## Cycle Details

### Cycle 1 (Critical)
**Path:** Auth → User → Auth
**Impact:** Prevents service startup
**Resolution:** Extract IUserProvider interface

### Cycle 2 (High)
**Path:** Order → Payment → Order
**Impact:** Testing impossible
**Resolution:** Use events for status updates

### Cycle 3 (Medium)
**Path:** Inventory → Product → Catalog → Inventory
**Impact:** Complex change propagation
**Resolution:** Extract shared ProductInfo module

## Recommended Action Order
1. Fix Auth ↔ User immediately (blocking deployment)
2. Fix Order ↔ Payment this sprint
3. Schedule Inventory cycle for next sprint
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Cycle not detected | Indirect/dynamic imports | Analyze runtime dependencies |
| Too many cycles | Monolithic design | Prioritize, fix most critical first |
| Resolution breaks functionality | Insufficient analysis | Test thoroughly, use feature flags |
| New cycles introduced | Resolution created new dependency | Review full graph after changes |
| Can't determine root cause | Complex interactions | Diagram data and control flow |

## Related Operations

- [op-manage-module-dependencies.md](op-manage-module-dependencies.md) - Overall dependency management
- [op-identify-module-boundaries.md](op-identify-module-boundaries.md) - May need to redefine boundaries
- [op-decompose-monolith.md](op-decompose-monolith.md) - Cycles block decomposition
