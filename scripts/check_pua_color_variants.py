#!/usr/bin/env python3
"""Verify semantic PUA color washes preserve the monochrome brush geometry."""

from __future__ import annotations

import colorsys
import xml.etree.ElementTree as ET
from pathlib import Path

from build_pua_color_variants import PIGMENTS


ROOT = Path(__file__).resolve().parents[1]
MONO = ROOT / "assets" / "pua" / "patterns"
COLOR = ROOT / "assets" / "pua-color" / "patterns"
SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}
NEUTRAL_PIGMENTS = {"black", "gray", "silver", "white"}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def shapes(root: ET.Element) -> list[ET.Element]:
    return [element for element in root.iter() if local(element.tag) in SHAPES]


def geometry(element: ET.Element) -> tuple[str, tuple[tuple[str, str], ...]]:
    ignored = {"fill", "class"}
    return local(element.tag), tuple(sorted((key, value) for key, value in element.attrib.items() if key not in ignored))


def saturation(fill: str) -> float:
    if len(fill) != 7 or not fill.startswith("#"):
        return 0.0
    rgb = tuple(int(fill[index:index + 2], 16) / 255 for index in (1, 3, 5))
    return colorsys.rgb_to_hls(*rgb)[2]


def main() -> None:
    failures: list[str] = []
    for name in sorted(PIGMENTS):
        mono_path = MONO / f"{name}.svg"
        color_path = COLOR / f"{name}.svg"
        if not color_path.exists():
            failures.append(f"missing {color_path}")
            continue
        mono_root = ET.parse(mono_path).getroot()
        color_root = ET.parse(color_path).getroot()
        if color_root.get("data-color-variant") != "sumi-e-color-wash-v1":
            failures.append(f"{color_path}: missing familiar pigment contract")
        if color_root.get("data-pigment") != name:
            failures.append(f"{color_path}: wrong pigment metadata")
        if color_root.get("viewBox") != mono_root.get("viewBox") or color_root.get("data-pua") != mono_root.get("data-pua"):
            failures.append(f"{color_path}: card geometry or code point changed")
        mono_shapes, color_shapes = shapes(mono_root), shapes(color_root)
        if [geometry(element) for element in mono_shapes] != [geometry(element) for element in color_shapes]:
            failures.append(f"{color_path}: color derivative changed brush geometry")
        fills = [element.get("fill", "") for element in color_shapes if element.get("fill") not in {None, "none"}]
        if not fills or any(len(fill) != 7 or not fill.startswith("#") for fill in fills):
            failures.append(f"{color_path}: missing normalized color fills")
        if name not in NEUTRAL_PIGMENTS and max((saturation(fill) for fill in fills), default=0) < .10:
            failures.append(f"{color_path}: pigment wash is not visibly chromatic")
        if any("ink-color-wash" not in element.get("class", "").split() for element in color_shapes if element.get("fill") not in {None, "none"}):
            failures.append(f"{color_path}: colored mark missing ink-color-wash role")
        if any(local(element.tag) in {"image", "filter"} for element in color_root.iter()):
            failures.append(f"{color_path}: raster or filter effect is not allowed")
    extra = sorted(path.stem for path in COLOR.glob("*.svg") if path.stem not in PIGMENTS)
    if extra:
        failures.append(f"unexpected PUA color variants: {', '.join(extra)}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PUA color variants checked: {len(PIGMENTS)} geometry-preserving familiar pigment washes")


if __name__ == "__main__":
    main()
