---
operation: identify-module-boundaries
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-modularization
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Identify Module Boundaries

## When to Use

Use this operation when:
- Designing a new system and need to define module structure
- Refactoring a monolith and need to find natural boundaries
- Migrating to microservices and need to identify service candidates
- Existing modules are unclear or overlapping
- Evaluating architectural changes to module structure

## Prerequisites

- Understanding of system domain and business processes
- Access to existing codebase (if refactoring)
- Knowledge of user workflows and use cases
- Stakeholder input on domain boundaries

## Procedure

### Step 1: Map Domain Concepts

Identify the core domain concepts in your system.

**Domain Modeling Approach:**
1. List all nouns from requirements (potential entities)
2. List all verbs (potential operations)
3. Group related concepts together

```markdown
## Domain Concept Mapping

### Nouns (Entities)
- User, Account, Profile, Credentials
- Order, OrderItem, Cart, Wishlist
- Product, Category, Inventory, Price
- Payment, Invoice, Refund
- Shipment, Address, TrackingNumber

### Verbs (Operations)
- Register, Login, Authenticate, ResetPassword
- CreateOrder, CancelOrder, RefundOrder
- AddToCart, Checkout, CalculateTotal
- ProcessPayment, IssueRefund
- Ship, Track, Deliver

### Concept Groups (Candidate Modules)
| Group | Concepts | Operations |
|-------|----------|------------|
| Identity | User, Account, Credentials | Register, Login, Authenticate |
| Profile | Profile, Preferences | UpdateProfile, GetPreferences |
| Catalog | Product, Category | Search, Browse, Filter |
| Pricing | Price, Discount | CalculatePrice, ApplyDiscount |
| Order | Order, OrderItem | CreateOrder, CancelOrder |
| Cart | Cart, CartItem | AddToCart, RemoveFromCart |
| Payment | Payment, Invoice | ProcessPayment, IssueRefund |
| Shipping | Shipment, Address | Ship, Track |
```

### Step 2: Identify Change Vectors

Determine what causes each part of the system to change.

**Change Vector Analysis:**
| Area | What Triggers Change? | Change Frequency |
|------|----------------------|------------------|
| Authentication | Security policy, providers | Medium |
| User Profile | Business requirements | Low |
| Product Catalog | Marketing, inventory | High |
| Pricing | Sales, promotions | High |
| Orders | Business rules | Medium |
| Payments | Payment providers, compliance | Medium |
| Shipping | Carrier changes, regions | Low |

**Module Boundary Rule:** Things that change together should be in the same module. Things that change for different reasons should be in separate modules.

### Step 3: Find Natural Seams in Code

Look for existing patterns that suggest boundaries.

**Seam Indicators:**
| Indicator | What to Look For |
|-----------|------------------|
| Namespaces/Packages | Existing logical groupings |
| Database Tables | Tables that are always accessed together |
| API Endpoints | Endpoints that share common prefixes |
| Configuration | Settings that are logically grouped |
| Team Ownership | Code maintained by specific teams |

```bash
# Analyze code structure
tldr arch src/

# Find high-level groupings
ls -la src/

# Analyze import patterns
tldr importers module_name src/
```

### Step 4: Define Bounded Contexts

Apply Domain-Driven Design bounded context principles.

**Bounded Context Characteristics:**
- Has its own ubiquitous language
- Has its own data model
- Has clear input/output boundaries
- Can be developed independently

```markdown
## Bounded Contexts

### Identity Context
**Language:** User, Credentials, Session, Token
**Data Model:** Users, Sessions, Tokens tables
**Boundary:**
- Input: Registration data, login credentials
- Output: Authentication tokens, user identity

### Catalog Context
**Language:** Product, Category, Variant, SKU
**Data Model:** Products, Categories, Variants tables
**Boundary:**
- Input: Product queries, search terms
- Output: Product information, search results

### Order Context
**Language:** Order, LineItem, OrderStatus
**Data Model:** Orders, OrderItems tables
**Boundary:**
- Input: Cart contents, customer info
- Output: Order confirmation, order status
```

### Step 5: Validate Boundaries

Test proposed boundaries against quality criteria.

**Boundary Validation Checklist:**
- [ ] Each module has a single clear purpose
- [ ] Module can be tested in isolation
- [ ] Module can be deployed independently
- [ ] Module has minimal dependencies on others
- [ ] Module boundary aligns with team structure
- [ ] Module encapsulates its data (no shared databases)

**Boundary Stress Tests:**
1. **Independence Test:** Can this module be replaced without changing others?
2. **Scaling Test:** Can this module scale independently?
3. **Team Test:** Could a separate team own this module?
4. **Data Test:** Does this module own its data completely?

## Checklist

Copy this checklist and track your progress:

- [ ] **Domain Mapping**
  - [ ] List all domain nouns (entities)
  - [ ] List all domain verbs (operations)
  - [ ] Group related concepts
  - [ ] Create concept group table
- [ ] **Change Vector Analysis**
  - [ ] Identify what triggers changes in each area
  - [ ] Note change frequency for each area
  - [ ] Group areas by change triggers
- [ ] **Seam Identification**
  - [ ] Review existing namespaces/packages
  - [ ] Analyze database table relationships
  - [ ] Review API endpoint groupings
  - [ ] Consider team ownership
- [ ] **Bounded Context Definition**
  - [ ] Define ubiquitous language per context
  - [ ] Define data model per context
  - [ ] Define input/output boundaries
- [ ] **Boundary Validation**
  - [ ] Validate each module against checklist
  - [ ] Run boundary stress tests
  - [ ] Document validation results

## Examples

### Example: E-Commerce Module Boundaries

```markdown
# Module Boundary Analysis: E-Commerce Platform

## Domain Concept Groups

### Group 1: User Identity
**Concepts:** User, Account, Credentials, Session
**Operations:** Register, Login, Logout, ResetPassword
**Boundary:** Authentication and authorization concerns
**Module:** IdentityModule

### Group 2: Customer Profile
**Concepts:** Profile, Address, Preferences, PaymentMethods
**Operations:** UpdateProfile, AddAddress, SetPreferences
**Boundary:** Customer personal data management
**Module:** CustomerModule

### Group 3: Product Catalog
**Concepts:** Product, Category, Variant, Image
**Operations:** Search, Browse, Filter, GetDetails
**Boundary:** Product information and discovery
**Module:** CatalogModule

### Group 4: Shopping
**Concepts:** Cart, CartItem, Wishlist
**Operations:** AddToCart, RemoveFromCart, SaveForLater
**Boundary:** Pre-purchase shopping activity
**Module:** ShoppingModule

### Group 5: Orders
**Concepts:** Order, OrderItem, OrderStatus
**Operations:** CreateOrder, CancelOrder, GetOrderHistory
**Boundary:** Order lifecycle management
**Module:** OrderModule

### Group 6: Payments
**Concepts:** Payment, Transaction, Refund
**Operations:** ProcessPayment, IssueRefund, GetReceipt
**Boundary:** Financial transactions
**Module:** PaymentModule

### Group 7: Fulfillment
**Concepts:** Shipment, Package, Carrier, Tracking
**Operations:** Ship, Track, UpdateStatus
**Boundary:** Order fulfillment and delivery
**Module:** FulfillmentModule

## Validation Results

| Module | Independence | Scaling | Team | Data | Valid |
|--------|--------------|---------|------|------|-------|
| IdentityModule | YES | YES | YES | YES | PASS |
| CustomerModule | YES | YES | YES | YES | PASS |
| CatalogModule | YES | YES | YES | YES | PASS |
| ShoppingModule | PARTIAL* | YES | YES | YES | REVIEW |
| OrderModule | YES | YES | YES | YES | PASS |
| PaymentModule | YES | YES | YES | YES | PASS |
| FulfillmentModule | YES | YES | YES | YES | PASS |

*ShoppingModule has dependency on CatalogModule for product info
```

### Example: Monolith Seam Analysis

```markdown
# Seam Analysis: Legacy Monolith

## Package Structure Analysis
```
src/
├── controllers/     # Web layer
├── services/        # Business logic
├── models/          # Data models
├── repositories/    # Data access
└── utils/           # Shared utilities
```

**Finding:** Layered by technical concern, not domain. Need to reorganize.

## Database Table Clustering
- Users, Sessions, Tokens (always joined) → IdentityModule
- Products, Categories, ProductImages (always joined) → CatalogModule
- Orders, OrderItems (always joined) → OrderModule
- Products ↔ OrderItems (cross-boundary reference)

## API Endpoint Groupings
- /api/auth/* → IdentityModule
- /api/users/* → CustomerModule
- /api/products/* → CatalogModule
- /api/cart/* → ShoppingModule
- /api/orders/* → OrderModule
- /api/payments/* → PaymentModule

## Recommended Module Structure
```
src/
├── identity/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   └── repositories/
├── catalog/
├── shopping/
├── orders/
├── payments/
└── shared/          # Minimal shared code
```
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Overlapping modules | Unclear boundaries | Apply change vector analysis |
| Too many modules | Over-decomposition | Merge related modules |
| Too few modules | Under-decomposition | Split by change vectors |
| Circular dependencies | Poor boundary design | Introduce shared interface module |
| Shared database | Data not partitioned | Define data ownership per module |
| Unclear ownership | Boundary doesn't match teams | Align boundaries with team structure |

## Related Operations

- [op-apply-solid-principles.md](op-apply-solid-principles.md) - Validate modules with SOLID
- [op-design-module-apis.md](op-design-module-apis.md) - Define module interfaces
- [op-manage-module-dependencies.md](op-manage-module-dependencies.md) - Handle cross-module dependencies
- [op-decompose-monolith.md](op-decompose-monolith.md) - Execute monolith decomposition
