#!/usr/bin/env python3
"""
List available GitHub Actions runners and their specifications.

Usage:
    python list-runners.py [--self-hosted] [--repo OWNER/REPO]

Examples:
    python list-runners.py              # List GitHub-hosted runners
    python list-runners.py --self-hosted # List self-hosted runners
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from typing import Any, TypedDict


class RunnerSpecs(TypedDict):
    """Type definition for runner specifications."""

    os: str
    arch: str
    vcpus: int
    ram_gb: int
    storage_gb: int
    minute_multiplier: int


# GitHub-hosted runner specifications
GITHUB_RUNNERS: dict[str, RunnerSpecs] = {
    "ubuntu-latest": {
        "os": "Ubuntu 22.04",
        "arch": "x86_64",
        "vcpus": 4,
        "ram_gb": 16,
        "storage_gb": 14,
        "minute_multiplier": 1,
    },
    "ubuntu-24.04": {
        "os": "Ubuntu 24.04",
        "arch": "x86_64",
        "vcpus": 4,
        "ram_gb": 16,
        "storage_gb": 14,
        "minute_multiplier": 1,
    },
    "ubuntu-24.04-arm": {
        "os": "Ubuntu 24.04",
        "arch": "ARM64",
        "vcpus": 4,
        "ram_gb": 16,
        "storage_gb": 14,
        "minute_multiplier": 1,
    },
    "macos-14": {
        "os": "macOS 14 Sonoma",
        "arch": "ARM64 (M1)",
        "vcpus": 3,
        "ram_gb": 14,
        "storage_gb": 14,
        "minute_multiplier": 10,
    },
    "macos-13": {
        "os": "macOS 13 Ventura",
        "arch": "x86_64",
        "vcpus": 4,
        "ram_gb": 14,
        "storage_gb": 14,
        "minute_multiplier": 10,
    },
    "windows-latest": {
        "os": "Windows Server 2022",
        "arch": "x86_64",
        "vcpus": 4,
        "ram_gb": 16,
        "storage_gb": 14,
        "minute_multiplier": 2,
    },
}

# Free tier limits
FREE_TIER = {
    "free": {"linux": 2000, "macos": 200, "windows": 2000},
    "pro": {"linux": 3000, "macos": 300, "windows": 3000},
    "team": {"linux": 3000, "macos": 300, "windows": 3000},
}


def print_github_runners() -> None:
    """Print GitHub-hosted runner specifications."""
    print("\nGitHub-Hosted Runners")
    print("=" * 80)

    header = (
        f"{'Runner':<20} {'OS':<20} {'Arch':<12} {'CPUs':<6} {'RAM':<8} {'Cost':<6}"
    )
    print(header)
    print("-" * 80)

    for name, specs in GITHUB_RUNNERS.items():
        multiplier: int = specs["minute_multiplier"]
        cost = f"{multiplier}x" if multiplier > 1 else "1x"

        print(
            f"{name:<20} {specs['os']:<20} {specs['arch']:<12} "
            f"{specs['vcpus']:<6} {specs['ram_gb']}GB{'':<4} {cost:<6}"
        )

    print("\nFree Tier Monthly Minutes:")
    print("-" * 40)
    for tier, limits in FREE_TIER.items():
        print(
            f"  {tier.capitalize():8} Linux: {limits['linux']:4} | macOS: {limits['macos']:3} | Windows: {limits['windows']:4}"
        )

    print("\nNote: macOS minutes cost 10x Linux, Windows cost 2x Linux")


def get_self_hosted_runners(repo: str) -> list[dict[str, Any]]:
    """Get self-hosted runners for a repository."""
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/actions/runners"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return []

    import json

    data: dict[str, Any] = json.loads(result.stdout)
    runners: list[dict[str, Any]] = data.get("runners", [])
    return runners


def print_self_hosted_runners(repo: str) -> None:
    """Print self-hosted runners for a repository."""
    runners = get_self_hosted_runners(repo)

    print(f"\nSelf-Hosted Runners for {repo}")
    print("=" * 80)

    if not runners:
        print("No self-hosted runners configured")
        print(f"\nAdd runners at: https://github.com/{repo}/settings/actions/runners")
        return

    header = f"{'Name':<30} {'OS':<15} {'Status':<10} {'Labels':<25}"
    print(header)
    print("-" * 80)

    for runner in runners:
        name = runner.get("name", "unknown")[:30]
        os = runner.get("os", "unknown")
        status = runner.get("status", "unknown")
        labels = ", ".join(label["name"] for label in runner.get("labels", []))[:25]

        print(f"{name:<30} {os:<15} {status:<10} {labels:<25}")


def recommend_runners(platforms: list[str]) -> None:
    """Recommend runners for target platforms."""
    print("\nRecommended Runner Matrix")
    print("=" * 60)

    recommendations: dict[str, str] = {
        "linux-x64": "ubuntu-latest",
        "linux-arm64": "ubuntu-24.04-arm",
        "macos-arm64": "macos-14",
        "macos-x64": "macos-13",
        "windows-x64": "windows-latest",
    }

    for platform in platforms:
        if platform in recommendations:
            runner = recommendations[platform]
            specs: RunnerSpecs | None = GITHUB_RUNNERS.get(runner)
            print(f"\n  {platform}:")
            print(f"    Runner: {runner}")
            if specs is not None:
                print(f"    OS: {specs['os']}")
                print(f"    Cost: {specs['minute_multiplier']}x")
            else:
                print("    OS: unknown")
                print("    Cost: 1x")

    print("\nWorkflow snippet:")
    print("-" * 40)
    print("""
jobs:
  build:
    strategy:
      matrix:
        include:""")
    for platform in platforms:
        if platform in recommendations:
            print(f"          - os: {recommendations[platform]}")
            print(f"            target: {platform}")


def main() -> int:
    parser = argparse.ArgumentParser(description="List GitHub Actions runners")
    parser.add_argument(
        "--self-hosted",
        "-s",
        action="store_true",
        help="List self-hosted runners",
    )
    parser.add_argument("--repo", "-r", help="Repository (owner/repo)")
    parser.add_argument(
        "--recommend",
        nargs="+",
        choices=["linux-x64", "linux-arm64", "macos-arm64", "macos-x64", "windows-x64"],
        help="Recommend runners for platforms",
    )

    args = parser.parse_args()

    if args.recommend:
        recommend_runners(args.recommend)
        return 0

    print_github_runners()

    if args.self_hosted:
        repo = args.repo
        if not repo:
            result = subprocess.run(
                [
                    "gh",
                    "repo",
                    "view",
                    "--json",
                    "nameWithOwner",
                    "-q",
                    ".nameWithOwner",
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                repo = result.stdout.strip()

        if repo:
            print_self_hosted_runners(repo)

    return 0


if __name__ == "__main__":
    sys.exit(main())
