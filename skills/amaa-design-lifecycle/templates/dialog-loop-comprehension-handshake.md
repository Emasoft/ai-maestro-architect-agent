# Dialog loop A — Task-comprehension handshake

**Purpose:** Before a MEMBER writes a single line of code, ORCH and the assigned
MEMBER run this handshake so that misunderstandings, ambiguities, and foreseen
design problems are caught *before* effort is spent — not discovered in review.
The MEMBER MUST answer every question before coding starts.

**Who:** ORCH ⇄ assigned MEMBER (within-team direct edge, R6 v3). A surfaced
**design** problem is relayed by ORCH to ARCH, who runs
[op-accept-redesign-request.md](../references/op-accept-redesign-request.md).

**When:** Immediately after dispatch (`dispatch → dev`), before the first commit.

## Contents

- ORCH → MEMBER (question set)
- MEMBER → ORCH (answers)
- Resolution

---

## ORCH → MEMBER (question set)

> Task: **TRDD-<id8>** — <one-line title>
> Before you start, answer ALL of the following. Do not begin coding until we
> have closed every open item.
>
> 1. **Restate the task** in your own words — what is "done"?
> 2. **Files / domains** you will touch (and any you must NOT touch).
> 3. **Ambiguities** — anything in the TRDD or design you read more than one way.
> 4. **Foreseen risks / issues** — what could go wrong, what looks fragile.
> 5. **Anticipated NPT/EHT** — prerequisites you'll need first, and effects
>    (callers, docs, downstream tests) you'll have to handle after.

## MEMBER → ORCH (answers)

> 1. Restated task: …
> 2. Files/domains: …  (own: …; will NOT touch: …)
> 3. Ambiguities: … (or "none")
> 4. Foreseen risks: … (or "none")
> 5. NPT: … / EHT: … (or "none")
>
> **Open items I need resolved before I start:** … (or "none — ready to code")

## Resolution

- **No open items** → ORCH confirms; MEMBER starts (`dev`).
- **Implementation-level open items** → ORCH answers directly; loop closes.
- **Design-level open item (a TRDD/design assumption is wrong or unbuildable)**
  → ORCH relays to ARCH. ARCH classifies and, if it's a genuine design flaw,
  drives the `IMPLEMENTING → REVIEW` redesign loop (revise the TRDD or author
  new ones via split/group). The MEMBER does NOT improvise around it and does
  NOT start until the design is corrected and re-approved.

**Token rationale:** one structured round-trip here is far cheaper than a wrong
implementation discovered at review — which burns the MEMBER's dev tokens, the
reviewer's tokens, and a full redesign anyway.
