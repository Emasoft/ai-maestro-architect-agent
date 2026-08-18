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

## Notes and lessons learned
