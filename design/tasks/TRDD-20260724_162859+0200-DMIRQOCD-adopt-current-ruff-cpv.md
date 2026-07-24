---
trdd-id: DMIRQOCD
title: Adopt current ruff and CPV deliberately then bump the gate pins
column: backburner
created: 2026-07-24T16:28:59+0200
updated: 2026-07-24T16:28:59+0200
current-owner: ai-maestro-architect-agent
task-type: infra
scope: project
implementation-commits: []
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-24

- **WHY this exists:** v2.11.1 shipped after a validator-drift incident. Two gates
  were made deterministic by PINNING, which is the correct supply-chain fix but
  freezes the toolchain. This TRDD is the deliberate un-freeze.
- **Two pins are now in the tree** (both restore the last-clean-publish behavior,
  neither weakens a gate):
  1. **native ruff → `ruff==0.15.20`** in `scripts/publish.py` (Step 3 lint).
     ruff 0.16.0 broadened its DEFAULT rule set → 341 findings on byte-identical
     code (commit `1588fbc`).
  2. **CPV → `@v2.153.1`** at 4 sites: `scripts/publish.py` (Step 4 lint + Step 5
     strict), `.github/workflows/release.yml`, `.github/workflows/validate.yml`
     (commit `5dbeaa3`, BUMP PROTOCOL comment at each site).
- **What adopting newer versions will surface (already measured):**
  - native ruff 0.16.0: ~341 tree-wide default findings; 148 auto-fixable, the
    rest incl. genuine latent-quality signals (BLE001, S110, DTZ005, RUF012).
  - CPV HEAD (~v2.154.0): 2 `skillaudit:filesystem FS_WRITE` **false-positives**
    on benign gopls-install PROSE in `skills/amaa-planning-patterns/references/
    lsp-enforcement-checklist-part{1,2}*.md` (bash-comment "add $(go env GOPATH)/bin
    to ~/.zshrc"). These are a CPV classifier over-match, NOT plugin defects — do
    NOT reword the docs to dodge the scanner (forbidden). Filed upstream on CPV.
- **NEXT ACTION:** wait for the CPV FS_WRITE FP to be fixed upstream (track the CPV
  issue), then: (1) verify AMAA clean at the new CPV tag with
  `cpv-remote-validate plugin . --strict`; (2) bump ALL FOUR CPV pins in lockstep;
  (3) separately, adopt a chosen ruff and address its findings (curate a stable
  `[tool.ruff]` select so the set can't silently expand again), then bump the
  native pin. Each is its own verify-before-bump.
- **SUPERSEDED — do NOT carry forward:** nothing yet.
- **Durable artifacts:** the pin comments in `publish.py` (Step 4/5) and the two
  workflows are the load-bearing BUMP PROTOCOL; the CPV FP issue is the upstream
  tracker.

## Context

AMAA's publish/validate gates fetched their linters unpinned:
`uv run --with ruff …` and `uvx --from git+…/claude-plugins-validation …` (no ref).
Both resolve a moving target, so a new ruff or CPV release silently changed the
gate on unchanged code — a non-deterministic gate, not a stronger one. v2.11.1
pinned both to the versions current at the last clean publish (v2.11.0,
2026-07-02), mirroring the janitor's earlier CPV pin (janitor#71 / CPV#156).

## The deferred work (atomic: adopt-newer-toolchain, verify, bump)

1. **CPV:** once the FS_WRITE classifier FP is fixed upstream, verify AMAA clean at
   the new tag, then bump the 4 CPV pins together (BUMP PROTOCOL) and drop this
   note's item.
2. **ruff:** decide the target ruff, add an explicit `[tool.ruff]` config with a
   curated stable `select` (so defaults can't silently expand), fix the resulting
   real findings (the ~193 non-auto ones are judgment calls — blind-except,
   try-except-pass, naive-datetime), verify, then bump the native pin.

Reports (the drift histograms, the v2.153.1 verify) live in gitignored `reports/`
and the session scratchpad; this TRDD is the decision record.
