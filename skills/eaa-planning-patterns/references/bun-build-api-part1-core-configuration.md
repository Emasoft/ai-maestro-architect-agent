# Bun Build API - Part 1: Core Configuration

## Table of Contents
1. [Basic Usage](#basic-usage)
   - 1.1 What is Bun.build()?
   - 1.2 Minimum Working Example
   - 1.3 What This Does
2. [Build Options](#build-options)
   - 2.1 Complete Options Reference
   - 2.2 Target Option Details
   - 2.3 Format Option Details
3. [Multiple Entry Points](#multiple-entry-points)
   - 3.1 When to Use Multiple Entry Points
   - 3.2 Example: Multiple Entry Points
   - 3.3 Example: Entry Point Naming Control
4. [Minification Options](#minification-options)
   - 4.1 Basic Minification
   - 4.2 Granular Minification Control
   - 4.3 What Each Minification Option Does
   - 4.4 When NOT to Minify
5. [Code Splitting](#code-splitting)
   - 5.1 What is Code Splitting?
   - 5.2 Enabling Code Splitting
   - 5.3 How Code Splitting Works
   - 5.4 Example: Dynamic Import Pattern
   - 5.5 Code Splitting Requirements
6. [Environment Variables](#environment-variables)
   - 6.1 Inline Environment Variables at Build Time
   - 6.2 What define Does
   - 6.3 Example: Before and After
   - 6.4 Important Rules for define
   - 6.5 Reading from .env Files
7. [External Modules](#external-modules)
   - 7.1 What are External Modules?
   - 7.2 When to Use external
   - 7.3 Example: Excluding React from Bundle
   - 7.4 Example: Library Build with Externals
   - 7.5 Pattern Matching in external

**See also**: [Part 2: Output, Errors and Troubleshooting](bun-build-api-part2-output-errors.md)

---

## Basic Usage

### What is Bun.build()?
The `Bun.build()` function is Bun's built-in JavaScript bundler API. It takes source files and produces optimized output bundles. Unlike external bundlers (webpack, rollup, esbuild), Bun.build() is built directly into the Bun runtime.

### Minimum Working Example
```javascript
#!/usr/bin/env bun
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
});

if (!result.success) {
  console.error("Build failed");
  process.exit(1);
}

console.log("Build succeeded");
```

### What This Does
1. **entrypoints**: Specifies the starting file(s) for the build
2. **outdir**: Specifies where to write the bundled output files
3. **result.success**: Boolean indicating if the build completed without errors
4. **process.exit(1)**: Exits the process with error code 1 on failure

---

## Build Options

### Complete Options Reference

```javascript
const result = await Bun.build({
  // REQUIRED: Entry points for the build
  entrypoints: ["./src/index.js"],

  // REQUIRED: Output directory
  outdir: "./dist",

  // Target runtime environment
  target: "browser", // "browser" | "node" | "bun"

  // Output format
  format: "esm", // "esm" | "cjs" | "iife"

  // Enable/disable minification
  minify: true, // boolean | object

  // Source map generation
  sourcemap: "linked", // "none" | "inline" | "linked" | "external"

  // Enable code splitting
  splitting: true, // boolean

  // External modules (not bundled)
  external: ["react", "react-dom"],

  // Compile-time constants
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
    API_URL: JSON.stringify("https://api.example.com"),
  },

  // Loader configuration for specific extensions
  loader: {
    ".png": "file",
    ".svg": "text",
  },

  // Global name for IIFE bundles
  naming: {
    entry: "[dir]/[name].[ext]",
    chunk: "[name]-[hash].[ext]",
    asset: "[name]-[hash].[ext]",
  },

  // Drop specific syntax
  drop: ["console", "debugger"],

  // Add banner/footer to output
  banner: "/* Copyright 2024 */",
  footer: "/* End of bundle */",

  // Public path for assets
  publicPath: "/assets/",
});
```

### Target Option Details

**target: "browser"**
- Optimizes for browser execution
- Uses browser-compatible APIs
- Does not include Node.js built-ins

**target: "node"**
- Optimizes for Node.js execution
- Uses Node.js APIs
- Handles Node.js built-in modules

**target: "bun"**
- Optimizes for Bun runtime
- Uses Bun-specific APIs
- Best performance when running with Bun

### Format Option Details

**format: "esm"** (ES Modules)
```javascript
// Output uses import/export syntax
import { foo } from "./utils.js";
export { bar };
```

**format: "cjs"** (CommonJS)
```javascript
// Output uses require/module.exports syntax
const { foo } = require("./utils.js");
module.exports = { bar };
```

**format: "iife"** (Immediately Invoked Function Expression)
```javascript
// Output wraps code in a self-executing function
(function() {
  // Your code here
})();
```

---

## Multiple Entry Points

### When to Use Multiple Entry Points
Use multiple entry points when you have:
- Multiple independent pages in a web application
- Multiple CLI commands in a tool
- Library with multiple exports

### Example: Multiple Entry Points
```javascript
const result = await Bun.build({
  entrypoints: [
    "./src/client/app.js",
    "./src/admin/dashboard.js",
    "./src/worker/background.js",
  ],
  outdir: "./dist",
  target: "browser",
  format: "esm",
});

// Results in:
// dist/app.js
// dist/dashboard.js
// dist/background.js
```

### Example: Entry Point Naming Control
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  naming: {
    entry: "[dir]/[name]-[hash].[ext]",
  },
});

// Output: dist/index-a1b2c3d4.js
```

---

## Minification Options

### Basic Minification
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  minify: true, // Enables all minification
});
```

### Granular Minification Control
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  minify: {
    whitespace: true,   // Remove unnecessary whitespace
    identifiers: true,  // Shorten variable names
    syntax: true,       // Optimize syntax (e.g., true -> !0)
  },
});
```

### What Each Minification Option Does

**whitespace: true**
- Removes unnecessary spaces, newlines, and indentation
- Does NOT affect code behavior
- Reduces file size significantly

**identifiers: true**
- Renames local variables to shorter names (a, b, c, etc.)
- Does NOT rename exported symbols or properties
- Can break code that relies on function.name

**syntax: true**
- Transforms code to more compact equivalents
- Examples: `true` → `!0`, `false` → `!1`, `undefined` → `void 0`
- Does NOT change code behavior

### When NOT to Minify
- During development (harder to debug)
- When you need readable stack traces
- When debugging production issues
- For library code where consumers expect readable source

---

## Code Splitting

### What is Code Splitting?
Code splitting breaks your bundle into multiple smaller files. The browser only loads what it needs, improving initial page load time.

### Enabling Code Splitting
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  splitting: true, // Enables automatic code splitting
  format: "esm",   // Required: splitting only works with ESM
});
```

### How Code Splitting Works
When `splitting: true`:
1. Bun analyzes dynamic imports: `import("./module.js")`
2. Creates separate chunks for dynamically imported modules
3. Generates a manifest to load chunks on demand
4. Common code is extracted to shared chunks

### Example: Dynamic Import Pattern
```javascript
// src/index.js
async function loadFeature() {
  const module = await import("./heavy-feature.js");
  module.initialize();
}

document.getElementById("btn").addEventListener("click", loadFeature);
```

Build with splitting:
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  splitting: true,
  format: "esm",
});

// Results in:
// dist/index.js (main bundle)
// dist/heavy-feature-[hash].js (lazy chunk)
```

### Code Splitting Requirements
- `format` MUST be `"esm"` (not `"cjs"` or `"iife"`)
- Use dynamic `import()` syntax (not static imports)
- Browser must support ES modules

---

## Environment Variables

### Inline Environment Variables at Build Time
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
    "process.env.API_URL": JSON.stringify("https://api.example.com"),
    "process.env.VERSION": JSON.stringify("1.0.0"),
  },
});
```

### What define Does
The `define` option performs **compile-time replacement**:
1. Searches for exact matches in your code
2. Replaces them with the provided value
3. Dead code elimination removes unreachable branches

### Example: Before and After

**Before (source code):**
```javascript
if (process.env.NODE_ENV === "development") {
  console.log("Debug mode");
} else {
  console.log("Production mode");
}
```

**After build with define:**
```javascript
if ("production" === "development") {
  console.log("Debug mode");
} else {
  console.log("Production mode");
}
```

**After minification:**
```javascript
console.log("Production mode");
```

### Important Rules for define
1. **Always use JSON.stringify()** for string values
2. Keys are exact matches (case-sensitive)
3. Undefined replacements cause build errors
4. Use for constants only, not dynamic values

### Reading from .env Files
```javascript
import { load } from "bun";

// Load .env file
const env = await load(".env");

const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  define: {
    "process.env.API_KEY": JSON.stringify(env.API_KEY),
    "process.env.DATABASE_URL": JSON.stringify(env.DATABASE_URL),
  },
});
```

---

## External Modules

### What are External Modules?
External modules are dependencies that are NOT bundled into the output. They must be available at runtime.

### When to Use external
- Node.js built-in modules (fs, path, http)
- Large libraries you want to load from CDN
- Peer dependencies in library builds
- Modules that should be provided by the consumer

### Example: Excluding React from Bundle
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  external: ["react", "react-dom"],
  format: "esm",
});
```

**Result:**
```javascript
// dist/index.js will contain:
import React from "react"; // Not bundled, expects external module
import ReactDOM from "react-dom"; // Not bundled

// Your component code (bundled)
```

### Example: Library Build with Externals
```javascript
// Building a library that depends on lodash
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  external: ["lodash"], // Don't bundle lodash
  format: "esm",
  target: "node",
});
```

### Pattern Matching in external
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  external: [
    "react*", // Matches react, react-dom, react-router, etc.
    "@babel/*", // Matches all @babel scoped packages
    "node:*", // Matches all Node.js built-ins with node: prefix
  ],
});
```

---

**Continue to**: [Part 2: Output, Errors and Troubleshooting](bun-build-api-part2-output-errors.md)
