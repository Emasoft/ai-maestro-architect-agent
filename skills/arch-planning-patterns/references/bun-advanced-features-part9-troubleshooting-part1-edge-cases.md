# Bun Advanced Features Part 9.1: Edge Cases

## Table of Contents
- 1.1 [Monorepo / Workspaces](#monorepo--workspaces)
- 1.2 [Dynamic Imports](#dynamic-imports)
- 1.3 [Binary / Native Modules](#binary--native-modules)
- 1.4 [JSON Imports](#json-imports)

---

## Monorepo / Workspaces

When building applications that use workspace packages, you need to explicitly mark workspace packages as external to prevent bundling local workspace code into your output.

**Problem: Workspace packages being bundled instead of linked**

When you have multiple packages in a monorepo and some packages reference other workspace packages, Bun might try to bundle the referenced packages directly into the output, which defeats the purpose of using workspaces.

**Solution: Mark workspace packages as external**

Use the `external` option in your build configuration to prevent bundling workspace packages:

```javascript
// build.js
await Bun.build({
  entrypoints: ['apps/web/src/index.js'],
  outdir: 'apps/web/dist',
  target: 'node',
  external: [
    '@myorg/core',    // Explicitly list workspace packages
    '@myorg/utils',
    '@myorg/types'
  ]
});
```

**Alternative: Pattern-based external matching**

For larger monorepos with many workspace packages, you can use a more dynamic approach:

```javascript
// build.js
const workspacePatterns = ['@myorg/*'];  // Match all packages in @myorg scope

await Bun.build({
  entrypoints: ['apps/web/src/index.js'],
  outdir: 'apps/web/dist',
  target: 'node',
  external: workspacePatterns
});
```

**Key considerations:**

- Always use the scoped package name (`@myorg/package`) in the external array, not the directory name
- Workspace packages must be published or available at runtime for the application to function
- External workspace packages should already be installed in `node_modules/` through the workspace protocol
- If workspace packages have dependencies, those must also be external or explicitly handled

---

## Dynamic Imports

Dynamic imports require special build configuration to work correctly when creating separate chunks for each dynamically imported module.

**Problem: Dynamic imports not creating separate chunks**

When you use `import()` in your code, Bun should automatically create separate chunks, but this only happens when the correct build options are enabled.

**Solution: Enable splitting and configure chunk naming**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  splitting: true,  // Required for dynamic imports to create chunks
  format: 'esm',    // Required: splitting only works with ESM format
  naming: {
    chunk: '[name]-[hash].[ext]'  // Name pattern for dynamic import chunks
  }
});
```

**Chunk naming patterns:**

- `[name]` - Replaces with the original module name
- `[hash]` - Replaces with a hash of the module content
- `[dir]` - Replaces with the directory path
- `[ext]` - Replaces with the file extension (usually 'js')

**Example with custom chunk naming:**

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  splitting: true,
  format: 'esm',
  naming: {
    chunk: 'chunks/[name]-[hash].[ext]',  // Organize chunks in a subdirectory
    entry: '[dir]/[name].[ext]'
  }
});
```

**Result structure:**

```
dist/
├── index.js                    # Main entry point
├── chunks/
│   ├── feature-a-abc123.js    # Dynamic import chunk
│   ├── heavy-module-def456.js  # Dynamic import chunk
│   └── shared-ghi789.js        # Shared code between chunks
```

**Important notes:**

- `splitting: true` is required for proper code splitting
- ESM (`format: 'esm'`) is the only format that supports splitting
- CommonJS format will bundle everything into a single file
- Without splitting enabled, dynamic imports will still work but won't create separate files

---

## Binary / Native Modules

Binary and native modules are compiled code (`.node` files) that cannot be bundled. They must always be marked as external.

**Problem: Native modules causing build errors**

When you try to bundle native modules like `better-sqlite3`, `canvas`, or `sharp`, Bun cannot bundle the compiled binary files and produces errors.

**Solution: Mark all native modules as external**

Identify all native modules in your dependencies and explicitly mark them as external:

```javascript
// build.js
const nativeModules = [
  'better-sqlite3',  // Database
  'canvas',          // Image rendering
  'sharp',           // Image processing
  'sqlite3',         // Another database option
  'node-rdkafka',    // Apache Kafka client
  'cpu-features',    // CPU feature detection
  'v8'               // V8 engine bindings
];

await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  target: 'node',
  external: nativeModules
});
```

**Common native modules to mark external:**

| Package | Purpose | Notes |
|---------|---------|-------|
| `better-sqlite3` | SQLite database | Synchronous, requires binary |
| `sharp` | Image processing | Prebuilt binaries available |
| `canvas` | Node canvas rendering | Requires system graphics libraries |
| `bcrypt` | Password hashing | Has optional native module |
| `sqlite3` | SQLite driver | Alternative to better-sqlite3 |
| `node-rdkafka` | Apache Kafka client | Native C++ bindings |
| `leveldown` | LevelDB wrapper | Binary database |
| `re2` | Regular expression library | C++ binding |

**Dynamic detection of native modules:**

```javascript
// build.js
import { readFileSync } from 'fs';

const pkg = JSON.parse(readFileSync('./package.json', 'utf-8'));

// Extract optionalDependencies and devDependencies that are typically native
const nativeKeywords = ['sqlite', 'native', 'canvas', 'sharp', 'bcrypt', 'kafka'];
const externalModules = Object.keys(pkg.dependencies || {}).filter(dep =>
  nativeKeywords.some(keyword => dep.toLowerCase().includes(keyword))
);

console.log('Detected native modules:', externalModules);

await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  external: externalModules
});
```

**Key points:**

- Native modules must be in `node_modules/` at runtime
- The binary files (`.node`) are platform and architecture specific
- Distribution must include `node_modules/` with the correct binaries
- Rebuilding on the target platform is often necessary: `bun install --force`

---

## JSON Imports

JSON imports work by default in Bun, but you can customize how JSON is handled during bundling.

**Default behavior: JSON is inlined**

By default, when you import JSON files, Bun parses them at build time and inlines the parsed object into your bundle:

```javascript
// src/config.json
{
  "apiUrl": "https://api.example.com",
  "timeout": 5000
}

// src/index.js
import config from './config.json';
console.log(config.apiUrl);  // Works automatically
```

**Custom loader for JSON-as-string**

If you need JSON to remain as a string instead of being parsed into an object, you can use a custom loader:

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  loader: {
    '.json': 'text'  // Treat JSON files as plain text strings
  }
});
```

**With custom loader - JSON stays as string:**

```javascript
// src/index.js
import configStr from './config.json';  // configStr is now a string, not an object

const config = JSON.parse(configStr);   // Parse when needed
console.log(config.apiUrl);
```

**When to use each approach:**

| Approach | Use Case | Pros | Cons |
|----------|----------|------|------|
| Default (parsed) | Static configuration | Small bundle, fast access | JSON must be valid at build time |
| Custom text loader | Dynamic JSON processing | Can manipulate as string | Larger bundle if many JSON files |
| Dynamic import | Runtime JSON loading | Most flexible | Additional HTTP request |

---

**Next:** [Part 9.2 - Troubleshooting](./bun-advanced-features-part9-troubleshooting-part2-troubleshooting.md)

**Index:** [Part 9 - Edge Cases and Troubleshooting](./bun-advanced-features-part9-troubleshooting.md)
