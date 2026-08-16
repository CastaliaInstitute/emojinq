#!/usr/bin/env python3
"""Add sparse species cues to the stroke-only sea-creature PUA studies."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import brush_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "sea_creatures"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

DETAILS: dict[str, list[tuple[str, float, str]]] = {
    "coral": [
        ("M 35 51 C 31 44 30 37 32 31", .48, "branch-left"),
        ("M 37 43 C 41 37 44 32 44 26", .44, "branch-right"),
        ("M 27 34 C 24 30 22 27 22 23", .36, "branch-tip"),
    ],
    "crab": [
        ("M 24 31 C 30 27 41 27 49 31", .50, "carapace"),
        ("M 27 36 C 33 39 41 39 47 36", .40, "shell-ridge"),
        ("M 13 31 C 16 29 18 30 20 33", .38, "left-claw"),
        ("M 52 33 C 55 30 58 29 61 31", .38, "right-claw"),
    ],
    "dolphin": [
        ("M 19 39 C 27 34 36 33 45 35", .50, "back"),
        ("M 29 44 C 35 47 41 46 46 43", .40, "belly"),
        ("M 37 31 L 40 26", .38, "dorsal-fin"),
        ("M 25 45 L 21 49", .36, "flipper"),
    ],
    "jellyfish": [
        ("M 20 29 C 28 25 43 25 52 29", .52, "bell-rim"),
        ("M 27 36 C 28 43 27 49 29 55", .38, "tentacle-a"),
        ("M 36 36 C 35 43 37 50 36 57", .42, "tentacle-b"),
        ("M 44 35 C 43 42 46 48 44 54", .38, "tentacle-c"),
    ],
    "lobster": [
        ("M 22 34 C 29 30 40 30 49 34", .48, "carapace"),
        ("M 25 39 C 32 42 42 42 49 38", .42, "abdomen"),
        ("M 29 35 C 34 37 40 37 45 35", .34, "segment-gesture"),
    ],
    "manta": [
        ("M 13 25 C 21 28 28 31 36 32 C 45 30 53 27 60 24", .48, "wing-ridge"),
        ("M 24 28 C 27 32 29 35 30 39", .34, "left-ray"),
        ("M 48 28 C 45 32 43 35 42 39", .34, "right-ray"),
        ("M 36 32 C 36 39 37 45 38 51", .38, "tail"),
    ],
    "nautilus": [
        ("M 48 25 C 41 22 34 23 30 28 C 27 32 28 38 33 40", .52, "spiral-chamber"),
        ("M 51 31 C 47 28 43 28 40 31 C 38 34 39 37 42 38", .42, "spiral-inner"),
        ("M 22 40 C 28 46 35 49 43 48", .34, "shell-rib"),
    ],
    "octopus": [
        ("M 28 26 C 32 22 40 22 44 26", .44, "mantle"),
        ("M 25 40 C 20 45 17 47 14 48", .36, "arm-flow-left"),
        ("M 45 39 C 51 43 55 45 60 45", .36, "arm-flow-right"),
        ("M 28 43 C 30 46 31 49 31 52", .34, "sucker-line-left"),
        ("M 42 43 C 41 47 43 50 45 53", .34, "sucker-line-right"),
    ],
    "seahorse": [
        ("M 39 25 C 43 28 44 32 42 36 C 40 40 40 44 42 47", .48, "body-ridge"),
        ("M 43 29 L 48 31", .34, "fin"),
        ("M 39 33 L 44 35", .34, "body-segment-a"),
        ("M 39 38 L 44 40", .34, "body-segment-b"),
        ("M 36 48 C 32 51 29 53 27 54", .36, "tail-curl"),
    ],
    "shark": [
        ("M 15 37 C 24 34 35 34 45 37", .50, "lateral-line"),
        ("M 25 42 C 30 44 36 44 41 42", .36, "belly"),
        ("M 20 39 C 20 42 20 44 19 46", .34, "gill-a"),
        ("M 23 38 C 23 41 23 43 22 45", .34, "gill-b"),
    ],
    "turtle": [
        ("M 21 34 C 28 29 40 28 50 34", .50, "shell-arch"),
        ("M 24 39 C 31 42 41 42 50 38", .38, "shell-seam"),
    ],
    "whale": [
        ("M 14 36 C 24 33 35 34 47 38", .48, "back"),
        ("M 19 43 C 27 47 37 47 45 44", .38, "belly"),
        ("M 30 29 C 31 25 33 22 34 19", .36, "blow"),
        ("M 49 45 C 54 45 58 44 61 42", .34, "tail-root"),
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
        for parent in root.iter():
            for child in list(parent):
                if child.get("data-ink-role", "").startswith("naturalist-detail-"):
                    parent.remove(child)
        count = add_detail(root, name)
        root.set("data-naturalist-detail-pass", "species-cues-v1")
        tree.write(path, encoding="utf-8", xml_declaration=False)
        print(f"enriched sea creatures / {name}: {count} tapered detail marks")


if __name__ == "__main__":
    main()
