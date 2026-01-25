# LSP Enforcement Checklist for Remote Agents

Covers all 11 languages supported by Claude Code LSP (December 2025).

## Table of Contents

1. [Pre-Assignment Checks](#pre-assignment-checks)
2. [Installation Verification](#installation-verification)
3. [Remediation Procedures](#remediation-procedures)
4. [Post-Assignment Verification](#post-assignment-verification)
5. [Orchestrator Enforcement](#orchestrator-enforcement)
6. [Troubleshooting Guide](#troubleshooting-guide)

## Document Structure

This checklist is split into multiple focused documents for efficient reference:

| Document | Contents | Lines |
|----------|----------|-------|
| [Part 1: Installation](lsp-enforcement-checklist-part1-installation.md) | Pre-assignment checks, installation verification for all 11 languages | ~90 |
| [Part 2: Remediation](lsp-enforcement-checklist-part2-remediation.md) | Step-by-step fixes for each language when LSP is missing | ~340 |
| [Part 3: Verification](lsp-enforcement-checklist-part3-verification.md) | Post-assignment checks, quality gates, enforcement rules | ~135 |
| [Part 4: Troubleshooting Core](lsp-enforcement-checklist-part4-troubleshooting-core.md) | Python, TypeScript, Rust, Go troubleshooting | ~260 |
| [Part 5: Troubleshooting Extended](lsp-enforcement-checklist-part5-troubleshooting-extended.md) | Java, Kotlin, C/C++, C#, PHP, Ruby, cross-language issues | ~310 |

---

## Quick Reference: Supported Languages

| Language | LSP Server | Binary Check | Plugin Check |
|----------|------------|--------------|--------------|
| Python | pyright | `which pyright-langserver` | `/plugin list \| grep pyright` |
| TypeScript | typescript-language-server | `which typescript-language-server` | `/plugin list \| grep typescript` |
| Go | gopls | `which gopls` | `/plugin list \| grep gopls` |
| Rust | rust-analyzer | `which rust-analyzer` | `/plugin list \| grep rust` |
| Java | jdtls | `which jdtls` | `/plugin list \| grep java` |
| Kotlin | kotlin-language-server | `which kotlin-language-server` | `/plugin list \| grep kotlin` |
| C/C++ | clangd | `which clangd` | `/plugin list \| grep clangd` |
| C# | OmniSharp/csharp-ls | `which csharp-ls` | `/plugin list \| grep omnisharp` |
| PHP | intelephense | `which intelephense` | `/plugin list \| grep intelephense` |
| Ruby | solargraph | `which solargraph` | `/plugin list \| grep solargraph` |
| HTML/CSS | vscode-langservers | `which vscode-html-language-server` | `/plugin list \| grep html` |

---

## Pre-Assignment Checks

Before assigning work to a remote agent:

- [ ] Identify project languages (Python, TypeScript, Go, Rust, Java, Kotlin, C/C++, C#, PHP, Ruby, HTML/CSS)
- [ ] List required LSP servers for each language
- [ ] Verify agent has access to package managers (pip, npm, cargo, go, gem, dotnet, brew/apt)

**Full details**: [Part 1: Installation](lsp-enforcement-checklist-part1-installation.md)

---

## Installation Verification

### Quick Automated Check

```bash
python scripts/install_lsp.py --project-path /path/to/project --verify-only
```

Expected output:
```
[OK] python: pyright-langserver installed
[OK] typescript: typescript-language-server installed
```

If any show [MISSING], run without --verify-only to install.

**Full verification checklists by language**: [Part 1: Installation](lsp-enforcement-checklist-part1-installation.md)

---

## Remediation Procedures

When LSP verification fails, use the language-specific remediation procedures.

### Summary: Installation Commands

| Language | Quick Install Command |
|----------|----------------------|
| Python | `npm install -g pyright` |
| TypeScript | `npm install -g typescript-language-server typescript` |
| Rust | `rustup component add rust-analyzer` |
| Go | `go install golang.org/x/tools/gopls@latest` |
| Java | `brew install jdtls` (macOS) |
| Kotlin | `brew install kotlin-language-server` (macOS) |
| C/C++ | `brew install llvm` (macOS) / `apt install clangd` (Linux) |
| C# | `dotnet tool install -g csharp-ls` |
| PHP | `npm install -g intelephense` |
| Ruby | `gem install solargraph` |
| HTML/CSS | `npm install -g vscode-langservers-extracted` |

**Full remediation procedures**: [Part 2: Remediation](lsp-enforcement-checklist-part2-remediation.md)

---

## Post-Assignment Verification

After remote agent completes work, verify:

### 1. LSP Diagnostics Check
```bash
/plugin errors
# Expected: No errors in changed files
```

### 2. Type Safety Verification

Run language-specific type checkers:
- **Python**: `pyright src/module.py`
- **TypeScript**: `npx tsc --noEmit src/module.ts`
- **Rust**: `cargo check`
- **Go**: `gopls check ./...`

### 3. Quality Gates

Before accepting agent's work:
- [ ] All LSP diagnostics resolved
- [ ] Type checking passes for all languages
- [ ] No "any" types in TypeScript (unless explicitly allowed)
- [ ] No "type: ignore" in Python (unless documented)

**Full verification procedures**: [Part 3: Verification](lsp-enforcement-checklist-part3-verification.md)

---

## Orchestrator Enforcement

The orchestrator MUST:

1. **Before task assignment**: Run LSP verification script
2. **On failure**: Block assignment until LSP installed
3. **In task instructions**: Include "Ensure LSP diagnostics pass"
4. **On PR review**: Verify no LSP errors in changed files

### Rejection Criteria

Reject remote agent assignment if:
- LSP binaries not installed for project languages
- `/plugin errors` shows LSP failures
- Agent reports "executable not found" errors

**Full enforcement rules**: [Part 3: Verification](lsp-enforcement-checklist-part3-verification.md)

---

## Troubleshooting Guide

### Common Issues Quick Reference

| Issue | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| LSP won't start | Binary not in PATH | `which <lsp-binary>`, add to PATH |
| No diagnostics | Plugin not loaded | `/plugin install <lsp-name>` |
| Slow performance | Large directories included | Exclude node_modules, .venv |
| "Module not found" | Wrong venv/interpreter | Activate venv, check pyrightconfig.json |
| Stale cache | Old type definitions | Clear build cache, restart LSP |

### Language-Specific Troubleshooting

**Core Languages** (Python, TypeScript, Rust, Go):
- [Part 4: Troubleshooting Core](lsp-enforcement-checklist-part4-troubleshooting-core.md)

**Extended Languages** (Java, Kotlin, C/C++, C#, PHP, Ruby):
- [Part 5: Troubleshooting Extended](lsp-enforcement-checklist-part5-troubleshooting-extended.md)

---

## Benefits Tracked

Track LSP benefits in progress reports:
- Type errors caught before PR submission
- Reduced review cycles due to fewer basic errors
- Faster navigation to definitions/references

---

## Official Documentation

**Always refer to official documentation for the latest LSP server configurations.**

- [Claude Code LSP Servers Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp#lsp-servers)
- [Claude Code Plugin System](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Claude Code Best Practices](https://docs.anthropic.com/en/docs/claude-code/best-practices)

The official Anthropic documentation is the authoritative source for:
- LSP enforcement requirements and recommendations
- Verification and validation procedures
- Installation troubleshooting guides
- Integration with remote agent workflows
- LSP error handling and recovery strategies
