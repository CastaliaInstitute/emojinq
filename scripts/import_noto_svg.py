#!/usr/bin/env python3
"""Create a restrained grayscale, hand-drawn pass from an emoji SVG.

This intentionally uses only widely supported SVG primitives. It is an asset
preprocessor, not an SVG renderer for the ESP32.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from collapse_lines import roughen_path

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


def path_bounds(d: str) -> tuple[float, float, float, float] | None:
    values = [float(value) for value in re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", d)]
    if len(values) < 4:
        return None
    points = list(zip(values[0::2], values[1::2]))
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs), max(ys)


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
        for element in list(parent):
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
                    element.set("stroke", "#262421")
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
                    element.set("stroke-width", f"{base_width * pressure:.2f}")
                    element.set("stroke-linecap", "round")
                    element.set("stroke-linejoin", "round")
                    if element.get("d"):
                        # A restrained coordinate wobble keeps curves from
                        # looking plotter-perfect while preserving their
                        # recognizable construction at full-screen scale.
                        element.set("d", roughen_path(element.get("d", ""), shape_index, amount=0.22))
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
            if tag != "defs":
                decorate(element, clipped, stroke or parent_stroke)

    decorate(root)

    root.set("data-castalia-style", "sumi-e-ink-wobble-v2")
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
