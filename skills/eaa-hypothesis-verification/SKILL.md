---
name: eaa-hypothesis-verification
description: Use when verifying claims through Docker experimentation. Applies TBV principle to test claims before relying on them. Trigger with experiment setup or claim verification.
version: 1.0.0
compatibility: Requires AI Maestro installed.
agent: test-engineer
context: fork
---

# Hypothesis Verification Skill

## Overview

Patterns for **personally verifying claims** through controlled Docker experimentation. Use this skill when you need to test whether a claim (from docs, researchers, or developers) is actually true.

**TBV Principle**: Everything is "To Be Verified" until you personally test it. Claims from any source require experimental confirmation before relying on them for decisions.

## Prerequisites

- Docker installed and running
- Write access to experiment output directories
- Understanding of the claim to be verified
- Isolation environment for safe experimentation

## Instructions

1. Identify the claim to be verified (mark as TBV)
2. Set up Docker container for isolated testing
3. Design experiment with multiple approaches (Multiplicity Rule: 3+)
4. Execute experiments and collect measurements
5. Document findings in experimentation report
6. Classify result: VERIFIED, UNVERIFIED, or PARTIALLY VERIFIED
7. Clean up containers and archive prototype if valuable

### Checklist

Copy this checklist and track your progress:

- [ ] Identify the claim to be verified
- [ ] Mark claim as TBV (To Be Verified)
- [ ] Verify Docker is installed and running
- [ ] Create experiment directory: `experiments/<claim-name>/`
- [ ] Set up Docker container for isolated testing
- [ ] Design at least 3 different approaches (Multiplicity Rule)
- [ ] Implement Approach A
- [ ] Implement Approach B
- [ ] Implement Approach C
- [ ] Execute experiments and collect measurements
- [ ] Record raw data in `experiments/<claim-name>/data/`
- [ ] Create experimentation report: `experiments/<claim-name>/REPORT.md`
- [ ] Classify result: VERIFIED / UNVERIFIED / PARTIALLY VERIFIED
- [ ] Document conditions if PARTIALLY VERIFIED
- [ ] Clean up Docker containers
- [ ] Archive prototype if valuable: `prototypes/<claim-name>/`
- [ ] Create README for archived prototype (if applicable)

## Output

| Artifact | Location | Purpose |
|----------|----------|---------|
| **Experimentation Report** | `experiments/<claim-name>/REPORT.md` | Documents hypothesis, approaches tested, measurements, and classification |
| **Status Classification** | Report header | VERIFIED / UNVERIFIED / PARTIALLY VERIFIED / TBV |
| **Measurement Data** | `experiments/<claim-name>/data/` | Raw metrics, logs, benchmark results |
| **Prototype Archive** (if valuable) | `prototypes/<claim-name>/` | Working code with README explaining findings |
| **Docker Cleanup Log** | Terminal output | Confirms containers removed after experiment |

---

## Table of Contents

### Docker Experimentation
For Docker container setup and experiment infrastructure, see [docker-experimentation.md](references/docker-experimentation.md):
- 1. Why Docker is Required
- 2. Container Structure Template
- 3. docker-compose.yml Template
- 4. Container Cleanup Procedure

### Researcher vs Experimenter
For understanding the critical distinction between roles, see [researcher-vs-experimenter.md](references/researcher-vs-experimenter.md):
- 1. The Researcher (What OTHERS say is true)
- 2. The Experimenter (What I can PROVE is true)
- 3. The TBV Principle (To Be Verified)
- 4. Workflow Integration: Researcher → Experimenter

### Experiment Scenarios
For when to invoke the experimenter, see [experiment-scenarios.md](references/experiment-scenarios.md):
- 1. Case 1: Post-Research Validation
- 2. Case 2: Issue Reproduction in Isolation
- 3. Case 3: Architectural Bug Investigation
- 4. Case 4: New API/Tool Evaluation
- 5. Case 5: Fact-Checking Claims (Quick Verification)

### Multiplicity Rule
For the evidence-based selection process, see [multiplicity-rule.md](references/multiplicity-rule.md):
- 1. The Multiplicity Process
- 2. Example: Implementing a Paper Algorithm
- 3. Iterative Selection Workflow

### Output Templates
For experiment documentation and prototype archiving, see [output-templates.md](references/output-templates.md):
- 1. Experiment Directory Structure
- 2. Experimentation Report Template
- 3. Prototype Archive Policy
- 4. Archive README Template

---

## Quick Reference

### Status Classifications

| Status | Meaning | Safe to Rely On? |
|--------|---------|------------------|
| **VERIFIED** | Experimentally confirmed | YES |
| **UNVERIFIED** | Tested but failed to match claim | NO (dangerous) |
| **PARTIALLY VERIFIED** | True under specific conditions | YES (with conditions) |
| **TBV** | Not yet tested | NO (unknown risk) |

### Implementation vs Experimental Code

| Implementation Code | Experimental Code |
|--------------------|-------------------|
| Permanent (committed) | Ephemeral (deleted after) |
| Production-ready | Throwaway testbed |
| Follows specifications | Generates specifications |
| One chosen solution | Multiple solutions compared |
| Part of delivery | Part of decision-making |

### Workflow Integration Points

| Workflow | Trigger | Experimenter Action |
|----------|---------|---------------------|
| BUILD | Architecture decision needs validation | Validates with testbeds |
| DEBUG | Root cause unclear or fix uncertain | Reproduces in isolation, tests fixes |
| REVIEW | Performance concerns or architectural questions | Benchmarks alternatives |

### IRON RULES Summary

1. **Multiplicity**: Always test 3+ approaches
2. **Ephemeral code**: Delete after findings documented
3. **Evidence-based**: Conclusions backed by measurements
4. **Docker isolation**: ALL experiments in containers
5. **Documentation**: 50% output is the report
6. **TBV by default**: Everything unverified until tested

## Examples

### Example 1: Verify API Performance Claim

```
Claim: "Redis caches API responses 10x faster than in-memory dict"
Status: TBV

1. Create Docker container with Redis and Python
2. Implement both approaches:
   - Approach A: In-memory dict cache
   - Approach B: Redis cache
   - Approach C: Redis with connection pooling
3. Run 1000 iterations, measure latency
4. Results:
   - Dict: 0.001ms avg
   - Redis: 0.15ms avg
   - Redis pooled: 0.08ms avg
5. Classification: UNVERIFIED (Redis is slower for simple cases)
6. Conditions: Redis faster only for distributed scenarios
```

### Example 2: Verify Library Compatibility

```
Claim: "Library X works with Python 3.12"
Status: TBV

1. Docker container with Python 3.12
2. Install library X
3. Run test suite
4. Result: Import error on async module
5. Classification: UNVERIFIED
6. Action: Use Python 3.11 or wait for library update
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Docker not available | Docker daemon not running | Start Docker Desktop or docker service |
| Container cleanup failed | Orphaned containers | Run `docker system prune` |
| Experiment inconclusive | Insufficient test iterations | Increase sample size, reduce variables |
| Conflicting results | Environment differences | Standardize container configuration |
| Resource exhaustion | Too many containers | Clean up between experiments |

## Resources

- [docker-experimentation.md](references/docker-experimentation.md) - Container setup and templates
- [researcher-vs-experimenter.md](references/researcher-vs-experimenter.md) - Role distinction
- [experiment-scenarios.md](references/experiment-scenarios.md) - When to invoke experimenter
- [multiplicity-rule.md](references/multiplicity-rule.md) - Evidence-based selection process
- [output-templates.md](references/output-templates.md) - Report and archive templates
