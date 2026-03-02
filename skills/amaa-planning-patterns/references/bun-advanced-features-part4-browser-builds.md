# Bun Advanced Features Part 4: Browser Builds

## Table of Contents
1. [What is CDN and Browser Usage?](#what-is-cdn-and-browser-usage)
2. [Why Target Browsers and CDNs?](#why-target-browsers-and-cdns)
3. [Creating a Browser-Compatible Bundle](#creating-a-browser-compatible-bundle)
4. [Creating Multiple Module Formats](#creating-multiple-module-formats)
5. [ESM for Modern Browsers](#esm-for-modern-browsers)
6. [CDN-Ready Package Structure](#cdn-ready-package-structure)
7. [Import Maps for ESM](#import-maps-for-esm)
8. [Polyfills and Browser Compatibility](#polyfills-and-browser-compatibility)
9. [Source Maps for Browser Debugging](#source-maps-for-browser-debugging)
10. [CDN and Browser Best Practices](#cdn-and-browser-best-practices)

---

## What is CDN and Browser Usage?

CDN (Content Delivery Network) and browser usage refers to creating JavaScript bundles that can be loaded directly in web browsers via `<script>` tags or from CDN services like jsDelivr, unpkg, or cdnjs.

## Why Target Browsers and CDNs?

- **No Build Step for Users**: Developers can use your library with a simple `<script>` tag
- **Global Distribution**: CDNs provide fast delivery worldwide
- **Version Management**: CDNs host multiple versions of your library
- **Prototyping**: Quick to use for demos and prototypes

## Creating a Browser-Compatible Bundle

**Source Code (src/index.js):**

```javascript
// Library code
export function greet(name) {
  return `Hello, ${name}!`;
}

export function add(a, b) {
  return a + b;
}

export const VERSION = '1.0.0';
```

**Build for Browser (IIFE format):**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  format: 'iife',
  globalName: 'MyLib',
  minify: true,
  naming: {
    entry: '[name].min.js',
    chunk: 'chunks/[name]-[hash].[ext]',
    asset: 'assets/[name]-[hash].[ext]'
  }
});
```

**Build Command:**

```bash
bun run build.js
```

**Result (dist/index.min.js):**

```javascript
var MyLib=function(){"use strict";function greet(name){return`Hello, ${name}!`}function add(a,b){return a+b}const VERSION="1.0.0";return{greet:greet,add:add,VERSION:VERSION}}();
```

**Browser Usage:**

```html
<!DOCTYPE html>
<html>
<head>
  <title>MyLib Demo</title>
</head>
<body>
  <script src="dist/index.min.js"></script>
  <script>
    console.log(MyLib.greet('World')); // "Hello, World!"
    console.log(MyLib.add(2, 3)); // 5
    console.log(MyLib.VERSION); // "1.0.0"
  </script>
</body>
</html>
```

## Creating Multiple Module Formats

**Build Script (build-all.js):**

```javascript
const formats = [
  {
    format: 'iife',
    outfile: 'dist/mylib.iife.js',
    globalName: 'MyLib'
  },
  {
    format: 'esm',
    outfile: 'dist/mylib.esm.js'
  },
  {
    format: 'cjs',
    outfile: 'dist/mylib.cjs.js'
  }
];

for (const config of formats) {
  console.log(`Building ${config.format} format...`);

  await Bun.build({
    entrypoints: ['src/index.js'],
    outfile: config.outfile,
    format: config.format,
    globalName: config.globalName,
    minify: false
  });

  // Also create minified version
  await Bun.build({
    entrypoints: ['src/index.js'],
    outfile: config.outfile.replace('.js', '.min.js'),
    format: config.format,
    globalName: config.globalName,
    minify: true
  });
}

console.log('All formats built successfully');
```

## ESM for Modern Browsers

**Build Script:**

```javascript
// build-esm.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  format: 'esm',
  target: 'browser',
  minify: true,
  splitting: true
});
```

**Browser Usage (Modern):**

```html
<!DOCTYPE html>
<html>
<head>
  <title>ESM Demo</title>
</head>
<body>
  <script type="module">
    import { greet, add } from './dist/index.js';

    console.log(greet('World'));
    console.log(add(2, 3));
  </script>
</body>
</html>
```

## CDN-Ready Package Structure

**package.json Configuration:**

```json
{
  "name": "my-awesome-lib",
  "version": "1.0.0",
  "description": "An awesome library",
  "main": "dist/index.cjs.js",
  "module": "dist/index.esm.js",
  "browser": "dist/index.iife.min.js",
  "unpkg": "dist/index.iife.min.js",
  "jsdelivr": "dist/index.iife.min.js",
  "exports": {
    ".": {
      "import": "./dist/index.esm.js",
      "require": "./dist/index.cjs.js",
      "browser": "./dist/index.iife.min.js"
    }
  },
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "bun run build.js"
  }
}
```

**CDN Usage (unpkg):**

```html
<!-- Latest version -->
<script src="https://unpkg.com/my-awesome-lib"></script>

<!-- Specific version -->
<script src="https://unpkg.com/my-awesome-lib@1.0.0"></script>

<!-- Development (unminified) -->
<script src="https://unpkg.com/my-awesome-lib@1.0.0/dist/index.iife.js"></script>

<!-- Production (minified) -->
<script src="https://unpkg.com/my-awesome-lib@1.0.0/dist/index.iife.min.js"></script>
```

**CDN Usage (jsDelivr):**

```html
<!-- Latest version -->
<script src="https://cdn.jsdelivr.net/npm/my-awesome-lib"></script>

<!-- Specific version -->
<script src="https://cdn.jsdelivr.net/npm/my-awesome-lib@1.0.0"></script>

<!-- ESM version -->
<script type="module">
  import MyLib from 'https://cdn.jsdelivr.net/npm/my-awesome-lib@1.0.0/+esm';
</script>
```

## Import Maps for ESM

```html
<!DOCTYPE html>
<html>
<head>
  <title>Import Maps Demo</title>
  <script type="importmap">
    {
      "imports": {
        "my-awesome-lib": "https://cdn.jsdelivr.net/npm/my-awesome-lib@1.0.0/+esm",
        "another-lib": "https://unpkg.com/another-lib@2.0.0/dist/index.esm.js"
      }
    }
  </script>
</head>
<body>
  <script type="module">
    import { greet } from 'my-awesome-lib';
    import { helper } from 'another-lib';

    console.log(greet('World'));
  </script>
</body>
</html>
```

## Polyfills and Browser Compatibility

**Build with Polyfills:**

```javascript
// build-browser.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outfile: 'dist/mylib.min.js',
  format: 'iife',
  globalName: 'MyLib',
  target: 'browser',
  minify: true,
  banner: `
// Polyfill for Promise.allSettled
if (!Promise.allSettled) {
  Promise.allSettled = function(promises) {
    return Promise.all(
      promises.map(p =>
        Promise.resolve(p)
          .then(value => ({ status: 'fulfilled', value }))
          .catch(reason => ({ status: 'rejected', reason }))
      )
    );
  };
}
`
});
```

## Source Maps for Browser Debugging

**Build with Source Maps:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  format: 'iife',
  globalName: 'MyLib',
  minify: true,
  sourcemap: 'external'
});
```

**Result:**

```
dist/
├── index.js         # Minified code
└── index.js.map     # Source map file
```

**Browser Usage with Source Maps:**

The browser will automatically load the source map when you open DevTools, allowing you to debug the original source code.

## CDN and Browser Best Practices

1. **Provide multiple formats**: IIFE for browsers, ESM for modern usage, CJS for Node
2. **Create minified versions**: Always provide both `.js` and `.min.js` versions
3. **Configure package.json properly**: Use `browser`, `unpkg`, and `jsdelivr` fields
4. **Generate source maps**: Enable debugging with `sourcemap: 'external'`
5. **Version your releases**: Use semantic versioning and tag releases
6. **Test in browsers**: Verify your bundle works in target browsers
7. **Keep it small**: Minimize dependencies and bundle size
8. **Document CDN usage**: Show examples in your README
9. **Use global names wisely**: Choose unique, descriptive global variable names
10. **Consider tree shaking**: Export individual functions for better tree shaking

---

**Previous:** [Part 3 - Standalone Executables](./bun-advanced-features-part3-executables.md)

**Next:** [Part 5 - Monorepos (Monorepo and Workspaces)](./bun-advanced-features-part5-monorepos.md)
