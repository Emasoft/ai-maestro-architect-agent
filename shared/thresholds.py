"""
thresholds.py - Shared constants for Architect Agent planning scripts.

These thresholds configure behavior for plan validation, task complexity,
and command execution timeouts.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanningConfig:
    """Configuration for plan validation thresholds."""

    # Required phases that must be present in every plan
    REQUIRED_PHASES: tuple[str, ...] = (
        "analysis",
        "design",
        "implementation",
        "testing",
        "deployment",
    )

    # Risk categories that should be covered
    RISK_CATEGORIES: tuple[str, ...] = (
        "technical",
        "schedule",
        "resource",
        "external",
    )

    # Minimum risks per category for comprehensive coverage
    MIN_RISKS_PER_CATEGORY: int = 1


@dataclass(frozen=True)
class TaskComplexityConfig:
    """Configuration for task complexity limits."""

    # Maximum number of top-level components in architecture
    MAX_TOP_LEVEL_COMPONENTS: int = 10

    # Maximum sub-components per top-level component
    MAX_SUB_COMPONENTS: int = 8

    # Maximum dependencies per task
    MAX_DEPENDENCIES_PER_TASK: int = 5


@dataclass(frozen=True)
class TimeoutsConfig:
    """Configuration for command execution timeouts."""

    # Default timeout for shell commands (seconds)
    COMMAND: float = 60.0

    # Timeout for long-running operations (seconds)
    LONG_RUNNING: float = 300.0

    # Timeout for quick checks (seconds)
    QUICK_CHECK: float = 10.0


# Singleton instances
PLANNING = PlanningConfig()
TASK_COMPLEXITY = TaskComplexityConfig()
TIMEOUTS = TimeoutsConfig()


def is_architecture_too_complex(
    top_level_count: int,
    max_sub_components: int,
) -> bool:
    """Check if architecture exceeds complexity thresholds.

    Args:
        top_level_count: Number of top-level components
        max_sub_components: Maximum sub-components in any component

    Returns:
        True if architecture is too complex, False otherwise
    """
    return (
        top_level_count > TASK_COMPLEXITY.MAX_TOP_LEVEL_COMPONENTS
        or max_sub_components > TASK_COMPLEXITY.MAX_SUB_COMPONENTS
    )
