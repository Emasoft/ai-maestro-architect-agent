---
prrd-version: 1.1
updated: 2026-06-11T11:41:33+0200
project: ai-maestro-architect-agent
project-id: autonomous
canonical-source: design/requirements/PRRD.md
mirrors: []
---

# Project Requirements & Rules — ai-maestro-architect-agent

ARCHITECT role plugin (AMAA) — design column owner, TRDD shaping, split/group.

## §0. Canonical source + copies

| Path | Role | Update strategy |
|---|---|---|
| `design/requirements/PRRD.md` | **CANONICAL** for this project | Edit first. Bump `prrd-version:`. Update `updated:`. |

## §I. How to read this document

Rule citation form: `PRRD G<n>.<v>` (golden, user-set) or `PRRD S<n>.<v>`
(silver, manager-mutable). Rule numbers are globally unique across G/S;
promote/demote flips the letter without changing the number. The
`get-prrd.py <n>` script returns a rule's text by bare number. Full
spec: `~/.claude/rules/prrd-design-rules.md`.

## 🥇 GOLDEN — set by the USER (immutable to MANAGER)

- **G1.1** — Every agent that writes to GitHub (issue, issue comment, PR, PR comment, PR review, discussion, release note) MUST begin the body with a one-line self-identification of which agent/role/plugin authored it, because all AI Maestro agents share the single human-owner GitHub identity (the owner's gh CLI auth). Recommended leading line: _Posted by the Claude developing **<plugin-or-role>** (via the shared @owner gh auth)._ Commit messages SHOULD carry an `Agent: <role>` trailer.

## 🥈 SILVER — MANAGER-mutable (agents propose via COS)

- **S2.1** — A design document MUST reach REVIEW and be APPROVED before any handoff to the ORCHESTRATOR (AMOA); a DRAFT-state design is never handed off.
- **S3.1** — Every design handoff MUST be complete and unambiguous — no `[TBD]` / `[TODO]` / `[FIXME]` placeholders remain in the handed-off artifacts.
- **S4.1** — Every external API a design depends on MUST be researched and documented (delegate to `amaa-api-researcher`) before the design is APPROVED.
- **S5.1** — When a design flaw surfaces mid-dev (relayed by ORCH), the ARCHITECT drives the redesign loop (`IMPLEMENTING → REVIEW`) and revises or splits/groups the affected TRDD; the team never improvises around a design flaw.
- **S6.1** — Project TRDDs use the v2 `column:` schema and the `design/proposals/` → `design/tasks/` approval lifecycle; the legacy v1 `status:` enum is not used for TRDDs.
- **S7.1** — The ARCHITECT is the single writer of the design surface (design documents, the design state machine, TRDD shaping for its slice); other roles read it. A task needing a domain AMAA does not own delegates to the owner (ORCH routes) rather than writing across the boundary.

