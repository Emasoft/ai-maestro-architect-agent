# Bun Build API - Part 2: Output, Errors and Troubleshooting

## Table of Contents
1. [Output Naming](#output-naming)
   - 1.1 Default Naming Behavior
   - 1.2 Naming Configuration
   - 1.3 Naming Placeholders
   - 1.4 Example: Cache Busting with Hashes
2. [Error Handling](#error-handling)
   - 2.1 The result Object
   - 2.2 Checking Build Success
   - 2.3 Handling Build Errors
   - 2.4 Build Artifact Properties
   - 2.5 Complete Error Handling Pattern
3. [Troubleshooting](#troubleshooting)
   - 3.1 Problem: "Module not found" errors
   - 3.2 Problem: Build succeeds but runtime errors
   - 3.3 Problem: Code splitting not working
   - 3.4 Problem: Minification breaking code
   - 3.5 Problem: Environment variables not replaced
   - 3.6 Problem: Large bundle size
   - 3.7 Problem: Source maps not working
   - 3.8 Problem: Build is slow
4. [Complete Example](#complete-example-production-build-script)
   - 4.1 Production Build Script

**See also**: [Part 1: Core Configuration](bun-build-api-part1-core-configuration.md)

---

## Output Naming

### Default Naming Behavior
Without naming configuration:
```javascript
const result = await Bun.build({
  entrypoints: ["./src/client/app.js"],
  outdir: "./dist",
});

// Output: dist/app.js
```

### Naming Configuration
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  naming: {
    entry: "[dir]/[name].[ext]",        // Entry point files
    chunk: "[name]-[hash].[ext]",       // Code-split chunks
    asset: "assets/[name]-[hash].[ext]", // Non-JS assets
  },
});
```

### Naming Placeholders

**[name]**
- Original filename without extension
- Example: `index.js` → `[name]` = `index`

**[ext]**
- File extension
- Example: `index.js` → `[ext]` = `js`

**[hash]**
- Content-based hash for cache busting
- Example: `[hash]` = `a1b2c3d4`

**[dir]**
- Relative directory path from entry point
- Example: `src/client/app.js` → `[dir]` = `client`

### Example: Cache Busting with Hashes
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  naming: {
    entry: "[name]-[hash].[ext]",
  },
});

// Output: dist/index-a1b2c3d4.js
// Hash changes only when content changes
```

---

## Error Handling

### The result Object
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
});

// result properties:
// - success: boolean
// - outputs: BuildArtifact[]
// - logs: BuildMessage[]
```

### Checking Build Success
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
});

if (!result.success) {
  console.error("Build failed!");
  result.logs.forEach(log => {
    console.error(`[${log.level}] ${log.message}`);
  });
  process.exit(1);
}

console.log("Build succeeded!");
```

### Handling Build Errors
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  minify: true,
});

if (!result.success) {
  // Group errors by type
  const errors = result.logs.filter(log => log.level === "error");
  const warnings = result.logs.filter(log => log.level === "warning");

  console.error(`Build failed with ${errors.length} errors`);

  errors.forEach(error => {
    console.error(`\n${error.message}`);
    if (error.position) {
      console.error(`  at ${error.position.file}:${error.position.line}:${error.position.column}`);
    }
  });

  process.exit(1);
}
```

### Build Artifact Properties
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
});

if (result.success) {
  result.outputs.forEach(output => {
    console.log(`Built: ${output.path}`);
    console.log(`  Size: ${output.size} bytes`);
    console.log(`  Kind: ${output.kind}`); // "entry-point" | "chunk" | "asset"
  });
}
```

### Complete Error Handling Pattern
```javascript
#!/usr/bin/env bun

async function build() {
  try {
    const result = await Bun.build({
      entrypoints: ["./src/index.js"],
      outdir: "./dist",
      minify: true,
      sourcemap: "linked",
    });

    if (!result.success) {
      console.error("Build failed\n");
      result.logs.forEach(log => {
        const prefix = log.level === "error" ? "[ERROR]" : "[WARN]";
        console.error(`${prefix} ${log.message}`);
      });
      process.exit(1);
    }

    console.log("Build succeeded\n");
    result.outputs.forEach(output => {
      const sizeKB = (output.size / 1024).toFixed(2);
      console.log(`  ${output.path} (${sizeKB} KB)`);
    });

  } catch (error) {
    console.error("Unexpected error:", error.message);
    process.exit(1);
  }
}

await build();
```

---

## Troubleshooting

### Problem: "Module not found" errors

**Symptom:**
```
error: Cannot find module "./utils.js"
```

**Cause:**
- Incorrect relative path
- Missing file extension
- Case sensitivity mismatch

**Solution:**
```javascript
// Wrong
import utils from "./utils";

// Correct
import utils from "./utils.js";
```

### Problem: Build succeeds but runtime errors

**Symptom:**
Build completes but browser shows "Uncaught ReferenceError"

**Cause:**
External dependencies not marked as external

**Solution:**
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  external: ["react", "react-dom"], // Add external dependencies
});
```

### Problem: Code splitting not working

**Symptom:**
All code bundled into single file despite `splitting: true`

**Cause:**
- Format is not "esm"
- No dynamic imports in code

**Solution:**
```javascript
// 1. Ensure format is esm
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  splitting: true,
  format: "esm", // Required for splitting
});

// 2. Use dynamic imports
const module = await import("./module.js"); // Not: import module from "./module.js"
```

### Problem: Minification breaking code

**Symptom:**
Code works unminified but fails when minified

**Cause:**
- Code relies on function names
- Using eval() or new Function()
- Dynamic property access with computed strings

**Solution:**
```javascript
// Disable identifier minification
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  minify: {
    whitespace: true,
    identifiers: false, // Disable identifier renaming
    syntax: true,
  },
});
```

### Problem: Environment variables not replaced

**Symptom:**
`process.env.NODE_ENV` appears as-is in bundle

**Cause:**
- Forgot to wrap value in JSON.stringify()
- Typo in variable name

**Solution:**
```javascript
// Wrong
define: {
  "process.env.NODE_ENV": "production", // Missing JSON.stringify
}

// Correct
define: {
  "process.env.NODE_ENV": JSON.stringify("production"),
}
```

### Problem: Large bundle size

**Symptom:**
Output bundle is megabytes in size

**Diagnosis:**
Check what's in the bundle:
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
});

result.outputs.forEach(output => {
  console.log(`${output.path}: ${(output.size / 1024 / 1024).toFixed(2)} MB`);
});
```

**Solutions:**
1. Mark large libraries as external
2. Enable code splitting
3. Use dynamic imports for large features
4. Enable minification

```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  external: ["lodash", "moment"], // Don't bundle large deps
  splitting: true, // Split into chunks
  minify: true, // Compress output
});
```

### Problem: Source maps not working

**Symptom:**
Cannot debug minified code in browser

**Cause:**
- Wrong sourcemap setting
- Source maps not deployed

**Solution:**
```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"],
  outdir: "./dist",
  sourcemap: "linked", // Generates separate .map files
  minify: true,
});

// Ensure both .js and .map files are deployed
```

### Problem: Build is slow

**Symptom:**
Build takes several seconds or longer

**Optimizations:**
1. Reduce entry points
2. Mark node_modules as external
3. Disable source maps in production
4. Use incremental builds (future feature)

```javascript
const result = await Bun.build({
  entrypoints: ["./src/index.js"], // Single entry point
  outdir: "./dist",
  external: ["*"], // Mark all node_modules as external
  sourcemap: "none", // Disable source maps
});
```

---

## Complete Example: Production Build Script

```javascript
#!/usr/bin/env bun

const result = await Bun.build({
  // Entry points
  entrypoints: ["./src/index.js"],

  // Output configuration
  outdir: "./dist",
  naming: {
    entry: "[name]-[hash].[ext]",
    chunk: "chunks/[name]-[hash].[ext]",
    asset: "assets/[name]-[hash].[ext]",
  },

  // Build settings
  target: "browser",
  format: "esm",
  splitting: true,
  minify: {
    whitespace: true,
    identifiers: true,
    syntax: true,
  },
  sourcemap: "linked",

  // Environment configuration
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
    "process.env.API_URL": JSON.stringify(process.env.API_URL || "https://api.example.com"),
    "process.env.VERSION": JSON.stringify(process.env.npm_package_version || "1.0.0"),
  },

  // External dependencies
  external: [
    "react",
    "react-dom",
  ],

  // Optimization
  drop: ["console", "debugger"],

  // Metadata
  banner: `/*! MyApp v${process.env.npm_package_version || "1.0.0"} | MIT License */`,
});

// Error handling
if (!result.success) {
  console.error("Build failed\n");
  result.logs.forEach(log => {
    const prefix = log.level === "error" ? "[ERROR]" : "[WARN]";
    console.error(`${prefix} ${log.message}`);
  });
  process.exit(1);
}

// Success summary
console.log("Build succeeded\n");
console.log("Outputs:");
result.outputs.forEach(output => {
  const sizeKB = (output.size / 1024).toFixed(2);
  const type = output.kind === "entry-point" ? "ENTRY" : "CHUNK";
  console.log(`  [${type}] ${output.path} (${sizeKB} KB)`);
});

const totalSize = result.outputs.reduce((sum, o) => sum + o.size, 0);
console.log(`\nTotal size: ${(totalSize / 1024).toFixed(2)} KB`);
```

---

**End of Bun Build API Reference**
