# LSP Troubleshooting: Core Languages

Troubleshooting guide for Python, TypeScript, Rust, and Go LSP issues.

---

## Table of Contents

- [General LSP Issues](#general-lsp-issues)
  - [LSP Server Won't Start](#lsp-server-wont-start)
  - [LSP Diagnostics Not Appearing](#lsp-diagnostics-not-appearing)
  - [Performance Issues](#performance-issues)
- [Python (pyright) Issues](#python-pyright-issues)
  - ["Cannot find module" errors for installed packages](#cannot-find-module-errors-for-installed-packages)
  - ["Type is partially unknown" warnings](#type-is-partially-unknown-warnings)
- [TypeScript Issues](#typescript-issues)
  - ["Cannot find name" for global types](#cannot-find-name-for-global-types)
  - ["Property does not exist on type" after adding new field](#property-does-not-exist-on-type-after-adding-new-field)
- [Rust (rust-analyzer) Issues](#rust-rust-analyzer-issues)
  - ["Unresolved import" for workspace crates](#unresolved-import-for-workspace-crates)
  - ["Proc macro not expanded" errors](#proc-macro-not-expanded-errors)
  - ["Could not resolve macro" for custom derives](#could-not-resolve-macro-for-custom-derives)
- [Go (gopls) Issues](#go-gopls-issues)
  - ["Package not found" for local modules](#package-not-found-for-local-modules)
  - ["Undefined: package name" after adding import](#undefined-package-name-after-adding-import)
  - ["No required module provides package"](#no-required-module-provides-package)

---

## General LSP Issues

### LSP Server Won't Start

**Symptoms:**
- `/plugin errors` shows LSP initialization failures
- "Executable not found in $PATH" errors
- LSP features (go-to-definition, hover) not working

**Diagnosis Steps:**
1. Verify binary installed: `which <lsp-binary>`
2. Check plugin loaded: `/plugin list | grep <lsp-name>`
3. Review debug logs: `~/.claude/debug/lsp-*.log`
4. Test binary manually: `<lsp-binary> --version`

**Common Fixes:**
- Binary not in PATH: Add to PATH and restart Claude Code
- Plugin not loaded: Run `/plugin install <lsp-name>`
- Binary permissions: `chmod +x $(which <lsp-binary>)`
- Conflicting versions: Uninstall old versions, install latest

### LSP Diagnostics Not Appearing

**Symptoms:**
- No errors/warnings shown for obviously broken code
- `/plugin errors` shows "No diagnostics"

**Diagnosis:**
1. Check LSP server running: `/plugin list` (should show "active")
2. Verify file extension mapped: Check plugin's `extensionToLanguage`
3. Review initialization: Check `~/.claude/debug/lsp-*.log` for init errors

**Common Fixes:**
- File extension not mapped: Update plugin's `extensionToLanguage`
- LSP crashed: Restart Claude Code to restart LSP
- Wrong working directory: Ensure LSP started in project root

### Performance Issues

**Symptoms:**
- Slow auto-completion
- High CPU usage by LSP process
- Delayed diagnostics

**Solutions:**
- Exclude large directories (node_modules, .venv) in LSP settings
- Reduce diagnostics scope in initializationOptions
- Increase LSP memory limits in plugin config
- Use faster LSP implementations (e.g., pyright over pylsp)

---

## Python (pyright) Issues

### "Cannot find module" errors for installed packages

**Cause:** Virtual environment not detected or wrong Python interpreter

**Solution:**
```bash
# Check current Python interpreter
which python

# Activate virtual environment
source .venv/bin/activate

# Verify pyright sees packages
pyright --pythonpath .venv/lib/python*/site-packages src/

# Create pyrightconfig.json
cat > pyrightconfig.json <<EOF
{
  "venvPath": ".",
  "venv": ".venv",
  "executionEnvironments": [
    {
      "root": "src"
    }
  ]
}
EOF
```

### "Type is partially unknown" warnings

**Cause:** Missing type stubs for third-party libraries

**Solution:**
```bash
# Install type stubs
pip install types-requests types-pyyaml types-redis

# Or use pyright's stub generation
pyright --createstub <library-name>
```

---

## TypeScript Issues

### "Cannot find name" for global types

**Cause:** Missing @types packages or incorrect tsconfig.json

**Solution:**
```bash
# Install missing @types packages
npm install --save-dev @types/node @types/jest

# Check tsconfig.json includes types
cat tsconfig.json
# Should have:
{
  "compilerOptions": {
    "types": ["node", "jest"],
    "typeRoots": ["./node_modules/@types"]
  }
}

# Reload TypeScript server
npx tsc --build --clean && npx tsc --noEmit
```

### "Property does not exist on type" after adding new field

**Cause:** Stale TypeScript server cache

**Solution:**
```bash
# Clear TypeScript build cache
rm -rf .tsbuildinfo
npx tsc --build --clean

# Restart typescript-language-server
/plugin reload typescript-lsp

# Verify type definitions updated
npx tsc --noEmit --listFiles | grep <your-file>
```

---

## Rust (rust-analyzer) Issues

### "Unresolved import" for workspace crates

**Cause:** Cargo workspace not properly configured

**Solution:**
```bash
# Verify Cargo.toml workspace configuration
cat Cargo.toml
# Should have:
[workspace]
members = ["crate1", "crate2"]

# Regenerate Cargo.lock
cargo clean
cargo update

# Force rust-analyzer to reload
cargo check
```

### "Proc macro not expanded" errors

**Cause:** Procedural macros not being expanded by rust-analyzer

**Solution:**
```bash
# Enable proc-macro expansion in rust-analyzer config
# Create .vscode/settings.json or rust-analyzer.toml
{
  "rust-analyzer.cargo.buildScripts.enable": true,
  "rust-analyzer.procMacro.enable": true,
  "rust-analyzer.procMacro.attributes.enable": true
}

# Rebuild with proc-macros
cargo clean && cargo build
```

### "Could not resolve macro" for custom derives

**Cause:** Build scripts or dependencies not compiled

**Solution:**
```bash
# Run cargo build to compile proc-macros
cargo build

# Check build script execution
cargo build -vv | grep "Running"

# Reload rust-analyzer
cargo clean && cargo check
```

---

## Go (gopls) Issues

### "Package not found" for local modules

**Cause:** Go module not initialized or incorrect go.mod

**Solution:**
```bash
# Initialize Go module if missing
go mod init <module-path>

# Verify go.mod references local modules correctly
cat go.mod
# Should have:
module example.com/myproject
go 1.21
require (
  example.com/myproject/internal v0.0.0
)
replace example.com/myproject/internal => ./internal

# Download dependencies
go mod download
go mod tidy

# Reload gopls
gopls check ./...
```

### "Undefined: package name" after adding import

**Cause:** gopls cache not updated or module not downloaded

**Solution:**
```bash
# Download missing module
go get <module-path>
go mod tidy

# Clear gopls cache
rm -rf ~/.cache/gopls/

# Verify import path correct
go list -m all | grep <package-name>

# Reload gopls
gopls check ./...
```

### "No required module provides package"

**Cause:** Missing or incorrect module version in go.mod

**Solution:**
```bash
# Add missing module
go get <module-path>@latest

# Or specific version
go get <module-path>@v1.2.3

# Update go.mod and go.sum
go mod tidy

# Verify module added
grep <module-name> go.mod

# Reload gopls
gopls check ./...
```

---

**Next**: See [lsp-enforcement-checklist-part5-troubleshooting-extended.md](lsp-enforcement-checklist-part5-troubleshooting-extended.md) for JVM, Systems, and Web language troubleshooting.
