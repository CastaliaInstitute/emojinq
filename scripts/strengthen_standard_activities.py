#!/usr/bin/env python3
"""Strengthen all standard Activities glyphs at toddler scale."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "gray-all"
MANIFEST = ASSETS / "manifest.json"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def strengthen(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    root.set("data-naturalist-construction", "toddler-activity-equipment-anatomy-v1")
    root.set("data-toddler-review", "activities-complete-v1")
    mark_index = 0
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        element.set("pathLength", "1")
        original = float(element.get("data-activity-source-width", element.get("stroke-width", "1")))
        element.set("data-activity-source-width", f"{original:.2f}")
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
        element.set("data-toddler-clarity", "defining-activity-equipment-anatomy-v1")
        mark_index += 1
    if path.name.startswith(("1F3F3-", "1F3F4-")) and not any(
        element.get("id") == "activity-flag-recognition-cues" for element in root.iter()
    ):
        group = ET.SubElement(root, f"{{{NS}}}g", {"id": "activity-flag-recognition-cues"})
        shared = {
            "class": "ink-stroke",
            "data-ink-stroke": "tapered",
            "data-ink-role": "line-source-tapered",
            "pathLength": "1",
            "fill": "none",
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
            "data-ink-brush-pass": "loaded-contour-v2",
            "data-toddler-clarity": "defining-flag-pole-and-finial-v1",
        }
        ET.SubElement(
            group,
            f"{{{NS}}}path",
            {
                **shared,
                "d": "M 6 14 L 6 63",
                "stroke": "#262421",
                "stroke-width": "2.40",
                "data-activity-source-width": "1.00",
            },
        )
        ET.SubElement(
            group,
            f"{{{NS}}}circle",
            {
                **shared,
                "cx": "6",
                "cy": "11",
                "r": "2.2",
                "stroke": "#302e2a",
                "stroke-width": "1.76",
                "data-activity-source-width": "0.80",
            },
        )
        ET.SubElement(
            group,
            f"{{{NS}}}path",
            {
                **shared,
                "d": "M 10 24 C 20 20 27 26 37 22 M 10 47 C 22 43 31 49 43 45",
                "stroke": "#66635b",
                "stroke-width": "1.44",
                "data-activity-source-width": "0.80",
                "data-ink-brush-pass": "dry-edge-v2",
            },
        )
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = [entry for entry in entries if entry.get("group") == "Activities"]
    if len(selected) != 266:
        raise SystemExit(f"expected 266 Activities glyphs, found {len(selected)}")
    for entry in selected:
        strengthen(ASSETS / entry["source"])
    print("strengthened all 266 standard Activities glyphs for 32px recognition")


if __name__ == "__main__":
    main()
