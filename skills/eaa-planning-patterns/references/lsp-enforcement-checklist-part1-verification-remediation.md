# LSP Enforcement Checklist - Part 1: Verification & Remediation

Covers pre-assignment checks, installation verification, and remediation procedures for all 11 languages supported by Claude Code LSP (December 2025).

## Table of Contents
1. [Pre-Assignment Checks](#pre-assignment-checks)
2. [Installation Verification](#installation-verification)
   - 2.1 Core Languages (Python, TypeScript, Go, Rust)
   - 2.2 JVM Languages (Java, Kotlin)
   - 2.3 Systems Languages (C/C++, C#)
   - 2.4 Web Languages (PHP, Ruby, HTML/CSS)
3. [Automated Verification](#automated-verification)
4. [Remediation Procedures](#remediation-procedures)
   - 4.1 Python (pyright) Remediation
   - 4.2 TypeScript Remediation
   - 4.3 Rust (rust-analyzer) Remediation
   - 4.4 Go (gopls) Remediation
   - 4.5 Java (jdtls) Remediation
   - 4.6 Kotlin Remediation
   - 4.7 C/C++ (clangd) Remediation
   - 4.8 C# (OmniSharp) Remediation
   - 4.9 PHP (Intelephense) Remediation
   - 4.10 Ruby (Solargraph) Remediation
   - 4.11 HTML/CSS Remediation

**Related Documents:**
- [Part 2: Remediation](./lsp-enforcement-checklist-part2-remediation.md)
- [Part 3: Verification](./lsp-enforcement-checklist-part3-verification.md)
- [Part 4: Troubleshooting Core](./lsp-enforcement-checklist-part4-troubleshooting-core.md)
- [Part 5: Troubleshooting Extended](./lsp-enforcement-checklist-part5-troubleshooting-extended.md)
- [Index](./lsp-enforcement-checklist.md)

---

## Pre-Assignment Checks

Before assigning work to a remote agent:

- [ ] Identify project languages (Python, TypeScript, Go, Rust, Java, Kotlin, C/C++, C#, PHP, Ruby, HTML/CSS)
- [ ] List required LSP servers for each language
- [ ] Verify agent has access to package managers (pip, npm, cargo, go, gem, dotnet, brew/apt)

## Installation Verification

For each language in the project:

### Core Languages

#### Python
- [ ] pyright binary installed: `which pyright-langserver`
- [ ] pyright-lsp plugin installed: `/plugin list | grep pyright`

#### TypeScript/JavaScript
- [ ] typescript-language-server installed: `which typescript-language-server`
- [ ] typescript-lsp plugin installed: `/plugin list | grep typescript`

#### Go
- [ ] gopls installed: `which gopls`
- [ ] go-lsp plugin installed: `/plugin list | grep gopls`

#### Rust
- [ ] rust-analyzer installed: `which rust-analyzer`
- [ ] rust-lsp plugin installed: `/plugin list | grep rust`

### JVM Languages

#### Java
- [ ] jdtls installed: `which jdtls`
- [ ] JDK 11+ installed: `java --version`
- [ ] java-lsp plugin installed: `/plugin list | grep java`

#### Kotlin
- [ ] kotlin-language-server installed: `which kotlin-language-server`
- [ ] JDK 11+ installed: `java --version`
- [ ] kotlin-lsp plugin installed: `/plugin list | grep kotlin`

### Systems Languages

#### C/C++
- [ ] clangd installed: `which clangd`
- [ ] compile_commands.json exists (for project-aware analysis)
- [ ] cpp-lsp plugin installed: `/plugin list | grep clangd`

#### C#
- [ ] OmniSharp or csharp-ls installed: `which OmniSharp` or `dotnet tool list -g | grep csharp-ls`
- [ ] .NET SDK 6.0+ installed: `dotnet --version`
- [ ] csharp-lsp plugin installed: `/plugin list | grep omnisharp`

### Web Languages

#### PHP
- [ ] intelephense installed: `which intelephense`
- [ ] php-lsp plugin installed: `/plugin list | grep intelephense`

#### Ruby
- [ ] solargraph installed: `which solargraph`
- [ ] Ruby 2.7+ installed: `ruby --version`
- [ ] ruby-lsp plugin installed: `/plugin list | grep solargraph`

#### HTML/CSS
- [ ] html-language-server installed: `which vscode-html-language-server`
- [ ] css-language-server installed: `which vscode-css-language-server`
- [ ] html-lsp/css-lsp plugins installed: `/plugin list | grep html`

## Automated Verification

Run verification script:
```bash
python scripts/install_lsp.py --project-path /path/to/project --verify-only
```

Expected output:
```
[OK] python: pyright-langserver installed
[OK] typescript: typescript-language-server installed
```

If any show [MISSING], run without --verify-only to install.

---

## Remediation Procedures

If LSP verification fails for any language, follow these remediation steps:

### Python (pyright) Remediation

**If binary missing:**
```bash
# Install via npm (recommended)
npm install -g pyright

# Verify installation
which pyright-langserver
pyright --version
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install pyright-lsp

# Verify plugin loaded
/plugin list | grep pyright
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language python --project-path /path/to/project
```

### TypeScript (typescript-language-server) Remediation

**If binary missing:**
```bash
# Install via npm
npm install -g typescript-language-server typescript

# Verify installation
which typescript-language-server
typescript-language-server --version
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install typescript-lsp

# Verify plugin loaded
/plugin list | grep typescript
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language typescript --project-path /path/to/project
```

### Rust (rust-analyzer) Remediation

**If binary missing:**
```bash
# Install via rustup (recommended)
rustup component add rust-analyzer

# Or via cargo
cargo install rust-analyzer

# Verify installation
which rust-analyzer
rust-analyzer --version
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install rust-lsp

# Verify plugin loaded
/plugin list | grep rust
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language rust --project-path /path/to/project
```

### Go (gopls) Remediation

**If binary missing:**
```bash
# Install via go install
go install golang.org/x/tools/gopls@latest

# Ensure $GOPATH/bin is in PATH
export PATH=$PATH:$(go env GOPATH)/bin

# Verify installation
which gopls
gopls version
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install gopls-lsp

# Verify plugin loaded
/plugin list | grep gopls
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language go --project-path /path/to/project
```

### Java (jdtls) Remediation

**If binary missing:**
```bash
# macOS
brew install jdtls

# Linux (via SDKMAN)
curl -s "https://get.sdkman.io" | bash
sdk install java 21-tem
# Then download jdtls from Eclipse

# Verify installation
which jdtls
java --version  # JDK 11+ required
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install jdtls-lsp

# Verify plugin loaded
/plugin list | grep java
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language java --project-path /path/to/project
```

### Kotlin (kotlin-language-server) Remediation

**If binary missing:**
```bash
# macOS
brew install kotlin-language-server

# Via npm (cross-platform)
npm install -g kotlin-language-server

# Verify installation
which kotlin-language-server
java --version  # JDK 11+ required
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install kotlin-lsp

# Verify plugin loaded
/plugin list | grep kotlin
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language kotlin --project-path /path/to/project
```

### C/C++ (clangd) Remediation

**If binary missing:**
```bash
# macOS
brew install llvm
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"

# Linux (Debian/Ubuntu)
sudo apt install clangd

# Verify installation
which clangd
clangd --version
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install clangd-lsp

# Verify plugin loaded
/plugin list | grep clangd
```

**If compile_commands.json missing:**
```bash
# For CMake projects
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..

# For Make projects
bear -- make

# For Meson projects
meson compile -C builddir --ninja-args=-t,compdb > compile_commands.json
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language cpp --project-path /path/to/project
```

### C# (OmniSharp/csharp-ls) Remediation

**If binary missing:**
```bash
# Via .NET SDK (recommended)
dotnet tool install -g csharp-ls

# macOS (OmniSharp alternative)
brew install omnisharp-roslyn

# Verify installation
dotnet --version  # .NET SDK 6.0+ required
which csharp-ls || which OmniSharp
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install omnisharp-lsp

# Verify plugin loaded
/plugin list | grep omnisharp
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language csharp --project-path /path/to/project
```

### PHP (Intelephense) Remediation

**If binary missing:**
```bash
# Install via npm
npm install -g intelephense

# Verify installation
which intelephense
intelephense --version
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install intelephense-lsp

# Verify plugin loaded
/plugin list | grep intelephense
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language php --project-path /path/to/project
```

### Ruby (Solargraph) Remediation

**If binary missing:**
```bash
# Install via gem
gem install solargraph

# Download Ruby core documentation
solargraph download-core

# Verify installation
ruby --version  # Ruby 2.7+ required
which solargraph
solargraph --version
```

**If plugin missing:**
```bash
# Install Claude Code plugin
/plugin install solargraph-lsp

# Verify plugin loaded
/plugin list | grep solargraph
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language ruby --project-path /path/to/project
```

### HTML/CSS (Standalone Language Servers) Remediation

**If binary missing:**
```bash
# Install standalone servers (not VS Code dependent, just npm package name)
npm install -g vscode-langservers-extracted

# Verify installation
which vscode-html-language-server
which vscode-css-language-server
```

**If plugin missing:**
```bash
# Install Claude Code plugins
/plugin install html-lsp
/plugin install css-lsp

# Verify plugins loaded
/plugin list | grep html
/plugin list | grep css
```

**If both missing:**
```bash
# Run automated installation
python scripts/install_lsp.py --language html --project-path /path/to/project
python scripts/install_lsp.py --language css --project-path /path/to/project
```

---

**Next:** [Part 2: Remediation](lsp-enforcement-checklist-part2-remediation.md)
