#!/usr/bin/env python3
"""
eaa_send_message.py - AI Maestro message sending wrapper.

Sends messages to other agents via the AI Maestro API.

Usage:
    python eaa_send_message.py --to <agent> --subject <subject> --message <message>
    python eaa_send_message.py --to <agent> --subject <subject> --message <message> --priority high
    python eaa_send_message.py --to <agent> --subject <subject> --type request --message <message>

Environment:
    AIMAESTRO_API - API base URL (default: http://localhost:23000)
    SESSION_NAME - Sender agent name (auto-detected from tmux if not set)
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
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


def send_message(
    to: str,
    subject: str,
    message: str,
    priority: str = "normal",
    msg_type: str = "notification",
    api_url: str | None = None,
) -> dict[str, Any]:
    """Send message via AI Maestro API.

    Args:
        to: Recipient agent name (full session name like 'libs-svg-svgbbox')
        subject: Message subject
        message: Message content
        priority: Message priority (normal, high, urgent)
        msg_type: Message type (notification, request, response, status)
        api_url: API base URL (default: from env or localhost:23000)

    Returns:
        API response as dict
    """
    if api_url is None:
        api_url = os.environ.get("AIMAESTRO_API", "http://localhost:23000")

    sender = get_session_name()

    payload = {
        "from": sender,
        "to": to,
        "subject": subject,
        "priority": priority,
        "content": {
            "type": msg_type,
            "message": message,
        }
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        f"{api_url}/api/messages",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {error_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Send message via AI Maestro API"
    )
    parser.add_argument(
        "--to",
        required=True,
        help="Recipient agent name (full session name)",
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="Message subject",
    )
    parser.add_argument(
        "--message",
        required=True,
        help="Message content",
    )
    parser.add_argument(
        "--priority",
        choices=["normal", "high", "urgent"],
        default="normal",
        help="Message priority (default: normal)",
    )
    parser.add_argument(
        "--type",
        dest="msg_type",
        choices=["notification", "request", "response", "status"],
        default="notification",
        help="Message type (default: notification)",
    )
    parser.add_argument(
        "--api-url",
        help="AI Maestro API URL (default: from AIMAESTRO_API env or http://localhost:23000)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response",
    )

    args = parser.parse_args()

    result = send_message(
        to=args.to,
        subject=args.subject,
        message=args.message,
        priority=args.priority,
        msg_type=args.msg_type,
        api_url=args.api_url,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            msg_id = result.get("id", result.get("messageId", "unknown"))
            print(f"Message sent successfully (ID: {msg_id})")

    sys.exit(0 if "error" not in result else 1)


if __name__ == "__main__":
    main()
