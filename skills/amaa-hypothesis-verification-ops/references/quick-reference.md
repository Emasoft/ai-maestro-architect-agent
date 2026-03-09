# Hypothesis Verification - Quick Reference

## Table of Contents

- [Status Classifications](#status-classifications)
- [Implementation vs Experimental Code](#implementation-vs-experimental-code)
- [Workflow Integration Points](#workflow-integration-points)
- [IRON RULES Summary](#iron-rules-summary)
- [Examples](#examples)
## Status Classifications

| Status | Meaning | Safe to Rely On? |
|--------|---------|------------------|
| **VERIFIED** | Experimentally confirmed | YES |
| **UNVERIFIED** | Tested but failed to match claim | NO (dangerous) |
| **PARTIALLY VERIFIED** | True under specific conditions | YES (with conditions) |
| **TBV** | Not yet tested | NO (unknown risk) |

## Implementation vs Experimental Code

| Implementation Code | Experimental Code |
|--------------------|-------------------|
| Permanent (committed) | Ephemeral (deleted after) |
| Production-ready | Throwaway testbed |
| Follows specifications | Generates specifications |
| One chosen solution | Multiple solutions compared |
| Part of delivery | Part of decision-making |

## Workflow Integration Points

| Workflow | Trigger | Experimenter Action |
|----------|---------|---------------------|
| BUILD | Architecture decision needs validation | Validates with testbeds |
| DEBUG | Root cause unclear or fix uncertain | Reproduces in isolation, tests fixes |
| REVIEW | Performance concerns or architectural questions | Benchmarks alternatives |

## IRON RULES Summary

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
