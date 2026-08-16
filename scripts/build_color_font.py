#!/usr/bin/env python3
"""Add compressed OpenType-SVG color artwork to Emojinq's TTF fallback."""

from __future__ import annotations

import argparse
import colorsys
import copy
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.colorLib.builder import buildCOLR, buildCPAL
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import SVGPath
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables.S_V_G_ import SVGDocument

from build_font import glyph_name


NS = "http://www.w3.org/2000/svg"
SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}
TRANSFORM_RE = re.compile(r"([A-Za-z]+)\s*\(([^)]*)\)")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalized_hex(value: str) -> str | None:
    value = value.strip().lower()
    if value == "black":
        return "#000000"
    if value == "white":
        return "#ffffff"
    if len(value) == 4 and value.startswith("#"):
        return "#" + "".join(character * 2 for character in value[1:])
    if len(value) == 7 and value.startswith("#"):
        return value
    return None


def wash_rgba(value: str) -> tuple[float, float, float, float]:
    normalized = normalized_hex(value)
    if normalized is None:
        return (0.16, 0.15, 0.13, 1.0)
    red, green, blue = (int(normalized[index:index + 2], 16) / 255 for index in (1, 3, 5))
    hue, saturation, lightness = colorsys.rgb_to_hls(red, green, blue)
    saturation *= 0.78
    lightness = 0.12 + lightness * 0.76
    red, green, blue = colorsys.hls_to_rgb(hue, lightness, saturation)
    paper = (0xF4 / 255, 0xF1 / 255, 0xE9 / 255)
    mixed = tuple(channel * 0.88 + paper_channel * 0.12 for channel, paper_channel in zip((red, green, blue), paper))
    return (*mixed, 0.76)


def multiply_affine(
    left: tuple[float, float, float, float, float, float],
    right: tuple[float, float, float, float, float, float],
) -> tuple[float, float, float, float, float, float]:
    """Compose SVG affine matrices so ``left`` is applied after ``right``."""
    a, b, c, d, e, f = left
    g, h, i, j, k, l = right
    return (
        a * g + c * h,
        b * g + d * h,
        a * i + c * j,
        b * i + d * j,
        a * k + c * l + e,
        b * k + d * l + f,
    )


def normalized_transform(value: str) -> str:
    """Collapse OpenMoji translate/rotate/scale lists to one parser-safe matrix."""
    result = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    for function, argument_text in TRANSFORM_RE.findall(value):
        arguments = [float(number) for number in re.split(r"[\s,]+", argument_text.strip()) if number]
        if function == "matrix" and len(arguments) == 6:
            operation = tuple(arguments)
        elif function == "translate" and len(arguments) in {1, 2}:
            operation = (1.0, 0.0, 0.0, 1.0, arguments[0], arguments[1] if len(arguments) == 2 else 0.0)
        elif function == "scale" and len(arguments) in {1, 2}:
            operation = (arguments[0], 0.0, 0.0, arguments[-1], 0.0, 0.0)
        elif function == "rotate" and len(arguments) in {1, 3}:
            radians = math.radians(arguments[0])
            rotation = (math.cos(radians), math.sin(radians), -math.sin(radians), math.cos(radians), 0.0, 0.0)
            if len(arguments) == 3:
                cx, cy = arguments[1:]
                operation = multiply_affine(
                    (1.0, 0.0, 0.0, 1.0, cx, cy),
                    multiply_affine(rotation, (1.0, 0.0, 0.0, 1.0, -cx, -cy)),
                )
            else:
                operation = rotation
        elif function == "skewX" and len(arguments) == 1:
            operation = (1.0, 0.0, math.tan(math.radians(arguments[0])), 1.0, 0.0, 0.0)
        else:
            raise ValueError(f"unsupported SVG transform: {function}({argument_text})")
        result = multiply_affine(result, operation)
    return "matrix(" + " ".join(f"{number:.12g}" for number in result) + ")"


def normalize_transforms(root: ET.Element) -> None:
    for element in root.iter():
        if value := element.get("transform"):
            element.set("transform", normalized_transform(value))


def color_groups(source: Path) -> list[tuple[str, ET.Element]]:
    """Return one transform-preserving SVG tree per non-black fill color."""
    root = ET.parse(source).getroot()
    normalize_transforms(root)
    colors: list[str] = []
    for element in root.iter():
        if local(element.tag) not in SHAPES:
            continue
        fill = normalized_hex(element.get("fill", "black"))
        if fill and fill not in {"#000000"} and fill not in colors:
            colors.append(fill)

    result = []
    for color in colors:
        layer_root = copy.deepcopy(root)

        def prune(parent: ET.Element) -> None:
            for child in list(parent):
                if child.get("id", "").lower() == "line":
                    parent.remove(child)
                    continue
                if local(child.tag) in SHAPES:
                    if normalized_hex(child.get("fill", "black")) != color:
                        parent.remove(child)
                else:
                    prune(child)

        prune(layer_root)
        result.append((color, layer_root))
    return result


def layer_glyph(root: ET.Element) -> object:
    pen = TTGlyphPen(None)
    quadratic = Cu2QuPen(pen, 1.0, all_quadratic=True)
    # SVGPath preserves nested OpenMoji transforms. The outer matrix converts
    # its 72-unit, y-down card to the font's 1000-unit, y-up coordinate space.
    SVGPath.fromstring(
        ET.tostring(root, encoding="unicode"),
        transform=(1000 / 72, 0, 0, -1000 / 72, 0, 1000),
    ).draw(quadratic)
    return pen.glyph()


def svg_document(source: Path, glyph_id: int) -> str:
    root = ET.parse(source).getroot()
    content = "".join(ET.tostring(child, encoding="unicode") for child in list(root))
    scale = 1000 / 72
    return (
        f'<svg xmlns="{NS}" viewBox="0 0 1000 1000">'
        f'<g id="glyph{glyph_id}" transform="translate(0 1000) scale({scale:.9f} {-scale:.9f})">'
        f'{content}</g></svg>'
    )


def set_name(font: TTFont, name_id: int, value: str) -> None:
    font["name"].setName(value, name_id, 3, 1, 0x409)
    font["name"].setName(value, name_id, 1, 0, 0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-font", type=Path, default=Path("fonts/Emojinq-Regular.ttf"))
    parser.add_argument("--color-dir", type=Path, default=Path("assets/color-all"))
    parser.add_argument("--manifest", type=Path, default=Path("assets/color-all/manifest.json"))
    parser.add_argument("--pua-color-dir", type=Path, default=Path("assets/pua-color"))
    parser.add_argument("--pua-manifest", type=Path, default=Path("assets/pua/manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("fonts/Emojinq-Color.ttf"))
    args = parser.parse_args()

    font = TTFont(args.base_font)
    glyph_order = font.getGlyphOrder()
    glyph_ids = {name: index for index, name in enumerate(glyph_order)}
    documents: list[SVGDocument] = []
    color_glyphs: dict[str, list[tuple[str, int]]] = {}
    palette: list[tuple[float, float, float, float]] = []
    palette_index: dict[str, int] = {}
    ink_color = "#262421"
    palette_index[ink_color] = 0
    palette.append((0x26 / 255, 0x24 / 255, 0x21 / 255, 1.0))
    color_sources = Path(".cache/openmoji/color/svg")
    for item in json.loads(args.manifest.read_text(encoding="utf-8")):
        name = glyph_name([int(codepoint) for codepoint in item["codepoints"]])
        glyph_id = glyph_ids.get(name)
        source = args.color_dir / item["source"]
        if glyph_id is None or not source.exists():
            continue
        documents.append(SVGDocument(svg_document(source, glyph_id), glyph_id, glyph_id, True))

        layers: list[tuple[str, int]] = []
        upstream = color_sources / item["source"]
        if upstream.exists():
            for layer_index, (color, root) in enumerate(color_groups(upstream)):
                if color not in palette_index:
                    palette_index[color] = len(palette)
                    palette.append(wash_rgba(color))
                layer_name = f"{name}.wash{layer_index}"
                font["glyf"].glyphs[layer_name] = layer_glyph(root)
                font["hmtx"].metrics[layer_name] = font["hmtx"].metrics[name]
                glyph_order.append(layer_name)
                layers.append((layer_name, palette_index[color]))
        if layers:
            ink_layer = f"{name}.ink"
            font["glyf"].glyphs[ink_layer] = copy.deepcopy(font["glyf"].glyphs[name])
            font["hmtx"].metrics[ink_layer] = font["hmtx"].metrics[name]
            glyph_order.append(ink_layer)
            layers.append((ink_layer, palette_index[ink_color]))
            color_glyphs[name] = layers

    pua_documents = 0
    if args.pua_manifest.exists() and args.pua_color_dir.exists():
        for item in json.loads(args.pua_manifest.read_text(encoding="utf-8")):
            name = glyph_name([int(codepoint) for codepoint in item["codepoints"]])
            glyph_id = glyph_ids.get(name)
            source = args.pua_color_dir / item["source"]
            if glyph_id is None or not source.exists():
                continue
            documents.append(SVGDocument(svg_document(source, glyph_id), glyph_id, glyph_id, True))
            pua_documents += 1

    svg_table = newTable("SVG ")
    svg_table.docList = documents
    font["SVG "] = svg_table
    font.setGlyphOrder(glyph_order)
    glyph_map = {name: index for index, name in enumerate(glyph_order)}
    font["COLR"] = buildCOLR(color_glyphs, version=0, glyphMap=glyph_map)
    font["CPAL"] = buildCPAL([palette])
    set_name(font, 1, "Emojinq Color")
    set_name(font, 2, "Regular")
    set_name(font, 3, "Emojinq Color 2.1")
    set_name(font, 4, "Emojinq Color Regular")
    set_name(font, 6, "Emojinq-Color")
    set_name(font, 5, "Version 2.1")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    font.save(args.output)
    print(
        f"built {args.output} with {len(documents)} compressed SVG color glyphs, "
        f"including {pua_documents} PUA color glyphs, {len(color_glyphs)} COLR glyphs, "
        f"and {len(palette)} wash colors"
    )


if __name__ == "__main__":
    main()
