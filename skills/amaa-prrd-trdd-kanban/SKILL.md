---
name: amaa-prrd-trdd-kanban
description: "ARCHITECT's role in the PRRD / TRDD / Kanban workflow. Use when ARCH shapes a proto-TRDD into a full TRDD, decides whether to split (1→N), group (N→1), or pass-through, authors all the verification / impact / delivery frontmatter, and writes the prose body with acceptance criteria."
allowed-tools: "Bash(python3:*), Bash(get-prrd.py:*), Bash(findprrd.py:*), Bash(findtrdd.py:*), Bash(kanban.py:*), Read, Edit, Grep, Glob"
metadata:
  author: "Emasoft"
  version: "1.0.0"
---

## Overview

This is the ARCHITECT's role-specific layer of the PRRD / TRDD /
Kanban model. For universal mechanics, see `prrd-trdd-kanban` in
`ai-maestro-plugin`.

ARCHITECT owns the **design column** — the only column with a 1→N
(split) and N→1 (group) topology. A proto-TRDD comes in; one or more
fully-designed TRDDs come out. The output TRDDs land in `dispatch`
ready for assignment.

## Columns ARCH owns

| Column | Ownership detail |
|---|---|
| `design` | ARCH receives proto-TRDDs from ORCH. Shapes them: fills frontmatter, writes the body, sets acceptance criteria, decides task-type / test-requirements / audit-requirements / release-via, identifies NPT and EHT children. |

## Transitions ARCH triggers

- **#4** `design → dispatch` — pass-through, no decomposition needed
- **#5** `design → superseded` — split: original retired, N child TRDDs created
- **#5b** `(new) → dispatch` — child TRDDs born from a split or group

## PRRD authority

ARCHITECT may **propose** PRRD changes (typically silver) when a
recurring design constraint should become formal:

```bash
prrd-edit.py propose silver "<text>" \
            --target <N or null for new rule> \
            --proposed-by architect-<team> \
            --routed-via cos-<team>
```

Common scenarios for ARCH-originated proposals:
- A pattern recurred across N TRDDs and should become a rule
- A library / dependency / framework choice should be project-wide
- A boundary between modules should be enforced

## Per-column checklists

### Shaping a proto-TRDD (design column, single output)

- [ ] Read the proto-TRDD's body — paraphrase of user request
- [ ] Identify `task-type:` (`feature` / `bugfix` / `refactor` /
      `docs` / `infra` / `security` / `artifact` / `spike` / `audit`)
- [ ] Set `severity:` and `effort:` based on judgment
- [ ] Determine `release-via:` (`publish` for tools/packages,
      `deploy` for services, `none` for internal-only)
- [ ] Identify `test-requirements:` (which test types are mandatory)
- [ ] Identify `audit-requirements:` (security scan? adversarial scan?)
- [ ] Identify `review-requirements:` (human-review? code-review?
      design-review?)
- [ ] If artifact-producing, set `artifact-kinds:` (`icon` /`sound` /
      `html` / `animation` etc.)
- [ ] Identify `runtime-targets:` (which platforms must pass)
- [ ] Identify `impacts:` (does this change install / dependencies /
      config / migration / public-api / ci-pipeline?)
- [ ] Identify NPT children: prerequisites that must complete BEFORE
      `dev` can proceed. Author each as a separate TRDD; link via `npt:`
- [ ] Identify EHT children: consequence-handling tasks that must
      complete BEFORE `complete`. Author each as a separate TRDD;
      link via `eht:`
- [ ] Write the body:
      - `## STATE` block (mandatory if multi-session)
      - `## Acceptance criteria` — bulleted list of testable items
      - `## Design notes` — rationale, alternatives considered
      - `## Out of scope` — explicit non-goals
- [ ] Cite relevant PRRD rules in `relevant-rules:`
- [ ] Edit `column: dispatch`, `assignee: null`, bump `updated:`
- [ ] AMP-send to ORCH (via COS): "TRDD-<id> designed; ready for dispatch"

### Splitting a proto-TRDD (1 → N)

- [ ] Read the proto-TRDD; identify N independent sub-tasks
- [ ] For each sub-task, author a new TRDD with:
      - fresh UUID and timestamp
      - `parent-trdd: <T_parent.short_ref>`
      - `supersedes: [<T_parent.short_ref>]`
      - `column: dispatch` (or `design` if it needs further design)
      - own task-type, test-requirements, etc.
- [ ] Update the parent TRDD:
      - `column: superseded`
      - `superseded-by: [<all-child-refs>]`
- [ ] Stage + commit all new files + parent edit:
      `git add design/tasks/TRDD-*; git commit -m "design: split
      TRDD-<parent> into <N>"`
- [ ] AMP-send to ORCH (via COS): "TRDD-<parent> split into <N>:
      <child-refs>"

### Grouping (N → 1)

- [ ] Identify the N proto-TRDDs being merged
- [ ] Author the new combined TRDD:
      - fresh UUID and timestamp
      - `supersedes: [<all-input-refs>]`
      - merged frontmatter (test-requirements = union of inputs, etc.)
      - body explains the rationale for grouping
- [ ] For each input TRDD:
      - `column: superseded`
      - `superseded-by: [<combined-ref>]`
- [ ] Stage + commit
- [ ] AMP-send to ORCH (via COS): "TRDDs <input-refs> grouped into
      <combined-ref>"

### Citing PRRD rules

When designing, ALWAYS consult the PRRD for relevant constraints:

```bash
findprrd.py --grep "<keyword>"     # find rules touching a topic
get-prrd.py --list                 # browse all rules
get-prrd.py --cite <N.v>           # quote the rule in the body
```

Cite in:
- `relevant-rules:` frontmatter (bare numbers, pinned versions allowed)
- Body prose (`PRRD G64.134 — Use AID auth ...`)

A TRDD with empty `relevant-rules:` is a TRDD claiming to be
unconstrained by any rule. Possible but worth verifying.

## NPT vs EHT discipline

| Concept | Purpose | Position in parent's pipeline | Example |
|---|---|---|---|
| **NPT** | Prerequisite | Must complete BEFORE parent's `dev` | "Refactor auth module" needs NPT "Update auth schema first" |
| **EHT** | Effects handling | Must complete BEFORE parent's `complete` | "Refactor auth module" needs EHT "Update all callers", "Update docs" |

ARCHITECT decides both lists during design. NPTs are usually
authored at the same time as the parent. EHTs may be authored later
(during `dev`) when consequences are clearer.

## Resources

- Universal skill: `prrd-trdd-kanban`
- Existing design skills: `amaa-design-management`, `amaa-design-lifecycle`,
  `amaa-design-communication-patterns`
- ARCHITECT persona: `agents/ai-maestro-architect-agent-main-agent.md`
