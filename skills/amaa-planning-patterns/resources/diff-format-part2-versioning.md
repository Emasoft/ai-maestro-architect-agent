# Part 2: Version Tracking

**Parent document**: [diff-format.md](diff-format.md)

---

## 2.1 Version Format: MAJOR.MINOR.PATCH

Plan versions follow semantic versioning adapted for plans:

### MAJOR Version

Increment for breaking changes to plan structure:
- Removing phases
- Changing critical path
- Altering success criteria for completed work
- Major scope changes

### MINOR Version

Increment for non-breaking additions or modifications:
- Adding new phases
- Adding new tasks
- Refining descriptions
- Adding dependencies that don't break existing work

### PATCH Version

Increment for trivial changes:
- Typo fixes
- Clarifications
- Formatting improvements
- Minor wording changes

---

## 2.2 Version Increment Rules

1. Start at `1.0.0` for initial plan
2. Increment MAJOR when breaking changes occur
3. Increment MINOR when adding functionality or making significant updates
4. Increment PATCH for trivial corrections
5. Reset lower components when incrementing higher (e.g., `1.2.3` → `2.0.0`)

### Decision Guide

| Change Type | Version Increment | Example |
|-------------|-------------------|---------|
| Remove a phase | MAJOR | 1.2.3 → 2.0.0 |
| Change success criteria after completion | MAJOR | 1.2.3 → 2.0.0 |
| Add new phase | MINOR | 1.2.3 → 1.3.0 |
| Add new tasks | MINOR | 1.2.3 → 1.3.0 |
| Clarify task description | PATCH | 1.2.3 → 1.2.4 |
| Fix typo | PATCH | 1.2.3 → 1.2.4 |

---

## 2.3 Version Metadata

Each plan file should include version metadata in frontmatter:

```yaml
---
plan_name: "Project Alpha Implementation"
version: "2.1.0"
created: "2025-01-01T10:00:00Z"
modified: "2025-01-05T14:30:00Z"
author: "orchestrator-agent"
status: "active"
---
```

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `plan_name` | Human-readable plan title | "Project Alpha Implementation" |
| `version` | Current version number | "2.1.0" |
| `created` | Initial creation timestamp | "2025-01-01T10:00:00Z" |
| `modified` | Last modification timestamp | "2025-01-05T14:30:00Z" |
| `author` | Who created/owns the plan | "orchestrator-agent" |
| `status` | Plan lifecycle state | "active", "draft", "completed", "archived" |

---

## 2.4 Linking Diffs to Git Commits

Plan diffs should be committed alongside plan updates.

### Directory Structure

```
plans/
├── project-alpha.md              # Current plan (v2.1.0)
├── diffs/
│   ├── 1.0.0-to-1.1.0.diff.md   # First update
│   ├── 1.1.0-to-2.0.0.diff.md   # Breaking change
│   └── 2.0.0-to-2.1.0.diff.md   # Latest change
└── archive/
    ├── project-alpha-v1.0.0.md  # Original plan
    ├── project-alpha-v1.1.0.md  # First revision
    └── project-alpha-v2.0.0.md  # After breaking change
```

### Git Commit Message Format

Reference plan version in commit message:

```
Update project-alpha plan to v2.1.0

- Added Phase 4: Monitoring and Observability
- Modified Phase 3 success criteria to include performance benchmarks
- Removed redundant logging tasks (consolidated into Phase 4)

See: plans/diffs/2.0.0-to-2.1.0.diff.md
```

### Commit Checklist

When committing plan changes:

1. Update plan frontmatter version
2. Update `modified` timestamp
3. Generate diff file
4. Archive previous version
5. Commit all files together
6. Reference diff in commit message

---

**Previous**: [Part 1: Format Specification](diff-format-part1-format-spec.md)

**Next**: [Part 3: Tooling Integration](diff-format-part3-tooling.md)
