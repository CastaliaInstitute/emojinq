#!/usr/bin/env python3
"""Validate the generated full-set Emojinq TTF."""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=Path, nargs="?", default=Path("fonts/Emojinq-Regular.ttf"))
    args = parser.parse_args()
    font = TTFont(args.font)
    glyph_count = len(font.getGlyphOrder()) - 1
    cmap_count = len(font.getBestCmap() or {})
    if glyph_count < 4000:
        raise SystemExit(f"expected full-set font, found only {glyph_count} glyphs")
    if cmap_count < 1000:
        raise SystemExit(f"unexpectedly small Unicode cmap: {cmap_count}")
    if "GSUB" not in font:
        raise SystemExit("sequence substitutions missing: GSUB table not found")
    print(f"font checked: {glyph_count} glyphs, {cmap_count} direct code points, GSUB present")


if __name__ == "__main__":
    main()
