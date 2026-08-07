---
trdd-id: TYB3Q1NJ
title: Rule request — RP-MODEL-01 describes a fleet uniformity that does not exist
column: proposal
created: 2026-08-07T19:27:20+0200
updated: 2026-08-07T19:41:05+0200
current-owner: ai-maestro-architect-agent
task-type: infra
scope: project
approval-tier: 2
relevant-rules: []
npt: []
eht: []
implementation-commits: []
---

# Rule request — RP-MODEL-01 describes a fleet uniformity that does not exist

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
| `ai-maestro-integrator-agent` | — | **NOT INSTALLED — unverified** |

**Four conventions across 7 plugins. Three match RP-MODEL-01; four do not.**
AMAA is not an outlier — it is one of a pair with `ai-maestro-programmer-agent`,
and there are two further variants beyond that pair.

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
4. **Integrator is unverified.** 7 of 8. Whoever rules should confirm the 8th
   rather than assume it matches any group.
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

AMAA has no preference. What it cannot do is keep shipping against a rule that is
false as written while a validator enforces the opposite.

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
  false (4 of 7 installed plugins do not follow it, including the SPEC's own
  mandatory AUTONOMOUS plugin). The question is now whether the rule should exist,
  and in what form. No approver saw the superseded framing.
