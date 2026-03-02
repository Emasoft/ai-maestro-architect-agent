---
name: api-design-guide
description: Comprehensive guide for designing module APIs, including principles for minimal surface area, versioning strategies, compatibility rules, and contract templates
version: 1.0.0
---

# API Design Guide for Module Interfaces

## Table of Contents

- [Overview](#overview)
- [Core API Design Principles](#core-api-design-principles)
  - [Principle 1: Minimal Surface Area](#principle-1-minimal-surface-area)
  - [Principle 2: Stable Contracts](#principle-2-stable-contracts)
  - [Principle 3: Clear Semantics](#principle-3-clear-semantics)
  - [Principle 4: Versioning from Day One](#principle-4-versioning-from-day-one)
- [API Contract Templates](#api-contract-templates)
  - [Template 1: Command API](#template-1-command-api)
  - [Template 2: Query API](#template-2-query-api)
  - [Template 3: Event API](#template-3-event-api)
- [Versioning Strategy](#versioning-strategy)
  - [Semantic Versioning](#semantic-versioning)
  - [Version Negotiation](#version-negotiation)
  - [Breaking Change Guidelines](#breaking-change-guidelines)
  - [Non-Breaking Changes](#non-breaking-changes)
- [Compatibility Rules](#compatibility-rules)
  - [Backward Compatibility](#backward-compatibility)
  - [Forward Compatibility](#forward-compatibility)
- [Data Transfer Objects (DTOs)](#data-transfer-objects-dtos)
  - [Why Use DTOs?](#why-use-dtos)
  - [DTO Example](#dto-example)
- [Error Handling Contracts](#error-handling-contracts)
  - [Error Types](#error-types)
  - [Result Type Pattern](#result-type-pattern)
- [API Documentation](#api-documentation)
  - [Documentation Checklist](#documentation-checklist)
  - [Example: Complete API Documentation](#example-complete-api-documentation)
- [API Testing](#api-testing)
  - [Contract Testing](#contract-testing)
- [Summary](#summary)

## Overview

A module's API is its public contract with other modules. Good API design is critical for maintainability, stability, and evolution of modular systems.

## Core API Design Principles

### Principle 1: Minimal Surface Area

**Definition:** Expose only what consumers need, hide everything else.

**Benefits:**
- Easier to maintain (fewer public contracts to honor)
- Easier to evolve (more freedom to change internals)
- Easier to understand (less to learn)
- Fewer breaking changes

**Example:**
```python
# BAD: Large API surface
class OrderModule:
    # Public
    def create_order()
    def cancel_order()
    def get_order()
    def validate_order()  # Internal concern
    def calculate_tax()   # Internal concern
    def check_inventory() # Internal concern
    def send_notification() # Internal concern
    # 4 public methods, 4 unnecessary public methods

# GOOD: Minimal surface
class OrderModule:
    # Public
    def create_order()
    def cancel_order()
    def get_order()

    # Private
    def _validate_order()
    def _calculate_tax()
    def _check_inventory()
    def _send_notification()
    # 3 public methods, internals hidden
```

### Principle 2: Stable Contracts

**Definition:** API contracts should be stable and change infrequently.

**Guidelines:**
- Design APIs to last years, not months
- Avoid leaking implementation details
- Use data transfer objects (DTOs) instead of internal models
- Anticipate future needs without over-engineering

**Example:**
```python
# BAD: Internal model exposed
def get_order(order_id: int) -> OrderEntity:
    # Returns database entity directly
    return db.query(OrderEntity).get(order_id)

# GOOD: DTO shields consumers from internal changes
def get_order(order_id: int) -> OrderDTO:
    entity = db.query(OrderEntity).get(order_id)
    return OrderDTO(
        id=entity.id,
        status=entity.status,
        total=entity.total,
        # Only expose what consumers need
    )
```

### Principle 3: Clear Semantics

**Definition:** API operations should have clear, unambiguous meaning.

**Guidelines:**
- Use verb-noun naming: `create_order()`, not `handle_order()`
- Be consistent with terminology
- Document preconditions and postconditions
- Define error conditions

**Example:**
```python
# UNCLEAR
def process(data):
    # What does "process" mean? What happens to data?
    pass

# CLEAR
def create_order(customer_id: str, items: List[OrderItem]) -> OrderResult:
    """
    Create a new order for a customer.

    Preconditions:
    - customer_id must exist
    - items list must not be empty
    - all item products must be in stock

    Postconditions:
    - Order is persisted
    - Inventory is reserved
    - Order confirmation email sent

    Returns:
    - OrderResult with order_id on success
    - OrderResult with error on failure

    Errors:
    - CustomerNotFound if customer_id invalid
    - OutOfStock if any item unavailable
    - InvalidItems if items list empty
    """
    pass
```

### Principle 4: Versioning from Day One

**Definition:** Plan for API evolution from the start.

**Strategies:**
- Include version in API identifier
- Document compatibility guarantees
- Use semantic versioning
- Provide migration paths

## API Contract Templates

### Template 1: Command API

Use for operations that change state:

```python
class OrderCommandAPI:
    """
    Commands for modifying order state.
    Version: 2.0.0
    """

    def create_order(
        self,
        customer_id: str,
        items: List[OrderItem],
        shipping_address: Address
    ) -> Result[OrderCreated, OrderError]:
        """
        Create a new order.

        Args:
            customer_id: Existing customer identifier
            items: List of products to order (min 1)
            shipping_address: Delivery address

        Returns:
            Success: OrderCreated with order_id, total, estimated_delivery
            Failure: OrderError with error_code, message

        Errors:
            - CUSTOMER_NOT_FOUND: customer_id doesn't exist
            - INVALID_ITEMS: items list empty or invalid
            - OUT_OF_STOCK: one or more items unavailable
            - INVALID_ADDRESS: shipping_address incomplete

        Side Effects:
            - Order record created in database
            - Inventory reserved for order items
            - Order confirmation email sent to customer

        Idempotency:
            - Not idempotent (creates new order each call)

        Performance:
            - Typical: 200ms
            - Maximum: 2000ms (including email sending)
        """
        pass
```

### Template 2: Query API

Use for operations that read state:

```python
class OrderQueryAPI:
    """
    Queries for reading order data.
    Version: 2.0.0
    """

    def get_order(
        self,
        order_id: str
    ) -> Result[OrderDTO, OrderError]:
        """
        Retrieve order details by ID.

        Args:
            order_id: Order identifier

        Returns:
            Success: OrderDTO with order details
            Failure: OrderError with NOT_FOUND error code

        Errors:
            - NOT_FOUND: order_id doesn't exist

        Side Effects:
            - None (read-only operation)

        Idempotency:
            - Idempotent (safe to call multiple times)

        Performance:
            - Typical: 50ms
            - Maximum: 500ms

        Caching:
            - Results cached for 5 minutes
            - Use cache_control parameter to bypass cache
        """
        pass
```

### Template 3: Event API

Use for asynchronous notifications:

```python
class OrderEventAPI:
    """
    Events published by Order module.
    Version: 2.0.0
    """

    def subscribe_order_created(
        self,
        handler: Callable[[OrderCreatedEvent], None]
    ) -> Subscription:
        """
        Subscribe to order creation events.

        Args:
            handler: Callback invoked for each OrderCreatedEvent

        Returns:
            Subscription object (call unsubscribe() to stop receiving events)

        Event Schema:
            OrderCreatedEvent:
                event_id: str (unique event identifier)
                timestamp: datetime (when event occurred)
                order_id: str (created order identifier)
                customer_id: str (customer who placed order)
                total: Decimal (order total amount)

        Guarantees:
            - At-least-once delivery (handler may be called multiple times for same event)
            - Events delivered in order (for same order_id)

        Handler Errors:
            - If handler raises exception, event will be retried (up to 3 times)

        Performance:
            - Handler must complete within 5 seconds (or event will be retried)
        """
        pass
```

## Versioning Strategy

### Semantic Versioning

Use semantic versioning (MAJOR.MINOR.PATCH) for module APIs:

- **MAJOR:** Breaking changes (incompatible API changes)
- **MINOR:** New features (backward-compatible additions)
- **PATCH:** Bug fixes (backward-compatible fixes)

**Example:**
- `1.0.0` → `1.1.0`: Added `cancel_order()` method (backward-compatible)
- `1.1.0` → `2.0.0`: Removed `delete_order()` method (breaking change)
- `1.1.0` → `1.1.1`: Fixed bug in `get_order()` (backward-compatible)

### Version Negotiation

Support multiple API versions simultaneously during transitions:

```python
class OrderModuleV1:
    """Legacy API - deprecated, supported until 2025-12-31"""
    def create_order(customer_id, items):
        pass

class OrderModuleV2:
    """Current API - introduced 2024-06-01"""
    def create_order(customer_id, items, shipping_address):
        pass
```

**Migration Path:**
1. Release v2 alongside v1
2. Deprecate v1 (announce sunset date)
3. Migrate consumers to v2
4. Remove v1 after sunset date

### Breaking Change Guidelines

**Breaking changes include:**
- Removing public methods
- Renaming public methods
- Changing method signatures (parameters, return types)
- Changing error conditions
- Changing side effects
- Changing performance characteristics significantly

**How to introduce breaking changes:**
1. Add new version (e.g., v2) alongside existing (v1)
2. Deprecate old version with sunset date
3. Provide migration guide
4. Give consumers time to migrate (6-12 months typical)
5. Remove old version after sunset

### Non-Breaking Changes

**Non-breaking changes include:**
- Adding new methods
- Adding optional parameters (with defaults)
- Returning additional fields in responses
- Fixing bugs that make API more correct
- Performance improvements

## Compatibility Rules

### Backward Compatibility

**Definition:** New version works with old consumers.

**Guidelines:**
- Never remove public methods (deprecate instead)
- Never change method signatures in incompatible ways
- Never change error conditions that break consumers
- Add optional parameters only (with sensible defaults)
- Extend response data (but don't remove fields)

### Forward Compatibility

**Definition:** Old version works with new consumers.

**Guidelines:**
- Ignore unknown fields in requests
- Use sensible defaults for missing optional fields
- Document which fields are required vs. optional

## Data Transfer Objects (DTOs)

### Why Use DTOs?

DTOs decouple internal models from API contracts:

- **Internal models** can change without breaking API
- **API stability** is preserved
- **Versioning** is easier (different DTOs for different versions)

### DTO Example

```python
# Internal model (can change freely)
class OrderEntity:
    id: int
    customer_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    # ... many internal fields

# DTO for API v2 (stable contract)
@dataclass
class OrderDTO:
    order_id: str  # Note: string (not int), consumers don't see internal ID
    customer_id: str
    status: OrderStatus  # Enum for type safety
    created_at: str  # ISO 8601 format
    total: str  # String to avoid float precision issues
    items: List[OrderItemDTO]

    # Internal fields not exposed:
    # - updated_at (internal concern)
    # - database implementation details

# Conversion layer
def to_dto(entity: OrderEntity) -> OrderDTO:
    return OrderDTO(
        order_id=str(entity.id),
        customer_id=str(entity.customer_id),
        status=OrderStatus(entity.status),
        created_at=entity.created_at.isoformat(),
        total=str(entity.total),
        items=[to_item_dto(item) for item in entity.items]
    )
```

## Error Handling Contracts

### Error Types

Define clear error types in API contracts:

```python
class OrderError(Enum):
    # Client errors (4xx equivalent)
    CUSTOMER_NOT_FOUND = "Customer ID does not exist"
    INVALID_ITEMS = "Items list is empty or contains invalid items"
    OUT_OF_STOCK = "One or more items are out of stock"
    INVALID_ADDRESS = "Shipping address is incomplete or invalid"
    ORDER_NOT_FOUND = "Order ID does not exist"
    ORDER_ALREADY_CANCELLED = "Order has already been cancelled"

    # Server errors (5xx equivalent)
    DATABASE_ERROR = "Database connection failed"
    PAYMENT_SERVICE_UNAVAILABLE = "Payment service is temporarily unavailable"
    INTERNAL_ERROR = "An unexpected error occurred"
```

### Result Type Pattern

Use Result types for explicit error handling:

```python
@dataclass
class Success[T]:
    value: T

@dataclass
class Failure[E]:
    error: E

Result = Success[T] | Failure[E]

# Usage
result = order_module.create_order(customer_id, items)
match result:
    case Success(order):
        print(f"Order created: {order.order_id}")
    case Failure(error):
        print(f"Error: {error.message}")
```

## API Documentation

### Documentation Checklist

Every public API method must document:

- [ ] Purpose (what it does)
- [ ] Parameters (what inputs it expects)
- [ ] Return value (what it returns)
- [ ] Errors (what can go wrong)
- [ ] Preconditions (what must be true before calling)
- [ ] Postconditions (what will be true after calling)
- [ ] Side effects (what changes it makes)
- [ ] Idempotency (safe to call multiple times?)
- [ ] Performance (typical/maximum latency)
- [ ] Version (when introduced, when deprecated)

### Example: Complete API Documentation

```python
def cancel_order(order_id: str, reason: str) -> Result[OrderCancelled, OrderError]:
    """
    Cancel an existing order.

    Introduced: v1.0.0

    Purpose:
        Cancels an order that has not yet shipped, refunding the customer
        and releasing reserved inventory.

    Parameters:
        order_id: Unique identifier of the order to cancel
        reason: Human-readable cancellation reason (for analytics)

    Returns:
        Success: OrderCancelled with refund_id and refund_amount
        Failure: OrderError with error_code and message

    Errors:
        - ORDER_NOT_FOUND: order_id doesn't exist
        - ORDER_ALREADY_SHIPPED: order has already shipped (cannot cancel)
        - ORDER_ALREADY_CANCELLED: order was already cancelled
        - REFUND_FAILED: payment refund failed (order not cancelled)

    Preconditions:
        - Order must exist
        - Order status must be 'pending' or 'processing' (not 'shipped' or 'delivered')

    Postconditions:
        - Order status set to 'cancelled'
        - Payment refund initiated
        - Inventory reservations released
        - Order cancellation email sent to customer

    Side Effects:
        - Updates order status in database
        - Initiates refund via payment service
        - Releases inventory via inventory service
        - Sends email via notification service

    Idempotency:
        - Idempotent: calling multiple times with same order_id has same effect
        - Returns ORDER_ALREADY_CANCELLED on subsequent calls

    Performance:
        - Typical: 300ms
        - Maximum: 3000ms (including external service calls)

    Example:
        result = order_module.cancel_order("ORD-12345", "Customer requested")
        match result:
            case Success(cancelled):
                print(f"Refund: {cancelled.refund_amount}")
            case Failure(error):
                if error.code == OrderError.ORDER_ALREADY_SHIPPED:
                    print("Cannot cancel shipped order")
    """
    pass
```

## API Testing

### Contract Testing

Test that API implementations honor contracts:

```python
def test_create_order_success():
    # Given: valid inputs
    customer_id = "CUST-123"
    items = [OrderItem(product_id="PROD-1", quantity=1)]
    address = Address(street="123 Main St", city="Springfield")

    # When: calling create_order
    result = order_module.create_order(customer_id, items, address)

    # Then: success result returned
    assert isinstance(result, Success)
    assert result.value.order_id is not None
    assert result.value.total > 0

def test_create_order_customer_not_found():
    # Given: invalid customer ID
    customer_id = "INVALID"
    items = [OrderItem(product_id="PROD-1", quantity=1)]
    address = Address(street="123 Main St", city="Springfield")

    # When: calling create_order
    result = order_module.create_order(customer_id, items, address)

    # Then: failure result with CUSTOMER_NOT_FOUND
    assert isinstance(result, Failure)
    assert result.error.code == OrderError.CUSTOMER_NOT_FOUND
```

## Summary

**Key Principles:**
1. Minimal surface area (expose only what's needed)
2. Stable contracts (design for longevity)
3. Clear semantics (unambiguous meaning)
4. Versioning from day one (plan for evolution)

**Best Practices:**
- Use DTOs to decouple internal models from API
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Document everything (purpose, parameters, errors, performance)
- Test contracts explicitly
- Support multiple versions during transitions
- Provide migration guides for breaking changes

**Remember:** A module's API is its most important artifact. Invest time in designing it well.
