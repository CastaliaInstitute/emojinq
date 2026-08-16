#!/usr/bin/env python3
"""Strengthen the complete standard Food & Drink category at toddler size.

The standard corpus begins with useful OpenMoji line anatomy, but its tapered
contours are intentionally delicate.  At the 32 px recognition gate those
sub-unit strokes fade before details such as stems, wrappers, handles, and
utensil tines can identify the food.  This pass preserves every source contour
while giving it a loaded/mid/dry sumi-e hierarchy that survives small display.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "gray-all"
MANIFEST = ASSETS / "manifest.json"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# Extra cues are reserved for silhouettes that still read as another familiar
# object after the category-wide pressure pass.  Coordinates use OpenMoji's
# 72-unit card and deliberately describe parts, not decoration.
CUES: dict[str, list[tuple[str, str, float]]] = {
    "1F34B-200D-1F7E9.svg": [
        ("M 22,48 C 31,48 43,43 51,33", "#302e2a", 2.10),
        ("M 31,45 L 27,37 M 40,41 L 35,31 M 47,36 L 42,27", "#66635b", 1.55),
        ("M 35,37 C 37,34 39,35 39,38 C 37,39 36,39 35,37", "#262421", 1.45),
    ],
    "1F357.svg": [
        ("M 31,51 C 27,53 27,57 30,59 C 30,63 35,64 37,60 C 41,59 41,54 37,52", "#302e2a", 2.05),
        ("M 33,48 L 35,55", "#66635b", 1.55),
    ],
    "1F358.svg": [
        ("M 24,25 L 27,27 M 35,21 L 37,24 M 45,26 L 42,28 M 28,35 L 31,36 M 44,36 L 47,34", "#66635b", 1.45),
        ("M 27,49 H 45 V 60 H 27 Z", "#302e2a", 1.95),
    ],
    "1F359.svg": [
        ("M 29,29 L 32,27 M 36,22 L 39,24 M 43,31 L 46,29", "#66635b", 1.45),
        ("M 29,48 H 44 V 61 H 29 Z", "#302e2a", 2.05),
    ],
    "1F35A.svg": [
        ("M 25,29 C 29,22 43,21 48,29", "#302e2a", 2.10),
        ("M 29,28 L 32,25 M 36,27 L 38,23 M 42,28 L 45,25", "#66635b", 1.45),
    ],
    "1F364.svg": [
        ("M 28,17 L 23,10 M 29,17 L 31,9 M 30,18 L 38,13", "#302e2a", 1.90),
        ("M 27,26 C 32,29 35,31 39,35 M 25,34 C 30,36 34,39 37,43 M 24,43 C 29,44 32,47 34,50", "#66635b", 1.45),
    ],
    "1F365.svg": [
        ("M 28,37 C 28,28 43,26 46,34 C 49,44 34,49 27,42 C 23,38 25,32 30,30", "#302e2a", 2.00),
        ("M 33,36 C 35,32 41,33 41,37 C 40,41 34,41 33,38", "#66635b", 1.45),
    ],
    "1F36E.svg": [
        ("M 24,49 C 30,54 43,55 49,49", "#302e2a", 2.00),
        ("M 27,27 C 32,24 42,24 47,27 M 29,31 L 46,31", "#66635b", 1.50),
    ],
    "1F375.svg": [
        ("M 29,20 C 25,16 31,13 28,9 M 38,20 C 34,16 41,13 38,9 M 47,20 C 43,16 50,13 47,9", "#66635b", 1.55),
    ],
    "1F379.svg": [
        ("M 22,21 C 29,12 43,11 51,20 Z M 36,18 L 31,33", "#302e2a", 1.85),
    ],
}

REPLACEMENTS: dict[str, list[tuple[str, str, float]]] = {
    "1F330.svg": [
        ("M 36,10 C 31,19 21,27 19,40 C 17,52 26,61 36,62 C 47,60 55,52 54,40 C 53,28 43,19 36,10 Z", "#262421", 2.45),
        ("M 22,44 C 29,50 43,52 51,44", "#302e2a", 2.05),
        ("M 28,48 L 25,53 M 36,50 V 56 M 44,48 L 47,53", "#66635b", 1.45),
    ],
    "1F35E.svg": [
        ("M 15,56 V 46 C 15,32 24,23 35,22 C 39,18 46,20 49,25 C 56,29 59,38 57,48 L 55,57 H 18 Z", "#262421", 2.45),
        ("M 16,47 C 27,43 45,43 57,48", "#302e2a", 1.95),
        ("M 27,30 C 29,34 29,38 27,41 M 37,26 C 39,31 39,35 37,39 M 47,30 C 49,34 49,37 47,40", "#66635b", 1.50),
    ],
}


def strengthen(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    root.set("data-naturalist-construction", "toddler-food-anatomy-v1")
    root.set("data-toddler-review", "food-complete-v1")

    mark_index = 0
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        # Keep the pass idempotent for direct review runs; ``make font`` also
        # regenerates gray-all before applying it.
        original = float(element.get("data-food-source-width", element.get("stroke-width", "1")))
        element.set("data-food-source-width", f"{original:.2f}")
        phase = mark_index % 3
        if phase == 0:
            width = original * 2.15
            element.set("stroke", "#302e2a")
            brush_pass = "loaded-contour-v2"
        elif phase == 1:
            width = original * 2.35
            element.set("stroke", "#262421")
            brush_pass = "loaded-contour-v2"
        else:
            width = original * 1.75
            element.set("stroke", "#66635b")
            brush_pass = "dry-edge-v2"
        element.set("stroke-width", f"{max(1.25, width):.2f}")
        element.set("data-ink-brush-pass", brush_pass)
        element.set("data-toddler-clarity", "defining-food-anatomy-v1")
        mark_index += 1

    replacement = REPLACEMENTS.get(path.name)
    if replacement:
        for child in list(root):
            if child.tag.rsplit("}", 1)[-1] != "title":
                root.remove(child)
        group = ET.SubElement(root, f"{{{NS}}}g", {
            "id": "food-recognition-replacement",
            "fill": "none",
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
            "data-toddler-clarity": "authored-food-silhouette-v1",
        })
        for index, (drawing, color, width) in enumerate(replacement):
            ET.SubElement(group, f"{{{NS}}}path", {
                "class": "ink-stroke",
                "d": drawing,
                "fill": "none",
                "stroke": color,
                "stroke-width": f"{width:.2f}",
                "pathLength": "1",
                "data-ink-stroke": "tapered",
                "data-ink-role": "recognition-silhouette",
                "data-ink-index": f"food-silhouette-{index}",
                "data-ink-brush-pass": "loaded-contour-v2" if width >= 1.8 else "dry-edge-v2",
            })

    for parent in root.iter():
        for child in list(parent):
            if child.get("id") == "food-recognition-cues":
                parent.remove(child)
    cues = CUES.get(path.name)
    if cues:
        group = ET.SubElement(root, f"{{{NS}}}g", {
            "id": "food-recognition-cues",
            "fill": "none",
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
            "data-toddler-clarity": "defining-food-cues-v1",
        })
        for index, (drawing, color, width) in enumerate(cues):
            ET.SubElement(group, f"{{{NS}}}path", {
                "class": "ink-stroke",
                "d": drawing,
                "fill": "none",
                "stroke": color,
                "stroke-width": f"{width:.2f}",
                "pathLength": "1",
                "data-ink-stroke": "tapered",
                "data-ink-role": "recognition-cue",
                "data-ink-index": f"food-cue-{index}",
                "data-ink-brush-pass": "loaded-contour-v2" if width >= 1.8 else "dry-edge-v2",
            })

    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    food = [entry for entry in entries if entry.get("group") == "Food & Drink"]
    if len(food) != 66:
        raise SystemExit(f"expected 66 Food & Drink glyphs, found {len(food)}")
    for entry in food:
        strengthen(ASSETS / entry["source"])
    print("strengthened all 66 standard Food & Drink glyphs for 32px recognition")


if __name__ == "__main__":
    main()
