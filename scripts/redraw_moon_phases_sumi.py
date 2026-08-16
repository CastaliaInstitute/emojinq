#!/usr/bin/env python3
"""Author distinct, toddler-readable sumi-e silhouettes for the moon phases."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/gray-all"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

OUTER_RIGHT = "C 51.5,8 64,20.5 64,36 C 64,51.5 51.5,64 36,64"
OUTER_LEFT = "C 20.5,64 8,51.5 8,36 C 8,20.5 20.5,8 36,8"

PHASES = {
    # New moon: an ink-loaded disk. Stars make the night-sky referent explicit.
    "1F311": "M 36,8 C 51.5,8 64,20.5 64,36 C 64,51.5 51.5,64 36,64 C 20.5,64 8,51.5 8,36 C 8,20.5 20.5,8 36,8 Z",
    # Waxing silhouettes place the illuminated brush mass on the right.
    "1F312": f"M 36,8 {OUTER_RIGHT} C 45,55 48,46 48,36 C 48,26 45,17 36,8 Z",
    "1F313": f"M 36,8 {OUTER_RIGHT} L 36,8 Z",
    "1F314": f"M 36,8 {OUTER_RIGHT} C 23,54 21,18 36,8 Z",
    # Full moon is a breathing outline rather than an indiscriminate disk.
    "1F315": "",
    # Waning silhouettes mirror the waxing sequence.
    "1F316": f"M 36,8 C 23,18 21,54 36,64 {OUTER_LEFT} Z",
    "1F317": f"M 36,8 L 36,64 {OUTER_LEFT} Z",
    "1F318": f"M 36,8 C 27,17 24,26 24,36 C 24,46 27,55 36,64 {OUTER_LEFT} Z",
}


def element(parent: ET.Element, tag: str, **attrs: str) -> ET.Element:
    return ET.SubElement(parent, f"{{{SVG_NS}}}{tag}", attrs)


def build(codepoint: str, phase: str) -> ET.ElementTree:
    root = ET.Element(
        f"{{{SVG_NS}}}svg",
        {
            "viewBox": "0 0 72 72",
            "role": "img",
            "aria-label": f"moon phase U+{codepoint}",
            "data-castalia-style": "sumi-e-naturalist-v2",
            "data-ink-stroke-system": "filled-brush-mass-v2",
            "data-ink-animation": "wash-v1",
        },
    )
    element(root, "title").text = f"Moon phase U+{codepoint} — toddler-readable sumi-e study"
    if phase:
        element(
            root,
            "path",
            **{
                "class": "ink-wash",
                "d": phase,
                "fill": "#262522",
                "data-ink-brush-pass": "loaded-ribbon-v2",
            },
        )
    else:
        element(
            root,
            "circle",
            **{
                "class": "ink-dry",
                "cx": "36",
                "cy": "36",
                "r": "27.5",
                "fill": "none",
                "stroke": "#262522",
                "stroke-width": "2.4",
                "data-ink-brush-pass": "dry-edge-v1",
            },
        )
        # Irregular crater gestures distinguish the full moon from a generic
        # circle without arranging themselves like a face.
        element(root, "path", **{"class": "ink-dry", "d": "M 23,24 C 25,20 30,21 31,24 C 29,27 25,27 23,24 Z", "fill": "none", "stroke": "#4a4943", "stroke-width": "1.6"})
        element(root, "path", **{"class": "ink-dry", "d": "M 44,31 C 48,29 51,32 49,36 C 46,38 43,35 44,31 Z", "fill": "none", "stroke": "#77746a", "stroke-width": "1.5"})
        element(root, "path", **{"class": "ink-dry", "d": "M 28,48 C 31,45 36,47 36,50", "fill": "none", "stroke": "#4a4943", "stroke-width": "1.4"})

    # Sparse stars supply a familiar night context without crowding the phase.
    element(root, "path", **{"class": "ink-wash", "d": "M 12,16 L 13.2,19.2 L 16,20 L 13.2,21 L 12,24 L 10.8,21 L 8,20 L 10.8,19.2 Z", "fill": "#4a4943", "data-ink-brush-pass": "loaded-dab-v1"})
    element(root, "circle", **{"class": "ink-dry", "cx": "59", "cy": "14", "r": "1.7", "fill": "#77746a", "data-ink-brush-pass": "dry-fragment-v1"})
    return ET.ElementTree(root)


def main() -> None:
    for codepoint, phase in PHASES.items():
        target = OUTPUT / f"{codepoint}.svg"
        build(codepoint, phase).write(target, encoding="utf-8", xml_declaration=True)
        print(target)


if __name__ == "__main__":
    main()
