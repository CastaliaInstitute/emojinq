#!/usr/bin/env python3
"""Replace ambiguous farm animal masses with toddler-readable brush anatomy."""

from __future__ import annotations

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import SHAPES, taper


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".cache/openmoji/black/svg"
OUTPUT = ROOT / "assets/pua/farm"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

SUBJECTS = {
    "bee": "1f41d.svg",
    "chicken": "1f414.svg",
    "cow": "1f404.svg",
    "honey": "1f36f.svg",
    "meat": "1f969.svg",
    "milk": "1f37c.svg",
    "pig": "1f416.svg",
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def source_shapes(filename: str) -> list[ET.Element]:
    root = ET.parse(SOURCE / filename).getroot()
    shapes: list[ET.Element] = []
    for element in root.iter():
        if local(element.tag) not in SHAPES:
            continue
        item = copy.deepcopy(element)
        item.set("fill", "none")
        item.set("stroke", "#262421")
        item.set("stroke-linecap", "round")
        item.set("stroke-linejoin", "round")
        item.set("stroke-width", "2.35")
        shapes.append(item)
    return shapes


def redraw(name: str, source: str) -> None:
    target = OUTPUT / f"{name}.svg"
    match = re.search(r'data-pua="([^"]+)"', target.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit(f"missing PUA code point in {target}")
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": f"farm / {name}",
        "data-pua": match.group(1),
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-naturalist-construction": "toddler-anatomy-v1",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = f"farm / {name} — toddler-readable anatomical sumi-e study"
    group = ET.SubElement(root, f"{{{NS}}}g", {"transform": "translate(7 7) scale(.81)"})
    for shape in source_shapes(source):
        group.append(shape)
    taper(root)
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        element.set("stroke-width", f"{float(element.get('stroke-width', '1')) * 1.5:.2f}")
        element.set("data-toddler-clarity", "defining-anatomy-v1")
    target.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main() -> None:
    missing = [source for source in SUBJECTS.values() if not (SOURCE / source).exists()]
    if missing:
        raise SystemExit(f"missing OpenMoji sources: {', '.join(missing)}")
    for name, source in SUBJECTS.items():
        redraw(name, source)
        print(f"redrew farm / {name} from {source}")


if __name__ == "__main__":
    main()
