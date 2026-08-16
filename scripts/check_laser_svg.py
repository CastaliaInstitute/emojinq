#!/usr/bin/env python3
"""Validate grayscale SVG exports for bamboo laser depth production."""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def svg_paths(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() == ".svg" else []
    return sorted(root.rglob("*.svg"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("build/laser-pua"))
    args = parser.parse_args()
    failures = []
    count = 0
    for svg in svg_paths(args.root):
        count += 1
        root = ET.parse(svg).getroot()
        if root.get("data-castalia-output") != "laser-grayscale-v1":
            failures.append(f"{svg}: missing laser output marker")
        if root.get("data-laser-depth-encoding") != "neutral-luminance-linear-v1":
            failures.append(f"{svg}: missing calibrated grayscale depth marker")
        if root.get("data-laser-black") != "deepest" or root.get("data-laser-white") != "lightest":
            failures.append(f"{svg}: missing black/deepest or white/lightest convention")
        tags = {local(node.tag) for node in root.iter()}
        if tags & {"image", "filter", "mask", "clipPath", "foreignObject"}:
            failures.append(f"{svg}: unsupported raster/effect element")
        text = svg.read_text()
        if re.search(r"opacity|url\(", text):
            failures.append(f"{svg}: opacity or filter paint remains")
        for node in root.iter():
            if any("opacity" in key.lower() for key in node.attrib):
                failures.append(f"{svg}: opacity attribute remains")
            for paint in (node.get("fill"), node.get("stroke")):
                if paint and paint.lower() != "none":
                    match = re.fullmatch(r"#([0-9a-fA-F]{6})", paint)
                    if not match or len(set(match.group(1)[index:index + 2].lower() for index in (0, 2, 4))) != 1:
                        failures.append(f"{svg}: non-grayscale paint remains: {paint}")
            if local(node.tag) == "path" and node.get("stroke-width"):
                try:
                    if float(node.get("stroke-width")) < 1.0:
                        failures.append(f"{svg}: stroke below 1.0 SVG unit")
                except ValueError:
                    failures.append(f"{svg}: invalid stroke width")
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    print(f"laser SVG checked: {count} grayscale scalable glyphs")


if __name__ == "__main__":
    main()
