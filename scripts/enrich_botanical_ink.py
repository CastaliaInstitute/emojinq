#!/usr/bin/env python3
"""Add observed botanical structure to the flora and herb SVG studies."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ROOT = Path(__file__).resolve().parents[1] / "assets/pua"


def mark(d: str, color: str = "#262522", width: str = "0.72", cls: str = "ink-stroke") -> ET.Element:
    return ET.Element(f"{{{NS}}}path", {
        "class": cls,
        "fill": "none",
        "stroke": color,
        "stroke-width": width,
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "pathLength": "1",
        "d": d,
    })


DETAILS = {
    "flora/apple": [
        ("M24 40 C29 38 34 39 38 42 M42 38 C45 39 48 41 49 44", "#77746a", "0.62"),
        ("M33 16 C35 19 35 22 34 25", "#262522", "0.66"),
    ],
    "flora/berrybush": [
        ("M20 28 C21 26 23 25 25 26 M48 28 C49 26 51 25 53 25", "#262522", "0.68"),
        ("M24 31 C22 29 21 28 20 27 M47 29 C45 27 44 26 43 25", "#77746a", "0.58", "ink-dry"),
    ],
    "flora/birch": [
        ("M32 26 L37 28 M32 34 L38 36 M33 43 L38 45", "#262522", "0.72"),
        ("M23 21 C25 20 27 20 29 21 M43 25 C45 23 47 22 49 22", "#77746a", "0.62", "ink-dry"),
    ],
    "flora/bush": [
        ("M20 47 C23 42 26 39 29 37 M39 49 C40 43 43 39 46 36 M48 48 C51 44 54 42 57 40", "#262522", "0.70"),
    ],
    "flora/fern": [
        ("M30 46 C28 43 26 41 23 40 M33 41 C31 38 29 36 26 34 M36 36 C34 33 32 31 30 29", "#77746a", "0.62"),
        ("M31 47 C35 44 39 42 42 40 M34 41 C38 39 42 36 46 33 M38 35 C42 32 46 29 49 26", "#262522", "0.62"),
    ],
    "flora/grass": [
        ("M33 51 C31 45 29 40 27 35 M39 51 C42 45 46 41 50 36 M36 50 C36 43 37 36 37 30", "#77746a", "0.52", "ink-dry"),
    ],
    "flora/maple": [
        ("M36 34 L31 27 M36 34 L41 27 M36 34 L36 21", "#262522", "0.72"),
    ],
    "flora/palm": [
        ("M37 25 C33 21 29 19 25 18 M39 24 C39 19 39 15 38 11 M41 25 C46 21 50 19 54 18", "#77746a", "0.62"),
        ("M32 22 C30 20 28 19 26 18 M46 21 C49 19 51 18 53 18", "#262522", "0.56", "ink-dry"),
    ],
    "flora/pine": [
        ("M34 29 C31 27 28 26 25 26 M37 34 C41 32 44 31 48 31 M34 40 C30 39 26 39 22 41 M38 45 C43 44 47 45 52 47", "#77746a", "0.62"),
    ],
    "flora/poplar": [
        ("M36 38 C34 32 34 25 36 17 M36 33 C39 29 40 25 41 20", "#77746a", "0.66"),
    ],
    "flora/reed": [
        ("M27 39 L30 39 M35 35 L39 35 M44 41 L47 41", "#262522", "0.66"),
    ],
    "flora/snag": [
        ("M33 38 L39 40 M32 45 L38 47 M34 51 L40 53", "#77746a", "0.72", "ink-dry"),
    ],
    "flora/spruce": [
        ("M34 28 C31 27 28 27 25 28 M38 34 C42 33 46 34 49 36 M34 40 C30 40 26 42 22 44 M39 46 C44 47 48 49 52 51", "#77746a", "0.58"),
    ],
    "flora/stump": [
        ("M27 28 C31 26 39 26 46 28 M29 30 C33 29 39 29 44 30 M25 39 C30 41 40 41 47 39 M25 47 C31 49 41 49 48 47", "#262522", "0.62"),
        ("M25 35 C30 37 40 37 48 35", "#77746a", "0.56", "ink-dry"),
    ],
    "flora/willow": [
        ("M23 35 C25 42 25 49 24 56 M30 36 C31 44 31 51 30 59 M43 36 C44 44 46 51 47 58 M50 35 C52 42 53 49 54 55", "#77746a", "0.58"),
    ],
    "herbs/aloe": [
        ("M36 52 C34 43 33 34 35 21 M36 52 C40 43 44 35 50 28 M34 51 C29 44 25 39 20 36", "#77746a", "0.62"),
    ],
    "herbs/basil": [
        ("M22 31 C26 32 29 34 32 36 M39 32 C43 30 46 28 49 26 M25 23 C28 25 31 27 33 29 M39 24 C42 22 44 20 46 19", "#77746a", "0.58"),
    ],
    "herbs/calendula": [
        ("M30 18 C32 19 34 20 36 21 M37 21 C39 19 41 18 43 17", "#77746a", "0.62"),
    ],
    "herbs/chamomile": [
        ("M25 20 C27 20 28 20 29 20 M45 23 C46 23 47 23 48 23", "#77746a", "0.58"),
    ],
    "herbs/chive": [
        ("M28 54 C28 44 29 34 30 24 M35 55 C36 45 37 35 38 25 M42 55 C43 45 45 36 47 28", "#77746a", "0.55", "ink-dry"),
    ],
    "herbs/cilantro": [
        ("M28 48 C30 42 32 37 34 32 M43 48 C41 42 39 37 37 32", "#77746a", "0.58"),
    ],
    "herbs/dandelion": [
        ("M36 25 C31 22 27 21 23 21 M37 25 C42 22 46 21 50 21 M36 28 C31 27 27 27 24 28", "#77746a", "0.56", "ink-dry"),
    ],
    "herbs/dill": [
        ("M34 35 C30 33 27 31 24 29 M38 35 C42 32 45 30 48 27 M35 42 C31 40 28 38 26 36", "#77746a", "0.58"),
    ],
    "herbs/echinacea": [
        ("M29 19 L25 15 M32 18 L30 13 M40 18 L43 13 M43 20 L48 16", "#77746a", "0.58"),
    ],
    "herbs/elderberry": [
        ("M27 38 C30 36 33 36 35 37 M38 37 C41 35 44 35 47 36", "#77746a", "0.62"),
    ],
    "herbs/garlic": [
        ("M28 45 C32 47 39 47 44 44 M30 50 C34 52 39 52 43 50", "#77746a", "0.60"),
    ],
    "herbs/ginger": [
        ("M23 44 C29 42 35 43 41 45 M30 48 C35 47 40 48 45 50", "#77746a", "0.62"),
    ],
    "herbs/lavender": [
        ("M32 25 C34 24 36 24 39 25 M32 21 C34 20 37 20 39 21 M32 17 C34 16 37 16 39 17", "#77746a", "0.55", "ink-dry"),
    ],
    "herbs/mint": [
        ("M20 37 C23 38 26 39 29 40 M43 35 C46 34 49 32 52 31 M24 25 C27 26 30 28 32 29 M40 24 C43 23 45 21 47 20", "#77746a", "0.60"),
    ],
    "herbs/nettle": [
        ("M31 49 C29 44 27 40 25 36 M40 49 C43 44 45 40 47 36", "#77746a", "0.64"),
    ],
    "herbs/oregano": [
        ("M28 45 C31 42 34 41 36 41 M39 40 C42 38 45 37 48 37", "#77746a", "0.58"),
    ],
    "herbs/parsley": [
        ("M30 50 C31 45 32 41 34 38 M36 50 C37 45 39 41 41 38 M42 50 C43 45 45 42 47 40", "#77746a", "0.56"),
    ],
    "herbs/plantain": [
        ("M36 55 C34 47 32 39 29 31 M36 55 C38 46 41 38 45 30 M35 53 C30 47 27 43 24 39", "#77746a", "0.62"),
    ],
    "herbs/rosemary": [
        ("M35 43 C31 41 28 39 25 37 M37 39 C41 37 44 35 47 32 M35 33 C31 31 28 29 25 27 M37 29 C40 27 43 24 46 21", "#77746a", "0.56"),
    ],
    "herbs/sage": [
        ("M17 37 C22 38 27 39 32 40 M40 35 C45 34 50 32 55 31", "#262522", "0.66"),
    ],
    "herbs/thyme": [
        ("M29 52 C31 47 32 43 33 38 M38 52 C40 47 42 43 44 39", "#77746a", "0.58", "ink-dry"),
    ],
    "herbs/yarrow": [
        ("M28 42 C31 40 33 39 35 39 M38 38 C41 36 44 35 47 34", "#77746a", "0.60"),
    ],
}


changed = 0
for key, specs in DETAILS.items():
    category, name = key.split("/")
    target = ROOT / category / f"{name}.svg"
    tree = ET.parse(target)
    root = tree.getroot()
    if root.get("data-ink-detail") == "botanical-naturalist-v2":
        continue
    group = ET.SubElement(root, f"{{{NS}}}g", {"data-ink-detail": "botanical-naturalist-v2"})
    for spec in specs:
        group.append(mark(*spec))
    root.set("data-ink-detail", "botanical-naturalist-v2")
    tree.write(target, encoding="utf-8", xml_declaration=True)
    changed += 1

print(f"enriched {changed} botanical glyphs with structural brush details")
