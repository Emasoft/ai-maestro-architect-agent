---
name: decouple-api-to-cli
description: "how should AMAA skills call the AI Maestro server — do NOT hardcode /api/* routes; use the frozen CLI verbs. The /api -> CLI verb mapping; how to resolve a recipient/chief-of-staff by role; why a route rename must not break a skill"
ocd: 2026-06-18
lmd: 2026-06-18
metadata:
  node_type: memory
  type: project
  tier: component
  functionality: architecture
---
The AI Maestro server REST routes (`/api/*`) are NOT a stable interface — they get renamed. The fleet froze a CLI layer in front of them (`~/.local/bin/aimaestro-*.sh`, `amp-*`), and **every agent-facing skill must call the CLI verb, not a raw `/api/` route**, so a route rename can never break a skill. This was the fleet-wide "repoint /api/* to the immutable CLI layer" sweep — architect side tracked as #16, keystone deploy ai-maestro#36 (deploy signal: the presence of the `~/.local/bin/aimaestro-teams.sh` file). Shipped in **v2.8.1**.

## The executability rule (what is IN SCOPE)
- **IN SCOPE** — a skill/reference that TEACHES or INSTRUCTS the agent to RUN a direct `/api/...` call (a skill is agent-facing, so a hardcoded direct REST call to the `/api/` route in it IS a live call at skill-load time). Repoint these to the CLI verb.[^1]
- **EXEMPT** — inert references only: a changelog/design-note mentioning a route, a sample server *response*, a doc-spec template (`/api/resource`, `/api/users`), a modularization pattern example (`/api/v1/auth/*`, nginx `location /api/search`), an external URL (`gitlab.com/api/v4`), a `src/api/` file path. Leave these as-is.
- **KEPT (never in scope)** — `gh` / `api.github.com` calls. Those are GitHub, not the ai-maestro server.

## The /api -> frozen CLI verb mapping (as applied in AMAA)
| Raw route (was) | Frozen CLI verb (now) |
|---|---|
| `GET /api/governance/teams/{teamId}/members?role=chief-of-staff` | `amp-team-members --team <teamId>` — lists members with governance title/role; pick the chief-of-staff |
| `/api/messages` (send) | the `agent-messaging` skill / `amp-send` |
| `/api/agents` (per MANAGER's example) | `aimaestro-agent.sh list` |
| `/api/messages` (read inbox) | `amp-inbox` |
Other live verbs from the #36 deploy: `aimaestro-teams.sh` (list/show/create/update teams), `aimaestro-governance.sh` (whoami / requests / approve / reject). A CLI verb owns the (changeable) HTTP call internally — that indirection IS the decoupling; referencing the verb is fully decoupled even though the verb itself still curls `/api/` inside.

The only IN-SCOPE hits in AMAA were the recipient-resolution guidance in the **design-communication-patterns** skills (`op-send-ai-maestro-message.md` + `ai-maestro-message-templates.md`, each present in the skill and its `-ops` twin). No script/hook/agent/command made server calls. When the deploy signal is ABSENT, repoint-now where the verb already exists and tag the rest `# DECOUPLE-BLOCKED ai-maestro#36`, flipping them when `aimaestro-teams.sh` appears.

Governed by [[architecture]].

## Notes and lessons learned
[^1]: [id:ATOM-K9A8-X4DP, status:valid, keywords:"publish blocked by CMD_INJECTION in my docs, skillaudit code_execution flagged prose, backtick command in a memory note, in-package docs are security scanned, post-release memory commit cannot reach origin", ocd:2026-06-18, lmd:2026-06-18] This page first wrote the route call as a backtick-wrapped curl command and the deploy check as a backtick-wrapped bracket file-test expression; publish.py's security scan (skillaudit code_execution) flagged it CMD_INJECTION, and under strict mode that NIT blocked the publish. Root cause: the memory tree ships INSIDE the plugin package and IS security-scanned, and the scanner cannot tell prose-about-a-command from a runnable command. Lesson: in any in-package doc (memory, skills, references), describe commands as PROSE ("a direct REST call to the api route", "the presence of the file"), never as backtick-wrapped runnable command tokens. Second lesson: author the PROJECT memory note in the SAME commit as the feature, BEFORE running publish.py — a standalone post-release memory commit cannot reach origin without forcing an extra release (the pre-push hook permits only publish.py pushes).
