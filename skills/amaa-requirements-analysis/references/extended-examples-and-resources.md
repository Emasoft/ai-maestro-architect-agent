---
name: extended-examples-and-resources
description: Additional planning phase examples, error handling details, and resource links for the eaa-requirements-analysis skill.
version: 1.0.0
parent-skill: eaa-requirements-analysis
---

## Contents

- [Error Handling Details](#error-handling-details)
  - [State file not found](#1-state-file-not-found-when-running-any-planning-command)
  - [Approval prerequisites failed](#2-approval-prerequisites-failed-when-running-approve-plan)
  - [GitHub Issue creation failed](#3-github-issue-creation-failed-during-plan-approval)
- [Extended Examples](#extended-examples)
  - [Example 1: Planning a Microservice from Scratch](#example-1-planning-a-microservice-from-scratch)
  - [Example 2: Iterating on a Plan After Initial Review](#example-2-iterating-on-a-plan-after-initial-review)
  - [Example 3: Recovering from a Failed Approval](#example-3-recovering-from-a-failed-approval)
- [Resources](#resources)
  - [Reference Documents](#reference-documents)
  - [Related Skills](#related-skills)
  - [External Dependencies](#external-dependencies)
- [Command Output Reference](#command-output-reference)

---

## Error Handling Details

Common errors encountered during the planning phase and how to resolve them:

**1. "State file not found" when running any planning command**
- Cause: Planning was not initialized, or the state file at `.claude/orchestrator-plan-phase.local.md` was deleted or moved.
- Resolution: Run `/start-planning "your goal"` to create the state file. If the file was accidentally deleted, use `scripts/reset_plan_phase.py --confirm` to reinitialize, then re-add your requirements and modules.

**2. "Approval prerequisites failed" when running /approve-plan**
- Cause: One or more exit criteria are not met (missing USER_REQUIREMENTS.md, incomplete requirement sections, modules without acceptance criteria, or no modules defined).
- Resolution: Run `/planning-status --verbose` to see which criteria are failing. Address each one: create USER_REQUIREMENTS.md if missing, mark all requirement sections complete with `/modify-requirement requirement "Name" --status complete`, and ensure every module has `--criteria` set. Then retry `/approve-plan`.

**3. "GitHub Issue creation failed" during plan approval**
- Cause: The GitHub CLI (`gh`) is not authenticated, the repository does not exist, or network connectivity is lost.
- Resolution: Run `gh auth status` to verify authentication. If not logged in, run `gh auth login`. Verify the repository exists with `gh repo view`. If you need to approve the plan without creating issues, use `/approve-plan --skip-issues` and create issues manually later.

---

## Extended Examples

### Example 1: Planning a Microservice from Scratch

```bash
# Initialize planning for a new notification microservice
/start-planning "Build a notification microservice supporting email, SMS, and push notifications"

# Define the core modules with acceptance criteria
/add-requirement module "notification-dispatcher" --criteria "Route notifications to correct channel based on user preferences" --priority critical
/add-requirement module "email-provider" --criteria "Send emails via SMTP with template support and retry logic" --priority high
/add-requirement module "sms-provider" --criteria "Send SMS via Twilio API with rate limiting" --priority high
/add-requirement module "push-provider" --criteria "Send push notifications via Firebase Cloud Messaging" --priority medium

# Add a custom requirement section for compliance
/add-requirement requirement "Compliance Requirements"

# Mark sections complete as you document them
/modify-requirement requirement "Functional Requirements" --status complete
/modify-requirement requirement "Non-Functional Requirements" --status complete
/modify-requirement requirement "Compliance Requirements" --status complete
/modify-requirement requirement "Architecture Design" --status complete

# Verify everything is ready, then approve
/planning-status --verbose
/approve-plan
```

### Example 2: Iterating on a Plan After Initial Review

```bash
# Check current status after initial planning
/planning-status

# User feedback: auth module needs to support SSO in addition to JWT
/modify-requirement module auth-jwt --criteria "Support JWT authentication AND SSO via SAML 2.0" --priority critical

# User feedback: remove the legacy-api module that is no longer needed
/remove-requirement module legacy-api

# Add a new module based on review feedback
/add-requirement module "rate-limiter" --criteria "Implement token bucket rate limiting per API key" --priority high

# Verify updated plan
/planning-status --verbose
```

### Example 3: Recovering from a Failed Approval

```bash
# Attempt to approve the plan
/approve-plan
# Output: "Approval prerequisites failed: Non-Functional Requirements is not complete"

# Fix the missing prerequisite
/modify-requirement requirement "Non-Functional Requirements" --status complete

# Run the prerequisite check script to verify everything
python3 scripts/check_plan_prerequisites.py --fix-suggestions

# Retry approval
/approve-plan
```

---

## Resources

### Reference Documents

Located in this skill's references directory:
- [start-planning-procedure.md](start-planning-procedure.md) - Detailed /start-planning command procedure, prerequisites, and post-initialization steps
- [requirement-management.md](requirement-management.md) - Complete guide to adding, modifying, and removing requirements and modules
- [plan-approval-transition.md](plan-approval-transition.md) - Approval validation checks, GitHub Issue creation, and state transitions
- [state-file-format.md](state-file-format.md) - YAML frontmatter schema, field definitions, and state file lifecycle
- [troubleshooting.md](troubleshooting.md) - Comprehensive troubleshooting for all planning commands and state recovery

### Related Skills

- `eaa-orchestration-commands` - The orchestration phase skill that follows after plan approval
- `eaa-agent-management` - Registering and assigning agents to approved modules
- `eaa-module-lifecycle` - Tracking module implementation progress after planning

### External Dependencies

- [GitHub CLI documentation](https://cli.github.com/manual/) - Required for issue creation during `/approve-plan`
- [AI Maestro messaging](https://github.com/Emasoft/ai-maestro) - Required for inter-agent communication during plan handoff

---

## Command Output Reference

Each planning command produces specific output. See detailed command documentation in SKILL.md sections 1.0-6.0.

| Command | Output Type | Details |
|---------|-------------|---------|
| `/start-planning` | State file creation + confirmation message | See section 1.0 |
| `/planning-status` | Formatted status table with progress | See section 2.0 |
| `/add-requirement` | Confirmation message + updated state | See section 3.0 |
| `/modify-requirement` | Confirmation message + updated state | See section 4.0 |
| `/remove-requirement` | Confirmation message + updated state | See section 5.0 |
| `/approve-plan` | Validation results + GitHub Issues created | See section 6.0 |
