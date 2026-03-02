#!/usr/bin/env python3
"""
eaa_init_design_folders.py - Initialize design document folder structure.

Creates the required folder structure for Architect Agent design documents:
    docs/design/
    ├── specs/      (SPEC documents)
    ├── plans/      (PLAN documents)
    ├── decisions/  (ADR - Architecture Decision Records)
    └── exports/    (Sanitized exports for GitHub)

Usage:
    python eaa_init_design_folders.py [--project-root PATH]
"""

import argparse
import sys
from pathlib import Path


def init_design_folders(project_root: Path) -> bool:
    """
    Initialize design document folder structure.

    Args:
        project_root: Project root directory

    Returns:
        True if successful, False otherwise
    """
    design_root = project_root / "docs" / "design"

    folders = [
        design_root / "specs",
        design_root / "plans",
        design_root / "decisions",
        design_root / "exports",
    ]

    try:
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {folder.relative_to(project_root)}")

        # Create a .gitkeep in exports folder to track it
        gitkeep = design_root / "exports" / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
            print(f"✓ Created: {gitkeep.relative_to(project_root)}")

        print(f"\n✓ Design folder structure initialized at {design_root}")
        return True

    except Exception as e:
        print(f"✗ ERROR: Failed to create design folders: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Initialize Architect Agent design document folders"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    args = parser.parse_args()

    if not args.project_root.exists():
        print(
            f"✗ ERROR: Project root does not exist: {args.project_root}",
            file=sys.stderr,
        )
        return 1

    if not args.project_root.is_dir():
        print(
            f"✗ ERROR: Project root is not a directory: {args.project_root}",
            file=sys.stderr,
        )
        return 1

    success = init_design_folders(args.project_root)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
