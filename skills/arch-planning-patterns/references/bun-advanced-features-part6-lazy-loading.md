# Bun Advanced Features Part 6: Lazy Loading

## Table of Contents
1. [What are Dynamic Imports?](#what-are-dynamic-imports)
2. [Basic Dynamic Import Syntax](#basic-dynamic-import-syntax)
3. [Simple Dynamic Import Example](#simple-dynamic-import-example)
4. [Conditional Module Loading](#conditional-module-loading)
5. [Feature-Based Dynamic Loading](#feature-based-dynamic-loading)
6. [Dynamic Import with Error Handling](#dynamic-import-with-error-handling)
7. [Plugin System with Dynamic Imports](#plugin-system-with-dynamic-imports)
8. [Route-Based Code Splitting (Web App)](#route-based-code-splitting-web-app)
9. [Locale/Translation Loading](#localetranslation-loading)
10. [Building with Dynamic Imports](#building-with-dynamic-imports)
11. [Dynamic Import Best Practices](#dynamic-import-best-practices)

---

## What are Dynamic Imports?

Dynamic imports allow you to load JavaScript modules at runtime instead of at compile time. The `import()` function returns a Promise that resolves to the module, enabling:

- **Code splitting**: Load code only when needed
- **Conditional loading**: Load modules based on runtime conditions
- **Lazy loading**: Defer loading of non-critical code
- **Runtime module resolution**: Choose which module to load dynamically

## Basic Dynamic Import Syntax

**Syntax:**

```javascript
const module = await import('./path/to/module.js');
```

**Or with .then():**

```javascript
import('./path/to/module.js').then(module => {
  // Use module
});
```

## Simple Dynamic Import Example

**Source Files:**

```javascript
// heavy-module.js
export function processData(data) {
  console.log('Processing large dataset...');
  // Expensive computation here
  return data.map(x => x * 2);
}

export const CHUNK_SIZE = 1000;
```

```javascript
// index.js
async function handleUserAction() {
  // Only load heavy-module when actually needed
  const { processData, CHUNK_SIZE } = await import('./heavy-module.js');

  const data = [1, 2, 3, 4, 5];
  const result = processData(data);

  console.log('Result:', result);
  console.log('Chunk size:', CHUNK_SIZE);
}

// Module is only loaded when this is called
handleUserAction();
```

## Conditional Module Loading

**Load different modules based on environment:**

```javascript
// config-loader.js
async function loadConfig() {
  const env = process.env.NODE_ENV;

  if (env === 'production') {
    const config = await import('./config.prod.js');
    return config.default;
  } else if (env === 'development') {
    const config = await import('./config.dev.js');
    return config.default;
  } else {
    const config = await import('./config.test.js');
    return config.default;
  }
}

const config = await loadConfig();
console.log('Loaded config:', config);
```

## Feature-Based Dynamic Loading

**Load features on demand:**

```javascript
// feature-loader.js
const features = new Map();

export async function loadFeature(featureName) {
  if (features.has(featureName)) {
    return features.get(featureName);
  }

  let feature;

  switch (featureName) {
    case 'analytics':
      feature = await import('./features/analytics.js');
      break;
    case 'chat':
      feature = await import('./features/chat.js');
      break;
    case 'video':
      feature = await import('./features/video.js');
      break;
    default:
      throw new Error(`Unknown feature: ${featureName}`);
  }

  features.set(featureName, feature);
  return feature;
}
```

**Usage:**

```javascript
// app.js
import { loadFeature } from './feature-loader.js';

async function enableAnalytics() {
  const analytics = await loadFeature('analytics');
  analytics.init({ apiKey: 'xxx' });
  analytics.track('page_view');
}

async function startChat() {
  const chat = await loadFeature('chat');
  chat.connect();
}
```

## Dynamic Import with Error Handling

```javascript
// robust-loader.js
async function loadModule(modulePath) {
  try {
    const module = await import(modulePath);
    return { success: true, module };
  } catch (error) {
    console.error(`Failed to load ${modulePath}:`, error);
    return { success: false, error };
  }
}

// Usage
const result = await loadModule('./optional-feature.js');

if (result.success) {
  result.module.init();
} else {
  console.log('Feature not available, continuing without it');
}
```

## Plugin System with Dynamic Imports

**Plugin loader:**

```javascript
// plugin-loader.js
export class PluginManager {
  constructor() {
    this.plugins = new Map();
  }

  async loadPlugin(pluginName) {
    try {
      const plugin = await import(`./plugins/${pluginName}.js`);

      if (typeof plugin.init !== 'function') {
        throw new Error(`Plugin ${pluginName} missing init function`);
      }

      await plugin.init();
      this.plugins.set(pluginName, plugin);

      console.log(`Plugin ${pluginName} loaded successfully`);
      return plugin;
    } catch (error) {
      console.error(`Failed to load plugin ${pluginName}:`, error);
      throw error;
    }
  }

  async loadAllPlugins(pluginNames) {
    const results = await Promise.allSettled(
      pluginNames.map(name => this.loadPlugin(name))
    );

    const loaded = results.filter(r => r.status === 'fulfilled').length;
    console.log(`Loaded ${loaded}/${pluginNames.length} plugins`);
  }

  getPlugin(pluginName) {
    return this.plugins.get(pluginName);
  }
}
```

**Plugin example:**

```javascript
// plugins/logger.js
export async function init() {
  console.log('Logger plugin initialized');
}

export function log(message) {
  console.log(`[PLUGIN] ${message}`);
}

export const metadata = {
  name: 'logger',
  version: '1.0.0'
};
```

**Usage:**

```javascript
// app.js
import { PluginManager } from './plugin-loader.js';

const manager = new PluginManager();

// Load plugins dynamically
await manager.loadAllPlugins(['logger', 'analytics', 'monitoring']);

// Use a plugin
const logger = manager.getPlugin('logger');
logger.log('Application started');
```

## Route-Based Code Splitting (Web App)

**Router with dynamic imports:**

```javascript
// router.js
const routes = {
  '/': () => import('./pages/home.js'),
  '/about': () => import('./pages/about.js'),
  '/products': () => import('./pages/products.js'),
  '/contact': () => import('./pages/contact.js')
};

export async function navigateTo(path) {
  const loader = routes[path];

  if (!loader) {
    console.error('Route not found:', path);
    return;
  }

  console.log('Loading route:', path);
  const page = await loader();

  // Render the page
  page.render();
}
```

**Page modules:**

```javascript
// pages/home.js
export function render() {
  document.body.innerHTML = '<h1>Home Page</h1>';
}
```

```javascript
// pages/products.js
export function render() {
  document.body.innerHTML = '<h1>Products Page</h1>';
}
```

**Usage:**

```javascript
// app.js
import { navigateTo } from './router.js';

// Only loads the home page initially
await navigateTo('/');

// Loads products page when needed
await navigateTo('/products');
```

## Locale/Translation Loading

**Dynamic locale loading:**

```javascript
// i18n.js
let currentLocale = 'en';
let translations = null;

export async function setLocale(locale) {
  const module = await import(`./locales/${locale}.js`);
  translations = module.default;
  currentLocale = locale;
  console.log(`Locale set to: ${locale}`);
}

export function t(key) {
  return translations?.[key] || key;
}
```

**Locale files:**

```javascript
// locales/en.js
export default {
  welcome: 'Welcome',
  goodbye: 'Goodbye',
  greeting: 'Hello, {name}!'
};
```

```javascript
// locales/es.js
export default {
  welcome: 'Bienvenido',
  goodbye: 'Adios',
  greeting: 'Hola, {name}!'
};
```

**Usage:**

```javascript
// app.js
import { setLocale, t } from './i18n.js';

// Load English (default)
await setLocale('en');
console.log(t('welcome')); // "Welcome"

// Switch to Spanish
await setLocale('es');
console.log(t('welcome')); // "Bienvenido"
```

## Building with Dynamic Imports

**Build configuration:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  splitting: true,  // Enable code splitting for dynamic imports
  format: 'esm',
  naming: {
    chunk: 'chunks/[name]-[hash].[ext]',
    entry: '[dir]/[name].[ext]',
    asset: 'assets/[name]-[hash].[ext]'
  }
});
```

**Result:**

Dynamic imports automatically create separate chunks:

```
dist/
├── index.js                    # Main entry
├── heavy-module-abc123.js      # Dynamically imported chunk
├── analytics-def456.js         # Another chunk
└── chat-ghi789.js              # Another chunk
```

## Dynamic Import Best Practices

1. **Use for large dependencies**: Only load heavy libraries when needed
2. **Error handling**: Always handle import failures gracefully
3. **Loading states**: Show loading indicators while imports resolve
4. **Preload critical chunks**: Use `<link rel="preload">` for known-needed chunks
5. **Cache loaded modules**: Store loaded modules to avoid re-importing
6. **Combine with code splitting**: Enable `splitting: true` in Bun build
7. **Avoid overuse**: Don't split every tiny module
8. **Test import paths**: Ensure paths work in both development and production
9. **Document async boundaries**: Make it clear where dynamic loading occurs
10. **Monitor chunk sizes**: Keep chunks reasonably sized

---

**Previous:** [Part 5 - Monorepos (Monorepo and Workspaces)](./bun-advanced-features-part5-monorepos.md)

**Next:** [Part 7 - Native Modules (Binary and Native Modules)](./bun-advanced-features-part7-native-modules.md)
