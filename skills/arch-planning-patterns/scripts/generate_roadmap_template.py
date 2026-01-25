#!/usr/bin/env python3
"""
Generate a roadmap template with phases and milestones.

ATLAS-ORCHESTRATOR: NO TIME ESTIMATIONS - Focus on what needs to be done, not when.

Usage:
    python generate-roadmap-template.py --phases 4 --output roadmap.md

Arguments:
    --phases: Number of phases (default: 4)
    --output: Output file path (default: roadmap.md)
    --help: Show this help message
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import atomic_write_text  # type: ignore[import-not-found]  # noqa: E402


def verify(output_path: Path) -> None:
    """Verify that the output file exists and is non-empty after writing.

    WHY: Fail-fast verification ensures we catch write failures immediately
    rather than discovering missing files later in the workflow.
    """
    if not output_path.exists():
        raise RuntimeError(
            f"Verification failed: output file does not exist: {output_path}"
        )
    if output_path.stat().st_size == 0:
        raise RuntimeError(f"Verification failed: output file is empty: {output_path}")


def generate_roadmap_template(phases: int, output_file: str) -> None:
    """Generate a milestone-based roadmap template with no time estimations."""
    # WHY: Using f-strings for template generation because it maintains readability
    # while allowing dynamic content insertion for phase counts and dates
    content = f"""# Project Roadmap

**Project**: [Project Name]
**Number of Phases**: {phases}
**Generated**: {datetime.now().strftime("%Y-%m-%d")}

## Executive Summary

[1-2 sentence summary of what will be built and key outcomes]

## Phase Overview

"""

    for p in range(1, phases + 1):
        content += f"Phase {p}: [Phase Name]\n"

    content += """
## Phases

"""
    # WHY: Each phase has consistent structure to ensure all planning aspects are covered
    # Entry/exit criteria enforce clear phase boundaries and prevent scope creep
    for p in range(1, phases + 1):
        content += f"""### Phase {p}: [Phase Name]

**Purpose**: [What will be accomplished in this phase]

**Components**:
- [Component 1]
- [Component 2]
- [Component 3]

**Entry Criteria**:
- [Requirement 1]
- [Requirement 2]

**Exit Criteria / Deliverables**:
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

**Milestones**:
- [Milestone 1: Early phase checkpoint]
- [Milestone 2: Mid-phase checkpoint]
- [Milestone 3: Phase completion]

**Team**:
- [Role]: [Person] ([% allocation])
- [Role]: [Person] ([% allocation])

**Budget**: $[amount]

**Risks**: [R-001, R-002, ...]

---

"""

    content += """## Key Milestones

"""
    # WHY: Three milestones per phase (early, mid, completion) provide regular checkpoints
    # without over-constraining the team with excessive milestone overhead
    milestone_num = 1
    for p in range(1, phases + 1):
        content += f"- Phase {p} Milestone {milestone_num}: [Early checkpoint]\n"
        milestone_num += 1
        content += f"- Phase {p} Milestone {milestone_num}: [Mid checkpoint]\n"
        milestone_num += 1
        content += f"- Phase {p} Milestone {milestone_num}: [Completion]\n"
        milestone_num += 1

    content += """
## Resource Allocation

### Team Composition

- [Role]: [Person] - [Phases involved]
- [Role]: [Person] - [Phases involved]
- [Role]: [Person] - [Phases involved]

### Budget Breakdown

| Phase | Personnel | Infrastructure | Services | Contingency | Total |
|-------|-----------|-----------------|----------|------------|-------|
"""

    for p in range(1, phases + 1):
        content += f"| Phase {p} | $[X] | $[X] | $[X] | $[X] | $[X] |\n"

    content += "| **Total** | **$[X]** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |\n"

    content += """
## Dependencies

### Inter-Phase Dependencies

"""
    # WHY: Sequential phase dependencies are the default; teams can modify for parallel phases
    for p in range(2, phases + 1):
        content += f"- Phase {p} depends on: Phase {p - 1}\n"

    content += """
### External Dependencies

- [Service/Team]: [Dependency]
- [Service/Team]: [Dependency]

## Critical Risks

| Risk ID | Risk Name | Impact | Probability | Mitigation |
|---------|-----------|--------|-------------|------------|
| R-001 | [Name] | [Impact] | [Probability] | [Mitigation] |
| R-002 | [Name] | [Impact] | [Probability] | [Mitigation] |

See Risk Register for complete list.

## Success Criteria

**Project Launch Criteria**:
- [ ] All {phases} phases are complete
- [ ] All deliverables are tested and approved
- [ ] All stakeholders have signed off
- [ ] Production environment is ready
- [ ] Monitoring and alerting is configured
- [ ] Go/No-Go decision: [Criteria for launch decision]

**Post-Launch Metrics**:
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
- [Metric 3]: [Target value]

## Assumptions

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]
- [Assumption 4]
- [Assumption 5]

## Constraints

- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

## Stakeholder Sign-Off

| Stakeholder | Role | Approval |
|-------------|------|----------|
| [Name] | [Role] | ☐ |
| [Name] | [Role] | ☐ |
| [Name] | [Role] | ☐ |

## Notes

[Additional notes, decisions, or context about the roadmap]

---

**Roadmap approved by**: _________________

**Roadmap review**: [As needed based on phase completion]
""".format(phases=phases)
    # WHY: atomic_write_text ensures file is written completely or not at all,
    # preventing partial/corrupt files on disk full or interrupt scenarios
    output_path = Path(output_file)
    atomic_write_text(content, output_path)

    # WHY: Verification after write ensures the file was actually created and is non-empty
    verify(output_path)

    print(f"Milestone-based roadmap template generated: {output_file}")


def main() -> None:
    # WHY: Using argparse for CLI to provide help text and validation automatically
    parser = argparse.ArgumentParser(
        description="Generate a milestone-based project roadmap template (no time estimations)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate-roadmap-template.py
  python generate-roadmap-template.py --phases 5 --output roadmap.md
  python generate-roadmap-template.py --phases 3
        """,
    )

    parser.add_argument(
        "--phases", type=int, default=4, help="Number of phases (default: 4)"
    )
    parser.add_argument(
        "--output", default="roadmap.md", help="Output file path (default: roadmap.md)"
    )

    args = parser.parse_args()

    try:
        generate_roadmap_template(args.phases, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # WHY: Explicit exit(0) signals success to calling scripts and CI/CD pipelines
    sys.exit(0)


if __name__ == "__main__":
    main()
