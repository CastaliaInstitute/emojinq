#!/usr/bin/env python3
"""Replace geometric people symbols with richer vector figure studies."""
from __future__ import annotations

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from collapse_lines import roughen_path

ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

SOURCES = {
    "astronaut": "1F9D1-200D-2708-FE0F.svg",
    "artist": "1F9D1-200D-1F3A8.svg",
    "baker": "1F9D1-200D-1F373.svg",
    "builder": "1F9D1-200D-1F3ED.svg",
    "farmer": "1F9D1-200D-1F33E.svg",
    "healer": "1F9D1-200D-2695-FE0F.svg",
    "nurse": "1F9D1-200D-2695-FE0F.svg",
    "prayer": "1F64F.svg",
    "sage": "1F9D1.svg",
    "seeker": "1F9D1.svg",
}


def source_file(name: str) -> Path:
    exact = ROOT / "assets/gray-all" / name
    if exact.exists():
        return exact
    matches = list((ROOT / "assets/gray-all").glob(name.lower())) + list((ROOT / "assets/gray-all").glob(name.upper()))
    if not matches:
        raise SystemExit(f"missing semantic source {name}")
    return matches[0]


def paths_from(source: Path) -> list[ET.Element]:
    root = ET.parse(source).getroot()
    result = []
    for index, element in enumerate(root.iter()):
        if element.tag.rsplit("}", 1)[-1] != "path" or not element.get("d"):
            continue
        item = copy.deepcopy(element)
        source_fill = item.get("fill", "#262522")
        # Preserve the source's grayscale wash hierarchy.  Flattening every
        # layer to black destroys the negative-space face and makes the figure
        # look like a pictogram; only non-grayscale color would need mapping.
        item.set("fill", source_fill if source_fill.startswith("#") else "#262522")
        if item.get("fill", "").lower() not in {"#dedbd4", "#dedbd4ff", "#ffffff", "#fff"}:
            item.set("d", roughen_path(item.get("d", ""), index, amount=.075))
            item.set("data-ink-brush-pass", "dry-contour-v1")
        item.set("class", "ink-wash")
        for key in ("stroke", "stroke-width", "style", "data-ink-stroke", "data-ink-wash"):
            item.attrib.pop(key, None)
        result.append(item)
    return result


def redraw(name: str, source_name: str) -> None:
    target = ROOT / "assets/pua/people" / f"{name}.svg"
    original = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', original)
    if not codepoint:
        raise SystemExit(f"missing PUA codepoint in {target}")
    source = source_file(source_name)
    body = "".join(ET.tostring(item, encoding="unicode") for item in paths_from(source))
    ground = '<path class="ink-dry" fill="#77746a" d="M 8 63 C 21 60 36 63 49 61 C 56 60 62 61 66 59"/>'
    svg = (f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="{NS}" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>people / {name} — naturalist sumi-e study</title>{body}{ground}</svg>
''')
    target.write_text(svg)


for name, source in SOURCES.items():
    redraw(name, source)
print(f"redrew {len(SOURCES)} people studies from semantic vector sources")
