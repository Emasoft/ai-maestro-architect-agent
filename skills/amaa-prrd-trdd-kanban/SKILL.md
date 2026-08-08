---
name: amaa-prrd-trdd-kanban
description: "ARCHITECT's role in the PRRD / TRDD / Kanban workflow. Use when ARCH shapes a proto-TRDD into a full TRDD, decides whether to split (1→N), group (N→1), or pass-through, authors all the verification / impact / delivery frontmatter, and writes the prose body with acceptance criteria."
allowed-tools: "Bash(python3:*), Bash(get-prrd.py:*), Bash(findprrd.py:*), Bash(findtrdd.py:*), Bash(kanban.py:*), Read, Edit, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.0.0"
---

## Overview

The ARCHITECT (AMAA) layer of the PRRD / TRDD / Kanban model. ARCH
owns the **design column** — the only column with a 1→N (split) and
N→1 (group) topology. A proto-TRDD comes in from ORCH; one or more
fully-designed TRDDs land in `dispatch`.

**This skill is the ARCHITECT judgment layer only — it owns no mechanics.**
Every pillar operation goes through the core `ama-*` skills in
`ai-maestro-plugin`: `ama-kanban-render` (see the board), `ama-trdd-find`
(search), `ama-trdd-write` (author), `ama-trdd-update` (edit fields),
`ama-trdd-transition` (move a card), `ama-prrd-get` / `ama-prrd-find` (read
rules), `ama-prrd-propose` (propose a rule), `ama-proposal-approvals`
(approve/refuse). What lives *here* is the split / group / pass-through
decision, which no core skill can make for you.

ARCH **self-mandates** all within-team design work — pass-through,
split, group, setting design frontmatter — writing
`min-approval-requirement: none`, `mandate: true`, `mandated-by: self`
and proceeding immediately. No approval round-trip exists to wait for.

Higher requirements (`chief-of-staff` / `manager` / `user`) apply to
force-`superseded` outside a normal split, editing TRDDs already past
design, and anything crossing a team/project, release, baseline or
governance boundary. **File those to `design/proposals/` and MOVE ON**
— D1 never-block: you do not spin-wait on an approver, ever.

`approval-tier: N` is **deprecated, decode-only, never written on a new
TRDD**; name the governance title instead. Legacy files migrate on next
touch, never in a mass rewrite. A file carries exactly one of the two.

## Prerequisites

- The core `ama-*` skills from `ai-maestro-plugin` are available — they carry
  the mechanics, the 17-column transition rules, and the approval vocabulary.
- The project PRRD exists and `design/tasks/` is present.
- A proto-TRDD sits in the `design` column awaiting ARCH.

## Instructions

1. Read the proto-TRDD body (the paraphrased user request).
2. Set `task-type:` (`feature` / `bugfix` / `refactor` / `docs` /
   `infra` / `security` / `artifact` / `spike` / `audit`).
3. Set `severity:` and `effort:` from judgment.
4. Set `release-via:` (`publish` for tools/packages, `deploy` for
   services, `none` for internal-only).
5. Set `test-requirements:`, `audit-requirements:`,
   `review-requirements:` (which test/scan/review types are mandatory).
6. If artifact-producing, set `artifact-kinds:`; set `runtime-targets:`
   (platforms that must pass) and `impacts:` (install / dependencies /
   config / migration / public-api / ci-pipeline).
6b. Set the **approval fields** on every TRDD you author:
    `min-approval-requirement:` (the governance title — `none` for
    in-scope design work), and when you are issuing it on your own
    authority, `mandate: true` + `mandated-by: self`. Record the
    no-round-trip line in `## Approval log`. Never write
    `approval-tier:`.
7. Identify **NPT children** — prerequisites that must complete BEFORE
   the parent's `dev`. Author each as a separate TRDD; link via `npt:`.
   Each child is **depth-1**: `derived: true`, `derived-kind: npt`,
   `parent-trdd:` set, and its own `npt:`/`eht:` EMPTY. Siblings order
   via `blocked-by:`.
8. Identify **EHT children** — consequence-handling tasks that must
   complete BEFORE the parent's `complete`. Link via `eht:`; same
   depth-1 field set with `derived-kind: eht`.
8b. **Completion gate.** The parent reaches `column: complete` only when
    every id in `npt:` ∪ `eht:` sits in a terminal column
    (`complete`/`published`/`live`/`superseded`). Otherwise it is
    `blocked`, with `blocked-by:` naming the open children and
    `pre-block-column:` recording where it was. "Complete pending EHTs"
    is not a state — the parent's own tests going green is not
    completion.
9. Decide topology: **pass-through** (#4 `design → dispatch`), **1→N
   split** (#5 parent → `superseded`, N children to `dispatch`), or
   **N→1 group** (one combined TRDD supersedes the inputs).
10. Write the body: `## STATE` (if multi-session), `## Acceptance
    criteria` (testable bullets), `## Design notes`, `## Out of scope`;
    cite rules in `relevant-rules:`.
11. Move on: pass-through sets `column: dispatch`, `assignee: null`,
    bumps `updated:`. On split/group, mark the parent/inputs
    `column: superseded` with `superseded-by: [<child-refs>]`.

## Output

- A fully-designed TRDD: complete frontmatter (task-type, severity,
  effort, release-via, the three requirement sets, runtime-targets,
  impacts, npt/eht, relevant-rules, **min-approval-requirement +
  mandate/mandated-by**) plus the prose body and an `## Approval log`
  line recording the mandate (or the filed request).
- On a split/group: N child TRDDs (fresh UUID + timestamp,
  `parent-trdd:`/`supersedes:`, own requirements) and the superseded
  parent/inputs.
- An AMP message to ORCH **via COS**: "TRDD-<id> designed; ready for
  dispatch" (or "split into <N>: <refs>" / "grouped into <ref>").
- New/edited TRDD files staged and committed.

## Error Handling

- **Ambiguous scope** — do not guess. Ask ORCH for clarification via
  COS before designing.
- **Too big for one TRDD** — split it 1→N rather than shipping an
  oversized proto-TRDD downstream.
- **Recurring design constraint** — when a pattern recurs across N
  TRDDs, or a library/boundary choice should be project-wide, file a
  PRRD proposal (`prrd-edit.py propose silver ... --routed-via
  cos-<team>`) instead of re-deciding per TRDD.
- **Edit past design / force-supersede outside a split** — non-exempt;
  request MANAGER approval first.

## Examples

**1→N split.** Proto-TRDD "add OAuth + audit logging" holds two
independent jobs. ARCH authors two children (each with fresh UUID,
`supersedes: [<parent>]`, own test/audit requirements), sets the
parent `column: superseded`, `superseded-by: [<both>]`, commits, and
AMPs ORCH via COS: "TRDD-7a1 split into 2: <c1>, <c2>".

**Setting requirements (pass-through).** Proto-TRDD "fix login race"
→ `task-type: bugfix`, `severity: high`, `release-via: deploy`,
`test-requirements: [unit, integration]`, `review-requirements:
[code-review]`. ARCH writes acceptance criteria, sets
`column: dispatch`, `assignee: null`, commits.

## Resources

For the full kanban mechanics, the 17-column transition rules, and the
approval vocabulary, use the core `ama-*` skills in `ai-maestro-plugin`
(`ama-kanban-render`, `ama-trdd-write`/`-update`/`-transition`/`-find`,
`ama-prrd-get`/`-find`/`-propose`, `ama-proposal-approvals`).

> **Superseded reference, recorded so it is not re-added:** this skill used to
> point at a single universal `prrd-trdd-kanban` skill in `ai-maestro-plugin`.
> Core replaced it with the granular `ama-*` skills above, so that name now
> resolves to nothing — a pointer to a skill that does not exist reads as
> "mechanics are handled elsewhere" and silently leaves them handled nowhere.
