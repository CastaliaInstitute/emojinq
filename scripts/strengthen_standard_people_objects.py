#!/usr/bin/env python3
"""Strengthen all standard People & Objects glyphs at toddler scale."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "gray-all"
MANIFEST = ASSETS / "manifest.json"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

NAME_OVERRIDES = {
    "1FA89.svg": "Harp",
    "1FA8A.svg": "Trombone",
    "1FA8E.svg": "Treasure Chest",
    "1FA8F.svg": "Shovel",
    "1FABE.svg": "Leafless Tree",
    "1FAC6.svg": "Fingerprint",
    "1FAC8.svg": "Hairy Creature",
    "1FACD.svg": "Orca",
    "1FADC.svg": "Root Vegetable",
    "1FADF.svg": "Splatter",
    "1FAE9.svg": "Face With Bags Under Eyes",
    "1FAEA.svg": "Distorted Face",
    "1FAEF.svg": "Fight Cloud",
}


def strengthen(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    if path.name in NAME_OVERRIDES:
        root.set("aria-label", NAME_OVERRIDES[path.name])
    root.set("data-naturalist-construction", "toddler-people-object-anatomy-v1")
    root.set("data-toddler-review", "people-objects-complete-v1")
    mark_index = 0
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        element.set("pathLength", "1")
        original = float(element.get("data-people-object-source-width", element.get("stroke-width", "1")))
        element.set("data-people-object-source-width", f"{original:.2f}")
        phase = mark_index % 3
        if phase == 0:
            width = original * 2.25
            element.set("stroke", "#302e2a")
            brush_pass = "loaded-contour-v2"
        elif phase == 1:
            width = original * 2.45
            element.set("stroke", "#262421")
            brush_pass = "loaded-contour-v2"
        else:
            width = original * 1.85
            element.set("stroke", "#66635b")
            brush_pass = "dry-edge-v2"
        element.set("stroke-width", f"{max(1.34, width):.2f}")
        element.set("data-ink-brush-pass", brush_pass)
        element.set("data-toddler-clarity", "defining-people-object-anatomy-v1")
        mark_index += 1
    if path.name == "1F484.svg" and not any(
        element.get("id") == "people-object-recognition-cues" for element in root.iter()
    ):
        group = ET.SubElement(root, f"{{{NS}}}g", {"id": "people-object-recognition-cues"})
        ET.SubElement(
            group,
            f"{{{NS}}}path",
            {
                "class": "ink-stroke",
                "data-ink-stroke": "tapered",
                "data-ink-role": "line-source-tapered",
                "pathLength": "1",
                "d": "M 28 19 L 45 11 M 28 39 L 45 39 M 29 49 L 44 49 M 23 66 L 50 66",
                "fill": "none",
                "stroke": "#262421",
                "stroke-width": "2.20",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
                "data-people-object-source-width": "0.90",
                "data-ink-brush-pass": "loaded-contour-v2",
                "data-toddler-clarity": "defining-lipstick-bullet-and-casing-v1",
            },
        )
    if path.name == "1FACD.svg" and not any(
        element.get("id") == "people-object-recognition-cues" for element in root.iter()
    ):
        group = ET.SubElement(root, f"{{{NS}}}g", {"id": "people-object-recognition-cues"})
        ET.SubElement(
            group,
            f"{{{NS}}}path",
            {
                "class": "ink-stroke",
                "data-ink-stroke": "tapered",
                "data-ink-role": "line-source-tapered",
                "pathLength": "1",
                "d": "M 28 25 C 38 22 50 25 58 34",
                "fill": "none",
                "stroke": "#302e2a",
                "stroke-width": "5.40",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
                "data-people-object-source-width": "1.40",
                "data-ink-brush-pass": "loaded-contour-v2",
                "data-toddler-clarity": "defining-orca-black-back-v1",
            },
        )
        ET.SubElement(
            group,
            f"{{{NS}}}path",
            {
                "class": "ink-stroke",
                "data-ink-stroke": "tapered",
                "data-ink-role": "line-source-tapered",
                "pathLength": "1",
                "d": "M 46 34 C 49 32 53 33 55 35 C 52 37 49 37 46 35 Z",
                "fill": "none",
                "stroke": "#66635b",
                "stroke-width": "1.55",
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
                "data-people-object-source-width": "0.84",
                "data-ink-brush-pass": "dry-edge-v2",
                "data-toddler-clarity": "defining-orca-eye-patch-v1",
            },
        )
    if path.name == "1FACD.svg":
        for child in list(root):
            if child.get("id") == "people-object-orca-ink-wash":
                root.remove(child)
        wash_group = ET.Element(
            f"{{{NS}}}g",
            {"id": "people-object-orca-ink-wash", "data-color-copy": "omit"},
        )
        for d, width, opacity in (
            ("M 25 29 C 36 24 49 27 57 34", "8.50", "0.58"),
            ("M 22 36 C 31 31 42 33 49 38", "5.20", "0.44"),
        ):
            ET.SubElement(
                wash_group,
                f"{{{NS}}}path",
                {
                    "class": "ink-stroke",
                    "data-ink-stroke": "tapered",
                    "data-ink-role": "recognition-brush-mass",
                    "pathLength": "1",
                    "d": d,
                    "fill": "none",
                    "stroke": "#4a4943",
                    "stroke-width": width,
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "opacity": opacity,
                    "data-ink-brush-pass": "loaded-ribbon-v2",
                    "data-toddler-clarity": "defining-orca-black-body-wash-v1",
                },
            )
        root.insert(0, wash_group)
    if path.name == "1F484.svg":
        for group in root.iter():
            if group.get("id") == "people-object-recognition-cues":
                cue = list(group)[0]
                cue.set(
                    "d",
                    "M 28 19 L 45 11 M 28 39 L 45 39 M 29 49 L 44 49 M 23 66 L 50 66",
                )
                cue.set("data-toddler-clarity", "defining-lipstick-bullet-and-casing-v1")
    if path.name == "1FACD.svg":
        for group in root.iter():
            if group.get("id") == "people-object-recognition-cues":
                back, patch = list(group)
                back.set("stroke-width", "5.40")
                back.set("data-toddler-clarity", "defining-orca-black-back-v1")
                patch.set("stroke", "#bcb9af")
                patch.set("stroke-width", "3.20")
                patch.set("data-toddler-clarity", "defining-orca-eye-patch-v1")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = [entry for entry in entries if entry.get("group") == "People & Objects"]
    if len(selected) != 2667:
        raise SystemExit(f"expected 2667 People & Objects glyphs, found {len(selected)}")
    for entry in selected:
        if entry["source"] in NAME_OVERRIDES:
            entry["label"] = NAME_OVERRIDES[entry["source"]]
        strengthen(ASSETS / entry["source"])
    MANIFEST.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print("strengthened all 2667 standard People & Objects glyphs for 32px recognition")


if __name__ == "__main__":
    main()
