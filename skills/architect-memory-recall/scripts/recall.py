#!/usr/bin/env python3
"""architect-memory-recall — symptom-ranked recall over a markdown memory dir.

Prefers `memgrep recall` when the binary is on PATH; otherwise ranks notes
with a built-in scorer so recall DEGRADES, NEVER BREAKS (issue #13 contract).

Ranking (fallback): tokenize the symptom into words of >= 3 chars; a note
scores 3 points per token hit on its recall SURFACE (frontmatter
`description:` / `title:` / `tags:` values) and 1 point per token hit in the
body. Zero-score notes are suppressed. Output best-first:
    <path> — <description>

Exit codes: 0 on success (including "no matches" and "memory dir missing" —
absence of memory is a normal state, not a failure); 2 on bad usage.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

SURFACE_WEIGHT = 3
BODY_WEIGHT = 1
MIN_TOKEN_LEN = 3


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter, body). Empty frontmatter when none present."""
    if text.startswith("---"):
        parts = text.split("\n---", 2)
        if len(parts) >= 2:
            return parts[0], parts[-1]
    return "", text


def surface_of(frontmatter: str) -> str:
    """Extract the recall surface: description, title, tags values."""
    surface_lines: list[str] = []
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if re.match(r"^(description|title|tags)\s*:", stripped):
            surface_lines.append(stripped.split(":", 1)[1])
    return " ".join(surface_lines)


def description_of(frontmatter: str) -> str:
    """Extract the description value for display."""
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if stripped.startswith("description:"):
            return stripped.split(":", 1)[1].strip().strip("\"'")
    return ""


def tokenize(symptom: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[A-Za-z0-9_-]+", symptom) if len(t) >= MIN_TOKEN_LEN]


def score_note(tokens: list[str], text: str) -> int:
    frontmatter, body = split_frontmatter(text)
    surface = surface_of(frontmatter).lower()
    body_lower = body.lower()
    score = 0
    for token in tokens:
        if token in surface:
            score += SURFACE_WEIGHT
        if token in body_lower:
            score += BODY_WEIGHT
    return score


def fallback_recall(symptom: str, memdir: Path, limit: int) -> int:
    tokens = tokenize(symptom)
    if not tokens:
        print("no matching memories")
        return 0
    scored: list[tuple[int, str, str]] = []
    for note in sorted(memdir.rglob("*.md")):
        if note.name == "MEMORY.md":
            continue  # the index is not a memory
        try:
            text = note.read_text(encoding="utf-8")
        except OSError:
            continue
        score = score_note(tokens, text)
        if score > 0:
            frontmatter, _ = split_frontmatter(text)
            scored.append((score, str(note), description_of(frontmatter)))
    if not scored:
        print("no matching memories")
        return 0
    scored.sort(key=lambda item: (-item[0], item[1]))
    for _, path, description in scored[:limit]:
        print(f"{path} — {description}" if description else path)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Symptom-ranked memory recall")
    parser.add_argument("symptom", help="The symptom/question wording to search for")
    parser.add_argument("--memdir", required=True, help="Markdown memory directory")
    parser.add_argument("--limit", type=int, default=10, help="Max notes to print")
    args = parser.parse_args()

    memdir = Path(args.memdir).expanduser()
    if not memdir.is_dir():
        print(f"memory dir not found: {memdir}")
        return 0  # a project without memories is a normal state

    if shutil.which("memgrep"):
        result = subprocess.run(
            ["memgrep", "recall", args.symptom, str(memdir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            print(output if output else "no matching memories")
            return 0
        # memgrep present but failing: degrade for THIS invocation, say so.
        print("memgrep failed — using built-in fallback ranker", file=sys.stderr)

    return fallback_recall(args.symptom, memdir, args.limit)


if __name__ == "__main__":
    sys.exit(main())
