# npm Publishing with Bun - Part 1: Setup & Configuration

## Table of Contents
1. [OIDC Trusted Publishing](#oidc-trusted-publishing)
   - 1.1 [Configure npm Package](#step-1-configure-npm-package)
   - 1.2 [Required Permissions](#step-2-required-permissions)
   - 1.3 [Registry URL Required](#step-3-registry-url-required)
   - 1.4 [Use npm for Publishing](#step-4-use-npm-not-bun-for-publishing)
   - 1.5 [Scoped Packages](#scoped-packages)
   - 1.6 [Critical Lessons Learned](#critical-lessons-learned)
2. [Traditional npm Token Publishing](#traditional-npm-token-publishing)
   - 2.1 [Generate npm Token](#step-1-generate-npm-token)
   - 2.2 [Add Token to GitHub Secrets](#step-2-add-token-to-github-secrets)
   - 2.3 [Configure .npmrc in Workflow](#step-3-configure-npmrc-in-workflow)
   - 2.4 [Publish with npm](#step-4-publish-with-npm)
3. [Version Management](#version-management)
   - 3.1 [Semantic Versioning Format](#semantic-versioning-format)
   - 3.2 [Using npm version Commands](#using-npm-version-commands)
   - 3.3 [Automated Version Bumping in CI](#automated-version-bumping-in-ci)
   - 3.4 [Changelog Generation](#changelog-generation)
4. [Pre-publish Validation](#pre-publish-validation)
   - 4.1 [prepublishOnly Script](#prepublishonly-script)
   - 4.2 [Dry Run Publishing](#dry-run-publishing)
   - 4.3 [Package Validation with npm pack](#package-validation-with-npm-pack)
   - 4.4 [Common Pre-publish Checklist](#common-pre-publish-checklist)
5. [Registry Configuration](#registry-configuration)
   - 5.1 [Default npm Registry](#default-npm-registry)
   - 5.2 [GitHub Packages Registry](#github-packages-registry)
   - 5.3 [Private Registry](#private-registry-verdaccio-artifactory-etc)
   - 5.4 [Multiple Registries](#multiple-registries-in-one-project)

**See also**: [Part 2: Advanced Publishing](./bun-npm-publishing-part2-advanced.md)

---

## OIDC Trusted Publishing

## Step 1: Configure npm Package
Go to https://www.npmjs.com/package/@scope/name/access

Add trusted publisher (OIDC or provenance):
| Field | Value |
|-------|-------|
| Owner | GitHub username/org |
| Repository | Repo name |
| Workflow | .github/workflows/publish.yml |

## Step 2: Required Permissions
```yaml
permissions:
  id-token: write  # Generates OIDC or provenance token
  contents: write  # For GitHub Release
```

## Step 3: Registry URL Required
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '24'
    registry-url: 'https://registry.npmjs.org'  # REQUIRED
```

## Step 4: Use npm (NOT bun) for Publishing
```yaml
- run: npm publish --access public
```

bun publish does NOT support OIDC or provenance as of January 2026.

**Tracking Issue**: https://github.com/oven-sh/bun/issues/15601

## Scoped Packages
Use --access public or set in package.json:
```json
{ "publishConfig": { "access": "public" } }
```

## Critical Lessons Learned

### Registry URL is Required for OIDC
Without `registry-url: 'https://registry.npmjs.org'` in setup-node, npm OIDC or provenance authentication will fail silently, hang, or attempt to use alternative authentication methods. This is the most common cause of workflow failures during trusted publishing setup. Always verify this line is present in your workflow.

### Scoped Packages Require --access public
When publishing @scope/name packages, you MUST use `npm publish --access public` in the workflow or set `"publishConfig": { "access": "public" }` in package.json. Without this, scoped package publishing will fail with permission errors.

---

## Traditional npm Token Publishing

When OIDC is not available or not desired, use traditional npm tokens for authentication.

### Step 1: Generate npm Token
1. Log in to npmjs.com
2. Go to **Account Settings** → **Access Tokens**
3. Click **Generate New Token**
4. Choose token type:
   - **Automation** - For CI/CD workflows (recommended)
   - **Publish** - For manual publishing
   - **Read-only** - For installation only

### Step 2: Add Token to GitHub Secrets
1. Go to GitHub repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `NPM_TOKEN`
4. Value: Paste the token from npmjs.com

### Step 3: Configure .npmrc in Workflow
```yaml
- name: Setup .npmrc
  run: |
    echo "//registry.npmjs.org/:_authToken=${{ secrets.NPM_TOKEN }}" > ~/.npmrc
```

### Step 4: Publish with npm
```yaml
- run: npm publish --access public
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Alternative: Use setup-node with Token
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '24'
    registry-url: 'https://registry.npmjs.org'
- run: npm publish --access public
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Why use traditional tokens?**
- Works with all npm-compatible registries
- No dependency on OIDC provider
- Simpler setup for private registries
- Compatible with bun publish (when bun adds token support)

---

## Version Management

Proper version management is critical for npm publishing. Follow semantic versioning (SemVer).

### Semantic Versioning Format
`MAJOR.MINOR.PATCH` (e.g., `1.4.2`)

- **MAJOR** - Breaking changes (1.0.0 → 2.0.0)
- **MINOR** - New features, backward compatible (1.0.0 → 1.1.0)
- **PATCH** - Bug fixes, backward compatible (1.0.0 → 1.0.1)

### Using npm version Commands
```bash
# Patch release (1.0.0 → 1.0.1)
npm version patch

# Minor release (1.0.0 → 1.1.0)
npm version minor

# Major release (1.0.0 → 2.0.0)
npm version major

# Pre-release (1.0.0 → 1.0.1-beta.0)
npm version prerelease --preid=beta

# Specific version
npm version 2.5.0
```

**What npm version does:**
1. Updates `version` field in `package.json`
2. Creates a git commit with message `v<version>`
3. Creates a git tag `v<version>`

### Automated Version Bumping in CI
```yaml
- name: Bump version
  run: |
    git config user.name "GitHub Actions"
    git config user.email "actions@github.com"
    npm version patch -m "Release v%s"
    git push --follow-tags
```

### Changelog Generation
Use `auto-changelog` or `conventional-changelog`:

```bash
# Install
bun add -D auto-changelog

# Generate CHANGELOG.md
bunx auto-changelog

# Add to package.json scripts
{
  "scripts": {
    "version": "auto-changelog -p && git add CHANGELOG.md"
  }
}
```

Now `npm version` will automatically update the changelog.

### Version Constraints in package.json
```json
{
  "engines": {
    "node": ">=18.0.0",
    "bun": ">=1.0.0"
  }
}
```

---

## Pre-publish Validation

Validate your package before publishing to catch errors early.

### prepublishOnly Script
Add to `package.json`:
```json
{
  "scripts": {
    "prepublishOnly": "bun run build && bun test"
  }
}
```

**Runs automatically before `npm publish`**. Use to:
- Build distribution files
- Run tests
- Lint code
- Type check

### Dry Run Publishing
Test publishing without actually publishing:
```bash
npm publish --dry-run
```

**Output shows:**
- Files included in package
- Package size
- tarball contents
- Warnings and errors

### Package Validation with npm pack
```bash
# Create tarball locally
npm pack

# Extract and inspect
tar -tzf <package-name>-<version>.tgz

# Test installation from tarball
cd /tmp/test-install
npm install /path/to/<package-name>-<version>.tgz
```

### Files Array Validation
Verify which files will be published:
```bash
npm publish --dry-run 2>&1 | grep -A 100 "package size"
```

### Linting and Type Checking
```json
{
  "scripts": {
    "prepublishOnly": "bun run lint && bun run typecheck && bun test && bun run build"
  }
}
```

### Common Pre-publish Checklist
- [ ] All tests pass
- [ ] Build artifacts exist (dist/, build/)
- [ ] README.md is up to date
- [ ] CHANGELOG.md is updated
- [ ] Version number is correct
- [ ] files array includes all necessary files
- [ ] main/module/exports point to correct files
- [ ] Dependencies are production-only (no dev deps)
- [ ] package.json metadata is accurate

---

## Registry Configuration

Configure npm to publish to different registries: npm, GitHub Packages, private registries.

### Default npm Registry
```bash
# Set default registry
npm config set registry https://registry.npmjs.org/

# Verify
npm config get registry
```

### GitHub Packages Registry
Publish to GitHub Packages instead of npmjs.com.

**Step 1: Add .npmrc to repository**
```
@your-org:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NODE_AUTH_TOKEN}
```

**Step 2: Update package.json**
```json
{
  "name": "@your-org/package-name",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/your-org/repo.git"
  },
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  }
}
```

**Step 3: Workflow with GITHUB_TOKEN**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '24'
    registry-url: 'https://npm.pkg.github.com'
    scope: '@your-org'
- run: npm publish
  env:
    NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Private Registry (Verdaccio, Artifactory, etc.)
```json
{
  "publishConfig": {
    "registry": "https://npm.company.com/"
  }
}
```

**.npmrc for private registry:**
```
registry=https://npm.company.com/
//npm.company.com/:_authToken=${NPM_TOKEN}
```

### Scoped Package Registry
Publish scoped packages to different registries:
```bash
# Set registry for @myorg scope
npm config set @myorg:registry https://npm.pkg.github.com
```

In `.npmrc`:
```
@myorg:registry=https://npm.pkg.github.com
@other-org:registry=https://registry.npmjs.org
```

### Multiple Registries in One Project
```
# Default registry
registry=https://registry.npmjs.org/

# GitHub Packages for @myorg
@myorg:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}

# Private registry for @company
@company:registry=https://npm.company.com
//npm.company.com/:_authToken=${COMPANY_NPM_TOKEN}
```

---

**Continue to**: [Part 2: Advanced Publishing](./bun-npm-publishing-part2-advanced.md)
