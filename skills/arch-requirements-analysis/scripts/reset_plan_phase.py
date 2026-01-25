#!/usr/bin/env python3
"""
Reset Plan Phase Script

Safely resets the plan phase by backing up and removing the state file.
Use with caution - this will lose all planning progress.

Usage:
    python3 reset_plan_phase.py --confirm
    python3 reset_plan_phase.py --confirm --no-backup
"""

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PLAN_STATE_FILE = Path(".claude/orchestrator-plan-phase.local.md")
BACKUP_DIR = Path("docs_dev/plan_backups")


def backup_state_file() -> Path | None:
    """Create a backup of the current state file."""
    if not PLAN_STATE_FILE.exists():
        return None

    # Ensure backup directory exists
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_path = BACKUP_DIR / f"plan-phase-backup-{timestamp}.md"

    shutil.copy2(PLAN_STATE_FILE, backup_path)
    return backup_path


def reset_plan_phase(create_backup: bool = True) -> bool:
    """Reset the plan phase by removing the state file."""
    if not PLAN_STATE_FILE.exists():
        print("No plan phase state file found. Nothing to reset.")
        return True

    # Create backup if requested
    backup_path = None
    if create_backup:
        backup_path = backup_state_file()
        if backup_path:
            print(f"Backup created: {backup_path}")

    # Remove the state file
    try:
        PLAN_STATE_FILE.unlink()
        print(f"Removed: {PLAN_STATE_FILE}")
        print("\nPlan phase has been reset.")
        print("Run /start-planning to begin a new plan.")
        return True
    except Exception as e:
        print(f"ERROR: Failed to remove state file: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Reset plan phase")
    parser.add_argument(
        "--confirm",
        action="store_true",
        required=True,
        help="Confirm the reset operation"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip backup creation"
    )

    args = parser.parse_args()

    if not args.confirm:
        print("ERROR: Must provide --confirm flag to proceed")
        print("This operation will remove all planning progress.")
        return 1

    print("WARNING: This will reset the plan phase!")
    print("All planning progress will be lost.")
    print()

    success = reset_plan_phase(create_backup=not args.no_backup)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
