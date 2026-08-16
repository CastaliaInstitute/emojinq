#!/usr/bin/env python3
"""Add loaded-brush recognition anatomy to PUA referents that collapse at 32px."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "pua"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

OUTLIERS: dict[str, list[tuple[str, dict[str, str]]]] = {
    "sea_creatures/whale.svg": [
        ("path", {"d": "M17 39 C21 31 31 28 42 30 C51 31 57 35 56 40 C55 46 47 49 36 49 C27 49 20 45 17 42 Z", "fill": "#77746a"}),
        ("path", {"d": "M18 40 L10 35 L13 41 L10 47 Z", "fill": "#4a4943"}),
        ("path", {"d": "M38 46 C41 51 45 53 49 52 C45 49 44 46 43 43 Z", "fill": "#4a4943"}),
        ("circle", {"cx": "52", "cy": "35", "r": "1.6", "fill": "#262421"}),
    ],
    "sea_creatures/seahorse.svg": [
        ("path", {"d": "M45 18 C41 14 35 15 35 20 C35 24 40 25 40 29 C35 34 32 41 34 48 C36 53 42 52 44 55 C47 60 41 64 36 61", "fill": "none", "stroke": "#4a4943", "stroke-width": "6.0"}),
        ("path", {"d": "M44 18 C50 18 54 20 50 22 L44 23 Z", "fill": "#77746a"}),
        ("path", {"d": "M34 34 L25 29 L27 42 Z", "fill": "#bcb9af", "stroke": "#66635b", "stroke-width": "1.4"}),
        ("circle", {"cx": "40", "cy": "19", "r": "1.8", "fill": "#262421"}),
    ],
    "sea_creatures/manta.svg": [
        ("path", {"d": "M8 34 C18 25 27 24 36 29 C45 24 54 25 64 34 C55 42 46 43 36 38 C26 43 17 42 8 34 Z", "fill": "#77746a"}),
        ("path", {"d": "M32 29 C34 26 39 26 41 29 L40 38 C38 41 34 41 32 38 Z", "fill": "#4a4943"}),
        ("path", {"d": "M36 39 C37 48 42 55 47 61", "fill": "none", "stroke": "#262421", "stroke-width": "2.6"}),
        ("circle", {"cx": "32", "cy": "31", "r": "1.5", "fill": "#262421"}),
        ("circle", {"cx": "41", "cy": "31", "r": "1.5", "fill": "#262421"}),
    ],
    "farm/carrot.svg": [
        ("path", {"d": "M29 27 C32 24 40 24 43 28 C42 39 39 50 36 58 C32 50 29 39 29 27 Z", "fill": "#77746a"}),
        ("path", {"d": "M35 27 C31 21 28 17 27 13 M36 26 C36 19 37 14 39 10 M38 27 C43 21 47 18 50 16", "fill": "none", "stroke": "#4a4943", "stroke-width": "3.0"}),
    ],
    "farm/egg.svg": [
        ("path", {"d": "M36 14 C29 16 24 25 24 36 C24 48 29 56 36 57 C44 56 49 48 49 36 C49 25 43 16 36 14 Z", "fill": "#d6d3ca", "stroke": "#4a4943", "stroke-width": "2.8"}),
        ("path", {"d": "M31 28 C34 31 38 31 41 28", "fill": "none", "stroke": "#bcb9af", "stroke-width": "2.0"}),
    ],
    "farm/flour.svg": [
        ("path", {"d": "M28 25 C31 21 41 21 44 25 L52 49 C47 55 26 55 20 49 Z", "fill": "#bcb9af", "stroke": "#4a4943", "stroke-width": "2.4"}),
        ("path", {"d": "M27 27 C33 29 40 29 46 27 M36 48 L36 34 M36 39 L30 35 M36 43 L42 38", "fill": "none", "stroke": "#66635b", "stroke-width": "2.0"}),
    ],
    "farm/strawberry.svg": [
        ("path", {"d": "M36 24 C27 19 20 25 22 35 C24 46 31 54 36 58 C42 53 49 45 51 35 C52 25 44 20 36 24 Z", "fill": "#77746a", "stroke": "#4a4943", "stroke-width": "1.8"}),
        ("path", {"d": "M36 26 C31 22 26 22 22 25 C28 26 31 30 36 31 C41 28 46 25 50 25 C45 21 40 22 36 26 Z", "fill": "#4a4943"}),
        ("path", {"d": "M29 34 L30 36 M38 36 L39 38 M44 33 L45 35 M33 45 L34 47 M41 46 L42 48", "fill": "none", "stroke": "#f4f1e9", "stroke-width": "1.8"}),
    ],
    "farm/wheat.svg": [
        ("path", {"d": "M36 59 L36 17", "fill": "none", "stroke": "#4a4943", "stroke-width": "3.0"}),
        ("ellipse", {"cx": "31", "cy": "20", "rx": "3.0", "ry": "5.0", "fill": "#77746a"}),
        ("ellipse", {"cx": "41", "cy": "25", "rx": "3.0", "ry": "5.0", "fill": "#77746a"}),
        ("ellipse", {"cx": "31", "cy": "31", "rx": "3.0", "ry": "5.0", "fill": "#4a4943"}),
        ("ellipse", {"cx": "41", "cy": "37", "rx": "3.0", "ry": "5.0", "fill": "#4a4943"}),
    ],
    "flora/berrybush.svg": [
        ("circle", {"cx": "25", "cy": "40", "r": "9", "fill": "#77746a"}),
        ("circle", {"cx": "36", "cy": "33", "r": "11", "fill": "#77746a"}),
        ("circle", {"cx": "48", "cy": "40", "r": "9", "fill": "#77746a"}),
        ("path", {"d": "M36 39 L36 59 M36 49 L27 43 M36 48 L46 41", "fill": "none", "stroke": "#4a4943", "stroke-width": "3.2"}),
        ("circle", {"cx": "24", "cy": "37", "r": "2.8", "fill": "#f4f1e9"}),
        ("circle", {"cx": "35", "cy": "27", "r": "2.8", "fill": "#262421"}),
        ("circle", {"cx": "43", "cy": "35", "r": "2.8", "fill": "#f4f1e9"}),
        ("circle", {"cx": "51", "cy": "41", "r": "2.8", "fill": "#262421"}),
    ],
    "flora/maple.svg": [
        ("path", {"d": "M36 12 L40 22 L48 18 L46 29 L56 28 L49 37 L54 43 L41 41 L36 55 L31 41 L18 43 L23 36 L16 28 L26 29 L24 18 L32 22 Z", "fill": "#77746a", "stroke": "#4a4943", "stroke-width": "1.6"}),
        ("path", {"d": "M36 39 L36 61", "fill": "none", "stroke": "#4a4943", "stroke-width": "3.2"}),
    ],
    "flora/willow.svg": [
        ("path", {"d": "M20 34 C20 26 28 21 36 22 C45 20 53 26 53 34 C50 39 44 40 38 37 C31 41 23 39 20 34 Z", "fill": "#77746a"}),
        ("path", {"d": "M25 33 C24 42 23 51 22 59 M32 34 C31 43 30 52 30 61 M43 34 C44 43 45 52 46 60 M49 32 C50 40 52 48 54 56", "fill": "none", "stroke": "#4a4943", "stroke-width": "2.8"}),
        ("path", {"d": "M36 34 C35 43 35 52 36 62", "fill": "none", "stroke": "#262421", "stroke-width": "3.4"}),
    ],
}


def main() -> None:
    for relative, marks in OUTLIERS.items():
        path = ASSETS / relative
        tree = ET.parse(path)
        root = tree.getroot()
        for parent in root.iter():
            for child in list(parent):
                if child.get("id") == "pua-toddler-recognition-cues":
                    parent.remove(child)
        group = ET.Element(
            f"{{{NS}}}g",
            {
                "id": "pua-toddler-recognition-cues",
                "data-ink-role": "recognition-brush-mass",
                "data-toddler-clarity": "defining-pua-object-anatomy-v1",
            },
        )
        for tag, attributes in marks:
            is_stroke = attributes.get("fill", "none") == "none"
            attributes = {
                "class": "ink-stroke" if is_stroke else "ink-wash",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
                **attributes,
            }
            if is_stroke:
                attributes["pathLength"] = "1"
            ET.SubElement(group, f"{{{NS}}}{tag}", attributes)
        # Paint the recognition anatomy last. These marks are the decisive loaded-brush
        # silhouette, so they must not be obscured by the inherited exploratory wash.
        root.append(group)
        tree.write(path, encoding="utf-8", xml_declaration=True)
    print(f"redrew {len(OUTLIERS)} PUA semantic outliers with toddler-readable brush anatomy")


if __name__ == "__main__":
    main()
