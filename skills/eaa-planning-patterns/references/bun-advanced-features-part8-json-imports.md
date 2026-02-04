# Bun Advanced Features: JSON Imports

> **Part 8 of 10** | See [bun-advanced-features.md](./bun-advanced-features.md) for the complete index.

---

## Table of Contents

- [JSON Imports](#json-imports)
  - [What are JSON Imports?](#what-are-json-imports)
  - [Basic JSON Import](#basic-json-import)
  - [JSON Import with Assert Attribute](#json-import-with-assert-attribute)
  - [Dynamic JSON Import](#dynamic-json-import)
  - [Importing Data Files](#importing-data-files)
  - [Package.json Import](#packagejson-import)
  - [Translation Files](#translation-files)
  - [TypeScript with JSON Imports](#typescript-with-json-imports)
  - [Building with JSON Imports](#building-with-json-imports)
  - [Environment-Specific JSON Loading](#environment-specific-json-loading)
  - [JSON Schema Validation](#json-schema-validation)
  - [Large JSON Files](#large-json-files)
  - [JSON Import Best Practices](#json-import-best-practices)
- [Cross-References](#cross-references)

---

## JSON Imports

### What are JSON Imports?

JSON imports allow you to directly import JSON files as JavaScript modules. This is useful for:

- **Configuration files**: Load settings from JSON
- **Static data**: Import datasets, translations, etc.
- **Type safety**: Get autocomplete and type checking (with TypeScript)
- **Build-time optimization**: JSON is parsed at build time, not runtime

### Basic JSON Import

**JSON file (config.json):**

```json
{
  "apiUrl": "https://api.example.com",
  "timeout": 5000,
  "retries": 3,
  "features": {
    "analytics": true,
    "chat": false
  }
}
```

**JavaScript file:**

```javascript
// Using import statement
import config from './config.json';

console.log('API URL:', config.apiUrl);
console.log('Timeout:', config.timeout);
console.log('Features:', config.features);
```

**With named import (TypeScript):**

```typescript
import type { Config } from './config.json';
import config from './config.json';

const apiUrl: string = config.apiUrl;
```

### JSON Import with Assert Attribute

**Modern syntax (import assertions):**

```javascript
import config from './config.json' assert { type: 'json' };

console.log(config);
```

**Or with `with` keyword (newer syntax):**

```javascript
import config from './config.json' with { type: 'json' };

console.log(config);
```

Note: Bun supports both syntaxes, but `assert` is more widely supported.

### Dynamic JSON Import

```javascript
// Load JSON dynamically
const config = await import('./config.json', {
  assert: { type: 'json' }
});

console.log('Loaded config:', config.default);
```

### Importing Data Files

**Dataset (users.json):**

```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com"
  },
  {
    "id": 3,
    "name": "Charlie",
    "email": "charlie@example.com"
  }
]
```

**Usage:**

```javascript
import users from './users.json';

console.log(`Total users: ${users.length}`);

for (const user of users) {
  console.log(`${user.name} (${user.email})`);
}

// Find a user
const alice = users.find(u => u.name === 'Alice');
console.log('Alice:', alice);
```

### Package.json Import

```javascript
import pkg from './package.json';

console.log(`${pkg.name} v${pkg.version}`);
console.log('Description:', pkg.description);
console.log('Author:', pkg.author);
console.log('License:', pkg.license);
```

### Translation Files

**Locales:**

```json
// locales/en.json
{
  "welcome": "Welcome",
  "login": "Log In",
  "logout": "Log Out",
  "settings": "Settings"
}
```

```json
// locales/es.json
{
  "welcome": "Bienvenido",
  "login": "Iniciar Sesion",
  "logout": "Cerrar Sesion",
  "settings": "Configuracion"
}
```

**Loader:**

```javascript
// i18n.js
import en from './locales/en.json';
import es from './locales/es.json';

const translations = { en, es };
let currentLocale = 'en';

export function setLocale(locale) {
  if (translations[locale]) {
    currentLocale = locale;
  }
}

export function t(key) {
  return translations[currentLocale][key] || key;
}
```

**Usage:**

```javascript
import { setLocale, t } from './i18n.js';

console.log(t('welcome'));  // "Welcome"

setLocale('es');
console.log(t('welcome'));  // "Bienvenido"
```

### TypeScript with JSON Imports

**Enable JSON imports in tsconfig.json:**

```json
{
  "compilerOptions": {
    "resolveJsonModule": true,
    "esModuleInterop": true
  }
}
```

**Define JSON structure:**

```typescript
// types.ts
export interface Config {
  apiUrl: string;
  timeout: number;
  retries: number;
  features: {
    analytics: boolean;
    chat: boolean;
  };
}
```

**Use with types:**

```typescript
// app.ts
import type { Config } from './types';
import config from './config.json';

// TypeScript knows the structure of config
const url: string = config.apiUrl;
const timeout: number = config.timeout;

function makeRequest(cfg: Config) {
  console.log(`Making request to ${cfg.apiUrl}`);
}

makeRequest(config);
```

### Building with JSON Imports

**Bun automatically inlines JSON during build:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  minify: true
});
```

**Source:**

```javascript
// src/index.js
import config from './config.json';
console.log(config.apiUrl);
```

**Output (dist/index.js):**

```javascript
// JSON is inlined at build time
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
  features: {
    analytics: true,
    chat: false
  }
};
console.log(config.apiUrl);
```

### Environment-Specific JSON Loading

**Dynamic loading based on environment:**

```javascript
// config-loader.js
const env = process.env.NODE_ENV || 'development';

let config;
if (env === 'production') {
  config = await import('./config.prod.json');
} else if (env === 'staging') {
  config = await import('./config.staging.json');
} else {
  config = await import('./config.dev.json');
}

export default config.default;
```

**Usage:**

```javascript
import config from './config-loader.js';

console.log('Environment:', process.env.NODE_ENV);
console.log('API URL:', config.apiUrl);
```

### JSON Schema Validation

**Validate imported JSON:**

```javascript
import Ajv from 'ajv';
import config from './config.json';

const ajv = new Ajv();

const schema = {
  type: 'object',
  properties: {
    apiUrl: { type: 'string' },
    timeout: { type: 'number' },
    retries: { type: 'number' }
  },
  required: ['apiUrl', 'timeout']
};

const validate = ajv.compile(schema);
const valid = validate(config);

if (!valid) {
  console.error('Config validation failed:', validate.errors);
  process.exit(1);
}

console.log('Config is valid');
```

### Large JSON Files

**For very large JSON files, consider streaming:**

```javascript
// Instead of importing directly
import largeData from './large-data.json';  // Loads entire file into memory

// Use Bun.file for streaming
const file = Bun.file('./large-data.json');
const data = await file.json();  // Still loads into memory, but more flexible

// Or stream line-by-line for NDJSON
const text = await file.text();
const lines = text.split('\n');
for (const line of lines) {
  const item = JSON.parse(line);
  // Process item
}
```

### JSON Import Best Practices

1. **Use for static data**: JSON imports are best for data that doesn't change at runtime
2. **Enable resolveJsonModule**: Always enable in TypeScript config
3. **Keep files small**: Large JSON files increase bundle size
4. **Type your JSON**: Define interfaces/types for imported JSON in TypeScript
5. **Validate at runtime**: Use schema validation for critical config
6. **Use import assertions**: Prefer `assert { type: 'json' }` for clarity
7. **Environment configs**: Use dynamic imports for environment-specific JSON
8. **Don't import secrets**: Never import sensitive data from JSON files in version control
9. **Consider alternatives**: For large datasets, consider fetching at runtime
10. **Freeze imported data**: Use `Object.freeze()` to prevent accidental mutations

**Example with Object.freeze:**

```javascript
import config from './config.json';

const frozenConfig = Object.freeze(config);

// This will throw an error in strict mode
frozenConfig.apiUrl = 'https://hacker.com';  // Error!
```

---

## Cross-References

- **Previous**: [Part 7: Native Modules](./bun-advanced-features-part7-native-modules.md)
- **Next**: [Part 9: Edge Cases](./bun-advanced-features-part9-edge-cases.md)
- **Related**: [Part 6: Dynamic Imports](./bun-advanced-features-part6-dynamic-imports.md) - For dynamic JSON loading
- **Index**: [Bun Advanced Features](./bun-advanced-features.md) - Complete feature index
