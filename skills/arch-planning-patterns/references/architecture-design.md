# Architecture Design: Creating Your System Blueprint

## Table of Contents

1. [What is Architecture Design?](#what-is-architecture-design)
2. [Architecture Design in Five Steps](#architecture-design-in-five-steps)
   - [Step 1: Identify System Components](#step-1-identify-system-components)
   - [Step 2: Define Component Responsibilities](#step-2-define-component-responsibilities)
   - [Step 3: Map Data Flows](#step-3-map-data-flows)
   - [Step 4: Identify Component Dependencies](#step-4-identify-component-dependencies)
   - [Step 5: Define Component Interfaces](#step-5-define-component-interfaces)
3. [Architecture Design Document Template](#architecture-design-document-template)
4. [Common Architecture Patterns](#common-architecture-patterns)
   - [Layered Architecture](#layered-architecture)
   - [Service-Based Architecture](#service-based-architecture)
   - [Event-Driven Architecture](#event-driven-architecture)
5. [Architecture Design Checklist](#architecture-design-checklist)
6. [Next Steps](#next-steps)

## What is Architecture Design?

Architecture design is the process of defining the fundamental structure of your system: what components exist, how they connect, what each component does, and how data flows between them.

**Output of this phase**: A complete architecture document that answers these questions:
- What are all the components in the system?
- What are the responsibilities of each component?
- How do components communicate?
- What are the dependencies between components?
- What are the interfaces (contracts) between components?

## Architecture Design in Five Steps

### Step 1: Identify System Components

List every distinct functional element your system needs.

**How to identify components**:
1. Read the project requirements line by line
2. For each requirement, ask: "What component must exist to fulfill this?"
3. Write the component name and its single primary responsibility
4. Group related components into logical domains

**Example**:
```
Requirement: "Users must be able to upload files"
→ Component needed: FileUploadService (responsibility: handle file upload protocol)
→ Secondary component: FileStorageBackend (responsibility: persist files to disk/cloud)
→ Secondary component: FileMetadataDB (responsibility: track file properties and access)
```

**Output**: A list of components, each with:
- Name (concrete noun, singular: UserAuthenticator, not Users or Authentication)
- Primary responsibility (one sentence describing what it does)
- Scope (what it is NOT responsible for - be explicit about boundaries)

### Step 2: Define Component Responsibilities

For each component, write a detailed responsibility statement.

**Template for each component**:
```
Component: [Name]
Responsibility: [What it does in 1-2 sentences]

Inputs:
  - [Data type] from [source]
  - [Data type] from [source]

Outputs:
  - [Data type] to [destination]
  - [Data type] to [destination]

NOT responsible for:
  - [Thing 1 - be explicit about boundaries]
  - [Thing 2]

Examples of what it handles:
  - [Concrete example]
  - [Concrete example]
```

**Example**:
```
Component: AuthenticationTokenValidator
Responsibility: Validates that incoming request contains a valid authentication token
and has not expired.

Inputs:
  - HTTP request with Authorization header from APIGateway
  - Authentication rules from SecurityConfigDB

Outputs:
  - Boolean (true if valid, false if invalid) to APIGateway
  - Reject reason string (if invalid) to LoggingService

NOT responsible for:
  - Creating tokens (that is TokenGenerator's job)
  - Storing tokens (that is TokenStore's job)
  - Deciding authorization rules (that is PolicyEngine's job)

Examples of what it handles:
  - Validating JWT tokens and checking expiration time
  - Checking token signature matches stored secret
  - Rejecting requests with malformed or missing tokens
```

### Step 3: Map Data Flows

Draw (or describe) how data moves between components.

**How to map data flows**:
1. Pick a common use case (example: "user logs in")
2. Trace which components are involved, in order
3. For each component-to-component connection, write:
   - What data is passed
   - What format (JSON, binary, etc.)
   - What the receiving component does with it
   - What is sent back

**Example data flow for "User Login"**:
```
1. User submits credentials
   → APIGateway receives HTTP POST request
   → sends {username, password} to CredentialValidator

2. CredentialValidator checks credentials
   → queries UserDB for user record
   → UserDB returns {user_id, password_hash, salt}
   → CredentialValidator computes hash and compares
   → sends {user_id, valid: true/false} back to APIGateway

3. APIGateway receives validation result
   → if valid: forwards user_id to TokenGenerator
   → if invalid: returns 401 Unauthorized to user

4. TokenGenerator creates token
   → generates JWT token with user_id
   → stores token in TokenStore
   → sends token back to APIGateway

5. APIGateway sends token to user
   → returns 200 OK with {token, expires_at} to user browser
```

**Document these flows as**:
- Numbered sequence lists (not diagrams, be explicit)
- For each step: originating component → receiving component → action → response
- Include error cases (what happens if something fails at this step)

### Step 4: Identify Component Dependencies

List what each component requires from other components to function.

**Dependency template**:
```
Component: [Name]

Direct dependencies (must exist):
  - [Component name]: for [specific purpose]
  - [Component name]: for [specific purpose]

Optional dependencies (enhances functionality):
  - [Component name]: enables [feature]

Dependency ordering (must initialize in this order):
  1. [Component A] - needed before anything else
  2. [Component B] - depends on A
  3. [Component C] - depends on A and B
```

**Example**:
```
Component: AuthenticationMiddleware

Direct dependencies (must exist):
  - AuthenticationTokenValidator: to validate each request token
  - LoggingService: to record authentication events
  - ConfigurationService: to read which endpoints require auth

Optional dependencies:
  - MetricsCollector: to track auth success/failure rates
  - SlackNotifier: to alert on suspicious auth patterns

Dependency ordering:
  1. ConfigurationService - read auth rules
  2. LoggingService - initialize logging
  3. AuthenticationTokenValidator - validate tokens
  4. AuthenticationMiddleware - use all above
```

### Step 5: Define Component Interfaces

For each component, describe how other components will interact with it.

**Interface definition template**:
```
Component: [Name]

Interface method 1: [method_name]
  Input: {field: type, field: type, ...}
  Output: {field: type, field: type, ...}
  Behavior: [what happens when called]
  Errors: [list of possible error conditions and responses]

Interface method 2: [method_name]
  Input: {field: type, field: type, ...}
  Output: {field: type, field: type, ...}
  Behavior: [what happens when called]
  Errors: [list of possible error conditions and responses]

Contracts (things callers must always do):
  - [Requirement: always provide X]
  - [Requirement: do not call method A before method B]

Guarantees (things this component always does):
  - [Guarantee: response time under 100ms]
  - [Guarantee: never returns partial data]
```

**Example**:
```
Component: UserProfileService

Interface method 1: getProfile(user_id)
  Input: {user_id: string (UUID)}
  Output: {user_id, name, email, created_at, profile_picture_url}
  Behavior: Retrieves user profile from database, returns all fields
  Errors:
    - UserNotFound (404) if user_id does not exist
    - DatabaseError (500) if database is unreachable

Interface method 2: updateProfile(user_id, updates)
  Input: {user_id: string (UUID), updates: {name?: string, email?: string, picture?: file}}
  Output: {success: boolean, updated_fields: string[], timestamp: datetime}
  Behavior: Updates specified fields only, overwrites existing values
  Errors:
    - UserNotFound (404) if user_id does not exist
    - InvalidEmail (400) if email format is wrong
    - FileTooLarge (413) if profile picture exceeds 5MB

Contracts:
  - Caller must authenticate before calling these methods
  - Caller must provide valid user_id (cannot be null)

Guarantees:
  - Response time under 200ms for getProfile
  - All profile data is consistent (no partial updates)
  - Email uniqueness is enforced across all users
```

## Architecture Design Document Template

Create a document with these sections:

```
# System Architecture

## 1. Component Inventory
[Table listing all components with descriptions]

## 2. Component Responsibilities
[Section 2 output: responsibility statements for each component]

## 3. Data Flow Diagrams
[Section 3 output: flows for major use cases]

## 4. Dependency Graph
[Section 4 output: dependency ordering]

## 5. Component Interfaces
[Section 5 output: interface definitions]

## 6. Design Decisions
[Why you chose this architecture]

## 7. Assumptions
[What you are assuming to be true]

## 8. Constraints
[What limitations this architecture has]
```

## Common Architecture Patterns

### Layered Architecture
Components organized in horizontal layers:
- Presentation Layer (user interfaces)
- Application Layer (business logic)
- Persistence Layer (data storage)

**Use when**: You have clear separation between UI, logic, and data concerns

### Service-Based Architecture
Components organized as independent services:
- Each service owns its data
- Services communicate via defined interfaces
- Loosely coupled, highly autonomous

**Use when**: You need independent deployment, scaling, or team ownership

### Event-Driven Architecture
Components communicate through events:
- Components emit events when state changes
- Other components react to events
- Asynchronous communication decouples components

**Use when**: You have real-time requirements or complex state synchronization

## Architecture Design Checklist

- ☐ Every component has a single, clearly-defined responsibility
- ☐ Every component is named with a concrete, singular noun
- ☐ Data flows are documented with concrete examples
- ☐ All dependencies between components are listed
- ☐ Component interfaces define inputs, outputs, and errors
- ☐ Architecture decisions are justified in writing
- ☐ Assumptions are explicit and documented
- ☐ At least one use-case flow has been fully traced
- ☐ Stakeholders have reviewed and approved the architecture

## Next Steps

Once your architecture design is complete and approved:
1. Move to Risk Identification (`risk-identification.md`) to identify what could go wrong
2. Use the architecture as the foundation for Roadmap Creation
3. Do not begin implementation until architecture is validated by stakeholders

---

**Related**: See `step-by-step-procedures.md` for the context of where architecture design fits in the full planning process.
