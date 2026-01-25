# Part 3: Tooling Integration

**Parent document**: [diff-format.md](diff-format.md)

---

## 3.1 generate_task_tracker.py Integration

The `generate_task_tracker.py` script uses plan diffs to:

1. **Detect Plan Changes**: Compare current plan against last tracked version
2. **Update Tracker**: Reflect new tasks, removed tasks, modified criteria
3. **Preserve Status**: Maintain completion status for unchanged tasks
4. **Flag Conflicts**: Highlight completed tasks that were modified
5. **Generate Changelog**: Create human-readable summary of tracking changes

### Example Usage

```bash
# Generate diff and update tracker
python scripts/generate_task_tracker.py \
  --plan plans/project-alpha.md \
  --previous-version plans/archive/project-alpha-v2.0.0.md \
  --output-diff plans/diffs/2.0.0-to-2.1.0.diff.md \
  --update-tracker
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--plan` | Path to current plan file |
| `--previous-version` | Path to previous plan version |
| `--output-diff` | Where to write the diff file |
| `--update-tracker` | Also update the task tracker |
| `--auto-version` | Automatically increment version |
| `--ignore-formatting` | Ignore whitespace-only changes |

---

## 3.2 Programmatic Diff Generation

The script generates diffs automatically by:

1. **Parsing Both Versions**: Extract structured data from old and new plan files
2. **Computing Differences**: Compare phases, tasks, dependencies, risks
3. **Categorizing Changes**: Classify as additions, removals, or modifications
4. **Formatting Output**: Generate markdown diff using standard format
5. **Validating Diff**: Ensure all changes are accounted for

### Key Functions

```python
def generate_plan_diff(old_plan_path, new_plan_path, output_path):
    """Generate a structured diff between two plan versions."""
    old_plan = parse_plan(old_plan_path)
    new_plan = parse_plan(new_plan_path)

    diff = {
        'phases_added': [],
        'phases_removed': [],
        'phases_modified': [],
        'tasks_added': [],
        'tasks_removed': [],
        'tasks_modified': [],
        'dependencies_added': [],
        'dependencies_removed': [],
        'risks_added': [],
        'risks_removed': []
    }

    # Compute differences
    compute_phase_diffs(old_plan, new_plan, diff)
    compute_task_diffs(old_plan, new_plan, diff)
    compute_dependency_diffs(old_plan, new_plan, diff)
    compute_risk_diffs(old_plan, new_plan, diff)

    # Format and write
    write_diff_markdown(diff, output_path)

    return diff
```

### Supporting Functions

| Function | Purpose |
|----------|---------|
| `parse_plan()` | Extract structured data from plan markdown |
| `compute_phase_diffs()` | Compare phases between versions |
| `compute_task_diffs()` | Compare tasks within phases |
| `compute_dependency_diffs()` | Compare task dependencies |
| `compute_risk_diffs()` | Compare risk entries |
| `write_diff_markdown()` | Format diff as markdown |

---

## 3.3 Diff Storage Location

Plan diffs are stored in a dedicated subdirectory:

```
PROJECT_ROOT/
├── plans/
│   ├── diffs/                    # All plan diffs
│   │   ├── YYYY-MM-DD_v{old}-to-v{new}.diff.md
│   │   └── index.md              # Index of all diffs
│   ├── archive/                  # Historical plan versions
│   └── {plan-name}.md            # Current active plan
└── scripts/
    └── generate_task_tracker.py  # Diff generation tool
```

### Naming Convention

Format: `YYYY-MM-DD_v{old}-to-v{new}.diff.md`

Examples:
- `2025-01-05_v2.0.0-to-v2.1.0.diff.md`
- `2025-01-10_v1.0.0-to-1.1.0.diff.md`
- `2025-02-01_v3.2.1-to-v4.0.0.diff.md`

### Index File

The `diffs/index.md` file provides a chronological listing:

```markdown
# Plan Diff Index

| Date | Version Change | Summary |
|------|----------------|---------|
| 2025-01-05 | 2.0.0 → 2.1.0 | Added monitoring phase |
| 2025-01-03 | 1.1.0 → 2.0.0 | Major restructure |
| 2025-01-01 | 1.0.0 → 1.1.0 | Initial refinements |
```

---

**Previous**: [Part 2: Version Tracking](diff-format-part2-versioning.md)

**Next**: [Part 4: Examples](diff-format-part4-examples.md)
