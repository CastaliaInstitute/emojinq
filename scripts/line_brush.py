"""Turn OpenMoji line vectors into pressure-shaped, stroke-only brushwork."""

from __future__ import annotations

import math
import re
import copy
import xml.etree.ElementTree as ET
from pathlib import Path

from svgpathtools import Path as SvgPath
from svgpathtools import parse_path

from collapse_lines import roughen_path
from svg_affine import IDENTITY, multiply, parse as parse_transform, text as transform_text

SVG_NS = "http://www.w3.org/2000/svg"
SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}
ECHO_CLASSES = {"ink-echo", "ink-echo-two", "ink-pencil", "ink-texture"}
NUMBER_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
ET.register_namespace("", SVG_NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def number(element: ET.Element, key: str, default: float = 0.0) -> float:
    try:
        return float(element.get(key, default))
    except (TypeError, ValueError):
        return default


def primitive_path(element: ET.Element) -> str:
    tag = local(element.tag)
    if tag == "path":
        return element.get("d", "")
    if tag == "line":
        return f"M {number(element, 'x1')} {number(element, 'y1')} L {number(element, 'x2')} {number(element, 'y2')}"
    if tag in {"polyline", "polygon"}:
        values = [float(value) for value in NUMBER_RE.findall(element.get("points", ""))]
        pairs = list(zip(values[0::2], values[1::2]))
        if len(pairs) < 2:
            return ""
        return "M " + " L ".join(f"{x} {y}" for x, y in pairs) + (" Z" if tag == "polygon" else "")
    if tag == "rect":
        x, y, width, height = (number(element, key) for key in ("x", "y", "width", "height"))
        return f"M {x} {y} H {x + width} V {y + height} H {x} Z"
    if tag in {"circle", "ellipse"}:
        cx, cy = number(element, "cx"), number(element, "cy")
        rx = number(element, "r") if tag == "circle" else number(element, "rx")
        ry = rx if tag == "circle" else number(element, "ry")
        k = 0.5522848
        return (
            f"M {cx + rx} {cy} C {cx + rx} {cy + k * ry} {cx + k * rx} {cy + ry} {cx} {cy + ry} "
            f"C {cx - k * rx} {cy + ry} {cx - rx} {cy + k * ry} {cx - rx} {cy} "
            f"C {cx - rx} {cy - k * ry} {cx - k * rx} {cy - ry} {cx} {cy - ry} "
            f"C {cx + k * rx} {cy - ry} {cx + rx} {cy - k * ry} {cx + rx} {cy} Z"
        )
    return ""


def base_width(element: ET.Element) -> float:
    try:
        source = float(element.get("stroke-width", "1.0"))
    except ValueError:
        source = 1.0
    # OpenMoji's widths are in a broader source scale. Compress them into a
    # loaded-nib range so thick paths do not become uniform black bands.
    return max(0.42, min(1.28, 0.38 + source * 0.30))


def pressure(t: float, seed: int) -> float:
    """A loaded-brush entry/middle/lift curve with restrained asymmetry."""
    loaded = 0.18 + 0.82 * math.sin(math.pi * t) ** 0.62
    asymmetry = 0.95 + 0.08 * math.sin(2.0 * math.pi * t + seed * 0.73)
    return max(0.14, min(1.08, loaded * asymmetry))


def sampled_segments(path: SvgPath, width: float, seed: int) -> list[tuple[str, float]]:
    if path.length() <= 1e-6:
        return []
    closed = path.isclosed()
    if closed:
        # Tiny eyes and enclosed details should read as one deliberate mark,
        # not as a four-way overlap. Keep their pressure modest and even.
        return [(path.d(), width * 0.82)]
    sample_count = max(18, min(120, round(path.length() * 2.2)))
    points = [path.point(index / (sample_count - 1)) for index in range(sample_count)]
    # Three long, overlapping passes give a gradual loaded-middle rhythm.
    # Four short passes made the joins read as little wedges or arrows at
    # glyph scale, especially on the long OpenMoji contours.
    pieces = 3
    result: list[tuple[str, float]] = []
    for piece in range(pieces):
        start = max(0, round(piece * (sample_count - 1) / pieces) - 2)
        end = min(sample_count - 1, round((piece + 1) * (sample_count - 1) / pieces) + 2)
        if end <= start:
            continue
        d = (
            f"M {points[start].real:.3f},{points[start].imag:.3f} "
            + " ".join(f"L {point.real:.3f},{point.imag:.3f}" for point in points[start + 1:end + 1])
        )
        midpoint = (start + end) / 2.0 / (sample_count - 1)
        # Keep adjacent passes close in weight. The overlap masks the join;
        # the pressure curve supplies the broad-nib variation without a
        # visible width jump.
        local_pressure = pressure(midpoint, seed)
        if piece:
            local_pressure = (local_pressure + pressure((start / (sample_count - 1)), seed)) / 2.0
        result.append((d, width * local_pressure))
    return result


def brush_path(d: str, element: ET.Element, seed: int) -> list[tuple[str, float, str]]:
    d = roughen_path(d, seed, amount=0.18)
    try:
        parsed = parse_path(d)
    except (TypeError, ValueError, ZeroDivisionError):
        return []
    width = base_width(element)
    output: list[tuple[str, float, str]] = []
    for sub_index, subpath in enumerate(parsed.continuous_subpaths()):
        cleaned = SvgPath(*[segment for segment in subpath if abs(segment.length()) > 1e-6])
        for segment, segment_width in sampled_segments(cleaned, width, seed + sub_index):
            tone = "#262421" if segment_width >= 0.72 else "#4a4943"
            output.append((segment, segment_width, tone))
    return output


def flatten_transformed_geometry(root: ET.Element) -> None:
    """Bake nested SVG transforms into paths before pressure shaping."""
    if not any("transform" in element.attrib for element in root.iter()):
        return
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.svgLib.path import SVGPath
    semantic_group_id = next(
        (
            element.get("id")
            for element in root.iter()
            if element.get("id") not in {None, "emoji", "line", "color", "line-supplement"}
        ),
        "line",
    )
    flat = ET.Element(f"{{{SVG_NS}}}svg", {"viewBox": root.get("viewBox", "0 0 72 72")})

    def collect(element: ET.Element, inherited: tuple[float, float, float, float, float, float]) -> None:
        combined = multiply(inherited, parse_transform(element.get("transform", "")))
        tag = local(element.tag)
        if tag in SHAPES:
            clone = copy.deepcopy(element)
            clone.set("transform", transform_text(combined))
            flat.append(clone)
            return
        if tag == "defs":
            return
        for child in list(element):
            collect(child, combined)

    collect(root, IDENTITY)
    pen = SVGPathPen(None)
    SVGPath.fromstring(ET.tostring(flat, encoding="unicode")).draw(pen)
    commands = pen.getCommands()
    for child in list(root):
        root.remove(child)
    line = ET.SubElement(root, f"{{{SVG_NS}}}g", {"id": semantic_group_id})
    ET.SubElement(
        line,
        f"{{{SVG_NS}}}path",
        {
            "d": commands,
            "fill": "none",
            "stroke": "#000000",
            "stroke-width": "2",
            "stroke-linecap": "round",
            "stroke-linejoin": "round",
        },
    )


def taper(root: ET.Element) -> None:
    flatten_transformed_geometry(root)
    root.set("data-castalia-style", "sumi-e-ink-wash-v1")
    root.set("data-ink-stroke-system", "tapered-v1")
    root.set("data-ink-coverage", "complete")
    root.set("data-ink-pressure", "loaded-middle-v1")
    index = 0

    def visit(parent: ET.Element, inside_defs: bool = False) -> None:
        nonlocal index
        for element in list(parent):
            tag = local(element.tag)
            if tag == "defs":
                continue
            if tag in SHAPES:
                classes = set(element.get("class", "").split())
                dasharray = element.get("stroke-dasharray", "").strip().lower()
                if classes & ECHO_CLASSES or dasharray not in {"", "none"}:
                    parent.remove(element)
                    continue
                d = primitive_path(element)
                marks = brush_path(d, element, index) if d else []
                position = list(parent).index(element)
                parent.remove(element)
                for mark_d, width, color in marks:
                    node = ET.Element(f"{{{SVG_NS}}}path", {
                        "class": "ink-stroke",
                        "data-ink-stroke": "tapered",
                        "data-ink-role": "line-source-tapered",
                        "data-ink-index": str(index),
                        "pathLength": "1",
                        "d": mark_d,
                        "fill": "none",
                        "stroke": color,
                        "stroke-width": f"{width:.2f}",
                        "stroke-linecap": "round",
                        "stroke-linejoin": "round",
                    })
                    parent.insert(position, node)
                    position += 1
                    index += 1
            else:
                visit(element, inside_defs)

    visit(root)


def convert(source: Path, target: Path) -> None:
    tree = ET.parse(source)
    taper(tree.getroot())
    target.parent.mkdir(parents=True, exist_ok=True)
    tree.write(target, encoding="utf-8", xml_declaration=True)
