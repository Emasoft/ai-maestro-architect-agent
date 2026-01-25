# Bun GitHub Actions: CI and Publishing

## Table of Contents
1. [Basic CI Workflow](#basic-ci-workflow)
2. [Matrix Builds](#matrix-builds)
3. [Caching Strategies](#caching-strategies)
4. [Artifact Management](#artifact-management)
5. [Publish Workflow](#publish-workflow)
6. [Release Automation](#release-automation)

---

**See also**: [Part 2 - Advanced Workflows](./bun-github-actions-part2-advanced.md) for Monorepo, Security, Docker, and PR workflows.

---

## Basic CI Workflow
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '24'
          registry-url: 'https://registry.npmjs.org'
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: '1.1.42'
      - run: npm ci
      - run: bun run build.js
      - run: npm test
```

## Matrix Builds

### Testing Across Multiple Bun Versions
```yaml
name: Matrix CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        bun-version: ['1.1.42', '1.1.30', 'latest']
        node-version: ['20', '22', '24']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          registry-url: 'https://registry.npmjs.org'
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: ${{ matrix.bun-version }}
      - run: npm ci
      - run: bun run build.js
      - run: npm test
      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.bun-version == '1.1.42'
        uses: codecov/codecov-action@v4
```

### OS-Specific Matrix
```yaml
strategy:
  matrix:
    include:
      - os: ubuntu-latest
        bun-cache-path: ~/.bun/install/cache
      - os: windows-latest
        bun-cache-path: ~/AppData/Roaming/Bun/install/cache
      - os: macos-latest
        bun-cache-path: ~/.bun/install/cache
```

### Minimal vs Full Matrix
```yaml
# Minimal: Only test critical combinations
strategy:
  matrix:
    os: [ubuntu-latest]
    bun-version: ['1.1.42']
    node-version: ['24']

# Full: Test all combinations
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    bun-version: ['1.1.30', '1.1.42', 'latest']
    node-version: ['20', '22', '24']
```

## Caching Strategies

### Bun Install Cache
```yaml
- name: Cache Bun dependencies
  uses: actions/cache@v4
  with:
    path: ~/.bun/install/cache
    key: ${{ runner.os }}-bun-${{ hashFiles('**/bun.lockb') }}
    restore-keys: |
      ${{ runner.os }}-bun-

- uses: oven-sh/setup-bun@v2
  with:
    bun-version: '1.1.42'

- run: bun install --frozen-lockfile
```

### Node Modules Cache
```yaml
- name: Cache node_modules
  uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-modules-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-modules-

- run: npm ci
```

### Build Artifacts Cache
```yaml
- name: Cache build outputs
  uses: actions/cache@v4
  with:
    path: |
      dist/
      .next/cache/
      .turbo/
    key: ${{ runner.os }}-build-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-build-
```

### Multi-Level Caching Strategy
```yaml
- name: Cache Bun install cache
  uses: actions/cache@v4
  with:
    path: ~/.bun/install/cache
    key: ${{ runner.os }}-bun-cache-${{ hashFiles('**/bun.lockb') }}
    restore-keys: |
      ${{ runner.os }}-bun-cache-

- name: Cache node_modules
  id: cache-node-modules
  uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-modules-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-modules-

- name: Install dependencies
  if: steps.cache-node-modules.outputs.cache-hit != 'true'
  run: npm ci

- name: Cache build
  uses: actions/cache@v4
  with:
    path: dist/
    key: ${{ runner.os }}-build-${{ github.sha }}
```

## Artifact Management

### Upload Build Artifacts
```yaml
- name: Build project
  run: bun run build.js

- name: Upload build artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-${{ runner.os }}-${{ github.sha }}
    path: |
      dist/
      build/
      *.tgz
    retention-days: 7
    if-no-files-found: error
```

### Download Artifacts from Previous Jobs
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bun run build.js
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/
      - run: npm test
```

### Package Tarball as Artifact
```yaml
- name: Create package tarball
  run: npm pack

- name: Upload tarball
  uses: actions/upload-artifact@v4
  with:
    name: npm-package
    path: '*.tgz'
```

### Artifact Retention for Releases
```yaml
- name: Upload release artifacts
  uses: actions/upload-artifact@v4
  with:
    name: release-${{ github.ref_name }}
    path: dist/
    retention-days: 90  # Keep release artifacts longer
```

## Publish Workflow

### Basic Publish with OIDC
```yaml
name: Publish
on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  id-token: write  # Required for npm OIDC

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '24'
          registry-url: 'https://registry.npmjs.org'
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: '1.1.42'
      - run: npm ci
      - run: bun run build.js
      - run: npm test

      - name: Validate version
        run: |
          TAG="${GITHUB_REF#refs/tags/v}"
          PKG=$(node -p "require('./package.json').version")
          [ "$TAG" = "$PKG" ] || exit 1

      # CRITICAL: Use npm publish, NOT bun publish (no OIDC support)
      - run: npm publish --access public
```

### Publish with Provenance
```yaml
- run: npm publish --access public --provenance
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Conditional Publishing
```yaml
- name: Check if version exists on npm
  id: check-version
  run: |
    VERSION=$(node -p "require('./package.json').version")
    if npm view "$(node -p "require('./package.json').name")@$VERSION" version 2>/dev/null; then
      echo "exists=true" >> $GITHUB_OUTPUT
    else
      echo "exists=false" >> $GITHUB_OUTPUT
    fi

- name: Publish to npm
  if: steps.check-version.outputs.exists == 'false'
  run: npm publish --access public
```

## Release Automation

### Create GitHub Release with Changelog
```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  id-token: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch all history for changelog

      - uses: actions/setup-node@v4
        with:
          node-version: '24'
          registry-url: 'https://registry.npmjs.org'

      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: '1.1.42'

      - run: npm ci
      - run: bun run build.js
      - run: npm test

      - name: Generate changelog
        id: changelog
        run: |
          PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -n "$PREVIOUS_TAG" ]; then
            CHANGELOG=$(git log $PREVIOUS_TAG..HEAD --pretty=format:"- %s (%h)" --no-merges)
          else
            CHANGELOG=$(git log --pretty=format:"- %s (%h)" --no-merges)
          fi
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGELOG" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create package tarball
        run: npm pack

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body: |
            ## Changes
            ${{ steps.changelog.outputs.changelog }}
          files: |
            *.tgz
            dist/**/*
          draft: false
          prerelease: false

      - name: Publish to npm
        run: npm publish --access public
```

### Release with Assets
```yaml
- name: Build binaries
  run: |
    bun build src/index.ts --compile --outfile=myapp-linux
    bun build src/index.ts --compile --outfile=myapp-macos
    bun build src/index.ts --compile --outfile=myapp-windows.exe

- name: Create Release
  uses: softprops/action-gh-release@v2
  with:
    files: |
      myapp-linux
      myapp-macos
      myapp-windows.exe
      *.tgz
```

### Automated Release Notes
```yaml
- name: Generate Release Notes
  uses: release-drafter/release-drafter@v6
  with:
    config-name: release-drafter.yml
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
