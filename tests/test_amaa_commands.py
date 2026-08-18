#!/usr/bin/env python3
"""Structural tests for the 4 slash commands (issue #14, M12).

Commands are markdown prompt files; "testing" them means asserting their
frontmatter and structure are well-formed so a broken command (bad frontmatter,
missing name/description, name/filename mismatch) is caught before publish. These
read the real command files shipped in commands/.

Frontmatter is parsed with a minimal dependency-free line parser (not pyyaml) so
the test runs under the publish pipeline's `uv run --with pytest pytest` command,
which does not install pyyaml.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
COMMANDS_DIR = REPO_ROOT / "commands"

EXPECTED_COMMANDS = {
    "amaa-add-requirement",
    "amaa-modify-requirement",
    "amaa-remove-requirement",
    "amaa-start-planning",
}


def command_files():
    return sorted(COMMANDS_DIR.glob("*.md"))


def split_frontmatter(text: str):
    """Return (frontmatter_dict, body) for a markdown file with YAML frontmatter.

    Minimal parser: top-level `key: value` lines only (no nesting needed for
    command frontmatter). Values keep their raw text; callers strip quotes.
    """
    assert text.startswith("---\n"), "file must open with a frontmatter block"
    end = text.index("\n---", 4)
    fm_block = text[4:end]
    body = text[end + 4 :]
    fm: dict[str, str] = {}
    for line in fm_block.splitlines():
        if not line or line[0] in " \t#":  # skip blanks, nested lines, comments
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip()
    return fm, body


def _unquote(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def test_all_expected_commands_present():
    """Exactly the 4 expected command files must ship."""
    found = {p.stem for p in command_files()}
    assert found == EXPECTED_COMMANDS, f"command set drift: {found ^ EXPECTED_COMMANDS}"


@pytest.mark.parametrize("cmd_path", command_files(), ids=lambda p: p.stem)
class TestCommandStructure:
    """Each command file must be structurally valid."""

    def test_frontmatter_has_keys(self, cmd_path):
        """The frontmatter must parse into at least name + description keys."""
        fm, _ = split_frontmatter(cmd_path.read_text(encoding="utf-8"))
        assert "name" in fm and "description" in fm

    def test_name_matches_filename(self, cmd_path):
        """The frontmatter `name` must equal the filename stem."""
        fm, _ = split_frontmatter(cmd_path.read_text(encoding="utf-8"))
        assert _unquote(fm.get("name", "")) == cmd_path.stem

    def test_description_present(self, cmd_path):
        """The frontmatter `description` must be a non-empty value."""
        fm, _ = split_frontmatter(cmd_path.read_text(encoding="utf-8"))
        assert _unquote(fm.get("description", "")).strip()

    def test_body_present(self, cmd_path):
        """There must be a non-empty body after the frontmatter."""
        _, body = split_frontmatter(cmd_path.read_text(encoding="utf-8"))
        assert body.strip(), f"{cmd_path.name}: empty body"

    def test_allowed_tools_is_flow_list_when_present(self, cmd_path):
        """If `allowed-tools` is present it must be a flow list (starts with '[')."""
        fm, _ = split_frontmatter(cmd_path.read_text(encoding="utf-8"))
        if "allowed-tools" in fm:
            assert fm["allowed-tools"].startswith("["), (
                f"{cmd_path.name}: allowed-tools must be a flow list, got {fm['allowed-tools']!r}"
            )
