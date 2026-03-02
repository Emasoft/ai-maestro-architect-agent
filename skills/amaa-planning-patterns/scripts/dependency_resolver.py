#!/usr/bin/env python3
"""
Universal Dependency Resolution Engine

WHY: Provides topological sorting for ANY dependency-ordered workflow.
     Essential for parallel task execution, build systems, installation sequences.
     Uses in-degree BFS algorithm for stable, deterministic ordering.

WHEN: Use whenever you need to determine execution order from dependency graphs.
      Examples: task scheduling, package installation, build pipelines, migration sequences.
"""

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Callable, Dict, List

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import atomic_write_text  # type: ignore  # noqa: E402


class DependencyResolver:
    """
    Resolves dependency graphs using topological sort.

    WHY: Separates graph loading, validation, and resolution into discrete steps.
         Allows reusable analysis (cycles, subgraphs) without reloading data.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize resolver.

        WHY: Verbose mode helps debug complex dependency chains and circular dependencies.
        """
        self.verbose = verbose
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.graph: Dict[str, List[str]] = {}  # node -> list of dependencies
        self.reverse_graph: Dict[str, List[str]] = {}  # node -> list of dependents

    def load_graph(self, file_path: str) -> None:
        """
        Load dependency graph from JSON or YAML file.

        WHY: Supports both JSON and YAML to accommodate different workflow formats.
             Validates structure early to fail fast on malformed input.

        Args:
            file_path: Path to graph definition file

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid or structure is malformed
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Graph file not found: {file_path}")

        # WHY: Read as text first to handle both JSON and YAML with appropriate parser
        content = path.read_text(encoding="utf-8")

        # WHY: Try JSON first as it's more common and faster to parse
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # WHY: Fall back to YAML only if JSON fails, requires yaml module
            try:
                import yaml as yaml_module

                data = yaml_module.safe_load(content)
            except ImportError:
                raise ValueError(
                    "YAML file detected but PyYAML not installed. Use JSON format or install PyYAML."
                ) from None
            except Exception as e:
                # WHY: Catch YAML parsing errors after successful import
                if "yaml" in type(e).__module__.lower():
                    raise ValueError(f"Invalid YAML format: {e}") from e
                raise

        # WHY: Validate top-level structure before processing
        if not isinstance(data, dict) or "nodes" not in data:
            raise ValueError(
                'Invalid graph format. Expected: {"nodes": {"A": {"deps": [...]}, ...}}'
            )

        self.nodes = data["nodes"]

        # WHY: Build adjacency lists for efficient graph traversal
        self.graph = {}
        self.reverse_graph = defaultdict(list)

        for node_id, node_data in self.nodes.items():
            # WHY: Default to empty deps if not specified, allows nodes with no dependencies
            deps = node_data.get("deps", []) if isinstance(node_data, dict) else []

            if not isinstance(deps, list):
                raise ValueError(
                    f"Node '{node_id}' has invalid deps (must be list): {deps}"
                )

            self.graph[node_id] = deps

            # WHY: Reverse graph enables finding all nodes that depend on a given node
            for dep in deps:
                self.reverse_graph[dep].append(node_id)

        # WHY: Ensure all referenced dependencies actually exist in the graph
        all_nodes = set(self.graph.keys())
        for node_id, deps in self.graph.items():
            missing = set(deps) - all_nodes
            if missing:
                raise ValueError(
                    f"Node '{node_id}' references non-existent dependencies: {missing}"
                )

        if self.verbose:
            print(f"Loaded graph with {len(self.nodes)} nodes", file=sys.stderr)

    def detect_cycles(self) -> List[List[str]]:
        """
        Detect all cycles in the dependency graph.

        WHY: Circular dependencies make topological sort impossible.
             Must detect and report ALL cycles for effective debugging.
             Uses DFS with path tracking for accurate cycle detection.

        Returns:
            List of cycles, where each cycle is a list of node IDs forming the loop
        """
        cycles = []
        visited = set()
        # WHY: Track current path to detect when we revisit a node in the same path
        rec_stack = set()
        path = []

        def dfs(node: str) -> None:
            """
            WHY: Recursive DFS maintains path state naturally via call stack.
                 Detects cycles when we encounter a node already in current path.
            """
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for dep in self.graph.get(node, []):
                if dep not in visited:
                    dfs(dep)
                elif dep in rec_stack:
                    # WHY: Found cycle - extract the loop from current path
                    cycle_start = path.index(dep)
                    cycle = path[cycle_start:] + [dep]
                    cycles.append(cycle)

            # WHY: Remove from recursion stack when backtracking
            path.pop()
            rec_stack.remove(node)

        # WHY: Start DFS from all nodes to catch disconnected cycles
        for node in self.graph:
            if node not in visited:
                dfs(node)

        if self.verbose and cycles:
            print(f"Detected {len(cycles)} cycle(s)", file=sys.stderr)
            for i, cycle in enumerate(cycles, 1):
                print(f"  Cycle {i}: {' -> '.join(cycle)}", file=sys.stderr)

        return cycles

    def topological_sort(self) -> List[str]:
        """
        Perform topological sort using Kahn's algorithm (in-degree BFS).

        WHY: Kahn's algorithm is more intuitive than DFS-based approaches.
             Produces stable ordering: nodes with same depth appear in lexicographic order.
             Detects cycles naturally when not all nodes can be processed.

        Returns:
            Ordered list of node IDs (dependencies before dependents)

        Raises:
            ValueError: If graph contains cycles (no valid topological order exists)
        """
        # WHY: Check for cycles first to provide detailed cycle information
        cycles = self.detect_cycles()
        if cycles:
            cycle_strs = [" -> ".join(c) for c in cycles]
            raise ValueError(
                "Cannot perform topological sort: circular dependencies detected:\n"
                + "\n".join(f"  - {c}" for c in cycle_strs)
            )

        # WHY: Calculate in-degree (number of dependencies) for each node
        in_degree = {node: len(deps) for node, deps in self.graph.items()}

        # WHY: Start with nodes that have no dependencies (in-degree = 0)
        #      Use sorted() for deterministic ordering when multiple nodes have same in-degree
        queue = deque(
            sorted([node for node, degree in in_degree.items() if degree == 0])
        )
        result = []

        while queue:
            # WHY: Process nodes in lexicographic order for deterministic results
            node = queue.popleft()
            result.append(node)

            if self.verbose:
                print(f"Processing: {node}", file=sys.stderr)

            # WHY: Decrease in-degree of all dependents (nodes that depend on current node)
            for dependent in sorted(self.reverse_graph.get(node, [])):
                in_degree[dependent] -= 1

                # WHY: When in-degree reaches 0, all dependencies are satisfied
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # WHY: Sanity check - if we didn't process all nodes, there's a cycle we missed
        if len(result) != len(self.graph):
            unprocessed = set(self.graph.keys()) - set(result)
            raise ValueError(
                f"Topological sort incomplete. Unprocessed nodes (likely in cycle): {unprocessed}"
            )

        return result

    def get_subgraph(self, node: str) -> List[str]:
        """
        Get all dependencies of a node (transitive closure).

        WHY: Useful for understanding complete dependency chain of a single task.
             Enables partial execution (only nodes needed for specific target).

        Args:
            node: Node ID to get dependencies for

        Returns:
            Ordered list of all dependencies (including transitive)

        Raises:
            KeyError: If node doesn't exist in graph
        """
        if node not in self.graph:
            raise KeyError(f"Node not found in graph: {node}")

        # WHY: BFS to collect all reachable nodes from this node's dependencies
        visited = set()
        queue = deque(self.graph[node])

        while queue:
            dep = queue.popleft()
            if dep not in visited:
                visited.add(dep)
                # WHY: Add this node's dependencies to queue for transitive closure
                queue.extend(self.graph.get(dep, []))

        # WHY: Return in topological order for correct execution sequence
        all_order = self.topological_sort()
        subgraph = [n for n in all_order if n in visited]

        if self.verbose:
            print(
                f"Subgraph for '{node}': {len(subgraph)} dependencies", file=sys.stderr
            )

        return subgraph

    def filter_tasks(
        self, predicate: Callable[[str, Dict[str, Any]], bool]
    ) -> List[str]:
        """
        Filter nodes by custom predicate function.

        WHY: Enables flexible queries on the graph (e.g., "all nodes with status=pending").
             Maintains topological order in filtered results.

        Args:
            predicate: Function(node_id, node_data) -> bool

        Returns:
            Ordered list of node IDs that match predicate
        """
        # WHY: Filter nodes using predicate, maintain insertion order
        matching = [
            node_id
            for node_id, node_data in self.nodes.items()
            if predicate(node_id, node_data)
        ]

        # WHY: Return in topological order for correct execution sequence
        all_order = self.topological_sort()
        filtered = [n for n in all_order if n in matching]

        if self.verbose:
            print(f"Filter matched {len(filtered)} nodes", file=sys.stderr)

        return filtered


def main() -> int:
    """
    CLI entry point.

    WHY: Provides command-line interface for standalone usage.
         Supports multiple output formats for integration with different tools.
    """
    parser = argparse.ArgumentParser(
        description="Universal dependency resolver using topological sort",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dependency_resolver.py --input tasks.json --output order.txt
  python dependency_resolver.py --input deps.json --format json --verbose
  python dependency_resolver.py --input workflow.yaml --output plan.json --format json

Input format (JSON):
  {
    "nodes": {
      "task_A": {"deps": ["task_B", "task_C"], "status": "pending"},
      "task_B": {"deps": []},
      "task_C": {"deps": ["task_B"]}
    }
  }

Output format (text):
  task_B
  task_C
  task_A

Output format (json):
  ["task_B", "task_C", "task_A"]
        """,
    )

    parser.add_argument(
        "--input", "-i", required=True, help="Input graph file (JSON or YAML)"
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output to stderr"
    )

    args = parser.parse_args()

    try:
        # WHY: Initialize resolver with verbose flag
        resolver = DependencyResolver(verbose=args.verbose)

        # WHY: Load and validate graph
        resolver.load_graph(args.input)

        # WHY: Perform topological sort (will raise on cycles)
        order = resolver.topological_sort()

        # WHY: Format output based on requested format
        if args.format == "json":
            output = json.dumps(order, indent=2)
        else:  # text
            output = "\n".join(order)

        # WHY: Write to file or stdout based on arguments
        if args.output:
            atomic_write_text(Path(args.output), output + "\n")
            if args.verbose:
                print(f"Written to {args.output}", file=sys.stderr)
        else:
            print(output)

        # WHY: Exit with success code
        return 0

    except Exception as e:
        # WHY: Print error to stderr and exit with error code
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
