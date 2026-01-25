# Part 5: Best Practices and Troubleshooting

**Parent document**: [diff-format.md](diff-format.md)

---

## 5.1 Best Practices

Follow these guidelines for effective diff management:

### 1. Generate Diffs Automatically

Use tooling to ensure consistency and completeness. Manual diffs are error-prone and may miss changes.

### 2. Include Rationale

Always explain why changes were made. Future readers need context to understand decisions.

### 3. Assess Impact

Document what each change affects. This helps teams prepare for downstream consequences.

### 4. Mark Breaking Changes

Use `!` prefix to highlight changes requiring attention. Breaking changes need immediate team awareness.

### 5. Link to Discussion

Reference GitHub issues, PRs, or meeting notes that led to changes. This creates an audit trail.

### 6. Review Before Committing

Treat plan diffs like code diffs - review carefully. A bad plan change can derail entire projects.

### 7. Archive Old Versions

Keep historical plan files for reference and rollback. Never delete plan history.

### 8. Update Tracker

Regenerate task tracker after plan changes to maintain sync. Stale trackers cause confusion.

### 9. Communicate Changes

Share diffs with team members affected by plan updates. Surprises damage trust.

### 10. Learn from Diffs

Analyze patterns in how plans evolve to improve future planning. Each diff teaches something.

---

## 5.2 Troubleshooting

### Problem: Diff Generation Fails

**Symptom**: `generate_task_tracker.py` cannot parse plan files

**Solutions**:
- Ensure both plan files follow standard plan-format.md structure
- Check for YAML frontmatter parsing errors
- Validate markdown syntax (headings, lists, code blocks)
- Run plan validator: `python scripts/validate-plan.py plans/my-plan.md`

---

### Problem: Diff Shows No Changes But Plans Differ

**Symptom**: Diff summary shows 0 changes but visual inspection shows differences

**Solutions**:
- Check if changes are only formatting/whitespace (not semantic)
- Ensure both files are using same heading levels for phases/tasks
- Verify task descriptions use consistent bullet point format
- Run diff with `--ignore-formatting` flag if available

---

### Problem: Breaking Changes Not Detected

**Symptom**: Script doesn't flag breaking changes automatically

**Solutions**:
- Breaking change detection requires manual review and marking
- Script can detect removals, but whether they're "breaking" is contextual
- Review diff output and manually add `!` prefix where appropriate
- Update script's breaking change heuristics for your project's needs

---

### Problem: Version Numbers Don't Match

**Symptom**: Plan file version doesn't match diff filename

**Solutions**:
- Always update plan frontmatter version before generating diff
- Use script's `--auto-version` flag to increment version automatically
- Ensure naming convention consistency: `v{old}-to-v{new}.diff.md`
- Validate version numbers follow semver: `MAJOR.MINOR.PATCH`

---

### Problem: Tracker Out of Sync with Plan

**Symptom**: Task tracker shows tasks that no longer exist in plan

**Solutions**:
- Regenerate tracker with `--update-tracker` flag
- Check for orphaned tasks marked complete but removed from plan
- Review diff to understand what was removed
- Manually reconcile tracker if automatic update fails

---

### Problem: Merge Conflicts in Diffs

**Symptom**: Git merge conflicts when multiple agents update plans

**Solutions**:
- Coordinate plan updates through single orchestrator agent
- Use plan locking mechanism during updates
- Regenerate diff after resolving plan merge conflicts
- Never manually edit diff files - regenerate instead

---

**Previous**: [Part 4: Examples](diff-format-part4-examples.md)

**Return to**: [diff-format.md](diff-format.md)
