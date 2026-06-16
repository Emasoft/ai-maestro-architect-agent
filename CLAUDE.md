# ai-maestro-architect-agent (AMAA) — project instructions

AMAA is the **ARCHITECT** role plugin of the AI Maestro fleet: one architect per project, owning technical architecture design, requirements analysis, API research, and complete implementation handoffs.

## Memory — use the GLOBAL janitor-hosted system (proactively)

AMAA uses the **global, user-level janitor memory system** — NOT a per-plugin one. The skills are `/janitor-memory-recall` · `/janitor-memory-write` · `/janitor-memory-update`; the protocol + recall law (index by the SYMPTOM, never the answer's jargon) live in `~/.claude/rules/markdown-memory-recall.md` (the janitor installs that rule every session). Three scopes:

- **LOCAL** `~/.claude/projects/<slug>/memory/` — machine-private notes (harness; paths, hostnames, hints).
- **PROJECT** `<repo>/.claude/project/memory/` — git-tracked + pushed, shared by every contributor (no secrets).
- **USER** `${CLAUDE_PLUGIN_DATA}/memory/` — the janitor's fixed plugin-data dir; cross-project knowledge.

AMAA ships **no per-plugin memory skills** — it relies solely on the janitor's global ones. (Distinct from `amaa-session-memory`, which restores transcript/session context — a separate concern.)

### The proactive-use contract (applies to the main agent AND every sub-agent it spawns)

- **RECALL BEFORE ACTING** — before authoring a TRDD, making a design decision, re-researching an API, recommending a candidate, or debugging a recurring problem, run `/janitor-memory-recall` first, indexed by the **symptom** (the user's words / the design question), across all 3 scopes. Unprompted. "Have we hit this before? did the user already state a preference?"
- **WRITE / UPDATE AFTER SOLVING** — after a non-trivial decision or solved problem, capture it via `/janitor-memory-write` / `/janitor-memory-update` (clean-the-fact-in-place + demote-the-error-to-a-`[^N]`-lesson). Unprompted.
- **MAINTAIN THE PROJECT WIKIMEM** — proactively keep this project's **PROJECT-scope** pages (`.claude/project/memory/`) current so architecture facts and design lessons are git-tracked and shared with every dev, not stranded in one session.
- **SCOPE ROUTING** — machine-private (local paths, usernames, hostnames, secrets) → **LOCAL**; project-shared with NO private data → **PROJECT**; cross-project → **USER**; **UNSURE → LOCAL** (the safe scope).
- **PROPAGATE** — when you spawn a sub-agent, include this same recall/write directive in its prompt. Memory discipline is inherited, not assumed.

### ARCHITECT-role recall emphasis (what's highest-value for AMAA)

WRITE: design decisions + their rationale, rejected alternatives + why, constraints the user stated, API research conclusions that contradicted expectations, gotchas that cost a session time — facts NOT derivable from the code or git history. The note's `description` carries the QUESTION/symptom vocabulary; the answer goes in the body.

DO NOT WRITE: what the repo already records — code structure, commit history, the design documents under `docs_dev/design/` (those are the artifact layer, not the memory layer) — or session-transient details.

### The zsh-safe recall command (never the space-joined string)

When composing a recall across the 3 scopes, use the **array form** from the rule — a space-joined unquoted `$ROOTS` silently returns 0 hits on zsh (the macOS default shell):

```bash
ROOTS=(); for d in "$LOCAL_MEM" "$PROJECT_MEM" "$USER_MEM"; do [ -d "$d" ] && ROOTS+=("$d"); done
memgrep recall "$SYMPTOM" "${ROOTS[@]}"
```

### Janitor-dependency coupling (a ratified invariant)

The memory system depends on the **user-level `ai-maestro-janitor` plugin** — the ONLY plugin installed at USER scope (guardian of the whole install: global memory, cron/resume, auth refresh, marketplace upkeep, security scanning). **janitor-always-present** is a USER-ratified architecture decision; it is what makes "rely on the global janitor memory system" safe by construction.
