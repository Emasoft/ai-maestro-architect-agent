# Bun GitHub Actions: Advanced Workflows

## Table of Contents

This document covers advanced GitHub Actions workflows for Bun projects. Content is organized into sections for efficient loading.

**See also**: [Part 1 - CI and Publishing](./bun-github-actions-part1-ci-publish.md) for Basic CI, Matrix Builds, Caching, Artifacts, and Publishing.

---

## Section 1: Monorepo Workflows
**File**: [bun-github-actions-part2-advanced-section1-monorepo.md](./bun-github-actions-part2-advanced-section1-monorepo.md)

Contents:
- 1.1 Path Filters for Affected Packages
- 1.2 Parallel Jobs for Multiple Packages
- 1.3 Turborepo Integration
- 1.4 Nx Integration

**When to use**: When working with monorepos containing multiple packages or apps that need selective testing and building based on changed paths.

---

## Section 2: Security Scanning
**File**: [bun-github-actions-part2-advanced-section2-security.md](./bun-github-actions-part2-advanced-section2-security.md)

Contents:
- 2.1 npm audit
- 2.2 Dependency Review
- 2.3 CodeQL Analysis
- 2.4 Snyk Scanning
- 2.5 License Compliance

**When to use**: When implementing security checks for vulnerabilities, license compliance, or code quality scanning in CI pipelines.

---

## Section 3: Docker Integration
**File**: [bun-github-actions-part2-advanced-section3-docker.md](./bun-github-actions-part2-advanced-section3-docker.md)

Contents:
- 3.1 Build Docker Image with Bun
- 3.2 Multi-Stage Dockerfile for Bun
- 3.3 Docker Compose for Testing

**When to use**: When containerizing Bun applications for deployment or running tests in isolated Docker environments.

---

## Section 4: Pull Request Workflows
**File**: [bun-github-actions-part2-advanced-section4-pr-workflows.md](./bun-github-actions-part2-advanced-section4-pr-workflows.md)

Contents:
- 4.1 PR Checks and Validation
- 4.2 Auto-Labeling PRs
- 4.3 PR Size Validation
- 4.4 Auto-Merge Dependabot PRs
- 4.5 PR Comment with Test Results

**When to use**: When automating pull request validation, labeling, size checks, or implementing auto-merge for dependency updates.

---

## Section 5: Permissions and Validation
**File**: [bun-github-actions-part2-advanced-section5-permissions.md](./bun-github-actions-part2-advanced-section5-permissions.md)

Contents:
- 5.1 Required Permissions (CI, Publishing, Security, PR Automation)
- 5.2 Version Validation (Tag Matches, Semver, Version Increment)
- 5.3 Troubleshooting Common Issues
- 5.4 Cross-References and Decision Tree

**When to use**: When configuring workflow permissions, validating version tags, or debugging common GitHub Actions issues with Bun.

---

## Quick Reference: Workflow Decision Tree

1. **Simple project** → Use Basic CI Workflow (Part 1)
2. **Multi-platform support needed** → Add Matrix Builds (Part 1)
3. **Monorepo** → See Section 1: Monorepo Workflows
4. **Publishing to npm** → Follow Publish Workflow (Part 1) + bun-npm-publishing.md
5. **Security requirements** → See Section 2: Security Scanning
6. **Docker deployment** → See Section 3: Docker Integration
7. **Active PRs** → See Section 4: Pull Request Workflows
8. **Permission issues** → See Section 5: Permissions and Validation
