# Bun Advanced Features Part 1: Build Optimization

## Table of Contents
1. [Code Splitting](#code-splitting)
   - 1.1 [What is Code Splitting?](#what-is-code-splitting)
   - 1.2 [Why Use Code Splitting?](#why-use-code-splitting)
   - 1.3 [How Bun Handles Code Splitting](#how-bun-handles-code-splitting)
   - 1.4 [Basic Code Splitting Example](#basic-code-splitting-example)
   - 1.5 [Code Splitting with Named Chunks](#code-splitting-with-named-chunks)
   - 1.6 [Manual Chunk Configuration](#manual-chunk-configuration)
   - 1.7 [Code Splitting Best Practices](#code-splitting-best-practices)
2. [Tree Shaking with Feature Flags](#tree-shaking-with-feature-flags)
   - 2.1 [What is Tree Shaking?](#what-is-tree-shaking)
   - 2.2 [What are Feature Flags?](#what-are-feature-flags)
   - 2.3 [How Bun Implements Tree Shaking](#how-bun-implements-tree-shaking)
   - 2.4 [Basic Tree Shaking Example](#basic-tree-shaking-example)
   - 2.5 [Feature Flags with define](#feature-flags-with-define)
   - 2.6 [Environment-Based Feature Flags](#environment-based-feature-flags)
   - 2.7 [Side Effects and Tree Shaking](#side-effects-and-tree-shaking)
   - 2.8 [Tree Shaking Best Practices](#tree-shaking-best-practices)

---

## Code Splitting

### What is Code Splitting?

Code splitting is a technique that divides your application code into multiple smaller files (called "chunks") that can be loaded on-demand or in parallel. This reduces the initial bundle size and improves application load time.

### Why Use Code Splitting?

- **Reduced Initial Load Time**: Users only download the code they need for the current page or feature
- **Better Caching**: Changes to one chunk don't invalidate the cache of other chunks
- **Parallel Loading**: Multiple chunks can be loaded simultaneously
- **On-Demand Loading**: Code for features can be loaded only when the user needs them

### How Bun Handles Code Splitting

Bun automatically performs code splitting when you use the `--splitting` flag with the build command. Bun analyzes your import graph and creates separate chunks for shared dependencies.

### Basic Code Splitting Example

**Source Files:**

```javascript
// src/index.js
import('./feature-a.js').then(module => {
  module.initFeatureA();
});

import('./feature-b.js').then(module => {
  module.initFeatureB();
});
```

```javascript
// src/feature-a.js
import { sharedUtil } from './shared.js';

export function initFeatureA() {
  console.log('Feature A initialized');
  sharedUtil();
}
```

```javascript
// src/feature-b.js
import { sharedUtil } from './shared.js';

export function initFeatureB() {
  console.log('Feature B initialized');
  sharedUtil();
}
```

```javascript
// src/shared.js
export function sharedUtil() {
  console.log('Shared utility called');
}
```

**Build Command:**

```bash
bun build src/index.js --outdir=dist --splitting
```

**Result:**

Bun will create:
- `dist/index.js` - Main entry point
- `dist/feature-a-[hash].js` - Feature A chunk
- `dist/feature-b-[hash].js` - Feature B chunk
- `dist/shared-[hash].js` - Shared code chunk (automatically extracted)

### Code Splitting with Named Chunks

You can control chunk names using the `naming.chunk` option:

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  splitting: true,
  naming: {
    chunk: 'chunks/[name]-[hash].[ext]',
    asset: 'assets/[name]-[hash].[ext]'
  }
});
```

**Note on `naming` option:**
- When `naming` is a string, it sets the entry point naming only
- Available tokens: `[name]`, `[ext]`, `[hash]`, `[dir]`
- Always include `[ext]` to preserve file extensions

### Manual Chunk Configuration

For more control over how chunks are created:

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  splitting: true,
  manualChunks: (id) => {
    // Put all vendor code in a separate chunk
    if (id.includes('node_modules')) {
      return 'vendor';
    }
    // Put all utility code in a utils chunk
    if (id.includes('/utils/')) {
      return 'utils';
    }
  }
});
```

### Code Splitting Best Practices

1. **Enable splitting for production builds**: Always use `--splitting` for production
2. **Use dynamic imports strategically**: Only split code that isn't needed immediately
3. **Monitor chunk sizes**: Keep chunks reasonably sized (30-200 KB gzipped)
4. **Preload critical chunks**: Use `<link rel="preload">` for important chunks
5. **Group related code**: Keep related modules together to minimize requests

---

## Tree Shaking with Feature Flags

### What is Tree Shaking?

Tree shaking is a dead code elimination technique that removes unused code from your final bundle. The name comes from the idea of "shaking" a tree to make dead leaves fall off.

### What are Feature Flags?

Feature flags (also called feature toggles) are conditional statements that enable or disable features in your code. When combined with tree shaking, feature flags can completely remove code for disabled features from your production bundle.

### How Bun Implements Tree Shaking

Bun performs tree shaking automatically during the build process. It analyzes which exports are actually imported and used, then removes unused code.

### Basic Tree Shaking Example

**Source Code:**

```javascript
// utils.js
export function usedFunction() {
  return 'This is used';
}

export function unusedFunction() {
  return 'This is never used';
}

export const USED_CONSTANT = 'Used';
export const UNUSED_CONSTANT = 'Unused';
```

```javascript
// index.js
import { usedFunction, USED_CONSTANT } from './utils.js';

console.log(usedFunction());
console.log(USED_CONSTANT);
```

**Build Command:**

```bash
bun build index.js --outfile=dist/bundle.js --minify
```

**Result:**

The final bundle will NOT include `unusedFunction` or `UNUSED_CONSTANT` because they are never imported.

### Feature Flags with define

The `define` option allows you to replace compile-time constants, enabling tree shaking based on feature flags:

**Source Code:**

```javascript
// features.js
export function experimentalFeature() {
  if (ENABLE_EXPERIMENTAL) {
    return 'Experimental feature enabled';
  }
  return 'Experimental feature disabled';
}

export function stableFeature() {
  return 'Stable feature';
}
```

```javascript
// index.js
import { experimentalFeature, stableFeature } from './features.js';

if (ENABLE_EXPERIMENTAL) {
  console.log(experimentalFeature());
}

console.log(stableFeature());
```

**Build Command for Production (experimental disabled):**

```bash
bun build index.js --outfile=dist/bundle.js \
  --define ENABLE_EXPERIMENTAL=false \
  --minify
```

**Build Script Example:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  minify: true,
  define: {
    ENABLE_EXPERIMENTAL: 'false',
    ENABLE_DEBUG_MODE: 'false',
    API_VERSION: '"v2"',
    MAX_RETRIES: '3'
  }
});
```

**Result:**

When `ENABLE_EXPERIMENTAL` is defined as `false`, Bun's tree shaker will:
1. Replace all occurrences of `ENABLE_EXPERIMENTAL` with `false`
2. Detect that the `if (false)` block is dead code
3. Remove the entire experimental feature code from the bundle

### Environment-Based Feature Flags

```javascript
// build.js
const isProduction = process.env.NODE_ENV === 'production';
const enableBetaFeatures = process.env.ENABLE_BETA === 'true';

await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  minify: isProduction,
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
    ENABLE_BETA: enableBetaFeatures.toString(),
    ENABLE_LOGGING: (!isProduction).toString(),
    ENABLE_ANALYTICS: isProduction.toString()
  }
});
```

**Usage in Code:**

```javascript
// analytics.js
export function trackEvent(eventName, data) {
  if (ENABLE_ANALYTICS) {
    // This entire block will be removed if ENABLE_ANALYTICS is false
    sendToAnalytics(eventName, data);
  }
}

export function logDebug(message) {
  if (ENABLE_LOGGING) {
    // This entire block will be removed if ENABLE_LOGGING is false
    console.log('[DEBUG]', message);
  }
}
```

### Side Effects and Tree Shaking

Bun respects the `sideEffects` field in `package.json` to determine which files can be safely tree-shaken:

```json
{
  "name": "my-library",
  "sideEffects": false
}
```

If your library has specific files with side effects:

```json
{
  "name": "my-library",
  "sideEffects": [
    "src/polyfills.js",
    "src/global-styles.css",
    "**/*.css"
  ]
}
```

### Tree Shaking Best Practices

1. **Use ES modules**: Tree shaking only works with ES module syntax (`import`/`export`)
2. **Avoid side effects**: Write pure modules without side effects when possible
3. **Mark side effects explicitly**: Use `sideEffects` field in `package.json`
4. **Use named exports**: Prefer named exports over default exports for better tree shaking
5. **Combine with minification**: Always enable minification to maximize dead code removal
6. **Test with production builds**: Verify that unused code is actually removed

---

**Next:** [Part 2 - Production Build (Drop Console/Debugger + Banner/Footer)](./bun-advanced-features-part2-production-build.md)
