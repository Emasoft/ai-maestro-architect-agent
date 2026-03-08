---
name: amaa-hypothesis-verification
description: Use when verifying technical claims through Docker-isolated experiments. Trigger with hypothesis test or experiment request.
agent: amaa-architect-main-agent
context: fork
user-invocable: false
---

# Hypothesis Verification Skill

## Overview

Verify claims through controlled Docker experimentation. Everything is "To Be Verified" (TBV) until you personally test it. Claims from any source require experimental confirmation.

## Prerequisites

- Docker installed and running
- Write access to experiment output directories
- Understanding of the claim to be verified

## Checklist

Copy this checklist and track your progress:

- [ ] Identify the claim and mark as TBV
- [ ] Set up Docker container for isolated testing
- [ ] Design experiment with 3+ approaches (Multiplicity Rule)
- [ ] Execute experiments and collect measurements
- [ ] Classify: VERIFIED / UNVERIFIED / PARTIALLY VERIFIED
- [ ] Document findings in experimentation report
- [ ] Clean up containers; archive prototype if valuable

## Instructions

1. Identify the claim and mark as TBV
2. Set up Docker container for isolated testing
3. Design experiment with 3+ approaches (Multiplicity Rule)
4. Execute experiments and collect measurements
5. Classify: VERIFIED / UNVERIFIED / PARTIALLY VERIFIED
6. Document findings in experimentation report
7. Clean up containers; archive prototype if valuable

## Reference Documents

| Document | Content |
|----------|---------|
| docker-experimentation.md | Container setup and templates |
| researcher-vs-experimenter.md | TBV principle and workflow |
| experiment-scenarios.md | Five verification case types |
| multiplicity-rule.md | Multi-approach selection process |
| output-templates.md | Report and directory templates |
| quick-reference.md | Status rules and iron rules |

## Examples

```
Claim: "Redis caches responses 10x faster than in-memory dict" (TBV)
-> Docker container with Redis + Python
-> Test 3 approaches: dict, Redis, Redis pooled (1000 iterations)
-> Result: Dict 0.001ms, Redis 0.15ms, Redis pooled 0.08ms
-> Classification: UNVERIFIED (Redis slower for simple cases)
```

## Error Handling

| Error | Solution |
|-------|----------|
| Docker not available | Start Docker Desktop or docker service |
| Container cleanup failed | Run `docker system prune` |
| Experiment inconclusive | Increase sample size, reduce variables |
| Conflicting results | Standardize container configuration |

## Output

| Artifact | Location |
|----------|----------|
| Experimentation Report | `experiments/<claim-name>/REPORT.md` |
| Measurement Data | `experiments/<claim-name>/data/` |
| Prototype Archive | `prototypes/<claim-name>/` (if valuable) |

## Resources

- docker-experimentation.md — Container setup and templates
- multiplicity-rule.md — Multi-approach selection process
- output-templates.md — Report and directory templates
- quick-reference.md — Status rules and iron rules
