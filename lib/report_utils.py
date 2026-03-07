"""Shared reporting utility — write verbose output to file, print summary to stdout.

All scripts should use report_output() instead of printing verbose content directly.
This ensures callers (agents, orchestrators, users) only see a concise summary,
while the full output is available in a timestamped file for on-demand reading.

NO external dependencies — Python 3.8+ stdlib only.
"""

import os
from datetime import datetime
from pathlib import Path


def report_output(
    script_name: str,
    summary: str,
    full_content: str,
    report_dir: str = "docs_dev/reports",
    exit_code: int = 0,
) -> str:
    """Write full_content to timestamped file, print summary + path to stdout.

    Args:
        script_name: Name of the calling script (used in filename).
        summary: 1-3 line concise summary printed to stdout.
        full_content: Full verbose output saved to file.
        report_dir: Directory for report files (relative to project root).
        exit_code: Exit code context (0=success, 1=failure). Affects prefix.

    Returns:
        Relative path to the report file.
    """
    project_root = Path(os.environ.get("CLAUDE_PROJECT_ROOT", str(Path.cwd())))
    report_path = project_root / report_dir
    report_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{script_name}_{timestamp}.md"
    filepath = report_path / filename
    filepath.write_text(full_content, encoding="utf-8")

    try:
        rel_path = str(filepath.relative_to(project_root))
    except ValueError:
        rel_path = str(filepath)

    status = "DONE" if exit_code == 0 else "FAILED"
    output = f"[{status}] {script_name} - {summary}\nFull report: {rel_path}"
    print(output)
    return rel_path


def make_report_header(script_name: str, args: dict | None = None) -> str:
    """Generate a standard markdown header for a report file.

    Args:
        script_name: Name of the script generating the report.
        args: Optional dict of CLI arguments to include.

    Returns:
        Markdown header string.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"# Report: {script_name}\n\n"
    header += f"**Generated:** {timestamp}\n"
    if args:
        header += f"**Arguments:** {args}\n"
    header += "\n---\n\n"
    return header
