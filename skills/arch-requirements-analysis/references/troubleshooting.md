# Troubleshooting Reference

## Table of Contents
- 5.1 When /start-planning fails
- 5.2 When /planning-status shows errors
- 5.3 When /add-requirement fails
- 5.4 When /modify-requirement fails
- 5.5 When /remove-requirement fails
- 5.6 When /approve-plan fails
- 5.7 State file corruption recovery
- 5.8 GitHub Issue creation problems
- 5.9 Exit blocking issues

---

## 5.1 When /start-planning fails

**Error: "Plan Phase already active"**

Cause: State file `.claude/orchestrator-plan-phase.local.md` already exists.

Solutions:
1. Resume existing plan: `/planning-status`
2. Delete state file to start fresh (requires user approval):
   ```bash
   rm .claude/orchestrator-plan-phase.local.md
   /start-planning "New goal"
   ```

**Error: "Goal is required"**

Cause: No goal provided to the command.

Solution: Provide goal as argument:
```bash
/start-planning "Your project goal here"
```

**Error: "Goal cannot be empty"**

Cause: Goal was provided but resolved to empty string after stripping quotes.

Solution: Provide a non-empty goal string.

**Error: "Failed to create state file"**

Cause: Permission issues or disk space.

Solutions:
1. Check `.claude/` directory exists and is writable
2. Check available disk space
3. Verify current working directory is correct

---

## 5.2 When /planning-status shows errors

**Error: "Not in Plan Phase"**

Cause: State file does not exist.

Solutions:
1. Run `/start-planning` to begin planning
2. Verify you are in the correct project directory

**Error: "Could not parse plan state file"**

Cause: State file has invalid YAML frontmatter.

Solutions:
1. Check for YAML syntax errors in the frontmatter
2. Ensure frontmatter starts and ends with `---`
3. Restore from backup or recreate the file

**Status shows incomplete when requirements are done:**

Cause: Status field not updated after completing requirements.

Solution: Mark sections complete:
```bash
/modify-requirement requirement "Functional Requirements" --status complete
```

---

## 5.3 When /add-requirement fails

**Error: "Not in Plan Phase"**

Cause: Plan phase state file does not exist.

Solution: Run `/start-planning` first.

**Error: "Requirement section 'X' already exists"**

Cause: Attempting to add a duplicate requirement section.

Solution: Use `/modify-requirement` to change existing section.

**Error: "Module 'X' already exists"**

Cause: Attempting to add a module with the same ID.

Solutions:
1. Use a different name (ID is derived from name)
2. Remove existing module first: `/remove-requirement module X`
3. Modify existing module: `/modify-requirement module X --criteria "new"`

**Module ID is different than expected:**

Cause: IDs are normalized to kebab-case.

Example:
- Input: "User Authentication"
- Result ID: "user-authentication"

This is expected behavior. Use the normalized ID in subsequent commands.

---

## 5.4 When /modify-requirement fails

**Error: "Requirement section 'X' not found"**

Cause: The specified requirement section does not exist.

Solutions:
1. Check exact name with `/planning-status`
2. Add the section first: `/add-requirement requirement "X"`

**Error: "Module 'X' not found"**

Cause: The specified module ID does not exist.

Solutions:
1. Check exact ID with `/planning-status`
2. Use the kebab-case ID, not the display name

**Error: "Cannot modify module with status 'in_progress'"**

Cause: Module work has started, modification restricted.

Solutions:
1. Wait for module completion, then modify
2. If urgent, manually edit the state file (not recommended)

**Status change has no effect:**

Cause: Same status provided as current status.

Solution: Verify current status with `/planning-status` before modifying.

---

## 5.5 When /remove-requirement fails

**Error: "Cannot remove: status is in_progress"**

Cause: Module is being worked on.

Solutions:
1. Wait for completion
2. Force removal (data loss risk):
   ```bash
   /remove-requirement module X --force
   ```

**Error: "Cannot remove: status is complete"**

Cause: Module work is already finished.

Solution: Use `--force` if absolutely necessary (not recommended).

**Error: "Cannot remove: has GitHub Issue"**

Cause: Module has an associated GitHub Issue.

Solutions:
1. Close the GitHub Issue manually first:
   ```bash
   gh issue close [issue-number]
   ```
2. Then remove the module
3. Or use `--force` to remove without closing issue

**Error: "Not found: module X"**

Cause: Invalid module ID provided.

Solution: Check exact IDs with `/planning-status`.

---

## 5.6 When /approve-plan fails

**Error: "Not in Plan Phase"**

Cause: Plan phase state file does not exist.

Solution: Run `/start-planning` first.

**Error: "Plan already approved"**

Cause: Plan was already approved.

Solution: Run `/start-orchestration` to begin implementation.

**Error: "Requirements file not found"**

Cause: USER_REQUIREMENTS.md does not exist.

Solution: Create the requirements document before approval:
```bash
# Create USER_REQUIREMENTS.md with your requirements
```

**Error: "Requirement section incomplete: X"**

Cause: Section X is not marked as complete.

Solution:
```bash
/modify-requirement requirement "X" --status complete
```

**Error: "No modules defined"**

Cause: No modules added to the plan.

Solution: Add at least one module:
```bash
/add-requirement module "core-feature" --criteria "Success criteria here"
```

**Error: "Module missing acceptance criteria: X"**

Cause: Module X has no acceptance criteria defined.

Solution:
```bash
/modify-requirement module X --criteria "Acceptance criteria here"
```

---

## 5.7 State file corruption recovery

**Symptoms of corruption:**
- Parse errors when running commands
- Missing or malformed YAML
- Unexpected command behavior

**Recovery procedure:**

1. **Backup current file:**
   ```bash
   cp .claude/orchestrator-plan-phase.local.md .claude/orchestrator-plan-phase.local.md.bak
   ```

2. **Check YAML syntax:**
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('.claude/orchestrator-plan-phase.local.md').read().split('---')[1])"
   ```

3. **Common YAML issues:**
   - Missing closing `---` delimiter
   - Improper indentation (use 2 spaces)
   - Unquoted strings with special characters
   - Missing colons after keys

4. **Recreate from backup data:**
   If file is unrecoverable, start fresh:
   ```bash
   rm .claude/orchestrator-plan-phase.local.md
   /start-planning "Your goal"
   # Re-add modules from memory or notes
   ```

---

## 5.8 GitHub Issue creation problems

**Warning: "Failed to create issue for X"**

Cause: gh CLI error (auth, network, permissions).

Solutions:
1. Check gh CLI authentication:
   ```bash
   gh auth status
   ```
2. Verify repository access:
   ```bash
   gh repo view
   ```
3. Retry approval or create issues manually

**Warning: "gh CLI not found"**

Cause: GitHub CLI not installed.

Solutions:
1. Install gh CLI: `brew install gh`
2. Or use `--skip-issues` flag:
   ```bash
   /approve-plan --skip-issues
   ```

**Warning: "Timeout creating issue"**

Cause: Network timeout (30 second limit).

Solutions:
1. Check network connection
2. Retry the command
3. Create issues manually via gh CLI or web UI

**Issues created but not linked:**

Cause: Issue was created but URL parsing failed.

Solution: Manually update state file with issue number:
```yaml
modules:
  - id: "module-id"
    github_issue: "#42"  # Add this manually
```

---

## 5.9 Exit blocking issues

**Stop hook blocks exit unexpectedly:**

Cause: Exit criteria not met.

Solution: Check which criteria are incomplete:
```bash
/planning-status
```
Complete remaining criteria before exit.

**Cannot exit even after plan approval:**

Cause: State file shows plan_phase_complete as false despite approval.

Solutions:
1. Re-run `/approve-plan`
2. Manually set in state file:
   ```yaml
   plan_phase_complete: true
   ```

**Need to exit urgently without completing plan:**

Solution: Delete or rename the state file (user must approve):
```bash
mv .claude/orchestrator-plan-phase.local.md .claude/orchestrator-plan-phase.local.md.paused
```

This allows exit, but plan progress will be lost unless file is restored.

**Stop hook not blocking when it should:**

Cause: Stop hook may not be properly configured.

Solutions:
1. Verify hooks are loaded: `/hooks`
2. Check plugin is enabled
3. Restart Claude Code session
