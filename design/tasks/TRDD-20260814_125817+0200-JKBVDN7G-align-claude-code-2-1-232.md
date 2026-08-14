---
trdd-id: JKBVDN7G
title: Align AMAA with Claude Code 2.1.225 through 2.1.232
column: dev
created: 2026-08-14T12:58:17+0200
updated: 2026-08-14T12:58:17+0200
current-owner: ai-maestro-architect-agent
task-type: infra
scope: project
approval-tier: 0
relevant-rules: []
implementation-commits: []
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-14

- **Scope:** Claude Code **2.1.225 → 2.1.232**. The previous alignment card,
  `TRDD-M3RV5THO` (archived), covered through **2.1.224** — so this card starts
  where that one stopped and MUST NOT re-litigate its decisions.
- **Directive from the USER**, who supplied the changelog directly.
- **Scope boundary:** this repo only. `~/.claude/rules/` belongs to the
  ai-maestro-janitor plugin — a different project — and per the cross-project rule
  is not editable from here. Anything needed there is filed as an issue instead.

## What is already clean — measured, not assumed

**The removed/renamed-feature axis has ZERO live hits.** `ultraplan` (removed in
2.1.222), `/ultrareview`, `/review` (now an alias of `/code-review`), and the
retired 200-subagent cap appear **only** inside
`design/archived/TRDD-M3RV5THO-…md`, which is terminal and frozen — those lines are
correct historical record, not stale references. The three `/review` hits under
`skills/` are false positives (`review-requirements:` and the prose "test/review").

**The fork-skill surface is guarded and needs no change:**

```
skills carrying `context: fork`      26
of those declaring `background:`     26   (all `background: false`)
enforcing tests                       2   test_fork_skill_declares_background
                                          test_every_fork_skill_is_synchronous
```

2.1.232 makes forking default-on, but the explicit `background: false` on every
fork skill means the harness default cannot reach them. **This is the previous
alignment working exactly as designed** — `test_fork_skill_declares_background`'s
docstring says it exists so that *"a default that flips again later must not be
able to change AMAA's runtime behavior silently"*. It flipped; nothing moved.
Record this as a success of the guard, not as a no-op.

## GAP A — the Agent-tool spawn surface has no equivalent guard

2.1.232: *"non-teammate agent spawns in interactive sessions now run in the
background by default"*.

`agents/ai-maestro-architect-agent-main-agent.md:378` states the delegation
protocol as:

> Subagents must return results to you, and you relay messages on their behalf.

If the default is now background for these spawns, the main agent receives an
agent id immediately and the result arrives later as a task-notification — so the
documented protocol no longer describes default platform behaviour. AMAA keeps
delegation deliberately ONE layer deep and the five bundled sub-agents are told
not to fan out, so the main agent is the only spawn site — which bounds the blast
radius but does not remove it.

- **OPEN QUESTION, and the card must not proceed past it on a guess:** does
  *"non-teammate agent spawns"* cover a plugin's own bundled sub-agents spawned
  via the Agent tool, or is "non-teammate" narrower (i.e. excluding agents the
  plugin ships)? The changelog wording does not settle it. **Rewriting a delegation
  protocol on a misreading of one adjective is exactly the failure this card should
  avoid** — resolve empirically or from the tool contract before editing.

## GAP B — cross-session addressing semantics are pinned to 2.1.224

`…main-agent.md:299` documents the native channel as
`(SendMessage / ListAgents, Claude Code 2.1.224)`. Three subsequent changes move it:

```
2.1.225  SendMessage can START a conversation with Remote Control sessions by name
2.1.229  ListAgents marks disconnected RC sessions `offline`, labels cloud `cloud`
2.1.232  `@` mentions another session; SendMessage delivers to a BARE NAME matching
         exactly one live session (no ref confirmation); sessions on one machine get
         unique names (`name-word-word` on collision)
```

**The security stance does not weaken — the FRICTION does.** That file's rule is
that the R6 communication graph is **self-enforced at send time**, because the
native channel never traverses the AI Maestro server and so has no 403 and no
evaluation point. Bare-name delivery and `@` mentions remove the ref-confirmation
step that previously sat in front of a send. So the same rule now guards a cheaper
action, which makes stating it *more* load-bearing, not less. `offline`/`cloud`
are new observable state the doc does not mention.

## Acceptance criteria

- [ ] GAP A's open question resolved from evidence (tool contract / empirical
      check), NOT from the changelog adjective alone — and the resolution recorded.
- [ ] If AMAA is affected: the delegation protocol text states what actually
      happens, and a guard exists so the NEXT default flip fails a test rather than
      silently changing behaviour (the fork-skill guard is the model to copy).
- [ ] GAP B: the cross-session section names the current addressing semantics, and
      the self-enforcement rule is restated against the reduced friction.
- [ ] `uv run python scripts/publish.py --patch --dry-run` green (398 tests + ruff
      + CPV lint + CPV strict) before any publish.
- [ ] No claim added that this card cannot verify on this machine.

## N — no-gos

- **Do NOT touch the fork skills.** They are correct and guarded; editing them
  would spend the guard's credibility for nothing.
- **Do NOT edit `~/.claude/rules/`** — different project, cross-project rule.
- **Do NOT re-open decisions settled in `TRDD-M3RV5THO`**; it is archived and frozen.

## NEXT ACTION

Resolve GAP A's open question. Advisor consulted 2026-08-14 on exactly this
(whether "non-teammate" covers a plugin's own bundled sub-agents, the right shape
of guard, and whether GAP B is load-bearing or documentation drift) — verify its
answer against the tool contract before acting on it.
