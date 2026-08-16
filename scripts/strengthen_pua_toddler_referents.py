#!/usr/bin/env python3
"""Strengthen reviewed physical PUA referents as object-scale candidates."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "pua"
MANIFEST = ASSETS / "manifest.json"
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"
CONCRETE_TRACKS = {"concrete", "referent"}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    developmental = json.loads(DEVELOPMENTAL.read_text(encoding="utf-8"))
    tracks = {
        entry["source"]: entry["track"]
        for entry in developmental["entries"]
        if entry.get("family") == "pua"
    }
    selected = [entry for entry in manifest if tracks.get(entry["source"]) in CONCRETE_TRACKS]
    if not selected:
        raise SystemExit("PUA taxonomy selected no object-scale referent candidates")
    selected_sources = {entry["source"] for entry in selected}
    for entry in manifest:
        path = ASSETS / entry["source"]
        tree = ET.parse(path)
        root = tree.getroot()
        if root.get("data-toddler-review") == "pua-concrete-referents-complete-v1":
            del root.attrib["data-toddler-review"]
        if entry["source"] not in selected_sources:
            root.attrib.pop("data-object-scale-candidate", None)
            tree.write(path, encoding="utf-8", xml_declaration=True)
            continue
        root.set("role", "img")
        root.set("aria-label", entry["label"].replace("/", " / ").replace("_", " "))
        root.set("data-object-scale-candidate", "pua-object-scale-candidate-v2")
        root.set(
            "data-naturalist-construction",
            root.get("data-naturalist-construction", "toddler-pua-referent-anatomy-v1"),
        )
        canonical_strength = bool(root.get("data-pua-familiar-source"))
        mark_index = 0
        for element in root.iter():
            if element.get("data-ink-role") != "line-source-tapered":
                continue
            original = float(element.get("data-pua-toddler-source-width", element.get("stroke-width", "1")))
            element.set("data-pua-toddler-source-width", f"{original:.2f}")
            if canonical_strength:
                # The canonical source has already passed its standard-emoji
                # toddler strengthening pass. Applying the PUA multiplier a
                # second time destroys the active white space.
                element.set("data-toddler-clarity", "canonical-referent-anatomy-v1")
                continue
            multiplier, tone, brush_pass = (
                (2.20, "#302e2a", "loaded-contour-v2"),
                (2.40, "#262421", "loaded-contour-v2"),
                (1.80, "#66635b", "dry-edge-v2"),
            )[mark_index % 3]
            element.set("stroke-width", f"{max(1.34, original * multiplier):.2f}")
            element.set("stroke", tone)
            element.set("data-ink-brush-pass", brush_pass)
            element.set("data-toddler-clarity", "defining-pua-referent-anatomy-v1")
            mark_index += 1
        tree.write(path, encoding="utf-8", xml_declaration=True)
    print(f"strengthened {len(selected)} reviewed PUA referent candidates for object-scale recognition")


if __name__ == "__main__":
    main()
