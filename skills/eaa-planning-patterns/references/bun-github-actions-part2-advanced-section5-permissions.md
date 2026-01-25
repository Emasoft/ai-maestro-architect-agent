# Bun GitHub Actions: Permissions and Validation

**Parent document**: [bun-github-actions-part2-advanced.md](./bun-github-actions-part2-advanced.md)

---

## Table of Contents
- 5.1 [Required Permissions](#required-permissions)
- 5.2 [Version Validation](#version-validation)
- 5.3 [Troubleshooting](#troubleshooting)
- 5.4 [Cross-References](#cross-references)

---

## Required Permissions

### Minimal Permissions for CI
```yaml
permissions:
  contents: read  # Read repository
```

### Permissions for Publishing
```yaml
permissions:
  contents: write      # Create releases
  id-token: write      # npm OIDC authentication
```

### Permissions for Security Scanning
```yaml
permissions:
  contents: read
  security-events: write  # CodeQL
  pull-requests: write    # Dependency review comments
```

### Permissions for PR Automation
```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
```

---

## Version Validation

### Validate Tag Matches package.json
```yaml
- name: Validate version
  run: |
    TAG="${GITHUB_REF#refs/tags/v}"
    PKG=$(node -p "require('./package.json').version")
    [ "$TAG" = "$PKG" ] || exit 1
```

### Validate Semantic Versioning
```yaml
- name: Validate semver
  run: |
    TAG="${GITHUB_REF#refs/tags/v}"
    if ! echo "$TAG" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'; then
      echo "Invalid semver: $TAG"
      exit 1
    fi
```

### Check Version Increment
```yaml
- name: Check version bump
  run: |
    git fetch --tags
    LATEST_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "v0.0.0")
    CURRENT_TAG="${GITHUB_REF#refs/tags/}"

    bunx semver $CURRENT_TAG -r ">$LATEST_TAG" || {
      echo "Version $CURRENT_TAG is not greater than $LATEST_TAG"
      exit 1
    }
```

---

## Troubleshooting

### Missing registry-url causes OIDC to fail silently or hang
If `registry-url: 'https://registry.npmjs.org'` is missing from the `actions/setup-node@v4` step, OIDC authentication will fail silently. The publish command may hang indefinitely or exit with unclear error messages. Always include this configuration when using OIDC for npm publishing.

### bun publish does not support OIDC
The `bun publish` command does not support npm's OIDC authentication mechanism. Always use `npm publish` instead, even in Bun-based projects. The setup-node action configures the npm authentication token correctly.

### Cache not restoring on Windows
Windows paths are case-insensitive but cache keys are case-sensitive. Ensure cache paths use consistent casing. Use `~` instead of `$HOME` for cross-platform compatibility.

### Matrix builds failing on specific OS
Some Bun features may not work identically across operating systems. Use `if: runner.os == 'ubuntu-latest'` to skip OS-specific steps. Check Bun's platform support matrix.

### Artifacts not found in dependent jobs
Ensure the artifact name matches exactly between upload and download steps. Artifacts are scoped to the workflow run, not across workflows.

### Docker build fails to find Bun
Use official `oven/bun` Docker images instead of manually installing Bun in Dockerfiles. The official images include all necessary dependencies.

### Dependabot PRs fail security checks
Dependabot may create PRs that introduce vulnerabilities. Always run security audits in PR checks before auto-merging.

### CodeQL analysis times out
CodeQL can be slow on large codebases. Use matrix builds to analyze different languages separately, or increase the timeout with `timeout-minutes: 30`.

---

## Cross-References

### Related Documents
- **[bun-npm-publishing.md](./bun-npm-publishing.md)** - Detailed npm publishing workflows, OIDC setup, provenance, version management
- **[bun-troubleshooting.md](./bun-troubleshooting.md)** - Common Bun issues, debugging techniques, error resolution

### Workflow Decision Tree
1. **Simple project** → Use Basic CI Workflow (Part 1)
2. **Multi-platform support needed** → Add Matrix Builds (Part 1)
3. **Monorepo** → Implement Monorepo Workflows (Section 1)
4. **Publishing to npm** → Follow Publish Workflow (Part 1) + bun-npm-publishing.md
5. **Security requirements** → Add Security Scanning (Section 2)
6. **Docker deployment** → Implement Docker Integration (Section 3)
7. **Active PRs** → Configure Pull Request Workflows (Section 4)

### Best Practices
- Always cache Bun dependencies and node_modules
- Use matrix builds to test across platforms early
- Enable security scanning for all public packages
- Implement version validation before publishing
- Use artifact management for build outputs
- Configure auto-merge only after successful tests
- Keep workflow files DRY with composite actions
