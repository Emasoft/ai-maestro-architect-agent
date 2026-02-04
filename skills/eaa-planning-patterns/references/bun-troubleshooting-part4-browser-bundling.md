# Bun Troubleshooting: Browser Bundling (Part 4)

> **Navigation**: [Index](bun-troubleshooting.md) | [Part 3: Permissions & Tests](bun-troubleshooting-part3-permissions-tests.md) | [Part 5: TypeScript & CSS](bun-troubleshooting-part5-typescript-css.md)

This section covers issues when bundling code for browser environments.

---

## Table of Contents

- [3. Node.js Modules in Browser](#3-nodejs-modules-in-browser)
  - [Problem Description](#problem-description)
  - [Root Cause](#root-cause)
  - [Solution](#solution)
  - [Complete Example](#complete-example)
  - [When This Issue Occurs](#when-this-issue-occurs)
- [4. Global Name Collision](#4-global-name-collision)
  - [Problem Description](#problem-description-1)
  - [Root Cause](#root-cause-1)
  - [Solution](#solution-1)
  - [Naming Conventions](#naming-conventions)
  - [Complete Example](#complete-example-1)
  - [When This Issue Occurs](#when-this-issue-occurs-1)

---

## 3. Node.js Modules in Browser

### Problem Description

When bundling code for browser usage, you encounter errors like:

```
ReferenceError: fs is not defined
Uncaught ReferenceError: path is not defined
```

These errors occur when your bundled JavaScript code tries to use Node.js built-in modules (such as `fs`, `path`, `url`, `crypto`) in a browser environment where these modules do not exist.

### Root Cause

Node.js provides built-in modules that interact with the operating system and file system. These modules are not available in browsers because:

- Browsers run in a sandboxed environment for security
- Browsers cannot access the file system directly
- Node.js APIs are server-side only

When Bun bundles your code for the browser, it may attempt to include these Node.js modules in the bundle. If you don't explicitly tell Bun to exclude them, they will be included, causing runtime errors.

### Solution

Configure Bun to exclude Node.js built-in modules from the browser bundle.

**Step 1**: Add the `external` configuration to your Bun build script:

```javascript
// build.js
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  external: ['fs', 'path', 'url', 'crypto', 'stream', 'buffer'],
});
```

**Step 2**: Identify all Node.js modules your code might reference:

Common Node.js built-in modules to externalize:
- `fs` - File system operations
- `path` - Path manipulation
- `url` - URL parsing
- `crypto` - Cryptographic functions
- `stream` - Stream operations
- `buffer` - Binary data handling
- `process` - Process information
- `os` - Operating system utilities
- `child_process` - Spawn subprocesses
- `http` / `https` - HTTP client/server
- `net` - Network operations
- `zlib` - Compression

**Step 3**: Create a comprehensive external list:

```javascript
// build.js
const nodeModules = [
  'fs', 'fs/promises',
  'path',
  'url',
  'crypto',
  'stream',
  'buffer',
  'process',
  'os',
  'child_process',
  'http', 'https',
  'net',
  'zlib',
  'util',
  'events',
  'assert',
];

await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  external: nodeModules,
  minify: true,
});
```

**Step 4**: For isomorphic code (code that runs in both Node.js and browser), use conditional imports:

```typescript
// src/utils.ts
let fileSystem;

if (typeof window === 'undefined') {
  // Node.js environment
  fileSystem = await import('fs');
} else {
  // Browser environment
  fileSystem = null;
}

export function readFile(path: string) {
  if (!fileSystem) {
    throw new Error('File system operations not available in browser');
  }
  return fileSystem.readFileSync(path, 'utf-8');
}
```

### Complete Example

**build.js**:
```javascript
const nodeModules = [
  'fs', 'path', 'url', 'crypto', 'stream', 'buffer',
  'process', 'os', 'child_process', 'http', 'https',
  'net', 'zlib', 'util', 'events', 'assert',
];

const result = await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'esm',
  external: nodeModules,
  minify: true,
  sourcemap: 'linked',
});

if (!result.success) {
  console.error('Build failed:', result.logs);
  process.exit(1);
}

console.log('Browser bundle created successfully');
```

### When This Issue Occurs

- Building code that targets the browser
- Bundling libraries that work in both Node.js and browser
- Using third-party packages that internally use Node.js APIs
- Creating web applications from Node.js codebases

---

## 4. Global Name Collision

### Problem Description

When building IIFE (Immediately Invoked Function Expression) bundles for browser usage, multiple libraries on the same page may conflict with each other:

```
Error: MyLibrary is already defined
Uncaught TypeError: window.MyLibrary is not a function
```

This happens when two or more bundled libraries use the same global variable name, causing one to overwrite the other.

### Root Cause

IIFE bundles expose their exports to the global scope (the `window` object in browsers) using a specified global name. If two libraries use the same global name, the second one loaded will overwrite the first, breaking functionality.

For example:
```javascript
// Library A
window.MyLibrary = { functionA: ... };

// Library B (loaded later)
window.MyLibrary = { functionB: ... };  // Overwrites Library A!
```

### Solution

Use a unique, namespaced global name for each library.

**Step 1**: Choose a unique global name using a namespace pattern:

```
CompanyName_ProjectName_LibraryName
```

**Step 2**: Configure the `globalName` in your Bun build configuration:

```javascript
// build.js
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'iife',
  globalName: 'MyCompany_MyProject_Utils',
});
```

**Step 3**: Document the global name in your README:

```markdown
## Browser Usage

Include the script in your HTML:

```html
<script src="my-library.js"></script>
<script>
  // Access the library via the global name
  const result = MyCompany_MyProject_Utils.doSomething();
</script>
```
```

### Naming Conventions

**Good Global Names**:
- `Acme_Dashboard_Charts` - Company_Project_Component
- `MyLib_Utils_v2` - Library_Module_Version
- `AuthSDK_Client` - Product_Component

**Bad Global Names**:
- `Utils` - Too generic
- `Library` - Too generic
- `MyLibrary` - Too generic
- `$` - Conflicts with jQuery
- `_` - Conflicts with Lodash

### Complete Example

**build.js**:
```javascript
const packageJson = require('./package.json');

// Generate unique global name from package name
// Example: @mycompany/my-library -> MyCompany_MyLibrary
const globalName = packageJson.name
  .replace('@', '')
  .replace('/', '_')
  .split('-')
  .map(word => word.charAt(0).toUpperCase() + word.slice(1))
  .join('');

await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'iife',
  globalName: globalName,
  minify: true,
});

console.log(`Built IIFE bundle with global name: ${globalName}`);
```

**Usage Documentation**:
```html
<!DOCTYPE html>
<html>
<head>
  <script src="my-library.js"></script>
</head>
<body>
  <script>
    // Library is available at window.MyCompany_MyLibrary
    const instance = new MyCompany_MyLibrary.Client({
      apiKey: 'your-key'
    });

    instance.connect();
  </script>
</body>
</html>
```

### When This Issue Occurs

- Building IIFE bundles for browser usage
- Multiple libraries loaded on the same page
- Legacy applications using global scope
- Libraries targeting older browsers without module support

---

> **Next**: [Part 5: TypeScript & CSS](bun-troubleshooting-part5-typescript-css.md)
