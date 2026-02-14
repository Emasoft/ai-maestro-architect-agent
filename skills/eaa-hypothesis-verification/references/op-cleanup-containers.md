---
procedure: support-skill
workflow-instruction: support
---

# Operation: Clean Up Experiment Containers


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Stop Running Containers](#step-1-stop-running-containers)
  - [Step 2: Remove Containers](#step-2-remove-containers)
  - [Step 3: Remove Images (Optional)](#step-3-remove-images-optional)
  - [Step 4: Remove Volumes (Optional)](#step-4-remove-volumes-optional)
  - [Step 5: Clean Unused Resources](#step-5-clean-unused-resources)
  - [Step 6: Verify Cleanup](#step-6-verify-cleanup)
  - [Step 7: Document Cleanup](#step-7-document-cleanup)
- [Cleanup Log](#cleanup-log)
  - [Resources Removed](#resources-removed)
  - [Disk Space Recovered](#disk-space-recovered)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Example](#example)
- [Cleanup Script](#cleanup-script)
- [Error Handling](#error-handling)

## Purpose

Remove Docker containers, images, and volumes created for the experiment to free resources and maintain a clean environment.

## When to Use

- After experiment is complete
- Before starting a new experiment
- When freeing disk space

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Experiment directory | Context | Yes |
| Container names | docker-compose.yml | Yes |

## Procedure

### Step 1: Stop Running Containers

```bash
EXPERIMENT_DIR="experiments/<claim-name>"
cd "${EXPERIMENT_DIR}"

# Stop containers
docker-compose down

# Verify stopped
docker-compose ps
# Should show no running containers
```

### Step 2: Remove Containers

```bash
# Remove stopped containers for this experiment
docker-compose rm -f

# Or remove specific containers
docker rm "experiment-<claim-name>"
```

### Step 3: Remove Images (Optional)

```bash
# Remove experiment-specific image
docker rmi "experiment-<claim-name>"

# List remaining images
docker images | grep experiment
```

### Step 4: Remove Volumes (Optional)

```bash
# List volumes
docker volume ls

# Remove experiment volumes
docker-compose down -v

# Or remove specific volumes
docker volume rm "<volume-name>"
```

### Step 5: Clean Unused Resources

```bash
# Remove unused containers, networks, images
docker system prune -f

# More aggressive cleanup (includes unused volumes)
docker system prune -a --volumes -f
```

**Warning:** The aggressive cleanup removes ALL unused resources, not just experiment-related ones.

### Step 6: Verify Cleanup

```bash
# Check no experiment containers remain
docker ps -a | grep experiment

# Check disk space recovered
docker system df
```

### Step 7: Document Cleanup

Add to experiment log:

```markdown
## Cleanup Log

**Date:** YYYY-MM-DD HH:MM
**Action:** Container cleanup completed

### Resources Removed

| Type | Name | Status |
|------|------|--------|
| Container | experiment-<claim> | Removed |
| Image | experiment-<claim>:latest | Removed |
| Volume | experiment_data | Removed |

### Disk Space Recovered

Before: X.X GB
After: Y.Y GB
Recovered: Z.Z GB
```

## Output

| Artifact | Content |
|----------|---------|
| Cleanup log | Record of removed resources |
| Clean Docker environment | No experiment resources remain |

## Verification Checklist

- [ ] Containers stopped
- [ ] Containers removed
- [ ] Images removed (if desired)
- [ ] Volumes removed (if desired)
- [ ] System prune executed
- [ ] Cleanup documented
- [ ] Disk space verified

## Example

```bash
# Complete cleanup for redis-performance experiment
cd experiments/redis-performance

# Stop and remove everything
docker-compose down -v --rmi local

# Verify cleanup
docker ps -a | grep redis-performance
# (should return nothing)

# Check disk space
docker system df
```

## Cleanup Script

Create a reusable cleanup script:

```bash
#!/bin/bash
# scripts/cleanup_experiment.sh

EXPERIMENT_DIR=$1

if [ -z "$EXPERIMENT_DIR" ]; then
    echo "Usage: cleanup_experiment.sh <experiment-dir>"
    exit 1
fi

cd "$EXPERIMENT_DIR" || exit 1

echo "Stopping containers..."
docker-compose down -v

echo "Removing images..."
docker-compose down --rmi local

echo "Pruning unused resources..."
docker system prune -f

echo "Cleanup complete."
docker system df
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Container in use | Process still attached | Stop process, then remove |
| Volume in use | Mounted to another container | Stop that container first |
| Image has dependents | Child images exist | Remove child images first |
| Permission denied | Running as non-root | Use sudo or fix Docker permissions |
