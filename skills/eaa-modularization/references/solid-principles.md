---
name: solid-principles
description: Detailed guide to SOLID principles for modular system design, covering Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion principles with examples
version: 1.0.0
---

# SOLID Principles for Modularization

## Table of Contents

- [Overview](#overview)
- [The Five SOLID Principles](#the-five-solid-principles)
  - [1. Single Responsibility Principle (SRP)](#1-single-responsibility-principle-srp)
  - [2. Open/Closed Principle (OCP)](#2-openclosed-principle-ocp)
  - [3. Liskov Substitution Principle (LSP)](#3-liskov-substitution-principle-lsp)
  - [4. Interface Segregation Principle (ISP)](#4-interface-segregation-principle-isp)
  - [5. Dependency Inversion Principle (DIP)](#5-dependency-inversion-principle-dip)
- [Applying SOLID to Module Boundaries](#applying-solid-to-module-boundaries)
  - [Step 1: Identify Responsibilities (SRP)](#step-1-identify-responsibilities-srp)
  - [Step 2: Design Extension Points (OCP)](#step-2-design-extension-points-ocp)
  - [Step 3: Define Contracts (LSP)](#step-3-define-contracts-lsp)
  - [Step 4: Minimize API Surface (ISP)](#step-4-minimize-api-surface-isp)
  - [Step 5: Invert Dependencies (DIP)](#step-5-invert-dependencies-dip)
- [Validation Checklist](#validation-checklist)
- [Common Violations and Fixes](#common-violations-and-fixes)
- [Summary](#summary)

## Overview

SOLID principles are five design principles that guide the creation of maintainable, scalable, and modular software systems. When applied to modularization, they help ensure modules are cohesive, loosely coupled, and easy to understand.

## The Five SOLID Principles

### 1. Single Responsibility Principle (SRP)

**Definition:** A module should have one, and only one, reason to change.

**Application to Modules:**
- Each module should address a single concern or responsibility
- Changes to one aspect of the system should only affect one module
- If a module handles multiple responsibilities, split it into focused modules

**Example - E-Commerce:**
```
BAD:
OrderModule
- Process orders
- Send email notifications
- Generate invoices
- Update inventory

GOOD:
OrderProcessingModule - Process orders only
NotificationModule - Send emails only
InvoiceModule - Generate invoices only
InventoryModule - Update stock levels only
```

**Signs of SRP Violation:**
- Module name contains "And" or "Manager"
- Multiple teams need to modify the same module
- Changes in unrelated features affect the same module
- Module has many imports from different domains

**Applying SRP:**
1. List all responsibilities of the current module
2. Group related responsibilities
3. Extract each group into a separate module
4. Define clear interfaces between new modules

### 2. Open/Closed Principle (OCP)

**Definition:** Modules should be open for extension but closed for modification.

**Application to Modules:**
- Modules should expose extension points (interfaces, hooks, plugins)
- Adding new functionality should not require changing existing module code
- Use dependency injection to allow behavior customization

**Example - Payment Processing:**
```
BAD:
PaymentModule:
  if payment_method == "credit_card":
    process_credit_card()
  elif payment_method == "paypal":
    process_paypal()
  # Adding new method requires modifying this code

GOOD:
PaymentModule:
  register_processor(payment_type, processor_interface)
  process_payment(payment_type, data)

PaymentProcessors:
  CreditCardProcessor(implements ProcessorInterface)
  PayPalProcessor(implements ProcessorInterface)
  # Adding new processor doesn't modify PaymentModule
```

**Extension Mechanisms:**
- Plugin architectures
- Strategy pattern
- Dependency injection
- Event-driven hooks

### 3. Liskov Substitution Principle (LSP)

**Definition:** Derived modules should be substitutable for their base modules without altering correctness.

**Application to Modules:**
- Module interfaces should be implemented consistently
- Swapping module implementations should not break consumers
- Contract guarantees must be preserved

**Example - Storage Modules:**
```
BAD:
StorageInterface:
  save(key, value) -> void

LocalStorageModule:
  save(key, value) -> void  # Always succeeds

CloudStorageModule:
  save(key, value) -> void  # Throws exception on network error
  # Violates LSP - different failure modes

GOOD:
StorageInterface:
  save(key, value) -> Result[Success, Error]

LocalStorageModule:
  save(key, value) -> Result  # Returns error on disk full

CloudStorageModule:
  save(key, value) -> Result  # Returns error on network failure
  # Both honor contract - caller handles Result
```

**LSP Compliance Checklist:**
- Return types match interface
- Exception contracts are consistent
- Performance characteristics are documented
- Side effects are predictable

### 4. Interface Segregation Principle (ISP)

**Definition:** Clients should not be forced to depend on interfaces they don't use.

**Application to Modules:**
- Module APIs should be small and focused
- Split large interfaces into role-specific interfaces
- Avoid "fat" module interfaces with many methods

**Example - User Module:**
```
BAD:
UserModule exposes:
  - authenticate()
  - register()
  - updateProfile()
  - deleteAccount()
  - generateReport()
  - exportData()

# Authentication service needs only authenticate(),
# but depends on entire interface

GOOD:
AuthenticationInterface:
  - authenticate()

RegistrationInterface:
  - register()

ProfileInterface:
  - updateProfile()

AccountInterface:
  - deleteAccount()

ReportingInterface:
  - generateReport()
  - exportData()

# Each consumer depends only on needed interface
```

**Benefits:**
- Reduces coupling between modules
- Easier to test (fewer methods to mock)
- Clearer separation of concerns
- Enables independent evolution

**Applying ISP:**
1. Analyze which methods each consumer actually uses
2. Group methods by consumer role
3. Extract role-specific interfaces
4. Module implements multiple focused interfaces

### 5. Dependency Inversion Principle (DIP)

**Definition:** High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Application to Modules:**
- Modules depend on interfaces, not concrete implementations
- Dependency direction flows toward stability
- Core business logic is independent of infrastructure

**Example - Order Processing:**
```
BAD:
OrderModule -> PostgreSQLRepository (concrete)
OrderModule -> SmtpEmailService (concrete)
# Core business logic depends on infrastructure

GOOD:
OrderModule -> RepositoryInterface (abstraction)
OrderModule -> EmailServiceInterface (abstraction)

PostgreSQLRepository implements RepositoryInterface
SmtpEmailService implements EmailServiceInterface
# Core logic depends only on abstractions
# Infrastructure implements interfaces
```

**Dependency Injection:**
- Constructor injection: Pass dependencies via constructor
- Setter injection: Configure dependencies after creation
- Interface injection: Dependencies provide injection method

**Benefits:**
- Modules can be tested with mocks
- Infrastructure can be swapped without changing business logic
- Parallel development of modules
- Easier to understand module responsibilities

## Applying SOLID to Module Boundaries

### Step 1: Identify Responsibilities (SRP)
- List all functions/classes in proposed module
- Group by responsibility
- Each group becomes a module candidate

### Step 2: Design Extension Points (OCP)
- Identify variation points
- Define interfaces for variable behavior
- Plan plugin/strategy mechanisms

### Step 3: Define Contracts (LSP)
- Specify interface contracts
- Document error handling
- Define performance expectations
- Ensure implementations honor contracts

### Step 4: Minimize API Surface (ISP)
- For each module consumer, list required operations
- Group operations by consumer role
- Create focused interfaces per role
- Module implements multiple role interfaces

### Step 5: Invert Dependencies (DIP)
- Identify module dependencies
- Define abstraction interfaces
- Inject concrete implementations
- Ensure dependency direction is correct

## Validation Checklist

Use this checklist to verify SOLID compliance:

**Single Responsibility:**
- [ ] Module has one clear reason to change
- [ ] Module name clearly states its purpose
- [ ] All code in module relates to that purpose

**Open/Closed:**
- [ ] New features can be added without modifying module
- [ ] Extension points are defined (interfaces, events, plugins)
- [ ] Module behavior is customizable via dependency injection

**Liskov Substitution:**
- [ ] All implementations of module interface are interchangeable
- [ ] Error handling is consistent across implementations
- [ ] Contracts are documented and honored

**Interface Segregation:**
- [ ] Module API is small and focused
- [ ] Consumers depend only on methods they use
- [ ] Large interfaces are split into role-specific interfaces

**Dependency Inversion:**
- [ ] Module depends on abstractions, not concrete classes
- [ ] Business logic is independent of infrastructure
- [ ] Dependencies are injected, not hard-coded

## Common Violations and Fixes

| Violation | Symptom | Fix |
|-----------|---------|-----|
| SRP violation | Module has multiple reasons to change | Split into focused modules |
| OCP violation | Must modify module to add features | Add extension points |
| LSP violation | Swapping implementations breaks system | Ensure consistent contracts |
| ISP violation | Consumers depend on unused methods | Split into role interfaces |
| DIP violation | Core logic depends on infrastructure | Introduce abstractions |

## Summary

SOLID principles are the foundation of good modularization:

1. **SRP** ensures modules are focused
2. **OCP** makes modules extensible
3. **LSP** makes modules substitutable
4. **ISP** makes module APIs minimal
5. **DIP** makes modules independent

Apply these principles iteratively as you design and refactor module boundaries.
