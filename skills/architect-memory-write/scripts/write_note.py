#!/usr/bin/env python3
"""architect-memory-write — author one schema-valid markdown memory note.

Writes `<memdir>/<name>.md` with the canonical frontmatter and appends the
index line to `<memdir>/MEMORY.md` (creating it if missing). Fail-fast:
invalid input or a name collision aborts with a specific error and NO
partial writes (the note is written before the index line, and the index
append happens only after the note write succeeded).

Exit codes: 0 written; 1 note already exists; 2 validation/usage error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

VALID_TYPES = ("user", "feedback", "project", "reference")
KEBAB_SET = set("abcdefghijklmnopqrstuvwxyz0123456789-")


def is_kebab(name: str) -> bool:
    return bool(name) and all(c in KEBAB_SET for c in name) and not name.startswith("-") and not name.endswith("-")


def title_from(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Write one markdown memory note")
    parser.add_argument("--memdir", required=True, help="Markdown memory directory")
    parser.add_argument("--name", required=True, help="kebab-case note slug (filename stem)")
    parser.add_argument("--description", required=True, help="Symptom-side recall surface")
    parser.add_argument("--type", required=True, choices=VALID_TYPES, dest="note_type")
    parser.add_argument("--title", default="", help="Human title (default: derived from name)")
    parser.add_argument("--body", default="", help="Note body (read from stdin when omitted)")
    args = parser.parse_args()

    name = args.name.strip()
    if not is_kebab(name):
        print(f"invalid name (must be kebab-case): {name!r}", file=sys.stderr)
        return 2
    description = args.description.strip()
    if not description:
        print("empty description — the description is the recall surface", file=sys.stderr)
        return 2
    body = args.body if args.body else sys.stdin.read()
    body = body.strip()
    if not body:
        print("empty body — a note must carry exactly one fact", file=sys.stderr)
        return 2

    memdir = Path(args.memdir).expanduser()
    memdir.mkdir(parents=True, exist_ok=True)
    note_path = memdir / f"{name}.md"
    if note_path.exists():
        print(f"note exists: {note_path} — edit it or pick a new name", file=sys.stderr)
        return 1

    title = args.title.strip() or title_from(name)
    escaped_description = description.replace('"', "'")
    note_text = (
        "---\n"
        f"name: {name}\n"
        f'description: "{escaped_description}"\n'
        "metadata:\n"
        "  node_type: memory\n"
        f"  type: {args.note_type}\n"
        "---\n"
        "\n"
        f"{body}\n"
    )
    note_path.write_text(note_text, encoding="utf-8")

    index_path = memdir / "MEMORY.md"
    index_line = f"- [{title}]({name}.md) — {description}\n"
    with index_path.open("a", encoding="utf-8") as index_file:
        index_file.write(index_line)

    print(f"wrote {note_path}")
    print(f"indexed: {index_line.strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
