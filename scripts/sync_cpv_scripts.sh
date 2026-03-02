#!/usr/bin/env bash
# Sync validation scripts from claude-plugins-validation (CPV) repo.
# Downloads scripts from Emasoft/claude-plugins-validation at a pinned commit SHA.
# Preserves existing non-CPV scripts (amaa_*.py).
#
# SUPPLY CHAIN SECURITY: This script pins to a specific commit SHA to prevent
# supply chain attacks via branch tampering. Do NOT replace PINNED_SHA with a
# branch name.
#
# To update the pinned SHA:
#   1. Review the new commits:
#      gh api repos/Emasoft/claude-plugins-validation/commits?per_page=10 --jq '.[].sha'
#   2. After verifying the commits are safe, update PINNED_SHA below:
#      gh api repos/Emasoft/claude-plugins-validation/git/ref/heads/master --jq '.object.sha'
#   3. Run this script to sync.
#
# Usage: bash scripts/sync_cpv_scripts.sh
# Requires: gh CLI authenticated

set -euo pipefail

REPO="Emasoft/claude-plugins-validation"
# Pinned commit SHA for supply chain security (do not use branch names)
PINNED_SHA="246ce10a5261b7d490fd5a5dd40884ebc00e3f8f"
REMOTE_DIR="scripts"
LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v gh &> /dev/null; then
    echo "ERROR: gh CLI not found. Install with: brew install gh"
    exit 1
fi

echo "Syncing validation scripts from $REPO (pinned: ${PINNED_SHA:0:12})..."

# List .py files in the remote scripts/ directory at the pinned commit
FILES=$(gh api "repos/$REPO/contents/$REMOTE_DIR?ref=$PINNED_SHA" --jq '.[] | select(.name | endswith(".py")) | .name' 2>/dev/null)

if [ -z "$FILES" ]; then
    echo "ERROR: Could not list files from $REPO/$REMOTE_DIR"
    exit 1
fi

UPDATED=0
FAILED=0

while IFS= read -r filename; do
    # Download raw content
    if gh api "repos/$REPO/contents/$REMOTE_DIR/$filename?ref=$PINNED_SHA" --jq '.content' 2>/dev/null | base64 -d > "$LOCAL_DIR/$filename.tmp" 2>/dev/null; then
        mv "$LOCAL_DIR/$filename.tmp" "$LOCAL_DIR/$filename"
        UPDATED=$((UPDATED + 1))
    else
        rm -f "$LOCAL_DIR/$filename.tmp"
        FAILED=$((FAILED + 1))
        echo "  WARN: Failed to download $filename"
    fi
done <<< "$FILES"

echo "Sync complete: $UPDATED updated, $FAILED failed"
