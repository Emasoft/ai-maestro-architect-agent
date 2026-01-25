# Custom LSP Plugin Template

## Table of Contents
1. Plugin Structure
2. plugin.json Template
3. .lsp.json Template
4. Advanced Options
5. Debug Logging

## Plugin Structure
```
~/.claude/plugins/my-lsp/
├── .claude-plugin/
│   └── plugin.json
└── .lsp.json  (optional, alternative to inline)
```

## plugin.json Template
```json
{
  "name": "my-language-lsp",
  "description": "LSP support for My Language",
  "version": "1.0.0",
  "lspServers": {
    "mylang": {
      "command": "mylang-lsp",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".ml": "mylang",
        ".mlt": "mylang"
      },
      "transport": "stdio",
      "restartOnCrash": true,
      "maxRestarts": 3,
      "startupTimeout": 10000,
      "shutdownTimeout": 5000
    }
  }
}
```

## .lsp.json Alternative
```json
{
  "mylang": {
    "command": "mylang-lsp",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ml": "mylang"
    }
  }
}
```

## Advanced Options
```json
{
  "mylang": {
    "command": "mylang-lsp",
    "args": ["--stdio"],
    "extensionToLanguage": { ".ml": "mylang" },
    "env": {
      "MY_LSP_LOG": "debug"
    },
    "initializationOptions": {
      "typeCheckingMode": "strict"
    },
    "settings": {
      "mylang.analysis.autoSearchPaths": true
    }
  }
}
```

## Debug Logging
```json
{
  "loggingConfig": {
    "args": ["--log-level", "4"],
    "env": {
      "LSP_LOG": "-level verbose -file ${CLAUDE_PLUGIN_LSP_LOG_FILE}"
    }
  }
}
```

Enable with: claude --enable-lsp-logging
Logs at: ~/.claude/debug/

## Official Documentation

**Always refer to official documentation for the latest LSP server configurations.**

- [Claude Code LSP Servers Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp#lsp-servers)
- [Claude Code Plugin System](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Plugin JSON Schema](https://docs.anthropic.com/en/docs/claude-code/plugins#plugin-structure)
- [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/)

The official Anthropic documentation is the authoritative source for:
- Plugin structure and manifest format
- LSP configuration schema and fields
- Environment variables and logging options
- Plugin lifecycle and initialization
- Debugging and diagnostics procedures
