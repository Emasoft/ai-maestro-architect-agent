#!/usr/bin/env python3
"""
Bun Build Script Template (Python version)

Usage:
    python3 bun-build-template.py
    python3 bun-build-template.py --watch
    python3 bun-build-template.py --dev
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

DIST_DIR = Path("./dist")
SRC_DIR = Path("./src")
ENTRY_POINT = SRC_DIR / "index.js"
BUNDLE_NAME = "bundle.min.js"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bun build wrapper script")
    parser.add_argument("--watch", action="store_true", help="Watch for file changes and rebuild")
    parser.add_argument("--dev", action="store_true", help="Build in development mode (no minify, inline sourcemap)")
    return parser.parse_args()


def build(is_dev: bool) -> bool:
    """Run bun build and report bundle sizes and build time."""
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    mode = "development" if is_dev else "production"
    print(f"Building {mode} bundles...\n")

    start_time = time.monotonic()

    cmd = [
        "bun", "build",
        str(ENTRY_POINT),
        "--outdir", str(DIST_DIR),
        "--outfile", BUNDLE_NAME,
        "--target", "browser",
        "--format", "esm",
    ]

    if is_dev:
        cmd.append("--sourcemap=inline")
    else:
        cmd.append("--minify")

    env_define = f'process.env.NODE_ENV={"development" if is_dev else "production"!r}'
    cmd += ["--define", env_define]

    result = subprocess.run(cmd, capture_output=True, text=True)

    elapsed_ms = int((time.monotonic() - start_time) * 1000)

    if result.returncode != 0:
        print("Build failed:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False

    # Report bundle sizes
    bundle_path = DIST_DIR / BUNDLE_NAME
    print("Bundle sizes:")
    if bundle_path.exists():
        size_kb = bundle_path.stat().st_size / 1024
        print(f"  {BUNDLE_NAME:<25} {size_kb:.1f} KB")

    print(f"\nBuild completed in {elapsed_ms}ms")
    return True


def watch(is_dev: bool) -> None:
    """Watch ./src for .js/.ts changes and rebuild on each change."""
    print("\nWatching for changes...")
    try:
        # Use the watchdog library if available, otherwise fall back to polling
        _watch_with_watchdog(is_dev)
    except ImportError:
        _watch_with_polling(is_dev)


def _watch_with_watchdog(is_dev: bool) -> None:
    from watchdog.events import (  # type: ignore[import]
        FileCreatedEvent,
        FileModifiedEvent,
        FileSystemEventHandler,
    )
    from watchdog.observers import Observer  # type: ignore[import]

    class RebuildHandler(FileSystemEventHandler):
        def on_modified(self, event: FileModifiedEvent) -> None:  # type: ignore[override]
            self._handle(event.src_path)

        def on_created(self, event: FileCreatedEvent) -> None:  # type: ignore[override]
            self._handle(event.src_path)

        def _handle(self, src_path: str) -> None:
            if src_path.endswith((".js", ".ts")):
                print(f"\nFile changed: {src_path}")
                build(is_dev)

    observer = Observer()
    observer.schedule(RebuildHandler(), str(SRC_DIR), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def _watch_with_polling(is_dev: bool) -> None:
    """Simple polling fallback when watchdog is not installed."""
    import hashlib

    def file_hash(path: Path) -> str:
        return hashlib.md5(path.read_bytes()).hexdigest()

    known: dict[str, str] = {}

    def snapshot() -> dict[str, str]:
        return {str(p): file_hash(p) for p in SRC_DIR.rglob("*") if p.suffix in (".js", ".ts") and p.is_file()}

    known = snapshot()
    try:
        while True:
            time.sleep(1)
            current = snapshot()
            for path, digest in current.items():
                if known.get(path) != digest:
                    print(f"\nFile changed: {path}")
                    build(is_dev)
            known = current
    except KeyboardInterrupt:
        pass


def main() -> None:
    args = parse_args()

    ok = build(args.dev)
    if not ok:
        sys.exit(1)

    if args.watch:
        watch(args.dev)


if __name__ == "__main__":
    main()
