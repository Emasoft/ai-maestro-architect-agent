---
procedure: support-skill
workflow-instruction: support
---

# Operation: Record Design Pattern Selection

## Purpose

Record when a design pattern is selected for application to a component or module, preserving the pattern choice and its justification.

## When to Use

- Design pattern chosen for a component
- Architectural pattern applied to system
- Communication pattern selected

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Pattern name | Selection | Yes |
| Applied to | Component/module | Yes |
| Justification | Analysis | Yes |

## Procedure

### Step 1: Ensure Patterns File Exists

```bash
PATTERNS_FILE="docs_dev/design/patterns.md"

if [ ! -f "$PATTERNS_FILE" ]; then
    cat > "$PATTERNS_FILE" << 'EOF'
# Design Patterns Registry

This document tracks design patterns applied to the system architecture.

---

## Applied Patterns

<!-- Patterns are listed below -->

EOF
fi
```

### Step 2: Add Pattern Entry

Append to `docs_dev/design/patterns.md`:

```markdown
### <Pattern Name>

**Category:** <Structural|Communication|Data|Resilience|etc.>
**Applied To:** <component/module name>
**Date Applied:** YYYY-MM-DD

#### Justification

<Why this pattern fits the use case>

#### Constraints Introduced

- <Limitation or constraint this pattern creates>
- <Another constraint>

#### Implementation Notes

- <Specific implementation guidance>
- <Configuration requirements>

#### References

- [ADR-XXX](decisions/ADR-XXX-*.md) - Related decision
- [External Resource](url) - Pattern documentation

---
```

### Step 3: Update Design Index

```python
def add_pattern_to_index(pattern: dict):
    """Add pattern to design index."""
    import json

    index_path = "docs_dev/design/index.json"

    with open(index_path) as f:
        index = json.load(f)

    # Create anchor from pattern name
    anchor = pattern["name"].lower().replace(" ", "-")

    index["patterns"].append({
        "name": pattern["name"],
        "category": pattern["category"],
        "applied_to": pattern["applied_to"],
        "file": f"patterns.md#{anchor}"
    })

    index["last_updated"] = datetime.now().isoformat()

    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
```

### Step 4: Update Session State

```python
def update_session_after_pattern(session_state: dict, pattern_name: str):
    """Update session state after recording a pattern."""
    session_state["last_activity"] = "pattern_selected"
    session_state["last_updated"] = datetime.now().isoformat()

    # Patterns count not typically tracked, but can be derived from index
    save_session_state(session_state)
```

### Step 5: Report Pattern Recorded

```markdown
## Pattern Recorded

**Pattern:** Repository Pattern
**Category:** Data
**Applied To:** data-access-layer

**File Updated:** docs_dev/design/patterns.md
**Index Updated:** Yes

**Current Patterns:**
1. Microservices (Structural) - system-wide
2. Repository Pattern (Data) - data-access-layer
```

## Output

| File | Content |
|------|---------|
| `docs_dev/design/patterns.md` | Updated patterns registry |
| `docs_dev/design/index.json` | Updated index |
| `.claude/eaa-session-state.local.md` | Updated session state |

## Verification Checklist

- [ ] Pattern name correct
- [ ] Applied component specified
- [ ] Justification documented
- [ ] Constraints listed
- [ ] patterns.md updated
- [ ] Index updated
- [ ] Session state updated

## Pattern Categories

| Category | Examples |
|----------|----------|
| **Structural** | Microservices, Monolith, Modular Monolith, Layered |
| **Communication** | Request-Response, Event-Driven, Message Queue, Pub-Sub |
| **Data** | Repository, CQRS, Event Sourcing, Unit of Work |
| **Resilience** | Circuit Breaker, Retry, Bulkhead, Timeout |
| **Behavioral** | Strategy, Observer, Command, State |
| **Creational** | Factory, Builder, Singleton, Dependency Injection |

## Example

```markdown
### Repository Pattern

**Category:** Data
**Applied To:** data-access-layer
**Date Applied:** 2026-02-05

#### Justification

Decouples business logic from data persistence, enabling:
- Easy switching between storage backends
- Simplified unit testing with mock repositories
- Clean separation of concerns

#### Constraints Introduced

- All data access must go through repositories
- No direct database queries in service layer
- Repository interfaces must be defined for each aggregate

#### Implementation Notes

- Use `IRepository<T>` interface for generic operations
- Create specific interfaces for complex queries
- Implement caching at repository level

#### References

- [ADR-003](decisions/ADR-003-data-access.md) - Data access decision
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Pattern already exists | Duplicate entry | Update existing or clarify scope |
| patterns.md corrupted | Bad edit | Restore from git or rebuild |
| Index mismatch | Missed update | Regenerate index from files |
