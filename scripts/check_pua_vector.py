#!/usr/bin/env python3
"""Verify that PUA artwork remains portable, scalable vector SVG."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}


def intentional_brush_fill(root: ET.Element, element: ET.Element, fill: str) -> bool:
    style = (root.get("data-castalia-style"), root.get("data-ink-stroke-system"))
    naturalist_fill = style == ("sumi-e-naturalist-v2", "filled-brush-mass-v2") and bool(
        set(element.get("class", "").split()).intersection({"ink-wash", "ink-dry"})
    )
    tapered_loaded_mass = style == ("sumi-e-ink-wash-v1", "tapered-v1") and (
        element.get("data-ink-brush-pass") == "loaded-mass-v1"
    )
    if not (naturalist_fill or tapered_loaded_mass):
        return False
    if not fill.startswith("#") or len(fill) not in {4, 7}:
        return False
    value = fill[1:]
    channels = [int(char * 2, 16) for char in value] if len(value) == 3 else [int(value[index:index + 2], 16) for index in (0, 2, 4)]
    return max(channels) - min(channels) <= 16


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
        if not tags.intersection(SHAPES):
            failures.append(f"{svg}: no vector geometry")
        for forbidden in ("image", "filter", "foreignObject"):
            if forbidden in tags:
                failures.append(f"{svg}: forbidden {forbidden} element")
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] in SHAPES:
                fill = element.get("fill", "").strip().lower()
                if fill and fill not in {"none", "transparent"} and not intentional_brush_fill(root, element, fill):
                    failures.append(f"{svg}: filled geometry {element.tag.rsplit('}', 1)[-1]}")
                    break
                style = element.get("style", "").lower().replace(" ", "")
                if "fill:" in style and "fill:none" not in style and "fill:transparent" not in style:
                    failures.append(f"{svg}: filled geometry in style")
                    break
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    print(f"PUA vector checked: {count} scalable SVGs, no embedded raster or filters")


if __name__ == "__main__":
    main()
