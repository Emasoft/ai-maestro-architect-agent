# PLUGIN-VALIDATION.md - Validation Procedures

> **Note**: The authoritative validator is the **remote CPV** (Claude Plugins
> Validation) toolchain, which is always current and never vendored. The
> `scripts/validate_*.py` and `scripts/publish.py` files in this repo are
> CPV-supplied helpers — treat the remote validator as the source of truth.

**How to validate the ai-maestro-architect-agent plugin before publishing.**

This document covers whole-plugin validation (CPV), the test suite (pytest via
`uv`), the SECURITY gates concept, what to do when a gate fails, and the
pre-publish checklist. It is the companion to `AMAA-ARCHITECTURE.md` (design
philosophy) and `AGENT_OPERATIONS.md` (operations).

---

## 1. Whole-Plugin Validation (CPV remote validator)

Whole-plugin validation uses the remote CPV validator. The canonical command:

```bash
uvx cpv-remote-validate plugin . --strict
```

Run it from the plugin root (`.`). `uvx` fetches the current CPV release on the
fly, so you always validate against the latest rules without keeping a vendored
copy in the repo.

### What it checks

CPV runs the full validator matrix across every component — the plugin manifest
(`.claude-plugin/plugin.json`), every agent in `agents/`, every skill in
`skills/`, every command in `commands/`, the hook config (`hooks/hooks.json`),
MCP registration, documentation, encoding, and cross-references. Each finding is
classified into one of five severity levels:

| Level | Meaning |
|-------|---------|
| **CRITICAL** | Breaks the plugin — must fix before anything else |
| **MAJOR** | Significant correctness / structure problem |
| **MINOR** | Convention or quality issue (e.g. a non-user-invocable skill missing its `Loaded by <agent>` line) |
| **NIT** | Cosmetic / nice-to-have (e.g. a reference file missing a Table of Contents) |
| **WARNING** | Advisory (e.g. a missing `.python-version`, an unknown top-level field) |

### `--strict` semantics

Without `--strict`, only CRITICAL and MAJOR findings block. **With `--strict`,
NITs and MINORs also block** — the gate passes only when every level (including
NIT and MINOR) is clean. This is the publish-grade bar: a plugin shipped to a
marketplace should carry zero CRITICAL / MAJOR / MINOR / NIT findings. Use
`--strict` as the real pre-publish check; drop it only for a quick mid-work
sanity pass where you intend to clean the lower severities later.

WARNINGs are advisory and do not block even under `--strict`, but each should be
reviewed and either fixed or consciously accepted.

---

## 2. The Test Suite (pytest via uv)

The plugin ships its own tests under `tests/`. Run them with `uv`, which
provisions an ephemeral environment with `pytest` and `pyyaml`:

```bash
uv run --with pytest --with pyyaml python -m pytest tests/ -q
```

The runner must exit 0 on all-pass and non-zero on any failure — that is what a
pre-publish test gate keys off of.

### Test files

| Test file | Covers |
|-----------|--------|
| `tests/test_amaa_design_create.py` | Design-document creation, UUID generation, index registration (DRAFT) |
| `tests/test_amaa_design_validate.py` | Design validation rules and completeness checks |
| `tests/test_amaa_redesign_loop.py` | The `IMPLEMENTING -> REVIEW` redesign-loop re-entry edge |
| `tests/test_amaa_github_issue_create.py` | GitHub issue creation for architect-assigned work |
| `tests/test_architect_memory.py` | The markdown memory recall / write skills (memgrep with grep fallback) |

Tests exercise the real scripts in `scripts/` (no mocked behaviour where a real
call is possible). When a test fails, the bug is in the plugin's own code or its
test — fix it at the source; do not weaken or skip the test to make the gate
pass.

### Type-check and lint (pre-test)

Before running tests, catch type and lint errors early:

```bash
uv run --with ruff ruff check scripts/ tests/
uv run --with mypy mypy scripts/        # repo ships a .mypy_cache; types are checked
```

A clean type-check + lint pass is cheaper than discovering the same errors as a
test failure later.

---

## 3. The SECURITY Gates Concept

Security validation runs as part of the remote CPV gate
(`cpv-remote-validate plugin . --strict`). This plugin does **not** vendor a
local security scanner — security, like every other validation, runs **only via
the CPV plugin**. The CPV security gate scans the whole tree for:

1. **Injection** — command substitution, `eval`/`exec` of strings, `shell=True`.
2. **Path traversal** — `../`, absolute paths, Windows-style paths.
3. **Secrets** — AWS keys, private keys, API tokens.
4. **Hardcoded user-path leaks** — `/Users/xxx/`, `/home/xxx/`.
5. **Dangerous files** — `.env`, `credentials.json`, and similar.

**No exempt, no allowlist for real threats — devitalize or remove.** A security
finding is cleared exactly one of two ways, never by suppression:

- **Devitalize** — if the flagged text is a benign *needle* (a detector
  signature, a documentation example, a regex pattern), rewrite it into a shape
  the scanner proves inert: a raw-string signature, a fenced non-executable
  example, data instead of code. The threat's executable shape is neutralized;
  nothing is added to an exceptions list.
- **Remove** — if it is genuine execution-class code or a real leaked secret,
  delete it. A live committed secret means rotate **and** purge git history.

The exempt/allowlist mechanism — adding an item to a "known-safe" exceptions
list so the scanner ignores it — is deliberately **not used**. An allowlist of
exempted items was found to be trivially exploitable: a malicious actor simply
names a payload to match an exempted entry and the scanner waves it through.
There is no rule-suppression and no exempt list here; the only outcomes are
*devitalize* or *remove*.

The local pre-push gate is installed automatically by `publish.py` — it writes
`.githooks/pre-push` from an inline template and sets `core.hooksPath`. Every
push is forced through `publish.py`, which runs the remote CPV `--strict` gate,
so a security or structure regression is caught before it can reach the remote.

---

## 4. What To Do On Failures

Triage failures by gate, in order:

| Failure surface | First move |
|-----------------|------------|
| **CRITICAL / MAJOR** (CPV) | Fix immediately — the plugin is broken or structurally wrong. Re-run CPV after each fix. |
| **MINOR / NIT** (CPV, under `--strict`) | Apply the convention fix (add the `Loaded by <agent>` line, add a missing TOC, etc.). These block only under `--strict`, but they are publish-blocking. |
| **WARNING** (CPV) | Review each; fix or consciously accept. Do not let them accumulate silently. |
| **Test failure** (pytest) | The bug is in the plugin's code or its test. Read the failing test top-down, find the root cause, fix the source — never skip the test. |
| **SECURITY finding** | Remove the offending pattern / secret / path. A live committed secret means rotate + purge history. Never suppress the rule. |

General rules:

- **Validate, fix, re-validate in a loop** until the gate is clean — a single
  pass is not a verdict, a clean *re-run after the fix* is.
- **Never make the gate pass by weakening the gate.** Suppressing a rule,
  dropping `--strict`, or skipping a test hides the problem instead of solving
  it.
- **Re-read before re-fixing.** If a fix does not work after two attempts, read
  the whole relevant section before trying again — most "still failing" loops
  are a stale mental model, not a stubborn bug.

---

## 5. Pre-Publish Checklist

Before publishing a new version of this plugin, verify every item:

- [ ] **Version bumped consistently** — `.claude-plugin/plugin.json`,
      `pyproject.toml`, and the `README.md` version line all agree (publish.py's
      built-in version-consistency step checks plugin.json / pyproject /
      `__version__`).
- [ ] **CPV strict pass** — `uvx cpv-remote-validate plugin . --strict` reports
      zero CRITICAL / MAJOR / MINOR / NIT.
- [ ] **WARNINGs reviewed** — each remaining CPV WARNING is either fixed or
      consciously accepted.
- [ ] **Tests green** —
      `uv run --with pytest --with pyyaml python -m pytest tests/ -q` exits 0.
- [ ] **Type-check + lint clean** — `ruff check` passes on `scripts/` and
      `tests/`.
- [ ] **Security scan clean** — the CPV `--strict` gate's security scan reports
      no injection, no secrets, no hardcoded user paths, no dangerous files. Any
      finding is devitalized or removed — never exempted.
- [ ] **No `[TBD]` / placeholders** — docs and skills are complete.
- [ ] **CHANGELOG updated** — the new version's entry describes what changed.
- [ ] **Pre-push hook active** — `publish.py` installs `.githooks/pre-push`
      automatically and forces every push through itself.

Only when every box is checked is the plugin ready to publish. A green
`--strict` CPV run plus a green test suite plus a clean security scan is the
minimum bar; the checklist above makes the rest explicit.
