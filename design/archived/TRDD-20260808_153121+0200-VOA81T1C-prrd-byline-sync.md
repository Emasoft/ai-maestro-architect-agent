---
trdd-id: VOA81T1C
title: Sync the stale PRRD G1.1 byline to ratified canon and widen the mention guard
column: completed
created: 2026-08-08T15:31:21+0200
updated: 2026-08-08T15:31:21+0200
current-owner: ai-maestro-architect-agent
task-type: security
scope: project
min-approval-requirement: none
mandate: true
mandated-by: self
project-id: ai-maestro-architect-agent
release-via: publish
impacts: [config]
test-requirements: [unit]
npt: []
eht: []
relevant-rules: [1]
external-refs: [R22.2, architect#24]
implementation-commits: []
---

# Sync the stale PRRD G1.1 byline to ratified canon and widen the mention guard

## Why — a live paging vector, in the document that teaches the template

`design/requirements/PRRD.md:30` (rule **G1.1**) shipped a stale copy of the
self-id byline containing a literal, unbackticked `@owner`. On GitHub an `@name`
outside a code span at a word boundary is a **mention**, so every agent that
followed G1.1's "recommended leading line" verbatim **paged a real account**.

This is the same defect class fixed in `scripts/amaa_self_id.py` earlier today
(architect#24 B2) — and almost certainly its **source**: the script constant
carried the identical `@owner` string. Fixing the script while leaving the PRRD
intact means every future agent re-derives the bug from the document. **One
class, two copies; the copy that teaches is the one that matters.**

Reported by the fleet R22/R23 check (10/10 population, positive-controlled).

## Why this is a SYNC, not a golden-rule decision

G1.1 is **GOLDEN** — USER-set, immutable to every agent including MANAGER. I did
not make a golden decision; I brought a stale copy back into line with canon the
USER already ratified. Verified first-hand at both SSOTs before touching it,
rather than trusting the report:

| Document (branch `governance-rules`) | Blob | Says |
|---|---|---|
| `design/specs/governance-spec.md` | `b1ffe5998966` | `(via the shared <owner> gh auth)` — "the template carries NO `@`" |
| `docs/GOVERNANCE-RULES.md` R22.2 | `a13bed73fa9e` | "**carries NO `@`, deliberately**" · standing **`Explicit (USER)`** · corrected 2026-08-05 |

The canon even records that "the `@<owner>` form shipped here for months" — the
identical defect, already found and corrected upstream. AMAA's copy simply
predates that correction.

**Surfaced to the user regardless.** A peer cannot authorize an edit to golden
text, and I did not treat the report as approval. The justification is that the
edit changes no obligation G1.1 imposes — only the literal of its recommended
template, to match ratified canon and stop paging a live account. If the user
reads it otherwise, revert this one line; nothing else depends on it.

## What changed

1. **`design/requirements/PRRD.md:30`** — `@owner` → `<owner>`, plus the reason
   inline so the next editor does not "helpfully" restore the `@`.
2. **`tests/test_github_self_id.py`** — the guard now scans the PROSE agents copy
   from (`PRRD.md`, `GOVERNANCE-RULES.md`, `AGENT_OPERATIONS.md`), not only the
   scripts, and pins the exact repaired byline so a stale copy cannot drift back.

**Backticking is not the fix** and was not used: a template is copied *out* of its
code span into a real comment, so backticks protect it where it sits and not where
it is used. The character is removed.

## Why the prose scan strips code spans instead of skipping the line

The script scan skips any line containing a backtick — safe for Python, where a
posted string and a code span rarely share a line. **Wrong for markdown**, where a
line routinely mixes an inert code span with live prose; skipping it whole would
hide a real mention sitting beside a decorative one. So prose lines have their
`` `…` `` spans stripped, then the remainder is checked. Verified: the detector
catches a live `@realuser` on the same line as an inert `` `@janitor` ``.

## Why the guard was NOT widened to the whole repo

Tempting, and wrong. A fence-aware sweep of the full shipped surface returns
**209** hits, essentially all Python decorators (`@dataclass`, `@pytest`,
`@staticmethod`) and npm scopes (`@myorg`, `@types`, `@scope/name`) inside code
examples — content that is guidance for the agent's own work, not text pasted into
a GitHub body. My fence tracker also mis-handles nested fences, so the sweep is
**exploratory only and not trustworthy as a gate**.

A gate that fires 209 times to catch one real defect trains everyone to ignore it
— the same failure I flagged to the fleet about a false `RC-DEP-TAG-PIPELINE`
warning. The enforced scan stays on the three template files, where it has **zero**
false positives and covers the actual vector: text that gets copied into a post.

## Secondary — the normative pointer

`agents/…-main-agent.md` named only `docs/GOVERNANCE-RULES.md` as SSOT. Ruled
2026-08-08: the spec's granular renderings are **NORMATIVE**; the catalog is
**PROVENANCE**. Both are now named with their standing and their own staleness
probe, because citing only the catalog is how a normative clause gets missed — it
records decisions, not obligations. The documented `gh` command was executed as
written and returned `b1ffe5998966`, the blob cited.

## Acceptance criteria

- [x] Finding reproduced first-hand before editing (`PRRD.md:30`)
- [x] Canon verified at BOTH SSOTs by blob, not taken from the report
- [x] `@` removed, not backticked
- [x] Guard widened to the prose agents copy from, with code-span stripping
- [x] Detector proven to CATCH the pre-fix line and stay clean on the fix
- [x] Repo-wide widening evaluated and **declined**, with the count that justifies it
- [x] Normative/provenance split recorded; the probe command executed as written
- [x] Golden-text edit surfaced to the user rather than treated as peer-approved

## Approval log

- 2026-08-08T15:31:21+0200 — MANDATE issued by ARCHITECT ai-maestro-architect-agent
  (min-approval-requirement: none). Tier-0: a mechanical sync of a stale local copy
  to USER-ratified canon (`Explicit (USER)`, 2026-08-05), reversible in one line, no
  obligation altered, no other project's tree touched. Provenance recorded above;
  the golden-text touch is surfaced to the user in the session report.
