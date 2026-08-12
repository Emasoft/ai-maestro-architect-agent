#!/usr/bin/env python3
"""Suite-wide convention: never select a markdown SECTION by first match.

Origin (ai-maestro#131). A guard that slices a document with `str.find` /
`str.index` takes whichever occurrence comes first, which may be a
true-but-irrelevant one — a cross-reference in prose rather than the section
itself. The guard then passes or fails for reasons unrelated to the invariant it
claims to test. The COS hit this three times in one day; their selector anchored
on the first `out.summary(` chose a WARN early-exit whose window could never
contain the text under test, reddening a correct file.

**Why this test exists rather than another round of per-site fixes.** Both that
agent and this one fixed one selector, and both then found a second selector of
the same shape in their own tree that the first fix had not prompted them to
check. Fixing an instance is not fixing a class, and the condition under which
this rots is precisely "nothing is red, so nothing prompts the look" — every
anchor happens to be unique today. So the convention is enforced by a test
instead of remembered.

**Scope is deliberately narrow.** This bans first-match selection of *markdown
sections* (anchors containing `##` or `**`), which is where the defect lives. It
does NOT ban `.find`/`.index` generally, because several uses are correct by
definition and a guard that fires on them would be noise that trains everyone to
ignore it:

  - a frontmatter terminator — the FIRST `\\n---` after the opening delimiter IS
    the boundary, not an arbitrary pick;
  - a YAML field lookup (`^uuid:`) — the first match IS the field;
  - a CLI argv position (`argv.index("--priority")`).

The sanctioned way to select a section is `_select_unique()`: refuse on
ambiguity, AND assert the slice carries a marker only the real section can carry.
Either half alone is weaker — uniqueness still silently picks a unique-but-wrong
anchor, and a content check alone still picks by position when the anchor repeats.

**Measured coverage, stated because a guard's blind spot is worth more than its
hit rate.** Run against this repo's own pre-fix commit (5a12a5b), it catches
**one of the two** selectors that were live there:

  - CAUGHT  `text.find("## Communication Permissions")` — literal anchor.
  - MISSED  `marker = "**Inbound discipline**"` … `persona.find(marker)` — the
    anchor is a VARIABLE, so a source-level pattern cannot see it.

So this is a net, not a proof. It catches the common inline shape and will not
catch an indirected one; a reviewer still has to look. Widening it to resolve
variables would mean parsing rather than matching, and a pattern that silently
misses a case is safer than one that pretends to cover it.
"""

import re
from pathlib import Path

TESTS_DIR = Path(__file__).parent
SELF = Path(__file__).name

# `.find("## X")` / `.index("**Y**")` — a NAMED section anchor passed to a
# first-match selector. Matches the literal-string form only; that is the shape
# that bites.
#
# The anchor must carry a heading marker AND a title (>=2 word chars). That
# second requirement is load-bearing and was found by falsifying this detector
# rather than by reasoning: without it the pattern flags
# `text.find("\n## ", start + 1)`, which is the section-END search — a bare
# delimiter, applied from an offset, after the START was already property-
# selected. Flagging it would have made this guard fire on correct code, which is
# how a guard earns its way into being ignored.
FIRST_MATCH_SECTION_SELECT = re.compile(
    r"""\.\s*(?:find|index)\s*\(\s*(['"])"""
    r"""(?P<anchor>(?=[^'"]*(?:\#\#|\*\*))(?=[^'"]*\w{2})[^'"]*)\1"""
)


def _test_files() -> list[Path]:
    return sorted(p for p in TESTS_DIR.glob("test_*.py") if p.name != SELF)


def test_there_are_test_files_to_scan():
    """A convention test that scans nothing passes vacuously."""
    assert _test_files(), "no test files found — this guard would assert nothing"


def test_no_markdown_section_is_selected_by_first_match():
    offenders: list[str] = []
    for path in _test_files():
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue  # a comment describing the anti-pattern is not the anti-pattern
            m = FIRST_MATCH_SECTION_SELECT.search(line)
            if m:
                offenders.append(f"{path.name}:{i} selects {m.group('anchor')!r} by first match")
    assert not offenders, (
        "markdown sections must be selected via _select_unique() (refuse on ambiguity + "
        "assert the slice carries a real-section marker), never by first match:\n  "
        + "\n  ".join(offenders)
    )


def test_the_detector_actually_catches_the_shape():
    """A convention guard nobody has falsified is a decoration.

    Verified against the exact pre-fix forms from this repo's own history, and
    against the legitimate uses it must NOT flag.
    """
    caught = [
        'start = text.find("## Communication Permissions")',
        'start = persona.index("**Inbound discipline**")',
        "  s = doc.find('### **Inbound discipline** — three channels')",
    ]
    for line in caught:
        assert FIRST_MATCH_SECTION_SELECT.search(line), f"detector missed the anti-pattern: {line!r}"

    ignored = [
        'end = text.index("\\n---", 4)',  # frontmatter terminator — correct by definition
        'match = re.search(r"^uuid:\\s*(.+)$", content, re.MULTILINE)',  # field lookup
        'assert argv[argv.index("--priority") + 1] == "high"',  # argv position
        'nxt = text.find("\\n## ", start + 1)',  # section END, after a property-selected start
    ]
    for line in ignored:
        assert not FIRST_MATCH_SECTION_SELECT.search(line), f"detector false-positived on: {line!r}"
