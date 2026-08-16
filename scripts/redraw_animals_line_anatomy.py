#!/usr/bin/env python3
"""Build the animal PUA studies from anatomical OpenMoji line sources.

The earlier animal studies used broad filled masses and collapsed into tiny
symbols in the contact sheet.  These compositions keep the source anatomy
(eyes, ears, joints, feet, wings, and tails), compose it at card scale, and
run the same pressure treatment as the standard Unicode corpus.  The output
is deliberately stroke-only; no raster or filled brush ribbon is shipped.
"""

from __future__ import annotations

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import SHAPES, taper

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".cache" / "openmoji" / "black" / "svg"
OUT = ROOT / "assets" / "pua" / "animals"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# One animal at a useful reading size, or a small composition of distinct
# animals.  The transforms leave a consistent margin around the 72-unit card.
COMPOSITIONS: dict[str, list[tuple[str, str, float]]] = {
    "calf": [("1f404.svg", "translate(8 8) scale(.78)", 1.0)],
    "lamb": [("1f411.svg", "translate(8 8) scale(.78)", 1.0)],
    "predator": [("1f43a.svg", "translate(6 7) scale(.84)", 1.0)],
    "prey": [("1f407.svg", "translate(7 8) scale(.82)", 1.0)],
    "squirrel": [("1f43f.svg", "translate(7 7) scale(.84)", 1.0)],
    "colony": [
        ("1f41d.svg", "translate(4 13) scale(.48)", 2.2),
        ("1f41d.svg", "translate(25 5) scale(.54)", 2.0),
        ("1f41d.svg", "translate(40 20) scale(.38)", 2.5),
    ],
    "flock": [
        ("1f426.svg", "translate(2 26) scale(.42)", 2.2),
        ("1f426.svg", "translate(25 13) scale(.50)", 2.0),
        ("1f426.svg", "translate(45 5) scale(.33)", 2.7),
    ],
    "migration": [
        ("1f986.svg", "translate(1 28) scale(.34)", 2.5),
        ("1f986.svg", "translate(23 17) scale(.43)", 2.2),
        ("1f986.svg", "translate(48 5) scale(.34)", 2.5),
    ],
    "herd": [
        ("1f404.svg", "translate(4 17) scale(.43)", 2.2),
        ("1f404.svg", "translate(24 8) scale(.52)", 2.0),
        ("1f404.svg", "translate(42 19) scale(.38)", 2.4),
    ],
    "pack": [
        ("1f43a.svg", "translate(1 17) scale(.46)", 2.2),
        ("1f43a.svg", "translate(24 8) scale(.52)", 2.0),
        ("1f43a.svg", "translate(44 18) scale(.40)", 2.4),
    ],
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def source_shapes(filename: str, width_scale: float) -> list[ET.Element]:
    root = ET.parse(SOURCE / filename).getroot()
    shapes: list[ET.Element] = []
    for element in root.iter():
        if local(element.tag) not in SHAPES:
            continue
        item = copy.deepcopy(element)
        # OpenMoji uses un-stroked filled circles for tiny eyes.  The taper
        # pass will turn those into one deliberate closed stroke.
        item.set("fill", "none")
        item.set("stroke", "#262421")
        item.set("stroke-linecap", "round")
        item.set("stroke-linejoin", "round")
        item.set("stroke-width", f"{2.0 / width_scale:.3f}")
        shapes.append(item)
    return shapes


def write(name: str, entries: list[tuple[str, str, float]]) -> None:
    target = OUT / f"{name}.svg"
    original = target.read_text(encoding="utf-8")
    match = re.search(r'data-pua="([^"]+)"', original)
    if not match:
        raise SystemExit(f"missing PUA code point in {target}")

    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": f"animals / {name}",
        "data-pua": match.group(1),
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-ink-path-units": "normalized",
        "data-naturalist-construction": "profile-anatomy-v7",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = (
        f"animals / {name} — anatomical line study"
    )
    for filename, transform, scale in entries:
        group = ET.SubElement(root, f"{{{NS}}}g", {"transform": transform})
        for shape in source_shapes(filename, scale):
            group.append(shape)
    taper(root)
    # These SVGs are displayed directly in the review gallery as well as
    # compiled into the font. Give their anatomical strokes enough body to
    # survive card-size viewing; the TTF builder applies its own text-size
    # compensation downstream.
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        # A three-wolf pack has substantially more overlapping anatomy than a
        # single animal. Keep its contour open enough to retain sumi-e negative
        # space while leaving every head, leg, and tail readable.
        body_multiplier = 1.10 if name == "pack" else 1.45
        element.set("stroke-width", f"{float(element.get('stroke-width', '1')) * body_multiplier:.2f}")
        element.set("data-toddler-clarity", "defining-anatomy-v1")
    target.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main() -> None:
    missing = sorted({filename for entries in COMPOSITIONS.values() for filename, _, _ in entries if not (SOURCE / filename).exists()})
    if missing:
        raise SystemExit(f"missing OpenMoji sources: {', '.join(missing)}")
    for name, entries in COMPOSITIONS.items():
        write(name, entries)
        print(f"redrew animals / {name}: {len(entries)} anatomical source(s)")


if __name__ == "__main__":
    main()
