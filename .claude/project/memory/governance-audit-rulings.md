---
name: governance-audit-rulings
description: "why do two archived TRDD filenames use lowercase uuid ids / is the baseline-tag-protect third github ruleset approved / governance audit flagged extra ruleset or wrong trdd id format — hub rulings say grandfathered and compliant, do not migrate or remove"
ocd: 2026-08-18
lmd: 2026-08-18
metadata:
  node_type: memory
  type: project
  tier: component
publish-globally: false
---

# governance-audit-rulings


^ATOM-HBS5-GSH0 [desc: "Hub rulings: legacy-uuid archived TRDD filenames grandfathered; baseline-tag-protect ruleset compliant", keywords: legacy_uuid_trdd_filename lowercase_hex_id_in_archived_trdd baseline-tag-protect_extra_ruleset third_github_ruleset_unapproved tier-2_ruleset_deviation_provenance do_not_rename_archived_trdd_files, type: project, ocd: 2026-08-18, lmd: 2026-08-18]

Two hub rulings from the Phase-2 GO dispatch (2026-08-18, USER-delegated hub, programme TRDD-BRRJK57P), recorded so future governance audits find provenance in-repo. (1) LEGACY-UUID FILENAMES — RECORD, DON'T MIGRATE: design/archived/TRDD-20260619_010136+0200-536c42e3-*.md and TRDD-20260622_030254+0200-364ccafc-*.md predate the v2 8-char base36 id scheme; renaming archived files would break inbound references for zero gain. They are grandfathered v1 ids — no lint pass should rename them. (2) BASELINE-TAG-PROTECT — RULED RATIFIED-BASELINE COMPLIANCE: the third GitHub ruleset (id 17715767, target tag, deletion+update on refs/tags/v*.*.*, bypass_actors []) is additive hardening consistent with the ratified baseline's intent; axis2 V1's Tier-2 provenance question is CLOSED by this ruling. Decision record: TRDD-ET0STPKK.


^ATOM-8OXF-85HY [desc: "Phase-2 remediation outcome: script-surface fix, lifecycle guard, dead-code delete, fail-fast ratchet live", keywords: phase-2_remediation_landed planning_patterns_scripts_crash_fixed archive_bypass_guard fail-fast_ratchet_extend-select run_search_script_empty_result git_mv_drops_working_tree_edits, type: project, ocd: 2026-08-18, lmd: 2026-08-18]

Phase-2 remediation (hub programme TRDD-BRRJK57P, GO 2026-08-18) landed in v2.15.24+: (1) planning-patterns scripts fixed — the 10 cross_platform importers pointed at nonexistent skills/shared, now parents[3]/lib; analyzer_scaffold's generated template inlines the atomic helpers so generated analyzers are standalone (TRDD-WDM195GD, 2ca94c3). (2) design-lifecycle machine ratified 5-state; archive subcommand gained an allowed-from guard (implemented/deprecated/superseded, --force override, None-status refusal); 14 docs reconciled; phantom implementing/completed vocabulary removed everywhere incl. sync-status label maps (TRDD-QW4ISL8Z, 8ef38f3). (3) lib/report_utils.py deleted — mandate with zero callers (TRDD-HN65IC8P, 9d2c936). (4) fail-fast ratchet LIVE: pyproject [tool.ruff.lint] extend-select = BLE001,S110,PLW1510,TRY004; every subprocess.run carries explicit check= and every remaining broad except carries a per-site noqa WITH its reason; real defects fixed: run_search_script clones (crashed search read as 'no results'), publish.py manifest/NODEJS swallows, claude-plugin-install read_plugin_meta + frontmatter-validator false-PASS (TRDD-DMIRQOCD, aa118ea/0cbcbe5/9276e2e). Gotcha worth keeping: git mv stages the rename from the INDEX, not the working tree — edit-then-mv silently drops the edits from the commit.

## Notes and lessons learned
