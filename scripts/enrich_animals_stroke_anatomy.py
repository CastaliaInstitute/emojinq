#!/usr/bin/env python3
"""Add sparse naturalist anatomy marks to the stroke-only animal studies.

The base animals come from OpenMoji line anatomy.  This pass adds only a few
long, directional marks suggested by a natural-history field sketch: ribs,
shoulders, fur direction, feather structure, and ground gestures.  It never
adds filled masses, opacity, hatching, or a second enclosing contour.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import brush_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "animals"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# Coordinates are card-space studies, not source-specific annotations.  Each
# entry is a small vocabulary of long directional marks for one composition.
DETAILS: dict[str, list[tuple[str, float, str]]] = {
    "calf": [
        ("M 21 30 C 27 27 35 27 42 29", .72, "shoulder"),
        ("M 24 36 C 30 34 36 34 42 36", .55, "rib"),
        ("M 25 41 C 31 44 37 44 43 42", .48, "belly"),
    ],
    "lamb": [
        ("M 22 29 C 28 26 35 26 41 29", .62, "wool-back"),
        ("M 24 35 C 30 32 38 33 44 36", .52, "wool-rib"),
        ("M 27 42 C 33 45 39 45 45 42", .46, "wool-belly"),
    ],
    "predator": [
        ("M 23 35 C 28 32 34 32 39 34", .64, "shoulder"),
        ("M 26 42 C 32 45 38 45 43 43", .50, "rib"),
        ("M 18 34 C 20 33 22 33 24 34", .44, "muzzle"),
    ],
    "prey": [
        ("M 27 36 C 33 33 40 34 45 37", .58, "back"),
        ("M 28 45 C 34 48 40 48 45 46", .48, "haunch"),
        ("M 23 29 C 24 26 25 23 25 20", .40, "ear"),
    ],
    "squirrel": [
        ("M 29 35 C 34 32 40 32 44 35", .62, "shoulder"),
        ("M 29 45 C 34 48 40 48 45 46", .48, "haunch"),
        ("M 47 17 C 51 20 53 24 53 28", .56, "tail-outer"),
        ("M 46 21 C 49 24 50 28 49 32", .44, "tail-inner"),
        ("M 48 25 C 50 28 50 31 48 34", .38, "tail-dry"),
    ],
    "colony": [
        ("M 10 34 C 14 32 18 32 21 34", .42, "bee-a-wing"),
        ("M 29 30 C 34 28 39 28 43 31", .42, "bee-b-wing"),
        ("M 47 35 C 51 33 55 34 58 36", .38, "bee-c-wing"),
    ],
    "flock": [
        ("M 10 30 C 14 28 18 29 21 31", .40, "wing-a"),
        ("M 31 20 C 35 18 39 19 42 21", .42, "wing-b"),
        ("M 51 32 C 55 30 59 31 62 34", .38, "wing-c"),
    ],
    "migration": [
        ("M 9 25 C 13 23 17 24 20 27", .38, "flight-a"),
        ("M 30 16 C 34 14 38 15 41 18", .40, "flight-b"),
        ("M 50 31 C 54 29 58 30 61 33", .38, "flight-c"),
    ],
    "herd": [
        ("M 10 34 C 16 31 23 31 29 34", .48, "back-a"),
        ("M 32 31 C 38 28 46 29 52 32", .50, "back-b"),
        ("M 13 43 C 18 45 23 45 27 44", .40, "rib-a"),
        ("M 36 41 C 41 44 46 44 50 42", .40, "rib-b"),
    ],
    "pack": [
        ("M 10 34 C 15 31 21 31 26 34", .48, "shoulder-a"),
        ("M 31 31 C 36 29 43 30 48 33", .48, "shoulder-b"),
        ("M 12 43 C 17 46 22 46 26 44", .40, "rib-a"),
        ("M 34 41 C 39 44 44 44 48 42", .40, "rib-b"),
    ],
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def add_detail(root: ET.Element, name: str) -> int:
    index = sum(1 for element in root.iter() if local(element.tag) == "path")
    added = 0
    for d, width, role in DETAILS.get(name, []):
        source = ET.Element(f"{{{NS}}}path", {
            "d": d,
            "fill": "none",
            "stroke": "#4a4943",
            "stroke-width": str(width),
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
        })
        for mark_d, mark_width, color in brush_path(d, source, index):
            root.append(ET.Element(f"{{{NS}}}path", {
                "class": "ink-stroke",
                "data-ink-stroke": "tapered",
                "data-ink-role": f"naturalist-detail-{role}",
                "data-ink-index": str(index),
                "pathLength": "1",
                "d": mark_d,
                "fill": "none",
                "stroke": color,
                "stroke-width": f"{mark_width:.2f}",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
            }))
            index += 1
            added += 1
    return added


def main() -> None:
    for path in sorted(OUT.glob("*.svg")):
        name = path.stem
        tree = ET.parse(path)
        root = tree.getroot()
        # Idempotence: remove only this pass's marks before re-adding them.
        for parent in root.iter():
            for child in list(parent):
                if child.get("data-ink-role", "").startswith("naturalist-detail-"):
                    parent.remove(child)
        count = add_detail(root, name)
        root.set("data-naturalist-detail-pass", "anatomy-direction-v1")
        tree.write(path, encoding="utf-8", xml_declaration=False)
        print(f"enriched animals / {name}: {count} tapered detail marks")


if __name__ == "__main__":
    main()
