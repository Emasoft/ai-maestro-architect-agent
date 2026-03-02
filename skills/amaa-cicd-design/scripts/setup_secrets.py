#!/usr/bin/env python3
"""
Setup GitHub repository secrets for CI/CD.
Interactive script to configure required secrets.

Usage:
    python setup-secrets.py [--repo OWNER/REPO] [--env ENVIRONMENT]

Examples:
    python setup-secrets.py                    # Current repo
    python setup-secrets.py --repo myorg/myapp # Specific repo
    python setup-secrets.py --env production   # Environment secrets
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SecretConfig:
    """Configuration for a secret."""

    name: str
    description: str
    required: bool = True
    from_file: bool = False
    env_var: str | None = None


class SecretsManager:
    """Manage GitHub repository secrets."""

    # Platform-specific secrets
    PLATFORM_SECRETS = {
        "apple": [
            SecretConfig(
                "APPLE_CERTIFICATE",
                "Base64-encoded P12 certificate",
                from_file=True,
            ),
            SecretConfig("APPLE_CERTIFICATE_PASSWORD", "Certificate password"),
            SecretConfig("APPLE_ID", "Apple ID email"),
            SecretConfig("NOTARIZATION_PASSWORD", "App-specific password"),
            SecretConfig("APPLE_TEAM_ID", "Team ID from developer.apple.com"),
        ],
        "windows": [
            SecretConfig(
                "WINDOWS_CERTIFICATE",
                "Base64-encoded PFX certificate",
                from_file=True,
            ),
            SecretConfig("WINDOWS_CERTIFICATE_PASSWORD", "Certificate password"),
        ],
        "android": [
            SecretConfig(
                "ANDROID_KEYSTORE",
                "Base64-encoded keystore file",
                from_file=True,
            ),
            SecretConfig("KEYSTORE_PASSWORD", "Keystore password"),
            SecretConfig("KEY_ALIAS", "Key alias name"),
            SecretConfig("KEY_PASSWORD", "Key password"),
        ],
        "npm": [
            SecretConfig("NPM_TOKEN", "npm access token"),
        ],
        "pypi": [
            SecretConfig("PYPI_API_TOKEN", "PyPI API token"),
        ],
        "crates": [
            SecretConfig("CRATES_IO_TOKEN", "crates.io token"),
        ],
        "docker": [
            SecretConfig("DOCKERHUB_USERNAME", "Docker Hub username"),
            SecretConfig("DOCKERHUB_TOKEN", "Docker Hub access token"),
        ],
        "codecov": [
            SecretConfig("CODECOV_TOKEN", "Codecov upload token", required=False),
        ],
    }

    def __init__(self, repo: str | None = None, environment: str | None = None):
        self.repo = repo or self._get_current_repo()
        self.environment = environment

    def _get_current_repo(self) -> str:
        """Get current repository from git remote."""
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("Error: Not in a git repository or gh CLI not configured")
            sys.exit(1)
        return result.stdout.strip()

    def list_secrets(self) -> list[str]:
        """List currently configured secrets."""
        cmd = ["gh", "secret", "list", "-R", self.repo]
        if self.environment:
            cmd.extend(["--env", self.environment])

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return []

        secrets = []
        for line in result.stdout.strip().split("\n"):
            if line:
                secrets.append(line.split()[0])
        return secrets

    def set_secret(self, name: str, value: str) -> bool:
        """Set a secret value."""
        cmd = ["gh", "secret", "set", name, "-R", self.repo, "--body", value]
        if self.environment:
            cmd.extend(["--env", self.environment])

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0

    def set_secret_from_file(self, name: str, path: Path) -> bool:
        """Set a secret from a file (base64 encoded)."""
        import base64

        if not path.exists():
            print(f"File not found: {path}")
            return False

        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        return self.set_secret(name, encoded)

    def interactive_setup(self, platforms: list[str]) -> None:
        """Interactive setup of secrets for specified platforms."""
        print(f"\nSetting up secrets for: {self.repo}")
        if self.environment:
            print(f"Environment: {self.environment}")
        print("=" * 60)

        existing = set(self.list_secrets())
        print(f"\nCurrently configured: {len(existing)} secrets")

        for platform in platforms:
            if platform not in self.PLATFORM_SECRETS:
                print(f"\nUnknown platform: {platform}")
                continue

            secrets = self.PLATFORM_SECRETS[platform]
            print(f"\n--- {platform.upper()} ---")

            for secret in secrets:
                if secret.name in existing:
                    print(f"  {secret.name}: already configured")
                    continue

                if not secret.required:
                    response = input(f"  Configure {secret.name}? [y/N]: ")
                    if response.lower() != "y":
                        continue

                print(f"  {secret.name}: {secret.description}")

                if secret.from_file:
                    path = input("    File path (or skip): ")
                    if path and path.lower() != "skip":
                        if self.set_secret_from_file(secret.name, Path(path)):
                            print("    Set successfully")
                        else:
                            print("    Failed to set")
                else:
                    import getpass

                    value = getpass.getpass("    Value (or skip): ")
                    if value and value.lower() != "skip":
                        if self.set_secret(secret.name, value):
                            print("    Set successfully")
                        else:
                            print("    Failed to set")

        print("\n" + "=" * 60)
        print("Setup complete!")
        print(f"Verify at: https://github.com/{self.repo}/settings/secrets/actions")

    def verify_secrets(self, platforms: list[str]) -> bool:
        """Verify all required secrets are configured."""
        print(f"\nVerifying secrets for: {self.repo}")
        print("=" * 60)

        existing = set(self.list_secrets())
        missing = []

        for platform in platforms:
            if platform not in self.PLATFORM_SECRETS:
                continue

            secrets = self.PLATFORM_SECRETS[platform]
            print(f"\n{platform.upper()}:")

            for secret in secrets:
                if not secret.required:
                    continue

                if secret.name in existing:
                    print(f"  [OK] {secret.name}")
                else:
                    print(f"  [MISSING] {secret.name}")
                    missing.append(secret.name)

        if missing:
            print(f"\nMissing {len(missing)} required secrets!")
            return False

        print("\nAll required secrets configured!")
        return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Setup GitHub repository secrets")
    parser.add_argument("--repo", "-r", help="Repository (owner/repo)")
    parser.add_argument("--env", "-e", help="Environment name")
    parser.add_argument(
        "--verify", "-v", action="store_true", help="Verify secrets only"
    )
    parser.add_argument(
        "--platforms",
        "-p",
        nargs="+",
        default=["apple", "windows", "android", "npm", "pypi", "crates", "codecov"],
        help="Platforms to configure",
    )

    args = parser.parse_args()

    manager = SecretsManager(args.repo, args.env)

    if args.verify:
        return 0 if manager.verify_secrets(args.platforms) else 1

    manager.interactive_setup(args.platforms)
    return 0


if __name__ == "__main__":
    sys.exit(main())
