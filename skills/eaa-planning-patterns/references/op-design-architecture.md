---
operation: design-architecture
procedure: proc-create-design
workflow-instruction: Step 7 - Design Document Creation
parent-skill: eaa-planning-patterns
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Design System Architecture

## When to Use

Use this operation when:
- Starting a new project and need to plan its structure
- Designing the structural blueprint of a system
- Defining system components and their responsibilities
- Mapping data flows between components
- Identifying component dependencies and interfaces

## Prerequisites

- Clear understanding of project scope and requirements
- Stakeholder requirements documented
- Domain knowledge or access to domain experts
- Write access to planning output directories

## Procedure

### Step 1: Identify System Components

List all the major building blocks of your system.

**Questions to answer:**
- What are the major functional areas?
- What services or modules will exist?
- What external systems will integrate?
- What databases or storage will be needed?

**Document format:**
```markdown
## System Components

| Component | Type | Description |
|-----------|------|-------------|
| auth-service | Service | Handles user authentication |
| user-store | Database | Stores user profiles and credentials |
| api-gateway | Gateway | Routes and validates API requests |
```

### Step 2: Define Component Responsibilities

For each component, define its single responsibility.

**Apply Single Responsibility Principle:**
- Each component should have one reason to change
- Responsibilities should not overlap
- If a component has multiple responsibilities, split it

**Document format:**
```markdown
### Component: auth-service

**Responsibility:** Authenticate users and issue tokens

**Does:**
- Validates credentials against user-store
- Issues JWT tokens on successful authentication
- Validates existing tokens
- Handles token refresh

**Does NOT:**
- Store user data (user-store responsibility)
- Route requests (api-gateway responsibility)
- Manage user profiles (profile-service responsibility)
```

### Step 3: Map Data Flows

Document how data moves between components.

**Questions to answer:**
- What data enters the system?
- What transformations occur?
- What data exits the system?
- What data is stored?

**Document format:**
```markdown
## Data Flows

### Login Flow
1. Client -> api-gateway: Login request (email, password)
2. api-gateway -> auth-service: Validated credentials
3. auth-service -> user-store: Query user by email
4. user-store -> auth-service: User record
5. auth-service -> api-gateway: JWT token
6. api-gateway -> Client: Token response
```

### Step 4: Identify Component Dependencies

Create a dependency map showing which components depend on others.

**Rules:**
- Dependencies should flow in one direction
- Avoid circular dependencies
- Core services should have fewer dependencies

**Document format:**
```markdown
## Dependency Graph

api-gateway
  └── auth-service
        └── user-store
  └── profile-service
        └── user-store
```

### Step 5: Define Component Interfaces

Specify how components communicate with each other.

**Document format:**
```markdown
### Interface: auth-service

**Endpoint:** POST /auth/login
**Input:**
```json
{
  "email": "string",
  "password": "string"
}
```
**Output:**
```json
{
  "token": "string",
  "expires_at": "timestamp"
}
```
**Errors:**
- 401: Invalid credentials
- 400: Missing required fields
```

### Step 6: Select Design Patterns

Choose architectural patterns that fit your requirements.

**Common patterns:**
| Pattern | Use When |
|---------|----------|
| Layered | Clear separation of concerns needed |
| Microservices | Independent deployment required |
| Event-Driven | Loose coupling, async processing |
| CQRS | Separate read/write patterns |
| Hexagonal | Testability and port/adapter flexibility |

### Step 7: Create Architecture Document

Compile all findings into the architecture design document.

```bash
python scripts/eaa_architecture_generator.py --output docs_dev/design/architecture.md
```

## Checklist

Copy this checklist and track your progress:

- [ ] List all system components
- [ ] Define single responsibility for each component
- [ ] Map all data flows between components
- [ ] Create dependency graph
- [ ] Identify circular dependencies (none allowed)
- [ ] Define interfaces for each component
- [ ] Select architectural pattern(s)
- [ ] Create architecture diagram
- [ ] Write architecture design document
- [ ] Have stakeholders review architecture

## Examples

### Example: E-Commerce Authentication System Architecture

```markdown
# Authentication System Architecture

## Components

| Component | Type | Responsibility |
|-----------|------|----------------|
| api-gateway | Gateway | Request routing and validation |
| auth-service | Service | User authentication and token management |
| user-store | Database | User credential storage |
| token-cache | Cache | Token validation cache |
| audit-logger | Service | Authentication event logging |

## Data Flows

### Login Flow
1. Client -> api-gateway: Login request
2. api-gateway -> auth-service: Validated credentials
3. auth-service -> user-store: Query user
4. auth-service -> token-cache: Store token
5. auth-service -> audit-logger: Log event
6. api-gateway -> Client: Token response

## Dependency Graph

api-gateway
  └── auth-service
        ├── user-store
        ├── token-cache
        └── audit-logger

## Architectural Pattern: Hexagonal

Selected hexagonal architecture for:
- Testability: Easy to mock external dependencies
- Flexibility: Can swap database implementations
- Clean boundaries: Ports and adapters pattern
```

### Example: Microservices Pattern

```markdown
## Architectural Pattern: Microservices

### Service Boundaries
- auth-service: Authentication domain
- user-service: User profile domain
- order-service: Order management domain
- payment-service: Payment processing domain

### Communication
- Synchronous: REST APIs for queries
- Asynchronous: Event bus for commands

### Data Ownership
Each service owns its database:
- auth-service -> auth-db
- user-service -> user-db
- order-service -> order-db
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Circular dependency detected | Components depend on each other | Introduce abstraction or split component |
| Component has multiple responsibilities | Violation of SRP | Split into focused components |
| Unclear data flow | Missing documentation | Trace actual data path step by step |
| Interface mismatch | Input/output not aligned | Coordinate interface definitions between teams |
| Pattern mismatch | Wrong pattern for requirements | Re-evaluate requirements against pattern capabilities |

## Related Operations

- [op-identify-risks.md](op-identify-risks.md) - Identify risks after architecture design
- [op-create-roadmap.md](op-create-roadmap.md) - Create roadmap based on architecture
- [op-plan-implementation.md](op-plan-implementation.md) - Plan implementation tasks
