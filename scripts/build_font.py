#!/usr/bin/env python3
"""Build the complete Emojinq monochrome TrueType font from SVG geometry.

OpenMoji supplies centerline strokes, while TrueType glyphs require filled
outlines. This builder samples each stroke, applies a tapered brush profile,
and writes the resulting contours into a conventional TTF. Sequence entries
also receive OpenType ``liga`` substitutions when their component glyphs are
available.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeatures
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path as parse_svg_path
from fontTools.ttLib import TTFont
from svgpathtools import Path as SvgPath
from svgpathtools import parse_path
from style_contract import assert_sumi_e

SVG_NS = "http://www.w3.org/2000/svg"
SHAPES = {"path", "line", "rect", "circle", "ellipse", "polygon", "polyline"}
NUMBER_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def glyph_name(codepoints: list[int]) -> str:
    return "emojinq_" + "_".join(f"{cp:X}" for cp in codepoints)


def transform_point(point: complex, upm: int, view_size: float = 72.0) -> tuple[float, float]:
    scale = upm / view_size
    return point.real * scale, upm - point.imag * scale


def path_data(element: ET.Element) -> str | None:
    tag = local(element.tag)
    if tag == "path":
        return element.get("d")
    if tag == "line":
        return f"M {element.get('x1', '0')} {element.get('y1', '0')} L {element.get('x2', '0')} {element.get('y2', '0')}"
    if tag == "rect":
        x, y = float(element.get("x", 0)), float(element.get("y", 0))
        w, h = float(element.get("width", 0)), float(element.get("height", 0))
        return f"M {x} {y} L {x + w} {y} L {x + w} {y + h} L {x} {y + h} Z"
    if tag in {"polygon", "polyline"}:
        values = [float(v) for v in NUMBER_RE.findall(element.get("points", ""))]
        pairs = list(zip(values[0::2], values[1::2]))
        if len(pairs) < 2:
            return None
        close = " Z" if tag == "polygon" else ""
        return "M " + " L ".join(f"{x} {y}" for x, y in pairs) + close
    if tag in {"circle", "ellipse"}:
        cx, cy = float(element.get("cx", 0)), float(element.get("cy", 0))
        rx = float(element.get("r", element.get("rx", 0)))
        ry = float(element.get("r", element.get("ry", 0)))
        points = [
            (cx + math.cos(i * math.tau / 32) * rx, cy + math.sin(i * math.tau / 32) * ry)
            for i in range(32)
        ]
        return "M " + " L ".join(f"{x} {y}" for x, y in points) + " Z"
    return None


def is_closed(d: str) -> bool:
    return d.strip().lower().endswith("z")


def stroke_width(element: ET.Element, inherited: float = 2.0) -> float:
    try:
        return min(float(element.get("stroke-width", inherited)), 3.0)
    except ValueError:
        return inherited


def add_polygon(pen: TTGlyphPen, points: list[tuple[float, float]], upm: int) -> None:
    if len(points) < 3:
        return
    transformed = [transform_point(complex(x, y), upm) for x, y in points]
    pen.moveTo(transformed[0])
    for point in transformed[1:]:
        pen.lineTo(point)
    pen.closePath()


def stroke_outline(pen: TTGlyphPen, d: str, width: float, upm: int, seed: int) -> None:
    parsed = parse_path(d)
    subpaths = parsed.continuous_subpaths()
    for sub_index, centerline in enumerate(subpaths):
        centerline = SvgPath(*[segment for segment in centerline if abs(segment.length()) > 1e-6])
        if not centerline:
            continue
        _stroke_subpath(pen, centerline, width, upm, seed + sub_index, centerline.isclosed())


def _stroke_subpath(pen: TTGlyphPen, centerline: SvgPath, width: float, upm: int, seed: int, closed: bool) -> None:
    length = max(1.0, centerline.length())
    count = max(8, min(180, int(length / 1.2)))
    ts = [i / count for i in range(count)] if closed else [i / (count - 1) for i in range(count)]
    points = [centerline.point(t) for t in ts]
    left: list[tuple[float, float]] = []
    right: list[tuple[float, float]] = []
    phase = (seed * 1.61803398875) % math.tau
    secondary_phase = (seed * 0.75487766625) % math.tau
    for i, point in enumerate(points):
        before = points[i - 1] if i else points[-1] if closed else points[1]
        after = points[(i + 1) % len(points)] if (i + 1 < len(points) or closed) else points[-2]
        tangent = after - before
        magnitude = abs(tangent) or 1.0
        normal = complex(-tangent.imag / magnitude, tangent.real / magnitude)
        if closed:
            taper = 1.0
            progress = i / max(1, len(points) - 1)
        else:
            progress = i / (len(points) - 1)
            taper = 0.16 + 0.84 * math.sin(math.pi * progress) ** 0.55
        pressure = (
            1.0
            + 0.085 * math.sin(progress * math.tau + phase)
            + 0.028 * math.sin(progress * math.tau * 3.5 + secondary_phase)
        )
        radius = width * 0.5 * taper * pressure
        left.append(transform_point(point + normal * radius, upm))
        right.append(transform_point(point - normal * radius, upm))
    outline = left + list(reversed(right))
    if len(outline) >= 3:
        pen.moveTo(outline[0])
        for point in outline[1:]:
            pen.lineTo(point)
        pen.closePath()


def make_glyph(svg: Path, upm: int) -> object:
    root = ET.parse(svg).getroot()
    pen = TTGlyphPen(None)
    index = 0

    def visit(parent: ET.Element, inherited_stroke: bool = False, inherited_width: float = 2.0, in_clip: bool = False) -> None:
        nonlocal index
        for element in list(parent):
            tag = local(element.tag)
            clipped = in_clip or tag == "clipPath"
            if tag in SHAPES and not clipped:
                d = path_data(element)
                stroke = inherited_stroke or element.get("stroke", "none") != "none"
                fill = element.get("fill", "black") != "none"
                if d and stroke:
                    stroke_outline(pen, d, stroke_width(element, inherited_width) * 0.9, upm, index)
                    index += 1
                elif d and fill and element.get("data-ink-wash") != "true":
                    quadratic = Cu2QuPen(pen, 1.0, all_quadratic=True)
                    transform = TransformPen(quadratic, (upm / 72, 0, 0, -upm / 72, 0, upm))
                    parse_svg_path(d, transform)
            child_stroke = inherited_stroke or element.get("stroke", "none") != "none"
            try:
                child_width = float(element.get("stroke-width", inherited_width))
            except ValueError:
                child_width = inherited_width
            if tag != "defs":
                visit(element, child_stroke, child_width, clipped)

    visit(root)
    return pen.glyph()


def build(
    source_dir: Path,
    manifest_path: Path,
    output: Path,
    alpha_dir: Path | None = None,
    alpha_manifest: Path | None = None,
    extra_dirs: list[Path] | None = None,
    extra_manifests: list[Path] | None = None,
) -> None:
    upm = 1000
    entries = json.loads(manifest_path.read_text())
    if alpha_dir and alpha_manifest:
        entries.extend({**item, "source_dir": str(alpha_dir), "alpha": True} for item in json.loads(alpha_manifest.read_text()))
    for extra_dir, extra_manifest in zip(extra_dirs or [], extra_manifests or []):
        entries.extend({**item, "source_dir": str(extra_dir)} for item in json.loads(extra_manifest.read_text()))
    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    glyph_order = [".notdef"]
    metrics = {".notdef": (upm, 0)}
    cmap: dict[int, str] = {}
    single_by_cp: dict[int, str] = {}
    alpha_by_cp: dict[int, str] = {}
    sequences: list[tuple[list[int], str]] = []
    for item in entries:
        cps = [int(cp) for cp in item["codepoints"]]
        name = glyph_name(cps)
        # The upstream emoji manifest contains one repeated alias. Keep the
        # first occurrence so glyph order and glyph data remain synchronized
        # when the Yuji alphabet is appended.
        if name in glyphs:
            continue
        source = Path(item.get("source_dir", source_dir)) / item["source"]
        if not source.exists():
            continue
        # A TTF has no reliable visual-style flag. Validate every source
        # before outlining it so a non-sumi-e SVG can never enter the font.
        assert_sumi_e(source)
        glyphs[name] = make_glyph(source, upm)
        glyph_order.append(name)
        if item.get("alpha"):
            # Optical spacing from the actual painted bounds. This avoids the
            # disconnected, typewriter rhythm of identical 1000-unit cells.
            if getattr(glyphs[name], "numberOfContours", 0) > 0:
                glyphs[name].recalcBounds(None)
                advance = max(500, min(1000, glyphs[name].xMax + 120))
            else:
                advance = 400
            metrics[name] = (advance, 0)
        else:
            metrics[name] = (upm, 0)
        if len(cps) == 1:
            single_by_cp.setdefault(cps[0], name)
            if item.get("alpha"):
                alpha_by_cp[cps[0]] = name
        else:
            sequences.append((cps, name))
    cmap.update(single_by_cp)

    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=880, descent=-120)
    fb.setupNameTable({
        "familyName": "Emojinq",
        "styleName": "Regular",
        "fullName": "Emojinq Regular",
        "psName": "Emojinq-Regular",
        "uniqueFontIdentifier": "Emojinq Regular 2.0",
        "version": "Version 2.0",
    })
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, usWinAscent=880, usWinDescent=120)
    fb.setupPost()
    fb.setupHead()
    output.parent.mkdir(parents=True, exist_ok=True)
    fb.save(output)

    component_names = set(glyph_order)
    with tempfile.NamedTemporaryFile("w", suffix=".fea", delete=False) as feature_file:
        feature_file.write("feature kern {\n")
        for left, right, value in (
            ("A", "V", -90), ("A", "W", -80), ("A", "Y", -90),
            ("V", "A", -70), ("V", "o", -55), ("W", "A", -65),
            ("W", "o", -45), ("Y", "a", -45), ("Y", "o", -45),
            ("T", "a", -60), ("T", "e", -55), ("T", "o", -60),
            ("L", "T", -35), ("P", "a", -35), ("R", "a", -30),
        ):
            left_name = alpha_by_cp.get(ord(left))
            right_name = alpha_by_cp.get(ord(right))
            if left_name and right_name:
                feature_file.write(f"  pos {left_name} {right_name} {value};\n")
        feature_file.write("} kern;\n")
        feature_file.write("feature liga {\n")
        for cps, target in sequences:
            parts = [single_by_cp.get(cp) for cp in cps]
            if target in component_names and all(parts):
                feature_file.write(f"  sub {' '.join(parts)} by {target};\n")
        feature_file.write("} liga;\n")
        feature_path = feature_file.name
    font = TTFont(output)
    addOpenTypeFeatures(font, feature_path)
    font.save(output)
    print(f"built {len(glyph_order) - 1} glyphs, {len(cmap)} direct code points in {output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=Path("assets/gray-all"))
    parser.add_argument("--manifest", type=Path, default=Path("assets/gray-all/manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("fonts/Emojinq-Regular.ttf"))
    parser.add_argument("--alpha-dir", type=Path)
    parser.add_argument("--alpha-manifest", type=Path)
    parser.add_argument("--extra-dir", type=Path, action="append")
    parser.add_argument("--extra-manifest", type=Path, action="append")
    args = parser.parse_args()
    build(args.source_dir, args.manifest, args.output, args.alpha_dir, args.alpha_manifest, args.extra_dir, args.extra_manifest)


if __name__ == "__main__":
    main()
