---
trdd-id: G5YIPLBD
title: Agent model pin omission is fleet-conformant — no change to agents
column: complete
created: 2026-08-29T22:51:05+0200
updated: 2026-08-29T22:51:05+0200
current-owner: amaa-session
task-type: audit
scope: project
project-id: autonomous
npt: []
eht: []
implementation-commits: []
---

# Agent model pin omission is fleet-conformant — no change to agents

## Why this card exists

While correcting a stale fact in `architecture.md` (published v2.17.8), a git trace
surfaced what looked like a half-finished change: commit `dce503e` (2026-07-03)
deleted the `model:` frontmatter pin from all 6 `agents/*.md` (`opus` x5,
`sonnet` x1) for cache warmth, promising *"force opus at the dispatch call site
when an agent genuinely needs it, not in the definition"* — and no dispatch-site
pin was ever added.

That reading was escalated to the USER and to the ai-maestro hub as a probable
cost defect: the planner, deliberately on `sonnet` for cheaper planning, had been
inheriting the invoking session's model (usually Opus) since 2026-07-03.

**That framing was wrong, and this card is the correction.**

## What the evidence actually says

Read from the PRIMARY source, `ai-maestro/design/specs/role-plugins-spec.md`,
**spec-version 1.2.0**.

> **RULED 2026-08-08 (ai-maestro#136, closing `TRDD-TYB3Q1NJ`): role-plugin MAIN
> agents OMIT `model:`.** ROLE is orthogonal to model — model choice is a
> cost/capability decision belonging to whoever launches the session; a pin lets
> the role author spend the operator's budget, is the only spelling that silently
> degrades under an org model-restriction, and conflicts with the CPV CA-04
> cache-warmth default. **Migration is on-next-release**: the six plugins carrying
> a key drop it at their next publish; carrying a key past that publish is a
> conformance failure, before it is not.

**AMAA's main-agent carrying no `model:` key is therefore the RULED state**, not a
deviation. This plugin is ahead of the migration, not behind it.

**Subagent policy is deliberately OPEN**, in the ruling's own words: *"The ruling
below binds MAIN agents only; subagent pinning policy is deliberately OPEN — a
cheap-tier pin (`sonnet` on a bounded mechanical worker) is the delegation-tiering
guidance applied, while an `opus` subagent pin spends the operator's budget exactly
as a main-agent pin does."* So AMAA's 5 helper sub-agents omitting the key is
PERMITTED — it is not prescribed, and a `sonnet` pin on the planner would be
equally permitted.

`RP-MODEL-01` also records two corrections of its own, both 2026-08-08, and the
second one matters here: the claim *"subagents already omit `model:` everywhere"*
was measured **FALSE** — `amama-report-generator` pinned `opus` through v2.16.1,
and a re-measure at current remote tips counts **15 pinned subagents** (integrator
×10, orchestrator ×5). The pre-ruling main-agent distribution (`opus` ×4, no key
×2 including architect, `inherit` ×1, `sonnet` ×1 on the *mandatory* autonomous
plugin) is retained in the spec only as the historical record of drift.

## Provenance warning — how this card was nearly wrong

The first draft of this card cited spec-version **1.0.0** and asserted that
`RP-MODEL-01` *prescribes* omitting on subagents. Both were wrong. That draft was
built from a SECONDARY source: another project's TRDD *describing* the rule, read
out of a version-pinned plugin **cache** directory
(`ai-maestro-plugin/3.2.2/design/archived/…-OH3N6OXJ.md`), where four other cached
versions also sat and one was picked arbitrarily.

The spec had been amended **twice** since that description was written. Reading the
primary at `ai-maestro/design/specs/role-plugins-spec.md` reversed two of this
card's stated reasons while leaving its decision intact.

**A document's description of a rule is not the rule.** A cached copy is dated by
construction, and a cache directory holding five versions of the same file offers
no signal about which one is current.

### Exactly where that ruling lives — stated as a limit, not a footnote

Going to "the primary" is only half a fix if the primary is a local checkout. Measured:

- The spec file has **no uncommitted edits**; the ruling is committed, not a draft.
- `RULED 2026-08-08` is **PRESENT on the remote branch `governance-rules`** and
  **ABSENT from `origin/HEAD`** — which has never carried this file at all.
- `governance-rules` is the canonical location for fleet spec text: the installed
  global rule `universal-kanban.md` cites specs by "`ai-maestro` `governance-rules`
  head" for exactly this reason.

So the ruling is published to the branch governance specs are published to, and
**not** to mainline. A contributor cloning the default branch will not see it. That
is the honest scope of this card's citation: binding as fleet governance, invisible
to a mainline reader.

Corroboration that the ruling is applied and not merely written: the spec grades
another plugin against it — *"**model:** ✓ conformant with the RULED policy — no
`model:` key (RP-MODEL-01, ruled 2026-08-08)"* — i.e. a plugin in exactly AMAA's
state is scored conformant.

**And the reason this card is cheap to have been wrong about twice:** its decision is
the NULL ACTION. "Change nothing" holds under the old text, under the new ruling, and
under no ruling at all. An audit that concludes *change nothing* is robust to being
wrong about why — which is not a licence to reason sloppily, but is why two reversed
rationales cost a document edit rather than a bad commit to `agents/`.

## Decision

**Change nothing in `agents/`.** No `model:` pin is restored, on the main agent or
on any sub-agent.

- **Main-agent omission is the RULED state** (2026-08-08, ai-maestro#136). Adding
  `model: opus` back would MANUFACTURE a conformance failure at the next publish.
  This is the decisive reason and it alone settles the card.
- Subagent omission is PERMITTED — the ruling binds main agents only and leaves
  subagent pinning deliberately open. Nothing is broken by leaving them unpinned.
- The ruling's own stated reasoning independently endorses the posture `dce503e`
  adopted: a pin lets the role author spend the operator's budget, silently degrades
  under an org model-restriction, and conflicts with CA-04.

**The cost observation survives the decision, and is NOT closed by it.** Omitting
the pin does mean the planner inherits the session model. That is a real cost
difference from the `sonnet` it once pinned; it is simply not a *conformance*
defect, and the remedy — if one is ever wanted — is the CA-04 pattern of choosing
the model at the dispatch call site, which `skills/amaa-planning-patterns/scripts/executor.py`
already carries as advisory guidance ("Agent defaults (sonnet) are calibrated for
quality... Upgrade to opus: challenging tasks need reasoning"). Whether to convert
that guidance into a mechanical pin is an owner decision about cost, and the ruling
makes it explicitly available: a `sonnet` pin on a bounded mechanical sub-agent is
named in the spec as "the delegation-tiering guidance applied" — permitted, not a
violation. Restoring the planner's `sonnet` is an option the owner may take at any
time; it is simply not something this audit is entitled to do unasked. It is not a defect
to be fixed by an audit.

## Method — what was actually verified, so a reader can re-run it

- **No `model:` key on any of the 6 agents**: read the YAML frontmatter of every
  `agents/*.md` directly. Not a grep — the frontmatter block itself.
- **No dispatch-site pin anywhere**: `git grep -nIE '(opus|sonnet|haiku)'` across
  **every tracked file of every type** (not an `--include` list, which had missed
  JSON/YAML/TOML). Exactly 3 files match: the memory page, a validator's allowed-set
  (`AGENT_VALID_MODELS`), and the advisory table in `executor.py`.
- **The pin history**: `git log -G` (regex on diff text), **not** `git log -S`.
  The pickaxe reports only commits where a string's *count* changes, so it cannot
  see a value swap like `model: opus` -> `model: sonnet[1m]`.

## Traps this card is filed to prevent

- **`\b` does not work in `git grep -E`** (POSIX ERE, not GNU). Measured on this
  repo, same scope, same moment: `git grep -cIE '\b(opus|sonnet|haiku)\b'` returns
  **0 files**; without `\b`, **3**. A regex that cannot match returns a population
  of zero that is indistinguishable from a clean corpus. This nearly "confirmed"
  the wrong conclusion here.
- **A keyword net cannot establish a negative.** "No dispatch-site pin exists" was
  first claimed from a hand-built alternation. The warrant that actually holds is a
  population-complete sweep whose rows were *read*, not counted.
- **A commit message is not a promise the repo keeps.** `dce503e` stated a
  compensating action that was never performed. Read the tree, not the intent.
- **A description of a rule is not the rule, and a cache is dated by construction.**
  This card's first draft cited spec-version 1.0.0 and a prescription that had been
  amended away twice, because it was built from another project's TRDD *about* the
  spec, read from one arbitrarily-chosen directory among five cached versions. The
  primary was on disk the whole time. Go to the primary before reversing anything.
- **The inverse trap, which is the one that caught this card:** an unkept promise
  is not automatically a defect. `dce503e`'s second half was never needed for the
  subagents, because the spec wanted them unpinned anyway. A gap between stated
  intent and final state can mean the intent was superseded, not abandoned.

## Acceptance criteria

- [x] Determine whether the missing dispatch-site pin is a defect — **it is not**.
      Main-agent omission is the RULED state (ai-maestro#136); subagent pinning is
      deliberately open, so neither omission is a violation.
- [x] Decide on restoring pins — **no**, with the reasoning recorded above.
- [x] Correct the overstated framing published in `architecture.md` v2.17.8
      (the "uncompensated" atom and its lesson) via supersession, never deletion.
- [x] Leave the cost question explicitly open as an owner decision rather than
      silently closing it.

## Approval log

- 2026-08-29T22:51:05+0200 — Tier 0, self-authorized under the USER directive of
  2026-08-29 ("complete all pending tasks and TRDDs, decide by yourself, base your
  decisions on verified facts and tests"). An audit of this plugin's own agent
  frontmatter, resolved by reading an authoritative fleet spec; no other team's
  source touched, no plugin modified. The fable-advisor was unavailable
  (`agentlenspro model-headroom fable` reported Fable at 100% of its own weekly
  window), so no advisor verdict was obtained — recorded here rather than omitted.
  The ai-maestro hub was consulted by SendMessage in parallel; the decision did not
  wait on its reply and does not rest on it.
