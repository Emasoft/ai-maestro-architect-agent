# Orchestrator LSP Management Guide

How the orchestrator manages LSP servers for remote AI agents.

## Table of Contents

1. [Critical Distinction: Global vs Local](#critical-distinction-global-vs-local)
   - [Why This Matters](#why-this-matters)
2. [Overview](#overview)
3. [Orchestrator Responsibilities](#orchestrator-responsibilities)
   - [1. One-Time Setup: Install Global Binaries](#1-one-time-setup-install-global-binaries)
   - [2. Before Task Assignment](#2-before-task-assignment)
   - [3. Include in Task Assignment Message](#3-include-in-task-assignment-message)
   - [4. After Task Completion](#4-after-task-completion)
4. [Command Reference](#command-reference)
   - [Orchestrator Commands (Global Binaries)](#orchestrator-commands-global-binaries)
   - [Remote Agent Commands (Local Activation)](#remote-agent-commands-local-activation)
   - [Common Options](#common-options)
5. [Workflow Examples](#workflow-examples)
   - [Example 1: Python-Only Project](#example-1-python-only-project)
   - [Example 2: Full-Stack TypeScript/Go Project](#example-2-full-stack-typescriptgo-project)
   - [Example 3: Multi-Language Monorepo](#example-3-multi-language-monorepo)
   - [Example 4: Agent Switching Projects](#example-4-agent-switching-projects)
6. [Task Assignment Template](#task-assignment-template)
7. [JSON API for Automation](#json-api-for-automation)
8. [Shared Package Handling](#shared-package-handling)
9. [Troubleshooting](#troubleshooting)
   - [Agent Reports "Binary not found"](#agent-reports-binary-not-found)
   - [Agent Has Wrong LSP Activated](#agent-has-wrong-lsp-activated)
   - [Activation State Corrupted](#activation-state-corrupted)
   - [Project Languages Changed (Branch Switch)](#project-languages-changed-branch-switch)
   - [Agent Started Without Activation](#agent-started-without-activation)
10. [Best Practices](#best-practices)
    - [For Orchestrator](#for-orchestrator)
    - [For Remote Agents](#for-remote-agents)
    - [For Both](#for-both)
11. [Local State File](#local-state-file)
12. [Official Documentation](#official-documentation)
13. [Supported Languages (13 total)](#supported-languages-13-total)
    - [Apple Platform Notes](#apple-platform-notes)

## Critical Distinction: Global vs Local

**LSP management has TWO separate concerns:**

| Concern | Who Does It | Scope | Commands |
|---------|-------------|-------|----------|
| **Global Binaries** | Orchestrator | System-wide (once) | `--install-binaries`, `--uninstall-binaries` |
| **Local Activation** | Remote Agent | Per-project | `--activate`, `--deactivate`, `--sync` |

### Why This Matters

- **Orchestrator** installs binaries globally (shared across all projects)
- **Orchestrator** NEVER activates LSP locally (it doesn't write code)
- **Remote agents** activate only the LSP plugins needed for their assigned project
- **Remote agents** deactivate unneeded plugins to save resources

## Overview

The orchestrator ensures:
1. All required binaries are installed globally (one-time setup)
2. Remote agents know which LSP plugins to activate locally

This optimizes:
- **Memory usage**: Agents only activate needed LSP plugins
- **Startup time**: Fewer active plugins = faster response
- **Resource isolation**: Each project has its own activation state
- **Clean handoffs**: Agents deactivate when switching projects

## Orchestrator Responsibilities

### 1. One-Time Setup: Install Global Binaries

Before any task assignment, ensure all required binaries are installed globally:

```bash
# Install ALL supported LSP binaries globally (recommended for orchestrator machine)
python install_lsp.py --install-binaries --all

# Or install specific languages needed for your projects
python install_lsp.py --install-binaries --languages python,typescript,go,rust

# Verify global binaries are available
python install_lsp.py --verify-binaries --all
```

### 2. Before Task Assignment

Generate activation instructions for the remote agent:

```bash
# Generate instructions showing what agent needs to activate
python install_lsp.py --project-path /path/to/project --generate-instructions

# Check current global binary status
python install_lsp.py --status --json
```

### 3. Include in Task Assignment Message

When assigning a task to a remote agent, include:

```markdown
## LSP Activation Required

Before starting work, activate LSP plugins for this project:

```bash
# Activate LSP for project languages (recommended)
python install_lsp.py --project-path /path/to/project --sync

# This will:
# - Activate LSP plugins for detected languages
# - Deactivate LSP plugins not needed for this project
# - Create local state file at .claude/lsp-state.json
```

Verify setup:
```bash
python install_lsp.py --status --project-path /path/to/project
```
```

### 4. After Task Completion

Instruct agent to clean up:

```bash
# Agent should deactivate all LSP before switching projects
python install_lsp.py --deactivate-all

# Verify no LSP errors in modified files
/plugin errors
```

## Command Reference

### Orchestrator Commands (Global Binaries)

| Command | Purpose |
|---------|---------|
| `--install-binaries --all` | Install ALL LSP binaries globally |
| `--install-binaries --languages X,Y` | Install specific LSP binaries globally |
| `--uninstall-binaries --languages X,Y` | Remove specific LSP binaries globally |
| `--verify-binaries` | Verify global binaries are installed |
| `--generate-instructions` | Create activation instructions for agent |
| `--status --json` | Show status in JSON for automation |

### Remote Agent Commands (Local Activation)

| Command | Purpose |
|---------|---------|
| `--activate --project-path PATH` | Activate LSP for detected languages |
| `--activate --languages X,Y` | Activate specific LSP plugins |
| `--deactivate --languages X,Y` | Deactivate specific LSP plugins |
| `--deactivate-all` | Deactivate ALL LSP plugins (clean slate) |
| `--sync --project-path PATH` | Activate needed, deactivate others |
| `--status` | Show global + local activation status |

### Common Options

| Option | Purpose |
|--------|---------|
| `--project-path PATH` | Project to analyze/activate |
| `--languages X,Y,Z` | Specific languages to target |
| `--all` | All supported languages |
| `--json` | JSON output for automation |
| `-q, --quiet` | Suppress output |

## Workflow Examples

### Example 1: Python-Only Project

Orchestrator assigns Python project to agent:

```
Orchestrator (one-time global setup):
  python install_lsp.py --install-binaries --all

Orchestrator generates instructions:
  python install_lsp.py --project-path /projects/python-app --generate-instructions

Instructions sent to agent:
  "Activate LSP for this Python project:
   python install_lsp.py --project-path /projects/python-app --sync

   This will:
   - Activate: python (pyright)
   - Deactivate: all others
   - State saved to: /projects/python-app/.claude/lsp-state.json"
```

### Example 2: Full-Stack TypeScript/Go Project

```
Orchestrator generates instructions:
  python install_lsp.py --project-path /projects/fullstack --generate-instructions

Instructions sent to agent:
  "Activate LSP for this full-stack project:
   python install_lsp.py --project-path /projects/fullstack --sync

   This will:
   - Activate: typescript, go, html, css
   - Deactivate: python, java, rust, etc."

After agent completes work:
  "Clean up before next assignment:
   python install_lsp.py --deactivate-all"
```

### Example 3: Multi-Language Monorepo

```
Orchestrator generates instructions:
  python install_lsp.py --project-path /projects/monorepo --generate-instructions

Instructions sent to agent:
  "This is a large monorepo with 5 languages.
   Activate all required LSP plugins:
   python install_lsp.py --project-path /projects/monorepo --sync

   Expected activated: python, typescript, go, rust, java

   Note: Higher resource usage expected due to multiple LSP plugins."
```

### Example 4: Agent Switching Projects

```
Agent finishing Project A (Python):
  python install_lsp.py --deactivate-all

Agent starting Project B (TypeScript/React):
  python install_lsp.py --project-path /projects/react-app --sync

  # Only typescript, html, css activated
  # Clean state from previous project
```

## Task Assignment Template

Include this in every task assignment:

```markdown
## Environment Setup

### LSP Activation
Required languages: {detected_languages}

Activate before starting:
```bash
python install_lsp.py --project-path {project_path} --sync
```

This creates a local state file at `{project_path}/.claude/lsp-state.json`.

### Verification
After activation, verify status:
```bash
python install_lsp.py --status --project-path {project_path}
/plugin errors  # Should show no errors
```

### Quality Gate
Before submitting work:
- [ ] All LSP diagnostics resolved
- [ ] Type checking passes for all languages
- [ ] No "any" types in TypeScript
- [ ] No "type: ignore" in Python

### Cleanup
After completing work:
```bash
python install_lsp.py --deactivate-all
```
```

## JSON API for Automation

For automated orchestration:

```python
import subprocess
import json

# Get global + local status
result = subprocess.run(
    ["python", "install_lsp.py", "--status", "--json"],
    capture_output=True, text=True
)
status = json.loads(result.stdout)
# {
#   "global_binaries_installed": ["python", "typescript", ...],
#   "local_lsp_activated": ["python"],
#   "supported_languages": ["python", "typescript", ...]
# }

# Orchestrator: Install global binaries
subprocess.run([
    "python", "install_lsp.py",
    "--install-binaries", "--all"
], check=True)

# Remote agent: Sync activation for project
subprocess.run([
    "python", "install_lsp.py",
    "--project-path", "/path/to/project",
    "--sync", "-q"
], check=True)

# Remote agent: Cleanup after task
subprocess.run([
    "python", "install_lsp.py",
    "--deactivate-all", "-q"
], check=True)
```

## Shared Package Handling

Some LSP servers share packages (e.g., html and css both use `vscode-langservers-extracted`).

The script handles this automatically:
- When uninstalling `html`, it checks if `css` still needs the package
- Only uninstalls the shared package when NEITHER language is needed
- Prevents breaking one language when cleaning up another

## Troubleshooting

### Agent Reports "Binary not found"

This is a GLOBAL issue - the orchestrator needs to install the binary:

```bash
# Orchestrator: Install missing binary globally
python install_lsp.py --install-binaries --languages {language}

# Verify binary is in PATH
echo $PATH
which {binary_name}
```

### Agent Has Wrong LSP Activated

This is a LOCAL issue - the agent needs to sync:

```bash
# Agent: Deactivate all, then sync fresh
python install_lsp.py --deactivate-all
python install_lsp.py --project-path /path/to/project --sync
```

### Activation State Corrupted

```bash
# Delete local state file and re-sync
rm -f /path/to/project/.claude/lsp-state.json
python install_lsp.py --project-path /path/to/project --sync
```

### Project Languages Changed (Branch Switch)

```bash
# Re-sync to detect new languages
python install_lsp.py --project-path . --sync
```

### Agent Started Without Activation

If agent is working without LSP (no type checking):

```bash
# Activate now
python install_lsp.py --project-path . --sync

# Verify activation
python install_lsp.py --status
```

## Best Practices

### For Orchestrator

1. **Install all binaries globally upfront**: Run `--install-binaries --all` once
2. **Never activate LSP locally**: Orchestrator doesn't write code
3. **Generate clear instructions**: Use `--generate-instructions` for each assignment
4. **Include cleanup step**: Always tell agents to `--deactivate-all` after work

### For Remote Agents

1. **Always sync before starting**: Run `--sync` to activate only needed LSP
2. **Verify activation**: Check `--status` shows correct languages activated
3. **Clean up after completion**: Run `--deactivate-all` before switching projects
4. **Report missing binaries**: If binary not found, ask orchestrator to install globally

### For Both

1. **One state file per project**: Located at `.claude/lsp-state.json`
2. **Never share activation state**: Each project manages its own activation
3. **Re-sync on branch switch**: Languages may change between branches

## Local State File

The activation state is stored at `<project>/.claude/lsp-state.json`:

```json
{
  "activated": ["python", "typescript"],
  "note": "LSP plugins activated for this project. Managed by install_lsp.py."
}
```

This file:
- Is local to each project
- Should be added to `.gitignore`
- Is managed automatically by `--activate`, `--deactivate`, and `--sync`

## Official Documentation

- [Claude Code LSP Servers](https://code.claude.com/docs/en/plugins-reference#lsp-servers)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins-reference)

## Supported Languages (13 total)

| Category | Languages |
|----------|-----------|
| **Core** | Python, TypeScript, Go, Rust |
| **JVM** | Java, Kotlin |
| **Systems** | C/C++, Objective-C, Swift, C# |
| **Web** | PHP, Ruby, HTML, CSS |

### Apple Platform Notes

- **Objective-C**: Uses `clangd` (same as C/C++). Install LLVM via brew/apt/choco.
- **Swift**: Uses `sourcekit-lsp` bundled with Xcode (macOS) or Swift toolchain (Linux).
  - macOS: `xcode-select --install`
  - Linux: Download Swift toolchain from swift.org
  - Cannot be uninstalled separately from Xcode/Swift toolchain
