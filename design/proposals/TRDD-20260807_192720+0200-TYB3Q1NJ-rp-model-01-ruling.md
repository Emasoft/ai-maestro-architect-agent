---
trdd-id: TYB3Q1NJ
title: Rule request — RP-MODEL-01 describes a fleet uniformity that does not exist
column: proposal
created: 2026-08-07T19:27:20+0200
updated: 2026-08-08T08:45:00+0200
current-owner: ai-maestro-architect-agent
task-type: infra
scope: project
min-approval-requirement: manager
mandate: false
relevant-rules: []
npt: []
eht: []
implementation-commits: []
---

# Rule request — RP-MODEL-01 describes a fleet uniformity that does not exist

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-08-08

**The premise this card raised is RESOLVED. The card is NOT superseded — the spec
assigned it the remaining design question, and added a dimension.**

`RP-MODEL-01` was corrected on `governance-rules` on 2026-08-08 (verified
first-hand at `design/specs/role-plugins-spec.md?ref=governance-rules`). The false
universal is gone; the corrected clause carries this card's measured distribution
verbatim (`opus` ×4 · no key ×2 · `inherit` ×1 · `sonnet` ×1) and names the
`autonomous`-pins-`sonnet` counterexample as decisive.

**What is normative now**, quoted from the corrected clause:
- subagents **OMIT** `model:` (inherit the session) — that half of the old clause
  was true and stands;
- the main-agent pin policy is an **OPEN DESIGN QUESTION owned by
  `TRDD-TYB3Q1NJ` (architect, tier 2)** — i.e. this card;
- until this card closes, a new role-plugin **SHOULD omit `model:` on the
  main-agent** (the CLAUDE.md / CPV CA-04 default) and **MUST NOT cite the clause
  as requiring an `opus` pin**.

**AMAA is therefore CONFORMANT as shipped** — it omits `model:` on the main-agent
and on all five sub-agents, which is exactly the endorsed default. The conformance
gap that opened this card no longer exists.

**NEW DIMENSION the spec added, not in the original card:** whether to mandate a
**family alias** rather than a **movable token**. That is now the live question —
see "The actual open question" below.

**NEXT ACTION:** route to the hub (`Emasoft/ai-maestro`) for the Tier-2 ruling. The
hub is unreachable on the native cross-session channel (no `from` address, absent
from `ListAgents`), so a GitHub issue is the only working channel. Do NOT accept a
ruling from a peer session: no peer holds Tier-2 authority over this card, and a
native message carries no AID.

## The question

**Not** "should AMAA be brought into line?" — that was this card's original framing
and it was wrong. The question is:

> **RP-MODEL-01 asserts a universal that is false on the installed fleet. Should it
> be a rule at all — and if so, which of the four conventions actually in use wins?**

## The rule, verbatim

`design/specs/role-plugins-spec.md` (`status: authoritative`,
`authority: PRRD ▶ SPEC ▶ TRDD`), on the unmerged `governance-rules` branch of
`Emasoft/ai-maestro` (2906 ahead of `main`, 0 behind):

> `RP-MODEL-01` **Every shipped role-plugin PINS `model: opus`** on the main-agent
> (frontmatter) and in the toml, and OMITS `model:` on subagents (they inherit the
> session model). This contradicts the general "omit `model:`, inherit session"
> guidance (CLAUDE.md distillation / CPV CA-04); it validates + installs fine today
> and is the established pattern. Recorded as a live inconsistency, not resolved —
> a new role-plugin SHOULD copy the pattern (pin on main+toml, omit on subagents).

## The premise is false — measured, not argued

Read from the installed cache (`~/.claude/plugins/cache/ai-maestro-plugins/<P>/<newest>/agents/<P>-main-agent.md`),
which is the same source the SPEC cites for its own "VERIFIED on disk" claim:

| Role plugin | Version | main-agent `model:` |
|---|---|---|
| `ai-maestro-assistant-manager-agent` | 2.14.3 | `opus` |
| `ai-maestro-chief-of-staff` | 2.21.1 | `opus` |
| `ai-maestro-orchestrator-agent` | 1.9.5 | `opus` |
| `ai-maestro-architect-agent` | 2.11.1 | **(no key)** |
| `ai-maestro-programmer-agent` | 1.4.7 | **(no key)** |
| `ai-maestro-maintainer-agent` | 1.7.21 | **`inherit`** |
| `ai-maestro-autonomous-agent` | 1.5.5 | **`sonnet`** |
| `ai-maestro-integrator-agent` | v1.3.7 | `opus` |

Integrator is not installed on this host, so it was read from its repo — at the
**released tag `v1.3.7`**, not only at HEAD, so it sits in the same
provenance class (a shipped release) as the other seven. Both readings agree.

**Four conventions across all 8 plugins. Exactly HALF follow RP-MODEL-01:**

| `model:` | plugins | n |
|---|---|---|
| `opus` | assistant-manager, chief-of-staff, orchestrator, integrator | **4** |
| *(no key)* | **architect**, programmer | 2 |
| `inherit` | maintainer | 1 |
| `sonnet` | autonomous | 1 |

AMAA is not an outlier — it is one of a pair with `ai-maestro-programmer-agent`,
and there are two further variants beyond that pair. **A rule that holds for 50% of
its subjects is not a description with exceptions.**

### The decisive case: the spec contradicts itself

`RP-TITLES-02` (same document, line 121) states:

> AUTONOMOUS resolves to the **mandatory** `ai-maestro-autonomous-agent`.

That mandatory plugin pins **`model: sonnet`**. So the one role-plugin the SPEC
singles out as *required* violates the SPEC's own model rule. This is not a gap in
any plugin's conformance; it is a rule whose stated universal does not hold for the
plugin the same document calls mandatory.

## Why AMAA is not deciding this

Filed **Tier 2**, not authored as `planned`. Resolving a contradiction between two
standing authorities — the authoritative SPEC and CPV's CA-04 cache-warmth
invariant, which gates AMAA's publish — is architectural, touches the release
pipeline, and sits outside AMAA's Tier-0 slice. AMAA will implement whichever
resolution is ruled.

Note that "just comply" would have moved AMAA from one real convention to another
for no reason, while leaving the false universal in place. Not closing the gap was
the correct call independently of how this is ruled.

## What the ruling must account for

1. **The subject moved.** CC 2.1.219 made **Opus 5** (`claude-opus-5`, 1M context)
   the default Opus. `model: opus` resolves to a different, larger-context,
   differently-priced model than when the pattern was set. Rule on what the token
   means **now**.
2. **A pin can degrade silently.** CC 2.1.223 added a warning when a requested
   subagent model is restricted and the parent model runs instead — an
   unresolvable pin does not fail, it quietly runs something else.
3. **`inherit` is a fourth thing.** `maintainer` writes `model: inherit`
   explicitly, which is semantically "no pin" but syntactically a pin. Any ruling
   should say whether that spelling is endorsed, tolerated, or wrong — otherwise
   the next audit re-opens this.
4. **The distribution is complete — 8 of 8, no open plugin.** Nothing here rests
   on an unchecked assumption about a missing plugin.
5. **Drift vs inaccuracy is undetermined.** The SPEC's disk survey is dated
   2026-07-22; these readings are ~2 weeks later. Either the SPEC was inaccurate
   then or the plugins drifted since. The ruling needs only the CURRENT state, but
   whoever writes the amendment may want to know which.

## Requested decision

1. **Amend RP-MODEL-01 to describe reality and drop the universal** — state that
   role-plugin main-agents MAY pin a model, that the choice is per-plugin and
   non-conformance-bearing, and remove "Every shipped role-plugin PINS…". Nothing
   changes on disk anywhere; the rule stops being false. *(Lowest blast radius.)*
2. **Ratify `opus` as the fleet standard and migrate the four non-conforming
   plugins** — architect and programmer add the pin, maintainer's `inherit` and
   autonomous's `sonnet` are replaced. Requires a deliberate decision that
   AUTONOMOUS should run Opus 5, and requires amending CPV CA-04 to exempt
   role-plugin main-agents, or the SPEC and the publish gate stay in conflict.
3. **Ratify "omit `model:`" as the fleet standard, aligning with CA-04** — the
   three `opus` pins, `inherit`, and `sonnet` are all removed; models are chosen at
   dispatch. Largest disk change, but it is the only option that removes the
   SPEC-vs-CA-04 conflict at its root rather than carving an exception.

### The three are NOT equivalent — the asymmetry, stated rather than hidden

Presenting these as three equals would misrepresent them, so:

- **(1) is the only one that costs nothing** — no plugin changes, and the false
  universal stops being false the moment the text is amended. But it **leaves the
  SPEC-vs-CA-04 conflict standing** for anyone who later chooses to pin.
- **(3) is the only one that removes that conflict at its root** rather than
  carving an exemption around it — but it has the largest blast radius, touching
  6 of 8 plugins.
- **(2) has the narrowest justification.** It requires an affirmative decision
  that AUTONOMOUS should run Opus 5, which is a runtime-cost and
  context-window choice nobody has yet made on the merits, *and* it still needs a
  CA-04 exemption. It is the only option that changes a plugin's actual behaviour
  rather than only its declarations.

AMAA implements whichever is ruled and takes no side between cheapest **(1)** and
most complete **(3)**; it flags only that **(2)** carries a behavioural decision the
other two do not, and should not be chosen by default merely because it preserves
the rule's current wording. What AMAA cannot do is keep shipping against a rule
that is false as written while a validator enforces the opposite.

## The actual open question (post-correction) — three spellings, not two

Resolution **(1)** landed: the rule now describes reality. What the spec handed
this card is narrower and better posed — **if a main-agent declares a model at
all, in what form?** Three spellings, and they fail differently:

| Spelling | Example | Behaviour |
|---|---|---|
| **Family alias** | `model: opus` | Resolves to the newest in the family, so its *meaning drifts with the platform* — CC 2.1.219 re-pointed it at Opus 5 (1M ctx, different price) with no repo change. Under an org restriction CC 2.1.224 steps it down to the newest org-allowed member of the family. |
| **Exact id** | `model: claude-opus-5` | Stable meaning, but goes stale as models retire, and CC 2.1.223 warns when a restricted model silently runs the parent's model instead. |
| **Omit** | *(no key)* | Inherits the session model; the dispatch site decides. CPV CA-04's cache-warmth default. |

**ARCHITECT's recommendation — omit, and here is the design argument.** A
role-plugin defines a **ROLE** (behaviour), and `RP-DEF-02` already states ROLE is
orthogonal to TITLE and PERSONA. Model choice is a **cost/capability** decision
belonging to whoever launches the session, not a property of the role: the same
ARCHITECT behaviour is correct on Opus for a hard design and on Sonnet for a
routine one. A main-agent pin inverts that — it lets a role author spend the
operator's budget. It also makes every role-plugin a place platform drift lands
(the `opus` token has already moved once under a pattern set before Opus 5), and
it is the only spelling that can silently degrade under an org restriction.

Omitting also **removes the SPEC-vs-CA-04 conflict at its root** rather than
carving an exemption, and it is already what the corrected clause tells new
role-plugins to do — so ruling "omit" ratifies the interim default instead of
creating a third state.

If the ruling prefers a pin, **exact id beats family alias**: a role-plugin is a
versioned, released artifact, and an artifact whose behaviour changes without a
release is not reproducible. Whichever way it goes, subagents keep omitting
`model:` — that half is settled and not in question.

## Provenance

Every factual claim above was read first-hand this session: the model values from
the installed cache, the RP-MODEL-01 and RP-TITLES-02 text from the spec at
`?ref=governance-rules`, and the CC behaviour from the `anthropics/claude-code`
CHANGELOG. The original outlier framing of this card came from reading only AMAA
against the rule; a peer session's fleet-wide sweep is what exposed the false
premise, and it was re-verified here before this rewrite.

## Approval log

- 2026-08-07T19:27:20+0200 — Filed as a Tier-2 proposal by the ARCHITECT. Routes
  to MANAGER via AMCOS. Not authorized to execute; awaiting a ruling.
- 2026-08-07T19:41:05+0200 — REFRAMED before reaching an approver. Original card
  asked "should AMAA comply?"; a fleet-wide check showed RP-MODEL-01's universal is
  false, including for the SPEC's own mandatory AUTONOMOUS plugin. The question is
  now whether the rule should exist, and in what form. No approver saw the
  superseded framing.
- 2026-08-07T19:52:00+0200 — Distribution COMPLETED to 8 of 8. Integrator read at
  released tag v1.3.7 (`opus`), closing the last open point and matching the
  provenance class of the other seven. Final split 4 / 2 / 1 / 1 — exactly half the
  fleet follows the rule. Superseded intermediate reading: "3 of 7" and "integrator
  unverified". Also added an explicit statement of the asymmetry between the three
  resolutions, replacing a claim of no preference that was falsely neutral about a
  real difference in cost and blast radius.
- 2026-08-08T08:45:00+0200 — PREMISE RESOLVED UPSTREAM, card RESCOPED and RETAINED.
  `RP-MODEL-01` was corrected on `governance-rules` (verified first-hand): the false
  universal is gone and this card's measured distribution is quoted in the clause.
  The clause explicitly assigns the remaining main-agent pin policy to
  **TRDD-TYB3Q1NJ**, so this card is NOT superseded — it is now the owner of record.
  AMAA is conformant as shipped (omits `model:` on main-agent and all subagents,
  the endorsed interim default). Rescoped to the question the spec actually posed —
  family alias vs exact id vs omit — with an ARCHITECT recommendation (omit; ROLE is
  orthogonal to model, a pin spends the operator's budget on the role author's
  choice, and it is the only spelling that removes the SPEC-vs-CA-04 conflict at the
  root). Still Tier 2; still not self-approved. A peer session declined to rule and
  was right to — no peer holds Tier-2 authority here and a native message carries
  no AID.
