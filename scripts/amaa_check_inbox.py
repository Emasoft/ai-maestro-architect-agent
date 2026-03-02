#!/usr/bin/env python3
"""
eaa_check_inbox.py - AI Maestro inbox checking wrapper.

Checks for unread messages using the AMP CLI commands.

Usage:
    python eaa_check_inbox.py                    # List unread messages
    python eaa_check_inbox.py --count            # Just show count
    python eaa_check_inbox.py --all              # List all messages (not just unread)
    python eaa_check_inbox.py --json             # Output raw JSON

Environment:
    SESSION_NAME - Agent name (auto-detected from tmux if not set)
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Any


def get_session_name() -> str:
    """Get current session name from environment or tmux."""
    # Check environment variable first
    session_name = os.environ.get("SESSION_NAME")
    if session_name:
        return session_name

    # Try to get from tmux
    try:
        result = subprocess.run(
            ["tmux", "display-message", "-p", "#S"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback to default
    return "architect-agent"


def check_inbox(
    unread_only: bool = True,
    count_only: bool = False,
    api_url: str | None = None,
) -> dict[str, Any]:
    """Check inbox via AMP CLI.

    Args:
        unread_only: Only return unread messages
        count_only: Only return count, not full messages
        api_url: Unused, kept for backward compatibility

    Returns:
        Parsed JSON response as dict
    """
    _ = api_url  # No longer used; AMP CLI handles routing internally

    try:
        result = subprocess.run(
            ["amp-inbox"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        return {"error": "amp-inbox command not found. Is AMP CLI installed?"}
    except subprocess.TimeoutExpired:
        return {"error": "amp-inbox command timed out after 30 seconds"}

    if result.returncode != 0:
        stderr = result.stderr.strip()
        return {"error": f"amp-inbox failed (exit {result.returncode}): {stderr}"}

    try:
        data: dict[str, Any] = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse amp-inbox output: {e}"}

    # Filter to unread only if requested
    if unread_only and "messages" in data:
        data["messages"] = [m for m in data["messages"] if m.get("status") == "unread"]

    # Return just the count if requested
    if count_only:
        messages = data.get("messages", [])
        return {"count": len(messages)}

    return data


def format_message(msg: dict[str, Any]) -> str:
    """Format a single message for display."""
    lines = []

    priority = msg.get("priority", "normal")
    priority_icon = {"urgent": "!!!", "high": "!!", "normal": ""}.get(priority, "")

    from_agent = msg.get("from", "unknown")
    subject = msg.get("subject", "(no subject)")
    timestamp = msg.get("timestamp", msg.get("createdAt", ""))[
        :19
    ]  # Truncate to datetime

    lines.append(f"{priority_icon} [{timestamp}] From: {from_agent}")
    lines.append(f"   Subject: {subject}")

    content = msg.get("content", {})
    if isinstance(content, dict):
        msg_text = content.get("message", "")
        msg_type = content.get("type", "")
        if msg_type:
            lines.append(f"   Type: {msg_type}")
        if msg_text:
            # Truncate long messages
            if len(msg_text) > 200:
                msg_text = msg_text[:197] + "..."
            lines.append(f"   Message: {msg_text}")

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Check AI Maestro inbox for messages")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Show all messages, not just unread",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Only show unread message count",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response",
    )

    args = parser.parse_args()

    result = check_inbox(
        unread_only=not args.all,
        count_only=args.count,
    )

    if args.json:
        print(json.dumps(result, indent=2))
        sys.exit(0 if "error" not in result else 1)

    if "error" in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.count:
        count = result.get("count", result.get("unreadCount", 0))
        print(f"Unread messages: {count}")
        sys.exit(0)

    messages = result.get("messages", [])

    if not messages:
        print("No messages found.")
        sys.exit(0)

    print(f"=== {len(messages)} message(s) ===\n")
    for msg in messages:
        print(format_message(msg))
        print("-" * 40)

    sys.exit(0)


if __name__ == "__main__":
    main()
