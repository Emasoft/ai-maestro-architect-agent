# Package.json Configuration for Bun

## Table of Contents
1. ESM Configuration
2. Conditional Exports
3. Browser Field
4. Scripts
5. Files Allowlist
6. Engine Requirements

## ESM First
```json
{ "type": "module" }
```

## Conditional Exports
```json
{
  "exports": {
    ".": {
      "import": "./src/index.js",
      "require": "./dist/index.cjs",
      "browser": "./dist/bundle.min.js",
      "default": "./src/index.js"
    }
  }
}
```

## Browser Field (Legacy Bundlers)
```json
{
  "browser": {
    "./src/index.js": "./dist/bundle.min.js"
  }
}
```

## Scripts
```json
{
  "scripts": {
    "build": "bun run build.js",
    "build:dev": "bun run build.js --dev",
    "build:watch": "bun run build.js --watch",
    "test": "bun test",
    "prepublishOnly": "npm run build && npm test"
  }
}
```

## Files Allowlist
```json
{
  "files": ["src/", "dist/", "LICENSE", "README.md"]
}
```

## Engine Requirements
```json
{
  "engines": { "node": ">=24.0.0" }
}
```
