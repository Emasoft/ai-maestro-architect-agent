---
operation: modify-module
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Modify Module Operation

## When to Use

Use this operation when:
- Updating acceptance criteria after discussion
- Changing module priority
- Renaming a module for clarity
- Changing module status

## Prerequisites

- [ ] Plan Phase is active
- [ ] Module exists with status `planned` or `pending`
- [ ] Module is NOT `in_progress` or `complete` (blocked modification)

## Procedure

### Step 1: Identify Module to Modify

```bash
/planning-status --verbose
```

Review modules and their current properties.

### Step 2: Execute Modification

```bash
/modify-requirement module module-id --criteria "New criteria" --priority critical
```

Available modifications:

| Argument | Description |
|----------|-------------|
| --name | New display name |
| --status | New status (planned/pending/in_progress/complete) |
| --criteria | New acceptance criteria |
| --priority | New priority (critical/high/medium/low) |

### Step 3: Verify Change

```bash
/planning-status --verbose
```

Confirm module shows updated properties.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify module ID with `/planning-status --verbose`
- [ ] Verify module status is planned or pending
- [ ] Determine which fields to update
- [ ] Execute `/modify-requirement module ...`
- [ ] Verify changes in status output

## Examples

### Example: Updating Acceptance Criteria

```bash
# After user feedback, add rate limiting requirement
/modify-requirement module user-login --criteria "Email/password auth with rate limiting"

# Expected output:
# Modified module: user-login
#   Acceptance Criteria: Email/password auth with rate limiting
```

### Example: Changing Priority

```bash
# Elevate priority based on business needs
/modify-requirement module audit-log --priority high

# Verify
/planning-status --verbose
# Shows: audit-log | High | ...
```

### Example: Renaming Module

```bash
# Rename for clarity
/modify-requirement module auth-2fa --name "Two-Factor Authentication Module"

# Note: ID remains auth-2fa, only display name changes
```

### Example: Multiple Modifications

```bash
# Update both criteria and priority
/modify-requirement module session-mgmt --criteria "Token refresh with 24h expiry" --priority critical
```

### Example: State File After Modification

```yaml
modules:
  - id: "auth-core"
    name: "Auth Core"
    status: "planned"
    priority: "critical"          # CHANGED from high
    acceptance_criteria: "JWT tokens with RS256 signing"  # CHANGED
    github_issue: null
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Module not found | ID mismatch | Check exact ID with `/planning-status --verbose` |
| Cannot modify | Status is in_progress/complete | Only planned/pending modules can be modified |
| Invalid priority | Unknown value | Use: critical, high, medium, or low |
| Invalid status | Unknown status | Use: planned, pending, in_progress, or complete |
| State file not found | Planning not started | Run `/start-planning` first |

## Related Operations

- [op-add-module.md](op-add-module.md) - Add new modules
- [op-remove-module.md](op-remove-module.md) - Remove planned modules
- [op-check-planning-status.md](op-check-planning-status.md) - View module details
