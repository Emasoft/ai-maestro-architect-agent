# Docker Experimentation

ALL experiments MUST run in Docker containers.

---

## Table of Contents

- 1. Why Docker is Required
- 2. Container Structure Template
- 3. docker-compose.yml Template
- 4. Container Cleanup Procedure

---

## 1. Why Docker is Required

| Concern | Docker Solution |
|---------|-----------------|
| **Reproducibility** | Same environment across runs, no "works on my machine" |
| **Security** | Isolated from host system, sandboxed execution |
| **Controlled environment** | Pinned dependencies, known state |
| **Clean teardown** | Container deletion removes all artifacts |
| **Parallelization** | Multiple experiments in isolated containers |

---

## 2. Container Structure Template

```
experiments/exp-[id]/
├── docker-compose.yml       # Orchestrates experiment containers
├── Dockerfile.testbed-a     # Container for approach A
├── Dockerfile.testbed-b     # Container for approach B
├── Dockerfile.testbed-c     # Container for approach C
├── testbed-a/
│   └── main.py
├── testbed-b/
│   └── main.py
├── testbed-c/
│   └── main.py
├── benchmark/
│   └── run_all.sh           # Runs all testbeds, collects metrics
└── RESULTS.md
```

---

## 3. docker-compose.yml Template

```yaml
version: "3.8"
services:
  testbed-a:
    build:
      context: .
      dockerfile: Dockerfile.testbed-a
    volumes:
      - ./results:/results
    environment:
      - EXPERIMENT_ID=exp-[id]
      - APPROACH=A
  testbed-b:
    build:
      context: .
      dockerfile: Dockerfile.testbed-b
    volumes:
      - ./results:/results
    environment:
      - EXPERIMENT_ID=exp-[id]
      - APPROACH=B
  testbed-c:
    build:
      context: .
      dockerfile: Dockerfile.testbed-c
    volumes:
      - ./results:/results
    environment:
      - EXPERIMENT_ID=exp-[id]
      - APPROACH=C
```

---

## 4. Container Cleanup Procedure

After experimentation concludes:

```bash
# Stop and remove all containers
docker-compose down -v --rmi local

# Verify cleanup
docker ps -a | grep exp-[id]  # Should return nothing
```

**IRON RULE**: Experimental code is NEVER committed to the main repository. It exists only in the experiments/ directory (which should be in .gitignore) and is deleted after findings are documented.
