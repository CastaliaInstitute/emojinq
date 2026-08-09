#!/usr/bin/env python3
"""Verify that PUA artwork remains portable, scalable vector SVG."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    args = parser.parse_args()
    failures = []
    count = 0
    for svg in sorted(args.root.rglob("*.svg")):
        if svg.parent.name == "references":
            continue
        count += 1
        root = ET.parse(svg).getroot()
        if root.get("viewBox") != "0 0 72 72":
            failures.append(f"{svg}: expected 0 0 72 72 viewBox")
        tags = {element.tag.rsplit("}", 1)[-1] for element in root.iter()}
        if "path" not in tags:
            failures.append(f"{svg}: no vector paths")
        for forbidden in ("image", "filter", "foreignObject"):
            if forbidden in tags:
                failures.append(f"{svg}: forbidden {forbidden} element")
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    print(f"PUA vector checked: {count} scalable SVGs, no embedded raster or filters")


if __name__ == "__main__":
    main()
