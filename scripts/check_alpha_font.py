#!/usr/bin/env python3
"""Verify that the compiled TTF renders every ASCII glyph visibly."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=Path)
    parser.add_argument("--size", type=int, default=128)
    args = parser.parse_args()
    font = ImageFont.truetype(str(args.font), args.size)
    ttf = TTFont(args.font)
    cmap = ttf.getBestCmap() or {}
    failures: list[str] = []
    checked = 0
    for codepoint in range(32, 127):
        character = chr(codepoint)
        glyph_name = cmap.get(codepoint)
        if glyph_name is None:
            failures.append(f"U+{codepoint:04X}: missing cmap entry")
            continue
        if codepoint == 32:
            continue
        image = Image.new("L", (args.size * 2, args.size * 2), 0)
        draw = ImageDraw.Draw(image)
        draw.text((args.size // 2, args.size // 2), character, font=font, fill=255)
        if image.getbbox() is None:
            failures.append(f"U+{codepoint:04X}: blank raster render")
        checked += 1
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"alpha font checked: {checked} visible ASCII glyphs at {args.size}px")


if __name__ == "__main__":
    main()
