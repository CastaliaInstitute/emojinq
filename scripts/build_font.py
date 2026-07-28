#!/usr/bin/env python3
"""Build a small monochrome OpenType font from Castalia Emoji SVG assets."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path

GLYPHS = {
    "person.svg": ("castalia_person", 0x1F464),
    "place.svg": ("castalia_place", 0x1F4CD),
    "thing.svg": ("castalia_thing", 0x1F4A1),
    "heart.svg": ("castalia_heart", 0x2764),
    "star.svg": ("castalia_star", 0x2B50),
    "sun.svg": ("castalia_sun", 0x2600),
    "moon.svg": ("castalia_moon", 0x1F319),
    "coffee.svg": ("castalia_coffee", 0x2615),
    "sunflower.svg": ("castalia_sunflower", 0x1F33B),
    "house.svg": ("castalia_house", 0x1F3E0),
    "book.svg": ("castalia_book", 0x1F4D6),
    "leaf.svg": ("castalia_leaf", 0x1F343),
}
SVG_NS = "http://www.w3.org/2000/svg"


def paths(svg: Path, element: ET.Element | None = None, in_clip: bool = False):
    if element is None:
        element = ET.parse(svg).getroot()
    in_clip = in_clip or element.tag == f"{{{SVG_NS}}}clipPath"
    if element.tag == f"{{{SVG_NS}}}path" and not in_clip:
        d = element.get("d")
        if d and element.get("fill", "black") != "none":
            yield d
    for child in element:
        yield from paths(svg, child, in_clip)

def make_glyph(svg: Path, upm: int):
    pen = TTGlyphPen(None)
    scale = upm / 128
    # SVG has a downward y axis; OpenType has an upward y axis.
    quadratic = Cu2QuPen(pen, 1.0, all_quadratic=True)
    transform = TransformPen(quadratic, (scale, 0, 0, -scale, 0, upm * 0.08))
    for d in paths(svg):
        parse_path(d, transform)
    return pen.glyph()


def build(source_dir: Path, output: Path) -> None:
    upm = 1000
    canonical_dir = source_dir.parent / "canonical"
    glyph_order = [".notdef"] + [item[0] for item in GLYPHS.values()]
    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    cmap = {}
    metrics = {".notdef": (600, 0)}
    for filename, (glyph_name, codepoint) in GLYPHS.items():
        source = canonical_dir / filename if (canonical_dir / filename).exists() else source_dir / filename
        glyphs[glyph_name] = make_glyph(source, upm)
        cmap[codepoint] = glyph_name
        metrics[glyph_name] = (upm, 0)

    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=880, descent=-120)
    fb.setupNameTable({
        "familyName": "Castalia Emoji",
        "styleName": "Regular",
        "fullName": "Castalia Emoji Regular",
        "psName": "CastaliaEmoji-Regular",
        "uniqueFontIdentifier": "Castalia Emoji Regular 1.0",
        "version": "Version 1.0",
    })
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, usWinAscent=880, usWinDescent=120)
    fb.setupPost()
    fb.setupHead()
    output.parent.mkdir(parents=True, exist_ok=True)
    fb.save(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=Path("assets/ink"))
    parser.add_argument("--output", type=Path, default=Path("fonts/CastaliaEmoji-Regular.ttf"))
    args = parser.parse_args()
    build(args.source_dir, args.output)


if __name__ == "__main__":
    main()
