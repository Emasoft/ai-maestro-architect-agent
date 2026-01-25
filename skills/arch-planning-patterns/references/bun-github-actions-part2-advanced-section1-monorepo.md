# Bun GitHub Actions: Monorepo Workflows

**Parent document**: [bun-github-actions-part2-advanced.md](./bun-github-actions-part2-advanced.md)

---

## Table of Contents
- 1.1 [Path Filters for Affected Packages](#path-filters-for-affected-packages)
- 1.2 [Parallel Jobs for Multiple Packages](#parallel-jobs-for-multiple-packages)
- 1.3 [Turborepo Integration](#turborepo-integration)
- 1.4 [Nx Integration](#nx-integration)

---

## Path Filters for Affected Packages

Use path filters to detect which packages changed and run tests only for affected code:

```yaml
name: Monorepo CI
on:
  pull_request:
    paths:
      - 'packages/**'
      - 'apps/**'

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            package-a:
              - 'packages/a/**'
            package-b:
              - 'packages/b/**'
            app-1:
              - 'apps/1/**'

  test-affected:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.packages != '[]' }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: ${{ fromJSON(needs.detect-changes.outputs.packages) }}
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun test --filter=${{ matrix.package }}
```

---

## Parallel Jobs for Multiple Packages

Run tests in parallel across multiple packages:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        package:
          - packages/core
          - packages/utils
          - packages/api
          - apps/web
          - apps/cli
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - name: Test ${{ matrix.package }}
        run: bun test
        working-directory: ${{ matrix.package }}
```

---

## Turborepo Integration

Use Turborepo for efficient monorepo builds:

```yaml
- name: Install Turborepo
  run: bun add -g turbo

- name: Build affected
  run: turbo run build --filter=[HEAD^1]

- name: Test affected
  run: turbo run test --filter=[HEAD^1]
```

---

## Nx Integration

Use Nx for monorepo orchestration:

```yaml
- name: Install Nx
  run: bun add -g nx

- name: Run affected tests
  run: nx affected --target=test --base=origin/main --head=HEAD

- name: Build affected apps
  run: nx affected --target=build --base=origin/main --head=HEAD
```
