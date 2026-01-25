#!/usr/bin/env python3
"""
Generate an empty risk register template.

Usage:
    python generate-risk-register.py --template markdown --output risks.md
    python generate-risk-register.py --template csv --risks 25 --output risks.csv

Arguments:
    --template: Format (markdown, csv, json) (default: markdown)
    --risks: Number of risk rows to pre-allocate (default: 20)
    --output: Output file path (default: risk-register.{ext})
    --help: Show this help message
"""

# WHY: Future annotations enable forward references and modern type hint syntax
from __future__ import annotations

import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "shared"))
from cross_platform import (  # type: ignore[import-not-found]  # noqa: E402
    atomic_write_json,
    atomic_write_text,
)


# WHY: Verification function ensures file was actually written to disk
# This catches silent write failures and disk-full conditions
def verify(output_path: Path) -> None:
    """Verify that output file exists and is non-empty after writing."""
    if not output_path.exists():
        raise RuntimeError(f"Verification failed: {output_path} was not created")
    if output_path.stat().st_size == 0:
        raise RuntimeError(f"Verification failed: {output_path} is empty")


# WHY: Markdown format is human-readable and works in GitHub/GitLab wikis
def generate_markdown_register(num_risks: int, output_file: str) -> None:
    """Generate a markdown-formatted risk register."""
    content = """# Risk Register

Date: {date}
Total Risks: {count}

## Risk Summary

| Risk ID | Risk Name | Impact | Probability | Score | Status |
|---------|-----------|--------|-------------|-------|--------|
""".format(date=datetime.now().strftime("%Y-%m-%d"), count=num_risks)

    # Add empty rows
    for i in range(1, num_risks + 1):
        content += f"| R-{i:03d} | | | | | |\n"

    content += """
## Detailed Risk Descriptions

"""

    for i in range(1, min(num_risks + 1, 6)):  # Show first 5 as examples
        content += f"""### Risk R-{i:03d}: [Risk Name]

**Description**: [Specific description of what could go wrong]

**Impact**: [CRITICAL / HIGH / MEDIUM / LOW]
- [Effect 1]
- [Effect 2]

**Probability**: [HIGH / MEDIUM / LOW]
- [Reason 1]
- [Reason 2]

**Risk Score**: [Impact] × [Probability] = [URGENT / IMPORTANT / MONITOR / LOW]

**Mitigation Strategy**: [Strategy type: Prevent / Reduce / Transfer / Accept]
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Owner**: [Person responsible]
**Target Date**: [When mitigation must be complete]
**Monitoring Indicator**: [How will we know if this risk is occurring?]
**Status**: [Not Started / In Progress / Complete / Mitigated]

---

"""

    content += """## Legend

**Impact Scale**:
- CRITICAL: Complete project failure or major consequences
- HIGH: Significant impact on schedule, budget, or quality
- MEDIUM: Notable impact but manageable
- LOW: Minor impact, easily managed

**Probability Scale**:
- HIGH: Likely to occur (>60% chance)
- MEDIUM: Possible (20-60% chance)
- LOW: Unlikely (<20% chance)

**Risk Score**:
- CRITICAL × HIGH = URGENT (address immediately)
- CRITICAL × MEDIUM = URGENT
- HIGH × HIGH = URGENT
- HIGH × MEDIUM = IMPORTANT
- MEDIUM × HIGH = IMPORTANT
- All others = MONITOR or LOW

**Mitigation Types**:
- Prevent: Actions to prevent risk from occurring
- Reduce: Actions to reduce probability or impact
- Transfer: Move risk to someone else (insurance, outsourcing)
- Accept: Acknowledge and accept the risk

---

**Instructions**: Fill in all required fields for each risk. Use this register to track risks throughout the project lifecycle.
"""

    output_path = Path(output_file)
    atomic_write_text(content, output_path)
    # WHY: Verify write succeeded before reporting success
    verify(output_path)

    print(f"Risk register (markdown) generated: {output_file}")


# WHY: CSV format integrates with spreadsheet tools (Excel, Google Sheets)
def generate_csv_register(num_risks: int, output_file: str) -> None:
    """Generate a CSV-formatted risk register."""
    lines = [
        "Risk_ID,Risk_Name,Description,Impact,Probability,Risk_Score,"
        "Mitigation_Strategy,Owner,Target_Date,Monitoring_Indicator,Status,Notes"
    ]

    for i in range(1, num_risks + 1):
        risk_id = f"R-{i:03d}"
        lines.append(f"{risk_id},,,,,,,,,,")

    content = "\n".join(lines)

    output_path = Path(output_file)
    atomic_write_text(content, output_path)
    # WHY: Verify write succeeded before reporting success
    verify(output_path)

    print(f"Risk register (CSV) generated: {output_file}")


# WHY: JSON format enables programmatic processing and API integration
def generate_json_register(num_risks: int, output_file: str) -> None:
    """Generate a JSON-formatted risk register."""
    register: dict[str, Any] = {
        "project": "Project Name",
        "generated": datetime.now().isoformat(),
        "total_risks": num_risks,
        "risks": [],
    }

    for i in range(1, num_risks + 1):
        register["risks"].append(
            {
                "risk_id": f"R-{i:03d}",
                "name": "",
                "description": "",
                "impact": "",  # CRITICAL, HIGH, MEDIUM, LOW
                "probability": "",  # HIGH, MEDIUM, LOW
                "risk_score": "",  # Calculated
                "mitigation_strategy": "",  # Prevent, Reduce, Transfer, Accept
                "mitigation_steps": [],
                "owner": "",
                "target_date": "",
                "monitoring_indicator": "",
                "status": "",  # Not Started, In Progress, Complete, Mitigated
                "notes": "",
            }
        )

    output_path = Path(output_file)
    atomic_write_json(register, output_path)
    # WHY: Verify write succeeded before reporting success
    verify(output_path)

    print(f"Risk register (JSON) generated: {output_file}")


# WHY: Main function handles CLI parsing and dispatches to format-specific generators
def main() -> None:
    """Parse arguments and generate risk register."""
    parser = argparse.ArgumentParser(
        description="Generate a risk register template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate-risk-register.py
  python generate-risk-register.py --template markdown --risks 30 --output risks.md
  python generate-risk-register.py --template csv --output project-risks.csv
  python generate-risk-register.py --template json --risks 20
        """,
    )

    parser.add_argument(
        "--template",
        choices=["markdown", "csv", "json"],
        default="markdown",
        help="Template format (default: markdown)",
    )
    parser.add_argument(
        "--risks",
        type=int,
        default=20,
        help="Number of risk rows to pre-allocate (default: 20)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: risk-register.{ext})",
    )

    args = parser.parse_args()

    if args.output is None:
        ext_map = {"markdown": "md", "csv": "csv", "json": "json"}
        args.output = f"risk-register.{ext_map[args.template]}"

    try:
        if args.template == "markdown":
            generate_markdown_register(args.risks, args.output)
        elif args.template == "csv":
            generate_csv_register(args.risks, args.output)
        elif args.template == "json":
            generate_json_register(args.risks, args.output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # WHY: Explicit success exit code for shell script integration
    sys.exit(0)


if __name__ == "__main__":
    main()
