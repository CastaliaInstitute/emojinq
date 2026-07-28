#!/usr/bin/env python3
"""Fetch the upstream Noto Color Emoji SVG directory for local generation."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

UPSTREAM = "https://github.com/googlefonts/noto-emoji.git"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-dir", type=Path, default=Path(".cache/noto-emoji"))
    parser.add_argument("--ref", default="main")
    args = parser.parse_args()
    repo = args.repo_dir
    if not (repo / ".git").exists():
        repo.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
            "--branch", args.ref, UPSTREAM, str(repo)
        ], check=True)
    subprocess.run(["git", "-C", str(repo), "sparse-checkout", "set", "svg"], check=True)
    subprocess.run(["git", "-C", str(repo), "checkout", args.ref], check=True)
    print(repo / "svg")


if __name__ == "__main__":
    main()
