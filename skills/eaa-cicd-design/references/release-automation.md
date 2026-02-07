# Release Automation


## Contents

- [Use Cases (Quick Reference)](#use-cases-quick-reference)
- [Overview](#overview)
- [Part Files](#part-files)
  - [Complete Release Workflow](#complete-release-workflow)
  - [Platform-Specific Publishing](#platform-specific-publishing)
- [Release Pipeline Stages](#release-pipeline-stages)
- [Semantic Versioning](#semantic-versioning)
  - [Version Format](#version-format)
  - [When to Bump](#when-to-bump)
- [Version Bumping Automation](#version-bumping-automation)
  - [Automated Version Bump PR](#automated-version-bump-pr)
- [Changelog Generation](#changelog-generation)
  - [Conventional Commits](#conventional-commits)
- [Checklist](#checklist)

---

## Use Cases (Quick Reference)

- When you need to understand the release workflow stages → [Release Pipeline Stages](#release-pipeline-stages)
- When you need to implement semantic versioning → [Semantic Versioning](#semantic-versioning)
- When you need to automatically bump versions → [Version Bumping Automation](#version-bumping-automation)
- When you need to generate changelogs → [Changelog Generation](#changelog-generation)
- When you need to create a complete release workflow → [Complete Release Workflow](release-automation-part1-complete-workflow.md)
- When you need to publish to package registries → [Complete Release Workflow](release-automation-part1-complete-workflow.md)
- When you need platform-specific publishing (Homebrew, Windows Store, Docker) → [Platform-Specific Publishing](release-automation-part2-platform-publishing.md)
- When you need to debug release pipeline issues → [Debug Script](release-automation-part2-platform-publishing.md) (section: Debug Script)

## Overview

Automated release pipelines ensure consistent, reproducible releases across all platforms. This reference covers the complete release workflow from version bumping to publishing.

---

## Part Files

### Complete Release Workflow

**File**: [release-automation-part1-complete-workflow.md](release-automation-part1-complete-workflow.md)

Tag-Triggered Release - When you need a complete tag-triggered CI/CD release pipeline:
- Stage 1: Validate - Validate tag and extract version
- Stage 2: Test - Run full test suite across platforms
- Stage 3: Build - Build release binaries for all platforms
- Stage 4: Build Installers - Create installers and checksums
- Stage 5: Create Release - Create GitHub Release with assets
- Stage 6: Publish - Publish to package registries (crates.io, npm, PyPI)

See [release-automation-part1-complete-workflow.md](release-automation-part1-complete-workflow.md) for full details.

### Platform-Specific Publishing

**File**: [release-automation-part2-platform-publishing.md](release-automation-part2-platform-publishing.md)

- Homebrew (macOS) - When you need to publish to Homebrew tap
- Windows Store - When you need to publish to Microsoft Store
- Docker Hub - When you need to publish Docker images
- Debug Script - When you need to troubleshoot release pipeline issues

See [release-automation-part2-platform-publishing.md](release-automation-part2-platform-publishing.md) for full details.

---

## Release Pipeline Stages

```
1. Version Bump        → Update version in manifests
2. Changelog           → Generate from commits
3. Build Matrix        → Compile for all platforms
4. Testing             → Final verification
5. Code Signing        → Sign binaries
6. Artifact Creation   → Package for distribution
7. GitHub Release      → Create release with assets
8. Package Publishing  → npm, PyPI, crates.io, etc.
9. Notifications       → Announce release
```

## Semantic Versioning

### Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
  1.0.0           # Stable release
  1.0.0-alpha.1   # Pre-release
  1.0.0-beta.2    # Beta release
  1.0.0-rc.1      # Release candidate
  2.0.0           # Breaking changes
```

### When to Bump

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking API change | MAJOR | Remove public function |
| New feature (backward compatible) | MINOR | Add new endpoint |
| Bug fix | PATCH | Fix calculation error |
| Pre-release | PRERELEASE | Alpha testing |

## Version Bumping Automation

### Automated Version Bump PR

```yaml
name: Version Bump

on:
  workflow_dispatch:
    inputs:
      bump:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    name: Bump Version
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Install cargo-edit
        run: cargo install cargo-edit

      - name: Bump version
        id: bump
        run: |
          cargo set-version --bump ${{ github.event.inputs.bump }}
          NEW_VERSION=$(grep '^version' Cargo.toml | head -1 | sed 's/.*"\(.*\)".*/\1/')
          echo "version=$NEW_VERSION" >> $GITHUB_OUTPUT

      - name: Create PR
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: "chore: bump version to ${{ steps.bump.outputs.version }}"
          title: "Release v${{ steps.bump.outputs.version }}"
          body: |
            ## Release v${{ steps.bump.outputs.version }}

            This PR bumps the version for the next release.

            ### Checklist
            - [ ] CHANGELOG updated
            - [ ] Documentation updated
            - [ ] Breaking changes documented (if major)
          branch: release/v${{ steps.bump.outputs.version }}
          base: main
```

## Changelog Generation

### Conventional Commits

```yaml
# Generate changelog from conventional commits
- name: Generate Changelog
  uses: orhun/git-cliff-action@v2
  with:
    config: cliff.toml
    args: --verbose
  env:
    OUTPUT: CHANGELOG.md
```

**cliff.toml**:
```toml
[changelog]
header = """
# Changelog\n
"""
body = """
{% for group, commits in commits | group_by(attribute="group") %}
    ## {{ group | upper_first }}
    {% for commit in commits %}
        - {{ commit.message | upper_first }} ({{ commit.id | truncate(length=7, end="") }})\
    {% endfor %}
{% endfor %}\n
"""
footer = ""

[git]
conventional_commits = true
filter_unconventional = true
commit_parsers = [
    { message = "^feat", group = "Features" },
    { message = "^fix", group = "Bug Fixes" },
    { message = "^doc", group = "Documentation" },
    { message = "^perf", group = "Performance" },
    { message = "^refactor", group = "Refactor" },
    { message = "^style", group = "Styling" },
    { message = "^test", group = "Testing" },
    { message = "^chore\\(release\\)", skip = true },
    { message = "^chore", group = "Miscellaneous" },
]
```

## Checklist

- [ ] Semantic versioning followed
- [ ] Version matches across all manifests
- [ ] Tests pass before release build
- [ ] All platform builds succeed
- [ ] Code signing configured
- [ ] Changelog generated
- [ ] GitHub Release created with assets
- [ ] Package registries updated
- [ ] Homebrew/package managers updated
- [ ] Docker images pushed
- [ ] Release announcement sent
