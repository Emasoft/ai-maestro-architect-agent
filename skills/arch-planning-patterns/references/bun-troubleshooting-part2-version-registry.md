# Bun Troubleshooting: Version & Registry Issues (Part 2)

> **Navigation**: [Index](bun-troubleshooting.md) | [Part 1: CI Publishing](bun-troubleshooting-part1-ci-publishing.md) | [Part 3: Permissions & Tests](bun-troubleshooting-part3-permissions-tests.md)

This section covers version mismatch and registry configuration issues.

---

## 5. Version Mismatch

### Problem Description

When publishing packages via GitHub releases, the version in the Git tag does not match the version in `package.json`:

```
Tag: v1.2.3
package.json: 1.2.2
```

This causes:
- Confusion about which version is actually published
- npm showing incorrect version numbers
- Changelog mismatches
- Failed installations due to version conflicts

### Root Cause

The GitHub release workflow is triggered by creating a Git tag, but the `package.json` version must be updated separately. If these steps are not synchronized, the versions diverge.

Common scenarios:
1. Developer creates a Git tag without updating `package.json`
2. Developer updates `package.json` but creates wrong Git tag
3. Automated release process doesn't validate version consistency

### Solution

Add validation to your GitHub Actions workflow to ensure tag and package.json versions match before publishing.

**Step 1**: Create a version validation script:

```javascript
// scripts/validate-version.js
const packageJson = require('../package.json');

// Get the tag from GitHub Actions environment
const tag = process.env.GITHUB_REF_NAME;

// Extract version from tag (remove 'v' prefix)
const tagVersion = tag.startsWith('v') ? tag.slice(1) : tag;

// Compare versions
if (packageJson.version !== tagVersion) {
  console.error(`Version mismatch!`);
  console.error(`  package.json: ${packageJson.version}`);
  console.error(`  Git tag:      ${tagVersion}`);
  console.error(`\nPlease update package.json to version ${tagVersion} before creating the tag.`);
  process.exit(1);
}

console.log(`✓ Version validated: ${packageJson.version}`);
```

**Step 2**: Add validation step to your workflow:

```yaml
name: Publish Package
on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v2
        with:
          bun-version: '1.1.42'

      - name: Validate version
        run: bun run scripts/validate-version.js
        env:
          GITHUB_REF_NAME: ${{ github.ref_name }}

      - name: Install dependencies
        run: bun install

      - name: Build
        run: bun run build

      - name: Publish
        run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Step 3**: Create a release checklist:

```markdown
## Release Checklist

Before creating a release:

1. Update `package.json` version:
   ```bash
   npm version 1.2.3 --no-git-tag-version
   ```

2. Update CHANGELOG.md with release notes

3. Commit the changes:
   ```bash
   git add package.json CHANGELOG.md
   git commit -m "chore: bump version to 1.2.3"
   git push
   ```

4. Create and push the tag:
   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```

5. Create GitHub release from the tag
```

### Automated Solution

**Create a package.json update script**:

```javascript
// scripts/bump-version.js
import { readFile, writeFile } from 'fs/promises';

const newVersion = process.argv[2];

if (!newVersion) {
  console.error('Usage: bun run scripts/bump-version.js <version>');
  process.exit(1);
}

// Validate semver format
const semverRegex = /^\d+\.\d+\.\d+$/;
if (!semverRegex.test(newVersion)) {
  console.error('Invalid version format. Use: major.minor.patch (e.g., 1.2.3)');
  process.exit(1);
}

// Update package.json
const packageJson = JSON.parse(await readFile('package.json', 'utf-8'));
packageJson.version = newVersion;
await writeFile('package.json', JSON.stringify(packageJson, null, 2) + '\n');

console.log(`✓ Updated package.json to version ${newVersion}`);
console.log(`\nNext steps:`);
console.log(`  git add package.json`);
console.log(`  git commit -m "chore: bump version to ${newVersion}"`);
console.log(`  git tag v${newVersion}`);
console.log(`  git push && git push --tags`);
```

**Usage**:
```bash
bun run scripts/bump-version.js 1.2.3
```

### When This Issue Occurs

- Publishing packages via GitHub releases
- Automated release workflows
- Manual tagging without version updates
- Multiple contributors creating releases

---

## 8. Missing registry-url

### Problem Description

When publishing to npm from GitHub Actions, authentication fails with errors like:

```
npm ERR! need auth This command requires you to be logged in.
npm ERR! need auth You need to authorize this machine using `npm adduser`
```

Or the package publishes to the wrong registry (GitHub Packages instead of npmjs.org).

### Root Cause

The `actions/setup-node` action needs to know which npm registry to authenticate against. Without the `registry-url` parameter, it:

- Cannot configure authentication properly
- May default to the wrong registry
- Cannot use the `NODE_AUTH_TOKEN` environment variable

### Solution

Add the `registry-url` parameter to the `actions/setup-node` step.

**Step 1**: Configure the registry URL:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    registry-url: 'https://registry.npmjs.org'
```

**Step 2**: Provide the authentication token:

```yaml
- name: Publish to npm
  run: npm publish --provenance --access public
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Complete Example

**Full publish workflow**:

```yaml
name: Publish to npm

on:
  release:
    types: [published]

permissions:
  contents: read
  id-token: write

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v2
        with:
          bun-version: '1.1.42'

      - name: Install dependencies
        run: bun install

      - name: Run tests
        run: bun test --timeout 30000

      - name: Build package
        run: bun run build

      - name: Setup Node.js for npm publishing
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
          scope: '@mycompany'  # Optional: for scoped packages

      - name: Publish to npm
        run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Publishing to Multiple Registries

If you need to publish to multiple registries (npm and GitHub Packages):

```yaml
jobs:
  publish-npm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      - run: bun install
      - run: bun run build
      - run: npm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

  publish-gpr:
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://npm.pkg.github.com'
      - run: bun install
      - run: bun run build
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Registry URLs

**Common npm registries**:
- npm.js: `https://registry.npmjs.org`
- GitHub Packages: `https://npm.pkg.github.com`
- GitLab: `https://gitlab.com/api/v4/packages/npm`
- Azure Artifacts: `https://pkgs.dev.azure.com/<organization>/_packaging/<feed>/npm/registry/`

### Setting Up NPM_TOKEN Secret

**Step 1**: Create an npm access token:
1. Log in to npmjs.com
2. Click your profile → Access Tokens
3. Generate New Token → Classic Token
4. Choose "Automation" type
5. Copy the token

**Step 2**: Add token to GitHub:
1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. New repository secret
4. Name: `NPM_TOKEN`
5. Value: paste your npm token
6. Add secret

**Step 3**: Verify the token has the correct scope:
- Should have "automation" or "publish" scope
- Should not be read-only
- Should not be expired

### When This Issue Occurs

- Publishing packages to npm from GitHub Actions
- Using `actions/setup-node` for publishing
- Authenticating to npm registry
- Publishing scoped packages
- Publishing to private registries

---

> **Next**: [Part 3: Permissions & Tests](bun-troubleshooting-part3-permissions-tests.md)
