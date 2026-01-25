#!/usr/bin/env python3
"""
Atlas Start Planning Script

Initializes Plan Phase Mode by creating the plan state file and setting up
requirements tracking. This is the entry point for the Two-Phase workflow.

Usage:
    python3 atlas_start_planning.py "Goal description here"
    python3 atlas_start_planning.py --goal "Build user authentication"
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

# Plan phase state file location
PLAN_STATE_FILE = Path(".claude/orchestrator-plan-phase.local.md")


def generate_plan_id() -> str:
    """Generate a unique plan ID based on timestamp."""
    now = datetime.now(timezone.utc)
    return f"plan-{now.strftime('%Y%m%d-%H%M%S')}"


def create_plan_state_file(goal: str) -> bool:
    """Create the plan phase state file with initial configuration."""
    plan_id = generate_plan_id()
    now = datetime.now(timezone.utc).isoformat()

    # Ensure .claude directory exists
    PLAN_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Check if already in plan phase
    if PLAN_STATE_FILE.exists():
        print(f"ERROR: Plan Phase already active. State file exists: {PLAN_STATE_FILE}")
        print("Use /planning-status to view current plan, or delete the state file to start fresh.")
        return False

    # Create the state file with YAML frontmatter
    content = f"""---
phase: "planning"
plan_id: "{plan_id}"
status: "drafting"
created_at: "{now}"

# User Goal (immutable without user approval)
goal: "{goal}"
goal_locked: true

# Requirements Progress
requirements_file: "USER_REQUIREMENTS.md"
requirements_complete: false
requirements_sections:
  - name: "Functional Requirements"
    status: "pending"
  - name: "Non-Functional Requirements"
    status: "pending"
  - name: "Architecture Design"
    status: "pending"

# Module Breakdown
modules: []

# Exit Criteria
plan_phase_complete: false
exit_criteria:
  - "USER_REQUIREMENTS.md complete"
  - "All modules defined with acceptance criteria"
  - "GitHub Issues created for all modules"
  - "User approved the plan"
---

# Plan Phase: {plan_id}

## Goal

{goal}

## Status

Phase: Planning (drafting)

## Instructions

1. Use `/planning-status` to view progress
2. Use `/add-requirement` to add requirements and modules
3. Use `/modify-requirement` to update specifications
4. Use `/approve-plan` when all requirements are complete

## Notes

- The stop hook will block exit until the plan is approved
- You can add/modify/remove requirements at any time during this phase
- GitHub Issues will be created when you run `/approve-plan`
"""

    try:
        PLAN_STATE_FILE.write_text(content, encoding="utf-8")
        print("✓ Plan Phase initialized")
        print(f"  Plan ID: {plan_id}")
        print(f"  Goal: {goal}")
        print(f"  State file: {PLAN_STATE_FILE}")
        print()
        print("Next steps:")
        print("  1. Create USER_REQUIREMENTS.md with detailed requirements")
        print("  2. Use /add-requirement to define modules")
        print("  3. Use /planning-status to track progress")
        print("  4. Use /approve-plan when ready to implement")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create state file: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize Plan Phase Mode for orchestrator workflow"
    )
    parser.add_argument(
        "goal",
        nargs="?",
        help="The goal/objective for this planning session"
    )
    parser.add_argument(
        "--goal", "-g",
        dest="goal_flag",
        help="Alternative way to specify the goal"
    )

    args = parser.parse_args()

    # Get goal from either positional or flag argument
    goal = args.goal or args.goal_flag

    if not goal:
        print("ERROR: Goal is required")
        print("Usage: /start-planning \"Your goal description here\"")
        return 1

    # Clean up goal string (remove surrounding quotes if present)
    goal = goal.strip().strip('"').strip("'")

    if not goal:
        print("ERROR: Goal cannot be empty")
        return 1

    success = create_plan_state_file(goal)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
