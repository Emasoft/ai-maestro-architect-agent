# Bun Migration Checklist

A comprehensive checklist for migrating JavaScript/TypeScript projects to Bun as the main bundler, with npm trusted publishing via GitHub Actions OIDC.

**Based on**: SVG-MATRIX v1.2.0 migration (December 2025), SVG-BBOX v1.1.2 release validation (January 2026)

---

## Table of Contents
1. Pre-Migration
2. Configuration
3. Build Setup
4. Testing
5. CI/CD
6. Publishing
7. Verification

## Pre-Migration
- [ ] Install Bun locally
- [ ] Verify kernel version (Linux 5.6+)
- [ ] Backup existing build config

## Configuration
- [ ] Set "type": "module" in package.json
- [ ] Configure conditional exports
- [ ] Add browser field for legacy bundlers
- [ ] Set files allowlist
- [ ] Set engine requirements (node >= 24)

## Build Setup
- [ ] Create build.js script
- [ ] Configure entry points
- [ ] Set target (browser/node)
- [ ] Configure external modules
- [ ] Set minification options
- [ ] Test build output

## Testing
- [ ] Convert tests to bun:test format
- [ ] Add lifecycle hooks
- [ ] Configure coverage
- [ ] Test in both Node.js and browser

## CI/CD
- [ ] Pin Bun version in workflows
- [ ] Add registry-url to setup-node
- [ ] Set id-token permission
- [ ] Add version validation step

## Publishing
- [ ] Configure npm trusted publishing
- [ ] Use npm publish (NOT bun publish)
- [ ] Set --access public for scoped packages
- [ ] Create GitHub Release

## Verification
- [ ] Bundle sizes acceptable
- [ ] All tests pass
- [ ] Browser bundle works in browsers
- [ ] Node.js bundle works in Node.js
- [ ] CDN access works

---

## Related References

- **Troubleshooting**: See `bun-troubleshooting.md` (14 issues covered)
- **Build API**: See `bun-build-api.md` for Bun.build() configuration
- **GitHub Actions**: See `bun-github-actions.md` for CI/CD setup
- **npm Publishing**: See `bun-npm-publishing.md` for OIDC trusted publishing
