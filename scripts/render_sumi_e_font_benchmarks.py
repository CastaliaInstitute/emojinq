#!/usr/bin/env python3
"""Render the book-derived cross-category benchmark directly from the TTF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BENCHMARK_CATEGORIES = {"adventure", "animals", "body", "brc", "castalia", "cave_locations", "cosmos", "dinosaurs", "faerie", "farm", "flora", "herbs", "locations", "materials", "patterns", "plants", "rockets", "sea_creatures", "weather_sky"}
OBJECT_STUDIES = {
    f"objects/{path.name}"
    for path in Path("assets/pua/objects").glob("*.svg")
    if "sumi-e-naturalist-v2" in path.read_text()
}
PEOPLE_STUDIES = {
    f"people/{path.name}"
    for path in Path("assets/pua/people").glob("*.svg")
    if "sumi-e-naturalist-v2" in path.read_text()
}
SCIENCE_STUDIES = {
    f"science/{path.name}"
    for path in Path("assets/pua/science").glob("*.svg")
    if "sumi-e-naturalist-v2" in path.read_text()
}
BENCHMARK_STUDIES = {
    *OBJECT_STUDIES,
    *SCIENCE_STUDIES,
    *PEOPLE_STUDIES,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=Path("fonts/Emojinq-Regular.ttf"))
    parser.add_argument("--manifest", type=Path, default=Path("assets/pua/manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("build/sumi-e-benchmark/font.jpg"))
    parser.add_argument("--size", type=int, default=128)
    args = parser.parse_args()

    entries = [
        entry for entry in json.loads(args.manifest.read_text())
        if (
            entry["source"].split("/", 1)[0] in BENCHMARK_CATEGORIES
            or entry["source"] in BENCHMARK_STUDIES
        ) and len(entry["codepoints"]) == 1
    ]
    entries.sort(key=lambda entry: entry["source"])
    columns = 6
    cell_w, cell_h = 192, 178
    rows = (len(entries) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "#d6d3ca")
    glyph_font = ImageFont.truetype(str(args.font), args.size)
    label_font = ImageFont.load_default()
    for index, entry in enumerate(entries):
        cell = Image.new("RGB", (cell_w, cell_h), "#f6f2e8")
        draw = ImageDraw.Draw(cell)
        character = chr(entry["codepoints"][0])
        bbox = draw.textbbox((0, 0), character, font=glyph_font)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (cell_w - width) / 2 - bbox[0]
        y = (136 - height) / 2 - bbox[1]
        draw.text((x, y), character, fill="#262522", font=glyph_font)
        draw.text((6, 151), Path(entry["source"]).stem[:24], fill="#262522", font=label_font)
        sheet.paste(cell, ((index % columns) * cell_w, (index // columns) * cell_h))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output, quality=92)
    print(f"rendered {len(entries)} compiled sumi-e benchmarks: {args.output}")


if __name__ == "__main__":
    main()
