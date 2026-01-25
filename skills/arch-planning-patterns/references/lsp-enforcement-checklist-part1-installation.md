# LSP Installation & Verification

This document covers pre-assignment checks and installation verification for all 11 languages supported by Claude Code LSP (December 2025).

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

**Next**: See [lsp-enforcement-checklist-part2-remediation.md](lsp-enforcement-checklist-part2-remediation.md) for remediation procedures when verification fails.
