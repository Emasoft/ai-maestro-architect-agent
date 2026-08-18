---
trdd-id: JKBVDN7G
title: Align AMAA with Claude Code 2.1.225 through 2.1.232
column: completed
created: 2026-08-14T12:58:17+0200
updated: 2026-08-18T19:54:10+0200
current-owner: ai-maestro-architect-agent
task-type: infra
scope: project
approval-tier: 0
relevant-rules: []
implementation-commits: [84a0e1c]
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

## Acceptance criteria (AS PLANNED — superseded; see "Acceptance criteria — final" below)

> These boxes are left UNCHECKED deliberately: this is the plan as written before the
> work, kept for comparison. The authoritative result is the **final** block further
> down, which records one criterion as only PARTIALLY met. Do not read the unchecked
> boxes here as outstanding work on a `complete` card.

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

## 2026-08-14 — DONE. Landed in `84a0e1c`; gate green.

- **GAP A's open question is RESOLVED EMPIRICALLY, and the evidence pre-dated the
  question.** I did not need to build a probe: **two Agent-tool spawns earlier in
  this same session** (the advisor consults) each returned an agent id immediately
  plus a later task-notification, with **no background flag passed**. That is the
  flipped default, observed on this machine, on this version, before the question
  was asked. So "non-teammate" does cover a plugin's own bundled sub-agents here.
  Recorded because the temptation was to settle it by parsing the adjective.
- **The fix shape is per-call explicitness**, not a restatement: the protocol now
  says to pass `run_in_background: false` at the spawn site, and says *why* — the
  same discipline that made the 26 fork skills a non-event when this default moved.
- **A THIRD item was found that this card had missed entirely:** 2.1.232 also turned
  `subagent_type: "fork"` on by default, and a fork **inherits the full parent
  conversation**. AMAA's docs said nothing about it. This is security-relevant, not
  merely cost: `main-agent.md` already establishes that inbound native-channel
  messages carry no AID and no verifiable author, so a fork copies unauthenticated
  content into an agent that never evaluated it — turning a message the main agent
  merely READ into instructions a second agent may ACT on. Explicit stance added.
- **GAP B** — comms version table extended with 2.1.225 / 2.1.229 / 2.1.232, plus the
  name-instability rule (a session name is no longer a stable identity; resolve via
  `ListAgents` at send time) and the friction argument: the rules did not weaken, the
  ref-confirmation step in front of a send disappeared, and this channel has no 403.

### The guard, and why it is not a keyword check

`tests/test_delegation_protocol_claims.py` (6 tests). It asserts SHORT COLLOCATIONS
lifted from each operative sentence, whitespace-collapsed on BOTH sides — **not** the
presence of a distinctive term. Memory
`a-doc-guard-that-asserts-a-mention-cannot-see-a-stale-claim` records that exact trap
hit **3× in one week on Claude Code changelog syncs**, each time with the token still
present and the sentence around it false; a rule's own rationale repeats its
vocabulary, so a term check survives deleting the rule. Recalling that before writing
the test is what stopped me shipping the weaker guard.

**Falsified for real, not asserted:** removing the operative sentence failed the
matching test by name; restoring it went green; no residue left in the tree. The
docstring states the limit — it catches DELETION, not weakening in place
(`do not` → `prefer not to` keeps the collocation and stays green).

## Acceptance criteria — final

- [x] GAP A resolved from evidence, not the changelog adjective (see above).
- [x] Protocol states actual behaviour; guard exists so the NEXT flip reds a test.
- [x] GAP B: current addressing semantics + self-enforcement restated.
- [x] `publish.py --patch --dry-run` green: **404 passed / 3 skipped** (was 398),
      ruff clean, CPV lint 0 errors, CPV strict `CRITICAL=0 MAJOR=0 MINOR=0 NIT=0`.
      `WARNING=15` is UNCHANGED — these edits added none; those 15 are the 10
      preload warnings owned by `TRDD-SGW7EITB` plus the 5 documented in `DMIRQOCD`.
- [~] **PARTIALLY met, stated rather than checked off:** two classes of claim in
      these edits rest on the USER-supplied changelog and were NOT independently
      verified on this machine — (i) that a fork inherits the full parent
      conversation (I did not spawn a fork subagent to observe inheritance), and
      (ii) the 2.1.225 / 2.1.229 row contents (Remote Control by-name reach,
      `offline` / `cloud` labels). They are documented as platform behaviour on the
      changelog's authority, which is legitimate, but they are not the same grade of
      evidence as GAP A's direct observation. Anyone extending this should know
      which claims are observed and which are cited.

## Not changed, deliberately

The 26 fork skills. All declare `background: false`, so the 2.1.232 flip could not
reach them — the previous alignment's guard worked exactly as designed. Editing them
would spend that guard's credibility for nothing, and fork-skill uniformity is
`TRDD-ZT5TP8YO`'s scope, whose trap section forbids loosening the test.
