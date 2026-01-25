# Bun Installation and Setup

## Table of Contents
1. Platform Installation
2. Version Requirements
3. Verification
4. Troubleshooting

## Platform Installation

### macOS/Linux
```bash
curl -fsSL https://bun.com/install | bash
```

### Windows
```powershell
powershell -c "irm bun.sh/install.ps1 | iex"
```

### Alternative Methods

```bash
# npm (all platforms)
npm install -g bun

# Homebrew (macOS)
brew install bun

# Scoop (Windows)
scoop install bun
```

**Note:** Linux requires `unzip` package and kernel 5.6+ (minimum 5.1).

## Version Requirements
| Tool | Minimum | Recommended |
|------|---------|-------------|
| Bun | 1.1.0 | 1.1.42+ |
| Node.js | 24.0.0 | 24.x |
| npm | 11.5.0 | 11.6.2+ |

Note: npm OIDC requires npm >= 11.5.0 (Node.js 24)

## Verification
```bash
bun --version
```

## CI/CD Setup
Always pin bun version in CI:
```yaml
- uses: oven-sh/setup-bun@v2
  with:
    bun-version: '1.1.42'
```

## Troubleshooting

### Installation Fails on Linux
**Problem**: Installation script fails with permission errors or missing dependencies.

**Solution**:
- Ensure you have `unzip` installed: `sudo apt-get install unzip` (Debian/Ubuntu) or `sudo yum install unzip` (RHEL/CentOS)
- Check kernel version: `uname -r` (must be 5.6 or higher)
- Try installing with sudo if permission denied: `curl -fsSL https://bun.com/install | sudo bash`

### Bun Command Not Found After Installation
**Problem**: Terminal doesn't recognize `bun` command after installation.

**Solution**:
- Reload your shell configuration: `source ~/.bashrc` or `source ~/.zshrc`
- Verify PATH includes Bun: `echo $PATH | grep bun`
- Manually add to PATH if needed: `export PATH="$HOME/.bun/bin:$PATH"`

### Version Mismatch in CI/CD
**Problem**: CI/CD uses different Bun version than expected.

**Solution**:
- Always pin the exact version in your workflow files
- Don't use `latest` or version ranges
- Update `.tool-versions` or `.node-version` files if using version managers

### Windows PowerShell Execution Policy Error
**Problem**: PowerShell blocks installation script execution.

**Solution**:
- Run PowerShell as Administrator
- Temporarily allow script execution: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- After installation, restore policy: `Set-ExecutionPolicy Restricted -Scope CurrentUser`

### npm Global Install Conflicts
**Problem**: Installing Bun via npm conflicts with existing installation.

**Solution**:
- Uninstall previous Bun installations first
- Use the official installer instead of npm when possible
- Check for conflicting installations: `which -a bun` (macOS/Linux) or `where bun` (Windows)
