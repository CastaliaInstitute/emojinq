#!/usr/bin/env python3
"""Strengthen all standard Flags glyphs at toddler scale."""

from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "gray-all"
MANIFEST = ASSETS / "manifest.json"
OPENMOJI_INDEX = ROOT / ".cache" / "openmoji" / "index-list.html"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

FLAG_LABEL = re.compile(
    r"<td>(1F1[0-9A-F]{2}-1F1[0-9A-F]{2})</td>\s*"
    r"<td>flags</td>\s*<td>[^<]+</td>\s*<td>(flag:[^<]+)</td>"
)


def flag_labels() -> dict[str, str]:
    if not OPENMOJI_INDEX.exists():
        raise SystemExit(f"OpenMoji metadata is required: {OPENMOJI_INDEX}")
    text = OPENMOJI_INDEX.read_text(encoding="utf-8")
    labels = {
        f"{code}.svg": html.unescape(label).replace("flag:", "Flag:", 1)
        for code, label in FLAG_LABEL.findall(text)
    }
    if len(labels) != 259:
        raise SystemExit(f"expected 259 OpenMoji flag labels, found {len(labels)}")
    return labels


def strengthen(path: Path, label: str | None) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    if label:
        root.set("aria-label", label)
    root.set("data-naturalist-construction", "toddler-flag-cloth-anatomy-v1")
    root.set("data-toddler-review", "flags-complete-v1")
    mark_index = 0
    for element in root.iter():
        if element.get("data-ink-role") != "line-source-tapered":
            continue
        element.set("pathLength", "1")
        original = float(element.get("data-flag-source-width", element.get("stroke-width", "1")))
        element.set("data-flag-source-width", f"{original:.2f}")
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
        element.set("data-toddler-clarity", "defining-flag-cloth-anatomy-v1")
        mark_index += 1
    if "-" in path.stem and not any(
        element.get("id") == "standard-flag-recognition-cues" for element in root.iter()
    ):
        group = ET.SubElement(root, f"{{{NS}}}g", {"id": "standard-flag-recognition-cues"})
        shared = {
            "class": "ink-stroke",
            "data-ink-stroke": "tapered",
            "data-ink-role": "line-source-tapered",
            "pathLength": "1",
            "fill": "none",
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
        }
        ET.SubElement(
            group,
            f"{{{NS}}}path",
            {
                **shared,
                "d": "M 5 13 L 5 64",
                "stroke": "#262421",
                "stroke-width": "2.45",
                "data-flag-source-width": "1.00",
                "data-ink-brush-pass": "loaded-contour-v2",
                "data-toddler-clarity": "defining-flag-pole-v1",
            },
        )
        ET.SubElement(
            group,
            f"{{{NS}}}circle",
            {
                **shared,
                "cx": "5",
                "cy": "10",
                "r": "2.2",
                "stroke": "#302e2a",
                "stroke-width": "1.80",
                "data-flag-source-width": "0.80",
                "data-ink-brush-pass": "loaded-contour-v2",
                "data-toddler-clarity": "defining-flag-finial-v1",
            },
        )
        ET.SubElement(
            group,
            f"{{{NS}}}path",
            {
                **shared,
                "d": "M 10 25 C 21 21 30 27 41 23 M 10 47 C 22 43 33 49 45 45",
                "stroke": "#66635b",
                "stroke-width": "1.50",
                "data-flag-source-width": "0.80",
                "data-ink-brush-pass": "dry-edge-v2",
                "data-toddler-clarity": "defining-flag-cloth-folds-v1",
            },
        )
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = [entry for entry in entries if entry.get("group") == "Flags"]
    if len(selected) != 285:
        raise SystemExit(f"expected 285 Flags glyphs, found {len(selected)}")
    labels = flag_labels()
    for entry in selected:
        label = labels.get(entry["source"])
        if "-" in Path(entry["source"]).stem and not label:
            raise SystemExit(f"missing flag identity for {entry['source']}")
        if label:
            entry["label"] = label
        strengthen(ASSETS / entry["source"], label)
    MANIFEST.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print("strengthened all 285 standard Flags glyphs; named 259 composed flags")


if __name__ == "__main__":
    main()
