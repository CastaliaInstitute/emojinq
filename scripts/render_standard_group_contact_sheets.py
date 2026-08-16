#!/usr/bin/env python3
"""Render paged standard-Unicode contact sheets for semantic visual review."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", action="append", required=True)
    parser.add_argument("--variant", choices=("ink", "color"), default="ink")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--size", type=int, default=48)
    parser.add_argument("--per-page", type=int, default=120)
    args = parser.parse_args()

    asset_root = Path("assets/color-all" if args.variant == "color" else "assets/gray-all")
    entries = [
        entry
        for entry in json.loads((asset_root / "manifest.json").read_text(encoding="utf-8"))
        if entry.get("group") in set(args.group)
    ]
    entries.sort(key=lambda entry: (entry.get("group", ""), entry["source"]))
    args.output.mkdir(parents=True, exist_ok=True)
    label_font = ImageFont.load_default()
    columns = 10
    cell_width, cell_height = args.size + 40, args.size + 34

    with tempfile.TemporaryDirectory(prefix="emojinq-standard-contact-") as directory:
        raster_root = Path(directory)
        for page_index, offset in enumerate(range(0, len(entries), args.per_page), start=1):
            selected = entries[offset:offset + args.per_page]
            rows = (len(selected) + columns - 1) // columns
            sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "#d6d3ca")
            for index, entry in enumerate(selected):
                png = raster_root / f"{offset + index}.png"
                subprocess.run(
                    ["rsvg-convert", "-w", str(args.size), "-h", str(args.size), "-o", str(png), str(asset_root / entry["source"])],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                glyph = Image.open(png).convert("RGBA")
                cell = Image.new("RGB", (cell_width, cell_height), "#f6f2e8")
                cell.paste(glyph, ((cell_width - args.size) // 2, 0), glyph)
                draw = ImageDraw.Draw(cell)
                draw.text((3, args.size + 3), Path(entry["source"]).stem[:14], fill="#262522", font=label_font)
                draw.text((3, args.size + 14), entry.get("label", "")[:18], fill="#66635b", font=label_font)
                sheet.paste(cell, ((index % columns) * cell_width, (index // columns) * cell_height))
            target = args.output / f"standard-{args.variant}-{page_index:02d}.png"
            sheet.save(target)
            print(f"rendered {len(selected)} glyphs: {target}")


if __name__ == "__main__":
    main()
