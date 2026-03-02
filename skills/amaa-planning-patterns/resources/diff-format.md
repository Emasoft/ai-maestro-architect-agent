# Plan Diff Format Specification

## Overview

A plan diff is a structured representation of changes between two versions of a plan. It tracks the evolution of a plan over time, documenting what was added, removed, or modified. Plan diffs are critical for:

- **Audit Trail**: Understanding why and when a plan changed
- **Change Review**: Assessing the impact of plan modifications before committing
- **Communication**: Explaining plan changes to stakeholders and team members
- **Rollback**: Reverting problematic changes by understanding what was altered
- **Learning**: Analyzing how plans evolve in response to reality

Plan diffs complement git diffs by providing semantic understanding of plan structure rather than just line-by-line text changes.

---

## Table of Contents

This specification is organized into the following sections:

### Part 1: Format Specification and Change Indicators
**File**: [diff-format-part1-format-spec.md](diff-format-part1-format-spec.md)

- 1.1 Diff Format Specification - Core markdown template for plan diffs
- 1.2 Change Indicators - Symbol meanings (+, -, ~, !, ?)
- 1.3 Breaking Change Examples - When to use the ! indicator

### Part 2: Version Tracking
**File**: [diff-format-part2-versioning.md](diff-format-part2-versioning.md)

- 2.1 Version Format (MAJOR.MINOR.PATCH) - Semantic versioning for plans
- 2.2 Version Increment Rules - When to increment each component
- 2.3 Version Metadata - YAML frontmatter format
- 2.4 Linking Diffs to Git Commits - Directory structure and commit messages

### Part 3: Tooling Integration
**File**: [diff-format-part3-tooling.md](diff-format-part3-tooling.md)

- 3.1 generate_task_tracker.py Integration - Script usage and capabilities
- 3.2 Programmatic Diff Generation - Key functions and algorithms
- 3.3 Diff Storage Location - Directory structure and naming conventions

### Part 4: Examples
**File**: [diff-format-part4-examples.md](diff-format-part4-examples.md)

- 4.1 Example 1: Small Diff (1-2 Task Changes) - PATCH version increment
- 4.2 Example 2: Medium Diff (Phase Restructure) - MAJOR version increment
- 4.3 Example 3: Large Diff (Major Replanning) - Complete pivot scenario

### Part 5: Best Practices and Troubleshooting
**File**: [diff-format-part5-best-practices.md](diff-format-part5-best-practices.md)

- 5.1 Best Practices - 10 guidelines for effective diff management
- 5.2 Troubleshooting - Common problems and solutions

---

## Quick Reference

### Change Indicator Symbols

| Symbol | Meaning | Usage |
|--------|---------|-------|
| `+` | Addition | New phases, tasks, dependencies, risks |
| `-` | Removal | Elements removed from plan |
| `~` | Modification | Elements changed |
| `!` | Breaking Change | Changes that invalidate prior work |
| `?` | Tentative | Proposed changes not yet finalized |

### Version Increment Summary

| Change Type | Version Component | Example |
|-------------|-------------------|---------|
| Breaking (remove phase, change critical path) | MAJOR | 1.0.0 → 2.0.0 |
| Non-breaking additions | MINOR | 1.0.0 → 1.1.0 |
| Typos, clarifications | PATCH | 1.0.0 → 1.0.1 |

---

## Reading Order

For comprehensive understanding, read the parts in order:

1. **Start with Part 1** to understand the diff format structure
2. **Read Part 2** to learn version tracking conventions
3. **Review Part 3** for tooling integration
4. **Study Part 4** examples to see the format in action
5. **Reference Part 5** for best practices and troubleshooting

For quick reference during diff creation, jump directly to the relevant part.
