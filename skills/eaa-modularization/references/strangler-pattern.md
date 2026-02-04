---
name: strangler-pattern
description: Step-by-step guide to breaking up monolithic applications using the Strangler Fig pattern, including incremental migration strategies, routing techniques, and risk mitigation
version: 1.0.0
---

# Breaking Up Monoliths: The Strangler Fig Pattern

## Table of Contents

- [Overview](#overview)
- [Why Strangler Pattern?](#why-strangler-pattern)
  - [The Big Rewrite Problem](#the-big-rewrite-problem)
  - [Strangler Pattern Benefits](#strangler-pattern-benefits)
- [The Strangler Fig Pattern](#the-strangler-fig-pattern)
  - [Pattern Overview](#pattern-overview)
  - [Five Stages](#five-stages)
- [Step-by-Step Monolith Decomposition](#step-by-step-monolith-decomposition)
  - [Step 1: Identify Extraction Candidate](#step-1-identify-extraction-candidate)
  - [Step 2: Build New Module](#step-2-build-new-module)
  - [Step 3: Route Traffic](#step-3-route-traffic)
  - [Step 4: Monitor and Validate](#step-4-monitor-and-validate)
  - [Step 5: Remove from Monolith](#step-5-remove-from-monolith)
- [Dealing with Dependencies](#dealing-with-dependencies)
  - [Dependency Types](#dependency-types)
  - [Shared Data Strategies](#shared-data-strategies)
- [Risk Mitigation](#risk-mitigation)
  - [Rollback Strategy](#rollback-strategy)
  - [Circuit Breaker](#circuit-breaker)
  - [Gradual Rollout](#gradual-rollout)
- [Module Dependency Graphs](#module-dependency-graphs)
  - [Visualizing Module Extraction](#visualizing-module-extraction)
  - [Dependency Visualization Tool](#dependency-visualization-tool)
- [Strangler Pattern Checklist](#strangler-pattern-checklist)
- [Example: Extracting Authentication](#example-extracting-authentication)
  - [Phase 1: Monolith (Before)](#phase-1-monolith-before)
  - [Phase 2: New Auth Module](#phase-2-new-auth-module)
  - [Phase 3: Router](#phase-3-router)
  - [Phase 4: Validation](#phase-4-validation)
  - [Phase 5: Complete](#phase-5-complete)
- [Summary](#summary)

## Overview

The Strangler Fig pattern is a technique for incrementally migrating from a monolithic architecture to a modular or microservices architecture. It's named after strangler fig plants that grow around trees, eventually replacing them.

## Why Strangler Pattern?

### The Big Rewrite Problem

**Anti-Pattern: Big Bang Rewrite**

Replace entire monolith in one massive project:
- High risk (everything breaks at once)
- Long development time (6+ months with no value delivered)
- Feature freeze (can't add features during rewrite)
- Integration surprises (find issues late)

**Success rate: ~20%** (most big rewrites fail or are abandoned)

### Strangler Pattern Benefits

| Benefit | Explanation |
|---------|-------------|
| Low risk | Migrate one piece at a time, rollback if needed |
| Continuous delivery | Ship value incrementally |
| Parallel development | Add features while migrating |
| Early learning | Discover issues early and adjust |
| Minimal disruption | Users see seamless transition |

## The Strangler Fig Pattern

### Pattern Overview

```
Phase 1: Monolith
┌─────────────────┐
│   Monolith      │
│   (All Logic)   │
└─────────────────┘

Phase 2: Intercept and Route
┌─────────────────┐
│   Router/Proxy  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
Monolith   New Module
(Most)     (Feature A)

Phase 3: Gradual Migration
┌─────────────────┐
│   Router/Proxy  │
└────────┬────────┘
         │
    ┌────┴───────┐
    │            │
Monolith   Modules (A,B,C)
(Some)

Phase 4: Complete Migration
┌─────────────────┐
│   Router/Proxy  │
└────────┬────────┘
         │
    Modules (A,B,C,D,E)
    (Monolith gone)
```

### Five Stages

1. **Identify** - Choose functionality to extract
2. **Build** - Implement new module alongside monolith
3. **Route** - Intercept traffic and route to new module
4. **Monitor** - Verify new module works correctly
5. **Remove** - Delete functionality from monolith

## Step-by-Step Monolith Decomposition

### Step 1: Identify Extraction Candidate

**Criteria for Good First Module:**
- Clear boundaries (well-defined inputs/outputs)
- High value (solves real problem)
- Low risk (not mission-critical)
- Minimal dependencies (few connections to monolith)
- Frequent changes (benefits from independent deployment)

**Example Candidates:**
```
E-Commerce Monolith:
✓ GOOD: Product Search (clear API, few dependencies)
✓ GOOD: Email Notifications (external concern, clear interface)
✗ BAD: Order Processing (core logic, many dependencies)
✗ BAD: Authentication (mission-critical, used everywhere)
```

**Analysis Template:**
```markdown
## Extraction Candidate: [Feature Name]

### Boundaries
- Inputs: [What data does it need?]
- Outputs: [What does it return?]
- Dependencies: [What else does it need?]

### Value
- Problem solved: [Why extract this?]
- Benefits: [What improves?]

### Risk
- Risk level: Low / Medium / High
- Mitigation: [How to reduce risk?]

### Dependencies
- Monolith calls: [What does monolith need from this?]
- Calls monolith: [What does this need from monolith?]
```

### Step 2: Build New Module

Build new module **alongside** monolith (not as replacement yet):

```python
# Monolith (existing)
class MonolithProductSearch:
    def search(query: str) -> List[Product]:
        # Old implementation
        pass

# New module (parallel implementation)
class ProductSearchModule:
    def search(query: str) -> SearchResult:
        # New implementation with better features
        pass
```

**Guidelines:**
- Keep both implementations running initially
- New module has same behavior (feature parity)
- New module has better design (improved structure)
- New module is independently deployable

### Step 3: Route Traffic

Introduce a router/proxy to direct traffic:

#### Routing Strategies

**Strategy 1: Feature Flag Routing**

```python
class Router:
    def search_products(query: str):
        if feature_flag('use_new_search'):
            return new_search_module.search(query)
        else:
            return monolith.search(query)
```

**Rollout:**
1. Start: 0% to new module
2. Canary: 5% to new module (test with small traffic)
3. Ramp: 25% → 50% → 100% (gradual rollout)
4. Complete: 100% to new module

**Strategy 2: User-Based Routing**

```python
class Router:
    def search_products(user: User, query: str):
        if user.is_beta_tester():
            return new_search_module.search(query)
        else:
            return monolith.search(query)
```

**Strategy 3: Shadow Routing (Dark Launch)**

```python
class Router:
    def search_products(query: str):
        # Primary: Use monolith
        result = monolith.search(query)

        # Shadow: Call new module (async, don't return result)
        asyncio.create_task(new_search_module.search(query))

        return result  # User sees monolith result
```

**Benefits:** Verify new module behavior without affecting users

#### Routing Implementation

**Option 1: Application-Level Routing**

```python
# In monolith code
from router import Router

router = Router()

@app.route('/search')
def search(query: str):
    return router.search_products(query)
```

**Option 2: API Gateway Routing**

```yaml
# nginx.conf or API Gateway config
location /api/search {
    if ($new_search_enabled) {
        proxy_pass http://search-module:8000;
    } else {
        proxy_pass http://monolith:8080;
    }
}
```

**Option 3: Service Mesh Routing**

```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: product-search
spec:
  http:
  - match:
    - headers:
        x-use-new-search:
          exact: "true"
    route:
    - destination:
        host: search-module
  - route:
    - destination:
        host: monolith
```

### Step 4: Monitor and Validate

**Metrics to Track:**

| Metric | Purpose | Target |
|--------|---------|--------|
| Error rate | Ensure new module is stable | < 0.1% errors |
| Latency | Ensure performance is acceptable | p95 < 200ms |
| Consistency | Compare monolith vs. new module results | > 99% match |
| Resource usage | Ensure efficient resource use | < monolith CPU/memory |

**Validation Techniques:**

**Technique 1: Parallel Run**

```python
def search_products(query: str):
    # Run both
    monolith_result = monolith.search(query)
    module_result = new_search_module.search(query)

    # Compare
    if monolith_result != module_result:
        log_difference(query, monolith_result, module_result)

    # Return monolith result (safe)
    return monolith_result
```

**Technique 2: A/B Testing**

- Split users into groups
- Group A: monolith
- Group B: new module
- Compare user behavior, errors, satisfaction

**Technique 3: Synthetic Testing**

- Run automated tests against both
- Compare results for known inputs
- Verify edge cases

### Step 5: Remove from Monolith

After new module is proven stable:

1. **Route 100% traffic** to new module
2. **Delete monolith code** that was replaced
3. **Remove routing logic** (simplify to direct calls)
4. **Update documentation** and team knowledge

**Before:**
```python
# Routing layer
def search(query: str):
    return router.search_products(query)

# Monolith (to be removed)
class MonolithSearch:
    def search(query: str):
        # Old implementation
        pass

# New module
class SearchModule:
    def search(query: str):
        # New implementation
        pass
```

**After:**
```python
# Direct call (routing removed)
def search(query: str):
    return search_module.search(query)

# Monolith code deleted

# New module (only implementation)
class SearchModule:
    def search(query: str):
        # New implementation
        pass
```

## Dealing with Dependencies

### Dependency Types

**Type 1: Monolith calls new module**

Easy - just route requests:
```python
# In monolith
search_result = search_module.search(query)
```

**Type 2: New module calls monolith**

Temporary - define interface, call monolith via API:
```python
# In new module
class MonolithClient:
    def get_user(user_id: str) -> User:
        response = requests.get(f"{monolith_url}/users/{user_id}")
        return User.from_json(response.json())
```

**Type 3: Shared data**

Challenging - options:
- **Dual writes:** Write to both datastores during transition
- **Database views:** Create view in new module DB that reads from monolith DB
- **Event streaming:** Replicate data via events (Kafka, etc.)

### Shared Data Strategies

#### Strategy 1: Database Federation

Keep single database, but logically separate:

```
Single Database:
- users table (owned by UserModule)
- products table (owned by ProductModule)
- orders table (owned by OrderModule)

Modules query foreign tables via IDs (not joins)
```

#### Strategy 2: Dual Writes

During transition, write to both datastores:

```python
def create_order(order: Order):
    # Write to new module DB
    new_db.orders.insert(order)

    # Write to monolith DB (until migration complete)
    monolith_db.orders.insert(order)
```

#### Strategy 3: Event-Based Replication

Publish events, replicate to module datastores:

```python
# Monolith publishes event
event_bus.publish(OrderCreated(order_id, customer_id, total))

# New module subscribes
@subscribe('OrderCreated')
def handle_order_created(event):
    new_db.orders.insert(Order.from_event(event))
```

## Risk Mitigation

### Rollback Strategy

Always plan for rollback:

```python
# Feature flag with rollback
if feature_flag('use_new_search'):
    try:
        return new_search_module.search(query)
    except Exception as e:
        log_error(e)
        # Automatic rollback to monolith
        return monolith.search(query)
else:
    return monolith.search(query)
```

### Circuit Breaker

Automatically fallback on repeated failures:

```python
class CircuitBreaker:
    def call_with_fallback(primary, fallback):
        if self.is_open():  # Circuit open = too many failures
            return fallback()

        try:
            result = primary()
            self.record_success()
            return result
        except Exception:
            self.record_failure()
            if self.should_open():
                self.open_circuit()
            return fallback()

# Usage
result = circuit_breaker.call_with_fallback(
    primary=lambda: new_search_module.search(query),
    fallback=lambda: monolith.search(query)
)
```

### Gradual Rollout

**Week 1:** 5% traffic → monitor for errors
**Week 2:** 25% traffic → check performance
**Week 3:** 50% traffic → validate at scale
**Week 4:** 100% traffic → full migration

If issues detected at any stage, rollback to previous %.

## Module Dependency Graphs

### Visualizing Module Extraction

**Before Extraction:**
```
Monolith
├── Search (to extract)
├── Users
├── Orders (depends on Search)
└── Products (depends on Search)
```

**Dependency Analysis:**
```
Search depends on:
- Products (to get product data)

Depends on Search:
- Orders (to search products when creating order)
- Users (to show recent searches)
```

**After Extraction:**
```
SearchModule
  ↓ depends on
ProductModule (via API)

OrderModule → SearchModule (via API)
UserModule → SearchModule (via API)

Monolith
├── Users (still here)
├── Orders (still here)
└── Products (still here)
```

### Dependency Visualization Tool

```python
# Generate dependency graph
import graphviz

def generate_dependency_graph():
    dot = graphviz.Digraph()

    # Nodes
    dot.node('Monolith', shape='box')
    dot.node('SearchModule', shape='box', style='filled')
    dot.node('ProductModule', shape='box')

    # Edges
    dot.edge('SearchModule', 'ProductModule', label='uses')
    dot.edge('Monolith', 'SearchModule', label='calls')

    return dot

dot = generate_dependency_graph()
dot.render('dependencies.png')
```

## Strangler Pattern Checklist

For each extraction:

- [ ] **Identify candidate**
  - [ ] Clear boundaries defined
  - [ ] Value proposition documented
  - [ ] Risk assessment complete
  - [ ] Dependencies mapped
- [ ] **Build new module**
  - [ ] Feature parity with monolith
  - [ ] Independently deployable
  - [ ] Proper error handling
  - [ ] Monitoring instrumented
- [ ] **Route traffic**
  - [ ] Router/proxy implemented
  - [ ] Feature flag configured
  - [ ] Rollback plan documented
- [ ] **Monitor**
  - [ ] Error rate tracking
  - [ ] Latency monitoring
  - [ ] Result validation (parallel run or A/B test)
  - [ ] Resource usage monitoring
- [ ] **Remove from monolith**
  - [ ] 100% traffic to new module
  - [ ] Monolith code deleted
  - [ ] Routing simplified
  - [ ] Documentation updated

## Example: Extracting Authentication

### Phase 1: Monolith (Before)

```python
# In monolith
class UserService:
    def authenticate(username, password):
        user = db.users.find_one(username=username)
        if user and check_password(password, user.password_hash):
            return create_session(user)
        raise AuthenticationError()
```

### Phase 2: New Auth Module

```python
# New auth module (parallel)
class AuthModule:
    def authenticate(username, password) -> Result[Session, AuthError]:
        user = self.user_repo.find_by_username(username)
        if not user:
            return Failure(AuthError.USER_NOT_FOUND)

        if not self.password_hasher.verify(password, user.password_hash):
            return Failure(AuthError.INVALID_PASSWORD)

        session = self.session_manager.create(user)
        return Success(session)
```

### Phase 3: Router

```python
# Router with feature flag
class AuthRouter:
    def authenticate(username, password):
        if feature_flag('use_new_auth'):
            result = auth_module.authenticate(username, password)
            match result:
                case Success(session):
                    return session
                case Failure(error):
                    raise AuthenticationError(str(error))
        else:
            return monolith.authenticate(username, password)
```

### Phase 4: Validation

```bash
# Monitor error rates
grafana dashboard: auth-migration
- Monolith auth errors: 0.1%
- New module auth errors: 0.08% ✓ (better)

# A/B test
- Group A (monolith): 10000 requests, 10 failures
- Group B (new module): 10000 requests, 8 failures ✓ (comparable)
```

### Phase 5: Complete

```python
# Router removed - direct call
def authenticate(username, password):
    return auth_module.authenticate(username, password)

# Monolith code deleted
# class UserService: (DELETED)
```

## Summary

**Strangler Fig Pattern Steps:**
1. **Identify** - Choose feature to extract
2. **Build** - Implement new module alongside monolith
3. **Route** - Intercept and route traffic
4. **Monitor** - Validate stability and correctness
5. **Remove** - Delete monolith code

**Key Principles:**
- Incremental migration (not big bang)
- Parallel running (both systems coexist)
- Gradual rollout (5% → 25% → 50% → 100%)
- Continuous validation (monitor, test, compare)
- Rollback capability (always have escape hatch)

**Success Factors:**
- Start with low-risk, high-value features
- Automate routing and monitoring
- Validate thoroughly before full migration
- Document dependencies and contracts
- Celebrate incremental wins

The Strangler Pattern enables safe, incremental migration from monoliths to modular architectures.
