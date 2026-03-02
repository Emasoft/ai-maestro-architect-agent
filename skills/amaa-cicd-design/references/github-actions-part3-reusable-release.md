# GitHub Actions Part 3: Reusable Workflows and Releases


## Contents

- [Reusable Workflows](#reusable-workflows)
  - [Define Reusable Workflow](#define-reusable-workflow)
  - [Call Reusable Workflow](#call-reusable-workflow)
- [Release Workflow](#release-workflow)
  - [Create GitHub Release](#create-github-release)
  - [Publish to Package Registries](#publish-to-package-registries)
- [Security Best Practices](#security-best-practices)
  - [Permissions](#permissions)
  - [Pin Action Versions](#pin-action-versions)
  - [Dependency Review](#dependency-review)

---

## Reusable Workflows

### Define Reusable Workflow
```yaml
# .github/workflows/build-docker.yml
name: Build Docker Image

on:
  workflow_call:
    inputs:
      image-name:
        required: true
        type: string
    secrets:
      DOCKERHUB_TOKEN:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: docker/login-action@v3
        with:
          username: ${{ github.repository_owner }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ inputs.image-name }}:latest
```

### Call Reusable Workflow
```yaml
jobs:
  build-and-push:
    uses: ./.github/workflows/build-docker.yml
    with:
      image-name: myorg/myapp
    secrets:
      DOCKERHUB_TOKEN: ${{ secrets.DOCKERHUB_TOKEN }}
```

## Release Workflow

### Create GitHub Release
```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: artifacts/**/*
          generate_release_notes: true
          draft: false
          prerelease: ${{ contains(github.ref, 'alpha') || contains(github.ref, 'beta') }}
```

### Publish to Package Registries

```yaml
# npm
- name: Publish to npm
  run: |
    echo "//registry.npmjs.org/:_authToken=${{ secrets.NPM_TOKEN }}" > .npmrc
    npm publish

# PyPI
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}

# Crates.io
- name: Publish to crates.io
  run: cargo publish --token ${{ secrets.CRATES_IO_TOKEN }}

# Docker Hub
- name: Push to Docker Hub
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: ${{ github.repository }}:${{ github.ref_name }}
```

## Security Best Practices

### Permissions
```yaml
# Minimal permissions by default
permissions:
  contents: read

jobs:
  build:
    permissions:
      contents: read
      packages: write  # Only for jobs that need it
```

### Pin Action Versions
```yaml
# Bad: mutable tag
- uses: actions/checkout@main

# Good: immutable commit SHA
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

### Dependency Review
```yaml
- name: Dependency Review
  uses: actions/dependency-review-action@v4
  with:
    fail-on-severity: moderate
```

---
Back to [GitHub Actions Reference](github-actions.md)
