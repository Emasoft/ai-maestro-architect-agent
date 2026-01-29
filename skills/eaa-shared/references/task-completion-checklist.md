# Task Completion Checklist (Architect Agent)

## Before Reporting Task Complete

STOP and verify ALL of the following:

### 1. Acceptance Criteria Met
- [ ] ALL acceptance criteria from task definition satisfied
- [ ] Evidence documented for each criterion
- [ ] No "partial" or "mostly" completions
- [ ] Design decisions documented with rationale

### 2. Quality Gates Passed
- [ ] Linting passed (ruff check, eslint)
- [ ] Type checking passed (mypy, pyright)
- [ ] Tests pass (pytest, jest)
- [ ] No regressions introduced
- [ ] Architecture diagrams validated

### 3. Architecture Verification
- [ ] Design patterns applied correctly
- [ ] SOLID principles followed
- [ ] No circular dependencies introduced
- [ ] Component boundaries clearly defined
- [ ] Data flow documented
- [ ] Error handling strategy defined
- [ ] Scalability considerations addressed
- [ ] Security implications reviewed

### 4. Documentation Updated
- [ ] Code comments explain WHY (not just what)
- [ ] README updated if behavior changed
- [ ] CHANGELOG entry added (if applicable)
- [ ] Architecture Decision Records (ADRs) created
- [ ] System diagrams updated
- [ ] API contracts documented

### 5. Handoff Prepared
- [ ] Handoff document written to docs_dev/handoffs/
- [ ] Next steps clearly defined
- [ ] AI Maestro message queued
- [ ] Implementation guidelines provided

### 6. GitHub Updated (if applicable)
- [ ] PR created/updated with description
- [ ] Issue comments added with progress
- [ ] Labels updated to reflect status
- [ ] Projects board item moved

### 7. Session Memory Updated
- [ ] activeContext.md reflects completed work
- [ ] progress.md has completion entry
- [ ] patterns.md captures any new learnings
- [ ] Design decisions recorded

## Verification Loop

Before marking complete, ask yourself:

1. "If I was a different agent reading this, would I know what was done?"
2. "Is there any ambiguity about what 'done' means?"
3. "Did I actually test this, or am I assuming it works?"
4. "Are there edge cases I didn't handle?"
5. "Can another developer implement this from my design?"
6. "Did I document the WHY, not just the WHAT?"

If ANY answer is uncertain, the task is NOT complete. Continue work.

## Common Traps (Architect-Specific)

| Trap | Reality |
|------|---------|
| "Design looks good" | Does NOT equal "design validated" |
| "Pattern applied" | Does NOT equal "pattern applied correctly" |
| "Diagram created" | Does NOT equal "diagram accurate" |
| "Should scale" | Does NOT equal "proven to scale" |
| "Follows best practices" | Does NOT equal "appropriate for this context" |
| "Tests compile" | Does NOT equal "tests pass" |
| "Should work" | Does NOT equal "verified working" |
| "Almost done" | Does NOT equal "done" |

## Completion Report Format

When reporting completion:

```yaml
status: COMPLETE
task_id: <uuid>
summary: <1-2 sentences>
evidence:
  - <what proves it's done>
  - <diagram links, ADR references>
  - <validation results>
files_changed:
  - <path:lines>
design_decisions:
  - decision: <what was decided>
    rationale: <why this choice>
    alternatives: <what was rejected and why>
patterns_applied:
  - pattern: <name>
    location: <where>
    reason: <why>
next_steps: <what happens next>
handoff: <path to handoff doc>
implementation_notes: <guidance for implementers>
```

## Pre-Completion Checklist for Architects

Before declaring ANY architecture task complete:

1. **Validate against requirements** - Does design actually solve the problem?
2. **Review component boundaries** - Are responsibilities clearly separated?
3. **Check data flow** - Is data transformation explicit and documented?
4. **Consider failure modes** - What happens when things go wrong?
5. **Document trade-offs** - Every decision has pros and cons
6. **Provide implementation guidance** - Implementers need concrete direction
7. **Prepare handoff** - Include ADRs, diagrams, and constraints

## Architecture-Specific Verification

### Design Decisions
- [ ] All major decisions documented in ADRs
- [ ] Trade-offs explicitly stated
- [ ] Alternatives considered and documented
- [ ] Constraints clearly identified
- [ ] Assumptions documented

### Component Design
- [ ] Single responsibility principle followed
- [ ] Dependencies flow in correct direction
- [ ] Interfaces defined before implementations
- [ ] Error boundaries established
- [ ] Testability considered

### System Design
- [ ] Scalability approach documented
- [ ] Performance considerations addressed
- [ ] Security review completed
- [ ] Monitoring and observability planned
- [ ] Deployment strategy defined

### Documentation
- [ ] Architecture diagrams current
- [ ] Data models documented
- [ ] API contracts specified
- [ ] Error codes defined
- [ ] Configuration documented

## When to Escalate vs Complete

| Situation | Action |
|-----------|--------|
| All criteria met, verified | Mark COMPLETE |
| 1+ criteria unmet but fixable | Continue work, do NOT mark complete |
| Conflicting requirements | Mark BLOCKED, escalate for clarification |
| Technical constraint discovered | Mark BLOCKED, document constraint |
| Requires user decision | Mark WAITING, present options |
| Design review needed | Mark WAITING, request review |
