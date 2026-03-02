# Cross-Platform Build Automation


## Contents

- [Use Cases (Quick Reference)](#use-cases-quick-reference)
- [Overview](#overview)
- [Runner Matrix](#runner-matrix)
  - [Available GitHub-Hosted Runners](#available-github-hosted-runners)
  - [Free Tier Minutes](#free-tier-minutes)
- [Multi-Platform CI Workflow](#multi-platform-ci-workflow)
  - [Complete Matrix Build](#complete-matrix-build)
  - [Platform-Specific Jobs](#platform-specific-jobs)
    - [macOS with Code Signing](#macos-with-code-signing)
    - [Windows with Code Signing](#windows-with-code-signing)
    - [Linux with AppImage](#linux-with-appimage)
    - [Web with WASM](#web-with-wasm)
    - [Android with Gradle](#android-with-gradle)
- [Build Optimization](#build-optimization)
  - [Caching Strategies](#caching-strategies)
  - [Incremental Builds](#incremental-builds)
- [Checklist](#checklist)

---

## Use Cases (Quick Reference)

- When you need to choose runners for your target platforms → [Runner Matrix](#runner-matrix)
- When you need to check free tier minute limits → [Free Tier Minutes](#free-tier-minutes)
- When you need to configure a multi-platform CI workflow → [Multi-Platform CI Workflow](#multi-platform-ci-workflow)
- When you need to set up matrix builds with platform-specific configuration → [Complete Matrix Build](#complete-matrix-build)
- When you need to handle platform-specific build steps → [Platform-Specific Jobs](#platform-specific-jobs)
- When you need to optimize build times across platforms → [Build Optimization](#build-optimization)

## Overview

GitHub Actions provides hosted runners for all major platforms. This reference covers configuring cross-platform builds with proper matrix strategies.

## Runner Matrix

### Available GitHub-Hosted Runners

| Runner Label | OS | Architecture | vCPUs | RAM | Notes |
|--------------|----|----|-------|-----|-------|
| `ubuntu-latest` | Ubuntu 22.04 | x86_64 | 4 | 16GB | Most common, fastest startup |
| `ubuntu-24.04` | Ubuntu 24.04 | x86_64 | 4 | 16GB | Newer packages |
| `ubuntu-24.04-arm` | Ubuntu 24.04 | ARM64 | 4 | 16GB | ARM builds |
| `macos-14` | macOS 14 Sonoma | ARM64 (M1) | 3 | 14GB | Apple Silicon |
| `macos-13` | macOS 13 Ventura | x86_64 | 4 | 14GB | Intel Macs |
| `windows-latest` | Windows Server 2022 | x86_64 | 4 | 16GB | Windows builds |

### Free Tier Minutes

| Account | Linux | macOS | Windows |
|---------|-------|-------|---------|
| Free | 2000 min | 200 min | 2000 min |
| Pro | 3000 min | 300 min | 3000 min |
| Team | 3000 min | 300 min | 3000 min |

**Multipliers**: macOS = 10x, Windows = 2x Linux minutes.

## Multi-Platform CI Workflow

### Complete Matrix Build

```yaml
name: Cross-Platform CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  CARGO_TERM_COLOR: always
  RUST_BACKTRACE: 1

jobs:
  # Stage 1: Quick checks (Linux only)
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt

      - name: Cache cargo
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/bin/
            ~/.cargo/registry/
            ~/.cargo/git/
            target/
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Check formatting
        run: cargo fmt --all -- --check

      - name: Clippy
        run: cargo clippy --all-targets --all-features -- -D warnings

  # Stage 2: Test matrix
  test:
    name: Test ${{ matrix.os }}
    needs: lint
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            artifact: linux-x64
          - os: macos-14
            target: aarch64-apple-darwin
            artifact: macos-arm64
          - os: macos-13
            target: x86_64-apple-darwin
            artifact: macos-x64
          - os: windows-latest
            target: x86_64-pc-windows-msvc
            artifact: windows-x64

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.target }}

      - name: Cache cargo
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/bin/
            ~/.cargo/registry/
            ~/.cargo/git/
            target/
          key: ${{ runner.os }}-${{ matrix.target }}-cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Run tests
        run: cargo test --target ${{ matrix.target }} --all-features

      - name: Run doctests
        run: cargo test --doc --target ${{ matrix.target }}

  # Stage 3: Build artifacts
  build:
    name: Build ${{ matrix.artifact }}
    needs: test
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            artifact: linux-x64
            extension: ""
          - os: ubuntu-24.04-arm
            target: aarch64-unknown-linux-gnu
            artifact: linux-arm64
            extension: ""
          - os: macos-14
            target: aarch64-apple-darwin
            artifact: macos-arm64
            extension: ""
          - os: macos-13
            target: x86_64-apple-darwin
            artifact: macos-x64
            extension: ""
          - os: windows-latest
            target: x86_64-pc-windows-msvc
            artifact: windows-x64
            extension: ".exe"

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.target }}

      - name: Build release
        run: cargo build --release --target ${{ matrix.target }}

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: myapp-${{ matrix.artifact }}
          path: target/${{ matrix.target }}/release/myapp${{ matrix.extension }}
          retention-days: 7
```

### Platform-Specific Jobs

#### macOS with Code Signing

```yaml
build-macos:
  name: Build macOS
  runs-on: macos-14
  steps:
    - uses: actions/checkout@v4

    - name: Import certificates
      env:
        CERTIFICATE_P12: ${{ secrets.APPLE_CERTIFICATE }}
        CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
      run: |
        echo "$CERTIFICATE_P12" | base64 --decode > certificate.p12

        security create-keychain -p "" build.keychain
        security default-keychain -s build.keychain
        security unlock-keychain -p "" build.keychain

        security import certificate.p12 \
          -k build.keychain \
          -P "$CERTIFICATE_PASSWORD" \
          -T /usr/bin/codesign \
          -T /usr/bin/security

        security set-key-partition-list -S apple-tool:,apple: -s -k "" build.keychain

    - name: Build and sign
      run: |
        xcodebuild -scheme MyApp \
          -configuration Release \
          -archivePath MyApp.xcarchive \
          archive

        xcodebuild -exportArchive \
          -archivePath MyApp.xcarchive \
          -exportOptionsPlist ExportOptions.plist \
          -exportPath export/

    - name: Notarize
      env:
        APPLE_ID: ${{ secrets.APPLE_ID }}
        NOTARIZATION_PASSWORD: ${{ secrets.NOTARIZATION_PASSWORD }}
        TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
      run: |
        xcrun notarytool submit export/MyApp.dmg \
          --apple-id "$APPLE_ID" \
          --password "$NOTARIZATION_PASSWORD" \
          --team-id "$TEAM_ID" \
          --wait

        xcrun stapler staple export/MyApp.dmg

    - name: Upload
      uses: actions/upload-artifact@v4
      with:
        name: macos-app
        path: export/MyApp.dmg
```

#### Windows with Code Signing

```yaml
build-windows:
  name: Build Windows
  runs-on: windows-latest
  steps:
    - uses: actions/checkout@v4

    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: '8.0.x'

    - name: Build
      run: |
        dotnet restore
        dotnet build -c Release
        dotnet publish -c Release -r win-x64 --self-contained -o publish/

    - name: Code sign
      env:
        CERTIFICATE: ${{ secrets.WINDOWS_CERTIFICATE }}
        CERTIFICATE_PASSWORD: ${{ secrets.WINDOWS_CERTIFICATE_PASSWORD }}
      shell: powershell
      run: |
        $certBytes = [Convert]::FromBase64String($env:CERTIFICATE)
        [IO.File]::WriteAllBytes("certificate.pfx", $certBytes)

        $cert = Get-PfxCertificate -FilePath certificate.pfx `
          -Password (ConvertTo-SecureString $env:CERTIFICATE_PASSWORD -AsPlainText -Force)

        Get-ChildItem publish/*.exe | ForEach-Object {
          Set-AuthenticodeSignature -FilePath $_.FullName `
            -Certificate $cert `
            -TimestampServer "http://timestamp.digicert.com"
        }

        Remove-Item certificate.pfx

    - name: Create installer
      run: |
        choco install innosetup
        iscc installer.iss

    - name: Upload
      uses: actions/upload-artifact@v4
      with:
        name: windows-installer
        path: Output/MyApp-Setup.exe
```

#### Linux with AppImage

```yaml
build-linux:
  name: Build Linux
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libgtk-3-dev libwebkit2gtk-4.0-dev

    - name: Setup Rust
      uses: dtolnay/rust-toolchain@stable

    - name: Build
      run: cargo build --release

    - name: Create AppImage
      run: |
        wget -q https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
        chmod +x linuxdeploy-x86_64.AppImage

        mkdir -p AppDir/usr/bin AppDir/usr/share/applications AppDir/usr/share/icons/hicolor/256x256/apps

        cp target/release/myapp AppDir/usr/bin/
        cp assets/myapp.desktop AppDir/usr/share/applications/
        cp assets/icon.png AppDir/usr/share/icons/hicolor/256x256/apps/myapp.png

        ./linuxdeploy-x86_64.AppImage \
          --appdir AppDir \
          --output appimage \
          --desktop-file assets/myapp.desktop

    - name: Upload
      uses: actions/upload-artifact@v4
      with:
        name: linux-appimage
        path: MyApp-*.AppImage
```

#### Web with WASM

```yaml
build-web:
  name: Build Web
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Setup Rust
      uses: dtolnay/rust-toolchain@stable
      with:
        targets: wasm32-unknown-unknown

    - name: Install wasm-pack
      run: curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Setup pnpm
      uses: pnpm/action-setup@v2
      with:
        version: 8

    - name: Build WASM
      run: |
        wasm-pack build --target web --release
        wasm-opt -O3 pkg/myapp_bg.wasm -o pkg/myapp_bg.wasm

    - name: Build frontend
      working-directory: web
      run: |
        pnpm install
        pnpm run build

    - name: Upload
      uses: actions/upload-artifact@v4
      with:
        name: web-dist
        path: web/dist/
```

#### Android with Gradle

```yaml
build-android:
  name: Build Android
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Setup JDK
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Setup Android SDK
      uses: android-actions/setup-android@v3

    - name: Setup Gradle
      uses: gradle/actions/setup-gradle@v3

    - name: Build debug APK
      working-directory: android
      run: ./gradlew assembleDebug

    - name: Build release AAB
      working-directory: android
      env:
        KEYSTORE_BASE64: ${{ secrets.ANDROID_KEYSTORE }}
        KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
        KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      run: |
        echo "$KEYSTORE_BASE64" | base64 --decode > release.keystore
        ./gradlew bundleRelease
        rm release.keystore

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: android-debug-apk
        path: android/app/build/outputs/apk/debug/app-debug.apk

    - name: Upload AAB
      uses: actions/upload-artifact@v4
      with:
        name: android-release-aab
        path: android/app/build/outputs/bundle/release/app-release.aab
```

## Build Optimization

### Caching Strategies

```yaml
# Rust caching
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin/
      ~/.cargo/registry/index/
      ~/.cargo/registry/cache/
      ~/.cargo/git/db/
      target/
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-cargo-

# Node.js caching (with pnpm)
- uses: actions/cache@v4
  with:
    path: ~/.pnpm-store
    key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-pnpm-

# Gradle caching
- uses: gradle/actions/setup-gradle@v3
  with:
    cache-read-only: ${{ github.ref != 'refs/heads/main' }}

# Python caching
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### Incremental Builds

```yaml
# Use sccache for Rust
- name: Setup sccache
  uses: mozilla-actions/sccache-action@v0.0.4

- name: Build with sccache
  env:
    RUSTC_WRAPPER: sccache
    SCCACHE_GHA_ENABLED: true
  run: cargo build --release
```

## Checklist

- [ ] Matrix includes all target platforms
- [ ] Caching configured for each toolchain
- [ ] Code signing set up for macOS/Windows
- [ ] Artifacts named consistently
- [ ] Fail-fast disabled for better error visibility
- [ ] Concurrency prevents duplicate runs
- [ ] Free tier minutes considered
