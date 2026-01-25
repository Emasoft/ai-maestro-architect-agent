# Bun Advanced Features: Troubleshooting

> **Part 10 of 10** | See [bun-advanced-features.md](./bun-advanced-features.md) for the complete index.

---

## Troubleshooting

### Code Splitting Issues

**Problem: Chunks not being created**

Check that:
- `splitting: true` is enabled in build config
- You're using dynamic imports (`import()`)
- Target format supports splitting (ESM)

```javascript
// Correct
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  format: 'esm',  // Splitting requires ESM
  splitting: true
});
```

**Problem: Shared code duplicated across chunks**

Solution: Ensure `splitting: true` is enabled. Bun automatically extracts shared code.

**Problem: Too many small chunks**

Solution: Use `manualChunks` to group related modules:

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  splitting: true,
  manualChunks: (id) => {
    if (id.includes('node_modules')) return 'vendor';
    if (id.includes('/utils/')) return 'utils';
  }
});
```

### Tree Shaking Issues

**Problem: Dead code not being removed**

Check that:
- Code uses ES modules (`import`/`export`), not CommonJS
- `minify: true` is enabled
- Side effects are properly marked in `package.json`

```json
{
  "sideEffects": false
}
```

**Problem: Feature flag code not removed**

Ensure `define` replaces values at compile time:

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  minify: true,
  define: {
    ENABLE_FEATURE: 'false'  // Must be a string
  }
});
```

**Problem: External dependencies not tree-shaken**

Solution: External dependencies are not tree-shaken. Only bundled code is optimized.

### Drop Console/Debugger Issues

**Problem: Console statements still in output**

Check that `drop: ['console']` is specified:

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  drop: ['console', 'debugger']
});
```

**Problem: Need to keep error logs**

Use a custom logger as shown in [Part 2: Build Optimization](./bun-advanced-features-part2-build-optimization.md).

### Banner/Footer Issues

**Problem: Banner comments removed by minifier**

Use `/*!` instead of `/*` to preserve comments:

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  banner: '/*! This will be preserved */',
  minify: true
});
```

**Problem: Banner breaks code**

Ensure banner is valid JavaScript/comments and ends with newline.

### Standalone Executable Issues

**Problem: Executable doesn't run**

Check:
- File has execute permissions: `chmod +x myapp`
- Shebang is correct: `#!/usr/bin/env bun`
- Built for correct platform

**Problem: Dependencies missing**

Ensure all dependencies are installed before building:

```bash
bun install
bun build src/index.js --compile --outfile=myapp
```

**Problem: Executable too large**

Minimize dependencies and enable optimization:

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  compile: true,
  minify: true,
  drop: ['console', 'debugger']
});
```

### Monorepo/Workspace Issues

**Problem: Workspace dependency not found**

Check:
- `workspaces` field in root `package.json`
- Dependency uses `workspace:*` protocol
- Run `bun install` from root

**Problem: Circular dependencies**

Solution: Refactor to remove circular imports or use dynamic imports to break cycles.

**Problem: Wrong version installed**

Clear lockfile and reinstall:

```bash
rm bun.lockb
bun install
```

### Dynamic Import Issues

**Problem: Dynamic import fails at runtime**

Check:
- Path is correct (relative to importing file)
- File exists at that path
- Format is ESM

**Problem: Chunks not loading in browser**

Ensure:
- Web server serves all chunk files
- Paths in chunks are correct
- CORS is configured if loading from different origin

### Native Module Issues

**Problem: Native module not found**

Mark as external in build:

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  external: ['sharp', 'better-sqlite3']
});
```

**Problem: Platform mismatch**

Rebuild on target platform:

```bash
bun install --force
```

**Problem: Version incompatibility**

Use exact versions in `package.json`:

```json
{
  "dependencies": {
    "sharp": "0.33.0"
  }
}
```

### JSON Import Issues

**Problem: JSON import not working in TypeScript**

Enable in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "resolveJsonModule": true
  }
}
```

**Problem: JSON becomes huge in bundle**

For large JSON, load dynamically at runtime:

```javascript
// Instead of
import data from './large.json';

// Use
const data = await fetch('./large.json').then(r => r.json());
```

### General Build Issues

**Problem: Build hangs indefinitely**

Try:
- Smaller entrypoints
- Disable `splitting` temporarily
- Check for circular dependencies
- Update Bun: `bun upgrade`

**Problem: Out of memory**

Increase Node memory:

```bash
NODE_OPTIONS="--max-old-space-size=8192" bun build src/index.js
```

**Problem: Source maps not generated**

Specify sourcemap option:

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  sourcemap: 'external'  // or 'inline'
});
```

---

## Summary

This document series covered advanced Bun features essential for production-ready applications:

1. **[Code Splitting and Tree Shaking](./bun-advanced-features-part1-code-splitting-treeshaking.md)**: Automatically split code into chunks and remove unused code
2. **[Build Optimization](./bun-advanced-features-part2-build-optimization.md)**: Drop console/debugger and inject banners/footers
3. **[Standalone Executables](./bun-advanced-features-part3-standalone-executables.md)**: Create single-file binaries for easy distribution
4. **[CDN and Browser Usage](./bun-advanced-features-part4-cdn-browser.md)**: Build for browsers and CDN delivery
5. **[Monorepo and Workspaces](./bun-advanced-features-part5-monorepo-workspaces.md)**: Manage multiple packages in one repository
6. **[Dynamic Imports](./bun-advanced-features-part6-dynamic-imports.md)**: Load code on-demand for better performance
7. **[Binary and Native Modules](./bun-advanced-features-part7-native-modules.md)**: Use native code for performance-critical operations
8. **[JSON Imports](./bun-advanced-features-part8-json-imports.md)**: Import JSON files directly as modules
9. **[Edge Cases](./bun-advanced-features-part9-edge-cases.md)**: Handle workspaces, dynamic imports, native modules
10. **[Troubleshooting](./bun-advanced-features-part10-troubleshooting.md)**: Diagnose and fix common build issues

Each feature includes practical examples and troubleshooting guidance to help you implement them effectively in your projects.

---

## Cross-References

- **Previous**: [Part 9: Edge Cases](./bun-advanced-features-part9-edge-cases.md)
- **Index**: [Bun Advanced Features](./bun-advanced-features.md) - Complete feature index
