# Bun Advanced Features: Binary and Native Modules

> **Part 7 of 10** | See [bun-advanced-features.md](./bun-advanced-features.md) for the complete index.

---

## Binary and Native Modules

### What are Binary and Native Modules?

Binary and native modules are compiled extensions written in languages like C, C++, or Rust that can be called from JavaScript. They provide:

- **Performance**: Direct access to native code for CPU-intensive operations
- **System Access**: Interface with operating system APIs
- **Legacy Integration**: Use existing native libraries
- **Hardware Control**: Direct hardware access when needed

### How Bun Handles Native Modules

Bun has built-in support for Node.js native modules (`.node` files). Bun uses the same Node-API (N-API) as Node.js, ensuring compatibility with most native modules.

### Using Native Modules with Bun

**Install a native module:**

```bash
bun add sharp  # Image processing (native module)
```

**Usage:**

```javascript
// image-processor.js
import sharp from 'sharp';

async function resizeImage(inputPath, outputPath, width, height) {
  await sharp(inputPath)
    .resize(width, height)
    .toFile(outputPath);

  console.log(`Image resized to ${width}x${height}`);
}

await resizeImage('input.jpg', 'output.jpg', 800, 600);
```

### Common Native Modules

#### 1. Sharp (Image Processing)

```javascript
import sharp from 'sharp';

// Resize and convert format
await sharp('input.png')
  .resize(300, 200)
  .jpeg({ quality: 80 })
  .toFile('output.jpg');

// Get image metadata
const metadata = await sharp('image.jpg').metadata();
console.log('Dimensions:', metadata.width, 'x', metadata.height);
```

#### 2. bcrypt (Password Hashing)

```javascript
import bcrypt from 'bcrypt';

// Hash a password
const saltRounds = 10;
const password = 'mySecretPassword';
const hash = await bcrypt.hash(password, saltRounds);

console.log('Hashed password:', hash);

// Verify password
const isValid = await bcrypt.compare(password, hash);
console.log('Password valid:', isValid);
```

#### 3. SQLite3 (Database)

```javascript
import Database from 'better-sqlite3';

// Create/open database
const db = new Database('mydb.sqlite');

// Create table
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  )
`);

// Insert data
const insert = db.prepare('INSERT INTO users (name, email) VALUES (?, ?)');
insert.run('John Doe', 'john@example.com');

// Query data
const users = db.prepare('SELECT * FROM users').all();
console.log('Users:', users);
```

#### 4. Node-Canvas (Canvas API)

```javascript
import { createCanvas } from 'canvas';

const canvas = createCanvas(400, 300);
const ctx = canvas.getContext('2d');

// Draw a rectangle
ctx.fillStyle = 'blue';
ctx.fillRect(50, 50, 100, 100);

// Draw text
ctx.font = '30px Arial';
ctx.fillStyle = 'white';
ctx.fillText('Hello Canvas!', 60, 100);

// Save to file
const buffer = canvas.toBuffer('image/png');
await Bun.write('output.png', buffer);
```

### Building Native Modules with Bun

**If you have a native module in your dependencies:**

```bash
# Bun automatically handles native module compilation during install
bun install
```

**Rebuild native modules:**

```bash
# Force rebuild of native modules
bun rebuild sharp
```

### Creating a Native Addon (Advanced)

**1. Install node-gyp:**

```bash
bun add -d node-gyp
```

**2. Create binding.gyp:**

```json
{
  "targets": [
    {
      "target_name": "addon",
      "sources": [ "addon.cpp" ],
      "include_dirs": [
        "<!@(node -p \"require('node-addon-api').include\")"
      ],
      "dependencies": [
        "<!(node -p \"require('node-addon-api').gyp\")"
      ],
      "cflags!": [ "-fno-exceptions" ],
      "cflags_cc!": [ "-fno-exceptions" ],
      "defines": [ "NAPI_DISABLE_CPP_EXCEPTIONS" ]
    }
  ]
}
```

**3. Create C++ addon (addon.cpp):**

```cpp
#include <napi.h>

Napi::String Hello(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env();
  return Napi::String::New(env, "Hello from native code!");
}

Napi::Number Add(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env();

  if (info.Length() < 2 || !info[0].IsNumber() || !info[1].IsNumber()) {
    Napi::TypeError::New(env, "Two numbers expected").ThrowAsJavaScriptException();
    return Napi::Number::New(env, 0);
  }

  double arg0 = info[0].As<Napi::Number>().DoubleValue();
  double arg1 = info[1].As<Napi::Number>().DoubleValue();
  double result = arg0 + arg1;

  return Napi::Number::New(env, result);
}

Napi::Object Init(Napi::Env env, Napi::Object exports) {
  exports.Set("hello", Napi::Function::New(env, Hello));
  exports.Set("add", Napi::Function::New(env, Add));
  return exports;
}

NODE_API_MODULE(addon, Init)
```

**4. Build the addon:**

```bash
bun run node-gyp configure build
```

**5. Use the addon:**

```javascript
// index.js
import addon from './build/Release/addon.node';

console.log(addon.hello());  // "Hello from native code!"
console.log(addon.add(3, 7));  // 10
```

### Bundling Applications with Native Modules

**Build configuration:**

```javascript
// build.js
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  target: 'node',
  external: ['sharp', 'better-sqlite3', 'bcrypt']  // Don't bundle native modules
});
```

**Why external?**

Native modules (`.node` files) are binary and cannot be bundled. They must be kept external and distributed alongside your bundle.

### Distributing Apps with Native Modules

**Project structure:**

```
my-app/
├── dist/
│   └── index.js                    # Your bundled code
├── node_modules/
│   ├── sharp/
│   │   └── build/Release/sharp.node
│   └── better-sqlite3/
│       └── build/Release/better_sqlite3.node
└── package.json
```

**package.json:**

```json
{
  "name": "my-app",
  "type": "module",
  "main": "dist/index.js",
  "dependencies": {
    "sharp": "^0.33.0",
    "better-sqlite3": "^9.0.0"
  },
  "scripts": {
    "build": "bun build src/index.js --outdir dist --external sharp --external better-sqlite3",
    "start": "bun dist/index.js"
  }
}
```

**Distribution steps:**

1. Run `bun install` to get native modules for the target platform
2. Run `bun run build` to create the bundle
3. Include `dist/`, `node_modules/`, and `package.json` in distribution
4. Users run `bun install --production` then `bun start`

### Platform-Specific Native Modules

Some native modules are platform-specific. Handle this in your build:

```javascript
// platform-loader.js
let nativeModule;

if (process.platform === 'darwin') {
  nativeModule = await import('./native/macos/addon.node');
} else if (process.platform === 'linux') {
  nativeModule = await import('./native/linux/addon.node');
} else if (process.platform === 'win32') {
  nativeModule = await import('./native/windows/addon.node');
} else {
  throw new Error(`Unsupported platform: ${process.platform}`);
}

export default nativeModule;
```

### Troubleshooting Native Modules

**Problem: Module not found after building**

Solution: Make sure native modules are external:

```javascript
await Bun.build({
  entrypoints: ['src/index.js'],
  outdir: 'dist',
  external: ['sharp', 'better-sqlite3']  // Add all native modules here
});
```

**Problem: Wrong architecture/platform**

Solution: Rebuild on target platform:

```bash
bun install --force
```

**Problem: Version mismatch**

Solution: Use exact versions in `package.json`:

```json
{
  "dependencies": {
    "sharp": "0.33.0"  // Exact version, not ^0.33.0
  }
}
```

### Native Module Best Practices

1. **Mark as external**: Always external-mark native modules in build config
2. **Document system requirements**: Specify required build tools (Python, C++ compiler)
3. **Test on target platforms**: Verify native modules work on all target OS/architectures
4. **Use pre-built binaries**: Prefer modules with pre-built binaries (like sharp)
5. **Pin versions**: Use exact versions for reproducible builds
6. **Handle errors properly**: Let native module errors propagate - fail fast if loading fails
7. **Check compatibility**: Verify Bun compatibility before using a native module
8. **Include in distribution**: Don't forget to include `node_modules/` for native deps
9. **Document build process**: Explain how to rebuild native modules if needed
10. **Consider alternatives**: Use pure JS alternatives when performance isn't critical

---

## Cross-References

- **Previous**: [Part 6: Dynamic Imports](./bun-advanced-features-part6-dynamic-imports.md)
- **Next**: [Part 8: JSON Imports](./bun-advanced-features-part8-json-imports.md)
- **Related**: [Part 9: Edge Cases](./bun-advanced-features-part9-edge-cases.md) - Native module edge cases
- **Index**: [Bun Advanced Features](./bun-advanced-features.md) - Complete feature index
