#!/usr/bin/env python3
"""Validate the generated full-set Emojinq TTF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fontTools.ttLib import TTFont


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=Path, nargs="?", default=Path("fonts/Emojinq-Regular.ttf"))
    parser.add_argument("--pua-manifest", type=Path, default=Path("assets/pua/manifest.json"))
    args = parser.parse_args()
    font = TTFont(args.font)
    glyph_count = len(font.getGlyphOrder()) - 1
    cmap_count = len(font.getBestCmap() or {})
    if glyph_count < 4000:
        raise SystemExit(f"expected full-set font, found only {glyph_count} glyphs")
    if cmap_count < 1000:
        raise SystemExit(f"unexpectedly small Unicode cmap: {cmap_count}")
    cmap = font.getBestCmap() or {}
    missing_ascii = [chr(cp) for cp in range(48, 58) if cp not in cmap]
    missing_ascii += [chr(cp) for cp in range(65, 91) if cp not in cmap]
    missing_ascii += [chr(cp) for cp in range(97, 123) if cp not in cmap]
    if missing_ascii:
        raise SystemExit(f"ASCII alphanumerics missing: {''.join(missing_ascii)}")
    pua_entries = json.loads(args.pua_manifest.read_text())
    pua_codepoints = {cp for entry in pua_entries for cp in entry["codepoints"]}
    missing_pua = sorted(cp for cp in pua_codepoints if cp not in cmap)
    if missing_pua:
        preview = ", ".join(f"U+{cp:X}" for cp in missing_pua[:8])
        raise SystemExit(f"PUA code points missing from font: {preview}")
    if "GSUB" not in font:
        raise SystemExit("sequence substitutions missing: GSUB table not found")
    print(f"font checked: {glyph_count} glyphs, {cmap_count} direct code points, {len(pua_codepoints)} PUA code points, GSUB present")


if __name__ == "__main__":
    main()
