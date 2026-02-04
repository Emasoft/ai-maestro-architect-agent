# Bun Advanced Features: Standalone Executables

> **Part 3 of 10** | See [bun-advanced-features.md](./bun-advanced-features.md) for the complete index.

## Table of Contents

- [Standalone Executables](#standalone-executables)
  - [What is a Standalone Executable?](#what-is-a-standalone-executable)
  - [Why Create Standalone Executables?](#why-create-standalone-executables)
  - [Creating a Basic Executable](#creating-a-basic-executable)
  - [Executable with Dependencies](#executable-with-dependencies)
  - [Cross-Platform Executables](#cross-platform-executables)
  - [CLI Application Example](#cli-application-example)
  - [Including Static Assets](#including-static-assets)
  - [Server Application Example](#server-application-example)
  - [Executable Best Practices](#executable-best-practices)
  - [Executable Size Optimization](#executable-size-optimization)
- [Cross-References](#cross-references)

---

## Standalone Executables

### What is a Standalone Executable?

A standalone executable is a single binary file that contains your JavaScript/TypeScript code, all dependencies, and the Bun runtime itself. This allows you to distribute your application as a single file that can run on any machine without requiring Bun or Node.js to be installed.

### Why Create Standalone Executables?

- **Easy Distribution**: Share your app as a single file
- **No Runtime Required**: Users don't need Bun installed
- **Platform-Specific**: Create executables for different operating systems
- **Fast Startup**: Executables start faster than interpreted scripts
- **Dependency Bundling**: All dependencies included automatically

### Creating a Basic Executable

**Source Code (cli.js):**

```javascript
#!/usr/bin/env bun

console.log('Hello from standalone executable!');
console.log('Arguments:', process.argv.slice(2));
```

**Build Command:**

```bash
bun build cli.js --compile --outfile=myapp
```

**Result:**

Creates an executable file named `myapp` (or `myapp.exe` on Windows) that you can run directly:

```bash
./myapp arg1 arg2 arg3
```

### Executable with Dependencies

**Source Code (app.js):**

```javascript
#!/usr/bin/env bun

import chalk from 'chalk';
import figlet from 'figlet';

console.log(
  chalk.blue(
    figlet.textSync('MyApp', {
      font: 'Standard',
      horizontalLayout: 'default'
    })
  )
);

console.log(chalk.green('Version 1.0.0'));
console.log(chalk.yellow('Ready to work!'));
```

**Install Dependencies:**

```bash
bun add chalk figlet
```

**Build Command:**

```bash
bun build app.js --compile --outfile=myapp
```

**Result:**

The executable includes `chalk`, `figlet`, and all their dependencies. No `node_modules` needed to run it!

### Cross-Platform Executables

**Build Script (build.js):**

```javascript
import { $ } from 'bun';

const platforms = [
  { target: 'bun-linux-x64', outfile: 'myapp-linux-x64' },
  { target: 'bun-darwin-arm64', outfile: 'myapp-macos-arm64' },
  { target: 'bun-windows-x64', outfile: 'myapp-windows-x64.exe' }
];

for (const platform of platforms) {
  console.log(`Building for ${platform.target}...`);

  await $`bun build src/index.js --compile --target=${platform.target} --outfile=${platform.outfile}`;

  console.log(`✓ Created ${platform.outfile}`);
}
```

**Run Build:**

```bash
bun run build.js
```

### CLI Application Example

**Source Code (src/cli.js):**

```javascript
#!/usr/bin/env bun

import { parseArgs } from 'util';
import { readFileSync } from 'fs';

const { values, positionals } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    help: {
      type: 'boolean',
      short: 'h'
    },
    version: {
      type: 'boolean',
      short: 'v'
    },
    config: {
      type: 'string',
      short: 'c'
    }
  },
  allowPositionals: true
});

if (values.help) {
  console.log(`
Usage: myapp [options] <command>

Options:
  -h, --help       Show help
  -v, --version    Show version
  -c, --config     Config file path

Commands:
  process <file>   Process a file
  convert <file>   Convert a file
  `);
  process.exit(0);
}

if (values.version) {
  const pkg = JSON.parse(readFileSync('./package.json', 'utf-8'));
  console.log(`v${pkg.version}`);
  process.exit(0);
}

const [command, ...args] = positionals;

switch (command) {
  case 'process':
    console.log('Processing:', args[0]);
    break;
  case 'convert':
    console.log('Converting:', args[0]);
    break;
  default:
    console.error('Unknown command:', command);
    console.log('Run --help for usage information');
    process.exit(1);
}
```

**Build:**

```bash
bun build src/cli.js --compile --outfile=myapp
```

**Usage:**

```bash
./myapp --help
./myapp --version
./myapp process input.txt
./myapp convert --config=custom.json data.json
```

### Including Static Assets

**Project Structure:**

```
myapp/
├── src/
│   └── index.js
├── assets/
│   ├── templates/
│   │   └── default.html
│   └── data/
│       └── config.json
└── package.json
```

**Source Code (src/index.js):**

```javascript
import { file } from 'bun';

// Read assets from the executable
const template = await file('assets/templates/default.html').text();
const config = await file('assets/data/config.json').json();

console.log('Template loaded:', template.length, 'bytes');
console.log('Config:', config);
```

**Build with Assets:**

```bash
# Copy assets to a known location that will be bundled
bun build src/index.js --compile --outfile=myapp
```

Note: Currently, Bun's `--compile` automatically includes files accessed via `file()` or `require()` at build time.

### Server Application Example

**Source Code (server.js):**

```javascript
#!/usr/bin/env bun

const server = Bun.serve({
  port: process.env.PORT || 3000,
  fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === '/') {
      return new Response('Hello from standalone executable server!');
    }

    if (url.pathname === '/health') {
      return Response.json({ status: 'ok', uptime: process.uptime() });
    }

    return new Response('Not found', { status: 404 });
  }
});

console.log(`Server running at http://localhost:${server.port}`);
```

**Build:**

```bash
bun build server.js --compile --outfile=myserver
```

**Run:**

```bash
./myserver
# Or with custom port
PORT=8080 ./myserver
```

### Executable Best Practices

1. **Use shebang**: Start scripts with `#!/usr/bin/env bun` for clarity
2. **Handle arguments properly**: Use `Bun.argv.slice(2)` or a proper argument parser
3. **Include help/version**: Always provide `--help` and `--version` flags
4. **Test on target platforms**: Build and test executables on each target OS
5. **Minimize dependencies**: Smaller dependency tree = smaller executable
6. **Bundle static assets**: Include all needed files in the executable
7. **Handle errors gracefully**: Provide clear error messages for users
8. **Sign executables**: Sign your executables for macOS/Windows (optional but recommended)

### Executable Size Optimization

```javascript
// build-optimized.js
await Bun.build({
  entrypoints: ['src/index.js'],
  compile: true,
  outfile: 'myapp',
  minify: true,
  drop: ['console', 'debugger'],
  define: {
    'process.env.NODE_ENV': '"production"'
  }
});
```

---

## Cross-References

- **Previous**: [Part 2: Build Optimization](./bun-advanced-features-part2-build-optimization.md)
- **Next**: [Part 4: CDN and Browser Usage](./bun-advanced-features-part4-cdn-browser.md)
- **Related**: [Part 7: Native Modules](./bun-advanced-features-part7-native-modules.md) - For native module handling in executables
- **Index**: [Bun Advanced Features](./bun-advanced-features.md) - Complete feature index
