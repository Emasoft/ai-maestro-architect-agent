# Troubleshooting Reference

## Table of Contents
- When /amaa-start-planning fails
- When Checking Planning Status Shows Errors
- When /amaa-add-requirement fails
- When /amaa-modify-requirement fails
- When /amaa-remove-requirement fails
- When Plan Approval Fails
- State file corruption recovery

## 5.1 When /amaa-start-planning fails

**Error: "Plan Phase already active"**

Cause: State file `.claude/orchestrator-plan-phase.local.md` already exists.

Solutions:
1. Resume existing plan: check the plan state file at `.claude/orchestrator-plan-phase.local.md`
2. Delete state file to start fresh (requires user approval):
   ```bash
   rm .claude/orchestrator-plan-phase.local.md
   /amaa-start-planning "New goal"
   ```

**Error: "Goal is required"**

Cause: No goal provided to the command.

Solution: Provide goal as argument:
```bash
/amaa-start-planning "Your project goal here"
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

## 5.2 When Checking Planning Status Shows Errors

**Error: "Not in Plan Phase"**

Cause: State file does not exist.

Solutions:
1. Run `/amaa-start-planning` to begin planning
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
/amaa-modify-requirement requirement "Functional Requirements" --status complete
```

---

## 5.3 When /amaa-add-requirement fails

**Error: "Not in Plan Phase"**

Cause: Plan phase state file does not exist.

Solution: Run `/amaa-start-planning` first.

**Error: "Requirement section 'X' already exists"**

Cause: Attempting to add a duplicate requirement section.

Solution: Use `/amaa-modify-requirement` to change existing section.

**Error: "Module 'X' already exists"**

Cause: Attempting to add a module with the same ID.

Solutions:
1. Use a different name (ID is derived from name)
2. Remove existing module first: `/amaa-remove-requirement module X`
3. Modify existing module: `/amaa-modify-requirement module X --criteria "new"`

**Module ID is different than expected:**

Cause: IDs are normalized to kebab-case.

Example:
- Input: "User Authentication"
- Result ID: "user-authentication"

This is expected behavior. Use the normalized ID in subsequent commands.

---

## 5.4 When /amaa-modify-requirement fails

**Error: "Requirement section 'X' not found"**

Cause: The specified requirement section does not exist.

Solutions:
1. Check exact name by running `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py`
2. Add the section first: `/amaa-add-requirement requirement "X"`

**Error: "Module 'X' not found"**

Cause: The specified module ID does not exist.

Solutions:
1. Check exact ID by inspecting the plan state file at `.claude/orchestrator-plan-phase.local.md`
2. Use the kebab-case ID, not the display name

**Error: "Cannot modify module with status 'in-progress'"**

Cause: Module work has started, modification restricted.

Solutions:
1. Wait for module completion, then modify
2. If urgent, manually edit the state file (not recommended)

**Status change has no effect:**

Cause: Same status provided as current status.

Solution: Verify current status by checking the plan state file at `.claude/orchestrator-plan-phase.local.md` before modifying.

---

## 5.5 When /amaa-remove-requirement fails

**Error: "Cannot remove: status is in-progress"**

Cause: Module is being worked on.

Solutions:
1. Wait for completion
2. Force removal (data loss risk):
   ```bash
   /amaa-remove-requirement module X --force
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

Solution: Check exact IDs in the plan state file at `.claude/orchestrator-plan-phase.local.md`.

---

## 5.6 When Plan Approval Fails

**Error: "Not in Plan Phase"**

Cause: Plan phase state file does not exist.

Solution: Run `/amaa-start-planning` first.

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
/amaa-modify-requirement requirement "X" --status complete
```

**Error: "No modules defined"**

Cause: No modules added to the plan.

Solution: Add at least one module:
```bash
/amaa-add-requirement module "core-feature" --criteria "Success criteria here"
```

**Error: "Module missing acceptance criteria: X"**

Cause: Module X has no acceptance criteria defined.

Solution:
```bash
/amaa-modify-requirement module X --criteria "Acceptance criteria here"
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
   /amaa-start-planning "Your goal"
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
   # Mark all requirements as complete using /amaa-modify-requirement, then set plan_phase_complete: true in the state file
   # Use --skip-issues if needed when approving the plan
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

Solution: Check which criteria are incomplete by running:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_plan_prerequisites.py
```
Complete remaining criteria before exit.

**Cannot exit even after plan approval:**

Cause: State file shows plan_phase_complete as false despite approval.

Solutions:
1. Mark all requirements as complete using `/amaa-modify-requirement` and re-verify prerequisites
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
