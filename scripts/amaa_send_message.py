#!/usr/bin/env python3
"""
eaa_send_message.py - AI Maestro message sending wrapper.

Sends messages to other agents via the AMP CLI (amp-send).

Usage:
    python eaa_send_message.py --to <agent> --subject <s> --message <m>
    python eaa_send_message.py --to <agent> -s <subject> -m <msg> --priority high
    python eaa_send_message.py --to <agent> -s <subject> --type request -m <msg>

Environment:
    SESSION_NAME - Sender agent name (auto-detected from tmux if not set)
"""

import argparse
import json
import os
import subprocess
import sys


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
) -> dict[str, str]:
    """Send message via AMP CLI (amp-send).

    Args:
        to: Recipient agent name (full session name like 'libs-svg-svgbbox')
        subject: Message subject
        message: Message content
        priority: Message priority (normal, high, urgent)
        msg_type: Message type (notification, request, response, status)

    Returns:
        Dict with 'status' key on success, or 'error' key on failure.
    """
    try:
        result = subprocess.run(
            [
                "amp-send",
                to,
                subject,
                message,
                "--priority",
                priority,
                "--type",
                msg_type,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return {"status": "sent"}
        return {
            "error": result.stderr.strip()
            or f"amp-send exited with code {result.returncode}"
        }
    except FileNotFoundError:
        return {"error": "amp-send not found on PATH"}
    except subprocess.TimeoutExpired:
        return {"error": "amp-send timed out after 30 seconds"}
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Send message via AMP CLI")
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
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            print("Message sent successfully")

    sys.exit(0 if "error" not in result else 1)


if __name__ == "__main__":
    main()
