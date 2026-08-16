#!/usr/bin/env python3
"""Turn simple botanical/farm wash masses into outlined sumi-e studies.

The source drawings in these families already have the right semantic
silhouettes and brush-built secondary marks, but their primary masses were
rendering as solid pictograms.  This pass keeps the geometry, changes the
mass to a quiet gray wash, and adds one rounded contour per mass.  It is a
shared treatment for a family, not per-glyph annotation.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from collapse_lines import roughen_path


SHAPES = {"path", "ellipse", "circle", "rect", "polygon"}
WASH_COLORS = {"#262522", "#3c3b36", "#4a4943", "#4a4943ff"}
MID_COLORS = {"#77746a", "#77746aff"}
NUMBER_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def inline_fill(element: ET.Element) -> str | None:
    if element.get("fill"):
        return element.get("fill")
    for declaration in element.get("style", "").split(";"):
        key, _, value = declaration.partition(":")
        if key.strip() == "fill":
            return value.strip()
    return None


def style_mass(element: ET.Element, index: int) -> bool:
    if local(element.tag) not in SHAPES:
        return False
    if "ink-wash" not in element.get("class", "").split():
        return False
    if element.get("data-ink-contour") == "naturalist-v1":
        return False
    fill = inline_fill(element)
    if fill in {None, "none", "transparent"}:
        return False
    if fill.lower() in WASH_COLORS:
        element.set("fill", "#bcb9af")
    elif fill.lower() in MID_COLORS:
        element.set("fill", "#d0cdc3")
    else:
        return False
    element.attrib.pop("style", None)
    element.set("stroke", "#262522")
    element.set("stroke-width", "1.02" if local(element.tag) == "path" else "0.88")
    element.set("stroke-linecap", "round")
    element.set("stroke-linejoin", "round")
    element.set("data-ink-contour", "naturalist-v1")
    return True


def small_mark(element: ET.Element) -> bool:
    """Keep tiny eyes, seeds, and berry dots as solid brush marks."""
    tag = local(element.tag)
    if tag in {"ellipse", "circle"}:
        try:
            return max(float(element.get("rx", element.get("r", 0))), float(element.get("ry", element.get("r", 0)))) <= 2.8
        except ValueError:
            return False
    if tag == "path":
        values = [float(value) for value in NUMBER_RE.findall(element.get("d", ""))]
        if len(values) < 4:
            return False
        xs, ys = values[0::2], values[1::2]
        return max(xs) - min(xs) <= 5 and max(ys) - min(ys) <= 5
    return False


def remove_wash(path: Path) -> bool:
    tree = ET.parse(path)
    root = tree.getroot()
    changed = False
    for index, element in enumerate(root.iter()):
        if element.get("data-ink-contour") not in {"naturalist-v1", "naturalist-line-v1", "naturalist-line-v2"}:
            continue
        if small_mark(element):
            element.set("fill", "#262522")
            element.attrib.pop("stroke", None)
            element.attrib.pop("stroke-width", None)
            element.attrib.pop("stroke-linecap", None)
            element.attrib.pop("stroke-linejoin", None)
        else:
            element.set("fill", "none")
            if element.get("d"):
                element.set("d", roughen_path(element.get("d", ""), index, amount=0.055))
        element.set("data-ink-contour", "naturalist-line-v3")
        changed = True
    already_line = any(element.get("data-ink-contour") == "naturalist-line-v3" for element in root.iter())
    if changed or already_line:
        root.set("data-castalia-style", "sumi-e-ink-wash-v1")
        root.set("data-ink-stroke-system", "tapered-v1")
        tree.write(path, encoding="utf-8", xml_declaration=True)
    return changed or already_line


def process(path: Path) -> bool:
    tree = ET.parse(path)
    root = tree.getroot()
    changed = False
    for index, element in enumerate(root.iter()):
        changed = style_mass(element, index) or changed
    if not changed:
        return False
    root.set("data-castalia-style", "sumi-e-naturalist-v2")
    root.set("data-ink-stroke-system", "filled-brush-mass-v2")
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    parser.add_argument("--category", action="append", default=["farm", "flora", "herbs"])
    parser.add_argument("--remove-wash", action="store_true")
    args = parser.parse_args()
    changed = 0
    masses = 0
    for category in args.category:
        for path in sorted((args.root / category).glob("*.svg")):
            before = path.read_text()
            did_change = remove_wash(path) if args.remove_wash else process(path)
            if did_change:
                changed += 1
                masses += path.read_text().count('data-ink-contour="naturalist-v1"') - before.count('data-ink-contour="naturalist-v1"')
    print(f"outlined {masses} wash masses across {changed} naturalist glyphs")


if __name__ == "__main__":
    main()
