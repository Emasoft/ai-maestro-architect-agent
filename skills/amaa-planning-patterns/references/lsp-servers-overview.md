# LSP Server Integration for Remote Agents

## Table of Contents
1. What Are LSP Servers
2. Benefits for Remote Agents
3. Available LSP Plugins
4. Configuration Options
5. Enforcement Requirements

## What Are LSP Servers
Language Server Protocol (LSP) provides real-time diagnostics, navigation, and code intelligence to Claude Code agents.

## Benefits for Remote Agents
- Instant diagnostics after edits
- Type information and documentation
- Go to definition, find references
- Fewer type errors in submitted code

## Available LSP Plugins

| Plugin | Language | Install Command |
|--------|----------|-----------------|
| pyright-lsp | Python | `pip install pyright` |
| typescript-lsp | TypeScript | `npm install -g typescript-language-server typescript` |
| rust-lsp | Rust | See rust-analyzer installation |

## Configuration Methods

### 1. Dedicated .lsp.json
```json
{
  "python": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": { ".py": "python" }
  }
}
```

### 2. Inline in plugin.json
```json
{
  "name": "my-plugin",
  "lspServers": {
    "python": {
      "command": "pyright-langserver",
      "args": ["--stdio"],
      "extensionToLanguage": { ".py": "python" }
    }
  }
}
```

## Configuration Fields

### Required
- command: LSP binary (must be in PATH)
- extensionToLanguage: Maps extensions to language IDs

### Optional
- args: CLI arguments
- transport: "stdio" (default) or "socket"
- env: Environment variables
- initializationOptions: Server init options
- settings: Workspace settings
- restartOnCrash: Auto-restart on crash
- maxRestarts: Max restart attempts

## Enforcement Requirements

Remote agents MUST have LSP servers installed for project languages before starting work.

## Official Documentation

**Always refer to official documentation for the latest LSP server configurations.**

- [Claude Code LSP Servers Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp#lsp-servers)
- [Claude Code Plugin System](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/)

The official Anthropic documentation is the authoritative source for:
- Supported LSP configuration fields
- Plugin structure requirements
- LSP server lifecycle management
- Debugging and troubleshooting procedures
