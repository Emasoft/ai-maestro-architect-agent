---
procedure: support-skill
workflow-instruction: support
---

# Operation: Execute Experiments and Collect Measurements

## Purpose

Execute the designed experiment, run all approaches, collect measurements, and store raw data for analysis.

## When to Use

- Running the actual experiment
- Collecting performance measurements
- Gathering data for verification

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Experiment design | DESIGN.md | Yes |
| Docker environment | Setup complete | Yes |
| Measurement scripts | Design phase | Yes |

## Procedure

### Step 1: Verify Environment Ready

```bash
EXPERIMENT_DIR="experiments/<claim-name>"
cd "${EXPERIMENT_DIR}"

# Check Docker environment
docker-compose ps  # All services should be running

# Check results directory exists
mkdir -p results/raw
```

### Step 2: Run Pre-Experiment Checks

```python
# scripts/pre_check.py

def verify_environment():
    """Verify experiment environment is ready."""
    checks = {
        'docker_running': check_docker(),
        'services_up': check_services(),
        'disk_space': check_disk_space(min_gb=1),
        'dependencies': check_dependencies(),
    }

    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise RuntimeError(f"Pre-checks failed: {failed}")

    print("All pre-checks passed")
```

### Step 3: Execute Experiment

```bash
# Run experiment in Docker container
docker-compose run --rm experiment python scripts/run_experiment.py

# Or run interactively for debugging
docker-compose run --rm experiment bash
```

### Step 4: Collect Raw Data

Structure for raw data:

```
results/
  raw/
    run_001/
      approach_a.json
      approach_b.json
      approach_c.json
      system_metrics.json
      timestamp.txt
    run_002/
      ...
```

Data collection script:

```python
# scripts/collect_data.py

import json
import os
from datetime import datetime

def save_run_data(run_id: str, results: dict):
    """Save results from a single experiment run."""
    run_dir = f"results/raw/run_{run_id:03d}"
    os.makedirs(run_dir, exist_ok=True)

    # Save timestamp
    with open(f"{run_dir}/timestamp.txt", 'w') as f:
        f.write(datetime.now().isoformat())

    # Save results by approach
    for approach, data in results.items():
        with open(f"{run_dir}/{approach}.json", 'w') as f:
            json.dump(data, f, indent=2)

    # Save system metrics
    system_metrics = collect_system_metrics()
    with open(f"{run_dir}/system_metrics.json", 'w') as f:
        json.dump(system_metrics, f, indent=2)

def collect_system_metrics():
    """Collect system state during experiment."""
    import platform
    import psutil

    return {
        'platform': platform.platform(),
        'cpu_count': psutil.cpu_count(),
        'memory_total_gb': psutil.virtual_memory().total / (1024**3),
        'memory_available_gb': psutil.virtual_memory().available / (1024**3),
        'timestamp': datetime.now().isoformat()
    }
```

### Step 5: Run Multiple Iterations

For statistical significance, run multiple iterations:

```bash
# Run 5 iterations of the experiment
for i in $(seq 1 5); do
    echo "Running iteration $i..."
    docker-compose run --rm experiment python scripts/run_experiment.py \
        --run-id "$i" \
        --output-dir results/raw
    sleep 5  # Cool down between runs
done
```

### Step 6: Aggregate Results

```python
# scripts/aggregate_results.py

import json
import os
import statistics
from pathlib import Path

def aggregate_runs(results_dir: str) -> dict:
    """Aggregate results from multiple runs."""
    raw_dir = Path(results_dir) / "raw"

    # Collect all measurements by approach and metric
    measurements = {}

    for run_dir in sorted(raw_dir.iterdir()):
        if not run_dir.is_dir():
            continue

        for result_file in run_dir.glob("approach_*.json"):
            with open(result_file) as f:
                data = json.load(f)

            approach = result_file.stem
            if approach not in measurements:
                measurements[approach] = {}

            for metric, value in data.items():
                if metric not in measurements[approach]:
                    measurements[approach][metric] = []
                measurements[approach][metric].append(value)

    # Calculate statistics
    aggregated = {}
    for approach, metrics in measurements.items():
        aggregated[approach] = {}
        for metric, values in metrics.items():
            aggregated[approach][metric] = {
                'mean': statistics.mean(values),
                'median': statistics.median(values),
                'stdev': statistics.stdev(values) if len(values) > 1 else 0,
                'min': min(values),
                'max': max(values),
                'samples': len(values)
            }

    return aggregated

if __name__ == '__main__':
    results = aggregate_runs('results')

    with open('results/aggregated.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("Aggregated results saved to results/aggregated.json")
```

### Step 7: Validate Data Quality

```python
# Check for anomalies in collected data
def validate_data(aggregated: dict) -> list:
    """Validate data quality and return any issues."""
    issues = []

    for approach, metrics in aggregated.items():
        for metric, stats in metrics.items():
            # Check for high variance
            if stats['stdev'] > stats['mean'] * 0.5:
                issues.append(f"{approach}/{metric}: High variance (CV > 50%)")

            # Check for sufficient samples
            if stats['samples'] < 3:
                issues.append(f"{approach}/{metric}: Insufficient samples ({stats['samples']})")

            # Check for outliers
            range_ratio = (stats['max'] - stats['min']) / stats['mean'] if stats['mean'] > 0 else 0
            if range_ratio > 2:
                issues.append(f"{approach}/{metric}: Possible outliers (range > 2x mean)")

    return issues
```

## Output

| File | Content |
|------|---------|
| `results/raw/run_NNN/` | Raw data from each run |
| `results/aggregated.json` | Statistical summary |
| `results/data_quality.txt` | Validation issues |

## Verification Checklist

- [ ] Environment verified before run
- [ ] All approaches executed
- [ ] Multiple iterations completed (minimum 3)
- [ ] Raw data saved for each run
- [ ] System metrics captured
- [ ] Results aggregated
- [ ] Data quality validated
- [ ] No critical anomalies detected

## Example

```bash
# Complete experiment execution
cd experiments/redis-performance

# Verify environment
docker-compose up -d
docker-compose ps

# Run 5 iterations
for i in 1 2 3 4 5; do
    docker-compose run --rm experiment python scripts/run_experiment.py --run-id $i
done

# Aggregate results
docker-compose run --rm experiment python scripts/aggregate_results.py

# View results
cat results/aggregated.json
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Container crashes | Resource exhaustion | Reduce data size or iterations |
| Results vary wildly | Noisy environment | Add more iterations, increase warmup |
| Missing data files | Script error | Check script logs, re-run |
| Services unavailable | Docker network issue | Restart docker-compose |
