#!/usr/bin/env python3
"""Build the Emojinq treatment for every OpenMoji Black SVG input."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
import unicodedata
from pathlib import Path

from import_noto_svg import convert
from line_brush import taper
from openmoji_metadata import openmoji_labels
import xml.etree.ElementTree as ET

CODEPOINTS = re.compile(r"^(?:emoji_u)?([0-9a-f]+(?:[_-][0-9a-f]+)*)\.svg$", re.IGNORECASE)

# OpenMoji's upstream source for SQUARED NEW is an empty placeholder. Keep
# the full Unicode inventory renderable with a restrained vector fallback;
# this is a source repair, not a general per-glyph annotation mechanism.
EMPTY_FALLBACKS = {
    "1F195.svg": """<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 72 72\">
  <path fill=\"#262421\" d=\"M13 19 C13 16 16 14 19 14 H53 C56 14 59 16 59 19 V53 C59 56 56 58 53 58 H19 C16 58 13 56 13 53 Z\"/>
  <path fill=\"#f4f1e9\" d=\"M20 24 L20 47 L24 47 L24 31 L36 47 L40 47 L40 24 L36 24 L36 40 L24 24 Z\"/>
  <path fill=\"#f4f1e9\" d=\"M44 24 H54 V28 H48 V33 H53 V37 H48 V43 H54 V47 H44 Z\"/>
</svg>"""
}

# Standard source art is authored on a 72-unit card, but some upstream
# outlines deliberately touch its edge. A shared margin keeps every glyph
# safe for full-card rasterization without changing its internal geometry.
SAFE_CARD_VIEWBOX = "-6 -6 84 84"

# Keep names for newly assigned characters available even when the executing
# Python runtime ships an older Unicode database.
NAME_OVERRIDES = {
    0x1F6D8: "LANDSLIDE",
    0x1FA89: "HARP",
    0x1FA8A: "TROMBONE",
    0x1FA8E: "TREASURE CHEST",
    0x1FA8F: "SHOVEL",
    0x1FABE: "LEAFLESS TREE",
    0x1FAC6: "FINGERPRINT",
    0x1FAC8: "HAIRY CREATURE",
    0x1FACD: "ORCA",
    0x1FADC: "ROOT VEGETABLE",
    0x1FADF: "SPLATTER",
    0x1FAE9: "FACE WITH BAGS UNDER EYES",
    0x1FAEA: "DISTORTED FACE",
    0x1FAEF: "FIGHT CLOUD",
}


def group_for(codepoints: list[int]) -> str:
    cp = codepoints[0]
    if 0x1F1E6 <= cp <= 0x1F1FF:
        return "Flags"
    if cp in {0x23, 0x2A} or 0x30 <= cp <= 0x39:
        return "Keycaps & Digits"
    if 0x1F300 <= cp <= 0x1F5FF:
        if 0x1F32D <= cp <= 0x1F330 or 0x1F344 <= cp <= 0x1F37F:
            return "Food & Drink"
        if 0x1F331 <= cp <= 0x1F343 or 0x1F400 <= cp <= 0x1F43F:
            return "Animals & Nature"
        if 0x1F3A0 <= cp <= 0x1F3FF:
            return "Activities"
        return "People & Objects"
    if 0x1F600 <= cp <= 0x1F64F:
        return "Smileys & Emotion"
    if 0x1F680 <= cp <= 0x1F6FF:
        return "Travel & Places"
    if 0x1F900 <= cp <= 0x1FAFF:
        return "People & Objects"
    if 0x2300 <= cp <= 0x27BF:
        return "Symbols"
    return "Other"


def entry(source: Path, extra_labels: dict[str, str]) -> dict[str, object] | None:
    match = CODEPOINTS.match(source.name)
    if not match:
        return None
    codepoints = [int(value, 16) for value in re.split(r"[_-]", match.group(1))]
    label = " ".join(
        NAME_OVERRIDES.get(cp, unicodedata.name(chr(cp), ""))
        for cp in codepoints
        if cp not in {0xFE0E, 0xFE0F} and cp <= 0x10FFFF
    ).title()
    if not label:
        label = extra_labels.get(source.name.upper(), "")
    return {"name": source.stem.removeprefix("emoji_u"), "label": label, "source": source.name, "codepoints": codepoints, "group": group_for(codepoints)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--index", type=Path, default=Path(".cache/openmoji/index-list.html"))
    # Stroke-only sumi-e is the canonical production path. Keep the older
    # grayscale importer available for deliberate legacy experiments, but do
    # not let an omitted flag silently recreate filled emoji art.
    parser.add_argument("--mode", choices=("line", "grayscale"), default="line")
    args = parser.parse_args()
    if args.output_dir is None:
        args.output_dir = Path("assets/gray-all" if args.mode == "grayscale" else "assets/line-all")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Generated directories are disposable build products. Remove only SVG
    # outputs so renamed/removed upstream glyphs cannot linger in the gallery.
    for stale in args.output_dir.glob("*.svg"):
        stale.unlink()
    extra_labels = openmoji_labels(args.index)
    entries = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        for source in sorted(args.source_dir.glob("*.svg")):
            metadata = entry(source, extra_labels)
            if metadata is None:
                continue
            area = temp / source.name
            target = args.output_dir / source.name
            if source.name in EMPTY_FALLBACKS:
                area.write_text(EMPTY_FALLBACKS[source.name])
            if args.mode == "line":
                # Use OpenMoji's vector line anatomy directly, then apply a
                # loaded-middle pressure curve. Converting filled grayscale
                # art first loses tiny semantic marks and can create doubled
                # contours, especially around eyes and enclosed details.
                tree = ET.parse(area if source.name in EMPTY_FALLBACKS else source)
                taper(tree.getroot())
            else:
                if source.name not in EMPTY_FALLBACKS:
                    convert(source, area, str(metadata["name"]))
                else:
                    # Run the same normalization and metadata decoration used
                    # by imported source art for the empty fallback.
                    convert(area, area, str(metadata["name"]))
                tree = ET.parse(area)
            tree.getroot().set("viewBox", SAFE_CARD_VIEWBOX)
            if metadata["label"]:
                tree.getroot().set("role", "img")
                tree.getroot().set("aria-label", str(metadata["label"]))
            tree.write(target, encoding="utf-8", xml_declaration=True)
            root = tree.getroot()
            metadata["brushed"] = (
                root.get("data-ink-stroke-system") == "tapered-v1"
                and root.get("data-ink-coverage", "complete") == "complete"
            )
            entries.append(metadata)
    (args.output_dir / "manifest.json").write_text(json.dumps(entries, indent=2) + "\n")
    print(f"built {len(entries)} Emojinq glyphs in {args.output_dir}")


if __name__ == "__main__":
    main()
