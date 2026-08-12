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
hit rate.** Against this repo's own pre-fix commit (5a12a5b): **2 of 2**.

  - `text.find("## Communication Permissions")` — literal anchor.
  - `marker = "**Inbound discipline**"` … `persona.find(marker)` — resolved.

An earlier regex version scored 1 of 2 (it could not see through a variable).
Two rounds of correction got here, and each round's fix was aimed at a different
indirection than the one that actually bit:

  - The COS resolved **module-level** constants — matching *their* miss
    (`HEADING = "..."` at module scope), measured 2 of 2 on their tree.
  - Adopted unmodified it still scored 1 of 2 on mine, because *my* miss was
    **function-local**. So resolution here covers any `NAME = "literal"` binding
    in the file, whichever scope it sits in.

That is the reusable lesson: a fix verified on the tree that produced it can be
vacuous on the next tree while looking like an upgrade. Re-measure after adopting.

**Still a net, not a proof.** Runtime-built anchors (f-strings, concatenation,
values read from disk) and parameters remain invisible — going further means
evaluating rather than parsing. Collecting names across scopes can in principle
mis-resolve a name reused in two functions; that produces a loud false positive,
never a silent miss, which is the correct direction for a net to fail in.
"""

import ast
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


def _is_section_anchor(s: str) -> bool:
    """A NAMED markdown section: a heading marker plus an actual title."""
    return bool(re.search(r"\#\#|\*\*", s)) and bool(re.search(r"\w{2}", s))


def _offenders_in(path: Path) -> list[str]:
    """Report `.find`/`.index` calls whose anchor names a markdown section.

    Uses `ast` rather than a source regex so a **module-level constant** anchor is
    resolved before matching. Credit: ai-maestro-chief-of-staff on ai-maestro#131.
    My earlier regex version scored 1 of 2 on my own tree and would have scored
    **0 of 2 on theirs**, where every selector is `HEADING = "..."` then
    `.index(HEADING)` — a guard incapable of catching the pattern it was written
    for, shipping green. That is this issue's own failure mode reproduced inside
    its own fix, and it was only visible because they published the miss list.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:  # a syntactically broken test file fails elsewhere, loudly
        return []

    # Every `NAME = "literal"` binding in the file, module-level OR function-local.
    # The COS's version resolved module-level only, which matched THEIR miss
    # (`HEADING = "..."` at module scope). Re-measured on my own pre-fix commit it
    # still scored 1 of 2, because MY miss was function-local:
    #     marker = "**Inbound discipline**"   # inside the helper
    #     start = persona.find(marker)
    # Same class, different indirection — so adopting their fix unmodified would
    # have left my actual historical miss uncaught while looking like an upgrade.
    # Collecting all scopes can in principle mis-resolve a name reused across
    # functions; that yields a loud false positive, never a silent miss, which is
    # the right direction for a net.
    consts: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name):
                        consts[tgt.id] = node.value.value

    out: list[str] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr not in ("find", "index") or not node.args:
            continue
        arg = node.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            anchor, how = arg.value, "literal"
        elif isinstance(arg, ast.Name) and arg.id in consts:
            anchor, how = consts[arg.id], f"via {arg.id}"
        else:
            continue  # runtime-built or parameterised — invisible to static analysis
        if _is_section_anchor(anchor):
            out.append(f"{path.name}:{node.lineno} selects {anchor!r} ({how}) by first match")
    return out


def _test_files() -> list[Path]:
    return sorted(p for p in TESTS_DIR.glob("test_*.py") if p.name != SELF)


def test_there_are_test_files_to_scan():
    """A convention test that scans nothing passes vacuously."""
    assert _test_files(), "no test files found — this guard would assert nothing"


def test_no_markdown_section_is_selected_by_first_match():
    offenders: list[str] = []
    for path in _test_files():
        offenders.extend(_offenders_in(path))
    assert not offenders, (
        "markdown sections must be selected via _select_unique() (refuse on ambiguity + "
        "assert the slice carries a real-section marker), never by first match:\n  "
        + "\n  ".join(offenders)
    )


def test_the_detector_catches_both_anchor_shapes(tmp_path):
    """A convention guard nobody has falsified is a decoration.

    Three controls, the middle one added because the COS measured my regex version
    at 0 of 2 on their tree — every anchor there was a module-level constant.
    """
    literal = tmp_path / "test_seed_literal.py"
    literal.write_text('start = text.find("## Communication Permissions")\n', encoding="utf-8")
    assert _offenders_in(literal), "missed the LITERAL anchor shape"

    constant = tmp_path / "test_seed_constant.py"
    constant.write_text(
        'INBOUND_HEADING = "### Inbound discipline"\n'
        "start = persona.index(INBOUND_HEADING)\n",
        encoding="utf-8",
    )
    assert _offenders_in(constant), (
        "missed the CONSTANT anchor shape — the exact form that would make this guard "
        "vacuous on a tree that names its headings"
    )

    legit = tmp_path / "test_seed_legit.py"
    legit.write_text(
        'end = text.index("\\n---", 4)\n'  # frontmatter terminator — correct by definition
        'nxt = text.find("\\n## ", start + 1)\n'  # section END after a property-selected start
        'p = argv.index("--priority")\n',  # argv position
        encoding="utf-8",
    )
    assert not _offenders_in(legit), f"false-positived on correct code: {_offenders_in(legit)}"
