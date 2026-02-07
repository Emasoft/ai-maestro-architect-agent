---
procedure: support-skill
workflow-instruction: support
---

# Operation: Record Technology Stack Choice

## Purpose

Record when a technology is selected for the project stack, preserving the choice, version, purpose, and rationale.

## When to Use

- Technology selected for implementation
- Framework chosen
- Library or package added to requirements
- Service or tool selected

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Technology name | Selection | Yes |
| Version | Requirements | Yes |
| Purpose | Analysis | Yes |
| Rationale | Discussion | Yes |

## Procedure

### Step 1: Ensure Stack File Exists

```bash
STACK_FILE="docs_dev/design/stack.md"

if [ ! -f "$STACK_FILE" ]; then
    cat > "$STACK_FILE" << 'EOF'
# Technology Stack

This document tracks technology choices for the project.

---

## Core Technologies

<!-- Core language, framework, and runtime choices -->

---

## Infrastructure

<!-- Databases, caches, queues, etc. -->

---

## Development Tools

<!-- Build tools, testing, CI/CD, etc. -->

---

## External Services

<!-- Third-party APIs and services -->

EOF
fi
```

### Step 2: Determine Category

| Category | Examples |
|----------|----------|
| **Core Technologies** | Python, Node.js, React, FastAPI |
| **Infrastructure** | PostgreSQL, Redis, RabbitMQ, S3 |
| **Development Tools** | pytest, ruff, GitHub Actions |
| **External Services** | Stripe, Auth0, SendGrid |

### Step 3: Add Stack Entry

Add to appropriate section in `docs_dev/design/stack.md`:

```markdown
### <Technology Name>

**Version:** <version>
**Category:** <category>
**Purpose:** <what role it serves>
**Date Added:** YYYY-MM-DD

#### Rationale

<Why chosen over alternatives>

#### Compatibility Notes

- <Integration consideration>
- <Version constraints>

#### Related Technologies

- <Related tech in stack>

#### Reference

- [Official Documentation](url)
- [ADR-XXX](decisions/ADR-XXX-*.md) - Selection decision

---
```

### Step 4: Update Design Index

```python
def add_stack_to_index(tech: dict):
    """Add technology to design index."""
    import json

    index_path = "docs_dev/design/index.json"

    with open(index_path) as f:
        index = json.load(f)

    # Initialize stack section if needed
    if "stack" not in index:
        index["stack"] = []

    anchor = tech["name"].lower().replace(" ", "-").replace(".", "")

    index["stack"].append({
        "name": tech["name"],
        "version": tech["version"],
        "category": tech["category"],
        "purpose": tech["purpose"],
        "file": f"stack.md#{anchor}"
    })

    index["last_updated"] = datetime.now().isoformat()

    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
```

### Step 5: Update Session State

```python
def update_session_after_stack_choice(session_state: dict, tech_name: str):
    """Update session state after recording a stack choice."""
    session_state["last_activity"] = "technology_stack_updated"
    session_state["last_updated"] = datetime.now().isoformat()

    save_session_state(session_state)
```

### Step 6: Report Stack Updated

```markdown
## Stack Updated

**Technology:** Redis
**Version:** 7.2
**Category:** Infrastructure
**Purpose:** Session storage and caching

**File Updated:** docs_dev/design/stack.md
**Index Updated:** Yes

**Current Stack Summary:**

| Category | Technologies |
|----------|--------------|
| Core | Python 3.12, FastAPI |
| Infrastructure | PostgreSQL 16, Redis 7.2 |
| Development | pytest, ruff, mypy |
| External | Stripe, SendGrid |
```

## Output

| File | Content |
|------|---------|
| `docs_dev/design/stack.md` | Updated stack registry |
| `docs_dev/design/index.json` | Updated index |
| `.claude/eaa-session-state.local.md` | Updated session state |

## Verification Checklist

- [ ] Technology name correct
- [ ] Version specified
- [ ] Purpose documented
- [ ] Rationale provided
- [ ] Category assigned
- [ ] stack.md updated
- [ ] Index updated
- [ ] Session state updated

## Example

```markdown
### Redis

**Version:** 7.2
**Category:** Infrastructure
**Purpose:** Session storage and caching layer
**Date Added:** 2026-02-05

#### Rationale

Selected for session storage based on:
- Sub-millisecond latency for session lookups
- Built-in TTL support for automatic expiration
- Cluster mode for horizontal scaling
- Team familiarity (used in previous projects)

#### Compatibility Notes

- Requires Redis 7.x for JSON support
- Use redis-py 5.0+ for async support
- Configure max memory policy to `allkeys-lru`

#### Related Technologies

- Python redis-py client
- RedisInsight for monitoring

#### Reference

- [Redis Documentation](https://redis.io/docs/)
- [ADR-005](decisions/ADR-005-session-storage.md) - Session storage decision
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Duplicate entry | Tech already in stack | Update version or clarify scope |
| Version conflict | Incompatible versions | Document in compatibility notes |
| Category unclear | Tech spans categories | List primary category, note secondary |
