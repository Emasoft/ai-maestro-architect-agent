#!/usr/bin/env python3
"""Plan validation script for atlas-orchestrator.

Validates that plan files meet all requirements:
- All required phases present
- Success criteria are measurable
- Dependencies form a valid DAG
- Risk coverage is complete
- Architecture complexity is acceptable

Exits with non-zero code if validation fails.
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import atomic_write_json  # type: ignore[import-not-found]  # noqa: E402
from thresholds import (  # type: ignore[import-not-found]  # noqa: E402
    PLANNING,
    TASK_COMPLEXITY,
    is_architecture_too_complex,
)


@dataclass
class ValidationResult:
    """Result of plan validation."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


def validate_phases(content: str) -> tuple[bool, list[str], list[str]]:
    """Validate all required phases are present."""
    errors: list[str] = []
    warnings: list[str] = []

    phase_pattern = r"^##\s+Phase\s+\d+[:\s]+(\w+)"
    found_phases = set()

    for match in re.finditer(phase_pattern, content, re.MULTILINE | re.IGNORECASE):
        phase_name = match.group(1).lower()
        found_phases.add(phase_name)

    required = set(PLANNING.REQUIRED_PHASES)
    missing = required - found_phases

    if missing:
        errors.append(f"Missing required phases: {', '.join(missing)}")

    extra = found_phases - required
    if extra:
        warnings.append(f"Extra phases found: {', '.join(extra)}")

    return len(errors) == 0, errors, warnings


def validate_architecture_complexity(content: str) -> tuple[bool, list[str], list[str]]:
    """Validate architecture doesn't exceed complexity thresholds."""
    errors: list[str] = []
    warnings: list[str] = []

    # Find component sections
    component_pattern = r"^###\s+Component[:\s]+(.+)"
    components = re.findall(component_pattern, content, re.MULTILINE)

    top_level_count = len(components)

    # Count sub-components per component
    max_sub = 0
    sub_pattern = r"^####\s+"
    sections = content.split("### Component")
    for section in sections[1:]:  # Skip content before first component
        sub_count = len(re.findall(sub_pattern, section, re.MULTILINE))
        max_sub = max(max_sub, sub_count)

    if is_architecture_too_complex(top_level_count, max_sub):
        if top_level_count > TASK_COMPLEXITY.MAX_TOP_LEVEL_COMPONENTS:
            errors.append(
                f"Too many top-level components: {top_level_count} "
                f"(max: {TASK_COMPLEXITY.MAX_TOP_LEVEL_COMPONENTS})"
            )
        if max_sub > TASK_COMPLEXITY.MAX_SUB_COMPONENTS:
            errors.append(
                f"Component has too many sub-components: {max_sub} "
                f"(max: {TASK_COMPLEXITY.MAX_SUB_COMPONENTS})"
            )

    return len(errors) == 0, errors, warnings


def validate_risk_coverage(content: str) -> tuple[bool, list[str], list[str]]:
    """Validate risk assessment covers all categories."""
    errors: list[str] = []
    warnings: list[str] = []

    # Find risk section
    risk_section_match = re.search(
        r"##\s+(?:Phase\s+\d+[:\s]+)?Risk.*?\n(.*?)(?=\n##|\Z)",
        content,
        re.IGNORECASE | re.DOTALL,
    )

    if not risk_section_match:
        errors.append("No risk assessment section found")
        return False, errors, warnings

    risk_content = risk_section_match.group(1).lower()

    # Check each category
    for category in PLANNING.RISK_CATEGORIES:
        if category not in risk_content:
            warnings.append(f"Risk category not explicitly addressed: {category}")

    # Count risks
    risk_items = re.findall(r"^[-*]\s+\[.\]\s+", risk_content, re.MULTILINE)

    min_required = len(PLANNING.RISK_CATEGORIES) * PLANNING.MIN_RISKS_PER_CATEGORY
    if len(risk_items) < min_required:
        warnings.append(
            f"Only {len(risk_items)} risks identified "
            f"(recommended minimum: {min_required})"
        )

    return len(errors) == 0, errors, warnings


def validate_task_dependencies(content: str) -> tuple[bool, list[str], list[str]]:
    """Validate task dependencies form a valid DAG."""
    errors: list[str] = []
    warnings: list[str] = []

    # Find tasks with dependencies
    task_pattern = r"^[-*]\s+\[.\]\s+(.+?)(?:\s+\(depends on:?\s*(.+?)\))?$"
    tasks = {}
    dependencies = {}

    for match in re.finditer(task_pattern, content, re.MULTILINE | re.IGNORECASE):
        task_name = match.group(1).strip()
        deps = match.group(2)

        # Generate task ID
        task_id = re.sub(r"[^a-z0-9]+", "-", task_name.lower())[:50]
        tasks[task_id] = task_name

        if deps:
            dep_list = [d.strip() for d in re.split(r"[,;]", deps)]
            dependencies[task_id] = dep_list

            if len(dep_list) > TASK_COMPLEXITY.MAX_DEPENDENCIES_PER_TASK:
                warnings.append(
                    f"Task '{task_name}' has {len(dep_list)} dependencies "
                    f"(max recommended: {TASK_COMPLEXITY.MAX_DEPENDENCIES_PER_TASK})"
                )

    # Check for circular dependencies (simple DFS)
    def has_cycle(node: str, visited: set[str], path: set[str]) -> bool:
        if node in path:
            return True
        if node in visited:
            return False

        visited.add(node)
        path.add(node)

        for dep in dependencies.get(node, []):
            # Normalize dependency reference
            dep_id = re.sub(r"[^a-z0-9]+", "-", dep.lower())[:50]
            if has_cycle(dep_id, visited, path):
                return True

        path.remove(node)
        return False

    visited: set[str] = set()
    for task_id in tasks:
        if has_cycle(task_id, visited, set()):
            errors.append(
                f"Circular dependency detected involving task: {tasks[task_id]}"
            )
            break

    return len(errors) == 0, errors, warnings


def validate_success_criteria(content: str) -> tuple[bool, list[str], list[str]]:
    """Validate success criteria are measurable."""
    errors: list[str] = []
    warnings: list[str] = []

    # Find success criteria sections
    criteria_pattern = r"(?:success criteria|acceptance criteria|done when)[:\s]*\n(.*?)(?=\n##|\n###|\Z)"
    matches = re.finditer(criteria_pattern, content, re.IGNORECASE | re.DOTALL)

    vague_terms = [
        "appropriate",
        "sufficient",
        "reasonable",
        "adequate",
        "good",
        "proper",
    ]

    for match in matches:
        criteria_text = match.group(1)

        for term in vague_terms:
            if term in criteria_text.lower():
                warnings.append(
                    f"Vague term '{term}' found in success criteria. "
                    "Replace with measurable threshold."
                )

    # Check for measurable indicators
    measurable_patterns = [
        r"\d+%",  # Percentages
        r"\d+\s*(hours?|days?|minutes?)",  # Time
        r"exit code\s*\d+",  # Exit codes
        r"at least\s+\d+",  # Minimums
        r"no more than\s+\d+",  # Maximums
    ]

    has_measurable = any(
        re.search(p, content, re.IGNORECASE) for p in measurable_patterns
    )

    if not has_measurable:
        warnings.append(
            "No measurable success criteria found (percentages, counts, etc.)"
        )

    return True, errors, warnings  # Warnings only, not blocking


def validate_plan(plan_path: Path) -> ValidationResult:
    """Validate a plan file."""
    result = ValidationResult(valid=True)

    if not plan_path.exists():
        result.valid = False
        result.errors.append(f"Plan file not found: {plan_path}")
        return result

    content = plan_path.read_text(encoding="utf-8")

    # Run all validations
    validations = [
        ("phases", validate_phases),
        ("architecture", validate_architecture_complexity),
        ("risks", validate_risk_coverage),
        ("dependencies", validate_task_dependencies),
        ("criteria", validate_success_criteria),
    ]

    for name, validator in validations:
        valid, errors, warnings = validator(content)

        if not valid:
            result.valid = False

        result.errors.extend([f"[{name}] {e}" for e in errors])
        result.warnings.extend([f"[{name}] {w}" for w in warnings])

    # Collect metrics
    result.metrics = {
        "file": str(plan_path),
        "size_bytes": len(content),
        "lines": content.count("\n") + 1,
        "phases_found": len(re.findall(r"^##\s+Phase", content, re.MULTILINE)),
        "tasks_found": len(re.findall(r"^[-*]\s+\[.\]", content, re.MULTILINE)),
        "risks_found": len(
            re.findall(r"^[-*]\s+\[.\].*risk", content, re.MULTILINE | re.IGNORECASE)
        ),
    }

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate plan files")
    parser.add_argument(
        "--input", "-i", type=Path, required=True, help="Plan file to validate"
    )
    parser.add_argument(
        "--output", "-o", type=Path, help="Output validation report as JSON"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )

    args = parser.parse_args()

    result = validate_plan(args.input)

    # Print results
    print(f"Validating: {args.input}")
    print("=" * 50)

    if result.errors:
        print("\nERRORS:")
        for error in result.errors:
            print(f"  ✗ {error}")

    if result.warnings:
        print("\nWARNINGS:")
        for warning in result.warnings:
            print(f"  ⚠ {warning}")

    print("\nMETRICS:")
    for key, value in result.metrics.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 50)

    if args.strict and result.warnings:
        result.valid = False
        result.errors.extend(result.warnings)

    if result.valid:
        print("✓ VALIDATION PASSED")
    else:
        print("✗ VALIDATION FAILED")

    # Output JSON if requested
    if args.output:
        atomic_write_json(
            args.output,
            {
                "valid": result.valid,
                "errors": result.errors,
                "warnings": result.warnings,
                "metrics": result.metrics,
            },
        )
        print(f"\nReport written to: {args.output}")

    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
