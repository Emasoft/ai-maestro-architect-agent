# Bun GitHub Actions: Docker Integration

**Parent document**: [bun-github-actions-part2-advanced.md](./bun-github-actions-part2-advanced.md)

---

## Table of Contents
- 3.1 [Build Docker Image with Bun](#build-docker-image-with-bun)
- 3.2 [Multi-Stage Dockerfile for Bun](#multi-stage-dockerfile-for-bun)
- 3.3 [Docker Compose for Testing](#docker-compose-for-testing)

---

## Build Docker Image with Bun

Complete workflow for building and pushing Docker images:

```yaml
name: Docker Build
on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myorg/myapp
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Multi-Stage Dockerfile for Bun

Optimized multi-stage Dockerfile:

```dockerfile
# Dockerfile
FROM oven/bun:1.1.42 AS builder
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build.js

FROM oven/bun:1.1.42-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./
CMD ["bun", "run", "start"]
```

---

## Docker Compose for Testing

Run tests in Docker Compose environment:

```yaml
# .github/workflows/docker-test.yml
- name: Run tests in Docker
  run: |
    docker-compose up -d
    docker-compose run test bun test
    docker-compose down
```
