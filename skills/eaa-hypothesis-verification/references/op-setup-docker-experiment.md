---
procedure: support-skill
workflow-instruction: support
---

# Operation: Set Up Docker Experiment Container

## Purpose

Set up an isolated Docker container environment for running experiments to verify claims and hypotheses safely without affecting the host system or production data.

## When to Use

- Starting a new experiment to verify a claim
- Reproducing an issue in isolation
- Testing new APIs or tools safely

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Claim to verify | Assignment | Yes |
| Required tools | Claim analysis | Yes |
| Base image | Analysis | Yes |

## Procedure

### Step 1: Verify Docker Availability

```bash
# Check Docker is running
docker info > /dev/null 2>&1 || echo "ERROR: Docker is not running"

# Check Docker version
docker --version
```

### Step 2: Create Experiment Directory

```bash
CLAIM_NAME="redis-performance"  # Use kebab-case
EXPERIMENT_DIR="experiments/${CLAIM_NAME}"

mkdir -p "${EXPERIMENT_DIR}/data"
mkdir -p "${EXPERIMENT_DIR}/scripts"
mkdir -p "${EXPERIMENT_DIR}/results"
```

### Step 3: Create Dockerfile

```dockerfile
# experiments/<claim-name>/Dockerfile

# Choose appropriate base image
FROM python:3.12-slim

# Set working directory
WORKDIR /experiment

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy experiment scripts
COPY scripts/ ./scripts/

# Default command
CMD ["python", "scripts/run_experiment.py"]
```

### Step 4: Create docker-compose.yml (if services needed)

```yaml
# experiments/<claim-name>/docker-compose.yml

version: '3.8'

services:
  experiment:
    build: .
    volumes:
      - ./data:/experiment/data
      - ./results:/experiment/results
    environment:
      - EXPERIMENT_NAME=${CLAIM_NAME}
    depends_on:
      - redis  # Example dependency

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### Step 5: Create requirements.txt

```txt
# experiments/<claim-name>/requirements.txt

# Core experiment dependencies
pytest==8.0.0
matplotlib==3.8.0
pandas==2.1.0

# Claim-specific dependencies
redis==5.0.0  # Example for Redis experiment
```

### Step 6: Build Container

```bash
cd "${EXPERIMENT_DIR}"

# Build single container
docker build -t "experiment-${CLAIM_NAME}" .

# Or with docker-compose
docker-compose build
```

### Step 7: Verify Container Works

```bash
# Test container starts
docker run --rm "experiment-${CLAIM_NAME}" python --version

# Test with docker-compose
docker-compose up -d
docker-compose ps
docker-compose down
```

## Output

| File | Content |
|------|---------|
| `experiments/<claim>/Dockerfile` | Container definition |
| `experiments/<claim>/docker-compose.yml` | Service composition (if needed) |
| `experiments/<claim>/requirements.txt` | Dependencies |
| `experiments/<claim>/scripts/` | Experiment scripts |
| `experiments/<claim>/data/` | Input data |
| `experiments/<claim>/results/` | Output directory |

## Verification Checklist

- [ ] Docker is running
- [ ] Experiment directory created
- [ ] Dockerfile created with appropriate base image
- [ ] docker-compose.yml created (if services needed)
- [ ] requirements.txt lists all dependencies
- [ ] Container builds successfully
- [ ] Container runs without errors
- [ ] Volumes mounted correctly

## Example

```bash
# Set up experiment for Redis performance claim
CLAIM_NAME="redis-vs-dict-performance"

mkdir -p experiments/${CLAIM_NAME}/{data,scripts,results}

cat > experiments/${CLAIM_NAME}/Dockerfile << 'EOF'
FROM python:3.12-slim
WORKDIR /experiment
RUN pip install redis pytest
COPY scripts/ ./scripts/
CMD ["python", "scripts/benchmark.py"]
EOF

cat > experiments/${CLAIM_NAME}/docker-compose.yml << 'EOF'
version: '3.8'
services:
  experiment:
    build: .
    depends_on:
      - redis
  redis:
    image: redis:7-alpine
EOF

cd experiments/${CLAIM_NAME}
docker-compose build
docker-compose up -d
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Docker daemon not running | Service stopped | `sudo systemctl start docker` or start Docker Desktop |
| Build fails | Missing dependencies | Check Dockerfile and requirements |
| Container exits immediately | Missing CMD or error | Check container logs |
| Port conflict | Port already in use | Change port mapping in compose file |
