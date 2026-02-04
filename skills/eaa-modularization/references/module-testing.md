---
name: module-testing
description: Comprehensive testing strategies for modular systems, including unit testing, integration testing, contract testing, and mocking techniques for module dependencies
version: 1.0.0
---

# Module Testing Strategies

## Table of Contents

- [Overview](#overview)
- [Testing Pyramid for Modular Systems](#testing-pyramid-for-modular-systems)
- [Unit Testing Modules](#unit-testing-modules)
  - [Unit Test Definition](#unit-test-definition)
  - [Unit Test Example](#unit-test-example)
  - [Unit Test Best Practices](#unit-test-best-practices)
- [Mocking Module Dependencies](#mocking-module-dependencies)
  - [Why Mock?](#why-mock)
  - [Mocking Strategies](#mocking-strategies)
  - [Dependency Injection for Testing](#dependency-injection-for-testing)
- [Contract Testing](#contract-testing)
  - [What is Contract Testing?](#what-is-contract-testing)
  - [Contract Test Example](#contract-test-example)
  - [Consumer-Driven Contract Testing](#consumer-driven-contract-testing)
- [Integration Testing](#integration-testing)
  - [Integration Test Definition](#integration-test-definition)
  - [Integration Test Example](#integration-test-example)
  - [Integration Test Patterns](#integration-test-patterns)
- [Test Doubles Taxonomy](#test-doubles-taxonomy)
  - [Example of Each](#example-of-each)
- [Testing Strategies by Module Type](#testing-strategies-by-module-type)
  - [Strategy 1: Testing Domain Modules](#strategy-1-testing-domain-modules)
  - [Strategy 2: Testing Infrastructure Modules](#strategy-2-testing-infrastructure-modules)
  - [Strategy 3: Testing API Modules](#strategy-3-testing-api-modules)
- [Test Data Management](#test-data-management)
  - [Test Data Strategies](#test-data-strategies)
- [Summary](#summary)

## Overview

Testing modular systems requires different strategies than testing monolithic applications. This guide covers how to test modules in isolation and in integration with proper mocking, contract testing, and validation.

## Testing Pyramid for Modular Systems

```
        /\
       /  \  End-to-End Tests (Few)
      /____\
     /      \  Integration Tests (Some)
    /________\
   /          \  Contract Tests (Moderate)
  /____________\
 /              \  Unit Tests (Many)
/________________\
```

| Test Type | Scope | Speed | Quantity | Purpose |
|-----------|-------|-------|----------|---------|
| Unit | Single module, mocked deps | Fast | Many | Verify module logic |
| Contract | Module API | Fast | Moderate | Verify interface contracts |
| Integration | Multiple modules | Medium | Some | Verify module interactions |
| End-to-End | Entire system | Slow | Few | Verify user scenarios |

## Unit Testing Modules

### Unit Test Definition

A unit test for a module:
- Tests one module in isolation
- Mocks all dependencies on other modules
- Verifies internal logic and behavior
- Runs fast (milliseconds)

### Unit Test Example

```python
# Module under test
class OrderService:
    def __init__(
        self,
        customer_repo: CustomerRepository,
        inventory_service: InventoryService,
        payment_service: PaymentService
    ):
        self.customer_repo = customer_repo
        self.inventory_service = inventory_service
        self.payment_service = payment_service

    def create_order(
        self,
        customer_id: str,
        items: List[OrderItem]
    ) -> Result[Order, OrderError]:
        # 1. Validate customer exists
        customer = self.customer_repo.get(customer_id)
        if not customer:
            return Failure(OrderError.CUSTOMER_NOT_FOUND)

        # 2. Check inventory
        for item in items:
            if not self.inventory_service.is_available(item.product_id, item.quantity):
                return Failure(OrderError.OUT_OF_STOCK)

        # 3. Calculate total
        total = sum(item.price * item.quantity for item in items)

        # 4. Create order
        order = Order(customer_id=customer_id, items=items, total=total)
        return Success(order)

# Unit test (mocks all dependencies)
def test_create_order_success():
    # Arrange - create mocks
    customer_repo = Mock(spec=CustomerRepository)
    customer_repo.get.return_value = Customer(id="CUST-123", name="John")

    inventory_service = Mock(spec=InventoryService)
    inventory_service.is_available.return_value = True

    payment_service = Mock(spec=PaymentService)

    order_service = OrderService(
        customer_repo=customer_repo,
        inventory_service=inventory_service,
        payment_service=payment_service
    )

    # Act
    result = order_service.create_order(
        customer_id="CUST-123",
        items=[OrderItem(product_id="PROD-1", quantity=1, price=10.0)]
    )

    # Assert
    assert isinstance(result, Success)
    assert result.value.customer_id == "CUST-123"
    assert result.value.total == 10.0

    # Verify interactions
    customer_repo.get.assert_called_once_with("CUST-123")
    inventory_service.is_available.assert_called_once_with("PROD-1", 1)

def test_create_order_customer_not_found():
    # Arrange - mock returns None (customer not found)
    customer_repo = Mock(spec=CustomerRepository)
    customer_repo.get.return_value = None

    inventory_service = Mock(spec=InventoryService)
    payment_service = Mock(spec=PaymentService)

    order_service = OrderService(customer_repo, inventory_service, payment_service)

    # Act
    result = order_service.create_order(
        customer_id="INVALID",
        items=[OrderItem(product_id="PROD-1", quantity=1, price=10.0)]
    )

    # Assert
    assert isinstance(result, Failure)
    assert result.error == OrderError.CUSTOMER_NOT_FOUND

def test_create_order_out_of_stock():
    # Arrange - mock inventory returns False
    customer_repo = Mock(spec=CustomerRepository)
    customer_repo.get.return_value = Customer(id="CUST-123", name="John")

    inventory_service = Mock(spec=InventoryService)
    inventory_service.is_available.return_value = False  # Out of stock!

    payment_service = Mock(spec=PaymentService)

    order_service = OrderService(customer_repo, inventory_service, payment_service)

    # Act
    result = order_service.create_order(
        customer_id="CUST-123",
        items=[OrderItem(product_id="PROD-1", quantity=1, price=10.0)]
    )

    # Assert
    assert isinstance(result, Failure)
    assert result.error == OrderError.OUT_OF_STOCK
```

### Unit Test Best Practices

- **One assertion per test** (or closely related assertions)
- **Descriptive test names** (`test_create_order_when_customer_not_found_returns_error`)
- **Arrange-Act-Assert pattern** (setup, execute, verify)
- **Mock all external dependencies** (databases, APIs, other modules)
- **Test happy path and error cases**
- **Verify interactions** (was dependency called correctly?)

## Mocking Module Dependencies

### Why Mock?

| Reason | Explanation |
|--------|-------------|
| Speed | Avoid slow operations (DB, network) |
| Isolation | Test only the module under test |
| Reliability | Don't depend on external systems |
| Control | Simulate error conditions easily |

### Mocking Strategies

#### Strategy 1: Mock Objects

Use mocking library to create fake objects:

```python
from unittest.mock import Mock

# Create mock
customer_repo = Mock(spec=CustomerRepository)

# Configure behavior
customer_repo.get.return_value = Customer(id="123", name="John")

# Use in test
customer = customer_repo.get("123")  # Returns mocked customer

# Verify calls
customer_repo.get.assert_called_once_with("123")
```

#### Strategy 2: Stub Implementations

Create minimal real implementations for testing:

```python
# Stub implementation
class InMemoryCustomerRepository(CustomerRepository):
    def __init__(self):
        self.customers = {}

    def get(self, customer_id: str) -> Optional[Customer]:
        return self.customers.get(customer_id)

    def save(self, customer: Customer):
        self.customers[customer.id] = customer

# Use in test
repo = InMemoryCustomerRepository()
repo.save(Customer(id="123", name="John"))

order_service = OrderService(customer_repo=repo, ...)
result = order_service.create_order("123", items)
```

#### Strategy 3: Fake Services

For complex dependencies, create fake services:

```python
class FakePaymentService(PaymentService):
    """Fake payment service for testing - always succeeds"""

    def __init__(self):
        self.payments = []

    def charge(self, amount: Money, method: PaymentMethod) -> Result:
        payment = Payment(id=f"PAY-{len(self.payments)}", amount=amount)
        self.payments.append(payment)
        return Success(payment)
```

### Dependency Injection for Testing

Use dependency injection to make mocking easy:

```python
# Module designed for DI
class OrderService:
    def __init__(
        self,
        customer_repo: CustomerRepository,  # Interface, not concrete class
        inventory_service: InventoryService,
        payment_service: PaymentService
    ):
        # Dependencies injected via constructor
        self.customer_repo = customer_repo
        self.inventory_service = inventory_service
        self.payment_service = payment_service

# In production
order_service = OrderService(
    customer_repo=PostgreSQLCustomerRepository(),
    inventory_service=HTTPInventoryService(),
    payment_service=StripePaymentService()
)

# In tests
order_service = OrderService(
    customer_repo=Mock(spec=CustomerRepository),
    inventory_service=Mock(spec=InventoryService),
    payment_service=Mock(spec=PaymentService)
)
```

## Contract Testing

### What is Contract Testing?

Contract testing verifies that a module's API behaves according to its contract (interface specification).

**Focus:** Does the implementation honor the interface contract?

### Contract Test Example

```python
# Interface contract
class CustomerRepository(ABC):
    """
    Repository for customer data.

    Contract:
    - get(customer_id) returns Customer if exists, None otherwise
    - get(customer_id) raises RepositoryError on database failure
    - save(customer) persists customer
    - save(customer) is idempotent
    """

    @abstractmethod
    def get(self, customer_id: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass

# Contract test suite (tests ANY implementation)
class CustomerRepositoryContractTests:
    """
    Contract tests for CustomerRepository interface.
    Any implementation must pass these tests.
    """

    def test_get_existing_customer_returns_customer(self, repo: CustomerRepository):
        # Arrange
        customer = Customer(id="123", name="John")
        repo.save(customer)

        # Act
        result = repo.get("123")

        # Assert
        assert result is not None
        assert result.id == "123"
        assert result.name == "John"

    def test_get_nonexistent_customer_returns_none(self, repo: CustomerRepository):
        # Act
        result = repo.get("NONEXISTENT")

        # Assert
        assert result is None

    def test_save_is_idempotent(self, repo: CustomerRepository):
        # Arrange
        customer = Customer(id="123", name="John")

        # Act - save twice
        repo.save(customer)
        repo.save(customer)

        # Assert - only one customer
        result = repo.get("123")
        assert result is not None

# Test PostgreSQL implementation against contract
class TestPostgreSQLCustomerRepository(CustomerRepositoryContractTests):
    @pytest.fixture
    def repo(self):
        return PostgreSQLCustomerRepository(db_url="postgresql://test")

# Test InMemory implementation against contract
class TestInMemoryCustomerRepository(CustomerRepositoryContractTests):
    @pytest.fixture
    def repo(self):
        return InMemoryCustomerRepository()
```

### Consumer-Driven Contract Testing

For modules that depend on each other, use consumer-driven contracts:

```python
# OrderModule is consumer, CustomerModule is provider

# Consumer defines expected contract
class OrderModuleCustomerContract:
    """
    OrderModule expects CustomerModule to provide:
    - get_customer(customer_id) -> Customer or None
    - Customer has: id, name, email
    """

    def test_can_get_customer(self, customer_module):
        result = customer_module.get_customer("123")
        assert hasattr(result, 'id')
        assert hasattr(result, 'name')
        assert hasattr(result, 'email')

# Provider (CustomerModule) must pass consumer contract tests
class TestCustomerModuleMeetsOrderModuleContract(OrderModuleCustomerContract):
    @pytest.fixture
    def customer_module(self):
        return CustomerModule()
```

**Benefits:**
- Consumer defines what it needs (not provider guessing)
- Provider can't break consumer without failing tests
- Enables independent evolution

## Integration Testing

### Integration Test Definition

Integration tests verify that multiple modules work together correctly.

**Characteristics:**
- Tests real module interactions (not mocked)
- May use test databases, message queues, etc.
- Slower than unit tests (seconds)
- Fewer in number than unit tests

### Integration Test Example

```python
# Integration test (real modules, test database)
def test_order_creation_integration():
    # Arrange - use real implementations with test database
    db = TestDatabase()
    customer_repo = PostgreSQLCustomerRepository(db)
    inventory_service = InventoryService(db)
    payment_service = FakePaymentService()  # Fake (don't charge real money!)

    order_service = OrderService(customer_repo, inventory_service, payment_service)

    # Setup test data
    customer = Customer(id="CUST-123", name="John", email="john@example.com")
    customer_repo.save(customer)

    product = Product(id="PROD-1", name="Widget", price=10.0, stock=100)
    inventory_service.add_product(product)

    # Act
    result = order_service.create_order(
        customer_id="CUST-123",
        items=[OrderItem(product_id="PROD-1", quantity=2, price=10.0)]
    )

    # Assert
    assert isinstance(result, Success)
    order = result.value

    # Verify side effects
    assert order.total == 20.0
    assert inventory_service.get_stock("PROD-1") == 98  # Stock reduced
    assert len(payment_service.payments) == 1  # Payment recorded

    # Cleanup
    db.rollback()
```

### Integration Test Patterns

#### Pattern 1: Test Database

Use a real database in test mode:

```python
@pytest.fixture(scope="function")
def test_db():
    db = Database("postgresql://localhost/test_db")
    db.migrate()  # Apply schema
    yield db
    db.rollback()  # Clean up after test
```

#### Pattern 2: In-Memory Implementations

Use in-memory versions for speed:

```python
@pytest.fixture
def in_memory_services():
    return {
        'customer_repo': InMemoryCustomerRepository(),
        'inventory_service': InMemoryInventoryService(),
        'order_repo': InMemoryOrderRepository()
    }
```

#### Pattern 3: Containerized Dependencies

Use Docker containers for external dependencies:

```python
@pytest.fixture(scope="session")
def postgres_container():
    container = docker.run("postgres:14", ports={"5432": "5432"})
    wait_for_postgres(container)
    yield container
    container.stop()
```

## Test Doubles Taxonomy

| Type | Definition | Example |
|------|------------|---------|
| **Dummy** | Passed but never used | Placeholder for required parameter |
| **Stub** | Returns canned responses | `get()` always returns fixed customer |
| **Spy** | Records calls for verification | Tracks which methods were called |
| **Mock** | Pre-programmed with expected calls | Verifies `save()` called with specific args |
| **Fake** | Working implementation (simplified) | In-memory database |

### Example of Each

```python
# Dummy (never used, just fulfills parameter requirement)
dummy_logger = Mock(spec=Logger)
service = Service(logger=dummy_logger)  # logger never called in test

# Stub (returns fixed data)
stub_repo = Mock(spec=CustomerRepository)
stub_repo.get.return_value = Customer(id="123", name="John")

# Spy (records calls)
spy_repo = Mock(spec=CustomerRepository)
service.do_something()
spy_repo.save.assert_called_once()  # Verify save was called

# Mock (pre-programmed expectations)
mock_repo = Mock(spec=CustomerRepository)
mock_repo.get.assert_called_with("123")  # Expect specific call

# Fake (real simplified implementation)
fake_repo = InMemoryCustomerRepository()  # Actual working repository
```

## Testing Strategies by Module Type

### Strategy 1: Testing Domain Modules

Domain modules contain business logic:

```python
# Domain module
class OrderModule:
    def calculate_total(self, items: List[OrderItem]) -> Decimal:
        # Pure business logic (no dependencies)
        subtotal = sum(item.price * item.quantity for item in items)
        tax = subtotal * Decimal("0.08")
        return subtotal + tax

# Test (no mocks needed - pure logic)
def test_calculate_total():
    items = [
        OrderItem(price=Decimal("10.00"), quantity=2),
        OrderItem(price=Decimal("5.00"), quantity=1)
    ]
    result = OrderModule().calculate_total(items)
    assert result == Decimal("27.00")  # (10*2 + 5*1) * 1.08
```

**Testing focus:** Logic correctness, edge cases, calculations

### Strategy 2: Testing Infrastructure Modules

Infrastructure modules interact with external systems:

```python
# Infrastructure module
class PostgreSQLRepository:
    def save(self, entity: Entity):
        # Interacts with database
        pass

# Test with real database (integration test)
def test_save_persists_entity(test_db):
    repo = PostgreSQLRepository(test_db)
    entity = Entity(id="123", data="test")

    repo.save(entity)

    # Verify persisted
    result = repo.get("123")
    assert result.data == "test"
```

**Testing focus:** Correct interaction with external system, error handling

### Strategy 3: Testing API Modules

API modules expose interfaces to other modules:

```python
# API module
class OrderAPI:
    def create_order(
        self,
        customer_id: str,
        items: List[OrderItem]
    ) -> Result[OrderDTO, OrderError]:
        # Delegates to service
        result = self.order_service.create_order(customer_id, items)
        return result.map(to_dto)

# Test (mock service, focus on API contract)
def test_create_order_api():
    service = Mock(spec=OrderService)
    service.create_order.return_value = Success(Order(id="ORD-123", ...))

    api = OrderAPI(service)
    result = api.create_order("CUST-123", items)

    assert isinstance(result, Success)
    assert isinstance(result.value, OrderDTO)
    assert result.value.order_id == "ORD-123"
```

**Testing focus:** API contract, DTO conversion, error translation

## Test Data Management

### Test Data Strategies

**Strategy 1: Test Fixtures**

Pre-defined test data:

```python
@pytest.fixture
def sample_customer():
    return Customer(id="CUST-123", name="John Doe", email="john@example.com")

@pytest.fixture
def sample_order(sample_customer):
    return Order(
        id="ORD-456",
        customer_id=sample_customer.id,
        items=[OrderItem(product_id="PROD-1", quantity=1, price=10.0)],
        total=10.0
    )
```

**Strategy 2: Factory Pattern**

Generate test data dynamically:

```python
class CustomerFactory:
    @staticmethod
    def create(id="CUST-123", name="John Doe", email="john@example.com"):
        return Customer(id=id, name=name, email=email)

# Usage
customer1 = CustomerFactory.create()
customer2 = CustomerFactory.create(id="CUST-456", name="Jane Smith")
```

**Strategy 3: Faker Library**

Generate realistic fake data:

```python
from faker import Faker

fake = Faker()

customer = Customer(
    id=fake.uuid4(),
    name=fake.name(),
    email=fake.email()
)
```

## Summary

**Testing Strategies:**

| Test Type | Scope | Dependencies | Speed | Quantity |
|-----------|-------|--------------|-------|----------|
| Unit | Single module | Mocked | Fast | Many |
| Contract | Module API | Real/mocked | Fast | Moderate |
| Integration | Multiple modules | Real | Medium | Some |
| End-to-End | Entire system | Real | Slow | Few |

**Key Practices:**
- **Unit test** module logic with mocked dependencies
- **Contract test** interface implementations
- **Integration test** module interactions
- **Mock** external dependencies for unit tests
- **Use real implementations** for integration tests
- **Test data:** fixtures, factories, or fakers

**Mocking:**
- Use mocks for external dependencies (DB, APIs, other modules)
- Use stubs for simple return values
- Use fakes for complex behavior (in-memory DB)
- Verify interactions (was dependency called correctly?)

**Module Testing Enables:**
- Independent module development
- Confident refactoring
- Fast feedback loops
- Regression prevention
- Living documentation

Proper testing is essential for maintaining modular system quality and enabling independent module evolution.
