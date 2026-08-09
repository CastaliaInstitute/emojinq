#!/usr/bin/env python3
"""Check that every PUA SVG has a readable raster footprint at glyph size."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--minimum-area", type=int, default=120)
    args = parser.parse_args()

    failures = []
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
            image = Image.open(tmp.name).convert("RGBA")
        points = [(x, y) for y in range(args.size) for x in range(args.size) if image.getpixel((x, y))[3] >= 32]
        if not points:
            failures.append(f"{svg}: no visible ink")
            continue
        area = len(points)
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        width = max(xs) - min(xs) + 1
        height = max(ys) - min(ys) + 1
        if area < args.minimum_area or width < 5 or height < 5:
            failures.append(f"{svg}: area={area}, bbox={width}x{height}")
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    print(f"PUA legibility checked: {count} glyphs at {args.size}px")


if __name__ == "__main__":
    main()
