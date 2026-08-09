#!/usr/bin/env python3
"""Validate monochrome SVG exports for bamboo laser production."""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("build/laser-pua"))
    args = parser.parse_args()
    failures = []
    count = 0
    for svg in sorted(args.root.rglob("*.svg")):
        count += 1
        root = ET.parse(svg).getroot()
        if root.get("data-castalia-output") != "laser-monochrome-v1":
            failures.append(f"{svg}: missing laser output marker")
        tags = {local(node.tag) for node in root.iter()}
        if tags & {"image", "filter", "mask", "clipPath", "foreignObject"}:
            failures.append(f"{svg}: unsupported raster/effect element")
        text = svg.read_text()
        if re.search(r"opacity|url\(|#(?!000000\b)[0-9a-fA-F]{6}\b", text):
            failures.append(f"{svg}: non-binary paint remains")
        for node in root.iter():
            if local(node.tag) == "path" and node.get("stroke-width"):
                try:
                    if float(node.get("stroke-width")) < 1.0:
                        failures.append(f"{svg}: stroke below 1.0 SVG unit")
                except ValueError:
                    failures.append(f"{svg}: invalid stroke width")
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    print(f"laser SVG checked: {count} monochrome scalable glyphs")


if __name__ == "__main__":
    main()
