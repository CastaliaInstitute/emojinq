#!/usr/bin/env python3
"""Redraw all rocket-family PUA glyphs for recognition at toddler scale."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "rockets"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522", wobble=.26, dry=False) -> str:
    return svg_path(
        stroke_path(points(*values), width=max(width, 1.15), seed=seed, wobble=wobble),
        fill=color,
        class_name="ink-dry" if dry else "ink-wash",
    )


def mass(d: str, color="#3f3e39", role="ink-wash") -> str:
    return f'<path class="{role}" fill="{color}" d="{d}" data-ink-brush-pass="loaded-mass-v2"/>'


def contour(d: str, color="#77746a", width=1.6) -> str:
    return (
        f'<path class="ink-dry" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" d="{d}" '
        'data-ink-brush-pass="dry-contour-v2"/>'
    )


def dab(cx, cy, rx, ry, color="#262522", role="ink-wash") -> str:
    return f'<ellipse class="{role}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'


def group(transform: str, marks: list[str]) -> str:
    return f'<g transform="{transform}">{"".join(marks)}</g>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text(encoding="utf-8")
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="rockets / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>rockets / {name} — recognizable sumi-e machine study</title>{''.join(marks)}</svg>
''',
        encoding="utf-8",
    )


def upright_rocket(prefix: str, narrow=False) -> list[str]:
    half = 4 if narrow else 6
    left, right = 36 - half, 36 + half
    return [
        mass(f"M 36 9 C {left + 1} 14 {left} 22 {left} 30 L {left} 49 C 32 52 40 52 {right} 49 L {right} 30 C {right} 21 {right - 1} 14 36 9 Z", "#4a4943"),
        mass(f"M {left} 39 L {left - 8} 50 L {left} 47 Z M {right} 39 L {right + 8} 50 L {right} 47 Z", "#262522"),
        dab(36, 27, 2.5 if narrow else 3.3, 2.5 if narrow else 3.3, "#77746a", "ink-dry"),
        contour(f"M {left + 1} 37 C 34 39 38 39 {right - 1} 37", "#b2afa6", 1.2),
        ribbon([(36, 49, .12), (33, 57, .78), (36, 66, .08)], 3.2 if narrow else 4.5, f"{prefix}-flame", "#262522", .36),
        ribbon([(39, 50, .12), (42, 57, .66), (40, 63, .08)], 1.4, f"{prefix}-flame-dry", "#77746a", .32, True),
    ]


write("sounding-rocket", upright_rocket("sounding", True))


write("orbital-rocket", [
    group("rotate(43 36 36) translate(0 -2)", upright_rocket("orbital", False)),
    ribbon([(13, 59, .08), (20, 55, .76), (25, 49, .08)], 1.3, "orbital-exhaust-wisp", "#77746a", .35, True),
])


write("booster", [
    group("translate(-9 6) scale(.82)", upright_rocket("booster-left", True)[:-2]),
    group("translate(9 6) scale(.82)", upright_rocket("booster-right", True)[:-2]),
    group("translate(0 -2) scale(.92)", upright_rocket("booster-core", True)[:-2]),
    ribbon([(27, 51, .10), (24, 58, .72), (26, 66, .08)], 2.3, "booster-left-flame", "#4a4943", .34),
    ribbon([(36, 48, .10), (34, 58, .82), (37, 68, .08)], 3.3, "booster-core-flame", "#262522", .36),
    ribbon([(45, 51, .10), (48, 58, .72), (46, 65, .08)], 1.8, "booster-right-flame", "#77746a", .34, True),
])


write("launch", [
    group("translate(0 -5) scale(.88 1.0)", upright_rocket("launch", False)[:-2]),
    ribbon([(36, 44, .10), (32, 54, .82), (35, 64, .08)], 4.6, "launch-flame", "#262522", .38),
    mass("M 10 61 C 13 54 21 53 26 58 C 30 52 39 53 42 58 C 49 53 59 56 62 62 C 49 65 24 66 10 61 Z", "#77746a", "ink-dry"),
    contour("M 17 52 L 17 19 M 13 25 L 21 25 M 13 37 L 21 37 M 13 49 L 21 49", "#4a4943", 1.8),
])


write("capsule", [
    mass("M 15 24 C 20 10 50 8 58 23 C 48 28 27 29 15 24 Z", "#77746a", "ink-dry"),
    contour("M 17 23 C 27 17 46 17 57 22", "#4a4943", 1.3),
    ribbon([(22, 25, .10), (28, 39, .72), (31, 47, .08)], 1.3, "capsule-cord-left", "#77746a", .22, True),
    ribbon([(51, 25, .10), (44, 39, .72), (41, 47, .08)], 1.3, "capsule-cord-right", "#77746a", .22, True),
    mass("M 30 44 C 33 41 40 41 43 44 L 48 58 C 42 63 30 63 25 58 Z", "#4a4943"),
    mass("M 25 57 C 31 59 41 59 48 56 L 47 61 C 40 65 31 65 26 61 Z", "#262522"),
    dab(36, 50, 2.5, 2.5, "#77746a", "ink-dry"),
])


write("lunar-lander", [
    mass("M 26 28 C 31 23 43 23 48 29 L 47 42 C 42 47 30 47 25 42 Z", "#4a4943"),
    mass("M 29 29 L 36 25 L 43 29 L 42 36 L 30 36 Z", "#77746a", "ink-dry"),
    ribbon([(28, 42, .10), (21, 51, .75), (14, 58, .08)], 2.2, "lander-left-leg", "#262522", .28),
    ribbon([(44, 42, .10), (51, 51, .75), (59, 57, .08)], 1.8, "lander-right-leg", "#4a4943", .28),
    ribbon([(14, 58, .10), (9, 59, .74), (6, 58, .08)], 1.6, "lander-left-foot", "#262522", .25),
    ribbon([(58, 57, .10), (63, 59, .74), (67, 58, .08)], 1.4, "lander-right-foot", "#77746a", .25, True),
    ribbon([(36, 24, .10), (36, 16, .75), (42, 12, .08)], 1.5, "lander-antenna", "#262522", .28),
    dab(44, 11, 2.0, 1.5, "#77746a", "ink-dry"),
    contour("M 8 63 C 22 60 43 64 65 60", "#77746a", 1.2),
])


write("mission-control", [
    contour("M 12 13 L 60 13 L 58 40 L 14 40 Z", "#4a4943", 2.4),
    group("translate(20 -2) scale(.45)", upright_rocket("control-screen", True)[:4]),
    ribbon([(29, 31, .10), (37, 24, .70), (48, 20, .08)], 1.5, "control-trajectory", "#4a4943", .30, True),
    ribbon([(10, 52, .08), (25, 48, .72), (43, 50, .92), (62, 47, .08)], 4.4, "control-console", "#4a4943", .30),
    dab(22, 45, 3.2, 3.4, "#262522"),
    dab(49, 45, 3.0, 3.2, "#262522"),
    contour("M 18 53 L 27 53 M 44 53 L 54 53", "#b2afa6", 1.5),
])


write("rover", [
    mass("M 15 37 C 23 33 45 33 53 38 L 51 49 L 17 49 Z", "#4a4943"),
    contour("M 20 39 L 47 39 M 25 44 L 45 44", "#b2afa6", 1.2),
    dab(20, 53, 5.0, 5.0, "#262522"),
    dab(36, 53, 5.0, 5.0, "#262522"),
    dab(51, 52, 4.3, 4.3, "#262522"),
    ribbon([(35, 35, .10), (35, 25, .74), (33, 17, .08)], 2.0, "rover-mast", "#262522", .28),
    mass("M 27 14 L 41 14 L 43 20 L 29 21 Z", "#262522"),
    dab(38, 17, 1.4, 1.4, "#f3f0e6", "ink-dry"),
    ribbon([(51, 38, .10), (60, 31, .74), (65, 25, .08)], 1.7, "rover-arm", "#77746a", .30, True),
    contour("M 8 61 C 22 58 42 62 64 57", "#77746a", 1.2),
])


write("satellite", [
    mass("M 29 27 L 43 27 L 47 43 L 32 47 L 26 36 Z", "#4a4943"),
    mass("M 5 25 L 25 29 L 24 42 L 4 38 Z", "#77746a", "ink-dry"),
    mass("M 47 29 L 67 25 L 68 38 L 48 42 Z", "#77746a", "ink-dry"),
    contour("M 11 27 L 10 39 M 18 28 L 17 40 M 54 28 L 55 40 M 61 27 L 62 39", "#4a4943", 1.0),
    contour("M 28 34 C 34 28 42 29 47 34", "#b2afa6", 1.2),
    ribbon([(37, 28, .10), (38, 19, .74), (44, 13, .08)], 1.6, "satellite-antenna", "#262522", .28),
    mass("M 41 13 C 47 10 53 12 55 17 C 49 19 45 17 41 13 Z", "#77746a", "ink-dry"),
])


write("space-station", [
    ribbon([(7, 36, .08), (25, 35, .70), (45, 37, .95), (66, 35, .08)], 2.2, "station-truss", "#262522", .28),
    mass("M 25 28 L 47 28 L 51 44 L 23 44 Z", "#4a4943"),
    dab(28, 36, 5.5, 5.5, "#77746a", "ink-dry"),
    dab(43, 36, 5.5, 5.5, "#77746a", "ink-dry"),
    contour("M 5 20 L 24 23 L 22 32 L 4 29 Z M 48 22 L 68 19 L 68 29 L 50 32 Z", "#77746a", 1.25),
    contour("M 5 43 L 23 40 L 24 50 L 6 53 Z M 49 41 L 68 44 L 67 54 L 48 50 Z", "#77746a", 1.25),
    contour("M 12 21 L 11 30 M 18 22 L 17 31 M 55 21 L 56 31 M 62 20 L 63 30 M 12 42 L 13 52 M 18 41 L 19 51 M 55 42 L 54 51 M 62 43 L 61 53", "#4a4943", .8),
    ribbon([(36, 28, .10), (37, 18, .72), (42, 14, .08)], 1.4, "station-docking", "#262522", .26),
])


print("redrew 10 rocket glyphs for toddler recognition")
