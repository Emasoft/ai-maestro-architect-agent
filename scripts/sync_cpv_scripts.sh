#!/usr/bin/env bash
# Sync validation scripts from claude-plugins-validation (CPV) repo.
# Downloads latest scripts from Emasoft/claude-plugins-validation main branch.
# Preserves existing non-CPV scripts (amaa_*.py).
#
# Usage: bash scripts/sync_cpv_scripts.sh
# Requires: gh CLI authenticated

set -euo pipefail

REPO="Emasoft/claude-plugins-validation"
BRANCH="main"
REMOTE_DIR="scripts"
LOCAL_DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v gh &> /dev/null; then
    echo "ERROR: gh CLI not found. Install with: brew install gh"
    exit 1
fi

echo "Syncing validation scripts from $REPO ($BRANCH)..."

# List .py files in the remote scripts/ directory
FILES=$(gh api "repos/$REPO/contents/$REMOTE_DIR?ref=$BRANCH" --jq '.[] | select(.name | endswith(".py")) | .name' 2>/dev/null)

if [ -z "$FILES" ]; then
    echo "ERROR: Could not list files from $REPO/$REMOTE_DIR"
    exit 1
fi

UPDATED=0
FAILED=0

while IFS= read -r filename; do
    # Download raw content
    if gh api "repos/$REPO/contents/$REMOTE_DIR/$filename?ref=$BRANCH" --jq '.content' 2>/dev/null | base64 -d > "$LOCAL_DIR/$filename.tmp" 2>/dev/null; then
        mv "$LOCAL_DIR/$filename.tmp" "$LOCAL_DIR/$filename"
        UPDATED=$((UPDATED + 1))
    else
        rm -f "$LOCAL_DIR/$filename.tmp"
        FAILED=$((FAILED + 1))
        echo "  WARN: Failed to download $filename"
    fi
done <<< "$FILES"

echo "Sync complete: $UPDATED updated, $FAILED failed"
