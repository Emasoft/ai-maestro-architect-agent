# Bun Advanced Features Part 9: Edge Cases and Troubleshooting

## Overview

This document covers edge cases and troubleshooting for Bun's advanced features. Due to the comprehensive nature of this content, it has been split into focused parts.

---

## Table of Contents

### Part 1: Edge Cases
**File:** [bun-advanced-features-part9-troubleshooting-part1-edge-cases.md](./bun-advanced-features-part9-troubleshooting-part1-edge-cases.md)

- 1.1 Monorepo / Workspaces
  - Problem: Workspace packages being bundled instead of linked
  - Solution: Mark workspace packages as external
  - Pattern-based external matching for large monorepos
  - Key considerations for workspace external configuration
- 1.2 Dynamic Imports
  - Problem: Dynamic imports not creating separate chunks
  - Solution: Enable splitting and configure chunk naming
  - Chunk naming patterns ([name], [hash], [dir], [ext])
  - Custom chunk naming with subdirectory organization
  - Important notes on ESM format requirement
- 1.3 Binary / Native Modules
  - Problem: Native modules causing build errors
  - Solution: Mark all native modules as external
  - Common native modules table (better-sqlite3, sharp, canvas, etc.)
  - Dynamic detection of native modules from package.json
  - Key points on binary distribution
- 1.4 JSON Imports
  - Default behavior: JSON is inlined
  - Custom loader for JSON-as-string
  - When to use each approach (table comparison)

---

### Part 2: Troubleshooting
**File:** [bun-advanced-features-part9-troubleshooting-part2-troubleshooting.md](./bun-advanced-features-part9-troubleshooting-part2-troubleshooting.md)

- 2.1 Code Splitting Issues
  - Problem: Chunks not being created
  - Problem: Shared code duplicated across chunks
  - Problem: Too many small chunks (manualChunks solution)
- 2.2 Tree Shaking Issues
  - Problem: Dead code not being removed
  - Problem: Feature flag code not removed
  - Problem: External dependencies not tree-shaken
- 2.3 Drop Console/Debugger Issues
  - Problem: Console statements still in output
  - Problem: Need to keep error logs
- 2.4 Banner/Footer Issues
  - Problem: Banner comments removed by minifier
  - Problem: Banner breaks code
- 2.5 Standalone Executable Issues
  - Problem: Executable doesn't run
  - Problem: Dependencies missing
  - Problem: Executable too large
- 2.6 Monorepo/Workspace Issues
  - Problem: Workspace dependency not found
  - Problem: Circular dependencies
  - Problem: Wrong version installed
- 2.7 Dynamic Import Issues
  - Problem: Dynamic import fails at runtime
  - Problem: Chunks not loading in browser
- 2.8 Native Module Issues
  - Problem: Native module not found
  - Problem: Platform mismatch
  - Problem: Version incompatibility
- 2.9 JSON Import Issues
  - Problem: JSON import not working in TypeScript
  - Problem: JSON becomes huge in bundle
- 2.10 General Build Issues
  - Problem: Build hangs indefinitely
  - Problem: Out of memory
  - Problem: Source maps not generated

---

## Summary

This document series covered advanced Bun features essential for production-ready applications:

1. **Code Splitting**: Automatically split code into chunks for better performance
2. **Tree Shaking**: Remove unused code with feature flags and `define`
3. **Drop Console/Debugger**: Clean production builds by removing debug code
4. **Banner/Footer**: Inject copyright, licenses, and custom code
5. **Standalone Executables**: Create single-file binaries for easy distribution
6. **CDN/Browser Usage**: Build for browsers and CDN delivery
7. **Monorepo/Workspaces**: Manage multiple packages in one repository
8. **Dynamic Imports**: Load code on-demand for better performance
9. **Binary/Native Modules**: Use native code for performance-critical operations
10. **JSON Imports**: Import JSON files directly as modules

Each feature includes practical examples and troubleshooting guidance to help you implement them effectively in your projects.

---

**Previous:** [Part 8 - Data Imports (JSON Imports)](./bun-advanced-features-part8-json-imports.md)

**Index:** [Bun Advanced Features](./bun-advanced-features.md)
