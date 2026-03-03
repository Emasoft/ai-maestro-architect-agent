#!/usr/bin/env python3
"""Sync validation scripts from claude-plugins-validation (CPV) repo.

Downloads scripts from Emasoft/claude-plugins-validation at a pinned commit SHA.
Preserves existing non-CPV scripts (amaa_*.py).

SUPPLY CHAIN SECURITY: This script pins to a specific commit SHA to prevent
supply chain attacks via branch tampering. Do NOT replace PINNED_SHA with a
branch name.

To update the pinned SHA:
  1. Review the new commits:
     gh api repos/Emasoft/claude-plugins-validation/commits?per_page=10 --jq '.[].sha'
  2. After verifying the commits are safe, update PINNED_SHA below:
     gh api repos/Emasoft/claude-plugins-validation/git/ref/heads/master --jq '.object.sha'
  3. Run this script to sync.

Usage: python3 scripts/sync_cpv_scripts.py
Requires: gh CLI authenticated
Platform: cross-platform (macOS, Linux, Windows)
"""

import base64
import json
import subprocess
import sys
from pathlib import Path

REPO = "Emasoft/claude-plugins-validation"
# Pinned commit SHA for supply chain security (do not use branch names)
PINNED_SHA = "28140621ef92bbbdcb03a03fb90998de04289f69"
REMOTE_DIR = "scripts"
# Local directory is the same folder as this script
LOCAL_DIR = Path(__file__).parent.resolve()


def check_gh_cli() -> None:
    """Verify that the gh CLI is available on PATH."""
    result = subprocess.run(
        ["gh", "--version"],
        capture_output=True,
    )
    if result.returncode != 0:
        print("ERROR: gh CLI not found. Install with: brew install gh")
        sys.exit(1)


def list_remote_py_files() -> list[str]:
    """List .py files in the remote scripts/ directory at the pinned SHA."""
    result = subprocess.run(
        [
            "gh", "api",
            f"repos/{REPO}/contents/{REMOTE_DIR}?ref={PINNED_SHA}",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: Could not list files from {REPO}/{REMOTE_DIR}")
        print(result.stderr)
        sys.exit(1)

    entries = json.loads(result.stdout)
    return [entry["name"] for entry in entries if entry["name"].endswith(".py")]


def download_file(filename: str) -> bytes | None:
    """Download a single file from the remote repo and return its decoded bytes."""
    result = subprocess.run(
        [
            "gh", "api",
            f"repos/{REPO}/contents/{REMOTE_DIR}/{filename}?ref={PINNED_SHA}",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None

    data = json.loads(result.stdout)
    # GitHub API returns content as base64 with newlines; strip them before decoding
    encoded = data.get("content", "").replace("\n", "")
    if not encoded:
        return None

    return base64.b64decode(encoded)


def main() -> None:
    check_gh_cli()

    print(f"Syncing validation scripts from {REPO} (pinned: {PINNED_SHA[:12]})...")

    files = list_remote_py_files()
    if not files:
        print(f"ERROR: Could not list files from {REPO}/{REMOTE_DIR}")
        sys.exit(1)

    updated = 0
    failed = 0

    for filename in files:
        # Preserve existing amaa_*.py files (non-CPV scripts)
        if filename.startswith("amaa_"):
            continue

        content = download_file(filename)
        if content is None:
            failed += 1
            print(f"  WARN: Failed to download {filename}")
            continue

        # Write atomically via a temp file to avoid partial writes
        dest = LOCAL_DIR / filename
        tmp = LOCAL_DIR / (filename + ".tmp")
        tmp.write_bytes(content)
        tmp.replace(dest)
        updated += 1

    print(f"Sync complete: {updated} updated, {failed} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
