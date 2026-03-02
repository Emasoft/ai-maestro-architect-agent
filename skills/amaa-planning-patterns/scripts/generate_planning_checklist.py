#!/usr/bin/env python3
"""
Generate a customized planning checklist for a project.

Usage:
    python generate-planning-checklist.py --project "MyProject" --phases 4 --output checklist.md

Arguments:
    --project: Project name (required)
    --phases: Number of phases (default: 4)
    --output: Output file path (default: checklist-{date}.md)
    --help: Show this help message
"""

# WHY: Future annotations enable forward references and modern type hint syntax
from __future__ import annotations

# WHY: Standard library imports grouped together for clarity
import argparse
import sys
from datetime import datetime
from pathlib import Path

# WHY: Dynamic path insertion allows importing shared utilities from skill directory
SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import atomic_write_text  # type: ignore[import-not-found]  # noqa: E402


def verify_output_file(output_path: Path) -> bool:
    """
    Verify that the output file was written successfully.

    WHY: Post-write verification ensures file was actually created and is non-empty,
    catching silent write failures that might occur with atomic writes or filesystem issues.

    Args:
        output_path: Path to the file that should exist

    Returns:
        True if file exists and is non-empty, False otherwise
    """
    if not output_path.exists():
        return False
    if output_path.stat().st_size == 0:
        return False
    return True


def generate_planning_checklist(
    project_name: str, phases: int, output_file: str | Path | None = None
) -> None:
    """
    Generate a planning checklist for the given project.

    WHY: This function encapsulates checklist generation logic separate from CLI handling,
    making it reusable as a library function and easier to test.
    """
    output_path: Path
    if output_file is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_path = Path(f"checklist-{date_str}.md")
    else:
        output_path = Path(output_file)

    content = f"""# Planning Checklist: {project_name}

Project: {project_name}
Phases: {phases}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Pre-Planning

Before starting the planning process, verify:

- [ ] Project goal is clear and documented
- [ ] Stakeholders are identified
- [ ] Success criteria are defined
- [ ] Constraints are documented (timeline, budget, resources)
- [ ] Key assumptions are listed
- [ ] Planning team is assembled
- [ ] Time is allocated for planning (4-5 weeks minimum)

## Architecture Design Phase

Complete these items as you design your system architecture:

- [ ] System components are identified
- [ ] Each component has a single, clear responsibility
- [ ] Component interfaces are defined
- [ ] Data flows are documented with examples
- [ ] Dependencies between components are mapped
- [ ] Architecture document is complete
- [ ] Stakeholders have reviewed and approved
- [ ] No blockers preventing next phase

**Target completion date**: ___________

## Risk Identification Phase

Complete these items as you identify and plan for risks:

- [ ] At least 15 risks have been identified
- [ ] Risks span multiple categories (technical, business, security, etc.)
- [ ] Each risk has impact and probability assessed
- [ ] Risk score has been calculated (Impact × Probability)
- [ ] Mitigation strategy exists for each risk
- [ ] High-risk mitigations are scheduled in roadmap
- [ ] Risk monitoring indicators are defined
- [ ] Risk register is complete and stakeholders approved
- [ ] No blockers preventing next phase

**Target completion date**: ___________

## Roadmap Creation Phase

Complete these items as you create your execution roadmap:

- [ ] Project is broken into {phases} phases
- [ ] Each phase has clear entry/exit criteria
- [ ] Phases are sequenced by dependencies
- [ ] Milestones are defined for each phase
- [ ] Deliverables are specific and measurable
- [ ] Resources are allocated to each phase
- [ ] Buffer time is included (minimum 20% of phase length)
- [ ] Master roadmap is created (visual timeline)
- [ ] Stakeholders have reviewed and approved roadmap
- [ ] No blockers preventing next phase

**Target completion date**: ___________

## Implementation Planning Phase

Complete these items as you plan implementation tasks:

- [ ] Each milestone is broken into tasks (1-5 days each)
- [ ] Each task has clear owner assigned
- [ ] Task dependencies are mapped
- [ ] Tasks are ordered by dependency
- [ ] Daily stand-up process is defined
- [ ] Weekly status reporting is planned
- [ ] Change management process is defined
- [ ] Team understands and commits to plan
- [ ] No blockers preventing execution

**Target completion date**: ___________

## Post-Planning Verification

After all planning is complete, verify:

- [ ] Architecture design document is approved
- [ ] Risk register is approved
- [ ] Roadmap is approved
- [ ] Implementation plan is approved
- [ ] All stakeholders have signed off
- [ ] Team has resources needed
- [ ] Development environment is ready
- [ ] Version control is set up
- [ ] Monitoring and alerting is planned
- [ ] Ready to begin execution

## Sign-Off

### Architecture Review

Reviewed by: _________________ Date: _______

Comments: _________________________________________________________________

Approved: ☐ Yes ☐ No

### Risk Review

Reviewed by: _________________ Date: _______

Comments: _________________________________________________________________

Approved: ☐ Yes ☐ No

### Roadmap Review

Reviewed by: _________________ Date: _______

Comments: _________________________________________________________________

Approved: ☐ Yes ☐ No

### Implementation Plan Review

Reviewed by: _________________ Date: _______

Comments: _________________________________________________________________

Approved: ☐ Yes ☐ No

### Project Sponsor Sign-Off

Sponsor: _________________ Date: _______

Project approved to proceed: ☐ Yes ☐ No

Comments: _________________________________________________________________

## Notes

Use this space for any additional notes or decisions made during planning:

_____________________________________________________________________________

_____________________________________________________________________________

_____________________________________________________________________________

_____________________________________________________________________________

---

**Planning complete when**: All items above are checked and all stakeholders have signed off.

**Next step**: Begin execution according to the approved implementation plan.
"""

    # WHY: atomic_write_text ensures file is written completely or not at all
    atomic_write_text(output_path, content)

    # WHY: Post-write verification catches silent failures from filesystem issues
    if not verify_output_file(output_path):
        raise RuntimeError(
            f"Verification failed: output file not created or empty: {output_path}"
        )

    print(f"Planning checklist generated: {output_path}")


def main() -> None:
    """
    CLI entry point for generating planning checklists.

    WHY: Separate main function allows the script to be imported without executing,
    and provides clean error handling with proper exit codes.
    """
    parser = argparse.ArgumentParser(
        description="Generate a planning checklist for your project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate-planning-checklist.py --project "MyProject"
  python generate-planning-checklist.py --project "MyProject" --phases 5 --output my-checklist.md
        """,
    )

    parser.add_argument("--project", required=True, help="Project name (required)")
    parser.add_argument(
        "--phases", type=int, default=4, help="Number of phases (default: 4)"
    )
    parser.add_argument(
        "--output", default=None, help="Output file path (default: checklist-{date}.md)"
    )

    args = parser.parse_args()

    try:
        generate_planning_checklist(args.project, args.phases, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # WHY: Explicit exit(0) signals successful completion to calling processes and CI systems
    sys.exit(0)


if __name__ == "__main__":
    main()
