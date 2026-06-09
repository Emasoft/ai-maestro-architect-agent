# Memory protocol — recall before acting, index by the symptom (ARCHITECT)

The ARCHITECT (AMAA) keeps a persistent markdown memory: one fact per note,
stored in the project's memory directory. This rule is the recall half of the
memory system — how to FIND notes and the discipline that makes finding work.
The authoring half (note schema, when to save) is summarized below and
implemented by the `architect-memory-write` skill.

## The one law: index by the QUESTION, not the answer

A memory is found from the SYMPTOM, not the solution. When you write a note,
its `description:` (and `title`/`tags`) MUST carry the words a future session
will have when the problem RECURS — the user's words, the error text, the
design question — NOT the jargon of the answer.

- WRONG `description`: "OAuth creds live in the macOS keychain services".
  (Findable only if you already know the answer is "keychain".)
- RIGHT `description`: "rotator failed, had to log in manually — where are the
  creds / why did the swap fail" + the keychain fact in the BODY.

Two-hop recall: a symptom query lands on the note; the note's BODY gives the
answer. `description + title + tags` are the load-bearing recall surface.

## Recall BEFORE acting (the protocol)

Before making a design decision, authoring a TRDD, debugging a recurring
problem, or re-researching an API: RECALL first — "have we hit this before?".
Use the `architect-memory-recall` skill, or directly:

```bash
MEMDIR="$HOME/.claude/projects/<project-slug>/memory"   # slug = project path, dashed
SYMPTOM="the user's words / the error / the design question"

if command -v memgrep >/dev/null 2>&1; then
  memgrep recall "$SYMPTOM" "$MEMDIR"      # ranked best-first: path — description
else
  grep -rliE "$SYMPTOM" "$MEMDIR"          # fallback: degrade, never break
fi
```

Read the top 1-3 notes; the answer is in their bodies. If recall returns
nothing, the memory does not exist yet — write one after solving the problem.

## What the ARCHITECT writes (and what it does not)

WRITE: design decisions + their rationale, rejected alternatives + why,
constraints the user stated, API research conclusions that contradicted
expectations, gotchas that cost a session time. These are facts NOT derivable
from the code or git history.

DO NOT WRITE: what the repo already records (code structure, commit history,
design documents under `docs_dev/design/` — those are the artifact layer,
not the memory layer), or session-transient details.

## Note format (the schema `architect-memory-write` produces)

```yaml
---
name: <kebab-slug>                 # == filename stem
description: "<symptom surface — the load-bearing recall field>"
metadata:
  node_type: memory
  type: user | feedback | project | reference
---
<body: the one fact; for feedback/project add **Why:** and **How to apply:**>
```

`MEMORY.md` in the memory dir is the index — one line per note:
`- [Title](file.md) — hook`. Recall does not need the index (it scans the
notes directly), but the index is what a fresh session loads first.

## Availability

`memgrep` is a Rust binary (ships with the ai-maestro-janitor toolchain).
When absent, every recall path in this plugin degrades to plain grep over the
memory dir — recall degrades, never breaks. Never report recall as
unavailable: the fallback always works.
