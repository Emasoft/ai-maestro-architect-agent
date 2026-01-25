# Bun Troubleshooting: TypeScript & CSS (Part 5)

> **Navigation**: [Index](bun-troubleshooting.md) | [Part 4: Browser Bundling](bun-troubleshooting-part4-browser-bundling.md) | [Part 6: Sourcemaps](bun-troubleshooting-part6-sourcemaps.md)

This section covers TypeScript declaration generation and CSS bundling issues.

---

## 9. TypeScript Declarations

### Problem Description

After building your package with Bun, TypeScript users cannot import your types:

```typescript
import { MyFunction } from 'my-package';
//     ^^^^^^^^^^
// Error: Could not find a declaration file for module 'my-package'
```

Even though your package includes TypeScript source files, the published package lacks `.d.ts` declaration files that TypeScript needs.

### Root Cause

Bun's build tool transpiles TypeScript to JavaScript but does not generate TypeScript declaration files (`.d.ts`). These declaration files are required for:

- TypeScript users to get type checking
- IDE autocomplete and IntelliSense
- Type-safe imports

The TypeScript compiler (`tsc`) is still needed to generate these declaration files.

### Solution

Use the TypeScript compiler to generate declaration files after Bun builds the JavaScript.

**Step 1**: Install TypeScript as a dev dependency:

```bash
bun add -d typescript
```

**Step 2**: Create or update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "emitDeclarationOnly": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

**Key configuration options**:
- `declaration: true` - Generate `.d.ts` files
- `declarationMap: true` - Generate `.d.ts.map` files for debugging
- `emitDeclarationOnly: true` - Only generate declarations, not JavaScript
- `outDir: "./dist"` - Output directory for declaration files
- `rootDir: "./src"` - Source directory

**Step 3**: Update your build script:

```javascript
// build.js
// Step 1: Build JavaScript with Bun
const buildResult = await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'node',
  format: 'esm',
  minify: true,
  sourcemap: 'linked',
});

if (!buildResult.success) {
  console.error('Build failed:', buildResult.logs);
  process.exit(1);
}

console.log('✓ JavaScript built successfully');

// Step 2: Generate TypeScript declarations
const { spawn } = require('child_process');

const tsc = spawn('tsc', [], { stdio: 'inherit' });

tsc.on('close', (code) => {
  if (code !== 0) {
    console.error('TypeScript declaration generation failed');
    process.exit(code);
  }
  console.log('✓ TypeScript declarations generated successfully');
});
```

**Step 4**: Update package.json:

```json
{
  "name": "my-package",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  },
  "files": [
    "dist/**/*.js",
    "dist/**/*.d.ts",
    "dist/**/*.d.ts.map"
  ],
  "scripts": {
    "build": "bun run build.js",
    "prepublishOnly": "bun run build"
  },
  "devDependencies": {
    "typescript": "^5.3.3"
  }
}
```

### Advanced: Multiple Entry Points

For packages with multiple entry points:

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true,
    "emitDeclarationOnly": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

**package.json**:
```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./utils": {
      "types": "./dist/utils/index.d.ts",
      "import": "./dist/utils/index.js"
    },
    "./components": {
      "types": "./dist/components/index.d.ts",
      "import": "./dist/components/index.js"
    }
  },
  "typesVersions": {
    "*": {
      "utils": ["./dist/utils/index.d.ts"],
      "components": ["./dist/components/index.d.ts"]
    }
  }
}
```

**build.js**:
```javascript
await Bun.build({
  entrypoints: [
    './src/index.ts',
    './src/utils/index.ts',
    './src/components/index.ts'
  ],
  outdir: './dist',
  target: 'node',
  format: 'esm',
});

// Generate declarations for all entry points
exec('tsc', (error) => {
  if (error) {
    console.error('Declaration generation failed');
    process.exit(1);
  }
  console.log('✓ All declarations generated');
});
```

### Verification

After building, verify the declarations are correct:

```bash
# Check that .d.ts files exist
ls -R dist/*.d.ts

# Test TypeScript import
echo "import { MyFunction } from './dist/index.js';" > test-import.ts
tsc --noEmit test-import.ts
```

### When This Issue Occurs

- Publishing TypeScript libraries
- Users report missing type definitions
- IDE not showing autocomplete
- TypeScript compilation errors for package imports
- Publishing packages for TypeScript users

---

## 10. CSS Bundling

### Problem Description

When trying to import CSS files in your TypeScript code, you encounter errors:

```typescript
import './styles.css';
// Error: Cannot find module './styles.css'
```

Or CSS is not included in the built bundle, causing styling to be missing in production.

### Root Cause

Bun's bundler needs explicit configuration to handle CSS files. By default:
- Bun doesn't know how to process CSS imports
- CSS files are not included in the output
- TypeScript doesn't recognize CSS as a valid import

### Solution

Configure Bun to handle CSS files using the loader configuration.

**Step 1**: Configure the CSS loader in your build script:

```javascript
// build.js
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  loader: {
    '.css': 'css',  // Tell Bun to process CSS files
  },
});
```

**Step 2**: For TypeScript support, create a CSS module declaration:

```typescript
// src/types/css.d.ts
declare module '*.css' {
  const content: string;
  export default content;
}
```

**Step 3**: Update tsconfig.json to include the declaration:

```json
{
  "compilerOptions": {
    "typeRoots": ["./src/types", "./node_modules/@types"]
  },
  "include": ["src/**/*"]
}
```

### CSS Modules

For CSS Modules support (scoped class names):

**Step 1**: Configure CSS modules loader:

```javascript
// build.js
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  loader: {
    '.module.css': 'css',  // CSS modules
    '.css': 'css',         // Regular CSS
  },
});
```

**Step 2**: Create CSS modules type declaration:

```typescript
// src/types/css-modules.d.ts
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}
```

**Step 3**: Use CSS modules in your code:

```typescript
// src/Component.ts
import styles from './Component.module.css';

export function Component() {
  const element = document.createElement('div');
  element.className = styles.container;
  return element;
}
```

**Component.module.css**:
```css
.container {
  padding: 20px;
  background-color: #f0f0f0;
}

.title {
  font-size: 24px;
  color: #333;
}
```

### Multiple CSS Processing Options

**build.js with advanced CSS configuration**:

```javascript
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'esm',
  loader: {
    '.css': 'css',           // Regular CSS
    '.module.css': 'css',    // CSS Modules
    '.scss': 'css',          // SCSS (requires preprocessor)
    '.less': 'css',          // LESS (requires preprocessor)
  },
  minify: {
    whitespace: true,
    identifiers: false,
    syntax: true,
  },
});
```

### Extracting CSS to Separate Files

By default, CSS is bundled into the JavaScript. To extract it to a separate file:

```javascript
// build.js
const result = await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  loader: {
    '.css': 'css',
  },
  naming: {
    asset: '[name].[ext]',
    entry: '[name].js',
    chunk: '[name]-[hash].js',
  },
});

// CSS is automatically extracted to dist/index.css
console.log('Build outputs:', result.outputs.map(o => o.path));
```

### Complete Example

**Project structure**:
```
src/
  index.ts
  styles.css
  Component.ts
  Component.module.css
  types/
    css.d.ts
    css-modules.d.ts
build.js
package.json
```

**src/index.ts**:
```typescript
import './styles.css';
import { Component } from './Component';

const app = document.getElementById('app');
if (app) {
  app.appendChild(Component());
}
```

**src/styles.css**:
```css
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
```

**src/Component.ts**:
```typescript
import styles from './Component.module.css';

export function Component() {
  const div = document.createElement('div');
  div.className = styles.container;
  div.innerHTML = `<h1 class="${styles.title}">Hello World</h1>`;
  return div;
}
```

**build.js**:
```javascript
const result = await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'esm',
  loader: {
    '.css': 'css',
    '.module.css': 'css',
  },
  minify: true,
  sourcemap: 'linked',
});

if (!result.success) {
  console.error('Build failed');
  process.exit(1);
}

console.log('✓ Build complete');
console.log('Outputs:', result.outputs.map(o => o.path));
```

**package.json**:
```json
{
  "scripts": {
    "build": "bun run build.js",
    "dev": "bun run build.js --watch"
  }
}
```

### When This Issue Occurs

- Importing CSS in TypeScript/JavaScript
- Building for browser with styles
- Using CSS Modules
- Missing styles in production build
- TypeScript errors for CSS imports

---

> **Next**: [Part 6: Sourcemaps](bun-troubleshooting-part6-sourcemaps.md)
