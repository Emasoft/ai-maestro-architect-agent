# Bun Troubleshooting: Validation Issues (Part 7)

> **Navigation**: [Index](bun-troubleshooting.md) | [Part 6: Sourcemaps](bun-troubleshooting-part6-sourcemaps.md)

This section covers JSON validation, UMD validation, and version banner issues.

---

## 12. JSON Validation Fails on tsconfig.json

### Problem Description

When running JSON linting tools on your project, they fail on `tsconfig.json` with errors like:

```
error: invalid JSON - comments are not allowed
error: JSONError: Unexpected token / in JSON at position 452
```

Even though the file works perfectly with TypeScript tools, standard JSON validators reject it.

### Root Cause

TypeScript configuration files use JSONC (JSON with Comments), which is an extended JSON format that supports:
- Single-line comments: `// comment`
- Multi-line comments: `/* comment */`
- Trailing commas in arrays and objects

Standard JSON validators only accept pure JSON and reject these extensions. This causes validation tools to fail, even though TypeScript parses JSONC perfectly.

### Solution

Configure your JSON validation tools to skip `tsconfig.json` or use TypeScript-aware validation instead.

**Step 1**: Update your jsonlint configuration to exclude tsconfig.json:

```bash
# If using jsonlint or similar tools
jsonlint --exclude tsconfig.json --exclude tsconfig.*.json src/
```

**Step 2**: Create a `.jsonlintrc` configuration file:

```jsonc
{
  "exclude": [
    "tsconfig.json",
    "tsconfig.*.json",
    "node_modules/**"
  ],
  "defaultIndentation": 2
}
```

**Step 3**: Use TypeScript compiler for validation instead:

```bash
# Validate tsconfig.json with tsc
tsc --noEmit
```

This validates the TypeScript configuration using the TypeScript compiler itself.

**Step 4**: In CI/CD pipelines, skip tsconfig files:

```yaml
# GitHub Actions example
- name: Validate JSON files
  run: |
    find . -name "*.json" \
      ! -name "tsconfig.json" \
      ! -name "tsconfig.*.json" \
      ! -path "./node_modules/*" \
      -exec jsonlint {} \;
```

### Complete tsconfig.json Example with Comments

```jsonc
{
  "compilerOptions": {
    // Target modern JavaScript
    "target": "ES2022",
    // Use ES modules
    "module": "ESNext",
    // Resolve modules like bundlers do
    "moduleResolution": "bundler",
    // Include ES2022 library types
    "lib": ["ES2022"],
    // Enforce strict type checking
    "strict": true,
    // Enable esModuleInterop for CommonJS compatibility
    "esModuleInterop": true,
    // Skip type checking of declaration files
    "skipLibCheck": true,
    // Generate TypeScript declarations
    "declaration": true,
    // Generate declaration source maps
    "declarationMap": true,
    // Only emit declarations, not JavaScript
    "emitDeclarationOnly": true,
    // Output directory for declarations
    "outDir": "./dist",
    // Source directory
    "rootDir": "./src"
  },
  // Include all TypeScript files
  "include": ["src/**/*"],
  // Exclude node_modules, dist, and test files
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### Using json5 or JSONC Parser

For tools that need to parse JSONC files, use libraries that support JSON with comments:

**Using json5 library**:

```bash
npm install --save-dev json5
```

```javascript
// validate.js
import JSON5 from 'json5';
import { readFileSync } from 'fs';

try {
  const config = JSON5.parse(readFileSync('tsconfig.json', 'utf-8'));
  console.log('✓ tsconfig.json is valid');
} catch (error) {
  console.error('✗ Invalid tsconfig.json:', error.message);
  process.exit(1);
}
```

### Validation Script Example

Create a validation script that handles both JSON and JSONC:

```javascript
// scripts/validate-json.js
import JSON5 from 'json5';
import { readFileSync, readdirSync } from 'fs';
import { join } from 'path';

const jsonExtensions = ['.json'];
const jsonWithCommentsFiles = ['tsconfig.json', 'tsconfig.*.json'];

function validateFiles() {
  const files = readdirSync('.').filter(f =>
    f.endsWith('.json')
  );

  let errors = 0;

  for (const file of files) {
    // Skip JSONC files - they need special handling
    if (jsonWithCommentsFiles.some(pattern => {
      const regex = new RegExp('^' + pattern.replace('*', '.*') + '$');
      return regex.test(file);
    })) {
      try {
        const content = readFileSync(file, 'utf-8');
        JSON5.parse(content);
        console.log(`✓ ${file} (JSONC)`);
      } catch (error) {
        console.error(`✗ ${file}:`, error.message);
        errors++;
      }
    } else {
      // Standard JSON validation
      try {
        const content = readFileSync(file, 'utf-8');
        JSON.parse(content);
        console.log(`✓ ${file}`);
      } catch (error) {
        console.error(`✗ ${file}:`, error.message);
        errors++;
      }
    }
  }

  if (errors > 0) {
    process.exit(1);
  }
}

validateFiles();
```

**package.json**:
```json
{
  "scripts": {
    "validate:json": "bun run scripts/validate-json.js"
  }
}
```

### Best Practices

**When to use JSONC in tsconfig.json**:
```jsonc
{
  "compilerOptions": {
    // Explains what this target does
    "target": "ES2022",
    // These options enable strict type checking
    "strict": true,
    /*
     * This is a complex option that requires explanation
     * because it affects how module resolution works
     */
    "moduleResolution": "bundler"
  }
}
```

**Avoid JSONC in other JSON files**:
```json
{
  "name": "my-package",
  "version": "1.0.0"
}
```

These should remain pure JSON for maximum compatibility.

### ESLint Configuration Example

If using ESLint to validate JSON files:

**.eslintignore**:
```
tsconfig.json
tsconfig.*.json
```

### When This Issue Occurs

- Running JSON validators on TypeScript projects
- Using linting tools like jsonlint or eslint-plugin-json
- CI/CD pipelines validating all JSON files
- Pre-commit hooks checking file formats
- JSON schema validation tools
- Build scripts that validate project structure

---

## 13. UMD Validation Fails After Bun Build

### Problem Description

Release scripts that validate UMD output by checking for `module.exports` fail when using Bun's minifier.

**Error message:**
```
UMD wrapper missing CommonJS export (module.exports)
```

### Root Cause

Bun's minifier aggressively shortens variable names. The standard UMD pattern:
```javascript
typeof module === "object" && module.exports
```

Gets minified to:
```javascript
typeof t=="object"&&t.exports
```

The runtime behavior is identical, but string-matching validation fails.

### Solution

Update validation to check for the `.exports` pattern instead of the literal `module.exports`:

**Bash (release scripts):**
```bash
# Instead of:
grep -qF 'module.exports' "$MINIFIED_FILE"

# Use:
grep -qE '\.exports' "$MINIFIED_FILE"  # Matches both module.exports and t.exports
```

**JavaScript:**
```javascript
// Instead of: /module\.exports/
// Use: /\.exports/  // Matches both module.exports and t.exports
```

### Important Note

This is expected behavior from Bun's minifier and does NOT break UMD compatibility - the runtime logic is preserved, only the variable name changes.

---

## 14. Minified File Has Wrong Version in Banner

### Problem Description

After running `npm version`, the minified file banner still shows the old version number.

**Example:**
```
After bump: package.json shows 1.1.2
But minified banner shows: /*! MyLib.js v1.1.1 | MIT License */
```

### Root Cause

`npm version` updates package.json but doesn't rebuild bundles. The version in banner comments is embedded at build time and isn't automatically updated.

### Solution

Always rebuild after version bump:

```bash
# Bump version
npm version patch --no-git-tag-version

# Rebuild to update version in banners
bun run build.js

# Commit both files
git add package.json pnpm-lock.yaml dist/
git commit -m "chore(release): Bump version to X.Y.Z"
```

### Automated Approach (in release scripts)

```bash
bump_version() {
  npm version "$VERSION_TYPE" --no-git-tag-version
  bun run build.js  # Regenerate with new version in banner

  # Verify version sync
  local pkg_version=$(jq -r '.version' package.json)
  local banner_version=$(head -1 "$MINIFIED_FILE" | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+')

  if [[ "v$pkg_version" != "$banner_version" ]]; then
    echo "Version mismatch: package.json=$pkg_version, banner=$banner_version"
    exit 1
  fi
}
```

### Prevention

Add a pre-commit hook or CI check to validate version consistency:

```bash
#!/bin/bash
# .husky/pre-commit or CI script
PKG_VERSION=$(jq -r '.version' package.json)
BANNER_VERSION=$(head -1 dist/bundle.min.js | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' || echo "none")

if [[ "v$PKG_VERSION" != "$BANNER_VERSION" ]]; then
  echo "ERROR: Version mismatch - run 'bun run build.js' after version bump"
  exit 1
fi
```

---

## Summary

This troubleshooting guide covers the 14 most common issues with Bun:

1. **OIDC Authentication** - Use `npm publish` instead of `bun publish`
2. **Unpinned Versions** - Pin to specific version: `bun-version: '1.1.42'`
3. **Node.js Modules** - Use `external: ['fs', 'path', ...]`
4. **Global Names** - Use unique `globalName` for IIFE bundles
5. **Version Mismatch** - Validate tag matches package.json
6. **GitHub Permissions** - Add `contents: write` permission
7. **Test Timeouts** - Use `--timeout 30000` or per-test timeouts
8. **Missing Registry** - Set `registry-url: 'https://registry.npmjs.org'`
9. **TypeScript Declarations** - Run `tsc --emitDeclarationOnly` after build
10. **CSS Bundling** - Configure `loader: { '.css': 'css' }`
11. **Sourcemaps** - Use `sourcemap: 'linked'` with correct `publicPath`
12. **JSON Validation** - Skip tsconfig.json in JSON validators or use tsc --noEmit
13. **UMD Validation** - Check for `.exports` pattern, not literal `module.exports`
14. **Version Banner** - Rebuild after `npm version` to update minified file banners

For additional help, consult:
- [Bun Documentation](https://bun.sh/docs)
- [Bun GitHub Issues](https://github.com/oven-sh/bun/issues)
- [Bun Discord Community](https://bun.sh/discord)

---

> **Back to**: [Index](bun-troubleshooting.md)
