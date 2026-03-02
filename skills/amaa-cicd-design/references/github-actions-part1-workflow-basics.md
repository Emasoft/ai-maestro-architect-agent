# GitHub Actions Part 1: Workflow Basics and Runners


## Contents

- [Workflow Structure](#workflow-structure)
- [Runners](#runners)
  - [GitHub-Hosted Runners](#github-hosted-runners)
  - [Free Tier Limits](#free-tier-limits)
  - [Self-Hosted Runners](#self-hosted-runners)
- [Common Actions](#common-actions)
  - [Checkout](#checkout)
  - [Cache](#cache)
  - [Upload/Download Artifacts](#uploaddownload-artifacts)
  - [Setup Tools](#setup-tools)

---

## Workflow Structure

```yaml
name: Workflow Name

on:                          # Triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'      # Weekly Monday 6am
  workflow_dispatch:          # Manual trigger

concurrency:                  # Prevent duplicate runs
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:                          # Global environment variables
  NODE_VERSION: '20'
  RUST_VERSION: 'stable'

jobs:
  job-name:
    name: Display Name
    runs-on: ubuntu-latest
    permissions:              # Fine-grained permissions
      contents: read
      packages: write
    steps:
      - name: Step name
        uses: action/name@version
        with:
          input: value
```

## Runners

### GitHub-Hosted Runners

| Runner | OS | Architecture | Specs |
|--------|----|--------------| ------|
| `ubuntu-latest` | Ubuntu 22.04 | x86_64 | 4 CPU, 16GB RAM |
| `ubuntu-24.04` | Ubuntu 24.04 | x86_64 | 4 CPU, 16GB RAM |
| `ubuntu-24.04-arm` | Ubuntu 24.04 | ARM64 | 4 CPU, 16GB RAM |
| `macos-14` | macOS 14 | ARM64 (M1) | 3 CPU, 14GB RAM |
| `macos-13` | macOS 13 | x86_64 | 4 CPU, 14GB RAM |
| `windows-latest` | Windows Server 2022 | x86_64 | 4 CPU, 16GB RAM |

### Free Tier Limits

| Account Type | Linux/Windows | macOS |
|--------------|---------------|-------|
| Free | 2000 min/month | 200 min/month |
| Pro | 3000 min/month | 300 min/month |
| Team | 3000 min/month | 300 min/month |

### Self-Hosted Runners

For requirements beyond free tier:
```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, x64]  # Labels
```

## Common Actions

### Checkout
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0            # Full history for versioning
    submodules: recursive     # Include submodules
```

### Cache
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Upload/Download Artifacts
```yaml
# Upload
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
    retention-days: 7

# Download
- uses: actions/download-artifact@v4
  with:
    name: build-output
    path: dist/
```

### Setup Tools

```yaml
# Node.js
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'

# Python
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'

# Rust
- uses: dtolnay/rust-toolchain@stable
  with:
    components: clippy, rustfmt

# Go
- uses: actions/setup-go@v5
  with:
    go-version: '1.22'
    cache: true

# Java
- uses: actions/setup-java@v4
  with:
    distribution: 'temurin'
    java-version: '21'
    cache: 'gradle'

# .NET
- uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '8.0.x'
```

---
Back to [GitHub Actions Reference](github-actions.md)
