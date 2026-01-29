#!/usr/bin/env python3
"""
Plugin Validator - Validate architect-agent plugin structure

This script validates:
1. Plugin manifest (plugin.json) structure
2. Agent definitions
3. Command definitions
4. Skill structure
5. Hook configuration
6. Script references
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List


class ValidationResult:
    """Validation result tracker."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: List[str] = []

    def error(self, msg: str) -> None:
        """Add error."""
        self.errors.append(f"❌ ERROR: {msg}")

    def warning(self, msg: str) -> None:
        """Add warning."""
        self.warnings.append(f"⚠️  WARNING: {msg}")

    def success(self, msg: str) -> None:
        """Add success."""
        self.passed.append(f"✓ {msg}")

    def print_results(self, verbose: bool = False) -> int:
        """Print validation results."""
        if verbose and self.passed:
            print("\n=== PASSED CHECKS ===")
            for msg in self.passed:
                print(msg)

        if self.warnings:
            print("\n=== WARNINGS ===")
            for msg in self.warnings:
                print(msg)

        if self.errors:
            print("\n=== ERRORS ===")
            for msg in self.errors:
                print(msg)

        # Summary
        print("\n=== SUMMARY ===")
        print(f"Passed: {len(self.passed)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors: {len(self.errors)}")

        # Exit code
        if self.errors:
            return 1
        elif self.warnings:
            return 2
        return 0


def validate_plugin(plugin_dir: Path, _verbose: bool = False) -> ValidationResult:
    """Validate plugin structure."""
    del _verbose  # Parameter kept for API compatibility
    result = ValidationResult()

    # Check plugin directory exists
    if not plugin_dir.exists():
        result.error(f"Plugin directory not found: {plugin_dir}")
        return result

    result.success(f"Plugin directory exists: {plugin_dir}")

    # Check plugin.json
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        result.error("plugin.json not found in .claude-plugin/")
        return result

    result.success("plugin.json exists")

    # Parse plugin.json
    try:
        with open(plugin_json) as f:
            manifest = json.load(f)
        result.success("plugin.json is valid JSON")
    except json.JSONDecodeError as e:
        result.error(f"plugin.json is invalid JSON: {e}")
        return result

    # Validate required fields
    required_fields = ["name", "version", "description"]
    for field in required_fields:
        if field not in manifest:
            result.error(f"plugin.json missing required field: {field}")
        else:
            result.success(f"plugin.json has {field}: {manifest[field]}")

    # Check directories
    dirs_to_check = ["agents", "commands", "skills", "scripts", "hooks"]
    for dir_name in dirs_to_check:
        dir_path = plugin_dir / dir_name
        if dir_path.exists():
            result.success(f"{dir_name}/ directory exists")
        else:
            result.warning(f"{dir_name}/ directory not found")

    # Check hooks.json
    hooks_json = plugin_dir / "hooks" / "hooks.json"
    if hooks_json.exists():
        try:
            with open(hooks_json) as f:
                json.load(f)  # Validate JSON syntax
            result.success("hooks.json is valid JSON")
        except json.JSONDecodeError as e:
            result.error(f"hooks.json is invalid JSON: {e}")
    else:
        result.warning("hooks.json not found")

    # Check scripts exist
    scripts_dir = plugin_dir / "scripts"
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob("*.py"))
        result.success(f"Found {len(scripts)} Python scripts")

        # Check scripts are executable
        for script in scripts:
            content = script.read_text()
            if not content.startswith("#!/usr/bin/env python3"):
                result.warning(f"Script missing shebang: {script.name}")

    return result


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate architect-agent plugin structure"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show all passed checks",
    )
    parser.add_argument(
        "--plugin-dir",
        type=Path,
        help="Path to plugin directory (default: current directory's parent)",
    )

    args = parser.parse_args()

    # Determine plugin directory
    if args.plugin_dir:
        plugin_dir = args.plugin_dir
    else:
        # Assume we're running from scripts/ directory
        plugin_dir = Path(__file__).parent.parent

    print(f"Validating plugin: {plugin_dir}")
    print("=" * 60)

    result = validate_plugin(plugin_dir, args.verbose)
    exit_code = result.print_results(args.verbose)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
