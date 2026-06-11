#!/usr/bin/env python3
"""Tests for amaa_send_message.py (issue #7, M12).

Issue #7: the sender's identity and recipient must be resolved DYNAMICALLY from
the environment, not hardcoded to legacy names (ecos, orchestrator-master,
architect-agent, ...). These tests exercise the REAL get_session_name() and
send_message() — no mocks of the script's own logic.

Two techniques, both real:
  * get_session_name(): imported via importlib and driven with controlled env
    (monkeypatch.setenv / delenv) to assert the resolution PRECEDENCE
    (AIMAESTRO_AGENT > SESSION_NAME > tmux) and the unset-fallback. tmux is
    neutralized by emptying PATH so the subprocess lookup is FileNotFoundError —
    the real "tmux unavailable" branch.
  * send_message() argument-building: driven as a subprocess against a tiny
    real `amp-send` stand-in placed on PATH that records the argv it received.
    The script's argument-assembly logic runs unchanged; we assert the recorded
    recipient/subject/message/priority/type. (When `amp-send` is genuinely
    absent we assert the real FileNotFoundError return instead.)
"""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPT = REPO_ROOT / "scripts" / "amaa_send_message.py"

# Names the issue-#7 fix forbids get_session_name() from ever hardcoding.
LEGACY_HARDCODED_NAMES = {"ecos", "orchestrator-master", "architect-agent"}


def load_module():
    """Import amaa_send_message.py as a module to call its real functions."""
    spec = importlib.util.spec_from_file_location("amaa_send_message", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_identity_resolves_from_aimaestro_agent(monkeypatch):
    """get_session_name() returns $AIMAESTRO_AGENT when it is set (highest precedence)."""
    module = load_module()
    monkeypatch.setenv("AIMAESTRO_AGENT", "myteam-cos-design")
    monkeypatch.setenv("SESSION_NAME", "should-be-ignored")
    assert module.get_session_name() == "myteam-cos-design"


def test_aimaestro_agent_outranks_session_name(monkeypatch):
    """AIMAESTRO_AGENT takes precedence over SESSION_NAME when both are set."""
    module = load_module()
    monkeypatch.setenv("AIMAESTRO_AGENT", "primary-identity")
    monkeypatch.setenv("SESSION_NAME", "secondary-identity")
    # Proves the precedence is dynamic env resolution, not a coin-flip or a constant.
    assert module.get_session_name() == "primary-identity"


def test_identity_falls_back_to_session_name(monkeypatch):
    """With AIMAESTRO_AGENT unset, get_session_name() resolves $SESSION_NAME next."""
    module = load_module()
    monkeypatch.delenv("AIMAESTRO_AGENT", raising=False)
    monkeypatch.setenv("SESSION_NAME", "manual-override-name")
    assert module.get_session_name() == "manual-override-name"


def test_get_session_name_unset_fallback_is_never_a_legacy_name(monkeypatch):
    """Unset env + no tmux yields the neutral 'unknown-agent', and no legacy name is hardcoded in the script."""
    module = load_module()
    # The dynamic resolver echoes whatever the env says; it must never SUBSTITUTE
    # a legacy default of its own. Drive it through unset + env-set shapes and
    # assert it only ever returns the env value or the neutral 'unknown-agent'.
    monkeypatch.setenv("PATH", "")  # empty PATH -> tmux lookup is FileNotFoundError

    monkeypatch.delenv("AIMAESTRO_AGENT", raising=False)
    monkeypatch.delenv("SESSION_NAME", raising=False)
    resolved = module.get_session_name()
    assert resolved == "unknown-agent", f"unexpected fallback identity: {resolved!r}"
    assert resolved not in LEGACY_HARDCODED_NAMES

    # Even if the operator deliberately exports a legacy string, the resolver must
    # not bake one in on its own — it returns exactly the env-provided value and
    # nothing more. (Confirms the value comes from env, not from a hidden constant.)
    monkeypatch.setenv("AIMAESTRO_AGENT", "team-architect-001")
    assert module.get_session_name() == "team-architect-001"
    # Source contains none of the forbidden legacy identities as literals.
    src = SCRIPT.read_text(encoding="utf-8")
    for banned in LEGACY_HARDCODED_NAMES:
        assert f'"{banned}"' not in src and f"'{banned}'" not in src, (
            f"legacy identity {banned!r} is hardcoded in the script"
        )


def test_send_message_builds_correct_amp_send_argv(tmp_path, monkeypatch):
    """send_message() invokes amp-send with the recipient, subject, message, priority and type it was given."""
    module = load_module()

    # A real `amp-send` stand-in on PATH that records its argv to a file (the
    # script's argument-assembly runs unchanged; only the external service is
    # replaced by a trivial recorder, per the no-fake-internal-logic rule).
    # It is a POSIX /bin/sh script (absolute shebang) so it runs even though we
    # constrain PATH to only the stand-in's own directory.
    bindir = tmp_path / "bin"
    bindir.mkdir()
    argv_dump = tmp_path / "argv.txt"
    fake = bindir / "amp-send"
    fake.write_text(
        '#!/bin/sh\n'
        '# Record each positional arg on its own line, NUL-safe enough for tests.\n'
        f'for a in "$@"; do printf \'%s\\n\' "$a"; done > {str(argv_dump)!r}\n',
        encoding="utf-8",
    )
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", str(bindir))

    result = module.send_message(
        to="libs-svg-svgbbox",
        subject="Status update",
        message="all green",
        priority="high",
        msg_type="status",
    )
    assert result == {"status": "sent"}, f"unexpected send result: {result}"

    argv = argv_dump.read_text().splitlines()
    # Positional args first: recipient, subject, message.
    assert argv[0] == "libs-svg-svgbbox"
    assert argv[1] == "Status update"
    assert argv[2] == "all green"
    # Flags carry the resolved priority and type.
    assert argv[argv.index("--priority") + 1] == "high"
    assert argv[argv.index("--type") + 1] == "status"


def test_send_message_reports_error_when_amp_send_absent(monkeypatch):
    """With no amp-send on PATH, send_message() returns the real 'not found' error (no crash)."""
    module = load_module()
    monkeypatch.setenv("PATH", "")  # amp-send unresolvable -> FileNotFoundError branch
    result = module.send_message(
        to="some-agent",
        subject="s",
        message="m",
    )
    assert "error" in result, f"expected an error dict, got {result}"
    assert "amp-send not found" in result["error"], result["error"]
