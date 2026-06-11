# Dialog loop C — Pre-PR gate

**Purpose:** A MEMBER must clear an explicit "I believe it's done — open the PR?"
check with ORCH **before** opening a PR or notifying INT. This protects
INTEGRATOR tokens (and reviewer attention) from premature or incomplete PRs — INT
should only ever see PRs that ORCH has already agreed are ready.

**Who:** MEMBER ⇄ ORCH (direct edge). Only after ORCH clears the gate does the
MEMBER open the PR / notify INT.

**When:** End of `dev`, before `dev → testing` / before any PR is opened.

## Contents

- MEMBER → ORCH (readiness claim)
- ORCH decision
- Resolution

---

## MEMBER → ORCH (readiness claim)

> Task: **TRDD-<id8>**
> **I believe this is done. Open the PR?**
>
> - **Acceptance criteria:** <each criterion → met? with evidence>
> - **Tests:** <added/updated tests; local result: pass/fail counts>
> - **NPT/EHT:** <all prerequisites done; all effects handled — callers updated,
>   docs updated, downstream tests green> (or "none")
> - **Self-review:** <ran lint/typecheck? result> ; <anything I'm unsure about>
> - **Out of scope / deferred:** <anything intentionally not done, and why>

## ORCH decision

| Decision | When | Next |
|---|---|---|
| **Cleared** | criteria met, tests green, effects handled | MEMBER opens PR / notifies INT (`dev → testing`) |
| **Not yet** | a criterion unmet, tests failing, an EHT open | MEMBER returns to `dev`; loop B (in-dev issue) if blocked |
| **Design concern** | the "done" work reveals the design was wrong | ORCH relays to ARCH → redesign loop (`IMPLEMENTING → REVIEW`) |

## Resolution

> ORCH → MEMBER: [ ] cleared — open the PR  /  [ ] not yet — <what's missing>  /
> [ ] hold — ARCH is revising the design

**INT only sees ORCH-cleared PRs.** A MEMBER never opens a PR or pings INT on its
own initiative — the gate is what keeps premature PRs (and the token cost of
reviewing them) out of the INTEGRATOR's queue.

**Note on the column flip:** clearing this gate sends the work to `testing`/PR —
it does NOT mark the TRDD `completed`. INTEGRATOR owns the final `→ completed`
flip after validating the merged PR actually satisfies the TRDD. Nobody
self-marks completed.
