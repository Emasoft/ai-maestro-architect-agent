# Bun Advanced Features

> **Index Document** | This file provides an overview and navigation to all advanced Bun bundler features.

This guide covers advanced Bun bundler features essential for production-ready applications. Each topic is covered in detail in its own reference document.

---

## Quick Reference

| Part | Topic | Key Features |
|------|-------|--------------|
| [Part 1](./bun-advanced-features-part1-code-splitting-treeshaking.md) | Code Splitting & Tree Shaking | `splitting`, `define`, `sideEffects` |
| [Part 2](./bun-advanced-features-part2-build-optimization.md) | Build Optimization | `drop`, `banner`, `footer` |
| [Part 3](./bun-advanced-features-part3-standalone-executables.md) | Standalone Executables | `--compile`, cross-platform builds |
| [Part 4](./bun-advanced-features-part4-cdn-browser.md) | CDN and Browser Usage | IIFE, ESM, UMD formats |
| [Part 5](./bun-advanced-features-part5-monorepo-workspaces.md) | Monorepo and Workspaces | `workspaces`, `workspace:*` protocol |
| [Part 6](./bun-advanced-features-part6-dynamic-imports.md) | Dynamic Imports | `import()`, lazy loading |
| [Part 7](./bun-advanced-features-part7-native-modules.md) | Binary and Native Modules | `.node` files, `external` |
| [Part 8](./bun-advanced-features-part8-json-imports.md) | JSON Imports | Static JSON, `resolveJsonModule` |
| [Part 9](./bun-advanced-features-part9-edge-cases.md) | Edge Cases | Workspace bundling, chunk naming |
| [Part 10](./bun-advanced-features-part10-troubleshooting.md) | Troubleshooting | Common issues and solutions |

---

## Part 1: Code Splitting and Tree Shaking

**File**: [bun-advanced-features-part1-code-splitting-treeshaking.md](./bun-advanced-features-part1-code-splitting-treeshaking.md)

### Contents

- **Code Splitting**: Divide your application into smaller chunks loaded on-demand
  - What is Code Splitting and why use it
  - How Bun handles code splitting with `--splitting`
  - Basic and advanced examples
  - Named chunks with `naming.chunk`
  - Manual chunk configuration with `manualChunks`
  - Best practices

- **Tree Shaking with Feature Flags**: Remove unused code from bundles
  - What is tree shaking
  - Feature flags with `define` option
  - Environment-based feature flags
  - Side effects and `sideEffects` field
  - Best practices

### Key Build Options

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  splitting: true,
  define: { ENABLE_FEATURE: 'false' },
  minify: true
});
```

---

## Part 2: Build Optimization

**File**: [bun-advanced-features-part2-build-optimization.md](./bun-advanced-features-part2-build-optimization.md)

### Contents

- **Drop Console and Debugger Statements**: Remove debug code from production
  - Why drop console/debugger
  - Using `drop: ['console', 'debugger']`
  - Conditional dropping based on environment
  - Custom logging alternatives

- **Banner and Footer Injection**: Add custom text to bundle output
  - License headers and copyright notices
  - Polyfill injection
  - Environment configuration
  - UMD wrapper patterns
  - Dynamic generation from package.json

### Key Build Options

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  drop: ['console', 'debugger'],
  banner: '/*! Copyright 2024 */',
  footer: '// Build complete'
});
```

---

## Part 3: Standalone Executables

**File**: [bun-advanced-features-part3-standalone-executables.md](./bun-advanced-features-part3-standalone-executables.md)

### Contents

- What is a standalone executable
- Creating basic executables with `--compile`
- Including dependencies in executables
- Cross-platform builds (Linux, macOS, Windows)
- CLI application examples with argument parsing
- Including static assets
- Server application examples
- Size optimization techniques

### Key Build Command

```bash
bun build src/index.js --compile --outfile=myapp
```

### Cross-Platform Targets

- `bun-linux-x64`
- `bun-darwin-arm64`
- `bun-windows-x64`

---

## Part 4: CDN and Browser Usage

**File**: [bun-advanced-features-part4-cdn-browser.md](./bun-advanced-features-part4-cdn-browser.md)

### Contents

- Creating browser-compatible bundles
- IIFE format with `globalName`
- Multiple module formats (IIFE, ESM, CJS)
- ESM for modern browsers
- CDN-ready package.json configuration
- Using unpkg and jsDelivr
- Import maps for ESM
- Polyfills and browser compatibility
- Source maps for debugging

### Key Build Options

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  format: 'iife',
  globalName: 'MyLib',
  target: 'browser',
  minify: true
});
```

---

## Part 5: Monorepo and Workspaces

**File**: [bun-advanced-features-part5-monorepo-workspaces.md](./bun-advanced-features-part5-monorepo-workspaces.md)

### Contents

- What is a monorepo and workspaces
- Setting up a monorepo with Bun
- Workspace package configuration
- Installing dependencies across workspaces
- Workspace protocol (`workspace:*`, `workspace:^`)
- Running scripts across workspaces with `--filter`
- Building monorepo libraries
- Shared TypeScript configuration
- Versioning with changesets
- Parallel builds optimization

### Key Configuration

```json
{
  "workspaces": ["packages/*", "apps/*"],
  "dependencies": {
    "@myorg/core": "workspace:*"
  }
}
```

---

## Part 6: Dynamic Imports

**File**: [bun-advanced-features-part6-dynamic-imports.md](./bun-advanced-features-part6-dynamic-imports.md)

### Contents

- What are dynamic imports
- Basic syntax with `import()`
- Conditional module loading
- Feature-based dynamic loading
- Error handling for imports
- Plugin system implementation
- Route-based code splitting for web apps
- Locale/translation loading
- Building with dynamic imports
- Best practices

### Key Pattern

```javascript
const module = await import('./feature.js');
module.init();
```

---

## Part 7: Binary and Native Modules

**File**: [bun-advanced-features-part7-native-modules.md](./bun-advanced-features-part7-native-modules.md)

### Contents

- What are binary and native modules
- How Bun handles native modules (N-API)
- Using native modules (sharp, bcrypt, better-sqlite3, canvas)
- Building native modules with Bun
- Creating native addons with node-gyp
- Bundling applications with native modules
- Distributing apps with native dependencies
- Platform-specific modules
- Troubleshooting native modules

### Key Build Options

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  external: ['sharp', 'better-sqlite3', 'bcrypt']
});
```

---

## Part 8: JSON Imports

**File**: [bun-advanced-features-part8-json-imports.md](./bun-advanced-features-part8-json-imports.md)

### Contents

- What are JSON imports
- Basic JSON import syntax
- Import assertions (`assert { type: 'json' }`)
- Dynamic JSON import
- Importing data files and datasets
- Package.json import patterns
- Translation/locale files
- TypeScript with JSON imports
- Building with JSON imports (inlining)
- Environment-specific JSON loading
- JSON schema validation
- Handling large JSON files

### Key Pattern

```javascript
import config from './config.json';
console.log(config.apiUrl);
```

---

## Part 9: Edge Cases

**File**: [bun-advanced-features-part9-edge-cases.md](./bun-advanced-features-part9-edge-cases.md)

### Contents

- **Monorepo/Workspaces Edge Cases**
  - Workspace packages being bundled instead of linked
  - Using `external` for workspace packages
  - Pattern-based external matching

- **Dynamic Imports Edge Cases**
  - Dynamic imports not creating separate chunks
  - Enabling `splitting` and ESM format
  - Chunk naming patterns (`[name]`, `[hash]`, `[dir]`, `[ext]`)

- **Binary/Native Module Edge Cases**
  - Native modules causing build errors
  - Marking all native modules as external
  - Dynamic detection of native modules

- **JSON Import Edge Cases**
  - Default behavior (JSON inlined)
  - Custom loader for JSON-as-string
  - Conditional JSON handling

---

## Part 10: Troubleshooting

**File**: [bun-advanced-features-part10-troubleshooting.md](./bun-advanced-features-part10-troubleshooting.md)

### Contents

- **Code Splitting Issues**: Chunks not created, duplicated code, too many chunks
- **Tree Shaking Issues**: Dead code not removed, feature flags not working
- **Drop Console/Debugger Issues**: Statements still in output
- **Banner/Footer Issues**: Comments removed by minifier
- **Standalone Executable Issues**: Not running, missing dependencies, too large
- **Monorepo/Workspace Issues**: Dependencies not found, circular dependencies
- **Dynamic Import Issues**: Runtime failures, chunks not loading
- **Native Module Issues**: Not found, platform mismatch, version incompatibility
- **JSON Import Issues**: TypeScript errors, bundle size
- **General Build Issues**: Hangs, out of memory, source maps

---

## Common Build Patterns

### Production Build

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  minify: true,
  splitting: true,
  format: 'esm',
  drop: ['console', 'debugger'],
  sourcemap: 'external',
  define: {
    'process.env.NODE_ENV': '"production"'
  }
});
```

### Library Build (Multiple Formats)

```javascript
const formats = ['esm', 'cjs', 'iife'];

for (const format of formats) {
  await Bun.build({
    entrypoints: ['src/index.js'],
    outfile: `dist/mylib.${format}.js`,
    format,
    globalName: format === 'iife' ? 'MyLib' : undefined,
    minify: true
  });
}
```

### Monorepo Build

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  external: ['@myorg/*'],  // External all workspace packages
  target: 'node'
});
```

---

## See Also

- [Bun Documentation](https://bun.sh/docs)
- [Bun Build API](https://bun.sh/docs/bundler)
- [Bun CLI Reference](https://bun.sh/docs/cli/build)
