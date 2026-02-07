---
operation: design-module-apis
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-modularization
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Design Module APIs

## When to Use

Use this operation when:
- Defining interfaces between modules
- Creating contracts for module communication
- Designing DTOs for inter-module data transfer
- Establishing versioning strategy for APIs
- Defining error handling contracts between modules

## Prerequisites

- Module boundaries have been identified
- Module responsibilities are clearly defined
- Understanding of data that flows between modules
- Knowledge of consumers for each module

## Procedure

### Step 1: Define Public Interface for Each Module

Identify what operations each module exposes to others.

**Interface Design Principles:**
| Principle | Description |
|-----------|-------------|
| Minimal Surface | Expose only what consumers need |
| Cohesive Operations | Group related operations |
| Stable Contracts | Interfaces change rarely |
| Explicit Types | Clear input/output types |

```markdown
## Module: AuthModule

### Public Interface

```typescript
interface IAuthService {
  // Authentication
  authenticate(credentials: Credentials): Promise<AuthResult>;
  validateToken(token: string): Promise<TokenValidation>;
  refreshToken(refreshToken: string): Promise<AuthResult>;

  // Session Management
  logout(token: string): Promise<void>;
  invalidateAllSessions(userId: string): Promise<void>;
}
```

### Internal (Not Exposed)
- Password hashing implementation
- Token generation algorithm
- Session storage details
```

### Step 2: Document API Contracts

For each interface method, document the contract.

```markdown
## API Contract: authenticate()

### Description
Validates user credentials and returns authentication tokens.

### Input
```typescript
interface Credentials {
  email: string;       // Valid email format
  password: string;    // Minimum 8 characters
}
```

### Output (Success)
```typescript
interface AuthResult {
  success: true;
  accessToken: string;    // JWT, expires in 1 hour
  refreshToken: string;   // Opaque token, expires in 7 days
  expiresAt: number;      // Unix timestamp
  user: {
    id: string;
    email: string;
    name: string;
  };
}
```

### Output (Failure)
```typescript
interface AuthFailure {
  success: false;
  error: {
    code: 'INVALID_CREDENTIALS' | 'ACCOUNT_LOCKED' | 'ACCOUNT_DISABLED';
    message: string;
  };
}
```

### Preconditions
- Credentials must be non-empty
- Email must be valid format

### Postconditions
- On success: tokens are valid and can be used for protected operations
- On failure: no tokens are issued, error explains reason

### Side Effects
- Successful login updates last_login timestamp
- Failed login increments failed_attempt counter
```

### Step 3: Design Data Transfer Objects (DTOs)

Create DTOs for data that crosses module boundaries.

**DTO Design Rules:**
| Rule | Description |
|------|-------------|
| Immutable | DTOs should not change after creation |
| Flat | Minimize nesting when possible |
| Explicit | No optional fields without clear meaning |
| Versioned | Include version or be backward compatible |

```markdown
## DTOs: AuthModule

### UserDTO
```typescript
interface UserDTO {
  id: string;
  email: string;
  name: string;
  createdAt: string;     // ISO 8601
  lastLoginAt: string;   // ISO 8601
}
```

### TokenDTO
```typescript
interface TokenDTO {
  accessToken: string;
  refreshToken: string;
  expiresAt: number;     // Unix timestamp
  tokenType: 'Bearer';
}
```

### Do NOT Expose
- PasswordHash
- SessionId (internal)
- AuthAttempts (internal)
```

### Step 4: Plan Versioning Strategy

Define how APIs will evolve over time.

**Versioning Strategies:**
| Strategy | When to Use |
|----------|-------------|
| URL Versioning | `/api/v1/users` - Clear, visible |
| Header Versioning | `Api-Version: 1` - Cleaner URLs |
| Content Negotiation | `Accept: application/vnd.api.v1+json` |

**Version Change Rules:**
```markdown
## Versioning Rules

### No Version Change Required (Backward Compatible)
- Adding new optional fields to response
- Adding new endpoints
- Adding new optional query parameters
- Fixing bugs in existing behavior

### Minor Version Change (v1 → v1.1)
- Adding new required fields (with defaults)
- Deprecating fields (still present)
- Performance changes

### Major Version Change (v1 → v2)
- Removing fields
- Changing field types
- Changing endpoint paths
- Changing authentication method
```

### Step 5: Define Error Handling Contracts

Establish consistent error handling across modules.

```markdown
## Error Contract

### Standard Error Response
```typescript
interface ModuleError {
  code: string;           // Machine-readable code
  message: string;        // Human-readable message
  details?: object;       // Additional context
  timestamp: string;      // ISO 8601
  traceId?: string;       // For debugging
}
```

### Error Code Categories
| Prefix | Category | Example |
|--------|----------|---------|
| AUTH_ | Authentication | AUTH_INVALID_TOKEN |
| VAL_ | Validation | VAL_MISSING_FIELD |
| BIZ_ | Business Rule | BIZ_INSUFFICIENT_FUNDS |
| SYS_ | System | SYS_DATABASE_ERROR |

### Error Propagation Rules
1. Catch and wrap errors at module boundaries
2. Never expose internal implementation details
3. Always include error code for programmatic handling
4. Log full error internally, return sanitized error externally
```

## Checklist

Copy this checklist and track your progress:

- [ ] **Interface Definition**
  - [ ] List all modules
  - [ ] Define public interface for each module
  - [ ] Identify internal (non-exposed) operations
  - [ ] Apply minimal surface principle
- [ ] **Contract Documentation**
  - [ ] Document input types for each method
  - [ ] Document output types (success and failure)
  - [ ] Define preconditions and postconditions
  - [ ] Document side effects
- [ ] **DTO Design**
  - [ ] Create DTOs for cross-boundary data
  - [ ] Ensure DTOs are immutable
  - [ ] Keep DTOs flat when possible
  - [ ] Document what NOT to expose
- [ ] **Versioning Strategy**
  - [ ] Choose versioning approach
  - [ ] Document version change rules
  - [ ] Plan deprecation process
- [ ] **Error Handling**
  - [ ] Define standard error format
  - [ ] Create error code categories
  - [ ] Document error propagation rules

## Examples

### Example: Order Module API Design

```markdown
# API Design: OrderModule

## Public Interface

```typescript
interface IOrderService {
  // Commands
  createOrder(request: CreateOrderRequest): Promise<OrderResult>;
  cancelOrder(orderId: string, reason: string): Promise<CancelResult>;
  updateOrderStatus(orderId: string, status: OrderStatus): Promise<void>;

  // Queries
  getOrder(orderId: string): Promise<OrderDTO | null>;
  getOrdersByCustomer(customerId: string, options: QueryOptions): Promise<OrderListDTO>;
  getOrderStatus(orderId: string): Promise<OrderStatusDTO>;
}
```

## DTOs

### CreateOrderRequest
```typescript
interface CreateOrderRequest {
  customerId: string;
  items: OrderItemInput[];
  shippingAddress: AddressDTO;
  paymentMethod: PaymentMethodDTO;
  notes?: string;
}

interface OrderItemInput {
  productId: string;
  quantity: number;
  priceAtOrder: number;  // Captured at order time
}
```

### OrderDTO
```typescript
interface OrderDTO {
  id: string;
  customerId: string;
  status: OrderStatus;
  items: OrderItemDTO[];
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
  shippingAddress: AddressDTO;
  createdAt: string;
  updatedAt: string;
}
```

### OrderStatus
```typescript
type OrderStatus =
  | 'pending'
  | 'confirmed'
  | 'processing'
  | 'shipped'
  | 'delivered'
  | 'cancelled';
```

## Error Codes

| Code | Meaning | HTTP Status |
|------|---------|-------------|
| ORDER_NOT_FOUND | Order ID doesn't exist | 404 |
| ORDER_INVALID_STATUS | Invalid status transition | 400 |
| ORDER_ALREADY_CANCELLED | Cannot modify cancelled order | 409 |
| ORDER_ITEM_UNAVAILABLE | Product not in stock | 422 |
| ORDER_PAYMENT_FAILED | Payment processing failed | 402 |

## API Contract: createOrder()

### Input
- CreateOrderRequest with valid customer, items, address, payment

### Output (Success)
```typescript
interface OrderResult {
  success: true;
  order: OrderDTO;
  confirmationNumber: string;
}
```

### Output (Failure)
```typescript
interface OrderFailure {
  success: false;
  error: {
    code: string;
    message: string;
    invalidItems?: string[];  // If items unavailable
  };
}
```

### Preconditions
- Customer must exist
- All product IDs must be valid
- All items must be in stock
- Payment method must be valid

### Side Effects
- Creates order in database
- Reserves inventory
- Initiates payment processing
- Sends confirmation email
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Interface too broad | Exposing too many methods | Apply ISP, split into focused interfaces |
| Inconsistent DTOs | Different shapes for same data | Standardize DTO definitions |
| Missing error codes | Errors not categorized | Create error code taxonomy |
| Breaking changes | Interface modified incompatibly | Follow versioning rules |
| Leaky abstractions | Internal details in interface | Hide implementation, expose intent |

## Related Operations

- [op-identify-module-boundaries.md](op-identify-module-boundaries.md) - Define boundaries first
- [op-apply-solid-principles.md](op-apply-solid-principles.md) - Apply ISP to interfaces
- [op-manage-module-dependencies.md](op-manage-module-dependencies.md) - Handle inter-module dependencies
