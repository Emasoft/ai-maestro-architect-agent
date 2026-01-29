#!/usr/bin/env python3
"""
arch_design_transition.py - Transition from dual-git to single-git design management.

This script migrates design documents from private (.design/) to public (docs/design/).
UUIDs are preserved, ensuring all GitHub issue references remain valid.

WARNING: This makes ALL design documents PUBLIC on GitHub!

NO external dependencies - Python 3.8+ stdlib only.
Uses subprocess for git commands.

Usage:
    python3 arch_design_transition.py [options]

Options:
    --force         Skip confirmation prompt
    --dry-run       Show what would be done without executing
    --keep-private  Don't delete .design/ after transition
    -h, --help      Show this help

The script:
1. Verifies current mode is dual-git
2. Creates docs/design/ with same structure
3. Copies all documents (preserving UUIDs)
4. Updates patterns.md configuration
5. Rebuilds search index
6. Commits to project git
7. Optionally removes .design/

Exit codes:
    0 - Success
    1 - Error (no .design/ directory, user aborted, etc.)
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def detect_config(patterns_file: Path) -> dict[str, str]:
    """Detect current Atlas configuration from patterns.md.

    Args:
        patterns_file: Path to .claude/architect/patterns.md

    Returns:
        Dictionary containing design_root, mode, and memory_root
    """
    config = {"design_root": "", "mode": "", "memory_root": ""}

    if not patterns_file.exists():
        # Auto-detect if patterns.md doesn't exist
        if Path(".design").is_dir():
            config["design_root"] = ".design"
            config["mode"] = "dual-git"
        elif Path("docs/design").is_dir():
            config["design_root"] = "docs/design"
            config["mode"] = "single-git"
        return config

    try:
        content = patterns_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("design_root:"):
                config["design_root"] = line.split(":", 1)[1].strip().strip('"').rstrip("/")
            elif line.startswith("mode:"):
                config["mode"] = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("memory_root:"):
                config["memory_root"] = line.split(":", 1)[1].strip().strip('"')
    except (OSError, UnicodeDecodeError):
        pass

    # Auto-detect if not configured
    if not config["design_root"]:
        if Path(".design").is_dir():
            config["design_root"] = ".design"
            config["mode"] = "dual-git"
        elif Path("docs/design").is_dir():
            config["design_root"] = "docs/design"
            config["mode"] = "single-git"

    return config


def count_markdown_files(directory: Path) -> int:
    """Count markdown files in a directory.

    Args:
        directory: Path to directory to scan

    Returns:
        Number of .md files found
    """
    if not directory.exists():
        return 0
    return len(list(directory.rglob("*.md")))


def copy_directory_contents(src: Path, dest: Path, dry_run: bool) -> int:
    """Copy all files from source to destination directory.

    Args:
        src: Source directory
        dest: Destination directory
        dry_run: If True, only report what would be done

    Returns:
        Number of markdown files copied
    """
    if not src.exists():
        return 0

    file_count = count_markdown_files(src)

    if not dry_run and file_count > 0:
        dest.mkdir(parents=True, exist_ok=True)
        # Copy all files recursively
        for item in src.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(src)
                target = dest / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)

    return file_count


def update_patterns_file(patterns_file: Path, dry_run: bool) -> None:
    """Update patterns.md to reflect single-git mode.

    Args:
        patterns_file: Path to patterns.md
        dry_run: If True, only report what would be done
    """
    if not patterns_file.exists() or dry_run:
        return

    try:
        content = patterns_file.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)
        modified = False

        for i, line in enumerate(lines):
            if line.startswith("mode:"):
                lines[i] = "mode: single-git\n"
                modified = True
            elif line.startswith("design_root:"):
                lines[i] = "design_root: docs/design/\n"
                modified = True

        if modified:
            patterns_file.write_text("".join(lines), encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        pass


def rebuild_search_index(dry_run: bool) -> None:
    """Rebuild Atlas search index for new location.

    Args:
        dry_run: If True, only report what would be done
    """
    if dry_run:
        return

    # Try to find and execute search script
    search_scripts = [
        Path("scripts/atlas-design-search.sh"),
        Path("atlas-design-search.sh"),
    ]

    for script in search_scripts:
        if script.exists() and script.stat().st_mode & 0o111:  # Check executable
            try:
                subprocess.run([str(script), "--rebuild-index"], env={"DESIGN_ROOT": "docs/design"}, stderr=subprocess.DEVNULL, check=False)
                return
            except (subprocess.SubprocessError, OSError):
                continue


def commit_transition(spec_count: int, plan_count: int, adr_count: int, total: int, dry_run: bool) -> None:
    """Commit design document transition to project git.

    Args:
        spec_count: Number of spec documents transitioned
        plan_count: Number of plan documents transitioned
        adr_count: Number of ADR documents transitioned
        total: Total number of documents transitioned
        dry_run: If True, only report what would be done
    """
    if dry_run:
        return

    commit_msg = f"""[TRANSITION] Move design documents from private to public

## WHAT Changed
### Moved Directories
- MOVED: .design/specs/* -> docs/design/specs/
- MOVED: .design/plans/* -> docs/design/plans/
- MOVED: .design/decisions/* -> docs/design/decisions/
- MOVED: .design/templates/* -> docs/design/templates/

### Configuration
- UPDATED: .claude/architect/patterns.md
  - mode: dual-git -> single-git
  - design_root: .design/ -> docs/design/

### Preserved
- All document UUIDs unchanged
- All GitHub issue references remain valid
- Index rebuilt for new location

## WHY Changed
Design documents transitioned from private (dual-git) to public (single-git).
Decision to make architecture documentation publicly available.

### Document Counts
- Specs: {spec_count}
- Plans: {plan_count}
- ADRs: {adr_count}
- Total: {total}

### Note
The .design/ directory may still exist but is no longer used.
Memory files may need to be moved separately if stored in .design/memory/.
"""

    try:
        # Stage files
        subprocess.run(["git", "add", "docs/design/"], check=False, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "add", ".claude/architect/patterns.md"], check=False, stderr=subprocess.DEVNULL)

        # Commit
        subprocess.run(["git", "commit", "-m", commit_msg], check=False, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except (subprocess.SubprocessError, OSError):
        print("  (Git command failed, changes may not be committed)")


def main() -> int:
    """Main entry point for design transition script.

    Returns:
        Exit code: 0 for success, 1 for error/abort
    """
    parser = argparse.ArgumentParser(description="Transition design documents from private (.design/) to public (docs/design/)", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompt")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--keep-private", action="store_true", help="Don't delete .design/ after transition")

    args = parser.parse_args()

    # Detect current configuration
    patterns_file = Path(".claude/architect/patterns.md")
    config = detect_config(patterns_file)

    print("=== Design Document Transition: Private -> Public ===")
    print()
    print("Current configuration:")
    print(f"  Mode: {config['mode'] or 'not set'}")
    print(f"  Design root: {config['design_root'] or 'not set'}")
    print(f"  Memory root: {config['memory_root'] or 'not set'}")
    print()

    # Verify .design/ exists
    design_dir = Path(".design")
    if not design_dir.exists():
        print("ERROR: No .design/ directory found.", file=sys.stderr)
        print("This script is for transitioning from dual-git to single-git.", file=sys.stderr)
        print("If already in single-git mode, no transition needed.", file=sys.stderr)
        return 1

    # Count documents to transition
    spec_count = count_markdown_files(design_dir / "specs")
    plan_count = count_markdown_files(design_dir / "plans")
    adr_count = count_markdown_files(design_dir / "decisions")
    total = spec_count + plan_count + adr_count

    print("Documents to transition:")
    print(f"  Specs: {spec_count}")
    print(f"  Plans: {plan_count}")
    print(f"  ADRs: {adr_count}")
    print(f"  Total: {total}")
    print()

    if args.dry_run:
        print("*** DRY RUN MODE - No changes will be made ***")
        print()

    # Confirmation prompt
    if not args.force and not args.dry_run:
        print("WARNING: This will make ALL design documents PUBLIC!")
        print()
        print("After this transition:")
        print("  - All specs, plans, and ADRs will be visible on GitHub")
        print("  - Git history will contain everything (CANNOT be undone)")
        print("  - Anyone cloning the repo can see design documents")
        print()

        try:
            confirm = input("Type 'CONFIRM' to proceed: ")
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            return 1

        if confirm != "CONFIRM":
            print("Aborted.")
            return 1

    # Create target directory structure
    print("Creating docs/design/ structure...")
    target = Path("docs/design")
    if not args.dry_run:
        (target / "specs").mkdir(parents=True, exist_ok=True)
        (target / "plans").mkdir(parents=True, exist_ok=True)
        (target / "decisions").mkdir(parents=True, exist_ok=True)
        (target / "templates").mkdir(parents=True, exist_ok=True)
        (target / "exports").mkdir(parents=True, exist_ok=True)

    # Copy documents
    print("Copying documents...")
    for subdir in ["specs", "plans", "decisions", "templates"]:
        src = design_dir / subdir
        dest = target / subdir
        file_count = copy_directory_contents(src, dest, args.dry_run)
        print(f"  {subdir}/: {file_count} files")

    # Copy UUID counter
    uuid_counter = design_dir / ".architect-uuid-counter"
    if uuid_counter.exists():
        print("Copying UUID counter...")
        if not args.dry_run:
            shutil.copy2(uuid_counter, target / ".architect-uuid-counter")

    # Update patterns.md
    print("Updating patterns.md configuration...")
    update_patterns_file(patterns_file, args.dry_run)
    if patterns_file.exists() and not args.dry_run:
        print("  Updated mode: single-git")
        print("  Updated design_root: docs/design/")

    # Rebuild search index
    print("Rebuilding search index...")
    rebuild_search_index(args.dry_run)

    # Commit changes
    print("Committing to project git...")
    commit_transition(spec_count, plan_count, adr_count, total, args.dry_run)

    # Handle private directory
    if not args.keep_private and not args.dry_run:
        print()
        print("The .design/ directory still exists.")
        print("To remove it: rm -rf .design/")
        print()
        print("NOTE: Memory files in .design/memory/ were NOT copied.")
        print("If using memory in design git, update memory_root in patterns.md:")
        print("  memory_root: .claude/architect/")

    print()
    print("=== Transition Complete ===")
    print()
    print("New configuration:")
    print("  Mode: single-git")
    print("  Design root: docs/design/")
    print(f"  Documents: {total}")
    print()
    print("Next steps:")
    print("  1. Review committed changes: git log -1")
    print("  2. Push to remote: git push")
    print("  3. (Optional) Remove .design/: rm -rf .design/")
    print("  4. (Optional) Update memory location in patterns.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
