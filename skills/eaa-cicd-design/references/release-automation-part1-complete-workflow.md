# Release Automation: Complete Release Workflow


## Contents

- [Table of Contents](#table-of-contents)
- [Tag-Triggered Release](#tag-triggered-release)

---

> **Parent document**: [release-automation.md](release-automation.md)

## Table of Contents

- [Tag-Triggered Release](#tag-triggered-release) - When you need a complete tag-triggered CI/CD release pipeline
  - [Stage 1: Validate](#stage-1-validate) - Validate tag and extract version
  - [Stage 2: Test](#stage-2-test) - Run full test suite across platforms
  - [Stage 3: Build](#stage-3-build) - Build release binaries for all platforms
  - [Stage 4: Build Installers](#stage-4-build-installers) - Create installers and checksums
  - [Stage 5: Create Release](#stage-5-create-release) - Create GitHub Release with assets
  - [Stage 6: Publish](#stage-6-publish) - Publish to package registries (crates.io, npm, PyPI)

---

## Tag-Triggered Release

This workflow demonstrates a complete release pipeline triggered by version tags. It includes validation, testing, cross-platform builds, and publishing to multiple package registries.

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  packages: write

env:
  CARGO_TERM_COLOR: always

jobs:
  # Stage 1: Validate tag and extract version
  validate:
    name: Validate Release
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
      prerelease: ${{ steps.version.outputs.prerelease }}
    steps:
      - uses: actions/checkout@v4

      - name: Extract version
        id: version
        run: |
          TAG="${GITHUB_REF#refs/tags/v}"
          echo "version=$TAG" >> $GITHUB_OUTPUT

          if [[ "$TAG" == *"-"* ]]; then
            echo "prerelease=true" >> $GITHUB_OUTPUT
          else
            echo "prerelease=false" >> $GITHUB_OUTPUT
          fi

      - name: Verify version matches Cargo.toml
        run: |
          CARGO_VERSION=$(grep '^version' Cargo.toml | head -1 | sed 's/.*"\(.*\)".*/\1/')
          if [[ "$CARGO_VERSION" != "${{ steps.version.outputs.version }}" ]]; then
            echo "Version mismatch: tag=${{ steps.version.outputs.version }}, Cargo.toml=$CARGO_VERSION"
            exit 1
          fi

  # Stage 2: Run full test suite
  test:
    name: Test
    needs: validate
    strategy:
      fail-fast: true
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - name: Run tests
        run: cargo test --all-features --release

  # Stage 3: Build release binaries
  build:
    name: Build ${{ matrix.artifact }}
    needs: test
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            artifact: linux-x64
            ext: ""
          - os: ubuntu-24.04-arm
            target: aarch64-unknown-linux-gnu
            artifact: linux-arm64
            ext: ""
          - os: macos-14
            target: aarch64-apple-darwin
            artifact: macos-arm64
            ext: ""
          - os: macos-13
            target: x86_64-apple-darwin
            artifact: macos-x64
            ext: ""
          - os: windows-latest
            target: x86_64-pc-windows-msvc
            artifact: windows-x64
            ext: ".exe"

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.target }}

      - name: Build
        run: cargo build --release --target ${{ matrix.target }}

      - name: Package (Unix)
        if: runner.os != 'Windows'
        run: |
          mkdir -p dist
          cp target/${{ matrix.target }}/release/myapp${{ matrix.ext }} dist/
          cd dist
          tar -czvf myapp-${{ needs.validate.outputs.version }}-${{ matrix.artifact }}.tar.gz myapp${{ matrix.ext }}

      - name: Package (Windows)
        if: runner.os == 'Windows'
        run: |
          mkdir dist
          cp target/${{ matrix.target }}/release/myapp${{ matrix.ext }} dist/
          cd dist
          7z a myapp-${{ needs.validate.outputs.version }}-${{ matrix.artifact }}.zip myapp${{ matrix.ext }}

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: myapp-${{ matrix.artifact }}
          path: dist/myapp-*

  # Stage 4: Build platform installers
  build-installers:
    name: Build Installers
    needs: [validate, build]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/

      - name: Create checksums
        run: |
          cd artifacts
          find . -type f \( -name "*.tar.gz" -o -name "*.zip" \) -exec sha256sum {} \; > checksums.sha256

      - name: Upload checksums
        uses: actions/upload-artifact@v4
        with:
          name: checksums
          path: artifacts/checksums.sha256

  # Stage 5: Create GitHub Release
  release:
    name: Create Release
    needs: [validate, build, build-installers]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/

      - name: Generate changelog
        id: changelog
        run: |
          # Get previous tag
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")

          if [[ -n "$PREV_TAG" ]]; then
            echo "## Changes since $PREV_TAG" > CHANGELOG.md
            echo "" >> CHANGELOG.md
            git log --pretty=format:"- %s (%h)" "$PREV_TAG"..HEAD >> CHANGELOG.md
          else
            echo "## Initial Release" > CHANGELOG.md
          fi

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          name: v${{ needs.validate.outputs.version }}
          body_path: CHANGELOG.md
          draft: false
          prerelease: ${{ needs.validate.outputs.prerelease }}
          files: |
            artifacts/**/*.tar.gz
            artifacts/**/*.zip
            artifacts/**/checksums.sha256
          generate_release_notes: true

  # Stage 6: Publish to package registries
  publish-crates:
    name: Publish to crates.io
    needs: [validate, release]
    if: needs.validate.outputs.prerelease == 'false'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - name: Publish
        run: cargo publish --token ${{ secrets.CRATES_IO_TOKEN }}

  publish-npm:
    name: Publish to npm
    needs: [validate, release]
    if: needs.validate.outputs.prerelease == 'false'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - name: Publish
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

  publish-pypi:
    name: Publish to PyPI
    needs: [validate, release]
    if: needs.validate.outputs.prerelease == 'false'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Build and publish
        run: |
          pip install build twine
          python -m build
          twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```
