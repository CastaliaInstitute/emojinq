#!/usr/bin/env python3
"""Convert simple SVG stroke paths into filled, tapered brush ribbons.

This is intentionally conservative: it only rewrites stroke-only paths. Fill
art and already-authored wash masses are left intact for human review.
"""
from __future__ import annotations

import argparse
import hashlib
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from svgpathtools import parse_path

from sumi_brush import BrushPoint, stroke_path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def style_value(element: ET.Element, name: str) -> str | None:
    value = element.get(name)
    if value:
        return value.strip()
    style = element.get("style", "")
    match = re.search(rf"(?:^|;)\s*{name}\s*:\s*([^;]+)", style)
    return match.group(1).strip() if match else None


def sample(d: str, seed: str) -> list[BrushPoint]:
    path = parse_path(d)
    out: list[BrushPoint] = []
    point_index = 0
    for segment in path:
        length = max(1.0, float(segment.length(error=1e-3)))
        count = max(4, min(36, math.ceil(length / 1.8)))
        for index in range(count):
            point = segment.point(index / (count - 1))
            digest = hashlib.sha1(f"{seed}:{point_index}".encode()).hexdigest()
            noise = int(digest[:8], 16) / 0xFFFFFFFF
            progress = point_index / max(1, sum(max(4, min(36, math.ceil(max(1.0, float(item.length(error=1e-3))) / 1.8))) for item in path) - 1)
            pressure = 0.70 + noise * 0.46 + 0.08 * math.sin(math.pi * progress)
            out.append(BrushPoint(float(point.real), float(point.imag), pressure))
            point_index += 1
    if path:
        point = path[-1].end
        out.append(BrushPoint(float(point.real), float(point.imag), 0.58))
    return out


def ink_tone(width: float) -> str:
    """Use neutral ink values as a material/depth cue, never transparency."""
    if width >= 2.15:
        return "#262522"
    if width >= 1.45:
        return "#4f4d47"
    return "#77746a"


def convert(path: Path) -> int:
    tree = ET.parse(path)
    root = tree.getroot()
    converted = 0
    for index, element in enumerate(root.iter()):
        if local(element.tag) != "path" or not element.get("d"):
            continue
        if element.get("data-ink-ribbon-pass") in {"v1", "v2"}:
            continue
        stroke = style_value(element, "stroke")
        fill = style_value(element, "fill")
        if not stroke or stroke == "none" or (fill and fill != "none"):
            continue
        try:
            base_width = float(element.get("stroke-width", "1.5"))
        except ValueError:
            base_width = 1.5
        points = sample(element.get("d", ""), f"{path}:{index}")
        if len(points) < 2:
            continue
        element.set("d", stroke_path(points, width=max(.45, base_width), seed=f"{path}:{index}", wobble=.13))
        element.set("fill", ink_tone(base_width * max(point.pressure for point in points)))
        element.set("class", "ink-wash")
        element.set("data-ink-ribbon-pass", "v2")
        for attr in ("stroke", "stroke-width", "stroke-linecap", "stroke-linejoin", "pathLength"):
            element.attrib.pop(attr, None)
        converted += 1
    if converted:
        root.set("data-castalia-style", "sumi-e-brush-ribbon-v1")
        root.set("data-ink-stroke-system", "filled-ribbon-v1")
        tree.write(path, encoding="utf-8", xml_declaration=True)
    return converted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path)
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    args = parser.parse_args()
    files = [args.file] if args.file else sorted(args.root.rglob("*.svg"))
    total = 0
    changed = 0
    for path in files:
        if path and path.exists() and path.parent.name != "references":
            count = convert(path)
            if count:
                changed += 1
                total += count
    print(f"ribbonized {changed} SVGs ({total} stroke paths)")


if __name__ == "__main__":
    main()
