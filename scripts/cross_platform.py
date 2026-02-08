#!/usr/bin/env python3
"""Cross-platform utility functions for architect-agent scripts."""

import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Any


def atomic_write_json(path: Path, data: Any, indent: int = 2) -> None:
    """Atomically write JSON data to a file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file first, then move atomically
    with tempfile.NamedTemporaryFile(
        mode="w", dir=path.parent, suffix=".tmp", delete=False, encoding="utf-8"
    ) as tmp:
        json.dump(data, tmp, indent=indent)
        tmp_path = Path(tmp.name)

    shutil.move(str(tmp_path), str(path))


def atomic_write_text(path: Path, content: str) -> None:
    """Atomically write text content to a file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w", dir=path.parent, suffix=".tmp", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    shutil.move(str(tmp_path), str(path))


def run_command(
    cmd: list[str], cwd: Path | None = None, timeout: float | None = None
) -> tuple[int, str, str]:
    """Run a command and return (exit_code, stdout, stderr).

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory (optional)
        timeout: Timeout in seconds (optional)

    Returns:
        Tuple of (exit_code, stdout, stderr)

    Raises:
        TimeoutError: If command exceeds timeout
    """
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as e:
        raise TimeoutError(
            f"Command timed out after {timeout}s: {' '.join(cmd)}"
        ) from e
