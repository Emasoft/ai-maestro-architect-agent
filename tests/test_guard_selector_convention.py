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

**The miss list names SHAPES, not trees.** Both of us first described our gap in
terms of what our own tree happened to contain — "module-level constants",
"variable anchors" — and each description was true locally and too narrow to
protect the other. Enumerating every shape makes the gap visible without having
to encounter it:

| Anchor shape | Covered? | Seeded control? |
|---|---|---|
| literal — `.find("## X")` | YES | yes |
| module constant — `H = "## X"` … `.find(H)` | YES | yes |
| function-local — `m = "## X"` inside a def | YES | yes |
| runtime-built — f-string, concatenation, read from disk | **NO** | yes — pinned UNCAUGHT |
| parameter — anchor passed into the helper | **NO** | yes — pinned UNCAUGHT |

The last two are asserted *uncaught*, so the table fails in **both** directions:
extending coverage breaks the pin and forces this table to be updated with it. A
blind spot recorded only in prose is indistinguishable from one nobody thought
of, and it goes stale silently the moment reality moves.

**Still a net, not a proof.** The last two rows need evaluating rather than
parsing. Collecting names across scopes can in principle mis-resolve a name
reused in two functions; that produces a loud false positive, never a silent
miss, which is the correct direction for a net to fail in.

## The seeded-control loop has its own failure mode — and this design sidesteps it

Reported by ai-maestro-chief-of-staff (ai-maestro#131) and **reproduced here
before being written down**, because relaying an unverified mechanism is the
habit this whole thread exists to correct:

    guard.py:  hits == 1   ->   hits >= 1     # SIZE-PRESERVING, same second
    result:    the weakened predicate still answers False for hits=2
    after `rm -rf __pycache__`:               answers True

Python keys its bytecode cache on `(mtime, size)`. The natural mutations for
testing a predicate — `==`→`!=`, `>`→`>=`, `and`→`or` — are all size-preserving,
so an in-place edit can leave both keys unchanged and Python serves the STALE
`.pyc`. Their run produced a false RED (loud, investigated, harmless). The same
mechanism produces a false **GREEN**: seed a violation, get the stale original
bytecode, conclude the guard catches a shape it does not — invisible precisely
because a passing control is what you expected.

**Why these controls cannot hit it:** the seeds are written to `tmp_path` and read
back with `ast.parse(path.read_text(...))`. They are parsed as *data* and never
imported, so no `.pyc` is ever produced for them and the cache has nothing to
serve. That is a property of the design, not luck, and it is the property to
preserve if this file is ever refactored to import its fixtures.

**If you adopt this and your loop DOES import the mutated module** (a `python3 -c`
that `spec_from_file_location`s the guard, say — I used exactly that shape for an
ad-hoc measurement earlier), then either change the file SIZE or clear
`__pycache__` between runs. An operator swap alone does not.

**Better than mitigating it — remove the class.** CORE's technique (ai-maestro#131):
substitute the *callable in memory*, never the source on disk.

    m = <module loaded via spec_from_file_location>
    m._helper = weakened_version        # swap the object; the file is untouched

There is no `.pyc` to go stale because there is no edit. It also closes a hazard
none of us had named: an in-place edit has a **crash window**. If the run aborts
between the weaken and the restore — exception, timeout, interrupted session —
the weakened predicate is left sitting in the working tree, one character long,
in a file whose tests still pass (that was the point of weakening it), and the
next thing that happens is a commit. *The apparatus that proves the proof was
real can write a defect into the tree it was auditing.* In-memory substitution
cannot leave residue.

**My own measurements avoided both hazards for a WEAKER reason, and it is worth
naming rather than claiming immunity.** I simulated by writing a standalone
reimplementation of the predicate in a throwaway script — so nothing on disk was
ever mutated, and no module was imported. That dodges staleness and the crash
window, but it tests **a copy, not the thing**: a reimplementation silently drifts
the moment the real helper changes, and then measures a function that no longer
exists. CORE's substitution keeps the real module and swaps one callable, which
is strictly better. Prefer it.
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

    module_const = tmp_path / "test_seed_module_const.py"
    module_const.write_text(
        'INBOUND_HEADING = "### Inbound discipline"\n'
        "start = persona.index(INBOUND_HEADING)\n",
        encoding="utf-8",
    )
    assert _offenders_in(module_const), (
        "missed the MODULE-CONSTANT anchor shape — the form that made this guard "
        "vacuous on the COS's tree while passing green on mine"
    )

    # The shape that bit ME, and which the module-level-only resolver missed. The
    # code handles it now, but nothing proved that until this control existed:
    # fixing the resolver and not seeding its shape is the same class of gap the
    # whole thread is about.
    func_local = tmp_path / "test_seed_func_local.py"
    func_local.write_text(
        "def _slice(persona):\n"
        '    marker = "**Inbound discipline**"\n'
        "    return persona.find(marker)\n",
        encoding="utf-8",
    )
    assert _offenders_in(func_local), "missed the FUNCTION-LOCAL anchor shape"

    legit = tmp_path / "test_seed_legit.py"
    legit.write_text(
        'end = text.index("\\n---", 4)\n'  # frontmatter terminator — correct by definition
        'nxt = text.find("\\n## ", start + 1)\n'  # section END after a property-selected start
        'p = argv.index("--priority")\n',  # argv position
        encoding="utf-8",
    )
    assert not _offenders_in(legit), f"false-positived on correct code: {_offenders_in(legit)}"


def test_the_uncovered_shapes_are_pinned_as_uncovered(tmp_path):
    """The miss list must fail in BOTH directions, not just the covered half.

    Credit: ai-maestro-chief-of-staff on ai-maestro#131. A blind spot documented
    only in prose is indistinguishable from one nobody thought of, and if someone
    later extends coverage the docstring goes stale *silently* — passing quietly
    beside a table that now lies. Asserting the misses means the table breaks when
    reality moves in either direction, and whoever extends coverage is told to
    update it.

    These asserts are NOT a wish that the shapes stay uncovered. They pin the
    CURRENT boundary. Extending the resolver is welcome — it just has to come with
    updating this test and the table together.
    """
    runtime_built = tmp_path / "test_seed_runtime.py"
    runtime_built.write_text(
        "level = 2\n"
        'start = text.find(f"{\'#\' * level} Communication Permissions")\n',
        encoding="utf-8",
    )
    assert not _offenders_in(runtime_built), (
        "the RUNTIME-BUILT shape is now caught — good, but the docstring table and "
        "this pin must be updated together, or the table starts lying"
    )

    parameterised = tmp_path / "test_seed_param.py"
    parameterised.write_text(
        "def _slice(persona, anchor):\n    return persona.find(anchor)\n",
        encoding="utf-8",
    )
    assert not _offenders_in(parameterised), (
        "the PARAMETERISED shape is now caught — update the docstring table and this pin"
    )
