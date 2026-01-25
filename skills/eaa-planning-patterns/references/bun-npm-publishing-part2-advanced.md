# npm Publishing with Bun - Part 2: Advanced Publishing

## Table of Contents
1. [Beta/Pre-release Channels](#betapre-release-channels)
   - 1.1 [Dist Tags](#dist-tags)
   - 1.2 [Publishing to Beta Channel](#publishing-to-beta-channel)
   - 1.3 [Publishing to Next Channel](#publishing-to-next-channel)
   - 1.4 [Publishing to Canary Channel](#publishing-to-canary-channel)
   - 1.5 [Automated Pre-release in CI](#automated-pre-release-in-ci)
   - 1.6 [Promoting Beta to Latest](#promoting-beta-to-latest)
   - 1.7 [Viewing and Removing Dist Tags](#viewing-dist-tags)
   - 1.8 [Best Practices for Pre-releases](#best-practices-for-pre-releases)
2. [Package.json Publishing Config](#packagejson-publishing-config)
   - 2.1 [publishConfig](#publishconfig)
   - 2.2 [files Array](#files-array)
   - 2.3 [main, module, exports](#main-module-exports)
   - 2.4 [bin for CLI Tools](#bin-for-cli-tools)
   - 2.5 [Metadata Fields](#metadata-fields)
   - 2.6 [engines Constraint](#engines-constraint)
   - 2.7 [peerDependencies](#peerdependencies)
3. [Unpublishing and Deprecation](#unpublishing-and-deprecation)
   - 3.1 [Unpublishing Packages](#unpublishing-packages)
   - 3.2 [Deprecating Packages](#deprecating-packages)
   - 3.3 [Un-deprecate](#un-deprecate)
   - 3.4 [When to Deprecate vs Unpublish](#when-to-deprecate-vs-unpublish)
   - 3.5 [Best Practices](#best-practices)
4. [Monorepo Publishing](#monorepo-publishing)
   - 4.1 [Bun Workspaces](#bun-workspaces)
   - 4.2 [Publishing from Workspaces](#publishing-from-workspaces)
   - 4.3 [Changesets (Recommended)](#changesets-recommended)
   - 4.4 [Lerna (Alternative)](#lerna-alternative)
   - 4.5 [Versioning Strategies](#versioning-strategies)
   - 4.6 [Monorepo Publishing Workflow Example](#monorepo-publishing-workflow-example)
   - 4.7 [Cross-package Dependencies](#cross-package-dependencies)
5. [Cross-references](#cross-references)

**See also**: [Part 1: Setup & Configuration](./bun-npm-publishing-part1-setup.md)

---

## Beta/Pre-release Channels

Publish pre-release versions to test before stable release.

### Dist Tags
npm uses **dist-tags** to manage release channels:
- `latest` - Stable releases (default)
- `next` - Next major version
- `beta` - Beta releases
- `canary` - Nightly/unstable builds
- `alpha` - Alpha releases

### Publishing to Beta/Next/Canary Channels
```bash
# Beta: npm version 2.0.0-beta.0 && npm publish --tag beta
# Next: npm version 2.0.0-next.0 && npm publish --tag next
# Canary: npm version 1.0.0-canary.$(date +%Y%m%d%H%M%S) && npm publish --tag canary
```
Users install with: `npm install package-name@beta` (or @next, @canary)

### Automated Pre-release in CI
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

### Promoting Beta to Latest
```bash
# Move beta tag to latest
npm dist-tag add package-name@2.0.0-beta.5 latest

# Or publish same version without tag
npm publish
```

### Viewing and Removing Dist Tags
```bash
npm dist-tag ls package-name    # List all tags
npm dist-tag rm package-name beta  # Remove a tag
```

### Best Practices for Pre-releases
1. **Use semantic pre-release format**: `1.0.0-beta.0`, `2.0.0-next.1`
2. **Always specify --tag**: Never publish pre-releases without a tag
3. **Automate canary builds**: Use CI to create nightly builds
4. **Document pre-release channels**: Tell users how to install beta/next
5. **Test before promoting**: Run full test suite before promoting beta → latest

---

## Package.json Publishing Config

Configure exactly what gets published and how users consume your package.

### publishConfig
```json
{
  "publishConfig": {
    "access": "public",
    "registry": "https://registry.npmjs.org/",
    "tag": "latest"
  }
}
```

**Options:**
- `access` - "public" or "restricted" (for scoped packages)
- `registry` - Override default registry for publishing
- `tag` - Default dist-tag (usually "latest")

### files Array
Explicitly control which files are included:
```json
{
  "files": [
    "dist",
    "README.md",
    "LICENSE",
    "package.json"
  ]
}
```

**Always included (cannot exclude):**
- `package.json`
- `README.md`
- `LICENSE` / `LICENCE`
- `CHANGELOG.md` / `HISTORY.md`

**Always excluded:**
- `.git`
- `node_modules`
- `.npmrc`
- Files in `.gitignore` (unless explicitly in files array)

### main, module, exports
```json
{
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./utils": {
      "import": "./dist/utils.mjs",
      "require": "./dist/utils.js"
    }
  }
}
```

**Why use exports?**
- Controls what users can import
- Supports ESM and CJS dual packages
- Prevents deep imports (`import 'pkg/internal/secret'`)

### bin for CLI Tools
```json
{
  "bin": { "my-tool": "./dist/cli.js" }
}
```
After install: `npx my-tool`. For multiple binaries, add multiple keys to `bin`.

### Metadata Fields
```json
{
  "name": "@scope/package-name",
  "version": "1.0.0",
  "description": "Short description for npm search",
  "keywords": ["bun", "npm", "tool"],
  "author": "Your Name <email@example.com>",
  "license": "MIT",
  "homepage": "https://github.com/user/repo#readme",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/user/repo.git"
  },
  "bugs": {
    "url": "https://github.com/user/repo/issues"
  }
}
```

### engines Constraint
```json
{
  "engines": {
    "node": ">=18.0.0",
    "bun": ">=1.0.0",
    "npm": ">=9.0.0"
  }
}
```

Enforce engines check:
```json
{
  "engines": {
    "node": ">=18.0.0"
  },
  "engineStrict": true
}
```

### peerDependencies
```json
{
  "peerDependencies": {
    "react": ">=18.0.0",
    "react-dom": ">=18.0.0"
  },
  "peerDependenciesMeta": {
    "react-dom": {
      "optional": true
    }
  }
}
```

---

## Unpublishing and Deprecation

Remove or mark packages as deprecated on npm.

### Unpublishing Packages

**CRITICAL**: Unpublishing is heavily restricted by npm to prevent breaking the ecosystem.

**npm Unpublish Policy:**
- Can unpublish within **72 hours** of publishing
- Cannot unpublish if other packages depend on it
- Cannot unpublish versions older than 72 hours
- Cannot unpublish if downloads > threshold

**Unpublish specific version:**
```bash
npm unpublish package-name@1.0.0
```

**Unpublish entire package:**
```bash
npm unpublish package-name --force
```

**When unpublishing fails:**
```
npm ERR! Cannot unpublish - package has been published for more than 72 hours
```

**Solution: Use deprecation instead.**

### Deprecating Packages

Deprecation marks a package/version as obsolete without removing it.

**Deprecate specific version:**
```bash
npm deprecate package-name@1.0.0 "Critical security vulnerability, use 1.0.1+"
```

**Deprecate all versions:**
```bash
npm deprecate package-name "Package is no longer maintained"
```

**Deprecate version range:**
```bash
npm deprecate package-name@"<2.0.0" "Use version 2.x or higher"
```

**Users will see:**
```bash
npm install package-name@1.0.0
npm WARN deprecated package-name@1.0.0: Critical security vulnerability, use 1.0.1+
```

### Un-deprecate
```bash
npm deprecate package-name@1.0.0 ""
```

### When to Deprecate vs Unpublish

| Scenario | Action |
|----------|--------|
| Published <72h ago, no dependents | Unpublish |
| Security vulnerability | Deprecate + publish fix |
| Package renamed/moved | Deprecate with migration message |
| Discontinued maintenance | Deprecate with notice |
| Accidental publish | Unpublish (if <72h) or deprecate |

### Best Practices
1. **Always provide a reason** in deprecation message
2. **Point to alternative** or migration path
3. **Deprecate before unpublishing** to warn users
4. **Use semver ranges** to deprecate multiple versions
5. **Monitor deprecation warnings** - users may still install

---

## Monorepo Publishing

Publish multiple packages from a single repository using workspaces.

### Bun Workspaces
**package.json (root):**
```json
{
  "name": "my-monorepo",
  "workspaces": [
    "packages/*"
  ]
}
```

**Structure:**
```
my-monorepo/
├── package.json
├── packages/
│   ├── pkg-a/
│   │   └── package.json
│   ├── pkg-b/
│   │   └── package.json
│   └── pkg-c/
│       └── package.json
```

### Publishing from Workspaces

**Publish single package:**
```bash
cd packages/pkg-a
npm publish
```

**Publish all packages:**
```bash
bun run --filter '*' publish
```

### Changesets (Recommended)
Changesets automates versioning and publishing for monorepos.

**Install:**
```bash
bun add -D @changesets/cli
bunx changeset init
```

**Workflow:**
1. Developer creates changeset:
   ```bash
   bunx changeset
   # Select packages changed
   # Select version bump type
   # Write summary
   ```

2. CI creates "Version Packages" PR:
   ```yaml
   - name: Create Release PR
     uses: changesets/action@v1
     with:
       publish: npm run publish
     env:
       GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
       NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
   ```

3. Merge PR → Packages published automatically

**Why Changesets?**
- Automates version bumping
- Generates changelogs
- Handles dependencies between workspace packages
- Creates release PRs
- Publishes only changed packages

### Lerna (Alternative)
```bash
bun add -D lerna

# Publish changed packages
bunx lerna publish
```

### Versioning Strategies

**Independent Versioning** (each package has own version):
```json
{
  "version": "independent"
}
```

**Fixed Versioning** (all packages share version):
```json
{
  "version": "1.0.0"
}
```

### Monorepo Publishing Workflow Example
```yaml
name: Publish Packages

on:
  push:
    branches: [main]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install

      - name: Publish with Changesets
        uses: changesets/action@v1
        with:
          publish: bun run publish
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**package.json (root):**
```json
{
  "scripts": {
    "publish": "changeset publish"
  }
}
```

### Cross-package Dependencies
```json
{
  "name": "@myorg/pkg-b",
  "dependencies": {
    "@myorg/pkg-a": "workspace:*"
  }
}
```

**On publish, `workspace:*` is replaced with actual version:**
```json
{
  "dependencies": {
    "@myorg/pkg-a": "^1.2.0"
  }
}
```

---

## Cross-references

Related documentation for Bun publishing workflows:

- **[bun-npm-publishing-part1-setup.md](./bun-npm-publishing-part1-setup.md)** - Setup & Configuration (OIDC, tokens, versioning, registry)
- **[bun-github-actions-index.md](./bun-github-actions-index.md)** - GitHub Actions CI/CD patterns for Bun projects
- **[bun-testing-index.md](./bun-testing-index.md)** - Testing strategies before publishing
- **[bun-build-api-index.md](./bun-build-api-index.md)** - Building distributable packages with Bun

**See also:**
- Official npm docs: https://docs.npmjs.com/cli/v10/commands/npm-publish
- Changesets: https://github.com/changesets/changesets
- Semantic Versioning: https://semver.org/
- npm dist-tags: https://docs.npmjs.com/cli/v10/commands/npm-dist-tag
