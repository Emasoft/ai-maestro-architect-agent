---
trdd-id: RQETHEMJ
title: Mint the dependency-resolver tag on every release
column: planned
created: 2026-08-08T12:22:14+0200
updated: 2026-08-08T12:22:14+0200
current-owner: ai-maestro-architect-agent
task-type: infra
scope: project
min-approval-requirement: none
mandate: true
mandated-by: self
project-id: ai-maestro-architect-agent
release-via: publish
impacts: [ci-pipeline, install]
test-requirements: [unit]
npt: []
eht: []
relevant-rules: []
external-refs: [architect#25, TRDD-JT3U4ZVM]
implementation-commits: []
---

# Mint the dependency-resolver tag on every release

## Why

Claude Code resolves a plugin's `dependencies` version constraints against git
tags, but it **filters the tag list to those starting with `{plugin-name}--v`**.
AMAA ships only `v{version}`, which matches that filter **zero** times — so any
plugin pinning a version range on AMAA fails with *"has no git tag satisfying
…"* while the release plainly exists on GitHub.

Independently confirmed twice: the hub audited all 13 marketplace plugins
(9 resolve, AMAA is one of 4 that do not — `0 prefixed tags of 20`), and CPV
queried the same four outliers and got `0` for each. AMAA is one of the eight
predefined governance roles, so this is a fleet-reachable install blocker
(`TRDD-JT3U4ZVM`).

The failure is invisible from the publishing side — the release succeeds, GitHub
shows it, every local check is green, and only a **downstream** install reveals
the tag is unreadable. That is why this is pinned by tests rather than left to
review.

## What changed

`scripts/publish.py`:

- New `dependency_resolver_tag(name, version)` — a named function, so the format
  is asserted by tests instead of buried in an f-string at the call site.
- Step 12 mints `{name}--v{version}` alongside `v{version}`. Both are annotated;
  they **coexist** — they are not alternatives (`v{version}` is what GitHub
  Releases and the marketplace notify chain read).
- Step 13 pushes commit + both tags with `git push --atomic`. Load-bearing: a
  partial push would ship a release the resolver cannot see, which is the exact
  failure this work removes.
- The tag is created with **git directly**, never `claude plugin tag <tag>` —
  that CLI's positional argument is a PATH, not a tag name, so passing a tag
  there silently does nothing.

The variable is named `dep_tag` deliberately: CPV's `RC-DEP-TAG-PIPELINE` check
keys on that identifier, and under any other name `--strict` would report on
every run that this plugin "never tags `{name}--v{version}`" — a false warning,
and false warnings train everyone to ignore the real one.

## The guard I added beyond the reference implementation

`_read_project_metadata` **swallows** a missing/malformed `.claude-plugin/plugin.json`
and returns the sentinel `"unknown"`. That sentinel is *truthy*, so an emptiness
check alone would let a release mint and atomically push `unknown--v{version}` —
a tag no consumer can resolve, failing in **someone else's** install while this
repo's CI stays green. `dependency_resolver_tag` now hard-fails on it, and on a
name carrying git-illegal ref characters (caught before tagging, rather than by
`git tag` after the bump and CHANGELOG are already committed).

The name is read from `plugin.json`, never the directory name.

## On the requested backfill — what I did instead, and why

Both the hub and CPV asked for a backfill of the currently-declared version via
`git tag "$N--v$V" "v$V" && git push origin "$N--v$V"`.

**That push is not available to me and I did not force it.** This repo's
`.githooks/pre-push` refuses any push whose process ancestry does not include
`scripts/publish.py`, so lint/tests/CPV-strict are re-verified immediately before
every push. Bypassing it — or reaching around it with `gh api` to create the ref
out of band — would be circumventing a deliberate quality gate to save one step.

The gap closes itself instead: **publishing this fix mints the resolver tag for
the new release, which then IS the declared version.** The concern behind the
backfill request — *"a future-only fix leaves the current declared version
unresolvable"* — does not survive publishing immediately, which is the plan.

**Known limitation, stated rather than hidden:** the 20 historical `v*` releases
remain without prefixed tags, so a consumer pinning a range that excludes the
current release still cannot resolve. No such consumer is known. If one appears,
the backfill belongs in a publish.py subcommand that runs under the hook, not in
a hand-run push.

## Acceptance criteria

- [x] Tag format asserted by unit tests, not by review
- [x] `v{version}` still minted — the two tags coexist
- [x] Both tags pushed in ONE `--atomic` transaction
- [x] Plugin name read from `plugin.json`, never the directory
- [x] Hard-fail on the `"unknown"` sentinel and on illegal ref characters
- [x] Variable named `dep_tag` (CPV `RC-DEP-TAG-PIPELINE` predicate)
- [x] No pre-push hook bypass
- [ ] Verified on origin with the check that cannot lie:
      `git ls-remote --tags origin | grep -- "--v"`

## Verification

The only trustworthy check is the one that reads the refs Claude Code itself
resolves against. `grep -c dep_tag scripts/publish.py` is a **one-way** signal:
`>0` means CPV's `--fix` will leave the stage alone; `0` is *inconclusive*, not a
failure — a plugin naming the variable `resolver_tag` is completely correct and
greps to zero. Confirm at release time on origin, never from the source shape.

## Approval log

- 2026-08-08T12:22:14+0200 — MANDATE issued by ARCHITECT ai-maestro-architect-agent
  (min-approval-requirement: none). Pre-approved: issuer authority >= required
  approver. In-scope infra work on AMAA's own release pipeline, reversible, no
  baseline deviation, no other project's tree touched.
