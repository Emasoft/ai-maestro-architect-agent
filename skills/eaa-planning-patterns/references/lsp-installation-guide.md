# LSP Server Installation Guide

Complete installation guide for all 11 languages supported by Claude Code LSP.

## Table of Contents
1. Core Languages
   - Python (Pyright)
   - TypeScript/JavaScript
   - Go (gopls)
   - Rust (rust-analyzer)
2. JVM Languages
   - Java (jdtls)
   - Kotlin
3. Systems Languages
   - C/C++ (clangd)
   - C# (OmniSharp)
4. Web Languages
   - PHP (Intelephense)
   - Ruby (Solargraph)
   - HTML/CSS
5. Verification
6. Troubleshooting

---

## 1. Core Languages

### Python (Pyright)

```bash
# Install binary
pip install pyright
# or
npm install -g pyright

# Install plugin
/plugin install pyright-lsp
```

### TypeScript/JavaScript

```bash
# Install binary
npm install -g typescript-language-server typescript

# Install plugin
/plugin install typescript-lsp
```

### Go (gopls)

```bash
# Install binary
go install golang.org/x/tools/gopls@latest

# Verify installation
gopls version

# Install plugin (or create custom - see below)
/plugin install gopls-lsp
```

**Custom plugin** (if marketplace plugin unavailable):
```json
// ~/.claude/plugins/go-lsp/.claude-plugin/plugin.json
{
  "name": "go-lsp",
  "description": "Go Language Server",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": { ".go": "go" }
    }
  }
}
```

### Rust (rust-analyzer)

```bash
# Install binary (via rustup)
rustup component add rust-analyzer

# Or standalone (macOS)
brew install rust-analyzer

# Install plugin
/plugin install rust-lsp
```

---

## 2. JVM Languages

### Java (Eclipse JDT Language Server)

**macOS:**
```bash
brew install jdtls
```

**Linux (Ubuntu/Debian):**
```bash
# Via SDKMAN
curl -s "https://get.sdkman.io" | bash
sdk install java 21-tem
# Then download jdtls from Eclipse
```

**Plugin configuration:**
```json
{
  "name": "java-lsp",
  "description": "Java Language Server (Eclipse JDT)",
  "lspServers": {
    "java": {
      "command": "jdtls",
      "args": [],
      "extensionToLanguage": { ".java": "java" }
    }
  }
}
```

### Kotlin

**macOS:**
```bash
brew install kotlin-language-server
```

**Via npm:**
```bash
npm install -g kotlin-language-server
```

**Requirements:** JDK 11+ must be installed.

---

## 3. Systems Languages

### C/C++ (clangd)

**macOS:**
```bash
brew install llvm
# Add to PATH: export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install clangd
```

**Plugin configuration:**
```json
{
  "name": "cpp-lsp",
  "description": "C/C++ Language Server (clangd)",
  "lspServers": {
    "cpp": {
      "command": "clangd",
      "args": ["--background-index"],
      "extensionToLanguage": {
        ".c": "c",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".h": "c",
        ".hpp": "cpp"
      }
    }
  }
}
```

### C# (OmniSharp / csharp-ls)

**Via .NET SDK:**
```bash
dotnet tool install -g csharp-ls
```

**macOS (OmniSharp):**
```bash
brew install omnisharp-roslyn
```

**Requirements:** .NET SDK 6.0+

---

## 4. Web Languages

### PHP (Intelephense)

```bash
npm install -g intelephense
```

**Note:** Premium features require license. Free tier provides core LSP functionality.

**Plugin configuration:**
```json
{
  "name": "php-lsp",
  "description": "PHP Language Server (Intelephense)",
  "lspServers": {
    "php": {
      "command": "intelephense",
      "args": ["--stdio"],
      "extensionToLanguage": { ".php": "php", ".phtml": "php" }
    }
  }
}
```

### Ruby (Solargraph)

```bash
gem install solargraph
solargraph download-core  # Download Ruby core documentation
```

**Requirements:** Ruby 2.7+

### HTML/CSS (Standalone Language Servers)

```bash
# The vscode-langservers-extracted package provides standalone LSP servers
# that work independently (not tied to VS Code - just the package name)
npm install -g vscode-langservers-extracted
```

This installs standalone binaries:
- `vscode-html-language-server` - HTML LSP
- `vscode-css-language-server` - CSS/SCSS/LESS LSP
- `vscode-json-language-server` - JSON LSP

**Alternative HTML server:**
```bash
npm install -g @anthropic-ai/html-language-server  # If available in marketplace
```

**Plugin configuration:**
```json
{
  "name": "html-lsp",
  "description": "HTML Language Server",
  "lspServers": {
    "html": {
      "command": "vscode-html-language-server",
      "args": ["--stdio"],
      "extensionToLanguage": { ".html": "html", ".htm": "html" }
    }
  }
}
```

---

## 5. Verification

```bash
# List installed plugins
/plugin list

# Check for LSP errors
/plugin errors

# Verify specific binary is installed
which pyright-langserver
which typescript-language-server
which gopls
which rust-analyzer
which clangd
which jdtls
```

**Test LSP in Claude Code:**
1. Open a file of the target language
2. Type `/lsp status` to check server status
3. Try go-to-definition on a symbol

---

## 6. Troubleshooting

### "Executable not found in $PATH"
1. Install the language server binary (see sections above)
2. Ensure it's in your PATH: `echo $PATH`
3. Restart Claude Code: `/exit` then relaunch

### LSP Not Starting
1. Check debug logs: `~/.claude/debug/`
2. Verify binary works standalone: `<binary> --version`
3. Check plugin.json syntax is valid JSON

### Plugin Not Recognized
1. Verify plugin directory structure:
   ```
   ~/.claude/plugins/<name>/
   └── .claude-plugin/
       └── plugin.json
   ```
2. Restart Claude Code after adding plugins

### Java/Kotlin: "JDK not found"
1. Install JDK 11+: `java --version`
2. Set JAVA_HOME: `export JAVA_HOME=$(/usr/libexec/java_home)`

### C#: "dotnet not found"
1. Install .NET SDK: https://dotnet.microsoft.com/download
2. Verify: `dotnet --version`

## Official Documentation

**Always refer to official documentation for the latest LSP server configurations.**

- [Claude Code LSP Servers Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp#lsp-servers)
- [Claude Code Plugin System](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Pyright Installation](https://microsoft.github.io/pyright/#/installation)
- [TypeScript Language Server](https://github.com/typescript-language-server/typescript-language-server)
- [Rust Analyzer Manual](https://rust-analyzer.github.io/manual.html)

The official Anthropic documentation is the authoritative source for:
- LSP plugin installation procedures
- Supported language servers
- Configuration options and examples
- Platform-specific installation requirements
