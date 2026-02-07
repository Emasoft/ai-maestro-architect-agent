---
operation: apply-solid-principles
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-modularization
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Apply SOLID Principles to Modularization

## When to Use

Use this operation when:
- Designing module boundaries for a new system
- Evaluating existing module design for quality
- Refactoring monolithic code into modules
- Reviewing module APIs for design issues
- Training team members on module design principles

## Prerequisites

- Understanding of the system's functional requirements
- List of candidate modules or existing module structure
- Knowledge of module responsibilities
- Access to codebase (if analyzing existing code)

## Procedure

### Step 1: Apply Single Responsibility Principle (SRP)

**Principle:** A module should have one, and only one, reason to change.

**Checklist for each module:**
- [ ] Can you describe the module's purpose in one sentence?
- [ ] Does the module change for only one business reason?
- [ ] Are all functions in the module related to that single purpose?

**Evaluation:**
```markdown
## SRP Assessment: AuthModule

**Purpose:** Handle user authentication

**Responsibilities:**
- [x] Validate credentials (related)
- [x] Issue tokens (related)
- [x] Refresh tokens (related)
- [ ] Send password reset emails (VIOLATION - notification concern)
- [ ] Log audit events (VIOLATION - observability concern)

**Action:** Extract email and audit to separate modules
```

**If SRP violated:** Split the module by responsibility.

### Step 2: Apply Interface Segregation Principle (ISP)

**Principle:** Clients should not be forced to depend on interfaces they don't use.

**Checklist for each module interface:**
- [ ] Do all consumers use all methods in the interface?
- [ ] Is the interface focused on a specific use case?
- [ ] Are there groups of methods used together?

**Evaluation:**
```markdown
## ISP Assessment: UserService Interface

**Current Interface:**
- createUser()      - Used by: Registration, Admin
- updateUser()      - Used by: Profile, Admin
- deleteUser()      - Used by: Admin only
- getUser()         - Used by: All
- getUserStats()    - Used by: Admin, Analytics
- exportUserData()  - Used by: Compliance only

**Problem:** Registration module must import interface with delete/export methods it never uses.

**Action:** Split into focused interfaces:
- IUserReader: getUser()
- IUserWriter: createUser(), updateUser(), deleteUser()
- IUserAnalytics: getUserStats()
- IUserCompliance: exportUserData()
```

### Step 3: Apply Dependency Inversion Principle (DIP)

**Principle:** High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Checklist for dependencies:**
- [ ] Does the module depend on interfaces rather than implementations?
- [ ] Can the implementation be swapped without changing the module?
- [ ] Are dependencies injected rather than instantiated internally?

**Evaluation:**
```markdown
## DIP Assessment: OrderService

**Current:**
```python
class OrderService:
    def __init__(self):
        self.db = PostgresDatabase()  # VIOLATION: concrete dependency
        self.mailer = SmtpMailer()    # VIOLATION: concrete dependency
```

**After DIP:**
```python
class OrderService:
    def __init__(self, db: IDatabase, mailer: IMailer):  # Abstraction
        self.db = db
        self.mailer = mailer
```

**Action:** Introduce interfaces and use dependency injection
```

### Step 4: Evaluate Cohesion

**Principle:** Elements within a module should be highly related to each other.

**Cohesion types (from best to worst):**
| Type | Description | Quality |
|------|-------------|---------|
| Functional | All elements contribute to a single task | Best |
| Sequential | Output of one element is input to another | Good |
| Communicational | Elements operate on same data | OK |
| Procedural | Elements follow a specific sequence | Poor |
| Temporal | Elements grouped by when they execute | Poor |
| Logical | Elements grouped by general category | Bad |
| Coincidental | No meaningful relationship | Worst |

**Checklist:**
- [ ] Can you delete a function without breaking others in the module?
- [ ] Do functions share internal data structures?
- [ ] Is there a clear domain concept the module represents?

### Step 5: Evaluate Coupling

**Principle:** Modules should have minimal dependencies on other modules.

**Coupling types (from best to worst):**
| Type | Description | Quality |
|------|-------------|---------|
| Message | Communicate via messages only | Best |
| Data | Share only primitive data types | Good |
| Stamp | Share data structures | OK |
| Control | One module controls another's behavior | Poor |
| External | Share external dependencies | Poor |
| Common | Share global data | Bad |
| Content | One module modifies another's internals | Worst |

**Checklist:**
- [ ] Count the number of dependencies for each module
- [ ] Identify dependencies that cross domain boundaries
- [ ] Check for circular dependencies

## Checklist

Copy this checklist and track your progress:

- [ ] **SRP Analysis**
  - [ ] List each module's single responsibility
  - [ ] Identify violations (multiple reasons to change)
  - [ ] Plan splits for violating modules
- [ ] **ISP Analysis**
  - [ ] List all interface methods
  - [ ] Map methods to consumers
  - [ ] Identify unused methods per consumer
  - [ ] Plan interface splits
- [ ] **DIP Analysis**
  - [ ] List concrete dependencies
  - [ ] Identify dependencies to abstract
  - [ ] Plan interface introductions
- [ ] **Cohesion Analysis**
  - [ ] Classify each module's cohesion type
  - [ ] Identify low-cohesion modules
  - [ ] Plan refactoring for low cohesion
- [ ] **Coupling Analysis**
  - [ ] Count dependencies per module
  - [ ] Identify high-coupling modules
  - [ ] Plan decoupling strategies

## Examples

### Example: E-Commerce Module SOLID Assessment

```markdown
# SOLID Assessment: E-Commerce System

## Module: OrderModule

### SRP Assessment
**Purpose:** Manage order lifecycle
**Responsibilities:**
- Create orders (OK)
- Update order status (OK)
- Calculate order totals (VIOLATION - calculation should be separate)
- Generate invoices (VIOLATION - invoicing is different domain)

**Action:** Extract PricingModule and InvoiceModule

### ISP Assessment
**Interface: IOrderService**
- createOrder() - Used by: Cart, Admin
- getOrder() - Used by: All
- cancelOrder() - Used by: Customer, Admin
- refundOrder() - Used by: Admin only
- generateReport() - Used by: Analytics only

**Action:** Split into IOrderWriter, IOrderReader, IOrderReporting

### DIP Assessment
**Current Dependencies:**
- PaymentGateway (concrete Stripe) - VIOLATION
- InventoryService (concrete) - VIOLATION
- Database (concrete Postgres) - VIOLATION

**Action:** Introduce IPaymentGateway, IInventory, IDatabase interfaces

### Cohesion: Functional (Good)
All functions related to order management

### Coupling: Data (Good)
Communicates via OrderDTO and OrderEvent
```

### Example: Before/After SOLID Refactoring

**Before (violations):**
```
UserModule
├── createUser()
├── authenticateUser()     # Auth concern
├── resetPassword()        # Auth concern
├── sendWelcomeEmail()     # Notification concern
├── generateUserReport()   # Reporting concern
└── exportToCSV()          # Export concern
```

**After (SOLID compliant):**
```
UserModule (SRP: User CRUD)
├── createUser()
├── updateUser()
├── deleteUser()
└── getUser()

AuthModule (SRP: Authentication)
├── authenticateUser()
├── resetPassword()
└── validateToken()

NotificationModule (SRP: Notifications)
├── sendWelcomeEmail()
├── sendPasswordResetEmail()
└── sendNotification()

ReportingModule (SRP: Reporting)
├── generateUserReport()
├── generateOrderReport()
└── exportToCSV()
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Module has many responsibilities | SRP violation | Split by business reason to change |
| Interface too large | ISP violation | Split into role-specific interfaces |
| Concrete dependencies | DIP violation | Introduce interfaces, use DI |
| Low cohesion | Unrelated elements grouped | Reorganize by domain concept |
| High coupling | Too many dependencies | Introduce abstractions, reduce API surface |
| Circular dependencies | Mutual module dependencies | Extract shared interface or split modules |

## Related Operations

- [op-identify-module-boundaries.md](op-identify-module-boundaries.md) - Find module boundaries
- [op-design-module-apis.md](op-design-module-apis.md) - Design module interfaces
- [op-manage-module-dependencies.md](op-manage-module-dependencies.md) - Handle dependencies
