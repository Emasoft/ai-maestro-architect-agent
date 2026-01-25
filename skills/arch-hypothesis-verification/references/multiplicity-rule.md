# Multiplicity and Selection Rule

**IRON RULE**: NEVER test only one or two solutions. ALWAYS test multiple varied approaches.

---

## Table of Contents

- 1. The Multiplicity Process
- 2. Example: Implementing a Paper Algorithm
- 3. Iterative Selection Workflow

---

## 1. The Multiplicity Process

```
┌─────────────────────────────────────────────────────────────┐
│  MULTIPLY: Generate N candidate approaches (N >= 3)        │
│  ↓                                                          │
│  EXPERIMENT: Test each candidate in isolation               │
│  ↓                                                          │
│  MEASURE: Record success, failures, benchmarks              │
│  ↓                                                          │
│  SELECT: Choose the winner based on evidence                │
│  ↓                                                          │
│  ITERATE: Use winner as base, generate N new variants       │
│  ↓                                                          │
│  REPEAT until optimal solution found or diminishing returns │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Example: Implementing a Paper Algorithm

**Wrong approach (single path)**:
```
Read paper → Implement algorithm → Done
```

**Correct approach (multiplicity and selection)**:
```
Iteration 1:
  - Approach A: Direct translation from pseudocode
  - Approach B: Optimized with SIMD instructions
  - Approach C: Approximation with neural network
  - Approach D: Divide-and-conquer variant
  → Benchmark all → Select B (fastest)

Iteration 2 (starting from B):
  - Variant B1: B with cache-friendly memory layout
  - Variant B2: B with parallel processing
  - Variant B3: B with lazy evaluation
  → Benchmark all → Select B2 (best throughput)

Iteration 3 (starting from B2):
  - Variant B2a: B2 with work-stealing scheduler
  - Variant B2b: B2 with fixed thread pool
  - Variant B2c: B2 with async/await
  → Benchmark all → Select B2a (optimal)

Final: B2a is the evidence-based optimal implementation
```

---

## 3. Iterative Selection Workflow

| Phase | Action | Output |
|-------|--------|--------|
| MULTIPLY | Generate 3+ candidate approaches | List of candidates |
| EXPERIMENT | Build testbed for each candidate | Docker containers |
| MEASURE | Run experiments, collect data | Benchmark results |
| SELECT | Choose winner based on evidence | Single winner |
| ITERATE | Generate variants of winner | New candidate list |
| REPEAT | Continue until optimal or diminishing returns | Final solution |

**Why minimum 3 approaches?**

| Number | Risk |
|--------|------|
| 1 | No comparison - you can't know if it's good |
| 2 | Binary choice - may miss better alternatives |
| 3+ | Real comparison - evidence-based selection |

**When to stop iterating**:
- Performance improvements < 5% between iterations
- All variations produce similar results
- Time budget exhausted
- Clear winner with no close contenders
