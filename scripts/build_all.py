#!/usr/bin/env python3
"""Build the Emojinq treatment for every OpenMoji Black SVG input."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
import unicodedata
from pathlib import Path

from collapse_lines import collapse
from import_noto_svg import convert
import xml.etree.ElementTree as ET

CODEPOINTS = re.compile(r"^(?:emoji_u)?([0-9a-f]+(?:[_-][0-9a-f]+)*)\.svg$", re.IGNORECASE)


def group_for(codepoints: list[int]) -> str:
    cp = codepoints[0]
    if 0x1F1E6 <= cp <= 0x1F1FF:
        return "Flags"
    if cp in {0x23, 0x2A} or 0x30 <= cp <= 0x39:
        return "Keycaps & Digits"
    if 0x1F300 <= cp <= 0x1F5FF:
        if 0x1F32D <= cp <= 0x1F37F:
            return "Food & Drink"
        if 0x1F3A0 <= cp <= 0x1F3FF:
            return "Activities"
        if 0x1F400 <= cp <= 0x1F43F:
            return "Animals & Nature"
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


def entry(source: Path) -> dict[str, object] | None:
    match = CODEPOINTS.match(source.name)
    if not match:
        return None
    codepoints = [int(value, 16) for value in re.split(r"[_-]", match.group(1))]
    label = " ".join(
        unicodedata.name(chr(cp), "")
        for cp in codepoints
        if cp not in {0xFE0E, 0xFE0F} and cp <= 0x10FFFF
    ).title()
    return {"name": source.stem.removeprefix("emoji_u"), "label": label, "source": source.name, "codepoints": codepoints, "group": group_for(codepoints)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--mode", choices=("grayscale", "line"), default="grayscale")
    args = parser.parse_args()
    if args.output_dir is None:
        args.output_dir = Path("assets/gray-all" if args.mode == "grayscale" else "assets/line-all")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Generated directories are disposable build products. Remove only SVG
    # outputs so renamed/removed upstream glyphs cannot linger in the gallery.
    for stale in args.output_dir.glob("*.svg"):
        stale.unlink()
    entries = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        for source in sorted(args.source_dir.glob("*.svg")):
            metadata = entry(source)
            if metadata is None:
                continue
            area = temp / source.name
            target = args.output_dir / source.name
            convert(source, area, str(metadata["name"]))
            tree = ET.parse(area)
            if args.mode == "line":
                collapse(tree.getroot())
            tree.write(target, encoding="utf-8", xml_declaration=True)
            entries.append(metadata)
    (args.output_dir / "manifest.json").write_text(json.dumps(entries, indent=2) + "\n")
    print(f"built {len(entries)} Emojinq glyphs in {args.output_dir}")


if __name__ == "__main__":
    main()
