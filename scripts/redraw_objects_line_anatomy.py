#!/usr/bin/env python3
"""Replace concrete object pictograms with toddler-readable brush anatomy.

Abstract verbs and ideas remain authored metaphors.  This pass is deliberately
limited to familiar, concrete nouns for which OpenMoji provides an immediately
recognizable outline.
"""

from __future__ import annotations

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import SHAPES, taper


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".cache/openmoji/black/svg"
OUTPUT = ROOT / "assets/pua/objects"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# Prefer the most familiar concrete visual referent for each vocabulary word.
SUBJECTS = {
    "bill": "1f4b5.svg",          # banknote
    "board": "1f4cb.svg",         # clipboard
    "canvas": "1f5bc.svg",        # framed picture/canvas
    "castle": "1f3f0.svg",
    "computer": "1f4bb.svg",
    "currency": "1f4b0.svg",      # money bag
    "doll": "1f9f8.svg",          # teddy bear
    "gallery": "1f5bc.svg",
    "game": "1f3ae.svg",
    "gift": "1f381.svg",
    "goods": "1f4e6.svg",         # package
    "knife": "1f52a.svg",
    "letter": "2709.svg",
    "motor": "2699.svg",          # gear
    "note": "1f4dd.svg",          # memo
    "oven": "1f373.svg",          # cooking/frying pan
    "paint": "1f3a8.svg",         # palette
    "pan": "1f373.svg",
    "pot": "1f372.svg",
    "printing": "1f5a8.svg",      # printer
    "puzzle": "1f9e9.svg",
    "recipe": "1f4d5.svg",        # book
    "repair": "1f527.svg",        # wrench
    "robot": "1f916.svg",
    "save": "1f4be.svg",          # floppy disk
    "sewing": "1faa1.svg",        # needle and thread
    "sock": "1f9e6.svg",
    "treasure": "1f9f0.svg",      # toolbox/chest silhouette
    "tune": "1f3b5.svg",          # musical note
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
        "aria-label": f"objects / {name}",
        "data-pua": match.group(1),
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-naturalist-construction": "toddler-anatomy-v1",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = (
        f"objects / {name} — toddler-readable anatomical sumi-e study"
    )
    group = ET.SubElement(root, f"{{{NS}}}g", {"transform": "translate(7 7) scale(.81)"})
    for shape in source_shapes(source):
        group.append(shape)
    taper(root)
    for element in root.iter():
        if element.get("data-ink-role") == "line-source-tapered":
            element.set("stroke-width", f"{float(element.get('stroke-width', '1')) * 1.5:.2f}")
            element.set("data-toddler-clarity", "defining-anatomy-v1")
    target.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main() -> None:
    missing = [source for source in SUBJECTS.values() if not (SOURCE / source).exists()]
    if missing:
        raise SystemExit(f"missing OpenMoji sources: {', '.join(missing)}")
    for name, source in SUBJECTS.items():
        redraw(name, source)
        print(f"redrew objects / {name} from {source}")


if __name__ == "__main__":
    main()
