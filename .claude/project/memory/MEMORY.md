# Project memory (wikimem) — PROJECT scope

The git-tracked, cross-dev memory wiki for ai-maestro-architect-agent (AMAA).
Recall surfaces these pages by symptom; the protocol lives in
`~/.claude/rules/markdown-memory-recall.md` (run `/janitor-memory-recall`). One
line per page — each a markdown link from the page title to its file.

- [architecture](architecture.md) — how AMAA works: the ARCHITECT-role overview + the parts map (agents, skills, design pipeline, hooks).
- [decouple-api-to-cli](decouple-api-to-cli.md) — skills must call the frozen CLI verbs, not raw `/api/*` routes; the `/api` → CLI verb mapping (e.g. recipient/chief-of-staff resolution).
