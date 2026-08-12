---
trdd-id: ZT5TP8YO
title: Adopt async fork skills selectively rather than banning them wholesale
column: backburner
created: 2026-08-12T16:06:26+0200
updated: 2026-08-12T16:06:26+0200
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

## Acceptance criteria

- [ ] Long-running candidates identified by measurement, with the numbers recorded here
- [ ] Completion protocol specified, including the never-arrives case
- [ ] Every call site of each flipped skill updated, enumerated by grep, not by memory
- [ ] Test amended to an explicit allow-list; proven to red on an unlisted async skill
- [ ] Full suite + ruff + CPV clean; published

## Approval log

- 2026-08-12T16:06:26+0200 — Tier 0, self-authorized. Authoring a `backburner`
  TRDD in AMAA's own repo about AMAA's own skills: exempt (TRDD intake). Filed
  before archiving TRDD-M3RV5THO specifically so the deferral survives the
  closure of the card that recorded it. No work started; this card is parked.
