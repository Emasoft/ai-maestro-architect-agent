# Changelog

All notable changes to this project will be documented in this file.

## [2.17.12] - 2026-09-28

Aligns the plugin to 3-pillars spec 4.0.0 and Claude Code 2.1.249–2.1.284 (TRDD-G4OVFAJI).

### Changed
- Kanban vocabulary: the retired 17-column teaching replaced with the ratified 22-column canon (19 lifecycle + 3 exception) across the persona, five sub-agents, and the kanban skill.
- Transition authority: the removed `design → dispatch` row replaced by the live `plan → dispatch` (assignee) path; the AMOA messaging edge sourced to governance-spec R6.5 (`arch-int-member-edges`), cross-checked 2026-09-28.
- Dead pointer to `~/.claude/rules/trdd-approval-tiers.md` replaced with the seeded overlay, qualified for non-seeded workdirs.
- Channel reference: six new version rows (2.1.251/260/261/271/277/284) and delivery-observable prose extended through 2.1.271 — a `SendMessage` result is not a read receipt.
- executor.py: todo-tools note updated to the 2.1.268 allowlist; the plan file remains the tracking artifact on every model.
- PROJECT wikimem: 4.0.0 canon atom + count-arithmetic lesson recorded (EHT).

### Miscellaneous
- Update uv.lock (pipeline-generated)

Session-authored implementation commits: 4641396, 762f451, a050136, 54166d3, 0ab9d0d, dae4be8, f3a5905, b135d23. Archived card: TRDD-G4OVFAJI (aa3ac57). Pipeline-generated: 9b3ce86 (uv.lock), e10bd37 (this release).

