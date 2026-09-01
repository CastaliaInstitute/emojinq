#!/usr/bin/env python3
"""Build familiar sea-creature silhouettes with tapered sumi-e linework."""

from __future__ import annotations

import copy
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import SHAPES, taper


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".cache/openmoji/black/svg"
OUTPUT = ROOT / "assets/pua/sea_creatures"
MANIFEST = json.loads((ROOT / "assets/pua/manifest.json").read_text(encoding="utf-8"))
PUA_BY_LABEL = {item["label"]: item["codepoints"][0] for item in MANIFEST}
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def source_path(filename: str) -> Path:
    value = Path(filename)
    if value.parts and value.parts[0] == "build":
        return ROOT / value
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
    "manta": "build/noun-derived/manta.svg",
    "seahorse": None,
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def codepoint_attr(name: str, existing: ET.Element) -> str:
    value = PUA_BY_LABEL.get(f"sea_creatures/{name}")
    if value is not None:
        return f'data-pua="U+{value:X}"'
    match = re.search(r'data-pua="([^"]+)"', ET.tostring(existing, encoding="unicode"))
    if match:
        return match.group(0)
    raise SystemExit(f"missing PUA code point in sea_creatures/{name}.svg")


def redraw(name: str, filename: str) -> None:
    target = OUTPUT / f"{name}.svg"
    existing = ET.parse(target).getroot()
    source = ET.parse(source_path(filename)).getroot() if filename else existing
    provenance = {
        key: existing.get(key)
        for key in (
            "data-reference-source",
            "data-reference-record",
            "data-license-status",
            "data-source-reference",
        )
        if existing.get(key)
    }
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": f"sea_creatures / {name}",
        "data-pua": codepoint_attr(name, existing).split('"', 2)[1],
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-naturalist-construction": "toddler-anatomy-v1",
        "data-object-scale-candidate": "pua-object-scale-candidate-v2",
        "data-intentional-components": "semantic-multipart-v1",
        "data-component-review": "severity-contact-sheet-2026-08-v1",
        **provenance,
    })
    ET.SubElement(root, f"{{{NS}}}title").text = (
        f"sea_creatures / {name} — toddler-readable anatomical sumi-e study"
    )
    source_transform = next(
        (element.get("transform") for element in source.iter()
         if local(element.tag) == "g" and element.get("transform")),
        None,
    )
    if source_transform is None and filename is None:
        source_transform = next(
            (element.get("transform") for element in existing.iter()
             if local(element.tag) == "g" and element.get("transform")),
            None,
        )
    group = ET.SubElement(
        root,
        f"{{{NS}}}g",
        {"transform": source_transform or "translate(7 7) scale(.81)"},
    )
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
        print(f"redrew sea_creatures / {name} from {filename or 'existing traced source'}")


if __name__ == "__main__":
    main()
