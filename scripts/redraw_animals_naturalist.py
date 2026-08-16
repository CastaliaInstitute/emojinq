#!/usr/bin/env python3
"""Compose the PUA animal concepts from richer local vector anatomy sources."""
from __future__ import annotations

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

SOURCE = {
    "cow": "1f404",
    "sheep": "1f411",
    "wolf": "1f43a",
    "rabbit": "1f407",
    "bee": "1f41d",
    "bird": "1f426",
    "goose": "1f986",
}

COMPOSITIONS = {
    "calf": [("cow", "translate(7 8) scale(.82)")],
    "lamb": [("sheep", "translate(8 8) scale(.82)")],
    "predator": [("wolf", "translate(5 7) scale(.86)")],
    "prey": [("rabbit", "translate(7 9) scale(.84)")],
    # Keep the group compositions inside a safe 3-unit margin. The previous
    # negative translations made the leftmost animals clip at card size.
    "colony": [("bee", "translate(3 9) scale(.48)"), ("bee", "translate(25 6) scale(.54)"), ("bee", "translate(42 12) scale(.36)")],
    # Use full bird anatomy here; the upstream short-wing bird collapses into
    # leaf-shaped marks when repeated at card size.
    "flock": [("goose", "translate(4 12) scale(.40)"), ("goose", "translate(25 5) scale(.43)"), ("goose", "translate(48 16) scale(.34)")],
    "migration": [("goose", "translate(2 28) scale(.34)"), ("goose", "translate(24 17) scale(.42)"), ("goose", "translate(49 5) scale(.34)")],
    "herd": [("cow", "translate(3 13) scale(.46)"), ("cow", "translate(25 8) scale(.48)"), ("cow", "translate(42 14) scale(.34)")],
    "pack": [("wolf", "translate(3 13) scale(.46)"), ("wolf", "translate(25 7) scale(.48)"), ("wolf", "translate(42 14) scale(.34)")],
}


def source_paths(code: str) -> list[ET.Element]:
    root = ET.parse(ROOT / "assets/gray-all" / f"{code}.svg").getroot()
    paths: list[ET.Element] = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] != "path" or not element.get("d"):
            continue
        item = copy.deepcopy(element)
        item.set("fill", "#262522")
        item.set("class", "ink-wash")
        for key in ("stroke", "stroke-width", "style", "data-ink-stroke"):
            item.attrib.pop(key, None)
        paths.append(item)
    return paths


def redraw(name: str, entries: list[tuple[str, str]]) -> None:
    target = ROOT / "assets/pua/animals" / f"{name}.svg"
    original = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', original)
    if not codepoint:
        raise SystemExit(f"missing PUA codepoint in {target}")
    groups: list[str] = []
    for source_name, transform in entries:
        code = SOURCE[source_name]
        body = []
        for path in source_paths(code):
            body.append(ET.tostring(path, encoding="unicode"))
        groups.append(f'<g transform="{transform}">{"".join(body)}</g>')
    accent = ""
    if name == "colony":
        accent = (
            '<path class="ink-wash" fill="#77746a" d="M 27 48 C 29 43 35 40 41 42 '
            'C 47 40 53 43 55 48 L 52 56 C 45 58 35 57 29 55 Z"/>'
            '<path class="ink-dry" fill="#262522" d="M 33 47 C 36 45 39 46 41 48 '
            'M 43 47 C 46 45 49 46 51 48 M 35 52 C 38 50 41 51 43 53 '
            'M 45 52 C 48 50 50 51 52 53"/>'
        )
    ground = '<path class="ink-dry" fill="#77746a" d="M 8 61 C 20 59 34 62 47 60 C 55 59 61 60 65 59"/>'
    svg = (f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="{NS}" viewBox="0 0 72 72" role="img" aria-label="animals / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>animals / {name} — naturalist sumi-e study</title>{"".join(groups)}{accent}{ground}</svg>
''')
    target.write_text(svg)


for animal, entries in COMPOSITIONS.items():
    redraw(animal, entries)
print(f"redrew {len(COMPOSITIONS)} animal studies from vector anatomy sources")
