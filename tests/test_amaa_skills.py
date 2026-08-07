#!/usr/bin/env python3
"""Structural tests for the shipped SKILL.md files.

Skills are markdown prompt files; "testing" them means asserting their
frontmatter is well-formed so a broken skill is caught before publish rather
than by a user whose workflow silently changes shape.

The load-bearing test here is `test_fork_skill_declares_background`. Claude Code
2.1.218 changed `context: fork` skills to run in the BACKGROUND by default, with
`background: false` as the per-skill opt-out. Every AMAA fork skill has a
synchronous body ("consult the reference doc -> follow the protocol -> report
back"), and the main agent's workflow consumes those results inline, so
background-by-default turns them into fire-and-forget: no error, no warning, the
caller just never receives the answer. Relying on the harness default is
therefore unsafe in EITHER direction — this suite requires the value to be
written down explicitly so a future default flip cannot move AMAA's behavior
without a failing test.

Frontmatter is parsed with a minimal dependency-free line parser (not pyyaml) so
the test runs under the publish pipeline's `uv run --with pytest pytest` command,
which does not install pyyaml.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# Claude Code 2.1.218 widened frontmatter booleans beyond true/false.
ACCEPTED_BOOLEANS = {
    "true",
    "false",
    "yes",
    "no",
    "on",
    "off",
    "1",
    "0",
}

BOOLEAN_FIELDS = ("background", "user-invocable", "disable-model-invocation")


def skill_files():
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def split_frontmatter(text: str):
    """Return (frontmatter_dict, body) for a markdown file with YAML frontmatter.

    Minimal parser: top-level `key: value` lines only. Nested lines (indented)
    are skipped, which is correct here — no skill frontmatter field this suite
    asserts on is nested.
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


def test_skills_directory_is_not_empty():
    """A globbing mistake must fail loudly, not silently parametrize zero cases."""
    assert skill_files(), f"no SKILL.md found under {SKILLS_DIR}"


@pytest.mark.parametrize("skill_path", skill_files(), ids=lambda p: p.parent.name)
class TestSkillStructure:
    """Each shipped SKILL.md must be structurally valid."""

    def test_frontmatter_has_keys(self, skill_path):
        """The frontmatter must parse into at least name + description keys."""
        fm, _ = split_frontmatter(skill_path.read_text(encoding="utf-8"))
        assert "name" in fm and "description" in fm

    def test_name_matches_directory(self, skill_path):
        """The frontmatter `name` must equal the containing directory name."""
        fm, _ = split_frontmatter(skill_path.read_text(encoding="utf-8"))
        assert _unquote(fm.get("name", "")) == skill_path.parent.name

    def test_description_present(self, skill_path):
        """The frontmatter `description` must be a non-empty value."""
        fm, _ = split_frontmatter(skill_path.read_text(encoding="utf-8"))
        assert _unquote(fm.get("description", "")).strip()

    def test_body_present(self, skill_path):
        """There must be a non-empty body after the frontmatter."""
        _, body = split_frontmatter(skill_path.read_text(encoding="utf-8"))
        assert body.strip(), f"{skill_path.parent.name}: empty body"

    def test_fork_skill_declares_background(self, skill_path):
        """A `context: fork` skill must state `background:` explicitly.

        Claude Code 2.1.218 made fork skills background-by-default. AMAA's fork
        skills are synchronous consults, so the harness default is wrong for
        them — and a default that flips again later must not be able to change
        AMAA's runtime behavior silently. Requiring the explicit key makes any
        such flip a test failure instead of a silent semantic change.
        """
        fm, _ = split_frontmatter(skill_path.read_text(encoding="utf-8"))
        if _unquote(fm.get("context", "")) != "fork":
            pytest.skip("not a fork skill")
        assert "background" in fm, (
            f"{skill_path.parent.name}: `context: fork` without an explicit "
            "`background:` — CC 2.1.218 would run it in the background, so the "
            "caller would never receive its result. Declare `background: false` "
            "(synchronous consult) or `background: true` (deliberate async)."
        )

    def test_booleans_use_accepted_spellings(self, skill_path):
        """Boolean frontmatter values must use a spelling the CLI accepts."""
        fm, _ = split_frontmatter(skill_path.read_text(encoding="utf-8"))
        for field in BOOLEAN_FIELDS:
            if field in fm:
                value = _unquote(fm[field]).lower()
                assert value in ACCEPTED_BOOLEANS, (
                    f"{skill_path.parent.name}: {field}={fm[field]!r} is not an "
                    f"accepted boolean spelling {sorted(ACCEPTED_BOOLEANS)}"
                )

    def test_agent_reference_has_no_colon(self, skill_path):
        """An `agent:` value must not contain ':' — reserved for plugin namespacing.

        Claude Code 2.1.218 made agent markdown files reject names containing
        ':'. A skill pointing at such a name would resolve to nothing.
        """
        fm, _ = split_frontmatter(skill_path.read_text(encoding="utf-8"))
        if "agent" not in fm:
            pytest.skip("skill declares no agent")
        agent = _unquote(fm["agent"])
        assert ":" not in agent, (
            f"{skill_path.parent.name}: agent {agent!r} contains ':', which CC "
            "2.1.218 rejects (reserved for plugin namespacing)"
        )


def test_every_fork_skill_is_synchronous():
    """AMAA ships no deliberately-async skill yet — assert that intent holds.

    This is the counterpart to the per-skill test: it pins the *fleet-visible*
    decision (every fork skill is a synchronous consult) rather than merely that
    a value was written. Adopting `background: true` for a genuinely long-running
    skill is a design change that must also rewrite the caller's completion
    protocol, so it should land as a deliberate edit to this test, never as a
    drive-by frontmatter tweak.
    """
    async_skills = []
    for skill_path in skill_files():
        fm, _ = split_frontmatter(skill_path.read_text(encoding="utf-8"))
        if _unquote(fm.get("context", "")) != "fork":
            continue
        if _unquote(fm.get("background", "")).lower() not in {"false", "no", "off", "0"}:
            async_skills.append(skill_path.parent.name)
    assert not async_skills, (
        "these fork skills are background/async: "
        f"{async_skills}. If that is intended, update the caller completion "
        "protocol in amaa-design-communication-patterns first, then amend this test."
    )
