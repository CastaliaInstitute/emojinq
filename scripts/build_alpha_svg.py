#!/usr/bin/env python3
"""Convert Yuji Boku ASCII glyphs to SVG sources and apply Emojinq treatment."""

from __future__ import annotations

import json
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from collapse_lines import roughen_path
from import_noto_svg import convert


def main() -> None:
    source = Path(".cache/base-font/YujiBoku-Regular.ttf")
    output = Path("assets/alpha-ink")
    output.mkdir(parents=True, exist_ok=True)
    for stale in output.glob("*.svg"):
        stale.unlink()
    font = TTFont(source)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap() or {}
    units_per_em = font["head"].unitsPerEm
    scale = 72 / units_per_em
    entries = []
    for codepoint in range(32, 127):
        glyph_name = cmap.get(codepoint)
        if not glyph_name:
            continue
        raw = SVGPathPen(glyph_set)
        # Emojinq's font builder interprets SVG coordinates in a 72-unit
        # viewBox. Normalize the Yuji font's native units here and flip the
        # font's upward-positive Y axis into SVG's downward-positive axis.
        pen = TransformPen(raw, (scale * 0.92, 0, 0, -scale, 0, 72))
        glyph_set[glyph_name].draw(pen)
        # Break up the mathematically perfect font outline very lightly. The
        # goal is a dry-brush edge, not visible distortion of the letter.
        path_data = roughen_path(raw.getCommands(), codepoint * 17, amount=0.11)
        source_svg = output / f"source-{codepoint:04X}.svg"
        source_svg.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72">'
            f'<path fill="#000000" d="{path_data}"/></svg>\n'
        )
        target = output / f"U+{codepoint:04X}.svg"
        convert(source_svg, target, f"U+{codepoint:04X}")
        source_svg.unlink()
        entries.append({"name": f"U+{codepoint:04X}", "source": target.name, "codepoints": [codepoint]})
    (output / "manifest.json").write_text(json.dumps(entries, indent=2) + "\n")
    print(f"built {len(entries)} treated alphanumeric SVGs in {output}")


if __name__ == "__main__":
    main()
