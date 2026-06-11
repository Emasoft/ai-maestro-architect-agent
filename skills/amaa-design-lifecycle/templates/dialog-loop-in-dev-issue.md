# Dialog loop B — In-dev issue dialog

**Purpose:** While implementing, the MEMBER raises any issue, ambiguity, or
blocker to ORCH **immediately** — never silently improvises around it. ORCH pulls
in the right owner: ARCH for a design problem, INT for a CI/merge problem. This
keeps the team from baking workarounds around a flaw that should be fixed at the
source.

**Who:** MEMBER ⇄ ORCH (direct edge). ORCH escalates within the team to ARCH
(design) or INT (CI/merge). MANAGER is not in this loop (R6 v3 — reached only via
COS at the team boundary).

**When:** Any time during `dev`, the moment an issue appears.

## Contents

- MEMBER → ORCH (issue report)
- ORCH routing
- Resolution

---

## MEMBER → ORCH (issue report)

> Task: **TRDD-<id8>**
> **Issue type:** [ ] design  [ ] CI/merge  [ ] ambiguity  [ ] blocker  [ ] other
> **What I hit:** <concrete description — file:line, error text, the assumption
> that didn't hold>
> **What I need:** <decision / clarification / a prerequisite / a design fix>
> **What I am NOT doing:** improvising around it. Paused pending your call.

## ORCH routing

| Issue type | ORCH routes to | Then |
|---|---|---|
| **Design flaw** (a TRDD/design assumption is wrong) | **ARCH** | ARCH runs [op-accept-redesign-request.md](../references/op-accept-redesign-request.md); may trigger `IMPLEMENTING → REVIEW` |
| **CI / merge / pipeline** | **INT** | INT advises or fixes the pipeline; MEMBER resumes |
| **Ambiguity** (design is fine, wording unclear) | answer directly | loop closes, MEMBER resumes |
| **Blocker** (needs an NPT) | author/dispatch the NPT | MEMBER waits or context-switches |

## Resolution

> ORCH → MEMBER: <decision / answer / "ARCH is revising the design, hold" /
> "NPT TRDD-<id8> dispatched, resume after">

The MEMBER resumes only on an explicit ORCH go-ahead. **Never** work around a
design flaw locally — that produces code that passes review but encodes the
wrong design, and the flaw resurfaces later at higher cost.
