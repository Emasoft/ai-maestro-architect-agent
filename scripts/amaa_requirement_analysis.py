#!/usr/bin/env python3
"""
Requirement Analysis Script for Emasoft Architect Agent

This script performs proactive requirement analysis to identify potential issues
BEFORE implementation begins. It enforces RULE 14: User Requirements Are Immutable.

Usage:
    python requirement-analysis.py init --project-root <path>
    python requirement-analysis.py parse --input <file_or_text>
    python requirement-analysis.py analyze --requirements <file>
    python requirement-analysis.py report --issue <description> --requirement <id>
    python requirement-analysis.py validate --implementation <path>

The script helps orchestrators:
1. Parse and document user requirements
2. Analyze feasibility of requirements
3. Detect conflicts between requirements
4. Generate requirement issue reports
5. Validate implementation against requirements
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_timestamp() -> str:
    """Return timestamp in format YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_requirements_dir(project_root: Path) -> Path:
    """Create requirements directory structure."""
    req_dir = project_root / "docs_dev" / "requirements"
    issues_dir = project_root / "docs_dev" / "requirement-issues"

    req_dir.mkdir(parents=True, exist_ok=True)
    issues_dir.mkdir(parents=True, exist_ok=True)

    return req_dir


def init_requirements(project_root: Path, project_name: str) -> None:
    """Initialize requirements tracking for a project."""
    req_dir = ensure_requirements_dir(project_root)

    # Create USER_REQUIREMENTS.md
    user_req_file = req_dir / "USER_REQUIREMENTS.md"
    if not user_req_file.exists():
        content = f"""# User Requirements - {project_name}

## Status: IMMUTABLE - Only user can modify these requirements

## About This Document

This document records ALL user requirements verbatim. Requirements are absolute
axioms that cannot be changed by the orchestrator or any agent without explicit
user approval.

**RULE 14**: User requirements are immutable. Any proposed changes must be:
1. Documented in a Requirement Issue Report
2. Presented to the user for decision
3. Only implemented after explicit user approval

---

## Requirements

### REQ-001: [Requirement Title]
- **User Statement**: "[exact quote from user]"
- **Recorded**: {get_timestamp()}
- **Status**: IMMUTABLE
- **Category**: [Technology/Feature/Constraint/Design]
- **User Decision**: [if any clarification was made]

---

## Requirement Categories

- **Technology**: User-specified technologies, frameworks, languages
- **Feature**: User-requested functionality and capabilities
- **Constraint**: User-specified limitations or boundaries
- **Design**: User-specified architecture or design decisions

---

## Change Log

| Date | Requirement | Change | User Decision |
|------|-------------|--------|---------------|
| | | | |

"""
        user_req_file.write_text(content, encoding="utf-8")
        print(f"Created: {user_req_file}")

    # Create REQUIREMENT_DECISIONS.md
    decisions_file = req_dir / "REQUIREMENT_DECISIONS.md"
    if not decisions_file.exists():
        content = f"""# Requirement Decisions Log - {project_name}

## Purpose

This document logs ALL user decisions regarding requirements. When requirement
issues arise, the user's decision is recorded here for future reference.

---

## Decisions

### DECISION-001: [Decision Title]
- **Date**: {get_timestamp()}
- **Related Requirement**: REQ-XXX
- **Issue**: [What issue was raised]
- **Options Presented**: [What alternatives were offered]
- **User Decision**: [What the user decided]
- **Rationale**: [Why user made this decision]
- **Implemented**: [Yes/No/Pending]

---

## Decision Summary

| ID | Requirement | Decision | Date |
|----|-------------|----------|------|
| | | | |

"""
        decisions_file.write_text(content, encoding="utf-8")
        print(f"Created: {decisions_file}")

    # Create REQUIREMENT_ANALYSIS.md
    analysis_file = req_dir / "REQUIREMENT_ANALYSIS.md"
    if not analysis_file.exists():
        content = f"""# Requirement Feasibility Analysis - {project_name}

## Purpose

This document contains the orchestrator's analysis of requirement feasibility.
This analysis does NOT change requirements - it identifies potential issues
for user review.

---

## Analysis Summary

| Requirement | Feasibility | Issues | Status |
|-------------|-------------|--------|--------|
| | | | |

---

## Detailed Analysis

### REQ-001 Analysis
- **Requirement**: [quote]
- **Feasibility**: [Feasible/Challenging/Infeasible]
- **Technical Considerations**: [details]
- **Potential Issues**: [if any]
- **Recommendation**: [for user consideration only]

---

## Conflict Analysis

### Conflict-001: [Title]
- **Requirements**: REQ-XXX vs REQ-YYY
- **Conflict Description**: [details]
- **Resolution Options**: [for user to choose]
- **User Decision**: [pending]

---

## Risk Assessment

| Risk | Severity | Affected Requirements | Mitigation |
|------|----------|----------------------|------------|
| | | | |

"""
        analysis_file.write_text(content, encoding="utf-8")
        print(f"Created: {analysis_file}")

    print(f"\nRequirements tracking initialized for: {project_name}")
    print(f"Directory: {req_dir}")


def parse_requirements(
    input_text: str, output_file: Optional[Path] = None
) -> list[dict[str, str]]:
    """
    Parse user statements to extract requirements.

    Looks for patterns like:
    - "I want X"
    - "Must have X"
    - "Use X for Y"
    - "Build X"
    - "Should support X"
    """
    requirements: list[dict[str, str]] = []

    # Patterns that indicate requirements
    patterns = [
        r"(?:I want|I need|must have|should have|need to have)\s+(.+?)(?:\.|$)",
        r"(?:Use|Build|Create|Make|Implement)\s+(.+?)(?:\.|$)",
        r"(?:Must|Should|Need to)\s+(?:be able to\s+)?(.+?)(?:\.|$)",
        r"(?:Support|Include|Add)\s+(.+?)(?:\.|$)",
        r"(?:Target|Deploy to|Run on)\s+(.+?)(?:\.|$)",
    ]

    req_id = 1
    for pattern in patterns:
        matches = re.finditer(pattern, input_text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            req: dict[str, str] = {
                "id": f"REQ-{req_id:03d}",
                "statement": match.group(0).strip(),
                "extracted": match.group(1).strip(),
                "timestamp": get_timestamp(),
                "status": "IMMUTABLE",
                "category": "Unclassified",
            }
            requirements.append(req)
            req_id += 1

    if output_file:
        output_file.write_text(json.dumps(requirements, indent=2), encoding="utf-8")
        print(f"Parsed {len(requirements)} requirements to: {output_file}")

    return requirements


def generate_issue_report(
    project_root: Path,
    requirement_id: str,
    requirement_text: str,
    issue_type: str,
    issue_description: str,
    alternatives: list[str],
) -> Path:
    """
    Generate a Requirement Issue Report.

    This report is generated when the orchestrator identifies an issue with
    a user requirement. The user must review and decide how to proceed.
    """
    issues_dir = project_root / "docs_dev" / "requirement-issues"
    issues_dir.mkdir(parents=True, exist_ok=True)

    timestamp = get_timestamp()
    safe_id = requirement_id.replace("-", "_").lower()
    filename = f"{timestamp}-{safe_id}-issue.md"
    report_path = issues_dir / filename

    alternatives_text = "\n".join(
        f"{i + 1}. {alt}" for i, alt in enumerate(alternatives)
    )

    content = f"""# Requirement Issue Report

**Date**: {timestamp}
**Requirement**: {requirement_id}
**Issue Type**: {issue_type}

---

## The Requirement

> {requirement_text}

---

## The Issue

{issue_description}

---

## Impact

If we proceed with the requirement as specified:
[Impact analysis here]

---

## Possible Alternatives (FOR USER CONSIDERATION ONLY)

{alternatives_text}

---

## Orchestrator Recommendation

**SUGGESTION ONLY - User must decide**

[Orchestrator's recommendation here]

---

## AWAITING USER DECISION

The orchestrator will NOT proceed until the user explicitly:
- [ ] Confirms original requirement (proceed as specified)
- [ ] Modifies the requirement (update specification)
- [ ] Chooses an alternative (specify which one)

---

## User Decision

**Decision**: [To be filled by user]

**Rationale**: [To be filled by user]

**Date**: [To be filled by user]

---

## Implementation Notes

After user decision:
- Update USER_REQUIREMENTS.md if requirement changed
- Log decision in REQUIREMENT_DECISIONS.md
- Proceed with implementation per user's direction

"""

    report_path.write_text(content, encoding="utf-8")
    print(f"Generated issue report: {report_path}")
    return report_path


def validate_implementation(
    project_root: Path, implementation_path: Path
) -> dict[str, str | list[str] | int]:
    """
    Validate that implementation matches user requirements.

    This checks for potential violations of RULE 14 by comparing
    what was implemented against what was required.
    """
    req_file = project_root / "docs_dev" / "requirements" / "USER_REQUIREMENTS.md"

    if not req_file.exists():
        return {
            "status": "ERROR",
            "message": "USER_REQUIREMENTS.md not found. Run 'init' first.",
        }

    # Parse requirements from file
    req_content = req_file.read_text(encoding="utf-8")

    # Basic validation - check if implementation files exist
    if not implementation_path.exists():
        return {
            "status": "ERROR",
            "message": f"Implementation path not found: {implementation_path}",
        }

    # Look for technology keywords in requirements
    tech_patterns = {
        "electron": r"\belectron\b",
        "rust": r"\brust\b",
        "python": r"\bpython\b",
        "typescript": r"\btypescript\b",
        "javascript": r"\bjavascript\b",
        "react": r"\breact\b",
        "vue": r"\bvue\b",
        "gui": r"\b(?:gui|graphical|visual|window)\b",
        "cli": r"\b(?:cli|command.?line|terminal)\b",
    }

    required_tech: list[str] = []
    for tech, pattern in tech_patterns.items():
        if re.search(pattern, req_content, re.IGNORECASE):
            required_tech.append(tech)

    # Check implementation for matching technologies
    # This is a simplified check - real implementation would be more thorough
    impl_files = list(implementation_path.rglob("*"))
    impl_extensions = set(f.suffix.lower() for f in impl_files if f.is_file())

    # Use typed local variables to avoid dict indexing type issues
    potential_issues: list[str] = []
    recommendations: list[str] = []
    status = "PENDING_REVIEW"

    # Check for GUI vs CLI mismatch
    if "gui" in required_tech and ".html" not in impl_extensions:
        potential_issues.append(
            "User requested GUI but no HTML files found in implementation"
        )

    if "electron" in required_tech:
        has_electron = any("electron" in str(f).lower() for f in impl_files)
        if not has_electron:
            potential_issues.append(
                "User requested Electron but no Electron files detected"
            )

    if potential_issues:
        status = "POTENTIAL_VIOLATION"
        recommendations.append("Review implementation against USER_REQUIREMENTS.md")
        recommendations.append(
            "Generate Requirement Issue Report if deviation confirmed"
        )

    return {
        "status": status,
        "required_technologies": required_tech,
        "implementation_files": len(impl_files),
        "file_extensions": list(impl_extensions),
        "potential_issues": potential_issues,
        "recommendations": recommendations,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Requirement Analysis for Emasoft Architect Agent (RULE 14 Enforcement)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize requirements tracking")
    init_parser.add_argument(
        "--project-root", type=Path, required=True, help="Project root directory"
    )
    init_parser.add_argument(
        "--project-name",
        type=str,
        default="Project",
        help="Project name for documentation",
    )

    # parse command
    parse_parser = subparsers.add_parser("parse", help="Parse requirements from text")
    parse_parser.add_argument(
        "--input", type=str, required=True, help="Input text or file path"
    )
    parse_parser.add_argument(
        "--output", type=Path, help="Output JSON file for parsed requirements"
    )

    # report command
    report_parser = subparsers.add_parser(
        "report", help="Generate requirement issue report"
    )
    report_parser.add_argument(
        "--project-root", type=Path, required=True, help="Project root directory"
    )
    report_parser.add_argument(
        "--requirement-id",
        type=str,
        required=True,
        help="Requirement ID (e.g., REQ-001)",
    )
    report_parser.add_argument(
        "--requirement-text", type=str, required=True, help="Exact requirement text"
    )
    report_parser.add_argument(
        "--issue-type",
        type=str,
        required=True,
        choices=["Feasibility", "Conflict", "Ambiguity", "Technical Limitation"],
        help="Type of issue",
    )
    report_parser.add_argument(
        "--description", type=str, required=True, help="Issue description"
    )
    report_parser.add_argument(
        "--alternatives",
        type=str,
        nargs="+",
        default=[],
        help="Alternative approaches for user consideration",
    )

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate implementation")
    validate_parser.add_argument(
        "--project-root", type=Path, required=True, help="Project root directory"
    )
    validate_parser.add_argument(
        "--implementation",
        type=Path,
        required=True,
        help="Implementation directory to validate",
    )

    args = parser.parse_args()

    if args.command == "init":
        init_requirements(args.project_root, args.project_name)

    elif args.command == "parse":
        input_text = args.input
        if os.path.isfile(input_text):
            input_text = Path(input_text).read_text(encoding="utf-8")
        requirements = parse_requirements(input_text, args.output)
        if not args.output:
            print(json.dumps(requirements, indent=2))

    elif args.command == "report":
        report_path = generate_issue_report(
            args.project_root,
            args.requirement_id,
            args.requirement_text,
            args.issue_type,
            args.description,
            args.alternatives,
        )
        print(f"Report generated: {report_path}")

    elif args.command == "validate":
        result = validate_implementation(args.project_root, args.implementation)
        print(json.dumps(result, indent=2))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
