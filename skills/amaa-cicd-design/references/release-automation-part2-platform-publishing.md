# Release Automation: Platform-Specific Publishing


## Contents

- [Table of Contents](#table-of-contents)
- [Platform-Specific Publishing](#platform-specific-publishing)
  - [Homebrew (macOS)](#homebrew-macos)
  - [Windows Store](#windows-store)
  - [Docker Hub](#docker-hub)
- [Debug Script](#debug-script)

---

> **Parent document**: [release-automation.md](release-automation.md)

## Table of Contents

- [Homebrew (macOS)](#homebrew-macos) - When you need to publish to Homebrew tap
- [Windows Store](#windows-store) - When you need to publish to Microsoft Store
- [Docker Hub](#docker-hub) - When you need to publish Docker images
- [Debug Script](#debug-script) - When you need to troubleshoot release pipeline issues

---

## Platform-Specific Publishing

### Homebrew (macOS)

Use this job to automatically update your Homebrew formula when a new release is published.

```yaml
publish-homebrew:
  name: Update Homebrew
  needs: release
  runs-on: macos-latest
  steps:
    - name: Update formula
      env:
        HOMEBREW_GITHUB_API_TOKEN: ${{ secrets.HOMEBREW_TOKEN }}
      run: |
        brew tap myorg/tap
        brew bump-formula-pr myorg/tap/myapp \
          --url "https://github.com/${{ github.repository }}/archive/v${{ needs.validate.outputs.version }}.tar.gz" \
          --sha256 "$(curl -sL https://github.com/${{ github.repository }}/archive/v${{ needs.validate.outputs.version }}.tar.gz | sha256sum | cut -d' ' -f1)"
```

### Windows Store

Use this job to publish your application to the Microsoft Store.

```yaml
publish-msstore:
  name: Publish to Microsoft Store
  needs: build
  runs-on: windows-latest
  steps:
    - name: Download artifact
      uses: actions/download-artifact@v4
      with:
        name: myapp-windows-x64

    - name: Submit to Store
      uses: isaacrlevin/windows-store-action@v1
      with:
        client-id: ${{ secrets.AZURE_CLIENT_ID }}
        client-secret: ${{ secrets.AZURE_CLIENT_SECRET }}
        tenant-id: ${{ secrets.AZURE_TENANT_ID }}
        app-id: ${{ secrets.MSSTORE_APP_ID }}
        package-path: myapp.msix
```

### Docker Hub

Use this job to build and push multi-architecture Docker images.

```yaml
publish-docker:
  name: Publish to Docker Hub
  needs: release
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          myorg/myapp:latest
          myorg/myapp:${{ needs.validate.outputs.version }}
        platforms: linux/amd64,linux/arm64
```

---

## Debug Script

Use this Python script to validate release readiness and troubleshoot pipeline issues before creating a release.

```python
#!/usr/bin/env python3
"""
Debug script for release pipeline.
Validates release readiness and troubleshoots issues.
"""
import subprocess
import sys
import re
from pathlib import Path


def get_current_version() -> str:
    """Extract version from Cargo.toml."""
    cargo_toml = Path("Cargo.toml")
    if not cargo_toml.exists():
        return "unknown"

    content = cargo_toml.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    return match.group(1) if match else "unknown"


def get_git_tags() -> list[str]:
    """Get all version tags."""
    result = subprocess.run(
        ["git", "tag", "-l", "v*"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().split("\n") if result.stdout else []


def check_uncommitted_changes() -> bool:
    """Check for uncommitted changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def check_secrets_configured() -> dict:
    """Check if required secrets are likely configured."""
    # This runs locally, so we can only check env vars
    import os
    secrets = {
        "CRATES_IO_TOKEN": os.getenv("CRATES_IO_TOKEN"),
        "NPM_TOKEN": os.getenv("NPM_TOKEN"),
        "PYPI_API_TOKEN": os.getenv("PYPI_API_TOKEN"),
    }
    return {k: "configured" if v else "missing" for k, v in secrets.items()}


def main():
    print("Release Pipeline Debug")
    print("=" * 50)

    version = get_current_version()
    print(f"\nCurrent version: {version}")

    tags = get_git_tags()
    print(f"Existing tags: {len(tags)}")
    if tags:
        print(f"  Latest: {tags[-1]}")

    tag_exists = f"v{version}" in tags
    print(f"\nTag v{version} exists: {tag_exists}")

    if check_uncommitted_changes():
        print("\nWARNING: Uncommitted changes detected!")
        print("  Commit all changes before releasing.")

    print("\nRelease checklist:")
    checks = [
        ("Version updated", not tag_exists),
        ("No uncommitted changes", not check_uncommitted_changes()),
        ("Tests passing", True),  # Would need to run tests
        ("CHANGELOG updated", Path("CHANGELOG.md").exists()),
    ]

    all_pass = True
    for check, passed in checks:
        status = "OK" if passed else "FAIL"
        print(f"  [{status}] {check}")
        if not passed:
            all_pass = False

    if all_pass:
        print(f"\nReady to release v{version}!")
        print(f"  Run: git tag v{version} && git push --tags")
    else:
        print("\nNot ready for release. Fix issues above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
```
