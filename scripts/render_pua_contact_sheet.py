#!/usr/bin/env python3
"""Render one contact sheet per PUA category for visual review."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    parser.add_argument("--output", type=Path, default=Path("build/pua-contact-sheets"))
    parser.add_argument("--size", type=int, default=128)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()

    categories = sorted(path for path in args.root.iterdir() if path.is_dir() and path.name != "references")
    for category in categories:
        files = sorted(category.glob("*.svg"))
        if not files:
            continue
        cells = []
        with tempfile.TemporaryDirectory() as temp_dir:
            for index, svg in enumerate(files):
                png = Path(temp_dir) / f"{index}.png"
                subprocess.run(["rsvg-convert", "-w", str(args.size), "-h", str(args.size), "-o", str(png), str(svg)], check=True)
                source = Image.open(png).convert("RGBA")
                cell = Image.new("RGB", (args.size + 32, args.size + 36), (246, 242, 232))
                cell.paste(source, (16, 0), source)
                ImageDraw.Draw(cell).text((4, args.size + 6), svg.stem[:20], fill=(38, 37, 34), font=font)
                cells.append(cell)
        columns = 6
        cell_w, cell_h = args.size + 32, args.size + 36
        rows = (len(cells) + columns - 1) // columns
        sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), (214, 211, 202))
        for index, cell in enumerate(cells):
            sheet.paste(cell, ((index % columns) * cell_w, (index // columns) * cell_h))
        sheet.save(args.output / f"{category.name}.jpg", quality=90)
        print(f"rendered {category.name}: {len(files)} glyphs")


if __name__ == "__main__":
    main()
