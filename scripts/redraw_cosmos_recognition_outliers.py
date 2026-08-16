#!/usr/bin/env python3
"""Repair cosmos glyphs whose silhouettes do not identify their subject.

These four studies keep the compact astronomical vocabulary used by the rest
of the family, but replace generic streaks and circles with observed, familiar
structures: a burning rock, overlapping eclipse disks, a spiral gas cloud,
and a dish-bearing robotic probe.
"""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "cosmos"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522", wobble=.28, dry=False) -> str:
    width = max(width, 1.15)
    return svg_path(
        stroke_path(points(*values), width=width, seed=seed, wobble=wobble),
        fill=color,
        class_name="ink-dry" if dry else "ink-wash",
    )


def mass(d: str, color="#4a4943", role="ink-wash") -> str:
    return f'<path class="{role}" fill="{color}" d="{d}" data-ink-brush-pass="loaded-mass-v2"/>'


def dab(cx: float, cy: float, rx: float, ry: float, color="#262522") -> str:
    return (
        f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'
    )


def contour(d: str, color="#4a4943", width=2.0) -> str:
    return (
        f'<path class="ink-dry" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" d="{d}" '
        'data-ink-brush-pass="dry-contour-v2"/>'
    )


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text(encoding="utf-8")
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="cosmos / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>cosmos / {name} — recognizable naturalist sumi-e study</title>{''.join(marks)}</svg>
''',
        encoding="utf-8",
    )


# A rock leads the gesture; three unequal flaming trails lift behind it.
write("meteor", [
    ribbon([(50, 48, .95), (39, 39, .78), (27, 27, .48), (13, 14, .08)], 5.4, "meteor-loaded-tail", "#4a4943", .34),
    ribbon([(47, 51, .90), (35, 45, .65), (22, 38, .30), (9, 31, .06)], 2.7, "meteor-dry-tail-low", "#77746a", .38, True),
    ribbon([(52, 43, .82), (43, 33, .62), (34, 21, .28), (28, 10, .06)], 2.1, "meteor-dry-tail-high", "#5f5c55", .36, True),
    mass("M 43 43 C 46 38 54 37 59 41 C 64 45 63 53 58 57 C 52 61 44 58 41 52 C 40 48 41 45 43 43 Z", "#262522"),
    mass("M 47 44 C 50 41 55 41 58 44 C 55 46 51 47 47 46 Z", "#77746a", "ink-dry"),
    dab(55, 51, 1.8, 1.5, "#77746a"),
])


# Two offset disks and a broken corona make the occultation unmistakable.
write("eclipse", [
    contour("M 18 36 C 18 25 26 17 37 17 C 48 17 56 25 56 36 C 56 47 48 55 37 55 C 26 55 18 47 18 36 Z", "#77746a", 2.4),
    contour("M 27 34 C 27 24 34 17 44 17 C 54 17 61 25 61 35 C 61 45 54 52 44 52 C 34 52 27 44 27 34 Z", "#262522", 3.0),
    ribbon([(16, 17, .10), (13, 13, .72), (10, 10, .06)], 1.6, "eclipse-ray-upper-left", "#77746a", .3, True),
    ribbon([(13, 36, .10), (8, 36, .72), (4, 35, .06)], 1.7, "eclipse-ray-left", "#4a4943", .3),
    ribbon([(18, 55, .10), (14, 59, .72), (11, 62, .06)], 1.5, "eclipse-ray-lower-left", "#77746a", .3, True),
    mass("M 20 22 C 23 18 28 15 33 14 C 29 18 26 22 24 27 Z", "#4a4943"),
])


# Uneven cloud lobes and detached stars read as a cloud in space, not an eye.
write("nebula", [
    contour("M 14 42 C 10 36 15 29 22 30 C 22 22 30 18 37 23 C 43 17 52 21 52 29 C 61 29 64 37 59 43 C 63 49 55 55 48 52 C 43 59 34 57 31 51 C 24 56 16 51 18 45 C 16 45 15 44 14 42 Z", "#77746a", 2.6),
    ribbon([(18, 43, .10), (27, 33, .72), (38, 31, .95), (50, 36, .60), (57, 43, .08)], 4.5, "nebula-cloud-sweep", "#4a4943", .46),
    ribbon([(25, 48, .10), (34, 42, .80), (44, 42, .70), (50, 47, .08)], 2.5, "nebula-cloud-fold", "#262522", .38, True),
    dab(33, 31, 3.0, 2.4, "#262522"),
    mass("M 12 16 L 14 21 L 19 22 L 15 25 L 14 30 L 11 25 L 7 23 L 11 21 Z", "#4a4943"),
    mass("M 57 12 L 59 16 L 63 18 L 59 20 L 57 25 L 55 20 L 51 18 L 55 16 Z", "#77746a", "ink-dry"),
])


# A parabolic dish, instrument body, antenna, and solar panel define a probe.
write("probe", [
    mass("M 31 17 C 41 16 49 22 51 31 C 43 35 34 34 27 27 C 25 23 27 19 31 17 Z", "#77746a", "ink-dry"),
    contour("M 28 18 C 36 25 43 29 51 31", "#262522", 2.1),
    ribbon([(41, 29, .12), (39, 37, .72), (38, 44, .08)], 2.0, "probe-dish-mast", "#262522"),
    mass("M 30 42 C 35 39 44 40 48 44 L 47 55 C 43 59 34 59 29 55 Z", "#4a4943"),
    contour("M 29 44 L 48 44 L 47 56 L 29 55 Z", "#262522", 1.5),
    mass("M 9 43 L 27 43 L 27 54 L 9 54 Z", "#77746a", "ink-dry"),
    contour("M 15 43 L 15 54 M 21 43 L 21 54 M 9 48 L 27 48", "#4a4943", 1.0),
    ribbon([(40, 42, .12), (49, 37, .72), (57, 31, .08)], 1.4, "probe-antenna", "#262522"),
    dab(58, 30, 2.0, 2.0, "#262522"),
])


print("redrew meteor, eclipse, nebula, and probe as recognizable cosmos brush studies")
