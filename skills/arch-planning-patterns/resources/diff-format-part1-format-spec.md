# Part 1: Format Specification and Change Indicators

**Parent document**: [diff-format.md](diff-format.md)

---

## 1.1 Diff Format Specification

Every plan diff follows this standardized markdown format:

```markdown
# Plan Diff: {plan-name}
Generated: {timestamp}
From: {version-a} → To: {version-b}
Author: {author-name}
Reason: {brief-explanation}

## Summary
- Phases Added: N
- Phases Removed: M
- Phases Modified: K
- Tasks Added: X
- Tasks Removed: Y
- Tasks Modified: Z
- Dependencies Added: A
- Dependencies Removed: B
- Risks Added: R
- Risks Removed: S

## Changes

### Phase Changes
+ Added: Phase N - {phase-name}
  Description: {phase-description}

- Removed: Phase M - {phase-name}
  Reason: {why-removed}

~ Modified: Phase K - {old-name} → {new-name}
  Changes: {what-changed}

### Task Changes
+ Added: [Phase N] {task-description}
  Dependencies: {task-dependencies}
  Success Criteria: {criteria}

- Removed: [Phase M] {task-description}
  Reason: {why-removed}
  Impact: {what-this-affects}

~ Modified: [Phase K] {old-task} → {new-task}
  Changes: {detailed-changes}
  Impact: {what-this-affects}

### Dependency Changes
+ Added: Task A → Task B
  Reason: {why-dependency-added}

- Removed: Task X → Task Y
  Reason: {why-dependency-removed}
  Impact: {how-this-affects-schedule}

### Risk Changes
+ Added: [{severity}] {risk-description}
  Mitigation: {mitigation-strategy}

- Removed: [{severity}] {risk-description}
  Reason: {why-no-longer-relevant}

### Success Criteria Changes
~ Modified: {old-criteria} → {new-criteria}
  Reason: {why-changed}

### Milestone Changes
+ Added: {milestone-name} - {target-date}
  Success Criteria: {criteria}

- Removed: {milestone-name}
  Reason: {why-removed}
```

---

## 1.2 Change Indicators

Each change type uses a specific prefix symbol with semantic meaning:

| Symbol | Meaning | Color (Rendered) | Usage |
|--------|---------|------------------|-------|
| `+` | Addition | Green | New phases, tasks, dependencies, risks added to plan |
| `-` | Removal | Red | Existing elements removed from plan |
| `~` | Modification | Yellow | Existing elements changed (name, description, criteria, etc.) |
| `!` | Breaking Change | Red/Bold | Changes that invalidate prior work or require major adjustments |
| `?` | Tentative | Gray | Proposed changes not yet finalized |

---

## 1.3 Breaking Change Examples

Breaking changes are modifications that invalidate prior work or require major adjustments:

- Removing a phase that other tasks depend on
- Changing success criteria that make completed work invalid
- Altering dependencies that break the critical path
- Modifying scope that requires re-estimation

Breaking changes should be marked explicitly:

```markdown
! Breaking: Removed Phase 2 - Backend API Development
  Impact: Frontend tasks in Phase 3 now blocked
  Action Required: Re-sequence frontend work or restore backend phase
```

### When to Use Breaking Change Indicator

Use the `!` prefix when a change:

1. **Invalidates completed work** - Success criteria changed after task marked done
2. **Blocks other tasks** - Removes a dependency that other tasks relied on
3. **Requires major adjustment** - Forces replanning of subsequent phases
4. **Changes critical path** - Alters the sequence of dependent tasks
5. **Affects team assignments** - Eliminates or restructures team responsibilities

---

**Next**: [Part 2: Version Tracking](diff-format-part2-versioning.md)
