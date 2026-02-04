# npm Publishing with Bun Projects - Complete Reference

This reference covers all aspects of publishing npm packages from Bun projects. The content is split into two parts for easier navigation.

---

## Table of Contents

- [Document Structure](#document-structure)
  - [[Part 1: Authentication & Setup]](#part-1-authentication--setup)
  - [[Part 2: Publishing Patterns]](#part-2-publishing-patterns)
- [Quick Decision Tree](#quick-decision-tree)
  - [Which Authentication Method?](#which-authentication-method)
  - [Which Registry?](#which-registry)
  - [Which Release Type?](#which-release-type)
- [Common Workflows](#common-workflows)
  - [Basic Publish Workflow (OIDC)](#basic-publish-workflow-oidc)
  - [Beta Release Workflow](#beta-release-workflow)
  - [Monorepo with Changesets](#monorepo-with-changesets)
- [Essential package.json Fields](#essential-packagejson-fields)
- [Troubleshooting Quick Reference](#troubleshooting-quick-reference)
- [Cross-references](#cross-references)

---

## Document Structure

### [Part 1: Authentication & Setup](./bun-npm-publishing-part1-authentication-setup.md)

Covers authentication methods and pre-publishing configuration:

| Section | Description | When to Read |
|---------|-------------|--------------|
| **OIDC Trusted Publishing** | Passwordless publishing via GitHub OIDC | Setting up secure CI/CD publishing without tokens |
| **Traditional npm Token Publishing** | Token-based authentication | When OIDC unavailable or using private registries |
| **Version Management** | SemVer, npm version commands, changelog | Before any release, version bumping |
| **Pre-publish Validation** | prepublishOnly, dry-run, npm pack | Before first publish, debugging publish issues |
| **Registry Configuration** | npm, GitHub Packages, private registries | Publishing to non-default registries |

**Quick Reference - Part 1:**
- OIDC requires `registry-url` in setup-node - most common failure cause
- Scoped packages require `--access public` or `publishConfig.access: "public"`
- `bun publish` does NOT support OIDC as of January 2026 - use `npm publish`
- Always use `npm publish --dry-run` before actual publishing

---

### [Part 2: Publishing Patterns](./bun-npm-publishing-part2-patterns.md)

Covers advanced publishing patterns and package configuration:

| Section | Description | When to Read |
|---------|-------------|--------------|
| **Beta/Pre-release Channels** | Dist tags, beta/next/canary releases | Publishing pre-release versions |
| **Package.json Publishing Config** | publishConfig, files, exports, bin | Configuring what gets published |
| **Unpublishing and Deprecation** | npm unpublish, npm deprecate | Removing or marking packages obsolete |
| **Monorepo Publishing** | Workspaces, Changesets, Lerna | Publishing multiple packages from one repo |

**Quick Reference - Part 2:**
- Always use `--tag beta` for pre-releases (never publish pre-release as latest)
- npm unpublish only works within 72 hours - use deprecation for older packages
- Use Changesets for monorepo versioning and publishing automation
- `workspace:*` is replaced with actual version on publish

---

## Quick Decision Tree

### Which Authentication Method?

```
Publishing from GitHub Actions?
├── Yes → Use OIDC Trusted Publishing (Part 1)
│         ├── Configure npm.js access settings
│         ├── Add id-token: write permission
│         └── Use npm publish (not bun)
└── No  → Use Traditional Token (Part 1)
          ├── Generate Automation token on npmjs.com
          └── Add to secrets/environment
```

### Which Registry?

```
Where to publish?
├── Public npm registry → Default (no config needed)
├── GitHub Packages → Configure @scope registry (Part 1)
├── Private registry → Set publishConfig.registry (Part 1)
└── Multiple registries → Scope-based .npmrc config (Part 1)
```

### Which Release Type?

```
What kind of release?
├── Stable release → npm publish (default latest tag)
├── Beta/Pre-release → npm publish --tag beta (Part 2)
├── Canary/Nightly → npm publish --tag canary (Part 2)
└── Monorepo packages → Changesets workflow (Part 2)
```

---

## Common Workflows

### Basic Publish Workflow (OIDC)

```yaml
name: Publish to npm
on:
  release:
    types: [published]

permissions:
  id-token: write
  contents: read

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - uses: actions/setup-node@v4
        with:
          node-version: '24'
          registry-url: 'https://registry.npmjs.org'
      - run: bun install
      - run: bun run build
      - run: bun test
      - run: npm publish --access public
```

### Beta Release Workflow

```yaml
- name: Publish Beta
  if: github.ref == 'refs/heads/develop'
  run: |
    VERSION=$(jq -r .version package.json)
    npm version ${VERSION}-beta.${GITHUB_RUN_NUMBER} --no-git-tag-version
    npm publish --tag beta
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Monorepo with Changesets

```yaml
- name: Publish with Changesets
  uses: changesets/action@v1
  with:
    publish: bun run publish
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## Essential package.json Fields

```json
{
  "name": "@scope/package-name",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist", "README.md", "LICENSE"],
  "publishConfig": {
    "access": "public"
  },
  "scripts": {
    "prepublishOnly": "bun run build && bun test"
  },
  "engines": {
    "node": ">=18.0.0",
    "bun": ">=1.0.0"
  }
}
```

---

## Troubleshooting Quick Reference

| Problem | Cause | Solution |
|---------|-------|----------|
| OIDC auth hangs/fails silently | Missing registry-url | Add `registry-url: 'https://registry.npmjs.org'` to setup-node |
| "You must sign up for private packages" | Missing --access public | Add `--access public` or `publishConfig.access` |
| "Cannot publish over existing version" | Version already exists | Bump version with `npm version patch/minor/major` |
| "npm ERR! 403 Forbidden" | Wrong token or permissions | Regenerate token, check package access settings |
| Unpublish fails | Package older than 72 hours | Use `npm deprecate` instead |
| Pre-release installed by default | Published without --tag | Use `npm dist-tag rm` then re-publish with `--tag` |
| Files missing from package | Not in files array | Add to `files` array or remove from `.gitignore` |
| bun publish OIDC fails | bun doesn't support OIDC | Use `npm publish` for OIDC publishing |

---

## Cross-references

Related documentation:

- **[bun-github-actions.md](./bun-github-actions.md)** - GitHub Actions CI/CD patterns for Bun projects
- **[bun-testing.md](./bun-testing.md)** - Testing strategies before publishing
- **[bun-build-api.md](./bun-build-api.md)** - Building distributable packages with Bun

**External Resources:**
- Official npm docs: https://docs.npmjs.com/cli/v10/commands/npm-publish
- Changesets: https://github.com/changesets/changesets
- Semantic Versioning: https://semver.org/
- npm dist-tags: https://docs.npmjs.com/cli/v10/commands/npm-dist-tag
- Bun OIDC tracking issue: https://github.com/oven-sh/bun/issues/15601
