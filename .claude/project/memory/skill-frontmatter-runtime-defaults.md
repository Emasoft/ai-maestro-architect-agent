---
name: skill-frontmatter-runtime-defaults
description: "a skill runs but the caller never gets its result / my fork skill went fire-and-forget with no error / a plugin kept validating clean after a Claude Code upgrade but changed behavior / who decides whether a context:fork skill is synchronous"
ocd: 2026-08-07
lmd: 2026-08-29
metadata:
  node_type: memory
  type: project
  tier: component
publish-globally: false
---

# skill-frontmatter-runtime-defaults

^ATOM-NY6F-6WI9 [desc: "Every context:fork skill in this plugin must declare background: explicitly, never left to the harness default, because AMAA's 26 fork skills are all synchronous consults.", keywords: should_i_set_background_false_on_fork_skills does_context_fork_skill_need_background_key explicit_background_key_required_amaa fork_skill_default_changed_silently, ocd: 2026-08-07, lmd: 2026-08-29]

Every `context: fork` skill in this plugin declares `background:` **explicitly**.
The value is never left to the harness default, in either direction.[^1]

^ATOM-ATZ3-QFZ0 [desc: "Claude Code 2.1.218 flipped context:fork skills to background-by-default, turning AMAA's 26 synchronous fork skills into silent fire-and-forget with no error and a still-green validator/test suite.", keywords: claude_code_2_1_218_background_by_default_change fork_skill_became_fire_and_forget caller_got_agent_name_instead_of_answer nothing_errored_but_behavior_changed why_did_my_fork_skill_stop_returning_a_result plugin_still_validates_clean_after_upgrade, ocd: 2026-08-07, lmd: 2026-08-29]

**Why:** Claude Code 2.1.218 changed `context: fork` skills to run in the
**background by default**, with `background: false` as the per-skill opt-out. All
26 of AMAA's fork skills are synchronous consults — the body says "consult the
reference doc → follow the protocol", and the main agent's workflow uses that
result inline before the next step. Background-by-default turned every one of them
into fire-and-forget: the caller got an agent name instead of an answer, proceeded
without it, and **nothing errored**. The plugin kept passing validation the whole
time. A silent semantic change is the expensive kind, because the usual signals —
a failing test, a red gate, an exception — all stay green.

^ATOM-7KWW-K57Q [desc: "How to apply: write background: false on every fork skill unless deliberately async, and if async, update the caller's DONE/ACK protocol in amaa-design-communication-patterns in the same change; tests/test_amaa_skills.py enforces this.", keywords: how_do_i_pin_a_fork_skill_to_synchronous adopting_async_fork_skill_checklist test_amaa_skills_py_enforces_background_key done_ack_completion_protocol_for_background_skills, ocd: 2026-08-07, lmd: 2026-08-29]

**How to apply:** when adding a fork skill, write `background: false` unless the
skill is deliberately async — and if it is, rewrite the caller's `[DONE]`/ACK
completion protocol in `amaa-design-communication-patterns` in the same change,
because a background skill's result arrives as a later notification rather than a
return value. `tests/test_amaa_skills.py` enforces the explicit key and pins the
all-synchronous intent, so a future default flip surfaces as a test failure
instead of another silent change. Adopting async is therefore a deliberate edit to
that test, never a drive-by frontmatter tweak.

^ATOM-WZC8-CE0B [desc: "Related: the same alignment pass fixed AMAA's one-layer delegation ceiling (no fan-out despite CC 2.1.219 allowing depth 3) and the AMP-vs-native-channel policy; full record TRDD-M3RV5THO.", keywords: one_layer_delegation_ceiling_no_fanout amp_vs_native_channel_policy trdd_m3rv5tho_full_record cc_2_1_219_depth_3_not_adopted, ocd: 2026-08-07, lmd: 2026-08-29]

**Related:** the same alignment pass set AMAA's self-imposed one-layer delegation
ceiling (bundled sub-agents do not fan out, despite CC 2.1.219 allowing depth 3)
and the AMP-vs-native-channel policy in
`skills/amaa-design-communication-patterns/references/native-cross-session-channel.md`.
Full record: `TRDD-M3RV5THO`.

## Notes and lessons learned

[^1]: [id:ATOM-NM0A-E2SQ, status:valid, desc:"A harness default flipped under 26 skills; every signal stayed green because the frontmatter was still valid and the skills still ran.", keywords:"every_gate_is_green_but_the_behavior_changed a_claude_code_upgrade_changed_my_plugin_without_editing_it plugin_validates_clean_but_the_caller_gets_no_answer unwritten_default_changed_under_me what_should_i_check_after_a_claude_code_upgrade", ocd:2026-08-07, lmd:2026-08-07] DO NOT treat a clean validator run, a green test suite, or the absence of an error as evidence that a Claude Code upgrade changed nothing, BECAUSE a harness DEFAULT can change the runtime meaning of frontmatter the plugin never edited — 2.1.218 flipped 26 fork skills to background-by-default here, and every signal stayed green: the frontmatter was still valid, the skills still "ran", CPV still reported zero findings. The only symptom was a caller that never received an answer. DO read the changelog against the plugin's own declared surface (frontmatter keys, hook events, agent fields, permission-rule forms) on every upgrade, and DO pin any harness default the plugin's behavior depends on by writing the value explicitly — an unwritten default is a dependency on someone else's decision, and it changes without notifying you.
