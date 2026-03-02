---
operation: decompose-monolith
procedure: proc-decompose-design
workflow-instruction: Step 10 - Design Decomposition
parent-skill: eaa-modularization
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Decompose Monolith (Strangler Fig Pattern)


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Understand the Strangler Fig Pattern](#step-1-understand-the-strangler-fig-pattern)
- [Strangler Fig Stages](#strangler-fig-stages)
  - [Step 2: Create Extraction Priority List](#step-2-create-extraction-priority-list)
- [Extraction Priority](#extraction-priority)
  - [Step 3: Design the Facade/Router](#step-3-design-the-facaderouter)
- [Facade Routing Configuration](#facade-routing-configuration)
  - [Step 4: Extract One Module at a Time](#step-4-extract-one-module-at-a-time)
- [Data Migration Strategy](#data-migration-strategy)
  - [Option A: Shared Database (Temporary)](#option-a-shared-database-temporary)
  - [Option B: Data Copy (For Read-Heavy)](#option-b-data-copy-for-read-heavy)
  - [Option C: Database Split (Clean Break)](#option-c-database-split-clean-break)
- [Traffic Shift Schedule](#traffic-shift-schedule)
  - [Step 5: Monitor and Validate](#step-5-monitor-and-validate)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example: E-Commerce Monolith Decomposition Plan](#example-e-commerce-monolith-decomposition-plan)
- [Current State](#current-state)
- [Target State](#target-state)
- [Phase 1: Foundation (Weeks 1-4)](#phase-1-foundation-weeks-1-4)
- [Phase 2: Auth (Weeks 5-8)](#phase-2-auth-weeks-5-8)
- [Phase 3: Catalog (Weeks 9-14)](#phase-3-catalog-weeks-9-14)
- [Phase 4-7: Remaining Modules (Weeks 15-30)](#phase-4-7-remaining-modules-weeks-15-30)
- [Phase 8: Retirement (Weeks 31-32)](#phase-8-retirement-weeks-31-32)
- [Risk Mitigation](#risk-mitigation)
  - [Example: Module Extraction Checklist](#example-module-extraction-checklist)
- [Pre-Extraction](#pre-extraction)
- [Infrastructure](#infrastructure)
- [Implementation](#implementation)
- [Data Migration](#data-migration)
- [Traffic Shift](#traffic-shift)
- [Cleanup](#cleanup)
- [Error Handling](#error-handling)
- [Related Operations](#related-operations)

## When to Use

Use this operation when:
- Migrating a monolithic application to modular architecture
- Breaking up a large codebase into independent modules
- Preparing for microservices migration
- Reducing coupling in an existing system
- Enabling independent deployment of components

## Prerequisites

- Module boundaries have been identified
- Circular dependencies have been detected and resolved
- Module APIs have been designed
- Understanding of the monolith's data model
- Stakeholder buy-in for incremental migration

## Procedure

### Step 1: Understand the Strangler Fig Pattern

The Strangler Fig pattern gradually replaces parts of a system while keeping it running.

**Pattern Principles:**
1. Never rewrite everything at once
2. New functionality goes to new modules
3. Gradually migrate existing functionality
4. Maintain backward compatibility during migration
5. Remove old code only after new code is proven

```markdown
## Strangler Fig Stages

Stage 1: Facade
┌─────────────────────────────────────────────┐
│                  Facade                      │
│  Routes all traffic to monolith             │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│               MONOLITH                       │
│  All functionality here                      │
└─────────────────────────────────────────────┘

Stage 2: First Module Extracted
┌─────────────────────────────────────────────┐
│                  Facade                      │
│  Routes auth to new module, rest to mono    │
└──────────┬─────────────────────┬────────────┘
           ▼                     ▼
┌──────────────────┐  ┌─────────────────────────┐
│   AuthModule     │  │      MONOLITH           │
│   (new)          │  │  (auth removed)         │
└──────────────────┘  └─────────────────────────┘

Stage N: Monolith Gone
┌─────────────────────────────────────────────┐
│               API Gateway                    │
│  Routes to appropriate modules              │
└───┬────────┬────────┬────────┬────────┬─────┘
    ▼        ▼        ▼        ▼        ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│ Auth   ││ Users  ││ Orders ││Products││Payment │
└────────┘└────────┘└────────┘└────────┘└────────┘
```

### Step 2: Create Extraction Priority List

Prioritize which modules to extract first.

**Prioritization Criteria:**
| Criterion | Weight | Description |
|-----------|--------|-------------|
| Independence | High | Modules with fewer dependencies first |
| Business Value | High | High-change or high-revenue areas |
| Risk | Medium | Low-risk extractions first |
| Team Readiness | Medium | Teams ready to own modules |
| Technical Debt | Low | Legacy code that needs rewriting |

**Priority List Template:**
```markdown
## Extraction Priority

| Priority | Module | Dependencies | Risk | Effort | Value |
|----------|--------|--------------|------|--------|-------|
| 1 | AuthModule | 1 | Low | Medium | High |
| 2 | NotificationModule | 0 | Low | Low | Medium |
| 3 | CatalogModule | 2 | Medium | High | High |
| 4 | OrderModule | 4 | High | High | High |
| 5 | PaymentModule | 3 | High | Medium | High |
```

### Step 3: Design the Facade/Router

Create a routing layer that directs traffic.

**Facade Responsibilities:**
- Route requests to appropriate module (new or monolith)
- Handle authentication consistently
- Translate between old and new APIs if needed
- Log for migration monitoring

```markdown
## Facade Routing Configuration

```yaml
routes:
  # Already migrated
  - path: /api/v1/auth/*
    target: auth-service
    status: migrated

  # In migration
  - path: /api/v1/products/*
    target: product-service
    status: in-migration
    feature_flag: products_v2
    fallback: monolith

  # Not yet migrated
  - path: /api/v1/orders/*
    target: monolith
    status: pending
```
```

### Step 4: Extract One Module at a Time

Follow this process for each module extraction.

**Extraction Steps:**

**4.1: Create New Module Shell**
```bash
# Create module directory structure
mkdir -p modules/auth/{src,tests,migrations}

# Initialize module
cd modules/auth && npm init
```

**4.2: Implement Module with Same Interface**
```typescript
// New module implements same interface as monolith code
interface IAuthService {
  login(email: string, password: string): Promise<AuthResult>;
  logout(token: string): Promise<void>;
  validateToken(token: string): Promise<TokenValidation>;
}
```

**4.3: Set Up Database Migration**
```markdown
## Data Migration Strategy

### Option A: Shared Database (Temporary)
- New module uses same database as monolith
- Use during transition period
- Plan for data separation later

### Option B: Data Copy (For Read-Heavy)
- Copy relevant data to new module's database
- Sync via events or CDC
- Module owns its data copy

### Option C: Database Split (Clean Break)
- New module has own database from start
- Migrate data once
- Preferred for independent modules
```

**4.4: Deploy Behind Feature Flag**
```typescript
// Facade routes based on feature flag
if (featureFlags.isEnabled('auth_v2', user)) {
  return authService.login(credentials);
} else {
  return monolith.authLogin(credentials);
}
```

**4.5: Gradually Shift Traffic**
```markdown
## Traffic Shift Schedule

| Day | New Module | Monolith | Notes |
|-----|------------|----------|-------|
| 1 | 1% | 99% | Initial canary |
| 3 | 10% | 90% | Expand if metrics OK |
| 7 | 50% | 50% | Half traffic |
| 14 | 90% | 10% | Near complete |
| 21 | 100% | 0% | Full migration |
```

**4.6: Remove Old Code**
```bash
# Only after 100% traffic and stability period
# Remove old code from monolith
git rm -r src/auth/
git commit -m "Remove auth code - migrated to auth-service"
```

### Step 5: Monitor and Validate

Track migration health continuously.

**Key Metrics:**
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Error Rate | <0.1% | >0.5% |
| Latency p99 | <200ms | >500ms |
| Feature Parity | 100% | <100% |
| Data Consistency | 100% | <99.9% |

## Checklist

Copy this checklist and track your progress:

- [ ] **Preparation**
  - [ ] Module boundaries identified
  - [ ] APIs designed
  - [ ] Dependencies mapped
  - [ ] Circular dependencies resolved
- [ ] **Planning**
  - [ ] Create extraction priority list
  - [ ] Design facade/router
  - [ ] Plan database strategy
  - [ ] Define success metrics
- [ ] **Per Module Extraction**
  - [ ] Create module shell
  - [ ] Implement interface
  - [ ] Set up data migration
  - [ ] Deploy behind feature flag
  - [ ] Shift traffic gradually (1%→10%→50%→90%→100%)
  - [ ] Monitor metrics
  - [ ] Remove old code after stability period
- [ ] **Completion**
  - [ ] All modules extracted
  - [ ] Monolith retired
  - [ ] Documentation updated

## Examples

### Example: E-Commerce Monolith Decomposition Plan

```markdown
# Decomposition Plan: E-Commerce Platform

## Current State
- Single Node.js monolith (150k LOC)
- PostgreSQL database (45 tables)
- 12 developers
- Deploy twice per week

## Target State
- 7 independent modules
- Module-owned databases
- 3-4 developers per module
- Deploy on demand per module

## Phase 1: Foundation (Weeks 1-4)
**Goal:** Set up infrastructure and extract first module

**Week 1-2:**
- [ ] Set up API Gateway/Facade
- [ ] Set up feature flag service
- [ ] Set up monitoring dashboards
- [ ] Define shared types package

**Week 3-4:**
- [ ] Extract NotificationModule (0 dependencies)
- [ ] Traffic shift: 1% → 100%
- [ ] Remove old notification code

## Phase 2: Auth (Weeks 5-8)
**Goal:** Extract authentication

- [ ] Create AuthModule
- [ ] Implement OAuth, session management
- [ ] Migrate users table to auth-db
- [ ] Traffic shift over 2 weeks
- [ ] Remove old auth code

## Phase 3: Catalog (Weeks 9-14)
**Goal:** Extract product catalog

- [ ] Create CatalogModule
- [ ] Implement product CRUD, search
- [ ] Split products/categories tables
- [ ] Traffic shift over 3 weeks
- [ ] Remove old catalog code

## Phase 4-7: Remaining Modules (Weeks 15-30)
- Orders (3 weeks)
- Payments (3 weeks)
- Customers (2 weeks)
- Shipping (2 weeks)

## Phase 8: Retirement (Weeks 31-32)
- [ ] Verify no traffic to monolith
- [ ] Archive monolith codebase
- [ ] Decommission monolith servers
- [ ] Celebration!

## Risk Mitigation
| Risk | Mitigation |
|------|------------|
| Data loss during migration | Run dual-write during transition |
| Feature regression | Comprehensive integration tests |
| Performance degradation | Canary deployments, instant rollback |
| Team disruption | Gradual handover, documentation |
```

### Example: Module Extraction Checklist

```markdown
# Extraction Checklist: AuthModule

## Pre-Extraction
- [x] Module boundary defined
- [x] API interface designed
- [x] Dependencies mapped (UserModule only)
- [x] No circular dependencies
- [x] Database strategy: separate auth-db

## Infrastructure
- [x] Module repository created
- [x] CI/CD pipeline configured
- [x] Monitoring/logging set up
- [x] Feature flag created: auth_v2

## Implementation
- [x] Core authentication logic
- [x] Session management
- [x] Token generation/validation
- [x] Unit tests (95% coverage)
- [x] Integration tests

## Data Migration
- [x] Migration script written
- [x] Dry run completed
- [x] Rollback plan documented
- [ ] Production migration (scheduled)

## Traffic Shift
- [x] 1% canary: 2 days, no issues
- [x] 10% traffic: 3 days, latency OK
- [ ] 50% traffic: in progress
- [ ] 90% traffic
- [ ] 100% traffic

## Cleanup
- [ ] Remove auth code from monolith
- [ ] Archive old auth tables
- [ ] Update documentation
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Feature regression | Incomplete implementation | Add missing functionality before traffic shift |
| Data inconsistency | Migration error | Run data reconciliation, fix sync |
| Performance worse | New module slower | Optimize, or rollback traffic |
| Circular dependency discovered | Analysis missed it | Pause extraction, resolve dependency |
| Team confusion | Unclear ownership | Update CODEOWNERS, communicate |

## Related Operations

- [op-identify-module-boundaries.md](op-identify-module-boundaries.md) - Must complete first
- [op-design-module-apis.md](op-design-module-apis.md) - APIs needed before extraction
- [op-detect-circular-dependencies.md](op-detect-circular-dependencies.md) - Must resolve before extraction
- [op-manage-module-dependencies.md](op-manage-module-dependencies.md) - Manage new dependencies
