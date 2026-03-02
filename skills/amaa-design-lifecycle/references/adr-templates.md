# ADR Templates

This document provides Architecture Decision Record (ADR) templates extracted from the EAA Architect Main Agent.

## Standard ADR Template

```markdown
# ADR [NUMBER]: [TITLE]

**Date:** [YYYY-MM-DD]
**Status:** Proposed | Accepted | Deprecated | Superseded by [ADR-XXX]
**Deciders:** [Names/roles]
**Context:** [Project/module]

## Context
[What is the issue we're trying to solve? Include relevant background, constraints, requirements.]

## Decision
[What is the decision we've made? Be specific and concrete.]

## Alternatives Considered

### Alternative 1: [NAME]
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

### Alternative 2: [NAME]
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

## Rationale
[Why did we choose this decision over the alternatives? What trade-offs did we accept?]

## Consequences

### Positive
- Positive consequence 1
- Positive consequence 2

### Negative
- Negative consequence 1 (mitigation: [STRATEGY])
- Negative consequence 2 (mitigation: [STRATEGY])

### Neutral
- Neutral consequence 1
- Neutral consequence 2

## Related Decisions
- Related to [ADR-XXX]
- Supersedes [ADR-XXX]
- Superseded by [ADR-XXX]

## Notes
[Any additional context, references, or follow-up items.]
```

## Usage Guidelines

**Location:** ADRs should be stored in `docs_dev/design/adrs/`

**When to Create:** See the "When to Create ADR vs Just Document Decision" section in the main design lifecycle documentation.

**Status Values:**
- **Proposed:** Decision is under consideration
- **Accepted:** Decision has been approved and is in effect
- **Deprecated:** Decision is no longer recommended but may still be in use
- **Superseded by [ADR-XXX]:** Decision has been replaced by a newer ADR

**Key Principles:**
1. Document the **context** before the decision
2. List **alternatives considered** with honest pros/cons
3. Explain **rationale** for the chosen approach
4. Identify both **positive and negative** consequences
5. Document **mitigations** for negative consequences
6. Link **related decisions** for traceability
