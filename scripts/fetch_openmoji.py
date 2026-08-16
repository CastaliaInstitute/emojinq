#!/usr/bin/env python3
"""Fetch the OpenMoji Black and Color SVG directories for local generation."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

UPSTREAM = "https://github.com/hfg-gmuend/openmoji.git"
PINNED_REF = "d05930b34516a0a3ff00aad0288ee05364cebd8b"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-dir", type=Path, default=Path(".cache/openmoji"))
    parser.add_argument(
        "--ref",
        default=PINNED_REF,
        help="OpenMoji git ref; defaults to the release-reviewed commit",
    )
    args = parser.parse_args()
    repo = args.repo_dir
    if not (repo / ".git").exists():
        repo.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "git", "clone", "--filter=blob:none", "--sparse", "--no-checkout",
            UPSTREAM, str(repo)
        ], check=True)
    subprocess.run(["git", "-C", str(repo), "sparse-checkout", "set", "black", "color"], check=True)
    subprocess.run(["git", "-C", str(repo), "fetch", "--depth", "1", "origin", args.ref], check=True)
    subprocess.run(["git", "-C", str(repo), "checkout", "--detach", "FETCH_HEAD"], check=True)
    resolved = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if args.ref == PINNED_REF and resolved != PINNED_REF:
        raise SystemExit(f"OpenMoji pin mismatch: expected {PINNED_REF}, found {resolved}")
    print(f"OpenMoji source: {resolved}")
    print(repo / "black" / "svg")
    print(repo / "color" / "svg")


if __name__ == "__main__":
    main()
