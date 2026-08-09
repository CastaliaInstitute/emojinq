#!/usr/bin/env python3
"""Reject exact raster duplicates across distinct PUA SVG glyphs."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    parser.add_argument("--size", type=int, default=96)
    args = parser.parse_args()
    hashes: dict[str, list[str]] = defaultdict(list)
    count = 0
    for svg in sorted(args.root.rglob("*.svg")):
        if svg.parent.name == "references":
            continue
        count += 1
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            subprocess.run(
                ["rsvg-convert", "-w", str(args.size), "-h", str(args.size), "-o", tmp.name, str(svg)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            pixels = Image.open(tmp.name).convert("L").tobytes()
        hashes[hashlib.sha256(pixels).hexdigest()].append(svg.as_posix())
    duplicates = [paths for paths in hashes.values() if len(paths) > 1]
    if duplicates:
        lines = ["\n".join(paths) for paths in duplicates[:10]]
        raise SystemExit("exact PUA raster duplicates:\n" + "\n\n".join(lines))
    print(f"PUA duplicate check: {count} distinct raster silhouettes at {args.size}px")


if __name__ == "__main__":
    main()
