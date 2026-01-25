# Output Templates

Templates for experiment documentation and prototype archiving.

---

## Table of Contents

- 1. Experiment Directory Structure
- 2. Experimentation Report Template
- 3. Prototype Archive Policy
- 4. Archive README Template

---

## 1. Experiment Directory Structure

**50% Code (Ephemeral)**:

```
experiments/
└── exp-2026-01-07-redis-vs-kafka/
    ├── testbed-redis/
    │   └── main.py          # Minimal Redis test
    ├── testbed-kafka/
    │   └── main.py          # Minimal Kafka test
    ├── benchmark.py          # Comparison script
    └── RESULTS.md            # Findings (kept)
```

**After experimentation concludes**: DELETE all code, KEEP only RESULTS.md

**Code lifecycle**:
```
1. CREATE: experiments/exp-[id]/ directory
2. WRITE: Minimal testbed code for each candidate
3. RUN: Execute experiments, collect measurements
4. DOCUMENT: Write RESULTS.md with findings
5. DECIDE: Orchestrator reviews and decides
6. DELETE: Remove all code, keep only RESULTS.md
   - Move RESULTS.md to docs_dev/experiments/
   - Delete experiments/exp-[id]/ directory entirely
```

---

## 2. Experimentation Report Template

```markdown
# Experimentation Report: [Title]

## Hypothesis
What we're testing and why.

## Candidates Tested
| Approach | Description | Rationale |
|----------|-------------|-----------|
| A | ... | ... |
| B | ... | ... |
| C | ... | ... |

## Experimental Setup
- Environment: [specs]
- Data/inputs: [description]
- Metrics measured: [list]

## Results

### Iteration 1
| Approach | Metric 1 | Metric 2 | Metric 3 | Notes |
|----------|----------|----------|----------|-------|
| A | 100ms | 50MB | 95% | Baseline |
| B | 45ms | 80MB | 98% | Fastest |
| C | 200ms | 30MB | 92% | Memory efficient |

**Winner**: B (fastest with acceptable memory)

### Iteration 2 (improving B)
| Variant | Metric 1 | Metric 2 | Metric 3 | Notes |
|---------|----------|----------|----------|-------|
| B1 | 42ms | 75MB | 98% | Slight improvement |
| B2 | 25ms | 85MB | 99% | Significant speedup |
| B3 | 40ms | 60MB | 97% | Memory optimized |

**Winner**: B2 (best throughput)

## Evidence-Based Conclusions

1. **Finding 1**: [Specific, measurable conclusion]
2. **Finding 2**: [Specific, measurable conclusion]
3. **Finding 3**: [Specific, measurable conclusion]

## Recommendation

Based on [N] experiments across [M] iterations:
- **Recommended approach**: [approach]
- **Rationale**: [evidence-based reasoning]
- **Trade-offs**: [what we're accepting]

## Technical Insights

- [Insight 1 discovered during experimentation]
- [Insight 2 discovered during experimentation]
- [Insight 3 discovered during experimentation]

## Appendix: Raw Data

[Benchmark results, logs, measurements]
```

---

## 3. Prototype Archive Policy

**Most experimental code is deleted. Some is preserved as reference prototypes.**

### When to Archive a Prototype

Preserve code ONLY when:

1. **Findings require a working example** - The discovery is too complex to explain without runnable code
2. **Technique demonstration** - Implementers need to see the technique in action
3. **Non-obvious implementation** - The winning approach has subtle details that prose can't capture
4. **Regression test baseline** - The experiment uncovered a bug that needs a reproducible test case

### What to Archive

| Keep | Discard |
|------|---------|
| Core algorithm/technique | Test harness scaffolding |
| Critical configuration | Logging and debugging code |
| Non-obvious edge case handling | Multiple approach variants (keep winner only) |
| Integration points | Benchmark infrastructure |

### Archive Structure

```
docs_dev/experiments/
├── exp-2026-01-07-redis-vs-kafka/
│   ├── RESULTS.md                      # Always kept
│   └── prototypes/                     # Optional archive
│       ├── README.md                   # Why this prototype was kept
│       └── winner-redis-streams/       # Minimal winning approach
│           ├── config.py               # Critical config only
│           └── stream_handler.py       # Core technique only
```

---

## 4. Archive README Template

Every archived prototype MUST include:

```markdown
# Prototype Archive: [Name]

## Why This Prototype Was Preserved

[1-2 sentences explaining why code is needed alongside documentation]

## What This Demonstrates

[Specific technique or finding this code illustrates]

## How Implementers Should Use This

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Files Included

| File | Purpose | Lines |
|------|---------|-------|
| config.py | Critical configuration pattern | 25 |
| stream_handler.py | Core technique implementation | 80 |

## What Was Removed

- Test harnesses (reproducible via docker-compose in RESULTS.md)
- Benchmark infrastructure (results in RESULTS.md)
- Alternative approaches (documented in RESULTS.md)

## Expiration

This prototype may be deleted after: [date or condition]
```

**IRON RULE**: Archived prototypes are REFERENCE MATERIAL, not production code. Implementers study them to understand techniques, then write fresh production code.
