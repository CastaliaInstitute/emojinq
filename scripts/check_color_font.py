#!/usr/bin/env python3
"""Verify the Emojinq Color font retains fallback outlines and SVG color."""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=Path, nargs="?", default=Path("fonts/Emojinq-Color.ttf"))
    parser.add_argument("--minimum-color-glyphs", type=int, default=4000)
    parser.add_argument("--minimum-pua-color-glyphs", type=int, default=12)
    args = parser.parse_args()
    font = TTFont(args.font)
    if "SVG " not in font:
        raise SystemExit("color font has no SVG table")
    if "COLR" not in font or "CPAL" not in font:
        raise SystemExit("color font has no Chromium-compatible COLR/CPAL tables")
    documents = font["SVG "].docList
    if len(documents) < args.minimum_color_glyphs:
        raise SystemExit(f"only {len(documents)} color glyphs")
    if "glyf" not in font or len(font.getBestCmap()) < 2500:
        raise SystemExit("color font lost its monochrome fallback outlines")
    pua_glyph_ids = {
        font.getGlyphID(name)
        for codepoint, name in font.getBestCmap().items()
        if 0xF0000 <= codepoint <= 0xFFFFD
    }
    pua_color_documents = sum(
        1 for document in documents
        if document.startGlyphID in pua_glyph_ids
    )
    if pua_color_documents < args.minimum_pua_color_glyphs:
        raise SystemExit(f"only {pua_color_documents} PUA color glyphs")
    sample = "\n".join(document.data for document in documents[:40])
    if "ink-color-wash" not in sample or "sumi-ink" not in sample:
        raise SystemExit("color documents do not contain wash and ink layers")
    colr_glyphs = len(font["COLR"].ColorLayers)
    if colr_glyphs < args.minimum_color_glyphs:
        raise SystemExit(f"only {colr_glyphs} COLR color glyphs")
    print(
        f"color font checked: {len(documents)} SVG and {colr_glyphs} COLR color glyphs "
        f"with {pua_color_documents} PUA color glyphs and TrueType fallback"
    )


if __name__ == "__main__":
    main()
