#!/usr/bin/env python3
"""Strengthen and semantically name every standard glyph outside prior category gates."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from openmoji_metadata import openmoji_labels


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "gray-all"
MANIFEST = ASSETS / "manifest.json"
INDEX = ROOT / ".cache" / "openmoji" / "index-list.html"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

REVIEWED = {
    "Smileys & Emotion": (197, "smileys-emotion-complete-v1", "toddler-facial-expression-anatomy-v1"),
    "Symbols": (219, "symbols-complete-v1", "toddler-symbol-object-anatomy-v1"),
    "Keycaps & Digits": (12, "keycaps-digits-complete-v1", "toddler-keycap-legibility-v1"),
    "Other": (492, "other-complete-v1", "toddler-openmoji-extra-anatomy-v1"),
}
QUEER_FLAGS = {f"E{code:X}.svg" for code in range(0x420, 0x436)}


def add_flag_cues(root: ET.Element) -> None:
    if any(element.get("id") == "extra-flag-recognition-cues" for element in root.iter()):
        return
    group = ET.SubElement(root, f"{{{NS}}}g", {"id": "extra-flag-recognition-cues"})
    shared = {
        "class": "ink-stroke",
        "data-ink-stroke": "tapered",
        "data-ink-role": "line-source-tapered",
        "pathLength": "1",
        "fill": "none",
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "data-remaining-standard-source-width": "1.00",
        "data-ink-brush-pass": "loaded-contour-v2",
        "data-toddler-clarity": "defining-extra-flag-cloth-anatomy-v1",
    }
    ET.SubElement(group, f"{{{NS}}}path", {**shared, "d": "M 5 10 L 5 64", "stroke": "#262421", "stroke-width": "2.55"})
    ET.SubElement(group, f"{{{NS}}}circle", {**shared, "cx": "5", "cy": "8", "r": "2.1", "stroke": "#302e2a", "stroke-width": "1.75"})
    ET.SubElement(
        group,
        f"{{{NS}}}path",
        {
            **shared,
            "d": "M 10 27 C 23 23 36 29 50 25 M 10 45 C 24 41 39 47 55 43",
            "stroke": "#66635b",
            "stroke-width": "1.46",
            "data-ink-brush-pass": "dry-edge-v2",
        },
    )


def strengthen(path: Path, label: str, review: str, construction: str) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    root.set("role", "img")
    root.set("aria-label", label)
    root.set("data-naturalist-construction", construction)
    root.set("data-toddler-review", review)
    mark_index = 0
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        element.set("pathLength", "1")
        original = float(element.get("data-remaining-standard-source-width", element.get("stroke-width", "1")))
        element.set("data-remaining-standard-source-width", f"{original:.2f}")
        multiplier, tone, brush_pass = (
            (2.25, "#302e2a", "loaded-contour-v2"),
            (2.45, "#262421", "loaded-contour-v2"),
            (1.85, "#66635b", "dry-edge-v2"),
        )[mark_index % 3]
        element.set("stroke-width", f"{max(1.34, original * multiplier):.2f}")
        element.set("stroke", tone)
        element.set("data-ink-brush-pass", brush_pass)
        element.set("data-toddler-clarity", "defining-remaining-standard-mark-v1")
        mark_index += 1
    if path.name in QUEER_FLAGS:
        add_flag_cues(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    labels = openmoji_labels(INDEX)
    for group, (expected, review, construction) in REVIEWED.items():
        selected = [entry for entry in entries if entry.get("group") == group]
        if len(selected) != expected:
            raise SystemExit(f"expected {expected} {group} glyphs, found {len(selected)}")
        for entry in selected:
            if not entry.get("label"):
                entry["label"] = labels.get(entry["source"].upper(), "")
            if not entry.get("label"):
                raise SystemExit(f"missing semantic identity for {entry['source']}")
            strengthen(ASSETS / entry["source"], str(entry["label"]), review, construction)
    MANIFEST.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print("strengthened and named all 920 remaining standard glyphs for 32px recognition")


if __name__ == "__main__":
    main()
