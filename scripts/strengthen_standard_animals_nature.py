#!/usr/bin/env python3
"""Strengthen all standard Animals & Nature glyphs for toddler recognition."""

from __future__ import annotations

import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import SHAPES, taper


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "gray-all"
MANIFEST = ASSETS / "manifest.json"
OPENMOJI = ROOT / ".cache" / "openmoji" / "black" / "svg"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

FACE_SOURCES = {
    "1F42D.svg",  # mouse
    "1F42E.svg",  # cow
    "1F42F.svg",  # tiger
    "1F430.svg",  # rabbit
    "1F431.svg",  # cat
    "1F432.svg",  # dragon
    "1F434.svg",  # horse
    "1F435.svg",  # monkey
    "1F436.svg",  # dog
    "1F437.svg",  # pig
    "1F438.svg",  # frog
    "1F439.svg",  # hamster
    "1F43A.svg",  # wolf
    "1F43B.svg",  # bear
    "1F43C.svg",  # panda
}

CUES: dict[str, list[tuple[str, str, float]]] = {
    "1F33D.svg": [
        ("M 16,16 L 31,31 M 14,21 L 27,34", "#302e2a", 1.55),
        ("M 17,25 L 25,17 M 21,30 L 30,21 M 26,34 L 34,26", "#66635b", 1.30),
    ],
    "1F33E.svg": [
        ("M 47,13 C 42,26 42,44 48,58", "#302e2a", 2.00),
        ("M 44,22 L 39,18 M 43,29 L 38,26 M 43,36 L 38,34 M 44,43 L 39,42 M 45,50 L 40,50", "#66635b", 1.35),
    ],
    "1F40B.svg": [
        ("M 25,27 C 27,25 29,26 29,29 C 27,30 25,29 25,27", "#262421", 1.55),
        ("M 31,20 C 28,15 24,13 21,16 M 32,20 C 35,15 39,14 42,17", "#66635b", 1.55),
    ],
    "1F41A.svg": [
        ("M 35,45 C 29,42 29,34 34,30 C 40,26 46,31 44,38 C 42,45 34,47 31,42 C 29,38 33,34 37,35", "#302e2a", 1.90),
        ("M 27,23 L 22,47 M 34,21 L 31,51 M 41,22 L 40,48", "#66635b", 1.35),
    ],
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def restore_front_face(path: Path, label: str) -> None:
    """Restore OpenMoji's readable front-facing species anatomy."""
    source = OPENMOJI / path.name.lower()
    if not source.exists():
        raise SystemExit(f"missing OpenMoji animal-face source: {source}")
    source_root = ET.parse(source).getroot()
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": label,
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-coverage": "complete",
        "data-ink-pressure": "loaded-middle-v1",
        "data-animal-face-source": "openmoji-front-anatomy-v1",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = f"{label} — front-facing species brush study"
    group = ET.SubElement(root, f"{{{NS}}}g", {
        "id": "animal-face-anatomy",
        "fill": "none",
        "stroke": "#262421",
        "stroke-width": "2",
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
    })
    for element in source_root.iter():
        if local(element.tag) not in SHAPES:
            continue
        item = copy.deepcopy(element)
        item.set("fill", "none")
        item.set("stroke", "#262421")
        item.set("stroke-width", "2")
        item.set("stroke-linecap", "round")
        item.set("stroke-linejoin", "round")
        group.append(item)
    taper(root)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def strengthen(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    root.set("data-naturalist-construction", "toddler-animal-botanical-anatomy-v1")
    root.set("data-toddler-review", "animals-nature-complete-v1")
    mark_index = 0
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        original = float(element.get("data-animal-source-width", element.get("stroke-width", "1")))
        element.set("data-animal-source-width", f"{original:.2f}")
        phase = mark_index % 3
        if phase == 0:
            width = original * 2.20
            element.set("stroke", "#302e2a")
            brush_pass = "loaded-contour-v2"
        elif phase == 1:
            width = original * 2.40
            element.set("stroke", "#262421")
            brush_pass = "loaded-contour-v2"
        else:
            width = original * 1.80
            element.set("stroke", "#66635b")
            brush_pass = "dry-edge-v2"
        element.set("stroke-width", f"{max(1.28, width):.2f}")
        element.set("data-ink-brush-pass", brush_pass)
        element.set("data-toddler-clarity", "defining-animal-botanical-anatomy-v1")
        mark_index += 1

    for parent in root.iter():
        for child in list(parent):
            if child.get("id") == "animal-recognition-cues":
                parent.remove(child)
    cues = CUES.get(path.name)
    if cues:
        group = ET.SubElement(root, f"{{{NS}}}g", {
            "id": "animal-recognition-cues",
            "fill": "none",
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
            "data-toddler-clarity": "defining-animal-botanical-cues-v1",
        })
        for index, (drawing, color, width) in enumerate(cues):
            ET.SubElement(group, f"{{{NS}}}path", {
                "class": "ink-stroke",
                "d": drawing,
                "fill": "none",
                "stroke": color,
                "stroke-width": f"{width:.2f}",
                "pathLength": "1",
                "data-ink-stroke": "tapered",
                "data-ink-role": "recognition-cue",
                "data-ink-index": f"animal-cue-{index}",
                "data-ink-brush-pass": "loaded-contour-v2" if width >= 1.8 else "dry-edge-v2",
            })
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = [entry for entry in entries if entry.get("group") == "Animals & Nature"]
    if len(selected) != 89:
        raise SystemExit(f"expected 89 Animals & Nature glyphs, found {len(selected)}")
    for entry in selected:
        path = ASSETS / entry["source"]
        if path.name in FACE_SOURCES:
            restore_front_face(path, str(entry["label"]))
        strengthen(path)
    print("strengthened all 89 standard Animals & Nature glyphs for 32px recognition")


if __name__ == "__main__":
    main()
