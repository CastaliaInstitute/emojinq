#!/usr/bin/env python3
"""Redraw foundational number, arithmetic, and measurement science glyphs."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "science"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def r(values, width, seed, color="#262522", *, dry=False) -> str:
    width = max(width * 1.35, 1.2)
    d = stroke_path(points(*values), width=width, seed=seed, wobble=.26, taper_start=.10, taper_end=.08)
    return (
        f'<path class="{"ink-dry" if dry else "ink-wash"}" d="{d}" fill="{color}" '
        f'data-ink-brush-pass="{"dry-edge-v2" if dry else "loaded-ribbon-v2"}"/>'
    )


def m(d: str, color="#4a4943") -> str:
    return f'<path class="ink-wash" d="{d}" fill="{color}" data-ink-brush-pass="loaded-mass-v2"/>'


def dab(cx, cy, rx=2.8, ry=2.8, color="#262522") -> str:
    return f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'


def baseline(name: str) -> str:
    return r([(9, 62, .1), (29, 59, .85), (60, 61, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def dots(name: str, positions: list[tuple[float, float]]) -> list[str]:
    colors = ("#262522", "#4a4943", "#77746a", "#262522", "#77746a", "#4a4943", "#262522", "#77746a", "#4a4943", "#262522")
    return [dab(x, y, 2.8, 2.8, colors[index]) for index, (x, y) in enumerate(positions)] + [baseline(name)]


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e mathematics study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "add": [
        r([(11, 36, .1), (34, 33, .9), (61, 36, .08)], 3.0, "add-horizontal"),
        r([(35, 10, .1), (34, 33, .8), (36, 59, .08)], 2.3, "add-vertical"),
        r([(18, 46, .1), (29, 43, .75), (41, 46, .08)], .65, "add-dry", "#bcb9af", dry=True),
    ],
    "balance": [
        r([(36, 9, .1), (35, 33, .75), (36, 62, .08)], 2.4, "balance-stem"),
        r([(10, 28, .1), (35, 24, .9), (62, 28, .08)], 2.2, "balance-beam"),
        r([(17, 28, .1), (14, 41, .75), (10, 50, .08)], .9, "balance-cord-a", "#77746a", dry=True),
        r([(56, 28, .1), (59, 40, .75), (63, 49, .08)], .7, "balance-cord-b", "#bcb9af", dry=True),
        r([(5, 51, .1), (13, 57, .75), (23, 51, .08)], 1.5, "balance-pan-a"),
        r([(51, 50, .1), (60, 56, .75), (68, 50, .08)], 1.0, "balance-pan-b", "#77746a", dry=True),
        r([(27, 64, .1), (36, 61, .75), (46, 64, .08)], .65, "balance-base", "#bcb9af", dry=True),
    ],
    "compare": [
        m("M 9 30 C 14 21 27 19 35 26 C 29 34 18 37 9 30 Z", "#4a4943"),
        m("M 38 43 C 46 34 59 34 65 42 C 58 50 46 52 38 43 Z", "#77746a"),
        r([(25, 44, .1), (35, 36, .75), (46, 28, .08)], 1.3, "compare-axis"),
        r([(12, 58, .1), (30, 55, .8), (55, 58, .08)], .65, "compare-ground", "#bcb9af", dry=True),
    ],
    "count": [
        dab(15, 24), dab(29, 24, color="#4a4943"), dab(43, 24, color="#77746a"), dab(57, 24),
        r([(12, 38, .1), (27, 35, .8), (45, 38, .9), (61, 34, .08)], 1.5, "count-thread"),
        r([(15, 44, .1), (15, 54, .75), (16, 61, .08)], .8, "count-tally-a", "#77746a", dry=True),
        r([(36, 43, .1), (36, 53, .75), (37, 60, .08)], .65, "count-tally-b", "#bcb9af", dry=True),
        baseline("count"),
    ],
    "divide": [
        r([(11, 36, .1), (34, 33, .9), (61, 36, .08)], 3.0, "divide-bar"),
        dab(36, 17, 3.5, 3.5), dab(35, 54, 3.2, 3.2, "#77746a"),
        r([(20, 44, .1), (32, 41, .75), (45, 44, .08)], .65, "divide-dry", "#bcb9af", dry=True),
    ],
    "eight": dots("eight", [(27, 16), (45, 16), (27, 29), (45, 29), (27, 42), (45, 42), (27, 55), (45, 55)]),
    "equal": [
        r([(11, 28, .1), (34, 25, .9), (61, 28, .08)], 2.8, "equal-top"),
        r([(11, 45, .1), (34, 42, .9), (61, 45, .08)], 1.8, "equal-bottom", "#77746a", dry=True),
        r([(20, 55, .1), (34, 52, .75), (49, 55, .08)], .65, "equal-breath", "#bcb9af", dry=True),
    ],
    "five": dots("five", [(24, 20), (48, 20), (36, 36), (24, 52), (48, 52)]),
    "four": dots("four", [(25, 22), (47, 22), (25, 48), (47, 48)]),
    "fraction": [
        r([(14, 57, .1), (27, 43, .75), (42, 28, .9), (57, 12, .08)], 2.8, "fraction-slash"),
        dab(20, 22, 4.0, 4.0), dab(52, 49, 3.7, 3.7, "#77746a"),
        r([(8, 63, .1), (27, 60, .8), (58, 62, .08)], .65, "fraction-ground", "#bcb9af", dry=True),
    ],
    "infinity": [
        r([(8, 37, .1), (16, 25, .75), (28, 25, .9), (36, 36, .9), (44, 47, .9), (56, 47, .75), (64, 36, .9), (56, 25, .75), (44, 25, .9), (36, 36, .9), (28, 47, .9), (16, 47, .75), (8, 37, .08)], 2.5, "infinity-loop"),
        r([(17, 56, .1), (34, 53, .8), (54, 56, .08)], .65, "infinity-ground", "#bcb9af", dry=True),
    ],
    "less": [
        r([(58, 15, .1), (43, 26, .75), (26, 37, .9), (43, 48, .75), (58, 57, .08)], 3.0, "less-mark"),
        dab(14, 37, 2.8, 2.8, "#77746a"),
        r([(12, 63, .1), (31, 60, .8), (57, 62, .08)], .65, "less-ground", "#bcb9af", dry=True),
    ],
    "many": [
        dab(12, 20), dab(26, 16, color="#4a4943"), dab(41, 20, color="#77746a"), dab(57, 16),
        dab(18, 34, color="#77746a"), dab(34, 32), dab(50, 35, color="#4a4943"),
        dab(12, 49), dab(28, 51, color="#77746a"), dab(45, 49, color="#4a4943"), dab(61, 52),
        r([(8, 62, .1), (30, 59, .85), (63, 61, .08)], .65, "many-ground", "#bcb9af", dry=True),
    ],
    "measure": [
        r([(9, 51, .1), (25, 38, .75), (41, 25, .9), (59, 11, .08)], 3.0, "measure-rule"),
        r([(20, 41, .1), (25, 46, .75), (28, 49, .08)], .8, "measure-tick-a", "#77746a", dry=True),
        r([(33, 30, .1), (38, 35, .75), (41, 38, .08)], .7, "measure-tick-b", "#bcb9af", dry=True),
        r([(46, 19, .1), (51, 24, .75), (54, 27, .08)], .65, "measure-tick-c", "#77746a", dry=True),
        r([(8, 63, .1), (28, 60, .85), (59, 62, .08)], .65, "measure-ground", "#bcb9af", dry=True),
    ],
    "more": [
        r([(14, 15, .1), (29, 26, .75), (46, 37, .9), (29, 48, .75), (14, 57, .08)], 3.0, "more-mark"),
        dab(59, 37, 3.2, 3.2, "#77746a"),
        r([(12, 63, .1), (31, 60, .8), (60, 62, .08)], .65, "more-ground", "#bcb9af", dry=True),
    ],
    "multiply": [
        r([(13, 13, .1), (34, 34, .85), (59, 59, .08)], 3.2, "multiply-a"),
        r([(59, 12, .1), (36, 34, .85), (13, 59, .08)], 2.0, "multiply-b", "#77746a", dry=True),
        dab(36, 35, 2.0, 2.0, "#bcb9af"),
    ],
    "nine": dots("nine", [(22, 17), (36, 17), (50, 17), (22, 34), (36, 34), (50, 34), (22, 51), (36, 51), (50, 51)]),
    "none": [
        r([(14, 48, .1), (12, 34, .75), (20, 21, .9), (34, 16, .85), (48, 22, .75), (56, 36, .9), (51, 50, .75), (37, 57, .9), (23, 53, .75), (14, 48, .08)], 2.2, "none-ring"),
        r([(16, 55, .1), (28, 43, .75), (42, 29, .9), (55, 16, .08)], 2.4, "none-slash"),
        r([(20, 62, .1), (35, 59, .75), (51, 61, .08)], .65, "none-ground", "#bcb9af", dry=True),
    ],
    "one": [
        r([(35, 11, .1), (34, 34, .8), (36, 60, .08)], 3.2, "one-stroke"),
        r([(22, 63, .1), (35, 60, .75), (49, 63, .08)], .65, "one-ground", "#bcb9af", dry=True),
    ],
    "scale": [
        r([(36, 10, .1), (35, 34, .75), (36, 62, .08)], 2.3, "scale-stem"),
        r([(10, 29, .1), (35, 25, .9), (62, 29, .08)], 2.0, "scale-beam"),
        r([(18, 29, .1), (14, 42, .75), (10, 50, .08)], .8, "scale-cord-a", "#77746a", dry=True),
        r([(55, 29, .1), (59, 41, .75), (63, 49, .08)], .65, "scale-cord-b", "#bcb9af", dry=True),
        m("M 5 51 C 10 46 19 46 24 51 C 20 57 10 59 5 51 Z", "#4a4943"),
        m("M 50 50 C 55 45 64 45 68 50 C 64 56 55 58 50 50 Z", "#77746a"),
        r([(27, 64, .1), (36, 61, .75), (46, 64, .08)], .65, "scale-base", "#bcb9af", dry=True),
    ],
    "seven": dots("seven", [(18, 18), (36, 18), (54, 18), (14, 39), (29, 39), (44, 39), (59, 39)]),
    "shape": [
        r([(8, 51, .1), (18, 34, .75), (28, 51, .08)], 2.0, "shape-triangle"),
        r([(36, 43, .1), (35, 32, .75), (42, 24, .9), (53, 24, .75), (60, 33, .9), (58, 44, .75), (49, 50, .9), (39, 47, .08)], 1.5, "shape-circle", "#77746a", dry=True),
        r([(12, 61, .1), (34, 58, .85), (60, 60, .08)], .65, "shape-ground", "#bcb9af", dry=True),
    ],
    "six": dots("six", [(22, 20), (36, 20), (50, 20), (22, 45), (36, 45), (50, 45)]),
    "subtract": [
        r([(10, 36, .1), (34, 33, .9), (62, 36, .08)], 3.2, "subtract-bar"),
        r([(18, 47, .1), (33, 44, .75), (49, 47, .08)], .65, "subtract-dry", "#bcb9af", dry=True),
    ],
    "ten": dots("ten", [(19, 16), (34, 16), (49, 16), (19, 29), (34, 29), (49, 29), (19, 42), (34, 42), (49, 42), (34, 55)]),
    "three": [
        r([(16, 20, .1), (34, 17, .85), (55, 20, .08)], 2.8, "three-a"),
        r([(17, 36, .1), (35, 33, .85), (55, 36, .08)], 2.0, "three-b", "#77746a", dry=True),
        r([(18, 52, .1), (35, 49, .85), (54, 52, .08)], 1.2, "three-c", "#bcb9af", dry=True),
    ],
    "two": [
        r([(15, 26, .1), (34, 22, .85), (57, 26, .08)], 2.9, "two-a"),
        r([(16, 47, .1), (35, 43, .85), (56, 47, .08)], 1.6, "two-b", "#77746a", dry=True),
        r([(23, 58, .1), (35, 55, .75), (48, 58, .08)], .65, "two-ground", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} science math/measurement glyphs as sumi-e studies")
