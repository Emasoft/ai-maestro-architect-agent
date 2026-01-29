#!/usr/bin/env python3
"""
eaa_stop_check.py - Stop hook to block exit with incomplete design work.

This script checks for:
1. Design documents in "draft" state (not approved)
2. Claude Tasks with pending/in_progress status
3. Open requirements without corresponding design docs
4. GitHub Issues assigned to architect that aren't closed

Exit codes:
- 0: Allow exit (all work complete)
- 2: Block exit (incomplete work found, returns JSON reason)
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def read_hook_input() -> dict[str, Any]:
    """Read hook input from stdin as JSON."""
    try:
        stdin_data = sys.stdin.read()
        if stdin_data.strip():
            return json.loads(stdin_data)
    except json.JSONDecodeError:
        pass
    return {}


def find_project_root() -> Path | None:
    """Find project root by looking for .claude or .git directory."""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".claude").exists() or (parent / ".git").exists():
            return parent
    return current


def check_draft_design_docs(project_root: Path) -> list[str]:
    """Check for design documents in draft state."""
    blockers: list[str] = []

    # Common locations for design documents
    design_dirs = [
        project_root / "docs" / "design",
        project_root / "design",
        project_root / "docs_dev" / "design",
        project_root / "thoughts" / "shared" / "handoffs",
    ]

    for design_dir in design_dirs:
        if not design_dir.exists():
            continue

        for doc in design_dir.rglob("*.md"):
            try:
                content = doc.read_text(encoding="utf-8")
                # Check for draft indicators in frontmatter or content
                if any(
                    indicator in content.lower()
                    for indicator in [
                        "status: draft",
                        "state: draft",
                        "[draft]",
                        "## draft",
                        "wip:",
                        "status: wip",
                        "in_progress",
                    ]
                ):
                    blockers.append(
                        f"Draft design doc: {doc.relative_to(project_root)}"
                    )
            except (OSError, UnicodeDecodeError):
                continue

    return blockers


def check_pending_tasks(project_root: Path) -> list[str]:
    """Check for pending/in-progress Claude Tasks."""
    blockers: list[str] = []

    # Check .claude/tasks directory
    tasks_dir = project_root / ".claude" / "tasks"
    if tasks_dir.exists():
        for task_file in tasks_dir.glob("*.json"):
            try:
                task_data = json.loads(task_file.read_text(encoding="utf-8"))
                status = task_data.get("status", "").lower()
                if status in ["pending", "in_progress", "in-progress", "running"]:
                    task_name = task_data.get("name", task_file.stem)
                    blockers.append(f"Pending task: {task_name} (status: {status})")
            except (json.JSONDecodeError, OSError):
                continue

    # Check thoughts/shared/handoffs for checkpoint files
    handoffs_dir = project_root / "thoughts" / "shared" / "handoffs"
    if handoffs_dir.exists():
        for checkpoint in handoffs_dir.rglob("current.md"):
            try:
                content = checkpoint.read_text(encoding="utf-8")
                if "IN_PROGRESS" in content or "PENDING" in content:
                    rel_path = checkpoint.relative_to(project_root)
                    blockers.append(f"Incomplete handoff: {rel_path}")
            except (OSError, UnicodeDecodeError):
                continue

    return blockers


def check_orphan_requirements(project_root: Path) -> list[str]:
    """Check for requirements without corresponding design documents."""
    blockers: list[str] = []

    # Look for requirements files
    req_patterns = ["requirements.md", "REQUIREMENTS.md", "requirements/*.md"]
    design_patterns = ["design/*.md", "docs/design/*.md"]

    req_files: list[Path] = []
    for pattern in req_patterns:
        req_files.extend(project_root.glob(pattern))

    design_files: set[str] = set()
    for pattern in design_patterns:
        for df in project_root.glob(pattern):
            design_files.add(df.stem.lower())

    for req_file in req_files:
        try:
            content = req_file.read_text(encoding="utf-8")
            # Look for requirement IDs like REQ-001, R001, etc.
            import re

            req_ids = re.findall(
                r"(?:REQ|R|REQUIREMENT)-?\d{1,4}", content, re.IGNORECASE
            )
            for req_id in req_ids:
                normalized = req_id.lower().replace("-", "")
                if (
                    normalized not in design_files
                    and f"design-{normalized}" not in design_files
                ):
                    # Only report if there's no design doc reference in the same file
                    if f"design for {req_id}" not in content.lower():
                        blockers.append(f"Requirement without design: {req_id}")
        except (OSError, UnicodeDecodeError):
            continue

    # Deduplicate
    return list(set(blockers))[:5]  # Limit to 5 to avoid noise


def check_github_issues() -> list[str]:
    """Check for open GitHub Issues assigned to architect."""
    blockers: list[str] = []

    # Check if gh CLI is available
    try:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "list",
                "--assignee",
                "@me",
                "--state",
                "open",
                "--json",
                "number,title,labels",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            issues = json.loads(result.stdout)
            for issue in issues[:5]:  # Limit to 5
                labels = [lbl.get("name", "") for lbl in issue.get("labels", [])]
                # Check if issue is architecture/design related
                if any(
                    label in ["architecture", "design", "planning", "architect"]
                    for label in labels
                ):
                    blockers.append(
                        f"Open issue #{issue['number']}: {issue['title'][:50]}"
                    )
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass  # gh CLI not available or timed out - skip this check

    return blockers


def main() -> None:
    """Main entry point for stop hook."""
    # Read hook input (contains session context) - reserved for future use
    _ = read_hook_input()

    # Find project root
    project_root = find_project_root()
    if not project_root:
        # Cannot determine project root - allow exit
        sys.exit(0)

    # Collect all blockers
    all_blockers: list[str] = []

    # Run all checks
    all_blockers.extend(check_draft_design_docs(project_root))
    all_blockers.extend(check_pending_tasks(project_root))
    all_blockers.extend(check_orphan_requirements(project_root))
    all_blockers.extend(check_github_issues())

    if not all_blockers:
        # All work complete - allow exit
        sys.exit(0)

    # Block exit with JSON reason
    output = {
        "decision": "block",
        "reason": f"Incomplete design work: {len(all_blockers)} items",
        "continue": True,
        "systemMessage": "Cannot exit - complete the following design work first:\n"
        + "\n".join(f"- {b}" for b in all_blockers[:10]),
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "blockers": all_blockers[:10],
            "blockerCount": len(all_blockers),
        },
    }

    print(json.dumps(output))
    sys.exit(2)


if __name__ == "__main__":
    main()
