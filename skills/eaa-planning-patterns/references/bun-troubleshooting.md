# Bun Troubleshooting Guide

## Table of Contents

- [Overview](#overview)
- [Quick Reference: All Issues](#quick-reference-all-issues)
- [Guide Structure](#guide-structure)
  - [Part 1: CI/CD Publishing Issues](#part-1-cicd-publishing-issues)
  - [Part 2: Version & Registry Issues](#part-2-version--registry-issues)
  - [Part 3: Permissions & Tests](#part-3-permissions--tests)
  - [Part 4: Browser Bundling](#part-4-browser-bundling)
  - [Part 5: TypeScript & CSS](#part-5-typescript--css)
  - [Part 6: Sourcemaps](#part-6-sourcemaps)
  - [Part 7: Validation Issues](#part-7-validation-issues)
- [Issue Categories by Symptom](#issue-categories-by-symptom)
  - [Authentication & Publishing Errors](#authentication--publishing-errors)
  - [Build Errors](#build-errors)
  - [Test Failures](#test-failures)
  - [CI/CD Failures](#cicd-failures)
  - [Runtime Errors](#runtime-errors)
  - [Release Issues](#release-issues)
- [Common Workflow Patterns](#common-workflow-patterns)
  - [Minimal Publish Workflow](#minimal-publish-workflow)
  - [Browser Build Configuration](#browser-build-configuration)
  - [TypeScript Package Configuration](#typescript-package-configuration)
- [Additional Resources](#additional-resources)
- [File Index](#file-index)

## Overview

This document is an index to the comprehensive Bun troubleshooting guide, covering the 14 most common issues encountered when using Bun for building, testing, and publishing JavaScript and TypeScript packages.

The guide has been split into focused sections for easier navigation and reference.

---

## Quick Reference: All Issues

| # | Issue | Quick Solution | Part |
|---|-------|----------------|------|
| 1 | OIDC Authentication Error | Use `npm publish` instead of `bun publish` | [Part 1](bun-troubleshooting-part1-ci-publishing.md) |
| 2 | Unpinned Version Issues | Pin version: `bun-version: '1.1.42'` | [Part 1](bun-troubleshooting-part1-ci-publishing.md) |
| 3 | Node.js Modules in Browser | Use `external: ['fs', 'path', ...]` | [Part 4](bun-troubleshooting-part4-browser-bundling.md) |
| 4 | Global Name Collision | Use unique `globalName` for IIFE | [Part 4](bun-troubleshooting-part4-browser-bundling.md) |
| 5 | Version Mismatch | Validate tag matches package.json | [Part 2](bun-troubleshooting-part2-version-registry.md) |
| 6 | GitHub Release Permissions | Add `contents: write` permission | [Part 3](bun-troubleshooting-part3-permissions-tests.md) |
| 7 | Test Timeouts | Use `--timeout 30000` | [Part 3](bun-troubleshooting-part3-permissions-tests.md) |
| 8 | Missing registry-url | Set `registry-url: 'https://registry.npmjs.org'` | [Part 2](bun-troubleshooting-part2-version-registry.md) |
| 9 | TypeScript Declarations | Run `tsc --emitDeclarationOnly` | [Part 5](bun-troubleshooting-part5-typescript-css.md) |
| 10 | CSS Bundling | Configure `loader: { '.css': 'css' }` | [Part 5](bun-troubleshooting-part5-typescript-css.md) |
| 11 | Sourcemap Issues | Use `sourcemap: 'linked'` | [Part 6](bun-troubleshooting-part6-sourcemaps.md) |
| 12 | JSON Validation Fails | Skip tsconfig.json or use `tsc --noEmit` | [Part 7](bun-troubleshooting-part7-validation.md) |
| 13 | UMD Validation Fails | Check for `.exports` pattern | [Part 7](bun-troubleshooting-part7-validation.md) |
| 14 | Wrong Version in Banner | Rebuild after `npm version` | [Part 7](bun-troubleshooting-part7-validation.md) |

---

## Guide Structure

### [Part 1: CI/CD Publishing Issues](bun-troubleshooting-part1-ci-publishing.md)

**Issues Covered:**
- 1. OIDC Authentication Error
  - Problem: `bun publish` fails with "missing authentication"
  - Solution: Use npm CLI for publishing with OIDC
- 2. Unpinned Version Issues
  - Problem: `bun-version: latest` causes flaky builds
  - Solution: Pin to specific version like `1.1.42`

**When to Read:** Setting up npm publishing workflows, experiencing authentication failures, or inconsistent CI builds.

---

### [Part 2: Version & Registry Issues](bun-troubleshooting-part2-version-registry.md)

**Issues Covered:**
- 5. Version Mismatch
  - Problem: Git tag doesn't match package.json version
  - Solution: Add version validation script to workflow
- 8. Missing registry-url
  - Problem: npm auth fails or publishes to wrong registry
  - Solution: Configure `registry-url` in setup-node action

**When to Read:** Publishing packages, version management, or registry configuration issues.

---

### [Part 3: Permissions & Tests](bun-troubleshooting-part3-permissions-tests.md)

**Issues Covered:**
- 6. GitHub Release Permissions
  - Problem: 403 Forbidden when creating releases
  - Solution: Add `contents: write` permission to workflow
- 7. Test Timeouts
  - Problem: Tests fail with "timeout exceeded"
  - Solution: Use `--timeout 30000` or per-test timeouts

**When to Read:** GitHub Actions permission errors, or tests timing out.

---

### [Part 4: Browser Bundling](bun-troubleshooting-part4-browser-bundling.md)

**Issues Covered:**
- 3. Node.js Modules in Browser
  - Problem: `ReferenceError: fs is not defined`
  - Solution: Use `external` config to exclude Node.js modules
- 4. Global Name Collision
  - Problem: Multiple libraries conflict on same page
  - Solution: Use unique, namespaced `globalName`

**When to Read:** Building for browser environments, IIFE bundles, or isomorphic code.

---

### [Part 5: TypeScript & CSS](bun-troubleshooting-part5-typescript-css.md)

**Issues Covered:**
- 9. TypeScript Declarations
  - Problem: "Could not find declaration file for module"
  - Solution: Run `tsc` with `emitDeclarationOnly` after Bun build
- 10. CSS Bundling
  - Problem: CSS imports fail or styles missing
  - Solution: Configure CSS loader in build config

**When to Read:** Publishing TypeScript libraries, or bundling CSS with JavaScript.

---

### [Part 6: Sourcemaps](bun-troubleshooting-part6-sourcemaps.md)

**Issues Covered:**
- 11. Sourcemap Issues
  - Problem: Debugging shows minified code, not source
  - Solution: Configure `sourcemap: 'linked'` with correct paths

**When to Read:** Debugging issues, error tracking setup, or production debugging.

---

### [Part 7: Validation Issues](bun-troubleshooting-part7-validation.md)

**Issues Covered:**
- 12. JSON Validation Fails on tsconfig.json
  - Problem: JSON linters reject JSONC comments
  - Solution: Exclude tsconfig.json or use JSONC-aware validators
- 13. UMD Validation Fails After Bun Build
  - Problem: Minifier renames `module.exports`
  - Solution: Check for `.exports` pattern instead
- 14. Minified File Has Wrong Version in Banner
  - Problem: Banner shows old version after `npm version`
  - Solution: Rebuild after version bump

**When to Read:** CI validation failures, release script issues, or version management.

---

## Issue Categories by Symptom

### Authentication & Publishing Errors
- "missing authentication" → Issue 1 (Part 1)
- "need auth" / wrong registry → Issue 8 (Part 2)
- "Resource not accessible" / 403 → Issue 6 (Part 3)

### Build Errors
- "fs/path/crypto is not defined" → Issue 3 (Part 4)
- "Cannot find module '*.css'" → Issue 10 (Part 5)
- "Could not find declaration file" → Issue 9 (Part 5)

### Test Failures
- "timeout exceeded" → Issue 7 (Part 3)

### CI/CD Failures
- Flaky builds with `latest` → Issue 2 (Part 1)
- Version mismatch → Issue 5 (Part 2)
- JSON validation fails → Issue 12 (Part 7)

### Runtime Errors
- Global name collision → Issue 4 (Part 4)
- Wrong sourcemap locations → Issue 11 (Part 6)

### Release Issues
- UMD validation fails → Issue 13 (Part 7)
- Wrong version in banner → Issue 14 (Part 7)

---

## Common Workflow Patterns

### Minimal Publish Workflow

```yaml
name: Publish
on:
  release:
    types: [published]

permissions:
  contents: write
  id-token: write

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: '1.1.42'  # Issue 2: Pin version

      - run: bun install
      - run: bun run build

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'  # Issue 8

      - run: npm publish --provenance --access public  # Issue 1: Use npm
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Browser Build Configuration

```javascript
// build.js - Handles Issues 3, 4, 10, 11
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'iife',
  globalName: 'MyCompany_MyLib',  // Issue 4
  external: ['fs', 'path', 'crypto'],  // Issue 3
  loader: { '.css': 'css' },  // Issue 10
  sourcemap: 'linked',  // Issue 11
  minify: true,
});
```

### TypeScript Package Configuration

```json
{
  "scripts": {
    "build": "bun run build.js && tsc",
    "test": "bun test --timeout 30000"
  }
}
```

```javascript
// build.js - Then run: tsc (for Issue 9)
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'node',
  format: 'esm',
});
```

---

## Additional Resources

- [Bun Documentation](https://bun.sh/docs)
- [Bun GitHub Issues](https://github.com/oven-sh/bun/issues)
- [Bun Discord Community](https://bun.sh/discord)

---

## File Index

| File | Lines | Issues Covered |
|------|-------|----------------|
| [bun-troubleshooting-part1-ci-publishing.md](bun-troubleshooting-part1-ci-publishing.md) | ~190 | 1, 2 |
| [bun-troubleshooting-part2-version-registry.md](bun-troubleshooting-part2-version-registry.md) | ~280 | 5, 8 |
| [bun-troubleshooting-part3-permissions-tests.md](bun-troubleshooting-part3-permissions-tests.md) | ~300 | 6, 7 |
| [bun-troubleshooting-part4-browser-bundling.md](bun-troubleshooting-part4-browser-bundling.md) | ~240 | 3, 4 |
| [bun-troubleshooting-part5-typescript-css.md](bun-troubleshooting-part5-typescript-css.md) | ~400 | 9, 10 |
| [bun-troubleshooting-part6-sourcemaps.md](bun-troubleshooting-part6-sourcemaps.md) | ~230 | 11 |
| [bun-troubleshooting-part7-validation.md](bun-troubleshooting-part7-validation.md) | ~350 | 12, 13, 14 |
