---
procedure: support-skill
workflow-instruction: support
---

# Operation: Design Experiment with Multiplicity Rule


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: State the Hypothesis](#step-1-state-the-hypothesis)
- [Hypothesis](#hypothesis)
  - [Step 2: Identify Minimum 3 Approaches](#step-2-identify-minimum-3-approaches)
  - [Step 3: Design Each Approach](#step-3-design-each-approach)
  - [Approach A: <Name> (Control)](#approach-a-name-control)
  - [Step 4: Define Measurement Protocol](#step-4-define-measurement-protocol)
- [Measurement Protocol](#measurement-protocol)
  - [Metrics to Collect](#metrics-to-collect)
  - [Test Parameters](#test-parameters)
  - [Environment Controls](#environment-controls)
  - [Step 5: Create Experiment Matrix](#step-5-create-experiment-matrix)
- [Experiment Matrix](#experiment-matrix)
  - [Step 6: Create Experiment Script Template](#step-6-create-experiment-script-template)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example](#example)
- [Hypothesis](#hypothesis)
  - [Approach A: In-Memory Dict (Control)](#approach-a-in-memory-dict-control)
  - [Approach B: Redis (Claimed)](#approach-b-redis-claimed)
  - [Approach C: Redis with Connection Pool (Alternative)](#approach-c-redis-with-connection-pool-alternative)
- [Metrics](#metrics)
- [Error Handling](#error-handling)

## Purpose

Design an experiment that tests multiple approaches (minimum 3) to verify a claim, following the Multiplicity Rule for evidence-based selection.

## When to Use

- Designing experiment methodology
- Evaluating multiple solutions to a problem
- Testing performance claims

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Claim to verify | Assignment | Yes |
| Success criteria | Analysis | Yes |
| Available approaches | Research | Yes |

## Procedure

### Step 1: State the Hypothesis

Document the claim being tested:

```markdown
## Hypothesis

**Claim:** "<Exact claim being tested>"
**Source:** <Where this claim came from>
**TBV Status:** To Be Verified

**Expected Outcome:**
<What the claim predicts will happen>

**Verification Criteria:**
- <Measurable criterion 1>
- <Measurable criterion 2>
```

### Step 2: Identify Minimum 3 Approaches

The Multiplicity Rule requires testing at least 3 different approaches.

**Approach Categories:**

| Category | Description |
|----------|-------------|
| **Control** | Baseline/naive implementation |
| **Claimed** | The approach described in the claim |
| **Alternative** | Different approach to same problem |
| **Optimized** | Enhanced version of claimed approach |

### Step 3: Design Each Approach

For each approach, document:

```markdown
### Approach A: <Name> (Control)

**Description:** <What this approach does>

**Implementation:**
```python
def approach_a():
    # Implementation details
    pass
```

**Expected Performance:**
- Time: <estimate>
- Memory: <estimate>

**Pros:**
- <advantage>

**Cons:**
- <disadvantage>
```

### Step 4: Define Measurement Protocol

```markdown
## Measurement Protocol

### Metrics to Collect

| Metric | Unit | How Measured |
|--------|------|--------------|
| Execution time | milliseconds | `time.perf_counter()` |
| Memory usage | bytes | `tracemalloc` |
| Throughput | ops/second | operations / time |
| Error rate | percentage | errors / total |

### Test Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Iterations | 1000 | Statistical significance |
| Warmup runs | 100 | Eliminate cold start |
| Data size | 10000 | Representative workload |

### Environment Controls

- [ ] Same hardware for all tests
- [ ] Same Docker container
- [ ] No concurrent processes
- [ ] Fixed random seed (if applicable)
```

### Step 5: Create Experiment Matrix

```markdown
## Experiment Matrix

| Test ID | Approach | Data Size | Iterations | Notes |
|---------|----------|-----------|------------|-------|
| T1 | A (Control) | 1000 | 1000 | Baseline |
| T2 | B (Claimed) | 1000 | 1000 | Main test |
| T3 | C (Alternative) | 1000 | 1000 | Comparison |
| T4 | A (Control) | 10000 | 1000 | Scale test |
| T5 | B (Claimed) | 10000 | 1000 | Scale test |
| T6 | C (Alternative) | 10000 | 1000 | Scale test |
```

### Step 6: Create Experiment Script Template

```python
# scripts/run_experiment.py

import time
import tracemalloc
import json
from dataclasses import dataclass
from typing import Callable, List

@dataclass
class Result:
    approach: str
    metric: str
    value: float
    unit: str
    parameters: dict

def measure_time(func: Callable, iterations: int) -> float:
    """Measure average execution time."""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    return (elapsed / iterations) * 1000  # milliseconds

def measure_memory(func: Callable) -> int:
    """Measure peak memory usage."""
    tracemalloc.start()
    func()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak

def run_approach(name: str, func: Callable, params: dict) -> List[Result]:
    """Run all measurements for one approach."""
    results = []

    # Warmup
    for _ in range(params.get('warmup', 100)):
        func()

    # Time measurement
    avg_time = measure_time(func, params['iterations'])
    results.append(Result(
        approach=name,
        metric='execution_time',
        value=avg_time,
        unit='ms',
        parameters=params
    ))

    # Memory measurement
    peak_memory = measure_memory(func)
    results.append(Result(
        approach=name,
        metric='peak_memory',
        value=peak_memory,
        unit='bytes',
        parameters=params
    ))

    return results

def approach_a():
    """Control: Naive implementation."""
    pass  # Implement

def approach_b():
    """Claimed: Implementation from claim."""
    pass  # Implement

def approach_c():
    """Alternative: Different approach."""
    pass  # Implement

if __name__ == '__main__':
    params = {
        'iterations': 1000,
        'warmup': 100,
        'data_size': 10000
    }

    all_results = []
    all_results.extend(run_approach('A (Control)', approach_a, params))
    all_results.extend(run_approach('B (Claimed)', approach_b, params))
    all_results.extend(run_approach('C (Alternative)', approach_c, params))

    # Save results
    with open('results/experiment_results.json', 'w') as f:
        json.dump([r.__dict__ for r in all_results], f, indent=2)
```

## Output

| File | Content |
|------|---------|
| `experiments/<claim>/DESIGN.md` | Experiment design document |
| `experiments/<claim>/scripts/run_experiment.py` | Experiment script |

## Verification Checklist

- [ ] Hypothesis clearly stated
- [ ] At least 3 approaches identified
- [ ] Each approach documented with pros/cons
- [ ] Measurement metrics defined
- [ ] Test parameters specified
- [ ] Environment controls documented
- [ ] Experiment matrix created
- [ ] Script template ready

## Example

```markdown
## Hypothesis

**Claim:** "Redis caches API responses 10x faster than in-memory dict"
**Source:** Blog post by Developer X
**TBV Status:** To Be Verified

### Approach A: In-Memory Dict (Control)
Python dict as cache.

### Approach B: Redis (Claimed)
Redis server via redis-py.

### Approach C: Redis with Connection Pool (Alternative)
Redis with persistent connections.

## Metrics
- Read latency (ms)
- Write latency (ms)
- Throughput (ops/sec)
```

## Error Handling

| Error | Solution |
|-------|----------|
| Fewer than 3 approaches | Add "do nothing" or naive baseline |
| Cannot measure metric | Use proxy metric or explain limitation |
| Approaches not comparable | Ensure same input/output contract |
