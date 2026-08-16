#!/usr/bin/env python3
"""Refine a focused science batch from local semantic vector sources."""
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
    "medicine": "2695.svg",
    "planet": "1FA90.svg",
    "universe": "1F30C.svg",
    "search": "1F50D.svg",
    "observe": "1F441.svg",
    "sensor": "1F4E1.svg",
    "fossil": "1F9AA.svg",
    "generation": "1F9EC.svg",
}


def source_path(name: str) -> Path:
    for path in (ROOT / "assets/gray-all" / name, ROOT / "assets/gray-all" / name.lower(), ROOT / "assets/gray-all" / name.upper()):
        if path.exists():
            return path
    raise SystemExit(f"missing science source {name}")


def paths_from(source: Path) -> list[ET.Element]:
    root = ET.parse(source).getroot()
    items = []
    for index, element in enumerate(root.iter()):
        if element.tag.rsplit("}", 1)[-1] != "path" or not element.get("d"):
            continue
        item = copy.deepcopy(element)
        fill = item.get("fill", "#262522")
        item.set("fill", fill if fill.startswith("#") else "#262522")
        if item.get("fill", "").lower() not in {"#dedbd4", "#dedbd4ff", "#ffffff", "#fff"}:
            item.set("d", roughen_path(item.get("d", ""), index, amount=.075))
            item.set("data-ink-brush-pass", "dry-contour-v1")
        item.set("class", "ink-wash")
        for key in ("stroke", "stroke-width", "style", "data-ink-stroke", "data-ink-wash"):
            item.attrib.pop(key, None)
        items.append(item)
    return items


for name, source_name in SOURCES.items():
    target = ROOT / "assets/pua/science" / f"{name}.svg"
    original = target.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA codepoint in {target}")
    body = "".join(ET.tostring(item, encoding="unicode") for item in paths_from(source_path(source_name)))
    # The eye's broad outer contour can reach the 0-unit edge after vector
    # rasterization. Preserve its proportions while reserving a small margin
    # for laser/export rasterizers.
    if name == "observe":
        body = f'<g transform="translate(1 0) scale(.972 1)">{body}</g>'
    ground = '<path class="ink-dry" fill="#77746a" d="M 8 62 C 21 60 36 63 50 61 C 57 60 63 61 66 59"/>'
    svg = (f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="{NS}" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e study</title>{body}{ground}</svg>
''')
    target.write_text(svg)
print(f"redrew {len(SOURCES)} focused science studies from vector sources")
