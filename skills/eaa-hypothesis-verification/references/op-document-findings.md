---
procedure: support-skill
workflow-instruction: support
---

# Operation: Document Findings in Experimentation Report

## Purpose

Create a comprehensive experimentation report documenting the hypothesis, methodology, results, and conclusions from the experiment.

## When to Use

- After completing experiment execution
- Before archiving experiment
- When reporting to orchestrator

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Aggregated results | Experiment execution | Yes |
| Experiment design | DESIGN.md | Yes |
| Data quality report | Execution phase | Yes |

## Procedure

### Step 1: Create Report Structure

Create `experiments/<claim-name>/REPORT.md`:

```markdown
# Experimentation Report: <Claim Name>

**Status:** VERIFIED | UNVERIFIED | PARTIALLY VERIFIED
**Date:** YYYY-MM-DD
**Experimenter:** <Name/Agent>
**Duration:** <Time spent>

---

## Executive Summary

<2-3 sentence summary of what was tested and the conclusion>

---

## Hypothesis

### Original Claim

"<Exact claim being tested>"

### Source

<Where this claim came from: blog, docs, colleague, etc.>

### Initial Status

TBV (To Be Verified)

---

## Methodology

### Approaches Tested

| Approach | Description | Purpose |
|----------|-------------|---------|
| A | <description> | Control/Baseline |
| B | <description> | Claimed approach |
| C | <description> | Alternative |

### Measurement Protocol

| Metric | Unit | Collection Method |
|--------|------|-------------------|
| <metric> | <unit> | <method> |

### Test Parameters

| Parameter | Value |
|-----------|-------|
| Iterations per run | <N> |
| Number of runs | <N> |
| Warmup iterations | <N> |
| Data size | <N> |

### Environment

| Property | Value |
|----------|-------|
| Docker image | <image:tag> |
| CPU | <cores> |
| Memory | <GB> |
| OS | <platform> |

---

## Results

### Summary Table

| Approach | <Metric 1> | <Metric 2> | <Metric 3> |
|----------|------------|------------|------------|
| A (Control) | <value +/- stdev> | <value> | <value> |
| B (Claimed) | <value +/- stdev> | <value> | <value> |
| C (Alternative) | <value +/- stdev> | <value> | <value> |

### Detailed Results

#### Approach A: <Name>

- **<Metric 1>:** <mean> +/- <stdev> (median: <median>, range: <min>-<max>)
- **<Metric 2>:** <values>

**Observations:**
<Notable behaviors or patterns observed>

#### Approach B: <Name>

<Same structure>

#### Approach C: <Name>

<Same structure>

### Visualization

<Include charts if applicable>

```
Approach A: ████████████████████ 45ms
Approach B: ████████ 18ms
Approach C: ██████████ 22ms
```

### Statistical Analysis

| Comparison | Difference | Significance |
|------------|------------|--------------|
| B vs A | <X>% faster | p < 0.05 |
| C vs A | <Y>% faster | p < 0.05 |
| B vs C | <Z>% faster | p > 0.05 (not significant) |

---

## Analysis

### Key Findings

1. **Finding 1:** <What the data shows>
2. **Finding 2:** <What the data shows>
3. **Finding 3:** <What the data shows>

### Claim Evaluation

**Original claim:** "<claim>"

**Evidence:**
- <Evidence point supporting or refuting>
- <Evidence point supporting or refuting>

**Conditions:**
- <Under what conditions is the claim true/false>

---

## Classification

### Final Status: <VERIFIED | UNVERIFIED | PARTIALLY VERIFIED>

### Justification

<Why this classification was chosen>

### Conditions (if PARTIALLY VERIFIED)

The claim is valid when:
- <Condition 1>
- <Condition 2>

The claim is NOT valid when:
- <Condition 1>
- <Condition 2>

---

## Recommendations

### For Implementation

<If claim is verified, how should it be implemented?>

### For Further Investigation

<If more research is needed>

---

## Limitations

- <Limitation of this experiment>
- <What was not tested>
- <Potential confounding factors>

---

## Appendix

### A. Raw Data Location

`results/raw/`

### B. Scripts Used

| Script | Purpose |
|--------|---------|
| `scripts/run_experiment.py` | Main experiment |
| `scripts/aggregate_results.py` | Data aggregation |

### C. Data Quality Notes

<Any issues with data quality and how addressed>

---

## References

- <Sources consulted>
```

### Step 2: Generate Visualizations

```python
# scripts/generate_charts.py

import json
import matplotlib.pyplot as plt

def create_comparison_chart(aggregated: dict, metric: str, output_file: str):
    """Create bar chart comparing approaches."""
    approaches = list(aggregated.keys())
    means = [aggregated[a][metric]['mean'] for a in approaches]
    stdevs = [aggregated[a][metric]['stdev'] for a in approaches]

    plt.figure(figsize=(10, 6))
    plt.bar(approaches, means, yerr=stdevs, capsize=5)
    plt.ylabel(f'{metric}')
    plt.title(f'Comparison: {metric}')
    plt.savefig(output_file)
    plt.close()
```

### Step 3: Calculate Statistical Significance

```python
# scripts/statistics.py

from scipy import stats

def compare_approaches(data_a: list, data_b: list) -> dict:
    """Compare two approaches statistically."""
    t_stat, p_value = stats.ttest_ind(data_a, data_b)

    mean_diff = statistics.mean(data_b) - statistics.mean(data_a)
    percent_diff = (mean_diff / statistics.mean(data_a)) * 100

    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'mean_difference': mean_diff,
        'percent_difference': percent_diff
    }
```

### Step 4: Finalize Report

Review checklist:
- [ ] All sections filled
- [ ] Data matches claims
- [ ] Visualizations included
- [ ] Classification justified
- [ ] Limitations acknowledged

## Output

| File | Content |
|------|---------|
| `experiments/<claim>/REPORT.md` | Complete experiment report |
| `experiments/<claim>/results/charts/` | Visualization files |

## Verification Checklist

- [ ] Executive summary written
- [ ] Hypothesis clearly stated
- [ ] Methodology documented
- [ ] Results table complete
- [ ] Statistical analysis included
- [ ] Classification justified
- [ ] Limitations acknowledged
- [ ] Report reviewed for accuracy

## Example

```markdown
# Experimentation Report: Redis vs Dict Performance

**Status:** UNVERIFIED
**Date:** 2026-02-05

## Executive Summary

The claim that "Redis caches 10x faster than dict" was UNVERIFIED. Testing showed in-memory dict is 150x faster for simple caching scenarios due to network overhead in Redis.

## Results Summary

| Approach | Avg Read Time |
|----------|---------------|
| Dict (Control) | 0.001ms |
| Redis | 0.15ms |
| Redis Pooled | 0.08ms |

## Classification: UNVERIFIED

The claim is false for single-instance applications. Redis only provides benefits in distributed scenarios.
```

## Error Handling

| Error | Solution |
|-------|----------|
| Insufficient data | Re-run experiments |
| Inconclusive results | Add more approaches or metrics |
| Statistical test fails | Use non-parametric test |
