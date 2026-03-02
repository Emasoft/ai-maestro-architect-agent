# Bun Advanced Features: Build Optimization

> **Part 2 of 10** | See [bun-advanced-features.md](./bun-advanced-features.md) for the complete index.

## Table of Contents

- [Drop Console and Debugger Statements](#drop-console-and-debugger-statements)
  - [What Does "Drop" Mean?](#what-does-drop-mean)
  - [Why Drop Console and Debugger?](#why-drop-console-and-debugger)
  - [Dropping Console Statements](#dropping-console-statements)
  - [Dropping Debugger Statements](#dropping-debugger-statements)
  - [Dropping Both Console and Debugger](#dropping-both-console-and-debugger)
  - [Conditional Dropping Based on Environment](#conditional-dropping-based-on-environment)
  - [Custom Logging Alternative](#custom-logging-alternative)
  - [Drop Best Practices](#drop-best-practices)
- [Banner and Footer Injection](#banner-and-footer-injection)
  - [What are Banners and Footers?](#what-are-banners-and-footers)
  - [Banner Injection](#banner-injection)
  - [Footer Injection](#footer-injection)
  - [Banner and Footer Together](#banner-and-footer-together)
  - [Practical Use Cases](#practical-use-cases)
  - [Dynamic Banner/Footer Generation](#dynamic-bannerfooter-generation)
  - [Banner/Footer Best Practices](#bannerfooter-best-practices)
- [Cross-References](#cross-references)

---

## Drop Console and Debugger Statements

### What Does "Drop" Mean?

"Dropping" console and debugger statements means completely removing these statements from your production code. This reduces bundle size and prevents sensitive information from appearing in production logs.

### Why Drop Console and Debugger?

- **Security**: Prevent leaking sensitive data through console logs
- **Performance**: Remove runtime overhead of console calls
- **Bundle Size**: Reduce the size of your production bundle
- **Clean Production Code**: Ensure debugging code doesn't reach users

### Dropping Console Statements

**Source Code:**

```javascript
// app.js
export function processData(data) {
  console.log('Processing data:', data);
  console.debug('Data length:', data.length);
  console.warn('This might be slow for large datasets');

  const result = data.map(item => item * 2);

  console.log('Result:', result);
  return result;
}

export function handleError(error) {
  console.error('Error occurred:', error);
  console.trace('Stack trace');
  throw error;
}
```

**Build Command:**

```bash
bun build app.js --outfile=dist/bundle.js --drop console
```

**Build Script:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/app.js'],
  outdir: 'dist',
  drop: ['console']
});
```

**Result:**

All console statements (`console.log`, `console.debug`, `console.warn`, `console.error`, `console.trace`, etc.) will be completely removed from the output bundle.

### Dropping Debugger Statements

**Source Code:**

```javascript
// debug.js
export function complexCalculation(x, y) {
  debugger; // Pause execution here during development

  const step1 = x * 2;
  debugger; // Check intermediate value

  const step2 = y + 10;
  debugger; // Check another value

  return step1 + step2;
}
```

**Build Command:**

```bash
bun build debug.js --outfile=dist/bundle.js --drop debugger
```

**Build Script:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/debug.js'],
  outdir: 'dist',
  drop: ['debugger']
});
```

**Result:**

All `debugger` statements will be removed from the output bundle.

### Dropping Both Console and Debugger

**Build Command:**

```bash
bun build app.js --outfile=dist/bundle.js --drop console --drop debugger
```

**Build Script:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/app.js'],
  outdir: 'dist',
  drop: ['console', 'debugger']
});
```

### Conditional Dropping Based on Environment

```javascript
// build.js
const isProduction = process.env.NODE_ENV === 'production';

await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  drop: isProduction ? ['console', 'debugger'] : []
});
```

### Custom Logging Alternative

If you want to keep some console statements in production (like errors), you can use a custom logger:

**Source Code:**

```javascript
// logger.js
export const logger = {
  log: (...args) => {
    if (ENABLE_LOGGING) {
      console.log(...args);
    }
  },
  error: (...args) => {
    // Always keep errors in production
    console.error(...args);
  }
};
```

```javascript
// app.js
import { logger } from './logger.js';

export function processData(data) {
  logger.log('Processing data:', data); // Will be tree-shaken if ENABLE_LOGGING is false

  try {
    return data.map(item => item * 2);
  } catch (error) {
    logger.error('Error:', error); // Will remain in production
    throw error;
  }
}
```

**Build Script:**

```javascript
// build.js
const isProduction = process.env.NODE_ENV === 'production';

await Bun.build({
  entrypoints: ['src/app.js'],
  outdir: 'dist',
  define: {
    ENABLE_LOGGING: (!isProduction).toString()
  },
  drop: isProduction ? ['debugger'] : []
});
```

### Drop Best Practices

1. **Always drop in production**: Use `drop: ['console', 'debugger']` for production builds
2. **Keep error logging**: Consider using a custom logger that preserves error logs
3. **Test production builds**: Verify that your app works without console/debugger statements
4. **Document logging strategy**: Make it clear which logs remain in production
5. **Use environment variables**: Configure dropping based on `NODE_ENV`

---

## Banner and Footer Injection

### What are Banners and Footers?

Banners and footers are custom text that Bun can inject at the beginning (banner) or end (footer) of your bundled output files. They are commonly used for:

- Copyright notices
- License headers
- Polyfills
- Environment setup code
- Global variable declarations

### Banner Injection

**Build Script:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  banner: `/*!
 * MyApp v1.0.0
 * Copyright (c) 2024 MyCompany
 * Licensed under MIT
 */
`
});
```

**Result (dist/index.js):**

```javascript
/*!
 * MyApp v1.0.0
 * Copyright (c) 2024 MyCompany
 * Licensed under MIT
 */

// Your bundled code follows...
export function myFunction() {
  // ...
}
```

### Footer Injection

**Build Script:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  footer: `
// Build completed at: ${new Date().toISOString()}
// Build environment: ${process.env.NODE_ENV}
`
});
```

**Result (dist/index.js):**

```javascript
// Your bundled code...
export function myFunction() {
  // ...
}

// Build completed at: 2024-01-01T12:00:00.000Z
// Build environment: production
```

### Banner and Footer Together

**Build Script:**

```javascript
// build.js
const version = require('./package.json').version;
const buildDate = new Date().toISOString();

await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  banner: `/*!
 * MyApp v${version}
 * Built: ${buildDate}
 * Copyright (c) 2024 MyCompany
 * Licensed under MIT License
 */
`,
  footer: `
/*
 * End of MyApp v${version}
 * For documentation visit: https://example.com/docs
 */
`
});
```

### Practical Use Cases

#### 1. License Header

```javascript
// build.js
const fs = require('fs');
const licenseHeader = fs.readFileSync('./LICENSE_HEADER.txt', 'utf-8');

await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  banner: licenseHeader
});
```

**LICENSE_HEADER.txt:**

```
/*!
 * MyLibrary
 *
 * Copyright (c) 2024 MyCompany, Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files...
 */
```

#### 2. Polyfill Injection

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  banner: `
// Polyfill for Array.prototype.at
if (!Array.prototype.at) {
  Array.prototype.at = function(index) {
    if (index < 0) index = this.length + index;
    return this[index];
  };
}
`
});
```

#### 3. Environment Configuration

```javascript
// build.js
const config = {
  API_URL: process.env.API_URL || 'https://api.example.com',
  APP_VERSION: require('./package.json').version,
  BUILD_TIME: new Date().toISOString()
};

await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  banner: `
// Application Configuration
const __APP_CONFIG__ = ${JSON.stringify(config, null, 2)};
`
});
```

#### 4. Source Map Reference

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  sourcemap: 'external',
  footer: '\n//# sourceMappingURL=index.js.map'
});
```

#### 5. UMD Wrapper

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  banner: `
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
  typeof define === 'function' && define.amd ? define(['exports'], factory) :
  (factory((global.MyLibrary = {})));
}(this, (function (exports) {
`,
  footer: `
})));
`
});
```

### Dynamic Banner/Footer Generation

```javascript
// build.js
function generateBanner() {
  const pkg = require('./package.json');
  const year = new Date().getFullYear();

  return `/*!
 * ${pkg.name} v${pkg.version}
 * ${pkg.description}
 *
 * Copyright (c) ${year} ${pkg.author}
 * Licensed under ${pkg.license}
 *
 * Build: ${new Date().toISOString()}
 * Node: ${process.version}
 * Bun: ${Bun.version}
 */
`;
}

await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  banner: generateBanner()
});
```

### Banner/Footer Best Practices

1. **Keep banners concise**: Large banners increase bundle size
2. **Use comments**: Wrap banners in `/*! */` to preserve them during minification
3. **Include version info**: Help users identify which version they're using
4. **Automate generation**: Generate banners from `package.json` and environment
5. **Test the output**: Verify that banners/footers don't break your code
6. **Consider minification**: The `!` in `/*!` preserves comments during minification

---

## Cross-References

- **Previous**: [Part 1: Code Splitting and Tree Shaking](./bun-advanced-features-part1-code-splitting-treeshaking.md)
- **Next**: [Part 3: Standalone Executables](./bun-advanced-features-part3-standalone-executables.md)
- **Related**: [Part 10: Troubleshooting](./bun-advanced-features-part10-troubleshooting.md) - For build issues
- **Index**: [Bun Advanced Features](./bun-advanced-features.md) - Complete feature index
