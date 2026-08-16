#!/usr/bin/env python3
"""Verify authored SVG brush structure and reject raster effects.

OpenMoji inputs under ``assets/source`` are intentionally excluded: they are
upstream reference material, not Emojinq artwork.  Everything else in the
repository is checked as a potential shipped/artifact SVG.  The documented
Color-wash variants may use muted fills only on elements explicitly tagged as
color-wash marks; their overlaid ink remains subject to the normal stroke and
grayscale brush-mass rules.
"""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def intentional_brush_fill(root: ET.Element, element: ET.Element, fill: str) -> bool:
    naturalist_root = (root.get("data-castalia-style"), root.get("data-ink-stroke-system")) == (
        "sumi-e-naturalist-v2", "filled-brush-mass-v2",
    )
    color_composite = root.get("data-color-variant") == "sumi-e-color-wash-v1"
    if not naturalist_root and not color_composite:
        return False
    if not set(element.get("class", "").split()).intersection({"ink-wash", "ink-dry"}):
        return False
    if not fill.startswith("#") or len(fill) not in {4, 7}:
        return False
    value = fill[1:]
    channels = [int(char * 2, 16) for char in value] if len(value) == 3 else [int(value[index:index + 2], 16) for index in (0, 2, 4)]
    return max(channels) - min(channels) <= 16


def intentional_color_wash(root: ET.Element, element: ET.Element, fill: str) -> bool:
    if root.get("data-color-variant") not in {
        "sumi-e-color-wash-v1",
        "sumi-e-familiar-referent-color-v1",
    }:
        return False
    if "ink-color-wash" not in element.get("class", "").split():
        return False
    return fill.startswith("#") and len(fill) in {4, 7}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets"))
    parser.add_argument("--exclude", action="append", default=["source"])
    args = parser.parse_args()

    files = [
        path for path in sorted(args.root.rglob("*.svg"))
        if not any(part in args.exclude for part in path.relative_to(args.root).parts)
    ]
    failures: list[str] = []
    for path in files:
        text = path.read_text(errors="replace")
        if "<image" in text or "<filter" in text or "<foreignObject" in text:
            failures.append(f"{path}: embedded raster/filter object")
            continue
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            failures.append(f"{path}: malformed SVG ({exc})")
            continue
        for element in root.iter():
            fill = element.get("fill", "").strip().lower()
            if (
                fill
                and fill not in {"none", "transparent"}
                and not intentional_brush_fill(root, element, fill)
                and not intentional_color_wash(root, element, fill)
            ):
                failures.append(f"{path}: {local(element.tag)} has fill={fill!r}")
                break
            if local(element.tag) in SHAPES and element.get("class") == "ink-stroke":
                if element.get("pathLength") != "1":
                    failures.append(f"{path}: ink-stroke missing pathLength=1")
                    break
    if failures:
        raise SystemExit("\n".join(failures[:40]) + ("\n..." if len(failures) > 40 else ""))
    print(f"stroke corpus checked: {len(files)} authored SVGs; source inputs excluded")


if __name__ == "__main__":
    main()
