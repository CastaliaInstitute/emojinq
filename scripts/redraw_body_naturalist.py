#!/usr/bin/env python3
"""Replace simple body pictograms with richer monochrome vector studies."""
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
    "blood": "1FA78.svg",
    "bones": "1F9B4.svg",
    "bounce": "1F3C0.svg",
    "breath": "1F32C.svg",
    "clap": "1F44F.svg",
    "crawl": "1F9CE.svg",
    "grab": "1F590.svg",
    "kick": "1F462.svg",
    "muscles": "1F4AA.svg",
    "pull": "1F9F2.svg",
    "pulse": "1F493.svg",
    "roll": "1F300.svg",
    "shake": "1F44B.svg",
    "walk": "1F6B6.svg",
    "wave": "1F30A.svg",
}


def source_path(name: str) -> Path:
    for path in (ROOT / "assets/gray-all" / name, ROOT / "assets/gray-all" / name.lower(), ROOT / "assets/gray-all" / name.upper()):
        if path.exists():
            return path
    raise SystemExit(f"missing body source {name}")


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
    target = ROOT / "assets/pua/body" / f"{name}.svg"
    original = target.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit(f"missing PUA codepoint in {target}")
    body = "".join(ET.tostring(item, encoding="unicode") for item in paths_from(source_path(source_name)))
    svg = (f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="{NS}" viewBox="0 0 72 72" role="img" aria-label="body / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>body / {name} — naturalist sumi-e study</title>{body}</svg>
''')
    target.write_text(svg)
print(f"redrew {len(SOURCES)} body studies from vector sources")
