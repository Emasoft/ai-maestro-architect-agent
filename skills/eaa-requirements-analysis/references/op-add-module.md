---
operation: add-module
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Add Module Operation

## When to Use

Use this operation when:
- Defining implementation units for the project
- Breaking down large features into manageable units
- Creating trackable work items (each becomes a GitHub Issue after approval)
- Specifying acceptance criteria for deliverables

## Prerequisites

- [ ] Plan Phase is active
- [ ] Module name is unique (will be converted to kebab-case ID)
- [ ] Acceptance criteria are defined
- [ ] Priority level is determined

## Procedure

### Step 1: Determine Module Properties

Define:
- **Name**: Descriptive name for the module
- **Acceptance Criteria**: What must be true for the module to be complete
- **Priority**: critical, high, medium (default), or low

### Step 2: Add the Module

```bash
/add-requirement module "module-name" --criteria "Acceptance criteria text" --priority high
```

Arguments:
| Argument | Required | Description |
|----------|----------|-------------|
| module | Yes | Keyword indicating module type |
| "module-name" | Yes | Name of the module |
| --criteria | Recommended | Acceptance criteria text |
| --priority | Optional | critical/high/medium/low (default: medium) |

### Step 3: Verify Addition

```bash
/planning-status --verbose
```

Confirm the module appears with correct criteria and priority.

## Checklist

Copy this checklist and track your progress:

- [ ] Define module name and scope
- [ ] Write clear acceptance criteria
- [ ] Determine priority level
- [ ] Execute `/add-requirement module ...`
- [ ] Verify module appears in `/planning-status --verbose`
- [ ] Review module ID (kebab-case conversion)

## Examples

### Example: Adding a Critical Module

```bash
/add-requirement module "user-authentication" --criteria "Support email/password login with rate limiting" --priority critical

# Expected output:
# Added module: user-authentication
#   ID: user-authentication
#   Priority: critical
#   Acceptance Criteria: Support email/password login with rate limiting
#   Status: planned
```

### Example: Adding Multiple Modules

```bash
# Core authentication
/add-requirement module "auth-core" --criteria "JWT token generation and validation" --priority critical

# User management
/add-requirement module "user-crud" --criteria "Create, read, update, delete user operations" --priority high

# API documentation
/add-requirement module "api-docs" --criteria "OpenAPI/Swagger documentation" --priority medium

# Audit logging
/add-requirement module "audit-log" --criteria "Log all authentication events" --priority low
```

### Example: Module ID Normalization

Module names are converted to kebab-case IDs:

| Input Name | Generated ID |
|------------|--------------|
| "User Authentication" | user-authentication |
| "OAuth2_Handler" | oauth2-handler |
| "API Docs Module" | api-docs-module |

### Example: State File After Addition

```yaml
modules:
  - id: "auth-core"
    name: "Auth Core"
    status: "planned"
    priority: "critical"
    acceptance_criteria: "JWT token generation and validation"
    github_issue: null
  - id: "user-crud"
    name: "User CRUD"
    status: "planned"
    priority: "high"
    acceptance_criteria: "Create, read, update, delete user operations"
    github_issue: null
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Module already exists | Duplicate ID | Use a different name or modify existing |
| State file not found | Planning not started | Run `/start-planning` first |
| Empty module name | No name provided | Provide module name in quotes |
| Invalid priority | Unknown priority value | Use: critical, high, medium, or low |

## Related Operations

- [op-modify-module.md](op-modify-module.md) - Update module criteria or priority
- [op-remove-module.md](op-remove-module.md) - Remove planned module
- [op-approve-plan.md](op-approve-plan.md) - Approve plan (creates GitHub Issues)
