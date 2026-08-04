#!/usr/bin/env python3
"""Create a restrained grayscale, hand-drawn pass from an emoji SVG.

This intentionally uses only widely supported SVG primitives. It is an asset
preprocessor, not an SVG renderer for the ESP32.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from collapse_lines import roughen_path
from svgpathtools import Path as SvgPath
from svgpathtools import parse_path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
STYLE_FILL = re.compile(r"(?:^|;)\s*fill\s*:\s*([^;]+)")
HEX_ANY = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?")


def gray(value: str) -> str:
    match = HEX.match(value.strip())
    if not match:
        return value
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    r, g, b = (int(digits[i : i + 2], 16) for i in (0, 2, 4))
    # Luma keeps dark source details dark while removing chroma.
    # Naturalist plates leave the paper visible: preserve tonal hierarchy but
    # lift saturated fills into pale wash rather than solid ink blocks.
    y = 170 + round((0.2126 * r + 0.7152 * g + 0.0722 * b) * 0.33)
    return f"#{y:02x}{y:02x}{y:02x}"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def fill_value(element: ET.Element) -> str | None:
    value = element.get("fill")
    if value:
        return value
    style = STYLE_FILL.search(element.get("style", ""))
    return style.group(1).strip() if style else None


def stroke_value(element: ET.Element) -> str | None:
    value = element.get("stroke")
    if value:
        return value
    match = re.search(r"(?:^|;)\s*stroke\s*:\s*([^;]+)", element.get("style", ""))
    return match.group(1).strip() if match else None


def pressure_for(element: ET.Element, index: int) -> float:
    """Return stable, non-cyclic pen pressure for one source mark."""
    geometry = "|".join(
        element.get(key, "")
        for key in ("d", "x1", "x2", "y1", "y2", "cx", "cy", "rx", "ry", "points")
    )
    digest = hashlib.sha1(f"{index}|{geometry}".encode()).hexdigest()
    noise = int(digest[:8], 16) / 0xFFFFFFFF
    return 0.56 + noise * 0.56


def tapered_outline(d: str, width: float) -> str | None:
    """Convert a centerline into one filled, tapered brush contour."""
    centerline = parse_path(d)
    centerline = SvgPath(*[segment for segment in centerline if abs(segment.length()) > 1e-6])
    if not centerline:
        return None
    closed = d.strip().lower().endswith("z")
    length = max(1.0, centerline.length())
    count = max(8, min(180, int(length / 1.2)))
    ts = [i / count for i in range(count)] if closed else [i / (count - 1) for i in range(count)]
    points = [centerline.point(t) for t in ts]
    left, right = [], []
    for i, point in enumerate(points):
        before = points[i - 1] if i else points[-1] if closed else points[1]
        after = points[(i + 1) % len(points)] if (i + 1 < len(points) or closed) else points[-2]
        tangent = after - before
        magnitude = abs(tangent) or 1.0
        normal = complex(-tangent.imag / magnitude, tangent.real / magnitude)
        progress = i / (len(points) - 1) if len(points) > 1 else 0.5
        taper = 1.0 if closed else 0.16 + 0.84 * math.sin(math.pi * progress) ** 0.55
        radius = width * 0.5 * taper
        left.append(point + normal * radius)
        right.append(point - normal * radius)
    if closed:
        # A closed centerline needs an outer and inner contour. Joining the
        # two offsets into one contour creates a self-intersecting spiral;
        # SVG renderers can then fill much of the enclosed artwork instead of
        # leaving an outlined ring (especially visible on the diya lamp).
        # Keep the offsets as separate, oppositely directed subpaths.
        if len(left) < 3 or len(right) < 3:
            return None
        contours = (left, list(reversed(right)))
        return " ".join(
            "M " + " L ".join(f"{point.real:.3f} {point.imag:.3f}" for point in contour) + " Z"
            for contour in contours
        )

    outline = left + list(reversed(right))
    if len(outline) < 3:
        return None
    values = [f"{point.real:.3f} {point.imag:.3f}" for point in outline]
    return "M " + " L ".join(values) + " Z"


def path_bounds(d: str) -> tuple[float, float, float, float] | None:
    values = [float(value) for value in re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", d)]
    if len(values) < 4:
        return None
    points = list(zip(values[0::2], values[1::2]))
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs), max(ys)


def primitive_path(element: ET.Element, tag: str) -> str:
    """Express stroked SVG primitives as centerline paths before tapering."""
    def number(key: str, default: float = 0.0) -> float:
        try:
            return float(element.get(key, default))
        except (TypeError, ValueError):
            return default

    if tag == "line":
        return f"M {number('x1')} {number('y1')} L {number('x2')} {number('y2')}"
    if tag in {"polyline", "polygon"}:
        values = re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", element.get("points", ""))
        pairs = list(zip(values[::2], values[1::2]))
        if len(pairs) < 2:
            return ""
        path = "M " + " L ".join(f"{x} {y}" for x, y in pairs)
        return path + (" Z" if tag == "polygon" else "")
    if tag == "rect":
        x, y, w, h = number("x"), number("y"), number("width"), number("height")
        rx = min(abs(number("rx")), abs(w) / 2, abs(h) / 2)
        ry = min(abs(number("ry", rx)), abs(w) / 2, abs(h) / 2)
        if not rx or not ry:
            return f"M {x} {y} H {x + w} V {y + h} H {x} Z"
        k = 0.5522848
        return (
            f"M {x + rx} {y} H {x + w - rx} "
            f"C {x + w - rx + k * rx} {y} {x + w} {y + ry - k * ry} {x + w} {y + ry} "
            f"V {y + h - ry} C {x + w} {y + h - ry + k * ry} {x + w - rx + k * rx} {y + h} {x + w - rx} {y + h} "
            f"H {x + rx} C {x + rx - k * rx} {y + h} {x} {y + h - ry + k * ry} {x} {y + h - ry} "
            f"V {y + ry} C {x} {y + ry - k * ry} {x + rx - k * rx} {y} {x + rx} {y} Z"
        )
    if tag in {"circle", "ellipse"}:
        cx, cy = number("cx"), number("cy")
        rx = number("r") if tag == "circle" else number("rx")
        ry = rx if tag == "circle" else number("ry")
        k = 0.5522848
        return (
            f"M {cx + rx} {cy} C {cx + rx} {cy + k * ry} {cx + k * rx} {cy + ry} {cx} {cy + ry} "
            f"C {cx - k * rx} {cy + ry} {cx - rx} {cy + k * ry} {cx - rx} {cy} "
            f"C {cx - rx} {cy - k * ry} {cx - k * rx} {cy - ry} {cx} {cy - ry} "
            f"C {cx + k * rx} {cy - ry} {cx + rx} {cy - k * ry} {cx + rx} {cy} Z"
        )
    return element.get("d", "")


def overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    intersection = ix * iy
    area_a = max(1.0, (a[2] - a[0]) * (a[3] - a[1]))
    area_b = max(1.0, (b[2] - b[0]) * (b[3] - b[1]))
    return intersection / min(area_a, area_b) > 0.78


def grayscale_attributes(root: ET.Element) -> None:
    for element in root.iter():
        for key, value in list(element.attrib.items()):
            element.set(key, HEX_ANY.sub(lambda match: gray(match.group(0)), value))


def convert(source: Path, target: Path, name: str) -> None:
    root = ET.parse(source).getroot()
    root.set("id", f"emojinq-{name}")
    root.set("role", "img")
    root.set("aria-label", name.replace("-", " "))
    grayscale_attributes(root)

    defs = ET.Element(f"{{{SVG_NS}}}defs")
    style = ET.SubElement(defs, f"{{{SVG_NS}}}style")
    style.text = """.ink-outline{stroke:#292929;stroke-width:1.7;stroke-linejoin:round;stroke-linecap:round}"""
    root.insert(0, defs)

    shape_index = 0
    outlined_bounds: list[tuple[float, float, float, float]] = []

    def decorate(parent: ET.Element, inside_clip: bool = False, inherited_stroke: str | None = None) -> None:
        nonlocal shape_index
        parent_stroke = stroke_value(parent) or inherited_stroke
        if not inside_clip:
            candidates = []
            for candidate in list(parent):
                candidate_tag = local(candidate.tag)
                candidate_stroke = stroke_value(candidate) or parent_stroke
                candidate_d = candidate.get("d", "").strip()
                bounds = path_bounds(candidate_d)
                if (
                    candidate_tag == "path"
                    and candidate_stroke
                    and candidate_stroke != "none"
                    and candidate_d.lower().endswith("z")
                    and bounds is not None
                    and (bounds[2] - bounds[0]) * (bounds[3] - bounds[1]) > 900
                ):
                    candidates.append((bounds, candidate))
            if candidates:
                _, source = max(candidates, key=lambda item: (item[0][2] - item[0][0]) * (item[0][3] - item[0][1]))
                wash = copy.deepcopy(source)
                wash.set("fill", "#dedbd4")
                wash.set("stroke", "none")
                wash.set("data-ink-wash", "true")
                wash.attrib.pop("class", None)
                wash.attrib.pop("style", None)
                wash.attrib.pop("stroke-width", None)
                parent.insert(0, wash)
        for element in list(parent):
            if element.get("data-ink-wash") == "true":
                continue
            tag = local(element.tag)
            clipped = inside_clip or tag == "clipPath"
            stroke = None
            if tag in {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}:
                fill = fill_value(element)
                stroke = stroke_value(element) or parent_stroke
                if stroke and stroke != "none":
                    # OpenMoji Black is already a line drawing. Preserve its
                    # paths as single marks, but vary pressure between marks
                    # so the result reads as pen work instead of a uniform
                    # digital outline.
                    element.attrib.pop("style", None)
                    try:
                        base_width = float(element.get("stroke-width", "2"))
                    except ValueError:
                        base_width = 2.0
                    # Some OpenMoji construction marks use very wide source
                    # strokes. Normalize those first so they become pressure
                    # variation, not chunky bars.
                    base_width = min(base_width, 2.0)
                    pressure = pressure_for(element, shape_index)
                    source_d = primitive_path(element, tag)
                    if source_d:
                        # A restrained coordinate wobble keeps curves from
                        # looking plotter-perfect while preserving their
                        # recognizable construction at full-screen scale.
                        source_d = roughen_path(source_d, shape_index, amount=0.22)
                        outline = tapered_outline(source_d, base_width * pressure)
                    else:
                        outline = None
                    if outline:
                        element.tag = f"{{{SVG_NS}}}path"
                        for key in ("x", "y", "x1", "x2", "y1", "y2", "cx", "cy", "r", "rx", "ry", "width", "height", "points"):
                            element.attrib.pop(key, None)
                        element.set("d", outline)
                        element.set("fill", "#262421")
                        # Closed tapered marks carry two contours. Even-odd
                        # makes their hollow center explicit, independent of
                        # source winding direction.
                        if source_d.strip().lower().endswith("z"):
                            element.set("fill-rule", "evenodd")
                        element.set("data-ink-stroke", "tapered")
                        for key in ("stroke", "stroke-width", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit"):
                            element.attrib.pop(key, None)
                    shape_index += 1
                elif fill and fill != "none":
                    element.set("fill", gray(fill))
                    element.attrib.pop("style", None)
                    if not clipped:
                        # One outline per visible geometry, with restrained
                        # broad-nib variation. Clipped color layers stay fill
                        # only so stacked source layers cannot double the edge.
                        bounds = path_bounds(element.get("d", ""))
                        duplicate = bounds is not None and any(overlaps(bounds, previous) for previous in outlined_bounds)
                        if not duplicate:
                            element.set("class", "ink-outline")
                            element.set("stroke-width", f"{2.15 + (shape_index % 5) * 0.22:.2f}")
                            if bounds is not None:
                                outlined_bounds.append(bounds)
                    shape_index += 1
                elif element.get("color") or (tag == "path" and not fill and not stroke):
                    # OpenMoji Black encodes many of its already-filled brush
                    # marks with `color` or the SVG default fill rather than
                    # an explicit `fill` or `stroke`.
                    # Preserve those single marks as tapered ink geometry
                    # instead of silently leaving them as unclassified paths.
                    element.set("fill", "#262421")
                    element.set("data-ink-stroke", "tapered")
                    element.attrib.pop("color", None)
                    element.attrib.pop("style", None)
                    shape_index += 1
            if tag != "defs":
                decorate(element, clipped, stroke or parent_stroke)

    decorate(root)

    root.set("data-castalia-style", "sumi-e-ink-wash-v1")
    root.set("data-ink-stroke-system", "tapered-v1")
    has_geometry = any(
        element.get("data-ink-stroke") == "tapered"
        or (local(element.tag) in {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"} and fill_value(element) not in {None, "none"})
        for element in root.iter()
    )
    root.set("data-ink-coverage", "complete" if has_geometry else "upstream-empty")
    target.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(target, encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    convert(args.input, args.output, args.name)


if __name__ == "__main__":
    main()
