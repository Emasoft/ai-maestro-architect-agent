#!/usr/bin/env python3
"""
Generate a task tracker from plan files or scratch.

This script creates task tracking documents that can parse existing plan files
or generate empty templates. It validates dependencies, calculates critical paths,
and supports multiple output formats.

FAIL-FAST APPROACH: No error handling - exits immediately on any error.

Usage:
    # Generate from scratch
    python generate-task-tracker.py --phases 4 --tasks-per-phase 8 --output tasks.csv

    # Parse from existing plan
    python generate-task-tracker.py --from-plan plans/GH-123-feature.md --output tracker.json

    # Validate plan structure only
    python generate-task-tracker.py --from-plan plans/GH-123-feature.md --validate

Arguments:
    --phases: Number of phases for template generation
    --tasks-per-phase: Tasks per phase for pre-allocation
    --from-plan: Path to existing plan file to parse
    --output: Output file path (extension determines format: .csv, .json)
    --validate: Only validate plan structure, don't generate output
    --help: Show this help message
"""

import sys
import argparse
import csv
import io
import re
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import atomic_write_json, atomic_write_text  # type: ignore[import-not-found]  # noqa: E402


class Task:
    """Represents a single task with dependencies and metadata."""

    def __init__(
        self,
        task_id: str,
        phase: int,
        name: str,
        status: str = "pending",
        dependencies: Optional[List[str]] = None,
        assignee: str = "",
        notes: str = "",
    ):
        """
        Initialize a task.

        Args:
            task_id: Unique task identifier
            phase: Phase number this task belongs to
            name: Task name/description
            status: Task status (pending, in_progress, completed, blocked)
            dependencies: List of task IDs this task depends on
            assignee: Person assigned to this task
            notes: Additional notes
        """
        self.task_id = task_id
        self.phase = phase
        self.name = name
        self.status = status
        self.dependencies = dependencies or []
        self.assignee = assignee
        self.notes = notes
        self.created = datetime.now().isoformat()
        self.updated = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.task_id,
            "phase": self.phase,
            "name": self.name,
            "status": self.status,
            "dependencies": self.dependencies,
            "assignee": self.assignee,
            "notes": self.notes,
            "created": self.created,
            "updated": self.updated,
        }

    def to_csv_row(self) -> List[str]:
        """Convert task to CSV row."""
        return [
            self.task_id,
            str(self.phase),
            self.name,
            self.status,
            ",".join(self.dependencies),
            self.assignee,
            self.notes,
            self.created,
            self.updated,
        ]


class TaskTracker:
    """Manages task collection, validation, and output."""

    def __init__(self) -> None:
        """Initialize task tracker."""
        self.tasks: List[Task] = []
        self.plan_file: Optional[str] = None

    def add_task(self, task: Task) -> None:
        """Add a task to the tracker."""
        self.tasks.append(task)

    def validate_dependencies(self) -> None:
        """
        Validate task dependencies form a DAG (no circular dependencies).

        Raises:
            SystemExit: If circular dependencies are detected
        """
        # Build adjacency list
        graph: Dict[str, List[str]] = {}
        task_ids = {task.task_id for task in self.tasks}

        for task in self.tasks:
            graph[task.task_id] = task.dependencies

            # Check that all dependencies exist
            for dep_id in task.dependencies:
                if dep_id not in task_ids:
                    print(
                        f"ERROR: Task {task.task_id} depends on non-existent task {dep_id}",
                        file=sys.stderr,
                    )
                    sys.exit(1)

        # Detect cycles using DFS with color marking
        # WHITE (0): unvisited, GRAY (1): in current path, BLACK (2): fully processed
        color: Dict[str, int] = {tid: 0 for tid in task_ids}

        def has_cycle_dfs(node: str, path: List[str]) -> bool:
            """DFS to detect cycles. Returns True if cycle found."""
            if color[node] == 1:  # GRAY - found back edge (cycle)
                cycle_start = path.index(node)
                cycle_path = " -> ".join(path[cycle_start:] + [node])
                print(
                    f"ERROR: Circular dependency detected: {cycle_path}",
                    file=sys.stderr,
                )
                return True

            if color[node] == 2:  # BLACK - already processed
                return False

            color[node] = 1  # Mark as GRAY (in current path)
            path.append(node)

            for neighbor in graph.get(node, []):
                if has_cycle_dfs(neighbor, path):
                    return True

            path.pop()
            color[node] = 2  # Mark as BLACK (fully processed)
            return False

        # Check each unvisited node
        for task_id in task_ids:
            if color[task_id] == 0:
                if has_cycle_dfs(task_id, []):
                    sys.exit(1)

    def calculate_critical_path(self) -> List[str]:
        """
        Calculate critical path through task dependencies using topological sort.

        Returns:
            List of task IDs representing the critical path
        """
        # Build adjacency list and in-degree count
        graph: Dict[str, List[str]] = {task.task_id: [] for task in self.tasks}
        in_degree: Dict[str, int] = {task.task_id: 0 for task in self.tasks}

        for task in self.tasks:
            for dep_id in task.dependencies:
                graph[dep_id].append(task.task_id)
                in_degree[task.task_id] += 1

        # Find all tasks with no dependencies (starting points)
        queue = deque([tid for tid, degree in in_degree.items() if degree == 0])

        # Track longest path to each task
        longest_path: Dict[str, int] = {tid: 0 for tid in graph}
        predecessor: Dict[str, Optional[str]] = {tid: None for tid in graph}

        # Process tasks in topological order
        while queue:
            current = queue.popleft()

            for neighbor in graph[current]:
                # Update longest path if we found a longer one
                if longest_path[current] + 1 > longest_path[neighbor]:
                    longest_path[neighbor] = longest_path[current] + 1
                    predecessor[neighbor] = current

                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Find the task with the longest path (end of critical path)
        critical_end = max(longest_path.items(), key=lambda x: x[1])[0]

        # Reconstruct critical path by walking backwards through predecessors
        critical_path: List[str] = []
        current_node: Optional[str] = critical_end
        while current_node is not None:
            critical_path.append(current_node)
            current_node = predecessor[current_node]

        critical_path.reverse()
        return critical_path

    def parse_plan_file(self, plan_path: str) -> None:
        """
        Parse a plan file and extract tasks.

        Expects markdown structure:
        ## Phase N: Name
        - [ ] Task description
        - [x] Completed task

        Dependencies can be specified as: Depends on: #task_id or Depends on: #task_id, #task_id2

        Args:
            plan_path: Path to the plan file

        Raises:
            SystemExit: If file not found or parse error
        """
        plan_file = Path(plan_path)
        if not plan_file.exists():
            print(f"ERROR: Plan file not found: {plan_path}", file=sys.stderr)
            sys.exit(1)

        self.plan_file = plan_path
        content = plan_file.read_text(encoding="utf-8")

        # Extract GH issue number from filename (GH-{number}-{slug}.md)
        gh_match = re.search(r"GH-(\d+)", plan_file.name)
        gh_prefix = f"GH{gh_match.group(1)}" if gh_match else "T"

        phase_pattern = re.compile(r"^##\s+(?:Phase\s+)?(\d+):\s*(.+)$", re.MULTILINE)
        task_pattern = re.compile(r"^-\s+\[([ x])\]\s+(.+)$", re.MULTILINE)

        # Find all phases
        phases = list(phase_pattern.finditer(content))

        if not phases:
            print(
                "ERROR: No phases found in plan file. Expected '## Phase N: Name' format",
                file=sys.stderr,
            )
            sys.exit(1)

        task_counter = 1

        for i, phase_match in enumerate(phases):
            phase_num = int(phase_match.group(1))
            # phase_match.group(2) contains phase name but is not used

            # Extract content between this phase and next phase (or end of file)
            start_pos = phase_match.end()
            end_pos = phases[i + 1].start() if i + 1 < len(phases) else len(content)
            phase_content = content[start_pos:end_pos]

            # Find all tasks in this phase
            for task_match in task_pattern.finditer(phase_content):
                is_completed = task_match.group(1) == "x"
                task_desc = task_match.group(2).strip()

                # Extract dependencies from task description
                dependencies: List[str] = []
                dep_match = re.search(
                    r"Depends on:\s*([#\w\-,\s]+)", task_desc, re.IGNORECASE
                )
                if dep_match:
                    dep_str = dep_match.group(1)
                    dependencies = [d.strip().lstrip("#") for d in dep_str.split(",")]
                    # Remove dependency text from description
                    task_desc = re.sub(
                        r"\s*Depends on:\s*[#\w\-,\s]+",
                        "",
                        task_desc,
                        flags=re.IGNORECASE,
                    ).strip()

                # Generate task ID
                task_id = f"{gh_prefix}-{task_counter:03d}"
                task_counter += 1

                status = "completed" if is_completed else "pending"

                task = Task(
                    task_id=task_id,
                    phase=phase_num,
                    name=task_desc,
                    status=status,
                    dependencies=dependencies,
                )

                self.add_task(task)

    def generate_template(self, phases: int, tasks_per_phase: int) -> None:
        """
        Generate empty task template.

        Args:
            phases: Number of phases
            tasks_per_phase: Tasks to pre-allocate per phase
        """
        task_counter = 1

        for phase in range(1, phases + 1):
            for task_num in range(1, tasks_per_phase + 1):
                task_id = f"T-{task_counter:03d}"
                task_counter += 1

                task = Task(
                    task_id=task_id,
                    phase=phase,
                    name=f"[Task {task_num} description]",
                    status="pending",
                )

                self.add_task(task)

    def export_csv(self, output_path: str) -> None:
        """
        Export tasks to CSV format.

        Args:
            output_path: Output file path
        """
        headers = [
            "id",
            "phase",
            "name",
            "status",
            "dependencies",
            "assignee",
            "notes",
            "created",
            "updated",
        ]

        # Build CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        for task in self.tasks:
            writer.writerow(task.to_csv_row())

        atomic_write_text(output.getvalue(), Path(output_path))
        print(f"CSV task tracker exported: {output_path}")

    def export_json(self, output_path: str) -> None:
        """
        Export tasks to JSON format.

        Args:
            output_path: Output file path
        """
        critical_path = self.calculate_critical_path() if self.tasks else []

        data = {
            "version": "1.0",
            "plan_file": self.plan_file,
            "generated": datetime.now().isoformat(),
            "tasks": [task.to_dict() for task in self.tasks],
            "metadata": {
                "total_tasks": len(self.tasks),
                "phases": len(set(task.phase for task in self.tasks)),
                "critical_path": critical_path,
                "critical_path_length": len(critical_path),
            },
        }

        atomic_write_json(data, Path(output_path))
        print(f"JSON task tracker exported: {output_path}")

    def export(self, output_path: str) -> None:
        """
        Export tasks to appropriate format based on file extension.

        Args:
            output_path: Output file path

        Raises:
            SystemExit: If unsupported format
        """
        ext = Path(output_path).suffix.lower()

        if ext == ".csv":
            self.export_csv(output_path)
        elif ext == ".json":
            self.export_json(output_path)
        else:
            print(
                f"ERROR: Unsupported output format: {ext}. Use .csv or .json",
                file=sys.stderr,
            )
            sys.exit(1)


def validate_plan_structure(plan_path: str) -> None:
    """
    Validate plan file structure without generating output.

    Args:
        plan_path: Path to plan file
    """
    print(f"Validating plan structure: {plan_path}")

    tracker = TaskTracker()
    tracker.parse_plan_file(plan_path)

    print(
        f"✓ Found {len(tracker.tasks)} tasks across {len(set(t.phase for t in tracker.tasks))} phases"
    )

    print("Validating dependencies...")
    tracker.validate_dependencies()
    print("✓ No circular dependencies detected")

    if tracker.tasks:
        critical_path = tracker.calculate_critical_path()
        print(f"✓ Critical path length: {len(critical_path)} tasks")
        print(f"  Critical path: {' -> '.join(critical_path)}")

    print("\nValidation successful!")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate task tracker from plan files or scratch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate empty template
  python generate-task-tracker.py --phases 4 --tasks-per-phase 8 --output tasks.csv

  # Parse from existing plan
  python generate-task-tracker.py --from-plan plans/GH-123-feature.md --output tracker.json

  # Validate plan structure
  python generate-task-tracker.py --from-plan plans/GH-123-feature.md --validate

  # Generate with default settings
  python generate-task-tracker.py --output my-tasks.csv
        """,
    )

    parser.add_argument(
        "--phases",
        type=int,
        default=4,
        help="Number of phases for template generation (default: 4)",
    )
    parser.add_argument(
        "--tasks-per-phase",
        type=int,
        default=8,
        help="Tasks per phase for pre-allocation (default: 8)",
    )
    parser.add_argument(
        "--from-plan",
        help="Path to existing plan file to parse (e.g., plans/GH-123-feature.md)",
    )
    parser.add_argument(
        "--output",
        default="task-tracker.csv",
        help="Output file path (extension determines format: .csv, .json)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Only validate plan structure, don't generate output",
    )

    args = parser.parse_args()

    # Validate mode
    if args.validate:
        if not args.from_plan:
            print("ERROR: --validate requires --from-plan", file=sys.stderr)
            sys.exit(1)
        validate_plan_structure(args.from_plan)
        return

    # Create tracker
    tracker = TaskTracker()

    # Generate or parse
    if args.from_plan:
        tracker.parse_plan_file(args.from_plan)
    else:
        tracker.generate_template(args.phases, args.tasks_per_phase)

    # Validate dependencies
    if tracker.tasks:
        tracker.validate_dependencies()

    # Export
    tracker.export(args.output)


if __name__ == "__main__":
    main()
