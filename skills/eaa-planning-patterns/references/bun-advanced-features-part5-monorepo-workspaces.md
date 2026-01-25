# Bun Advanced Features: Monorepo and Workspaces

> **Part 5 of 10** | See [bun-advanced-features.md](./bun-advanced-features.md) for the complete index.

---

## Monorepo and Workspaces

### What is a Monorepo?

A monorepo (monolithic repository) is a single repository that contains multiple projects or packages. These packages can depend on each other and share common tooling and configuration.

### What are Workspaces?

Workspaces are a way to manage multiple packages within a single repository. Each workspace is a separate package with its own `package.json`, but they all share a common root and can reference each other as dependencies.

### Why Use Monorepos and Workspaces?

- **Code Sharing**: Easily share code between related packages
- **Atomic Commits**: Change multiple packages in a single commit
- **Unified Versioning**: Coordinate releases across packages
- **Single Build Tool**: Use one set of build tools for all packages
- **Simplified Dependencies**: Automatic linking between workspace packages
- **Faster Development**: Install dependencies once for all packages

### Setting Up a Monorepo with Bun

**Project Structure:**

```
my-monorepo/
├── package.json           # Root package.json
├── bun.lockb             # Bun lockfile
├── packages/
│   ├── core/
│   │   ├── package.json
│   │   ├── src/
│   │   │   └── index.js
│   │   └── tsconfig.json
│   ├── utils/
│   │   ├── package.json
│   │   ├── src/
│   │   │   └── index.js
│   │   └── tsconfig.json
│   └── cli/
│       ├── package.json
│       ├── src/
│       │   └── index.js
│       └── tsconfig.json
└── apps/
    ├── web/
    │   ├── package.json
    │   └── src/
    │       └── index.js
    └── api/
        ├── package.json
        └── src/
            └── index.js
```

**Root package.json:**

```json
{
  "name": "my-monorepo",
  "version": "1.0.0",
  "workspaces": [
    "packages/*",
    "apps/*"
  ],
  "devDependencies": {
    "typescript": "^5.0.0"
  },
  "scripts": {
    "build": "bun run build:packages && bun run build:apps",
    "build:packages": "bun run --filter './packages/*' build",
    "build:apps": "bun run --filter './apps/*' build",
    "test": "bun test"
  }
}
```

### Workspace Package Configuration

**packages/core/package.json:**

```json
{
  "name": "@myorg/core",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "bun build src/index.js --outdir dist --format esm",
    "dev": "bun --watch src/index.js"
  }
}
```

**packages/utils/package.json:**

```json
{
  "name": "@myorg/utils",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "dependencies": {
    "@myorg/core": "workspace:*"
  },
  "scripts": {
    "build": "bun build src/index.js --outdir dist --format esm",
    "dev": "bun --watch src/index.js"
  }
}
```

**apps/web/package.json:**

```json
{
  "name": "@myorg/web",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@myorg/core": "workspace:*",
    "@myorg/utils": "workspace:*",
    "react": "^18.0.0"
  },
  "scripts": {
    "build": "bun build src/index.js --outdir dist",
    "dev": "bun --watch src/index.js"
  }
}
```

### Installing Dependencies in a Workspace

**Install for all workspaces:**

```bash
# From root
bun install
```

**Install a dependency in a specific workspace:**

```bash
# From root
bun add react --cwd packages/core

# Or from the workspace directory
cd packages/core
bun add react
```

**Install a dev dependency:**

```bash
bun add -d typescript --cwd packages/core
```

### Workspace Protocol

The `workspace:*` protocol tells Bun to link to the local workspace version:

```json
{
  "dependencies": {
    "@myorg/core": "workspace:*",
    "@myorg/utils": "workspace:^"
  }
}
```

- `workspace:*` - Always use the current version
- `workspace:^` - Use compatible version (respects semver)
- `workspace:~` - Use patch-level compatible version

### Running Scripts Across Workspaces

**Run a script in all workspaces:**

```bash
# Run build in all workspaces
bun run --filter '*' build
```

**Run a script in specific workspaces:**

```bash
# Run build in packages/* only
bun run --filter './packages/*' build

# Run test in apps/* only
bun run --filter './apps/*' test
```

**Run a script in a specific package:**

```bash
# Run build in @myorg/core
bun run --filter '@myorg/core' build
```

### Building a Monorepo Library

**packages/core/src/index.js:**

```javascript
export function createApp(config) {
  return {
    name: config.name,
    start() {
      console.log(`Starting ${this.name}...`);
    }
  };
}

export const VERSION = '1.0.0';
```

**packages/utils/src/index.js:**

```javascript
import { VERSION } from '@myorg/core';

export function formatVersion() {
  return `v${VERSION}`;
}

export function logger(message) {
  console.log(`[${formatVersion()}] ${message}`);
}
```

**apps/web/src/index.js:**

```javascript
import { createApp } from '@myorg/core';
import { logger } from '@myorg/utils';

const app = createApp({ name: 'WebApp' });

logger('Application initialized');
app.start();
```

### Build Configuration for Monorepo

**Root build.js:**

```javascript
import { readdirSync } from 'fs';
import { join } from 'path';

const packagesDir = 'packages';
const packages = readdirSync(packagesDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory())
  .map(dirent => dirent.name);

console.log('Building packages:', packages);

for (const pkg of packages) {
  const pkgPath = join(packagesDir, pkg);
  const srcPath = join(pkgPath, 'src/index.js');
  const outDir = join(pkgPath, 'dist');

  console.log(`Building ${pkg}...`);

  await Bun.build({
    entrypoints: [srcPath],
    outdir: outDir,
    format: 'esm',
    target: 'node',
    minify: false,
    sourcemap: 'external'
  });

  console.log(`✓ Built ${pkg}`);
}

console.log('\n✓ All packages built successfully');
```

**Run Build:**

```bash
bun run build.js
```

### Shared TypeScript Configuration

**Root tsconfig.json:**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "allowJs": true,
    "declaration": true,
    "declarationMap": true,
    "outDir": "dist",
    "rootDir": "src"
  }
}
```

**packages/core/tsconfig.json:**

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Versioning and Publishing

**Using Changesets:**

```bash
# Install changesets
bun add -d @changesets/cli

# Initialize
bunx changeset init
```

**Create a changeset:**

```bash
bunx changeset
```

**Version packages:**

```bash
bunx changeset version
```

**Publish packages:**

```bash
bunx changeset publish
```

### Monorepo Build Optimization

**Parallel Builds:**

```javascript
// build-parallel.js
import { readdirSync } from 'fs';
import { join } from 'path';

const packagesDir = 'packages';
const packages = readdirSync(packagesDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory())
  .map(dirent => dirent.name);

// Build all packages in parallel
const buildPromises = packages.map(async (pkg) => {
  const pkgPath = join(packagesDir, pkg);
  const srcPath = join(pkgPath, 'src/index.js');
  const outDir = join(pkgPath, 'dist');

  console.log(`Building ${pkg}...`);

  await Bun.build({
    entrypoints: [srcPath],
    outdir: outDir,
    format: 'esm'
  });

  return pkg;
});

const results = await Promise.all(buildPromises);
console.log('✓ Built packages:', results.join(', '));
```

### Monorepo Best Practices

1. **Use workspace protocol**: Always use `workspace:*` for local dependencies
2. **Shared configuration**: Put common configs in the root (tsconfig, eslint, etc.)
3. **Consistent naming**: Use scoped packages (`@myorg/package-name`)
4. **Build order**: Build dependencies before dependents
5. **Parallel builds**: Build independent packages in parallel
6. **Single lockfile**: Keep one `bun.lockb` at the root
7. **Private packages**: Mark non-publishable packages as `"private": true`
8. **Version together**: Consider using changesets or lerna for versioning
9. **Test from root**: Run tests from root to catch cross-package issues
10. **Document structure**: Maintain a clear README explaining the monorepo structure

---

## Cross-References

- **Previous**: [Part 4: CDN and Browser Usage](./bun-advanced-features-part4-cdn-browser.md)
- **Next**: [Part 6: Dynamic Imports](./bun-advanced-features-part6-dynamic-imports.md)
- **Related**: [Part 9: Edge Cases](./bun-advanced-features-part9-edge-cases.md) - Workspace-specific edge cases
- **Index**: [Bun Advanced Features](./bun-advanced-features.md) - Complete feature index
