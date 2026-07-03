---
trdd-id: 536c42e3-2a21-4d9f-8b6f-c746f3755780
title: Propagate governance R26–R40 into AMAA persona + SCEN, and apply the R6-v3/R29-R30/ruling-1 audit fixes (#17)
column: published
created: 2026-06-19T01:01:36+0200
updated: 2026-07-02T15:52:13+0200
published-version: 2.11.0
published-at: 2026-07-02T15:52:13+0200
current-owner: ai-maestro-architect-agent
assignee: ai-maestro-architect-agent
priority: 2
severity: MEDIUM
effort: L
task-type: docs
parent-trdd: null
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [lint]
review-requirements: [code-review]
relevant-rules: []
impacts: []
external-refs: ["github.com/Emasoft/ai-maestro-architect-agent/issues/17", "github.com/Emasoft/ai-maestro/issues/37"]
---

# TRDD-536c42e3 — Propagate governance R26–R40 into AMAA persona + SCEN, and apply the R6-v3/R29-R30/ruling-1 audit fixes (#17)

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-06-19

**Source of truth:** GitHub issue **Emasoft/ai-maestro-architect-agent#17** (MANAGER's adversarially-verified work order) + keystone **Emasoft/ai-maestro#37** (defines R23/R24/R25 + the 15 USER security rules R26–R40). Canonical rule text: `…/AI-MAESTRO-PLUGIN/ai-maestro-plugin/skills/team-governance/references/GOVERNANCE-RULES.md` v4.0.2 (READ-ONLY — other repo; R26–R40 at lines 1279–1432).

**Current plugin version:** v2.8.2. **Tree:** clean at start.

**Two-part scope:**
- **Phase 1 — governance audit fixes** (MANAGER's work order; R23 `/api/` part ALREADY DONE in v2.8.1/2.8.2 ✅ historical). LIVE: M2 (ROLE_BOUNDARIES per-AMAMA-approval → R29/R30 team-lifecycle), M3+A1 (FULL_PROJECT_WORKFLOW matrix+body direct-to-AMAMA → route via AMCOS, R6.2/6.3), M4 (edge-case-protocols ×2 twins + session-memory handoff files: direct-to-AMAMA escalation → via AMCOS, design-handoff AMAA→AMOA direct; R6.5), m5a-m5e/m7/A2 (ruling-1 apex-naming: USER→**MAESTRO** in the apex-authority sense, **KEEP PRRD Tier-3 `USER` token where it is the literal tier label**).
- **Phase 2 — R26–R40 persona + SCEN.** Internalize R26–R40 into `agents/ai-maestro-architect-agent-main-agent.md` (persona currently cites only R6). Highest-impact for ARCHITECT: R26 (identity immutable to self), R27 (self-install via core skills + own-COS approval + CPV scan), R28 (AID 3-check; never client-supplied id/title/scope), R32 (agents NEVER sudo / no X-Sudo-Token), R37 (apex = MAESTRO), R39 (users work via ASSISTANTs; AMAA never directly contacts users). **No SCEN tests exist yet** — create `tests/scenarios/SCEN-*.scen.md` from scratch.

**PHASE 1 — DONE (shipping in this release).** All audit fixes applied across 12 files (ROLE_BOUNDARIES M2+m5c; FULL_PROJECT_WORKFLOW M3+A1+m5b; edge-case ×2 twins M4+m5e; session-memory handoffs ×3 M4; AGENT_OPERATIONS A2; AMAA-ARCHITECTURE+SKILL m7; rule-14 m5d; main-agent m5a). CPV `--strict` clean (0/0/0/0). Literal Tier-3 `USER` ladder tokens preserved (caveat honored). 3 out-of-scope "Human Review via AMAMA" instances (AGENT_OPERATIONS:468, label-taxonomy:45-46) LEFT as-is (legit MANAGER human-review relay, R6.6) — flagged to MANAGER on #17 for confirmation.

**PHASE 2 — DONE (shipping in this release).** Persona `agents/ai-maestro-architect-agent-main-agent.md` now internalizes R26–R40 (new "Foundational governance rules R26–R40" block under Governance Integration: R26 identity-immutable, R27 self-install-via-core-skills, R28 AID 3-check, R32 never-sudo, R23 frozen-CLI, R36/R37 apex-MAESTRO, R38/R39 ASSISTANT-user model, R29/R30/R31 base-member) + fixed a residual "governance API" → frozen-CLI ref. Created `tests/scenarios/governance-scenarios.md` (SCEN-A01–A10) modeled on the MANAGER gold standard. CPV `--strict` clean (0/0/0/0; cleared a false-positive `skill/subagent` MAJOR by rewording the slash-list to prose).

**STATUS: COMPLETE.** Both phases shipped (Phase 1 = v2.9.0; Phase 2 = this release). Only open thread: the 3 "Human Review via AMAMA" relay lines flagged to the MANAGER on #17 (left as legit R6.6 human-review relay pending the MANAGER's call). No further AMAA action until the MANAGER responds.

**Load-bearing caveats:**
- ruling-1: change ONLY the apex-authority-sense `USER`→`MAESTRO`; the literal PRRD "Tier 3 — USER approval" ladder token stays `USER` (it is the tier label, borderline-exempt per the audit).
- R6-v3 routing: team-internal→MANAGER edges go via **AMCOS** (COS). The design handoff AMAA→AMOA is a DIRECT edge (never via AMAMA). COS→MANAGER (AMCOS→AMAMA) is PERMITTED (don't "fix" those).
- Cross-project: GOVERNANCE-RULES.md is READ-ONLY (it lives in ai-maestro-plugin). Apply changes ONLY in this repo.
- The `-ops` twins differ only in tail formatting; the cited lines are identical in both — fix both twins.

**SUPERSEDED — do NOT carry forward:**
- ✗ The audit's M1 (`/api/governance` recipient-resolution) + m6 (`/api/messages` error cell) — already fixed in v2.8.1/2.8.2 (the #16 decoupling). Treat the report's R23 section as historical.
- ✗ The v2.8.0 line numbers in the audit — re-locate against v2.8.2 (files shifted).

**Durable artifacts to read before acting:** #17 (full verified work order, per-finding file:line + exact replacement) · #37 (R26–R40 summary + canonical pointer) · GOVERNANCE-RULES.md v4.0.2 R26–R40 (lines 1279–1432) · [[decouple-api-to-cli]] (the R23 work already shipped).

## Background

The MANAGER (assistant-manager-agent) ran an adversarially-verified governance-compliance audit of AMAA against `GOVERNANCE-RULES.md` v4.0.2 and filed the work order as #17, bundled with the directive to propagate the 15 new USER-set security rules R26–R40 (keystone #37) into the AMAA persona + SCEN tests. The MANAGER edits only its own plugin; AMAA applies these in its own repo (cross-project rule).

## Plan

1. **Phase 1 (this release):** apply the audit fixes (M2/M3/M4/A1 MAJOR + m5*/m7/A2 MINOR). Group by file, disjoint scopes, exact MANAGER specs + caveats. CPV `--strict` clean → `publish.py --minor` → report on #17.
2. **Phase 2 (next release):** internalize R26–R40 into the persona; create the `tests/scenarios/` SCEN suite asserting the governance behaviors. CPV clean → publish → confirm on #17 + #37.

## Approval log
- 2026-06-19T01:01:36+0200 — Authored. Authority: MANAGER-assigned via #17 (Tier-0 in-repo application of a MANAGER directive). Executing autonomously under the standing fleet-readiness goal.
