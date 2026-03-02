# LSP Remediation Procedures

If LSP verification fails for any language, follow these remediation steps.

## Table of Contents

- [Python (pyright) Remediation](#python-pyright-remediation)
- [TypeScript (typescript-language-server) Remediation](#typescript-typescript-language-server-remediation)
- [Rust (rust-analyzer) Remediation](#rust-rust-analyzer-remediation)
- [Go (gopls) Remediation](#go-gopls-remediation)
- [Java (jdtls) Remediation](#java-jdtls-remediation)
- [Kotlin (kotlin-language-server) Remediation](#kotlin-kotlin-language-server-remediation)
- [C/C++ (clangd) Remediation](#cc-clangd-remediation)
- [C# (OmniSharp/csharp-ls) Remediation](#c-omnisharpcsharp-ls-remediation)
- [PHP (Intelephense) Remediation](#php-intelephense-remediation)
- [Ruby (Solargraph) Remediation](#ruby-solargraph-remediation)
- [HTML/CSS (Standalone Language Servers) Remediation](#htmlcss-standalone-language-servers-remediation)

---

## Python (pyright) Remediation

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

## TypeScript (typescript-language-server) Remediation

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

## Rust (rust-analyzer) Remediation

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

## Go (gopls) Remediation

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

## Java (jdtls) Remediation

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

## Kotlin (kotlin-language-server) Remediation

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

## C/C++ (clangd) Remediation

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

## C# (OmniSharp/csharp-ls) Remediation

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

## PHP (Intelephense) Remediation

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

## Ruby (Solargraph) Remediation

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

## HTML/CSS (Standalone Language Servers) Remediation

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

**Next**: See [lsp-enforcement-checklist-part3-verification.md](lsp-enforcement-checklist-part3-verification.md) for post-assignment verification procedures.
