#!/usr/bin/env python3
"""Apply a conservative pressure/wobble pass to simple stroked PUA SVGs.

This changes neither the number of marks nor their semantic geometry. It is
intended for the icon-like PUA families whose silhouettes are already sound
but whose lines are too mechanically uniform.
"""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from collapse_lines import roughen_path

SVG_NS = "http://www.w3.org/2000/svg"
SHAPES = {"path", "line", "polyline", "polygon", "rect", "circle", "ellipse"}
STROKE_RE = re.compile(r"(?:^|;)\s*stroke\s*:\s*([^;]+)")
FILL_RE = re.compile(r"(?:^|;)\s*fill\s*:\s*([^;]+)")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def style_value(element: ET.Element, name: str, pattern: re.Pattern[str]) -> str | None:
    if element.get(name):
        return element.get(name)
    match = pattern.search(element.get("style", ""))
    return match.group(1).strip() if match else None


def pressure(element: ET.Element, index: int) -> float:
    geometry = "|".join(element.get(k, "") for k in ("d", "x1", "x2", "y1", "y2", "points"))
    digest = hashlib.sha1(f"{index}|{geometry}".encode()).hexdigest()
    return 0.84 + (int(digest[:6], 16) / 0xFFFFFF) * 0.38


def brushify(path: Path) -> bool:
    tree = ET.parse(path)
    root = tree.getroot()
    changed = False
    index = 0
    for element in root.iter():
        if local(element.tag) not in SHAPES:
            continue
        if element.get("data-ink-brush-pass") == "v1":
            continue
        stroke = style_value(element, "stroke", STROKE_RE)
        fill = style_value(element, "fill", FILL_RE)
        if not stroke or stroke == "none" or (fill and fill != "none"):
            continue
        try:
            base = float(element.get("stroke-width", "1.5"))
        except ValueError:
            base = 1.5
        element.attrib.pop("style", None)
        element.set("stroke", stroke)
        element.set("stroke-width", f"{max(0.8, min(3.4, base * pressure(element, index))):.2f}")
        element.set("stroke-linecap", "round")
        element.set("stroke-linejoin", "round")
        if element.get("d"):
            element.set("d", roughen_path(element.get("d", ""), index, amount=0.08))
        element.set("data-ink-brush-pass", "v1")
        index += 1
        changed = True
    if changed:
        root.set("data-castalia-style", "sumi-e-ink-wash-v1")
        root.set("data-ink-stroke-system", "tapered-v1")
        tree.write(path, encoding="utf-8", xml_declaration=True)
    return changed


root = Path("assets/pua")
changed = 0
marks = 0
for svg in sorted(root.rglob("*.svg")):
    if svg.parent.name == "references":
        continue
    before = svg.read_text()
    if brushify(svg):
        changed += 1
        after = svg.read_text()
        marks += after.count('data-ink-brush-pass="v1"') - before.count('data-ink-brush-pass="v1"')
print(f"brushified {changed} PUA glyphs ({marks} marks)")
