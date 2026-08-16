#!/usr/bin/env python3
"""Build familiar sea-creature silhouettes with tapered sumi-e linework."""

from __future__ import annotations

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import SHAPES, taper


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".cache/openmoji/black/svg"
OUTPUT = ROOT / "assets/pua/sea_creatures"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def source_path(filename: str) -> Path:
    value = Path(filename)
    return SOURCE / f"{value.stem.upper()}{value.suffix.lower()}"

SUBJECTS = {
    "coral": "1fab8.svg",
    "crab": "1f980.svg",
    "dolphin": "1f42c.svg",
    "jellyfish": "1fabc.svg",
    "lobster": "1f99e.svg",
    "nautilus": "1f41a.svg",       # spiral shell
    "octopus": "1f419.svg",
    "shark": "1f988.svg",
    "turtle": "1f422.svg",
    "whale": "1f40b.svg",
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def redraw(name: str, filename: str) -> None:
    target = OUTPUT / f"{name}.svg"
    match = re.search(r'data-pua="([^"]+)"', target.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit(f"missing PUA code point in {target}")

    source = ET.parse(source_path(filename)).getroot()
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": f"sea_creatures / {name}",
        "data-pua": match.group(1),
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-naturalist-construction": "toddler-anatomy-v1",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = (
        f"sea_creatures / {name} — toddler-readable anatomical sumi-e study"
    )
    group = ET.SubElement(root, f"{{{NS}}}g", {"transform": "translate(7 7) scale(.81)"})
    for element in source.iter():
        if local(element.tag) not in SHAPES:
            continue
        item = copy.deepcopy(element)
        item.set("fill", "none")
        item.set("stroke", "#262421")
        item.set("stroke-linecap", "round")
        item.set("stroke-linejoin", "round")
        item.set("stroke-width", "2.35")
        group.append(item)

    taper(root)
    for element in root.iter():
        if element.get("data-ink-role") == "line-source-tapered":
            element.set("stroke-width", f"{float(element.get('stroke-width', '1')) * 1.5:.2f}")
            element.set("data-toddler-clarity", "defining-anatomy-v1")
    target.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main() -> None:
    for name, filename in SUBJECTS.items():
        redraw(name, filename)
        print(f"redrew sea_creatures / {name} from {filename}")


if __name__ == "__main__":
    main()
