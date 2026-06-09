---
name: architect-memory-recall
description: "Use before design decisions, TRDD authoring, or recurring-problem debugging. Trigger with 'have we hit this before' or 'recall memories about X'. Loaded by ai-maestro-architect-agent-main-agent"
context: fork
agent: ai-maestro-architect-agent-main-agent
user-invocable: true
---

# Architect Memory Recall

## Overview

Symptom-ranked recall over the project's markdown memory directory. Wraps
`memgrep recall` when the binary is installed and degrades to a pure-Python
grep fallback when it is not — recall degrades, never breaks. Index law:
notes are found by the QUESTION/symptom wording, never the answer's jargon
(see `rules/memory-protocol.md`).

## Prerequisites

- A memory directory of markdown notes (default:
  `$HOME/.claude/projects/<project-slug>/memory`, slug = project path with
  `/` replaced by `-`).
- `memgrep` on PATH is OPTIONAL — the bundled fallback runs without it.

## Instructions

1. Build the SYMPTOM query from the user's words, the error text, or the
   design question — NOT from the suspected answer's vocabulary.
2. Resolve the memory directory. If `$CLAUDE_PROJECT_DIR` is set, the slug is
   that path with `/` → `-`; otherwise derive it from the current working
   directory.
3. Run the recall script:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/architect-memory-recall/scripts/recall.py" \
     --memdir "$MEMDIR" "$SYMPTOM"
   ```

   The script prefers `memgrep recall` when available and otherwise ranks
   notes itself: frontmatter `description`/`title`/`tags` hits weigh 3×,
   body hits 1×, results print best-first as `path — description`.
4. Read the top 1-3 notes returned; the answer is in their bodies.
5. If nothing matches, say so — the memory does not exist yet. After solving
   the problem, capture it with the `architect-memory-write` skill.

## Output

Ranked note list, one per line: `<path> — <description>`. Empty result prints
`no matching memories` and exits 0 (absence of memory is not an error).

## Error Handling

- Memory dir missing → prints `memory dir not found: <path>` and exits 0
  (a project without memories is a normal state, not a failure).
- `memgrep` present but failing → falls back to the built-in ranker for that
  invocation and notes the degradation on stderr.

## Examples

```text
User: have we hit this before? the publish pipeline keeps leaving uv.lock dirty
User: recall memories about design decisions for the messaging layer
User: /architect-memory-recall handoff format disagreements
```

## Resources

- [recall.py](scripts/recall.py) — the gate + fallback implementation
- `rules/memory-protocol.md` — the recall discipline and note schema
