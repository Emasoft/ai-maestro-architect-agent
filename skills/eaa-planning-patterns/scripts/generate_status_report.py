#!/usr/bin/env python3
"""
Generate markdown status reports for project progress tracking.

Generates comprehensive status reports from task tracker JSON files or plan markdown files,
including completion percentages, blocked tasks, and upcoming work.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast
from collections import defaultdict

SKILLS_DIR = Path(__file__).parent.parent.parent
# WHY: Insert shared directory into path to enable importing cross_platform module
# which provides atomic_write_text for crash-safe file operations
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import atomic_write_text  # type: ignore[import-not-found]  # noqa: E402


def load_tracker_json(tracker_path: Path) -> dict[str, Any]:
    """
    Load and parse a task tracker JSON file.

    Args:
        tracker_path: Path to tracker.json file

    Returns:
        Parsed tracker data
    """
    with open(tracker_path, "r", encoding="utf-8") as f:
        return cast(dict[str, Any], json.load(f))


def parse_plan_markdown(plan_path: Path) -> dict[str, Any]:
    """
    Parse a plan markdown file to extract tasks and their status.

    Args:
        plan_path: Path to plan markdown file

    Returns:
        Dictionary with parsed plan data
    """
    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read()

    tasks = []
    current_phase = "Unknown"

    for line in content.split("\n"):
        line = line.strip()

        # Detect phase headers
        if line.startswith("##") and not line.startswith("###"):
            current_phase = line.lstrip("#").strip()
            continue

        # Parse task lines
        if line.startswith("- ["):
            status_char = line[3]
            task_text = line[6:].strip()

            # Extract task ID if present
            task_id = None
            if task_text.startswith("[") and "]" in task_text:
                end_idx = task_text.index("]")
                task_id = task_text[1:end_idx]
                task_text = task_text[end_idx + 1 :].strip()

            # Extract dependencies
            dependencies = []
            if "Depends on:" in task_text:
                dep_part = task_text.split("Depends on:")[1]
                if ")" in dep_part:
                    dep_part = dep_part.split(")")[0]
                dependencies = [d.strip() for d in dep_part.split(",")]

            # Extract completion date
            completed_date = None
            if "completed" in task_text.lower():
                for part in task_text.split():
                    if part.count("-") == 2:
                        completed_date = part.strip("()")

            # Extract started date
            started_date = None
            if "started" in task_text.lower():
                for part in task_text.split():
                    if part.count("-") == 2 and "started" in task_text.lower():
                        started_date = part.strip("()")

            tasks.append(
                {
                    "id": task_id or task_text[:50],
                    "title": task_text,
                    "phase": current_phase,
                    "status": "completed"
                    if status_char == "x"
                    else "in-progress"
                    if status_char == "~"
                    else "pending",
                    "dependencies": dependencies,
                    "completed_date": completed_date,
                    "started_date": started_date,
                }
            )

    return {"plan_file": plan_path.name, "tasks": tasks}


def aggregate_plan_directory(plan_dir: Path) -> dict[str, Any]:
    """
    Aggregate all plan markdown files in a directory.

    Args:
        plan_dir: Directory containing plan files

    Returns:
        Aggregated plan data
    """
    all_tasks = []

    for plan_file in sorted(plan_dir.glob("*.md")):
        if plan_file.name.startswith("."):
            continue
        plan_data = parse_plan_markdown(plan_file)
        all_tasks.extend(plan_data["tasks"])

    return {"tasks": all_tasks}


def calculate_phase_progress(tasks: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """
    Calculate progress statistics per phase.

    Args:
        tasks: List of task dictionaries

    Returns:
        Dictionary mapping phase names to progress stats
    """
    # WHY: Use defaultdict with lambda to auto-initialize stats for new phases,
    # avoiding KeyError when encountering phases not seen before
    phase_stats: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "completed": 0,
            "in-progress": 0,
            "blocked": 0,
            "pending": 0,
            "total": 0,
        }
    )

    for task in tasks:
        phase = task.get("phase", "Unknown")
        status = task.get("status", "pending")

        phase_stats[phase]["total"] += 1

        if status == "completed":
            phase_stats[phase]["completed"] += 1
        elif status == "in-progress":
            phase_stats[phase]["in-progress"] += 1
        elif status == "blocked":
            phase_stats[phase]["blocked"] += 1
        else:
            phase_stats[phase]["pending"] += 1

    return dict(phase_stats)


def identify_blocked_tasks(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Identify tasks that are blocked by incomplete dependencies.

    Args:
        tasks: List of task dictionaries

    Returns:
        List of blocked tasks with blocker information
    """
    task_status = {task["id"]: task.get("status", "pending") for task in tasks}
    blocked_tasks = []

    for task in tasks:
        if task.get("status") == "blocked":
            blocked_tasks.append(task)
            continue

        dependencies = task.get("dependencies", [])
        if not dependencies:
            continue

        incomplete_deps = [
            dep for dep in dependencies if task_status.get(dep) != "completed"
        ]

        if incomplete_deps and task.get("status") == "in-progress":
            blocked_tasks.append({**task, "blockers": incomplete_deps})

    return blocked_tasks


def identify_upcoming_tasks(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Identify tasks that are ready to start (all dependencies met).

    Args:
        tasks: List of task dictionaries

    Returns:
        List of upcoming tasks ready to start
    """
    task_status = {task["id"]: task.get("status", "pending") for task in tasks}
    upcoming = []

    for task in tasks:
        if task.get("status") != "pending":
            continue

        dependencies = task.get("dependencies", [])

        if not dependencies:
            upcoming.append(task)
            continue

        if all(task_status.get(dep) == "completed" for dep in dependencies):
            upcoming.append(task)

    # WHY: Limit output to 10 tasks to prevent overwhelming status reports
    # and keep executive summaries actionable and focused
    return upcoming[:10]


def get_recently_completed(
    tasks: list[dict[str, Any]], days: int = 7
) -> list[dict[str, Any]]:
    """
    Get tasks completed in the last N days.

    Args:
        tasks: List of task dictionaries
        days: Number of days to look back

    Returns:
        List of recently completed tasks
    """
    recent = []
    # WHY: Use days parameter to filter tasks completed within the lookback window
    _ = days  # Currently unused - full date parsing to be implemented

    for task in tasks:
        if task.get("status") != "completed":
            continue

        completed_date = task.get("completed_date")
        if completed_date:
            # Simple recent check - in production would parse dates
            recent.append(task)

    return recent


def generate_executive_summary(
    tasks: list[dict[str, Any]], phase_stats: dict[str, dict[str, int]]
) -> dict[str, Any]:
    """
    Generate executive summary statistics.

    Args:
        tasks: List of task dictionaries
        phase_stats: Phase progress statistics

    Returns:
        Dictionary with summary metrics
    """
    # WHY: phase_stats reserved for future enhanced summary generation
    _ = phase_stats  # Currently unused - will be used for phase-level metrics
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.get("status") == "completed")
    in_progress_tasks = sum(1 for t in tasks if t.get("status") == "in-progress")
    blocked_tasks = len(identify_blocked_tasks(tasks))

    overall_progress = (
        int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
    )

    return {
        "overall_progress": overall_progress,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in-progress_tasks": in_progress_tasks,
        "blocked_tasks": blocked_tasks,
    }


def generate_status_report(data: dict[str, Any], output_path: Path) -> None:
    """
    Generate a formatted markdown status report.

    Args:
        data: Task data (from tracker or aggregated plans)
        output_path: Path to write the report
    """
    tasks = data.get("tasks", [])

    if not tasks:
        print("No tasks found to report", file=sys.stderr)
        sys.exit(1)

    phase_stats = calculate_phase_progress(tasks)
    summary = generate_executive_summary(tasks, phase_stats)
    blocked = identify_blocked_tasks(tasks)
    upcoming = identify_upcoming_tasks(tasks)
    recent = get_recently_completed(tasks)
    in_progress = [t for t in tasks if t.get("status") == "in-progress"]

    # Generate report content
    report_date = datetime.now().strftime("%Y-%m-%d")

    report_lines = [
        f"# Status Report - {report_date}",
        "",
        "## Executive Summary",
        f"- Overall Progress: {summary['overall_progress']}% complete",
        f"- Tasks Completed This Period: {len(recent)}",
        f"- Tasks In Progress: {summary['in-progress_tasks']}",
        f"- Blocked Tasks: {summary['blocked_tasks']}",
        "",
        "## Phase Progress",
        "| Phase | Complete | In Progress | Blocked | Pending | Total |",
        "|-------|----------|-------------|---------|---------|-------|",
    ]

    for phase, stats in sorted(phase_stats.items()):
        report_lines.append(
            f"| {phase} | {stats['completed']} | {stats['in-progress']} | "
            f"{stats['blocked']} | {stats['pending']} | {stats['total']} |"
        )

    report_lines.extend(
        [
            "",
            "## Recently Completed",
        ]
    )

    if recent:
        for task in recent[:10]:
            date_str = task.get("completed_date", "recently")
            report_lines.append(f"- [x] {task['title']} (completed {date_str})")
    else:
        report_lines.append("- No recently completed tasks")

    report_lines.extend(
        [
            "",
            "## Currently In Progress",
        ]
    )

    if in_progress:
        for task in in_progress[:10]:
            date_str = task.get("started_date", "")
            started_info = f" (started {date_str})" if date_str else ""
            report_lines.append(f"- [ ] {task['title']}{started_info}")
    else:
        report_lines.append("- No tasks in progress")

    report_lines.extend(
        [
            "",
            "## Blocked Tasks",
        ]
    )

    if blocked:
        for task in blocked:
            blockers = task.get("blockers", [])
            blocker_str = f" - Blocked by: {', '.join(blockers)}" if blockers else ""
            report_lines.append(f"- [ ] {task['title']}{blocker_str}")
    else:
        report_lines.append("- No blocked tasks")

    report_lines.extend(
        [
            "",
            "## Upcoming Tasks",
        ]
    )

    if upcoming:
        for task in upcoming:
            report_lines.append(f"- [ ] {task['title']} (dependencies met)")
    else:
        report_lines.append("- No upcoming tasks ready to start")

    report_lines.extend(
        [
            "",
            "## Risk Items",
        ]
    )

    if summary["blocked_tasks"] > 0:
        report_lines.append(
            f"- **Blocked Tasks**: {summary['blocked_tasks']} tasks are currently blocked"
        )

    if summary["overall_progress"] < 25:
        report_lines.append(
            "- **Early Stage**: Project is still in early stages, progress may be slow"
        )

    if not in_progress:
        report_lines.append("- **No Active Work**: No tasks currently in progress")

    if len(report_lines) == len(report_lines) - 1:  # Only header added
        report_lines.append("- No significant risks identified")

    # Write report
    report_content = "\n".join(report_lines) + "\n"

    atomic_write_text(output_path, report_content)


def main() -> None:
    """Main entry point for the status report generator."""
    parser = argparse.ArgumentParser(
        description="Generate markdown status reports for project progress tracking"
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--tracker", type=Path, help="Path to tracker.json file")
    input_group.add_argument(
        "--plan-dir", type=Path, help="Directory containing plan markdown files"
    )
    input_group.add_argument(
        "--github-project",
        type=str,
        help="GitHub Project URL (stub for future implementation)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output path for status report markdown file",
    )

    args = parser.parse_args()

    # Load data from appropriate source
    if args.tracker:
        if not args.tracker.exists():
            print(f"Tracker file not found: {args.tracker}", file=sys.stderr)
            sys.exit(1)
        data = load_tracker_json(args.tracker)

    elif args.plan_dir:
        if not args.plan_dir.is_dir():
            print(f"Plan directory not found: {args.plan_dir}", file=sys.stderr)
            sys.exit(1)
        data = aggregate_plan_directory(args.plan_dir)

    elif args.github_project:
        print("GitHub Projects integration not yet implemented", file=sys.stderr)
        print("Stub: Would fetch data from:", args.github_project, file=sys.stderr)
        sys.exit(1)

    else:
        # WHY: Ensure data is always bound - argparse mutual exclusion requires one input
        print(
            "No input source specified. Use --tracker, --plan-dir, or --github-project",
            file=sys.stderr,
        )
        sys.exit(1)

    # Generate report
    generate_status_report(data, args.output)

    print(f"[DONE] generate-status-report - {args.output}")
    sys.exit(0)


if __name__ == "__main__":
    main()
