#!/usr/bin/env python3
"""Every skill template that builds a GitHub post body carries the PRRD G1.2 byline.

The scripts layer is guarded by tests/test_github_self_id.py; this guards the
template layer agents copy bodies FROM (architect#24 B2 follow-up).
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILLS = REPO_ROOT / "skills"

# Long, exact, and mention-free: matches the ratified byline in
# scripts/amaa_self_id.py SELF_ID_LINE (PRRD G1.2, mirroring GOV-R22).
BYLINE = "_Posted by the Claude developing the **ai-maestro-architect-agent**"
GH_POST = re.compile(r"gh (issue|pr|release) (create|comment)")


def test_every_gh_post_body_template_carries_the_byline():
    for path in SKILLS.rglob("*.md"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "--body" not in text or not GH_POST.search(text):
            continue
        assert BYLINE in text, (
            f"{path.relative_to(REPO_ROOT)} builds a GitHub post body via "
            f"`gh ... --body` but omits the PRRD G1.2 self-id byline; every "
            "posted body must start with it (see scripts/amaa_self_id.py)."
        )
        assert "Author: AMAA" not in text, (
            f"{path.relative_to(REPO_ROOT)} carries the invented 'Author: AMAA' "
            "form; templates must reuse the ratified SELF_ID_LINE wording "
            "verbatim, never a third byline shape."
        )
