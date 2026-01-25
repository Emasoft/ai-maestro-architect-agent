# Bun Troubleshooting: Sourcemaps (Part 6)

> **Navigation**: [Index](bun-troubleshooting.md) | [Part 5: TypeScript & CSS](bun-troubleshooting-part5-typescript-css.md) | [Part 7: Validation](bun-troubleshooting-part7-validation.md)

This section covers sourcemap configuration and debugging issues.

---

## 11. Sourcemap Issues

### Problem Description

After building your code with Bun, debugging in the browser or Node.js is difficult because:

- Error stack traces show minified code locations
- Breakpoints don't match the source code
- Developer tools show bundled code instead of original files
- Source maps are missing or incorrectly configured

### Root Cause

Sourcemaps are special files that map the compiled/minified code back to the original source code. Without proper sourcemap configuration:

- Debuggers cannot find the original source files
- Error messages reference bundled code, not source code
- Development experience is degraded

Bun supports multiple sourcemap formats, but they must be configured correctly.

### Solution

Configure Bun to generate sourcemaps with the correct format and paths.

**Step 1**: Add sourcemap configuration to your build:

```javascript
// build.js
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  sourcemap: 'linked',  // Generate linked sourcemaps
});
```

**Sourcemap options**:
- `'external'` - Generates separate `.js.map` files
- `'inline'` - Embeds sourcemap in the JavaScript file as base64
- `'linked'` - Generates separate `.js.map` files with `//# sourceMappingURL=` comment
- `'none'` - No sourcemaps

**Step 2**: Configure publicPath for browser builds:

```javascript
// build.js
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  sourcemap: 'linked',
  publicPath: '/static/',  // URL path where files will be served
});
```

This generates sourcemap URLs like:
```javascript
//# sourceMappingURL=/static/index.js.map
```

### Sourcemap Formats Explained

**External Sourcemaps** (`'external'`):
```javascript
await Bun.build({
  sourcemap: 'external',
});
```

Output:
- `dist/index.js` - No sourcemap reference
- `dist/index.js.map` - Sourcemap file

Use when:
- You want to manually reference sourcemaps
- Publishing to npm (don't include sourcemaps in bundle)

**Inline Sourcemaps** (`'inline'`):
```javascript
await Bun.build({
  sourcemap: 'inline',
});
```

Output:
- `dist/index.js` - Contains base64-encoded sourcemap

Example:
```javascript
// ... your code ...
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9...
```

Use when:
- Single-file distribution
- Avoiding separate file management
- Size is not a concern

**Linked Sourcemaps** (`'linked'`):
```javascript
await Bun.build({
  sourcemap: 'linked',
});
```

Output:
- `dist/index.js` - Contains sourcemap reference
- `dist/index.js.map` - Sourcemap file

Example:
```javascript
// ... your code ...
//# sourceMappingURL=index.js.map
```

Use when:
- Development builds
- Browser debugging
- Production with sourcemap support

### Complete Example

**build.js**:
```javascript
const isDevelopment = process.env.NODE_ENV !== 'production';

await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'esm',
  minify: !isDevelopment,
  sourcemap: isDevelopment ? 'linked' : 'external',
  publicPath: '/assets/',
  naming: {
    entry: '[name].[hash].js',
    chunk: '[name]-[hash].js',
    asset: '[name].[ext]',
  },
});
```

**package.json**:
```json
{
  "scripts": {
    "build": "NODE_ENV=production bun run build.js",
    "build:dev": "NODE_ENV=development bun run build.js",
    "dev": "NODE_ENV=development bun run build.js --watch"
  }
}
```

### Verifying Sourcemaps

**Step 1**: Check that sourcemap files are generated:

```bash
ls -la dist/
# Should show .js and .js.map files
```

**Step 2**: Verify sourcemap content:

```bash
cat dist/index.js.map
```

Should contain:
```json
{
  "version": 3,
  "sources": ["../src/index.ts"],
  "sourcesContent": ["..."],
  "mappings": "...",
  "names": [...]
}
```

**Step 3**: Test in browser DevTools:

1. Open the built page in browser
2. Open DevTools → Sources panel
3. You should see your original TypeScript files
4. Set breakpoints in the original source
5. Verify stack traces reference source files

### Sourcemaps for Node.js

For Node.js targets, enable source map support:

```javascript
// build.js
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'node',
  sourcemap: 'linked',
});
```

**Run with source map support**:

```bash
node --enable-source-maps dist/index.js
```

Or add to the built file:

```javascript
// dist/index.js
import { install } from 'source-map-support';
install();

// ... rest of your code
```

### Sourcemaps in Production

**Best practices**:

1. **Don't inline sourcemaps** in production (increases bundle size)
2. **Use external sourcemaps** that you can optionally serve
3. **Upload sourcemaps** to error tracking services (Sentry, Rollbar)
4. **Don't expose sourcemaps** publicly if they contain sensitive code

**Example: Conditional sourcemaps**:

```javascript
// build.js
const isProduction = process.env.NODE_ENV === 'production';

await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  minify: isProduction,
  sourcemap: isProduction ? 'external' : 'linked',
});

// Upload sourcemaps to error tracking service
if (isProduction) {
  const { exec } = require('child_process');
  exec('sentry-cli sourcemaps upload --org my-org --project my-project ./dist');
}
```

### When This Issue Occurs

- Debugging minified production code
- Error stack traces showing wrong locations
- Breakpoints not working in DevTools
- Cannot see original source in debugger
- Publishing packages for debugging

---

> **Next**: [Part 7: Validation](bun-troubleshooting-part7-validation.md)
