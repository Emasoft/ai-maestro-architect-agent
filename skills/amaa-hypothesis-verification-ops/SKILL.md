---
name: amaa-hypothesis-verification-ops
description: "Use when applying multiplicity rule or formatting experiment outputs. Trigger with verification ops request."
context: fork
user-invocable: false
agent: amaa-architect-main-agent
---

# Hypothesis Verification Operations

## Overview

Operational references for hypothesis verification: the multiplicity rule for testing 3+ approaches, report templates, and quick-reference classifications.

## Prerequisites

- Familiarity with the core hypothesis verification workflow

## Instructions

1. Apply the Multiplicity Rule: generate 3+ candidate approaches
2. Use output templates to document experiment results
3. Classify findings using status codes from quick reference
4. Archive prototypes only when code is essential to explain findings

## Checklist

Copy this checklist and track your progress:

- [ ] Generate 3+ candidate approaches per hypothesis
- [ ] Document each experiment using the report template
- [ ] Classify results (VERIFIED/UNVERIFIED/PARTIALLY VERIFIED)
- [ ] Archive or delete experimental code per policy

## Reference Documents

| Document | Content |
|----------|---------|
| [multiplicity-rule.md](references/multiplicity-rule.md) | The Multiplicity Process, Example: Implementing a Paper Algorithm, Iterative Selection Workflow |
| [output-templates.md](references/output-templates.md) | Experiment Directory Structure, Experimentation Report Template, Hypothesis, Candidates Tested, Experimental Setup, Results, Evidence-Based Conclusions |
| [quick-reference.md](references/quick-reference.md) | Status Classifications, Implementation vs Experimental Code, Workflow Integration Points, IRON RULES Summary, Examples |

## Examples

Example: `Test 3+ Redis configurations in Docker, measure latency, select winner by evidence, document in REPORT.md`

## Error Handling

| Issue | Fix |
|-------|-----|
| Too few candidates | Add approaches until 3+ exist |
| Inconclusive results | Increase sample size or iterations |

## Output

| Type | Description |
|------|-------------|
| Experimentation Report | `experiments/<claim>/REPORT.md` with template |
| Prototype Archive | `docs_dev/experiments/<claim>/prototypes/` if needed |

## Resources

See Reference Documents table above.
