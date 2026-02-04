#!/usr/bin/env python3
"""
Universal Analyzer Tool Scaffold Generator

WHY: Creates standardized analysis tools with consistent structure, reducing boilerplate
     and ensuring all analyzers follow the same patterns for maintainability.
"""

import argparse
import sys
from pathlib import Path
from textwrap import dedent
from typing import Dict

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))

from cross_platform import atomic_write_text  # type: ignore[import-not-found]  # noqa: E402


class AnalyzerScaffoldGenerator:
    """Generates analyzer tool scaffolds based on category templates."""

    CATEGORIES = {
        "dependency": "Dependency analysis (imports, packages, version conflicts)",
        "bundle": "Bundle analysis (size, composition, optimization)",
        "coverage": "Code coverage analysis (test coverage, gaps)",
        "performance": "Performance analysis (bottlenecks, profiling)",
        "security": "Security analysis (vulnerabilities, best practices)",
        "custom": "Custom analysis (generic template)",
    }

    def __init__(self, name: str, category: str, output: Path):
        self.name = name
        self.category = category
        self.output = output
        self.class_name = self._to_class_name(name)

    def _to_class_name(self, name: str) -> str:
        """Convert snake_case to PascalCase for class names."""
        # WHY: Class names should follow PEP 8 PascalCase convention
        return "".join(word.capitalize() for word in name.split("_"))

    def _get_category_methods(self) -> Dict[str, str]:
        """Return category-specific method implementations."""
        # WHY: Different analysis types need different default implementations

        templates = {
            "dependency": self._dependency_template,
            "bundle": self._bundle_template,
            "coverage": self._coverage_template,
            "performance": self._performance_template,
            "security": self._security_template,
            "custom": self._custom_template,
        }

        return templates.get(self.category, self._custom_template)()

    def _dependency_template(self) -> Dict[str, str]:
        """Template for dependency analysis tools."""
        return {
            "validate": '''        """Validate target is a valid dependency source."""
        # WHY: Early validation prevents wasted analysis time
        if not self.target.exists():
            raise FileNotFoundError(f"Target not found: {self.target}")

        # Add dependency-specific validation (requirements.txt, package.json, etc.)
        return True
            ''',
            "analyze": '''        """Analyze dependencies and their relationships."""
        # WHY: Structured analysis makes results queryable and actionable
        results = {
            'dependencies': [],
            'conflicts': [],
            'outdated': [],
            'security_issues': []
        }

        # Add dependency scanning logic here
        if self.verbose:
            print(f"Analyzing dependencies in {self.target}")

        return results
            ''',
            "description": "Dependency analysis (imports, packages, version conflicts)",
        }

    def _bundle_template(self) -> Dict[str, str]:
        """Template for bundle analysis tools."""
        return {
            "validate": '''        """Validate target is a valid bundle."""
        # WHY: Early validation prevents wasted analysis time
        if not self.target.exists():
            raise FileNotFoundError(f"Target not found: {self.target}")

        return True
            ''',
            "analyze": '''        """Analyze bundle size, composition, and optimization opportunities."""
        # WHY: Structured analysis makes results queryable and actionable
        results = {
            'total_size': 0,
            'components': [],
            'duplicates': [],
            'optimization_suggestions': []
        }

        # Add bundle analysis logic here
        if self.verbose:
            print(f"Analyzing bundle at {self.target}")

        return results
            ''',
            "description": "Bundle analysis (size, composition, optimization)",
        }

    def _coverage_template(self) -> Dict[str, str]:
        """Template for coverage analysis tools."""
        return {
            "validate": '''        """Validate target has coverage data."""
        # WHY: Early validation prevents wasted analysis time
        if not self.target.exists():
            raise FileNotFoundError(f"Target not found: {self.target}")

        return True
            ''',
            "analyze": '''        """Analyze code coverage and identify gaps."""
        # WHY: Structured analysis makes results queryable and actionable
        results = {
            'coverage_percentage': 0.0,
            'covered_lines': 0,
            'total_lines': 0,
            'uncovered_files': [],
            'gaps': []
        }

        # Add coverage analysis logic here
        if self.verbose:
            print(f"Analyzing coverage for {self.target}")

        return results
            ''',
            "description": "Code coverage analysis (test coverage, gaps)",
        }

    def _performance_template(self) -> Dict[str, str]:
        """Template for performance analysis tools."""
        return {
            "validate": '''        """Validate target can be profiled."""
        # WHY: Early validation prevents wasted analysis time
        if not self.target.exists():
            raise FileNotFoundError(f"Target not found: {self.target}")

        return True
            ''',
            "analyze": '''        """Analyze performance and identify bottlenecks."""
        # WHY: Structured analysis makes results queryable and actionable
        results = {
            'execution_time': 0.0,
            'bottlenecks': [],
            'memory_usage': {},
            'optimization_suggestions': []
        }

        # Add performance analysis logic here
        if self.verbose:
            print(f"Analyzing performance of {self.target}")

        return results
            ''',
            "description": "Performance analysis (bottlenecks, profiling)",
        }

    def _security_template(self) -> Dict[str, str]:
        """Template for security analysis tools."""
        return {
            "validate": '''        """Validate target can be scanned for security issues."""
        # WHY: Early validation prevents wasted analysis time
        if not self.target.exists():
            raise FileNotFoundError(f"Target not found: {self.target}")

        return True
            ''',
            "analyze": '''        """Scan for security vulnerabilities and best practice violations."""
        # WHY: Structured analysis makes results queryable and actionable
        results = {
            'vulnerabilities': [],
            'warnings': [],
            'best_practice_violations': [],
            'severity_counts': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        }

        # Add security scanning logic here
        if self.verbose:
            print(f"Scanning {self.target} for security issues")

        return results
            ''',
            "description": "Security analysis (vulnerabilities, best practices)",
        }

    def _custom_template(self) -> Dict[str, str]:
        """Template for custom analysis tools."""
        return {
            "validate": '''        """Validate target is suitable for analysis."""
        # WHY: Early validation prevents wasted analysis time
        if not self.target.exists():
            raise FileNotFoundError(f"Target not found: {self.target}")

        # Add custom validation logic here
        return True
            ''',
            "analyze": '''        """Perform custom analysis."""
        # WHY: Structured analysis makes results queryable and actionable
        results = {
            'findings': [],
            'metrics': {},
            'suggestions': []
        }

        # Add custom analysis logic here
        if self.verbose:
            print(f"Analyzing {self.target}")

        return results
            ''',
            "description": "Custom analysis (generic template)",
        }

    def generate(self) -> str:
        """Generate complete analyzer script."""
        # WHY: Template-based generation ensures consistency across all analyzers

        methods = self._get_category_methods()

        template = f'''#!/usr/bin/env python3
"""
{self.class_name} - {methods["description"]}

WHY: Provides automated analysis for {self.category} concerns, enabling
     data-driven decisions and early problem detection.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / 'shared'))
from cross_platform import atomic_write_json, atomic_write_text


class {self.class_name}:
    """
    {methods["description"]}

    WHY: Class-based structure allows for state management, easy testing,
         and extension through inheritance.
    """

    def __init__(self, target: Path, verbose: bool = False):
        """
        Initialize analyzer.

        Args:
            target: Path to analyze
            verbose: Enable verbose output

        WHY: Centralizes configuration and makes the analyzer reusable
        """
        self.target = target
        self.verbose = verbose
        self.results: Optional[Dict[str, Any]] = None

    def validate(self) -> bool:
        """
        Validate that the target is suitable for analysis.

        Returns:
            True if validation passes

        Raises:
            FileNotFoundError: If target doesn't exist
            ValueError: If target is invalid

        WHY: Fail-fast approach prevents invalid analysis and unclear errors
        """
{methods["validate"]}

    def analyze(self) -> Dict[str, Any]:
        """
        Perform the analysis.

        Returns:
            Dictionary containing analysis results

        WHY: Returning structured data enables programmatic consumption
             and further processing
        """
{methods["analyze"]}

    def report(self, output: Optional[Path] = None, json_format: bool = False) -> None:
        """
        Generate and output the analysis report.

        Args:
            output: Optional output file path
            json_format: Output in JSON format

        WHY: Flexible output supports both human and machine consumption
        """
        if self.results is None:
            raise RuntimeError("No results to report. Call analyze() first.")

        if json_format:
            # WHY: JSON enables integration with other tools and pipelines
            if output:
                atomic_write_json(self.results, output)
                if self.verbose:
                    print(f"JSON report written to {{output}}")
            else:
                print(json.dumps(self.results, indent=2, default=str))
        else:
            # WHY: Human-readable format for direct consumption
            report_lines = [
                f"{self.class_name} Report",
                "=" * 50,
                f"Target: {{self.target}}",
                "",
                "Results:",
            ]

            for key, value in self.results.items():
                report_lines.append(f"  {{key}}: {{value}}")

            report_text = "\\n".join(report_lines)

            if output:
                atomic_write_text(report_text, output)
                if self.verbose:
                    print(f"Report written to {{output}}")
            else:
                print(report_text)


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success, non-zero for failure)

    WHY: Proper exit codes enable shell scripting and CI/CD integration
    """
    parser = argparse.ArgumentParser(
        description="{methods["description"]}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'target',
        type=Path,
        help='Path to analyze'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output in JSON format'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Write report to file instead of stdout'
    )

    args = parser.parse_args()

    try:
        # WHY: Separate validation, analysis, and reporting allows for
        #      easier testing and debugging of each phase
        analyzer = {self.class_name}(args.target, verbose=args.verbose)
        analyzer.validate()
        analyzer.results = analyzer.analyze()
        analyzer.report(output=args.output, json_format=args.json)
        return 0

    except FileNotFoundError as e:
        print(f"Error: {{e}}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Validation error: {{e}}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Unexpected error: {{e}}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 3


if __name__ == '__main__':
    sys.exit(main())
'''

        return template

    def write(self) -> None:
        """Write generated scaffold to output file."""
        # WHY: File I/O separated from generation for easier testing

        content = self.generate()
        self.output.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_text(self.output, content)
        self.output.chmod(0o755)  # WHY: Make executable for direct CLI use

        if self.output.stat().st_size > 0:
            print("DONE analyzer_scaffold.py created")
        else:
            raise RuntimeError("Generated file is empty")


def main() -> int:
    """Main entry point for scaffold generator."""
    parser = argparse.ArgumentParser(
        description="Generate analyzer tool scaffolds with consistent structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(f"""
        Available categories:
        {chr(10).join(f"  {cat}: {desc}" for cat, desc in AnalyzerScaffoldGenerator.CATEGORIES.items())}

        Example usage:
          python analyzer_scaffold.py --name coverage_analyzer --category coverage --output my_analyzer.py
          python analyzer_scaffold.py --name security_scanner --category security --output scanner.py
        """),
    )

    parser.add_argument(
        "--name", required=True, help="Name for the analyzer (snake_case recommended)"
    )

    parser.add_argument(
        "--category",
        required=True,
        choices=list(AnalyzerScaffoldGenerator.CATEGORIES.keys()),
        help="Analysis category",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output file path for generated analyzer",
    )

    args = parser.parse_args()

    try:
        generator = AnalyzerScaffoldGenerator(
            name=args.name, category=args.category, output=args.output
        )
        generator.write()
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
