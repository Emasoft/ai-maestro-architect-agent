# Bun Advanced Features Part 9.2: Troubleshooting

## Table of Contents
- 2.1 [Code Splitting Issues](#code-splitting-issues)
- 2.2 [Tree Shaking Issues](#tree-shaking-issues)
- 2.3 [Drop Console/Debugger Issues](#drop-consoledebugger-issues)
- 2.4 [Banner/Footer Issues](#bannerfooter-issues)
- 2.5 [Standalone Executable Issues](#standalone-executable-issues)
- 2.6 [Monorepo/Workspace Issues](#monorepoworkspace-issues)
- 2.7 [Dynamic Import Issues](#dynamic-import-issues)
- 2.8 [Native Module Issues](#native-module-issues)
- 2.9 [JSON Import Issues](#json-import-issues)
- 2.10 [General Build Issues](#general-build-issues)

---

## Code Splitting Issues

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

---

## Tree Shaking Issues

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

---

## Drop Console/Debugger Issues

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

Use a custom logger as shown in Part 2 (Production Build).

---

## Banner/Footer Issues

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

---

## Standalone Executable Issues

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

---

## Monorepo/Workspace Issues

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

---

## Dynamic Import Issues

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

---

## Native Module Issues

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

---

## JSON Import Issues

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

---

## General Build Issues

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

**Previous:** [Part 9.1 - Edge Cases](./bun-advanced-features-part9-troubleshooting-part1-edge-cases.md)

**Index:** [Part 9 - Edge Cases and Troubleshooting](./bun-advanced-features-part9-troubleshooting.md)
