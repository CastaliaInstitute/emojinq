#!/usr/bin/env python3
"""Give familiar concrete PUA nouns the canonical sumi-e emoji anatomy."""

from __future__ import annotations

import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from pua_familiar_referents import FAMILIAR_REFERENTS


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "assets" / "gray-all"
PUA = ROOT / "assets" / "pua"
MANIFEST = PUA / "manifest.json"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def main() -> None:
    pua_entries = {entry["source"]: entry for entry in json.loads(MANIFEST.read_text(encoding="utf-8"))}
    standard_entries = {
        entry["source"]: entry
        for entry in json.loads((STANDARD / "manifest.json").read_text(encoding="utf-8"))
    }
    failures: list[str] = []
    for pua_source, standard_source in FAMILIAR_REFERENTS.items():
        if pua_source not in pua_entries:
            failures.append(f"missing PUA manifest entry: {pua_source}")
        if standard_source not in standard_entries:
            failures.append(f"missing standard source: {standard_source}")
        if not (STANDARD / standard_source).exists():
            failures.append(f"missing standard SVG: {standard_source}")
    if failures:
        raise SystemExit("\n".join(failures))

    for pua_source, standard_source in FAMILIAR_REFERENTS.items():
        target = PUA / pua_source
        old_root = ET.parse(target).getroot()
        codepoint = old_root.get("data-pua")
        if not codepoint:
            raise SystemExit(f"{target}: missing data-pua code point")

        source_root = ET.parse(STANDARD / standard_source).getroot()
        new_root = copy.deepcopy(source_root)
        label = pua_entries[pua_source]["label"].replace("/", " / ").replace("_", " ")
        new_root.attrib.pop("id", None)
        # PUA cards and font import use the fixed 72-unit design square.  The
        # standard gallery adds a six-unit browser preview margin, but its
        # actual anatomy remains within this design square.
        new_root.set("viewBox", "0 0 72 72")
        new_root.set("role", "img")
        new_root.set("aria-label", label)
        new_root.set("data-pua", codepoint)
        new_root.set("data-pua-familiar-source", standard_source.removesuffix(".svg"))
        new_root.set("data-naturalist-construction", "canonical-emoji-anatomy-transplant-v1")
        new_root.set("data-referent-review", "familiar-silhouette-v1")
        new_root.set("data-intentional-components", "canonical-emoji-anatomy-v1")
        if pua_source == "locations/theater.svg":
            # Comedy and tragedy are two intentionally separate masks, not a
            # stray raster fragment.  Keep that distinction explicit for the
            # detached-component audit.
            new_root.set("data-intentional-components", "paired-theater-masks-v1")
        title = next((node for node in new_root if local(node.tag) == "title"), None)
        if title is None:
            title = ET.Element(f"{{{NS}}}title")
            new_root.insert(0, title)
        title.text = (
            f"{label} — familiar {standard_entries[standard_source]['label']} "
            "sumi-e anatomy"
        )
        ET.ElementTree(new_root).write(target, encoding="utf-8", xml_declaration=True)

    print(f"transplanted {len(FAMILIAR_REFERENTS)} familiar PUA referent silhouettes")


if __name__ == "__main__":
    main()
