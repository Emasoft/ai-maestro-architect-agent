---
name: boundary-patterns
description: Techniques and patterns for identifying module boundaries in software systems, including domain analysis, change vector identification, seam finding, and bounded context definition
version: 1.0.0
---

# Module Boundary Identification Patterns

## Table of Contents

- [Overview](#overview)
- [Core Principle](#core-principle)
- [Step 1: Map Domain Concepts](#step-1-map-domain-concepts)
  - [Domain-Driven Design Approach](#domain-driven-design-approach)
  - [Entity Relationship Analysis](#entity-relationship-analysis)
- [Step 2: Identify Change Vectors](#step-2-identify-change-vectors)
  - [Change Vector Definition](#change-vector-definition)
  - [Change Scenario Analysis](#change-scenario-analysis)
- [Step 3: Find Natural Seams](#step-3-find-natural-seams)
  - [Code Seam Definition](#code-seam-definition)
  - [Architectural Boundaries](#architectural-boundaries)
  - [Identifying Seams in Existing Code](#identifying-seams-in-existing-code)
- [Step 4: Define Bounded Contexts](#step-4-define-bounded-contexts)
  - [Bounded Context Definition](#bounded-context-definition)
  - [Context Mapping](#context-mapping)
- [Step 5: Validate Boundaries](#step-5-validate-boundaries)
  - [Validation Techniques](#validation-techniques)
  - [Validation Checklist](#validation-checklist)
- [Common Boundary Patterns](#common-boundary-patterns)
  - [Pattern 1: Layer Boundaries](#pattern-1-layer-boundaries)
  - [Pattern 2: Feature Boundaries](#pattern-2-feature-boundaries)
  - [Pattern 3: Entity Boundaries](#pattern-3-entity-boundaries)
  - [Pattern 4: Workflow Boundaries](#pattern-4-workflow-boundaries)
  - [Pattern 5: Infrastructure Boundaries](#pattern-5-infrastructure-boundaries)
- [Anti-Patterns](#anti-patterns)
  - [Anti-Pattern 1: Anemic Modules](#anti-pattern-1-anemic-modules)
  - [Anti-Pattern 2: God Module](#anti-pattern-2-god-module)
  - [Anti-Pattern 3: Chatty Modules](#anti-pattern-3-chatty-modules)
  - [Anti-Pattern 4: Hidden Dependencies](#anti-pattern-4-hidden-dependencies)
  - [Anti-Pattern 5: Wrong Granularity](#anti-pattern-5-wrong-granularity)
- [Decision Framework](#decision-framework)
- [Summary](#summary)

## Overview

Identifying correct module boundaries is critical to successful modularization. This guide provides systematic techniques for finding natural boundaries in your system.

## Core Principle

**Modules should align with natural boundaries in your domain and change patterns.**

Good boundaries:
- Follow domain concepts
- Encapsulate things that change together
- Minimize coupling between modules
- Maximize cohesion within modules

## Step 1: Map Domain Concepts

### Domain-Driven Design Approach

Use Domain-Driven Design (DDD) to identify natural domain boundaries.

**Technique: Event Storming**

1. Gather stakeholders and developers
2. Identify domain events (things that happen)
3. Identify commands (things users do)
4. Identify aggregates (entities with identity)
5. Group related events/commands/aggregates

**Example - E-Commerce:**
```
Domain Events:
- Order Placed
- Payment Received
- Item Shipped
- Product Added to Catalog
- Customer Registered

Aggregates:
- Order (with line items)
- Product (with inventory)
- Customer (with addresses)
- Shipment (with tracking)

Potential Modules:
- OrderManagement (Order Placed, Payment Received)
- Catalog (Product Added)
- CustomerManagement (Customer Registered)
- Shipping (Item Shipped)
```

### Entity Relationship Analysis

Map entity relationships to identify cohesive clusters:

```
Strong relationships (same module):
Order -> OrderLineItem (1-to-many, always accessed together)
Customer -> Address (1-to-many, always accessed together)

Weak relationships (different modules):
Order -> Customer (many-to-one, referenced by ID)
Order -> Product (many-to-many, referenced by ID)
```

**Rule:** Entities with strong, frequent relationships belong in the same module.

## Step 2: Identify Change Vectors

### Change Vector Definition

A change vector is a type of change that typically affects multiple parts of the system together.

**Technique: Historical Change Analysis**

Analyze version control history to identify files that change together:

```bash
# Find files that changed together in last 50 commits
git log --pretty=format: --name-only -50 | sort | uniq -c | sort -rg
```

**Example Results:**
```
15 src/orders/order_service.py
15 src/orders/order_repository.py
15 src/orders/order_model.py
# These files change together -> same module

3 src/orders/order_service.py
3 src/payments/payment_service.py
# These rarely change together -> different modules
```

### Change Scenario Analysis

List typical change scenarios and affected components:

| Scenario | Affected Code | Proposed Module |
|----------|---------------|-----------------|
| Add new product type | Product model, Catalog UI, Search | ProductCatalog |
| Change payment provider | Payment processing logic | PaymentModule |
| Add shipping carrier | Shipping rates, Tracking | ShippingModule |
| Modify order workflow | Order state machine, Order events | OrderManagement |

**Pattern:** Code that changes together should be in the same module.

## Step 3: Find Natural Seams

### Code Seam Definition

A seam is a place in the code where you can alter behavior without editing code on both sides of the boundary.

**Technique: Dependency Analysis**

Visualize dependencies to find natural cut points:

```
Before (Tightly Coupled):
OrderService -> PaymentProcessor.charge_card()
OrderService -> EmailSender.send_receipt()
OrderService -> InventoryTracker.reserve_items()

After (Module Boundaries at Seams):
OrderService -> PaymentInterface.process()
OrderService -> NotificationInterface.send()
OrderService -> InventoryInterface.reserve()
```

### Architectural Boundaries

Common architectural seams:

| Seam Type | Boundary Location | Example |
|-----------|-------------------|---------|
| Layer boundaries | Between architectural layers | UI ↔ Business Logic ↔ Data |
| Protocol boundaries | Between communication protocols | HTTP ↔ Message Queue |
| Format boundaries | Between data formats | JSON ↔ Database ↔ XML |
| Platform boundaries | Between execution environments | Web ↔ Mobile ↔ Desktop |

### Identifying Seams in Existing Code

Look for these indicators of natural seams:

1. **Interface boundaries:** Existing interfaces often mark good seams
2. **Data transfer objects (DTOs):** Code that transforms DTOs is a seam
3. **Error boundaries:** Exception handlers separate concerns
4. **Transaction boundaries:** Database transactions mark consistency boundaries
5. **Security boundaries:** Authentication/authorization checks are seams

## Step 4: Define Bounded Contexts

### Bounded Context Definition

A bounded context is a conceptual boundary within which a domain model is consistent. The same term can mean different things in different contexts.

**Example: "Customer" in E-Commerce**

| Context | Customer Definition | Attributes |
|---------|---------------------|------------|
| Sales | Person buying products | Name, Email, Payment Methods |
| Shipping | Delivery recipient | Name, Address, Phone |
| Support | Person needing help | Name, Ticket History, Contact Preferences |
| Reporting | Data point | Customer ID, Purchase History |

**Module Mapping:**
- SalesModule: Customer = Buyer
- ShippingModule: Customer = Recipient
- SupportModule: Customer = SupportCase.customer
- ReportingModule: Customer = CustomerDimension

### Context Mapping

Document relationships between bounded contexts:

```
SalesContext -> ShippingContext: Order placed event
ShippingContext -> CustomerContext: Query address by ID
SupportContext -> SalesContext: Query order history by customer ID
```

**Translation at Boundaries:**

When data crosses context boundaries, translate between representations:

```python
# Sales context
SalesCustomer:
  customer_id
  email
  payment_methods[]

# Shipping context
ShippingRecipient:
  recipient_id  # Same as customer_id
  name
  address
  phone

# Translation layer
def to_recipient(sales_customer: SalesCustomer) -> ShippingRecipient:
    return ShippingRecipient(
        recipient_id=sales_customer.customer_id,
        name=sales_customer.name,
        # ...
    )
```

## Step 5: Validate Boundaries

### Validation Techniques

**1. Change Impact Analysis**

For each proposed boundary, ask:
- If I change code in Module A, will I need to change Module B?
- If yes, why? Can the boundary be improved?

**2. Testing Independence**

For each module:
- Can it be tested without starting other modules?
- Can dependencies be easily mocked?
- Are tests fast and isolated?

**3. Deployment Independence**

For each module:
- Can it be deployed without deploying other modules?
- What is the deployment coupling?
- Can it scale independently?

**4. Team Independence**

For each module:
- Can a team own and modify it without coordinating with other teams?
- Are responsibilities clear?
- Is the API stable?

### Validation Checklist

For each proposed module boundary, verify:

- [ ] **Domain alignment:** Module corresponds to a domain concept
- [ ] **Change locality:** Changes are typically within one module
- [ ] **Seam clarity:** Boundary is at a natural seam in the code
- [ ] **Bounded context:** Module has consistent domain model
- [ ] **Low coupling:** Few dependencies on other modules
- [ ] **High cohesion:** All code in module serves module's purpose
- [ ] **Testability:** Module can be tested independently
- [ ] **Team ownership:** A team can own the module

## Common Boundary Patterns

### Pattern 1: Layer Boundaries

Split system into architectural layers:

```
Presentation Layer
  ↓
Business Logic Layer
  ↓
Data Access Layer
```

**Use When:** Clear separation of UI, logic, and data concerns

### Pattern 2: Feature Boundaries

Split by user-facing features:

```
ProductSearchModule
ProductCatalogModule
ShoppingCartModule
CheckoutModule
```

**Use When:** Features evolve independently

### Pattern 3: Entity Boundaries

Split by domain entities:

```
UserModule
ProductModule
OrderModule
PaymentModule
```

**Use When:** Entities have rich behavior and clear lifecycles

### Pattern 4: Workflow Boundaries

Split by business workflows:

```
OrderCreationModule
OrderFulfillmentModule
OrderCancellationModule
ReturnProcessingModule
```

**Use When:** Workflows are complex and change independently

### Pattern 5: Infrastructure Boundaries

Split by technical concerns:

```
DatabaseModule
CacheModule
MessageQueueModule
EmailModule
```

**Use When:** Infrastructure needs to be swapped or scaled independently

## Anti-Patterns

### Anti-Pattern 1: Anemic Modules

**Problem:** Module is just data structures with getters/setters, no behavior.

**Fix:** Move behavior into the module where the data lives.

### Anti-Pattern 2: God Module

**Problem:** One module handles many responsibilities.

**Fix:** Apply Single Responsibility Principle - split into focused modules.

### Anti-Pattern 3: Chatty Modules

**Problem:** Modules make many fine-grained calls to each other.

**Fix:** Introduce coarser-grained APIs, batch operations, or move related code together.

### Anti-Pattern 4: Hidden Dependencies

**Problem:** Module depends on another module's internal implementation.

**Fix:** Make dependencies explicit through interfaces.

### Anti-Pattern 5: Wrong Granularity

**Problem:** Modules are too small (many tiny modules) or too large (few giant modules).

**Fix:** Balance between too many modules (overhead) and too few (coupling).

## Decision Framework

When deciding on a module boundary, consider:

| Factor | Good Boundary | Poor Boundary |
|--------|---------------|---------------|
| Change frequency | Changes are local to module | Changes ripple across modules |
| Cohesion | All code relates to module purpose | Code has multiple unrelated purposes |
| Coupling | Few, well-defined dependencies | Many implicit dependencies |
| Understanding | Clear responsibility | Unclear responsibility |
| Testing | Can test independently | Must test with other modules |
| Deployment | Can deploy independently | Must deploy together |
| Team ownership | One team owns module | Multiple teams modify module |

## Summary

Good module boundaries:

1. **Align with domain concepts** from DDD analysis
2. **Encapsulate change vectors** so changes are local
3. **Sit at natural seams** in the architecture
4. **Define bounded contexts** with consistent models
5. **Pass validation criteria** for coupling, cohesion, testability

**Process:**
1. Map domain concepts
2. Identify change vectors
3. Find natural seams
4. Define bounded contexts
5. Validate proposed boundaries
6. Iterate and refine

Start with domain analysis, validate with change patterns, and refine through testing.
