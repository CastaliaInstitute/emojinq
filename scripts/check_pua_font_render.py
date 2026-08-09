#!/usr/bin/env python3
"""Render every PUA code point from the shipped TTF and reject blank glyphs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=Path, default=Path("fonts/Emojinq-Regular.ttf"), nargs="?")
    parser.add_argument("--manifest", type=Path, default=Path("assets/pua/manifest.json"))
    parser.add_argument("--size", type=int, default=96)
    args = parser.parse_args()

    font = ImageFont.truetype(str(args.font), args.size)
    entries = json.loads(args.manifest.read_text())
    codepoints = sorted({cp for entry in entries for cp in entry["codepoints"]})
    failures = []
    for cp in codepoints:
        image = Image.new("L", (128, 128), 0)
        draw = ImageDraw.Draw(image)
        draw.text((8, 8), chr(cp), font=font, fill=255, stroke_width=0)
        bbox = image.getbbox()
        if bbox is None or bbox[2] - bbox[0] < 3 or bbox[3] - bbox[1] < 3:
            failures.append(f"U+{cp:05X}: blank or too small bbox={bbox}")
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    print(f"PUA font render checked: {len(codepoints)} code points at {args.size}px")


if __name__ == "__main__":
    main()
