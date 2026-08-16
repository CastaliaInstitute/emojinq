#!/usr/bin/env python3
"""Strengthen all standard Travel & Places glyphs at toddler scale."""

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
    if path.name == "1F6D8.svg":
        root.set("aria-label", "Landslide")
    root.set("data-naturalist-construction", "toddler-travel-mechanical-anatomy-v1")
    root.set("data-toddler-review", "travel-places-complete-v1")
    mark_index = 0
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        original = float(element.get("data-travel-source-width", element.get("stroke-width", "1")))
        element.set("data-travel-source-width", f"{original:.2f}")
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
        element.set("data-toddler-clarity", "defining-travel-mechanical-anatomy-v1")
        mark_index += 1
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = [entry for entry in entries if entry.get("group") == "Travel & Places"]
    if len(selected) != 202:
        raise SystemExit(f"expected 202 Travel & Places glyphs, found {len(selected)}")
    for entry in selected:
        strengthen(ASSETS / entry["source"])
    print("strengthened all 202 standard Travel & Places glyphs for 32px recognition")


if __name__ == "__main__":
    main()
