#!/usr/bin/env python3
"""Regression tests for the dependency-resolver release tag (architect#25).

Claude Code resolves a plugin's `dependencies` version constraints against git
tags, but it filters the tag list to those starting with `{plugin-name}--v`. A
repo tagged only `v2.8.0` matches that filter zero times, so every consumer that
pins a range on it fails with "has no git tag satisfying ..." while the release
plainly exists. These tests pin the tag FORMAT and the publish pipeline's use of
it, because the failure is silent from the publishing side: the release succeeds,
GitHub shows it, and only a downstream install reveals the tag is unreadable.

The publish pipeline is exercised structurally (the module is a script with a
`main()`, not an importable library API) plus a direct unit test of the pure
tag-building helper.
"""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
PUBLISH_PY = REPO_ROOT / "scripts" / "publish.py"
MANIFEST = REPO_ROOT / ".claude-plugin" / "plugin.json"


def _load_publish_module():
    """Import scripts/publish.py by path (it is a script, not a package member)."""
    spec = importlib.util.spec_from_file_location("amaa_publish", PUBLISH_PY)
    assert spec and spec.loader, f"cannot load {PUBLISH_PY}"
    module = importlib.util.module_from_spec(spec)
    # Register BEFORE exec: publish.py defines dataclasses, and @dataclass
    # resolves its own module out of sys.modules to build __annotations__. An
    # unregistered module makes that lookup return None and the import dies with
    # a bare AttributeError that looks nothing like the real cause.
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    return module


def test_publish_script_exists():
    """A missing publish.py must fail loudly, not silently skip every test."""
    assert PUBLISH_PY.is_file(), f"{PUBLISH_PY} not found"


class TestDependencyResolverTagFormat:
    """The tag string itself — the part Claude Code's filter actually reads."""

    def test_format_is_name_double_dash_v_version(self):
        mod = _load_publish_module()
        assert mod.dependency_resolver_tag("ai-maestro-architect-agent", "2.13.0") == (
            "ai-maestro-architect-agent--v2.13.0"
        )

    def test_separator_is_a_DOUBLE_dash(self):
        """A single dash is indistinguishable from a hyphen in the plugin name."""
        mod = _load_publish_module()
        tag = mod.dependency_resolver_tag("ai-maestro-architect-agent", "1.0.0")
        assert "--v" in tag
        assert not re.search(r"(?<!-)-v1\.0\.0$", tag), "separator collapsed to a single dash"

    def test_rejects_a_version_that_already_carries_v(self):
        """`v` belongs to the tag format; a `v`-prefixed version yields `--vv1.0.0`."""
        mod = _load_publish_module()
        with pytest.raises(ValueError, match="without a leading 'v'"):
            mod.dependency_resolver_tag("some-plugin", "v1.0.0")

    def test_rejects_empty_inputs(self):
        mod = _load_publish_module()
        with pytest.raises(ValueError):
            mod.dependency_resolver_tag("", "1.0.0")
        with pytest.raises(ValueError):
            mod.dependency_resolver_tag("some-plugin", "")

    def test_rejects_the_unknown_sentinel(self):
        """`_read_project_metadata` returns "unknown" on an unreadable manifest.

        That sentinel is truthy, so an emptiness check alone lets a release mint
        and atomically push `unknown--v{version}` — a tag no consumer resolves,
        failing in someone else's install while this repo's CI stays green.
        """
        mod = _load_publish_module()
        with pytest.raises(ValueError, match="unknown"):
            mod.dependency_resolver_tag("unknown", "1.0.0")

    def test_rejects_a_name_that_is_not_a_valid_ref_component(self):
        """Caught before tagging, not by `git tag` after the bump is committed."""
        mod = _load_publish_module()
        for bad in ("has space", "car^et", "ti~lde", "co:lon", "que?st", "st*ar", "brk[t", "back\\slash"):
            with pytest.raises(ValueError, match="valid git ref"):
                mod.dependency_resolver_tag(bad, "1.0.0")

    def test_tag_is_a_valid_git_ref_name(self):
        """git rejects refs with spaces, `~`, `^`, `:`, `?`, `*`, `[`, or `\\`."""
        mod = _load_publish_module()
        tag = mod.dependency_resolver_tag("ai-maestro-architect-agent", "10.20.30")
        assert not re.search(r"[ ~^:?*\[\\]", tag), f"invalid git ref characters in {tag!r}"


class TestPublishPipelineUsesTheTag:
    """Structural assertions — the helper existing is useless if unused."""

    def test_pipeline_calls_the_helper(self):
        src = PUBLISH_PY.read_text(encoding="utf-8")
        assert "dependency_resolver_tag(" in src, (
            "publish.py defines the resolver-tag helper but never calls it"
        )

    def test_pipeline_creates_the_tag_with_git_not_the_claude_cli(self):
        """`claude plugin tag <tag>` takes a PATH positional and silently no-ops."""
        src = PUBLISH_PY.read_text(encoding="utf-8")
        assert not re.search(r'"claude",\s*"plugin",\s*"tag"', src), (
            "publish.py shells out to `claude plugin tag`, whose positional arg is a "
            "PATH, not a tag name — it silently does nothing (architect#25)"
        )

    def test_both_tags_are_pushed_atomically(self):
        """A partial push ships a release the resolver cannot see."""
        src = PUBLISH_PY.read_text(encoding="utf-8")
        assert '"--atomic"' in src, "the release push is not atomic"
        push_lines = [ln for ln in src.splitlines() if "--atomic" in ln]
        assert push_lines, "no atomic push found"

    def test_bare_version_tag_is_still_created(self):
        """GitHub Releases + the marketplace notify chain read `v{version}`."""
        src = PUBLISH_PY.read_text(encoding="utf-8")
        assert 'f"v{new_version}"' in src, (
            "the bare v{version} tag was dropped — the two tags coexist, they are "
            "not alternatives"
        )


def test_manifest_keeps_its_dependency_version_pin():
    """The pin stays: the resolver bug was ours (wrong tag names), not upstream's.

    The original guidance was to drop the `version` field; that was retracted —
    dropping it would have treated a spec requirement we never met as an upstream
    bug, and silently removed the only floor protecting against an incompatible
    core.
    """
    import json

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    deps = manifest.get("dependencies", [])
    assert deps, "plugin.json declares no dependencies"
    for dep in deps:
        assert "version" in dep, (
            f"dependency {dep.get('name')!r} lost its version pin — the pin is kept "
            "deliberately (architect#25 correction)"
        )
