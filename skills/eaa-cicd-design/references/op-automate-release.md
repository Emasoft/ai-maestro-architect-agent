---
procedure: support-skill
workflow-instruction: support
---

# Operation: Automate Multi-Platform Release

## Purpose

Create automated release workflows that build artifacts for multiple platforms, create GitHub releases, and publish to package registries.

## When to Use

- Setting up automated releases for a project
- Publishing to multiple package registries
- Creating multi-platform release artifacts

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Release targets | Requirements | Yes |
| Package registries | Requirements | Yes |
| Version strategy | Requirements | Yes |

## Procedure

### Step 1: Define Release Trigger

```yaml
on:
  push:
    tags:
      - 'v*'  # Triggers on v1.0.0, v2.1.0, etc.
```

### Step 2: Design Release Pipeline

```
Stage 1: Validate      # Verify tag format and version
Stage 2: Test          # Run full test suite
Stage 3: Build         # Build artifacts for all platforms
Stage 4: Publish       # Publish to registries
Stage 5: Release       # Create GitHub release
```

### Step 3: Create Release Workflow

```yaml
name: Release

on:
  push:
    tags: ['v*']

jobs:
  validate:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v4
      - name: Extract version
        id: version
        run: echo "version=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

  test:
    needs: validate
    strategy:
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: ./run-tests.sh

  build:
    needs: test
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: linux-x64
          - os: macos-14
            target: macos-arm64
          - os: windows-latest
            target: windows-x64
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: ./build.sh
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.target }}
          path: dist/

  publish:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Download artifacts
        uses: actions/download-artifact@v4
      - name: Publish to registry
        env:
          TOKEN: ${{ secrets.REGISTRY_TOKEN }}
        run: ./publish.sh

  release:
    needs: [build, publish]
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            linux-x64/*
            macos-arm64/*
            windows-x64/*
          generate_release_notes: true
```

### Step 4: Configure Registry Publishing

**PyPI:**
```yaml
- name: Publish to PyPI
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    pip install build twine
    python -m build
    twine upload dist/*
```

**npm:**
```yaml
- name: Publish to npm
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
  run: npm publish
```

**GitHub Packages:**
```yaml
- name: Publish to GitHub Packages
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: npm publish --registry=https://npm.pkg.github.com
```

### Step 5: Add Changelog Generation

```yaml
- name: Generate changelog
  uses: orhun/git-cliff-action@v3
  with:
    config: cliff.toml
  env:
    OUTPUT: CHANGELOG.md
```

## Output

| File | Content |
|------|---------|
| `.github/workflows/release.yml` | Release workflow |
| `CHANGELOG.md` | Generated changelog |
| GitHub Release | With artifacts |

## Verification Checklist

- [ ] Tag trigger configured correctly
- [ ] All target platforms included
- [ ] Tests run before build
- [ ] Artifacts uploaded for each platform
- [ ] Registry publishing configured
- [ ] GitHub release created
- [ ] Changelog generated

## Example

```yaml
name: Release Python Package

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Build
        run: |
          pip install build
          python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          pip install twine
          twine upload dist/*

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          generate_release_notes: true
```

## Error Handling

| Error | Solution |
|-------|----------|
| Version mismatch | Verify pyproject.toml/package.json version |
| Upload failed | Check registry credentials |
| Build failed | Verify build configuration |
