#!/usr/bin/env python3
"""PRRD G1.1 regression tests for AMAA's GitHub-posting scripts (architect#24 B2).

Two defects are pinned here, both of which shipped and neither of which any
existing test caught:

1.  **A missing byline.** Every AI Maestro agent posts under the one shared
    human-owner `gh` identity, so a comment without the self-id line is
    indistinguishable from a human's. Two of the three posting scripts omitted
    it entirely.

2.  **A byline that pages a stranger.** The one script that DID carry a byline
    embedded a bare `@owner`. On GitHub an `@name` outside a code span at a word
    boundary is a MENTION — so every issue that script opened notified a real
    account. This is the failure mode that is invisible in review (it looks like
    prose) and irreversible once posted (edit history is retained).

Both are asserted against the shared constant AND against each call site, since
a correct constant that no site imports fixes nothing.
"""

import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS = REPO_ROOT / "scripts"

# Every script that writes a body to GitHub. Adding a new poster without adding
# it here is the gap this list exists to close.
POSTING_SCRIPTS = [
    "amaa_github_issue_create.py",
    "amaa_github_sync_status.py",
    "amaa_github_attach_document.py",
]


def _load_self_id():
    spec = importlib.util.spec_from_file_location("amaa_self_id", SCRIPTS / "amaa_self_id.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    return module


def test_self_id_module_exists():
    assert (SCRIPTS / "amaa_self_id.py").is_file(), "the shared G1.1 constant module is missing"


def test_byline_carries_no_at_mention():
    """A bare `@name` in the byline pages a real account on every post."""
    mod = _load_self_id()
    assert "@" not in mod.SELF_ID_LINE, (
        f"SELF_ID_LINE contains '@' and would render as a GitHub mention: {mod.SELF_ID_LINE!r}. "
        "Name the owner in plain words — the '@' adds only a notification to a stranger."
    )


def test_byline_identifies_the_plugin():
    mod = _load_self_id()
    assert "ai-maestro-architect-agent" in mod.SELF_ID_LINE
    assert mod.SELF_ID_LINE.startswith("_Posted by"), "byline must be recognisable at a glance"


def test_with_self_id_is_idempotent():
    """Call sites compose bodies from several helpers; a doubled byline is visible."""
    mod = _load_self_id()
    once = mod.with_self_id("## Design Status Update")
    assert once.startswith(mod.SELF_ID_LINE)
    assert mod.with_self_id(once) == once


def test_with_self_id_preserves_the_body():
    mod = _load_self_id()
    assert "## Design Status Update" in mod.with_self_id("## Design Status Update")


class TestEverySiteActuallyUsesIt:
    """A correct constant that no call site imports fixes nothing."""

    def test_every_posting_script_imports_the_shared_constant(self):
        for name in POSTING_SCRIPTS:
            src = (SCRIPTS / name).read_text(encoding="utf-8")
            assert "from amaa_self_id import" in src, (
                f"{name} posts to GitHub but does not import the shared G1.1 byline"
            )

    def test_no_script_redefines_the_byline_locally(self):
        """A local copy is how the `@owner` bug survived: one site, one definition."""
        for name in POSTING_SCRIPTS:
            src = (SCRIPTS / name).read_text(encoding="utf-8")
            assert not re.search(r"^SELF_ID_LINE\s*=", src, re.M), (
                f"{name} redefines SELF_ID_LINE locally — import it from amaa_self_id instead"
            )

    def test_no_posting_script_contains_a_bare_at_mention(self):
        """Catches an `@name` reintroduced anywhere in a posted body, not just the byline."""
        for name in POSTING_SCRIPTS:
            for i, line in enumerate((SCRIPTS / name).read_text(encoding="utf-8").splitlines(), 1):
                if "`" in line or line.lstrip().startswith("#"):
                    continue  # code spans are inert; comments are never posted
                hit = re.search(r"(?<![\w`/])@[A-Za-z][\w-]{2,}", line)
                assert not hit, f"{name}:{i} carries a bare mention {hit.group(0)!r}: {line.strip()!r}"
