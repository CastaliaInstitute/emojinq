#!/usr/bin/env python3
"""Turn field-study centerlines into tapered vector brush ribbons.

The authored studies use open contour paths for anatomy.  A constant-width
SVG stroke makes those contours look like stick diagrams, especially on legs,
tentacles, and wings.  This shared pass samples each centerline and outlines
it with the same pressure-shaped ribbon geometry used by the rest of Emojinq.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from svgpathtools import parse_path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def subpaths(d: str) -> list[str]:
    starts = [match.start() for match in re.finditer(r"(?=M\s)", d)]
    return [d[start:starts[index + 1] if index + 1 < len(starts) else None].strip() for index, start in enumerate(starts)]


def ribbon_for(d: str, width: float, seed: str) -> str | None:
    try:
        path = parse_path(d)
        length = path.length()
    except (ValueError, ZeroDivisionError):
        return None
    if length <= 0.01:
        return None
    count = max(3, min(48, int(length / 1.35) + 1))
    points = []
    for index in range(count):
        t = index / (count - 1)
        point = path.point(t)
        # A loaded nib bears down and lifts unevenly; the deterministic
        # pressure rhythm is deliberately gentle so anatomy stays legible.
        pressure = 0.78 + 0.20 * (0.5 + 0.5 * __import__("math").sin(t * 5.1 + len(seed)))
        points.append(BrushPoint(point.real, point.imag, pressure))
    return stroke_path(
        points,
        width=max(1.0, width * 1.12),
        seed=f"field-line-{seed}",
        wobble=.28,
        taper_start=.10,
        taper_end=.20,
    )


def convert(path: Path) -> bool:
    tree = ET.parse(path)
    root = tree.getroot()
    if root.get("data-field-lines") == "pressure-ribbon-v1":
        return False
    changed = False
    for parent in root.iter():
        children = list(parent)
        for index, node in enumerate(children):
            if node.tag.rsplit("}", 1)[-1] != "path":
                continue
            classes = set(node.get("class", "").split())
            if not classes.intersection({"ink-stroke", "ink-dry"}):
                continue
            if node.get("stroke", "none") == "none" or not node.get("d"):
                continue
            try:
                source_width = float(node.get("stroke-width", "1"))
            except ValueError:
                source_width = 1.0
            color = node.get("stroke", "#262522")
            replacement = []
            for part_index, part in enumerate(subpaths(node.get("d", ""))):
                ribbon = ribbon_for(part, source_width, f"{path.stem}-{index}-{part_index}")
                if ribbon is None:
                    continue
                dry = "ink-dry" in classes
                replacement.append(ET.Element(f"{{{NS}}}path", {
                    "class": "ink-dry" if dry else "ink-wash",
                    "d": ribbon,
                    "fill": color,
                    "data-ink-brush-pass": "dry-fragment-v1" if dry else "loaded-ribbon-v2",
                    "data-field-line": "pressure-ribbon-v1",
                }))
            if replacement:
                parent.remove(node)
                for offset, new_node in enumerate(replacement):
                    parent.insert(index + offset, new_node)
                changed = True
    if changed:
        root.set("data-field-lines", "pressure-ribbon-v1")
        tree.write(path, encoding="utf-8", xml_declaration=True)
    return changed


def main() -> None:
    changed = 0
    for path in sorted((ROOT / "assets" / "pua").glob("**/*.svg")):
        if path.parent.name in {"references"}:
            continue
        if path.exists() and convert(path):
            changed += 1
    print(f"brushified open field contours in {changed} PUA SVGs")


if __name__ == "__main__":
    main()
