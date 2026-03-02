# Bun GitHub Actions Reference Index

This document was split into two parts for easier navigation and maintainability.

## Part 1: CI and Publishing
**File**: [bun-github-actions-part1-ci-publish.md](./bun-github-actions-part1-ci-publish.md)

### Contents
1. **Basic CI Workflow** - Standard CI setup for Bun projects
2. **Matrix Builds** - Testing across multiple OS, Bun versions, and Node versions
3. **Caching Strategies** - Bun install cache, node_modules, build artifacts
4. **Artifact Management** - Upload/download artifacts between jobs
5. **Publish Workflow** - npm publishing with OIDC authentication
6. **Release Automation** - GitHub releases with changelog generation

---

## Part 2: Advanced Workflows
**File**: [bun-github-actions-part2-advanced.md](./bun-github-actions-part2-advanced.md)

### Contents
1. **Monorepo Workflows** - Path filters, Turborepo, Nx integration
2. **Security Scanning** - npm audit, CodeQL, Snyk, license compliance
3. **Docker Integration** - Build images, multi-stage Dockerfiles
4. **Pull Request Workflows** - PR checks, auto-labeling, auto-merge
5. **Required Permissions** - Permission configurations for different workflows
6. **Version Validation** - Tag validation, semver checks
7. **Troubleshooting** - Common issues and solutions
8. **Cross-References** - Related documents and decision trees

---

## Quick Navigation

| Task | Document |
|------|----------|
| Set up basic CI | [Part 1](./bun-github-actions-part1-ci-publish.md) (section: Basic CI Workflow) |
| Test on multiple platforms | [Part 1](./bun-github-actions-part1-ci-publish.md) (section: Matrix Builds) |
| Speed up builds with caching | [Part 1](./bun-github-actions-part1-ci-publish.md) (section: Caching Strategies) |
| Publish to npm | [Part 1](./bun-github-actions-part1-ci-publish.md) (section: Publish Workflow) |
| Create GitHub releases | [Part 1](./bun-github-actions-part1-ci-publish.md) (section: Release Automation) |
| Monorepo setup | [Part 2 Section 1](./bun-github-actions-part2-advanced-section1-monorepo.md) |
| Security audits | [Part 2 Section 2](./bun-github-actions-part2-advanced-section2-security.md) |
| Docker builds | [Part 2 Section 3](./bun-github-actions-part2-advanced-section3-docker.md) |
| PR automation | [Part 2 Section 4](./bun-github-actions-part2-advanced-section4-pr-workflows.md) |
| Fix common issues | [Part 2 Section 5](./bun-github-actions-part2-advanced-section5-permissions.md) (section: Troubleshooting) |

---

## Related Documents
- **[bun-npm-publishing.md](./bun-npm-publishing.md)** - Detailed npm publishing, OIDC, provenance
- **[bun-troubleshooting.md](./bun-troubleshooting.md)** - Common Bun issues and debugging
