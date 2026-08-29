---
name: decouple-api-to-cli
description: "how should AMAA skills call the AI Maestro server — do NOT hardcode /api/* routes; use the frozen CLI verbs. The /api -> CLI verb mapping; how to resolve a recipient/chief-of-staff by role; why a route rename must not break a skill"
ocd: 2026-06-18
lmd: 2026-08-29
metadata:
  node_type: memory
  type: project
  tier: component
  functionality: architecture
publish-globally: false
---

^ATOM-XYPW-0ST1 [desc: "AMAA skills must call the frozen CLI verb layer, never a raw /api/* route, because the server's REST routes get renamed without notice.", keywords: should_i_call_slash_api_directly_from_a_skill route_rename_broke_my_skill why_use_cli_verb_instead_of_rest_route what_is_the_frozen_cli_layer aimaestro_teams_sh_amp_star_verbs api_routes_not_stable_interface, ocd: 2026-06-18, lmd: 2026-08-29]

The AI Maestro server REST routes (`/api/*`) are NOT a stable interface — they get renamed. The fleet froze a CLI layer in front of them (`~/.local/bin/aimaestro-*.sh`, `amp-*`), and **every agent-facing skill must call the CLI verb, not a raw `/api/` route**, so a route rename can never break a skill. This was the fleet-wide "repoint /api/* to the immutable CLI layer" sweep — architect side tracked as #16, keystone deploy ai-maestro#36 (deploy signal: the presence of the `~/.local/bin/aimaestro-teams.sh` file). Shipped in **v2.8.1**.

## The executability rule (what is IN SCOPE)

^ATOM-B6VC-RMRO [desc: "Defines what counts as an in-scope hardcoded /api/ call needing repointing to a CLI verb vs an exempt inert reference vs a kept GitHub API call.", keywords: is_this_api_reference_in_scope_for_cli_repoint changelog_mentions_api_route_is_it_a_violation doc_spec_template_api_resource_exempt gh_api_github_com_not_in_scope what_counts_as_a_live_api_call_in_a_skill, ocd: 2026-06-18, lmd: 2026-08-29]

- **IN SCOPE** — a skill/reference that TEACHES or INSTRUCTS the agent to RUN a direct `/api/...` call (a skill is agent-facing, so a hardcoded direct REST call to the `/api/` route in it IS a live call at skill-load time). Repoint these to the CLI verb.[^1]
- **EXEMPT** — inert references only: a changelog/design-note mentioning a route, a sample server *response*, a doc-spec template (`/api/resource`, `/api/users`), a modularization pattern example (`/api/v1/auth/*`, nginx `location /api/search`), an external URL (`gitlab.com/api/v4`), a `src/api/` file path. Leave these as-is.
- **KEPT (never in scope)** — `gh` / `api.github.com` calls. Those are GitHub, not the ai-maestro server.

## The /api -> frozen CLI verb mapping (as applied in AMAA)

^ATOM-D299-NNZL [desc: "The concrete /api route -> frozen CLI verb mapping table plus the other live verbs from the #36 deploy, and why a verb that still curls /api/ internally is fully decoupled.", keywords: which_cli_verb_replaces_this_api_route amp_team_members_amp_send_amp_inbox_mapping aimaestro_teams_sh_aimaestro_governance_sh_verbs is_a_cli_verb_that_curls_api_internally_still_decoupled api_governance_teams_members_role_chief_of_staff, ocd: 2026-06-18, lmd: 2026-08-29]

| Raw route (was) | Frozen CLI verb (now) |
|---|---|
| `GET /api/governance/teams/{teamId}/members?role=chief-of-staff` | `amp-team-members --team <teamId>` — lists members with governance title/role; pick the chief-of-staff |
| `/api/messages` (send) | the `ai-maestro-plugin:agent-messaging` skill / `amp-send` |
| `/api/agents` (per MANAGER's example) | `aimaestro-agent.sh list` |
| `/api/messages` (read inbox) | `amp-inbox` |
Other live verbs from the #36 deploy: `aimaestro-teams.sh` (list/show/create/update teams), `aimaestro-governance.sh` (whoami / requests / approve / reject). A CLI verb owns the (changeable) HTTP call internally — that indirection IS the decoupling; referencing the verb is fully decoupled even though the verb itself still curls `/api/` inside.

^ATOM-W36H-XVW6 [desc: "The only in-scope /api hardcodes found in AMAA were in the design-communication-patterns recipient-resolution skills; the rest are tagged DECOUPLE-BLOCKED pending the deploy signal.", keywords: where_were_the_in_scope_api_hits_in_amaa design_communication_patterns_recipient_resolution op_send_ai_maestro_message decouple_blocked_ai_maestro_36_tag deploy_signal_absent_repoint_now_vs_later, ocd: 2026-06-18, lmd: 2026-08-29]

The only IN-SCOPE hits in AMAA were the recipient-resolution guidance in the **design-communication-patterns** skills (`op-send-ai-maestro-message.md` + `ai-maestro-message-templates.md`, each present in the skill and its `-ops` twin). No script/hook/agent/command made server calls. When the deploy signal is ABSENT, repoint-now where the verb already exists and tag the rest `# DECOUPLE-BLOCKED ai-maestro#36`, flipping them when `aimaestro-teams.sh` appears.

Governed by [[architecture]].

## Notes and lessons learned
[^1]: [id:ATOM-K9A8-X4DP, status:valid, keywords:"publish blocked by CMD_INJECTION in my docs, skillaudit code_execution flagged prose, backtick command in a memory note, in-package docs are security scanned, post-release memory commit cannot reach origin", ocd:2026-06-18, lmd:2026-06-18] This page first wrote the route call as a backtick-wrapped curl command and the deploy check as a backtick-wrapped bracket file-test expression; publish.py's security scan (skillaudit code_execution) flagged it CMD_INJECTION, and under strict mode that NIT blocked the publish. Root cause: the memory tree ships INSIDE the plugin package and IS security-scanned, and the scanner cannot tell prose-about-a-command from a runnable command. Lesson: in any in-package doc (memory, skills, references), describe commands as PROSE ("a direct REST call to the api route", "the presence of the file"), never as backtick-wrapped runnable command tokens. Second lesson: author the PROJECT memory note in the SAME commit as the feature, BEFORE running publish.py — a standalone post-release memory commit cannot reach origin without forcing an extra release (the pre-push hook permits only publish.py pushes).
