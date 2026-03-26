---
name: extended-examples-and-resources
description: "Extended examples and resources."
---

## Table of Contents

- Error Handling Details
- Extended Examples
- Resources
- Command Output Reference



## Error Handling Details

Common errors encountered during the planning phase and how to resolve them:

**1. "State file not found" when running any planning command**
- Cause: Planning was not initialized, or the state file at `.claude/orchestrator-plan-phase.local.md` was deleted or moved.
- Resolution: Run `/amaa-start-planning "your goal"` to create the state file. If the file was accidentally deleted, use `scripts/reset_plan_phase.py --confirm` to reinitialize, then re-add your requirements and modules.

**2. "Approval prerequisites failed" when running plan approval**
- Cause: One or more exit criteria are not met (missing USER_REQUIREMENTS.md, incomplete requirement sections, modules without acceptance criteria, or no modules defined).
- Resolution: Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py --fix-suggestions` to see which criteria are failing. Address each one: create USER_REQUIREMENTS.md if missing, mark all requirement sections complete with `/amaa-modify-requirement requirement "Name" --status complete`, and ensure every module has `--criteria` set. Then set `plan_phase_complete: true` in the state file.

**3. "GitHub Issue creation failed" during plan approval**
- Cause: The GitHub CLI (`gh`) is not authenticated, the repository does not exist, or network connectivity is lost.
- Resolution: Run `gh auth status` to verify authentication. If not logged in, run `gh auth login`. Verify the repository exists with `gh repo view`. If you need to approve the plan without creating issues, set `plan_phase_complete: true` in the state file and skip the issue creation step, then create issues manually later.

---

## Extended Examples

### Example 1: Planning a Microservice from Scratch

```bash
# Initialize planning for a new notification microservice

## Contents

- [Error Handling Details](#error-handling-details)
- [Extended Examples](#extended-examples)
- [Resources](#resources)
- [Command Output Reference](#command-output-reference)

---

/amaa-start-planning "Build a notification microservice supporting email, SMS, and push notifications"

# Define the core modules with acceptance criteria
/amaa-add-requirement module "notification-dispatcher" --criteria "Route notifications to correct channel based on user preferences" --priority critical
/amaa-add-requirement module "email-provider" --criteria "Send emails via SMTP with template support and retry logic" --priority high
/amaa-add-requirement module "sms-provider" --criteria "Send SMS via Twilio API with rate limiting" --priority high
/amaa-add-requirement module "push-provider" --criteria "Send push notifications via Firebase Cloud Messaging" --priority medium

# Add a custom requirement section for compliance
/amaa-add-requirement requirement "Compliance Requirements"

# Mark sections complete as you document them
/amaa-modify-requirement requirement "Functional Requirements" --status complete
/amaa-modify-requirement requirement "Non-Functional Requirements" --status complete
/amaa-modify-requirement requirement "Compliance Requirements" --status complete
/amaa-modify-requirement requirement "Architecture Design" --status complete

# Verify everything is ready
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py --fix-suggestions

# Approve plan transition: set plan_phase_complete: true in state file
```

### Example 2: Iterating on a Plan After Initial Review

```bash
# Check current status after initial planning
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py

# User feedback: auth module needs to support SSO in addition to JWT
/amaa-modify-requirement module auth-jwt --criteria "Support JWT authentication AND SSO via SAML 2.0" --priority critical

# User feedback: remove the legacy-api module that is no longer needed
/amaa-remove-requirement module legacy-api

# Add a new module based on review feedback
/amaa-add-requirement module "rate-limiter" --criteria "Implement token bucket rate limiting per API key" --priority high

# Verify updated plan
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py --fix-suggestions
```

### Example 3: Recovering from a Failed Approval

```bash
# Attempt to approve the plan (set plan_phase_complete: true in state file)
# Output: "Approval prerequisites failed: Non-Functional Requirements is not complete"

# Fix the missing prerequisite
/amaa-modify-requirement requirement "Non-Functional Requirements" --status complete

# Run the prerequisite check script to verify everything
python3 scripts/check_plan_prerequisites.py --fix-suggestions

# Retry approval: set plan_phase_complete: true in state file
```

---

## Resources

### Reference Documents

Located in this skill's references directory:
- start-planning-procedure - Detailed /amaa-start-planning command procedure, prerequisites, and post-initialization steps
- requirement-management - Complete guide to adding, modifying, and removing requirements and modules
- plan-approval-transition - Approval validation checks, GitHub Issue creation, and state transitions
- state-file-format - YAML frontmatter schema, field definitions, and state file lifecycle
- [troubleshooting.md](troubleshooting.md) - Comprehensive troubleshooting for all planning commands and state recovery

### Related Skills

- `amaa-orchestration-commands` - The orchestration phase skill that follows after plan approval
- `amaa-agent-management` - Registering and assigning agents to approved modules
- `amaa-module-lifecycle` - Tracking module implementation progress after planning

### External Dependencies

- [GitHub CLI documentation](https://cli.github.com/manual/) - Required for issue creation during approve plan transition
- [AI Maestro messaging](https://github.com/Emasoft/ai-maestro) - Required for inter-agent communication during plan handoff

---

## Command Output Reference

Each planning command produces specific output. See detailed command documentation in SKILL.md sections 1.0-6.0.

| Command | Output Type | Details |
|---------|-------------|---------|
| `/amaa-start-planning` | State file creation + confirmation message | See section 1.0 |
| `python3 scripts/check_plan_prerequisites.py` | Formatted status table with progress | See section 2.0 |
| `/amaa-add-requirement` | Confirmation message + updated state | See section 3.0 |
| `/amaa-modify-requirement` | Confirmation message + updated state | See section 4.0 |
| `/amaa-remove-requirement` | Confirmation message + updated state | See section 5.0 |
| Approve plan transition | Validation results + GitHub Issues created | See section 6.0 |
