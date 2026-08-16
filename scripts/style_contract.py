"""Shared visual contract for the Emojinq sumi-e asset pipeline."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

SUMI_E_STYLE = "sumi-e-ink-wash-v1"
SUMI_E_STROKE_SYSTEM = "tapered-v1"
BRUSH_MASS_STYLE = "sumi-e-naturalist-v2"
BRUSH_MASS_STROKE_SYSTEM = "filled-brush-mass-v2"
VALID_CONTRACTS = {
    (SUMI_E_STYLE, SUMI_E_STROKE_SYSTEM),
    (BRUSH_MASS_STYLE, BRUSH_MASS_STROKE_SYSTEM),
}


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _is_neutral(paint: str) -> bool:
    value = paint.strip().lower()
    if value in {"none", "transparent"}:
        return True
    if not value.startswith("#") or len(value) not in {4, 7}:
        return False
    if len(value) == 4:
        channels = [int(char * 2, 16) for char in value[1:]]
    else:
        channels = [int(value[index:index + 2], 16) for index in (1, 3, 5)]
    return max(channels) - min(channels) <= 16


def assert_sumi_e(path: Path) -> None:
    """Raise a useful error when an SVG is not an Emojinq sumi-e asset."""
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        raise ValueError(f"cannot read SVG {path}: {exc}") from exc
    style = root.get("data-castalia-style")
    stroke_system = root.get("data-ink-stroke-system")
    if (style, stroke_system) not in VALID_CONTRACTS:
        raise ValueError(
            f"{path}: expected one of {sorted(VALID_CONTRACTS)}, "
            f"found {style!r}/{stroke_system!r}"
        )
    if (style, stroke_system) == (BRUSH_MASS_STYLE, BRUSH_MASS_STROKE_SYSTEM):
        brush_marks = 0
        visible_marks = 0
        tones: set[str] = set()
        for element in root.iter():
            if _local(element.tag) not in {"path", "ellipse", "circle"}:
                continue
            fill = element.get("fill", "").strip().lower()
            stroke = element.get("stroke", "").strip().lower()
            if fill and fill not in {"none", "transparent"}:
                classes = set(element.get("class", "").split())
                if not classes.intersection({"ink-wash", "ink-dry"}):
                    raise ValueError(f"{path}: filled brush geometry lacks ink-wash/ink-dry role")
                if not _is_neutral(fill):
                    raise ValueError(f"{path}: non-neutral brush fill {fill!r}")
                brush_marks += 1
                visible_marks += 1
                tones.add(fill)
            if stroke and stroke not in {"none", "transparent"}:
                if not _is_neutral(stroke):
                    raise ValueError(f"{path}: non-neutral brush stroke {stroke!r}")
                visible_marks += 1
                tones.add(stroke)
        if brush_marks < 1 or visible_marks < 2:
            raise ValueError(f"{path}: brush-mass study needs a wash plus supporting gestures")
        if len(tones) < 2:
            raise ValueError(f"{path}: brush-mass study needs a dark/light ink hierarchy")
