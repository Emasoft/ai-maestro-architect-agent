---
procedure: support-skill
workflow-instruction: support
---

# Operation: Configure Cross-Platform Matrix Build

## Purpose

Configure matrix builds to run jobs across multiple operating systems, language versions, or other dimensions simultaneously.

## When to Use

- Testing on multiple platforms (Linux, macOS, Windows)
- Testing across multiple language versions
- Building artifacts for multiple platforms

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Target platforms | Requirements | Yes |
| Language versions | Requirements | If applicable |
| Build variations | Requirements | If needed |

## Procedure

### Step 1: Identify Matrix Dimensions

Common dimensions:
- Operating system: `os: [ubuntu-latest, macos-14, windows-latest]`
- Language version: `python-version: ["3.10", "3.11", "3.12"]`
- Node version: `node-version: [18, 20, 22]`
- Architecture: `arch: [x64, arm64]`

### Step 2: Define Basic Matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: ./run-tests.sh
```

### Step 3: Add Multiple Dimensions

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
        python-version: ["3.10", "3.11", "3.12"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pytest
```

### Step 4: Configure Matrix Options

```yaml
strategy:
  fail-fast: false  # Don't cancel other jobs if one fails
  max-parallel: 4   # Limit concurrent jobs
  matrix:
    os: [ubuntu-latest, macos-14]
```

### Step 5: Add Include/Exclude for Special Cases

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-14, windows-latest]
    python-version: ["3.10", "3.11", "3.12"]
    exclude:
      # Don't test Python 3.10 on Windows
      - os: windows-latest
        python-version: "3.10"
    include:
      # Add specific combination with extra variable
      - os: ubuntu-latest
        python-version: "3.12"
        experimental: true
```

### Step 6: Use Matrix Values in Steps

```yaml
jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            artifact: linux-x64
          - os: macos-14
            artifact: macos-arm64
          - os: windows-latest
            artifact: windows-x64
    runs-on: ${{ matrix.os }}
    steps:
      - name: Build
        run: ./build.sh

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.artifact }}
          path: dist/
```

## Output

| File | Content |
|------|---------|
| `.github/workflows/<name>.yml` | Workflow with matrix configuration |

## Verification Checklist

- [ ] All target platforms included
- [ ] All language versions included
- [ ] Exclusions defined for incompatible combinations
- [ ] fail-fast configured appropriately
- [ ] max-parallel set if needed
- [ ] Matrix values used correctly in steps

## Example

```yaml
name: Cross-Platform CI

on: [push, pull_request]

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
        python-version: ["3.10", "3.11", "3.12"]

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Run tests
        run: pytest --cov=src tests/
```

## Error Handling

| Error | Solution |
|-------|----------|
| Matrix generates too many jobs | Use exclude or reduce dimensions |
| Platform-specific failures | Check OS-specific commands |
| Timeout issues | Increase timeout or optimize tests |
