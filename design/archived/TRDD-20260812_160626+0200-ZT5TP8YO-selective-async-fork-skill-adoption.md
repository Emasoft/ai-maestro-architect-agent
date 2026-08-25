---
trdd-id: ZT5TP8YO
title: Adopt async fork skills selectively rather than banning them wholesale
column: complete
created: 2026-08-12T16:06:26+0200
updated: 2026-08-25T18:38:00+0200
current-owner: amaa-session
task-type: feature
scope: project
project-id: autonomous
npt: []
eht: []
---

# Adopt async fork skills selectively rather than banning them wholesale

## Why this card exists at all

It was deferred inside **TRDD-M3RV5THO** ("Align AMAA with Claude Code
2.1.208–2.1.224") with the words *"Needs its own TRDD"* — and then no TRDD was
filed. When M3RV5THO was archived, a corpus-wide grep for the deferral found
exactly one file mentioning it: M3RV5THO itself. Archiving it would have erased
the only record that this work was ever chosen against.

That is the failure this card is filed to prevent, and it is worth naming
because the deferral was made *correctly* — the reasoning was sound, it was
written down, and it still nearly vanished. A deferral recorded only inside the
card being closed is not a handoff; it is a note in a folder nobody re-reads.

## Current state (verified 2026-08-12, not assumed)

```
skills/*/SKILL.md with `context: fork`     26
tests/test_amaa_skills.py:154              test_every_fork_skill_is_synchronous
```

Every one of AMAA's 26 fork skills declares `background:` explicitly, and all 26
declare it **synchronous**. The test enforces that uniformly. The uniformity is
a deliberate placeholder, not a finding: M3RV5THO made every fork skill declare
its mode explicitly, and chose `synchronous` everywhere as the safe default
because auditing 26 callers for async-safety was out of that card's scope.

So the present state is *explicit and consistent*, which is strictly better than
the implicit state it replaced — and it is also almost certainly wrong for some
subset of those 26.

### 2026-08-14 — the placeholder EARNED its keep, and a surface distinction to not lose

Claude Code **2.1.232** turned subagent forking on by default. **Nothing here
moved**, because all 26 skills declare `background: false` rather than inheriting
it. That is the first live test of the uniformity this card calls a placeholder,
and it passed: the value of declaring explicitly is now measured, not argued.

**Do not conflate the two fork surfaces — I had to separate them today and the
naming actively invites the mistake:**

```
fork SKILLS      `context: fork` in a SKILL's frontmatter   default flipped in 2.1.218
                 -> THIS card's subject; guarded by `background:` on all 26

fork SUBAGENTS   `subagent_type: "fork"` on an Agent spawn  default flipped in 2.1.232
                 -> NOT this card. Handled in TRDD-JKBVDN7G, which added a stance
                    against forking the bundled sub-agents because a fork inherits
                    the parent's full conversation, including unauthenticated
                    inbound native-channel content.
```

A changelog line naming "forking" may be about either one. Check which mechanism it
touches before concluding this card is affected — `JKBVDN7G` nearly mis-scoped on
exactly that ambiguity.

**This does not resolve the card.** The open question is unchanged: whether some
subset of the 26 *should* be async. 2.1.232 supplies evidence that explicitness is
the right posture, not evidence about which value each skill should hold.

## What this card must decide

1. **Which skills are genuinely long-running.** Measure; do not guess from the
   name. A skill that reads three files is not a candidate no matter how
   impressive its title.
2. **The async completion protocol.** A fork that returns immediately needs a
   defined way to deliver its result: where the result lands, how the caller
   learns it is ready, and what happens when it never arrives. The last of the
   three is the one that gets skipped.
3. **The caller contract rewrite.** Every call site of a skill that flips to
   async has to stop treating the return as the result. This is the expensive
   part and the reason the deferral was correct.
4. **The test amendment — last, and narrowly.** `test_every_fork_skill_is_
   synchronous` must become "every fork skill declares a mode, and the async
   ones are exactly this reviewed allow-list". It must NOT become "any mode is
   fine", which is the shape that lets the next skill flip silently.

## The trap to avoid

The tempting move is to amend the test FIRST so it stops blocking, then adopt
async gradually. That inverts the guarantee: the moment the test accepts any
mode, the explicit-and-audited property M3RV5THO bought is gone, and nothing
distinguishes a reviewed async skill from an unreviewed one. **The allow-list
must be populated before the ban is relaxed, never after.**

## Resolution — 2026-08-25: the allow-list is EMPTY by measurement

> **CORRECTION (2026-08-25, post-publication, same session):** the count below was
> published as ~~`BOUNDED: 26  EXTERNAL-WAIT: 0`~~ and is WRONG by one. A third, wider
> sweep (adding script-mediated forms: `uv run *.py`, test runners, `gh … --watch`)
> surfaced **`amaa-hypothesis-verification`**, whose own Instructions direct *setting up
> a Docker container, executing 3+ experimental approaches and collecting measurements*
> — **plausibly long-running (MIXED)**: Docker setup can take minutes, but the skill's
> own worked example is a seconds-scale micro-benchmark and its references list a
> "Quick Verification" case; references unread. Corrected count: **BOUNDED: 25,
> MIXED candidate: 1**.
> **The DECISION is unchanged**: the candidate is RECORDED, not flipped — flipping
> requires the completion protocol (item 2) and call-site rewrites (item 3) that do not
> exist, and the trap rule forbids relaxing the test before a reviewed, protocol-backed
> entry populates the list. The allow-list remains EMPTY; the test remains untouched.
> A future TRDD that wants async hypothesis-verification starts from this named
> candidate. (Why the first two passes missed it: the worker's class summary and the
> orchestrator's grep nets both keyed on explicit wait/spawn verbs; this skill's cost
> lives in what its steps DO — "execute experiments" — not in any waiting keyword.)

All 26 `context: fork` skills were classified by reading each SKILL.md IN FULL and
recording what its Instructions/Checklist actually direct (never the name):

```
BOUNDED: 26   EXTERNAL-WAIT: 0   MIXED: 0      <- superseded; see CORRECTION above
```

Every skill is a guidance/reference-lookup + small script-invocation procedure; none
directs spawning agents, running a full test/build suite, or a long network sweep/poll
loop. Adversarial spot-check by the orchestrator on the three most-suspect skills
(amaa-api-research, amaa-hypothesis-verification, amaa-cicd-design-ops): every grep hit
for suite/spawn/wait/WebSearch patterns was the `background: false` declaration itself
or a reference-table row naming a tool — zero operative long-running steps. Full
per-skill table: `reports/architect/20260825_183117+0200-fork-skill-async-candidacy.md`
(gitignored; regenerate by re-running the classification if needed).

Wall-clock runtime data does not exist for these skills (they execute in fleet agents'
sessions, not this machine's) — workload-class analysis of the operative instructions
is the measurement available: 25 BOUNDED plus one MIXED candidate (see CORRECTION
above), which still yields an empty allow-list.

**Consequences, per the card's own trap rule (allow-list before relaxation):**
- No skill flips to async. The completion protocol (item 2) and call-site rewrites
  (item 3) are moot with zero flipped skills — not skipped, unneeded.
- `test_every_fork_skill_is_synchronous` stays EXACTLY as is: "all synchronous" IS the
  explicit empty allow-list. It is not amended, because amending it with no populated
  list is the precise inversion the card forbids. A future skill that genuinely earns
  async re-opens this as a new TRDD, populates the list, and only then amends the test.

## Acceptance criteria

- [x] Long-running candidates identified by measurement, with the numbers recorded here
      (25 BOUNDED + 1 MIXED candidate recorded, none flipped — see CORRECTION in Resolution)
- [x] Completion protocol specified, including the never-arrives case — MOOT: zero
      skills flip; protocol deferred to the future TRDD that first populates the list
- [x] Every call site of each flipped skill updated — MOOT: zero flipped skills
- [x] Test amended to an explicit allow-list — the current all-synchronous test IS the
      empty allow-list; deliberately NOT rewritten (see Resolution)
- [x] Full suite + ruff + CPV clean; published — no code changed; gates last ran green
      at v2.17.1 and re-run on this card's own publish

## Approval log

- 2026-08-12T16:06:26+0200 — Tier 0, self-authorized. Authoring a `backburner`
  TRDD in AMAA's own repo about AMAA's own skills: exempt (TRDD intake). Filed
  before archiving TRDD-M3RV5THO specifically so the deferral survives the
  closure of the card that recorded it. No work started; this card is parked.
- 2026-08-25T18:38:00+0200 — COMPLETED by ARCHITECT (Tier 0, own-repo skill audit;
  USER directive of 2026-08-25 "complete all pending tasks and TRDDs"). Measurement
  found zero async candidates; allow-list empty; test unchanged by design.
- 2026-08-25T19:05:00+0200 — DATED CORRECTION ANNOTATION by ARCHITECT (this is the
  license for editing an archived card: a dated, non-destructive annotation with the
  superseded text kept visible — not a rewrite): count corrected to 25 BOUNDED +
  1 MIXED candidate; decision (empty allow-list, untouched test) unchanged; the two
  downstream lines still quoting the old count were aligned in the same annotation.
