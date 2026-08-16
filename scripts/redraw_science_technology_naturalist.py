#!/usr/bin/env python3
"""Redraw technology, making, and systems glyphs as naturalist sumi-e."""

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


def ground(name: str, y=62) -> str:
    return r([(7, y, .1), (29, y - 3, .85), (63, y - 1, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def ring(name: str, cx=36, cy=35, rx=16, ry=16, color="#77746a", width=1.6) -> str:
    return r([
        (cx-rx, cy+4, .1), (cx-rx, cy-7, .75), (cx-rx/2, cy-ry+1, .9),
        (cx+3, cy-ry, .85), (cx+rx-1, cy-7, .9), (cx+rx, cy+5, .8),
        (cx+rx/2, cy+ry-1, .9), (cx-3, cy+ry, .85), (cx-rx+1, cy+7, .08)
    ], width, name, color, dry=color != "#262522")


def wheel(name: str, cx=36, cy=36, radius=15) -> list[str]:
    return [
        ring(f"{name}-rim", cx, cy, radius, radius, "#77746a", 1.7),
        dab(cx, cy, 3.5, 3.5),
        r([(cx, cy-radius+2, .1), (cx, cy, .8), (cx+radius-1, cy+1, .08)], .8, f"{name}-spoke-a", "#bcb9af", dry=True),
        r([(cx-radius+2, cy+2, .1), (cx, cy, .8), (cx+2, cy+radius-1, .08)], .65, f"{name}-spoke-b", "#77746a", dry=True),
    ]


def leaf(name: str, x: float, y: float, flip=False, color="#4a4943") -> list[str]:
    s = -1 if flip else 1
    return [
        m(f"M {x} {y} C {x+7*s} {y-8} {x+17*s} {y-7} {x+21*s} {y-2} C {x+15*s} {y+5} {x+6*s} {y+6} {x} {y} Z", color),
        r([(x+2*s, y, .1), (x+10*s, y-2, .75), (x+18*s, y-3, .08)], .6, f"{name}-vein", "#bcb9af", dry=True),
    ]


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e technology study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "algorithm": [
        dab(12, 18, 3.4, 3.4), dab(36, 18, 3.0, 3.0, "#77746a"), dab(59, 18, 2.7, 2.7, "#4a4943"),
        dab(24, 49, 3.0, 3.0, "#4a4943"), dab(50, 49, 2.6, 2.6, "#77746a"),
        r([(15, 19, .1), (27, 18, .8), (33, 18, .08)], 1.2, "algorithm-a"),
        r([(39, 19, .1), (50, 18, .8), (56, 18, .08)], .8, "algorithm-b", "#77746a", dry=True),
        r([(36, 22, .1), (31, 35, .8), (25, 46, .08)], 1.0, "algorithm-c"),
        r([(38, 22, .1), (44, 35, .8), (49, 46, .08)], .65, "algorithm-d", "#bcb9af", dry=True), ground("algorithm", 63),
    ],
    "architecture": [
        r([(7, 59, .1), (7, 35, .8), (22, 19, .9), (36, 35, .08)], 2.0, "architecture-left"),
        r([(36, 35, .1), (50, 20, .8), (65, 35, .9), (64, 59, .08)], 1.4, "architecture-right", "#77746a", dry=True),
        r([(22, 59, .1), (22, 38, .75), (23, 22, .08)], 1.2, "architecture-post-a"),
        r([(50, 59, .1), (50, 38, .75), (51, 23, .08)], .7, "architecture-post-b", "#bcb9af", dry=True), ground("architecture", 64),
    ],
    "code": [
        r([(26, 17, .1), (15, 28, .8), (7, 37, .9), (16, 46, .8), (26, 55, .08)], 2.4, "code-left"),
        r([(46, 17, .1), (57, 28, .8), (65, 37, .9), (56, 46, .8), (46, 55, .08)], 1.5, "code-right", "#77746a", dry=True),
        r([(42, 12, .1), (36, 34, .8), (29, 60, .08)], 1.2, "code-slash", "#bcb9af", dry=True), ground("code", 65),
    ],
    "craft": [
        r([(10, 55, .1), (25, 42, .75), (42, 27, .9), (58, 12, .08)], 2.8, "craft-tool"),
        m("M 54 8 L 66 13 L 59 22 L 49 16 Z", "#77746a"),
        r([(14, 42, .1), (27, 48, .8), (39, 43, .08)], 1.4, "craft-hand"),
        r([(9, 63, .1), (29, 59, .8), (59, 62, .08)], .65, "craft-ground", "#bcb9af", dry=True),
    ],
    "data": [
        dab(12, 22, 3.2, 3.2), dab(28, 18, 2.7, 2.7, "#77746a"), dab(45, 23, 3.0, 3.0, "#4a4943"), dab(61, 18, 2.3, 2.3, "#bcb9af"),
        dab(19, 42, 2.5, 2.5, "#77746a"), dab(37, 39, 3.2, 3.2), dab(55, 44, 2.7, 2.7, "#77746a"),
        r([(11, 55, .1), (29, 51, .8), (48, 55, .9), (63, 50, .08)], 1.0, "data-thread", "#77746a", dry=True), ground("data", 64),
    ],
    "design": [
        r([(9, 55, .1), (22, 44, .8), (35, 47, .9), (47, 32, .8), (61, 35, .08)], 2.2, "design-line"),
        r([(14, 20, .1), (28, 16, .8), (43, 20, .08)], 1.0, "design-guide-a", "#77746a", dry=True),
        r([(28, 10, .1), (28, 18, .75), (29, 28, .08)], .65, "design-guide-b", "#bcb9af", dry=True),
        dab(10, 55, 3.0, 3.0), dab(61, 35, 2.4, 2.4, "#77746a"), ground("design", 64),
    ],
    "emergence": [
        r([(36, 61, .1), (35, 48, .8), (37, 36, .08)], 2.3, "emergence-stem"),
        *leaf("emergence", 36, 43, True, "#4a4943"),
        r([(8, 46, .1), (20, 40, .8), (31, 44, .08)], 1.1, "emergence-water-a", "#77746a", dry=True),
        r([(9, 55, .1), (23, 50, .8), (34, 54, .08)], .65, "emergence-water-b", "#bcb9af", dry=True),
        dab(58, 23, 2.3, 2.3, "#77746a"), ground("emergence", 64),
    ],
    "engine": [
        r([(11, 49, .1), (12, 31, .75), (24, 24, .9), (43, 27, .75), (45, 49, .08)], 3.0, "engine-boiler"),
        r([(44, 49, .1), (44, 19, .75), (58, 19, .9), (59, 49, .08)], 2.2, "engine-cab", "#77746a"),
        m("M 18 11 L 29 11 L 27 27 L 20 27 Z", "#4a4943"),
        r([(8, 50, .1), (31, 48, .85), (62, 50, .08)], 2.2, "engine-chassis"),
        dab(21, 54, 5.7, 5.7), dab(47, 54, 5.7, 5.7, "#4a4943"),
        dab(53, 28, 3.2, 3.6, "#262522"),
        r([(58, 49, .1), (64, 54, .75), (68, 58, .08)], 1.5, "engine-cowcatcher", "#77746a"),
        ground("engine", 64),
    ],
    "engineering": [
        r([(7, 57, .1), (19, 39, .8), (31, 56, .9), (43, 36, .8), (64, 56, .08)], 2.1, "engineering-truss"),
        r([(8, 57, .1), (35, 53, .85), (64, 56, .08)], 1.5, "engineering-deck"),
        *wheel("engineering-wheel", 51, 23, 9),
        r([(14, 64, .1), (33, 60, .8), (61, 63, .08)], .65, "engineering-ground", "#bcb9af", dry=True),
    ],
    "feedback": [
        r([(17, 51, .1), (10, 39, .75), (13, 25, .9), (25, 16, .8), (40, 15, .9), (54, 23, .8), (61, 36, .08)], 2.1, "feedback-forward"),
        m("M 56 31 L 66 37 L 58 44 Z", "#4a4943"),
        r([(56, 48, .1), (45, 57, .8), (30, 60, .9), (17, 52, .08)], 1.0, "feedback-return", "#77746a", dry=True),
        m("M 21 47 L 11 52 L 20 59 Z", "#77746a"), dab(36, 36, 2.3, 2.3, "#bcb9af"),
    ],
    "innovation": [
        r([(16, 59, .1), (28, 48, .8), (38, 35, .9), (53, 23, .08)], 2.3, "innovation-rise"),
        m("M 49 17 L 64 20 L 56 31 Z", "#4a4943"),
        *leaf("innovation", 30, 42, True, "#77746a"),
        dab(12, 54, 2.4, 2.4, "#bcb9af"), ground("innovation", 64),
    ],
    "interface": [
        r([(35, 8, .1), (34, 31, .8), (36, 63, .08)], 1.6, "interface-boundary", "#77746a", dry=True),
        m("M 6 33 C 13 24 25 22 33 28 C 28 38 17 43 7 39 Z", "#4a4943"),
        r([(39, 47, .1), (49, 39, .8), (63, 42, .08)], 1.6, "interface-hand"),
        r([(39, 39, .1), (48, 33, .75), (57, 34, .08)], .65, "interface-touch", "#bcb9af", dry=True), ground("interface", 65),
    ],
    "invention": [
        *wheel("invention-wheel", 30, 42, 13),
        r([(39, 31, .1), (48, 22, .75), (58, 13, .08)], 2.0, "invention-lift"),
        m("M 54 8 L 66 12 L 59 21 Z", "#4a4943"),
        dab(12, 18, 2.2, 2.2, "#bcb9af"), ground("invention", 64),
    ],
    "labor": [
        r([(10, 56, .1), (23, 44, .75), (38, 30, .9), (55, 14, .08)], 3.0, "labor-handle"),
        m("M 50 9 L 65 15 L 58 25 L 44 18 Z", "#4a4943"),
        r([(10, 43, .1), (21, 48, .8), (32, 43, .08)], 1.3, "labor-hand"), ground("labor", 64),
    ],
    "network": [
        dab(10, 20, 3.4, 3.4), dab(36, 13, 3.0, 3.0, "#77746a"), dab(62, 22, 3.2, 3.2),
        dab(22, 50, 3.0, 3.0, "#4a4943"), dab(51, 51, 2.8, 2.8, "#77746a"),
        r([(13, 20, .1), (25, 16, .8), (33, 14, .08)], 1.1, "network-a"),
        r([(39, 14, .1), (52, 18, .8), (59, 21, .08)], .8, "network-b", "#77746a", dry=True),
        r([(12, 23, .1), (17, 36, .8), (21, 47, .08)], 1.0, "network-c"),
        r([(25, 49, .1), (37, 50, .8), (48, 51, .08)], .65, "network-d", "#bcb9af", dry=True),
        r([(60, 24, .1), (56, 37, .8), (52, 48, .08)], .8, "network-e", "#77746a", dry=True), ground("network", 64),
    ],
    "production": [
        *wheel("production-wheel", 24, 44, 12),
        *wheel("production-wheel-b", 49, 38, 10),
        r([(7, 59, .1), (28, 55, .8), (60, 58, .08)], 1.3, "production-belt"),
        dab(61, 23, 2.4, 2.4, "#bcb9af"), ground("production", 64),
    ],
    "program": [
        r([(9, 15, .1), (9, 37, .8), (10, 59, .08)], 1.6, "program-left"),
        r([(62, 14, .1), (61, 37, .8), (62, 58, .08)], .9, "program-right", "#77746a", dry=True),
        dab(22, 25, 3.0, 3.0), dab(36, 36, 3.0, 3.0, "#4a4943"), dab(50, 47, 2.7, 2.7, "#77746a"),
        r([(22, 25, .1), (36, 36, .8), (50, 47, .08)], .7, "program-thread", "#bcb9af", dry=True), ground("program", 64),
    ],
    "return": [
        r([(61, 25, .1), (48, 17, .75), (32, 18, .9), (18, 28, .8), (13, 43, .9), (22, 56, .8), (39, 59, .08)], 2.2, "return-loop"),
        m("M 54 18 L 65 25 L 55 33 Z", "#4a4943"),
        r([(20, 63, .1), (35, 59, .8), (53, 62, .08)], .65, "return-ground", "#bcb9af", dry=True),
    ],
    "sequence": [
        dab(10, 36, 3.3, 3.3), dab(27, 34, 3.0, 3.0, "#77746a"), dab(44, 36, 2.8, 2.8, "#4a4943"),
        r([(14, 36, .1), (27, 32, .8), (43, 35, .9), (57, 32, .08)], 1.8, "sequence-line"),
        m("M 54 25 L 67 32 L 55 40 Z", "#77746a"), ground("sequence"),
    ],
    "server": [
        r([(15, 59, .1), (15, 15, .75), (57, 15, .9), (57, 59, .75), (15, 59, .08)], 2.5, "server-rack"),
        r([(16, 28, .1), (36, 26, .85), (56, 28, .08)], 2.0, "server-shelf-a"),
        r([(16, 42, .1), (36, 40, .85), (56, 42, .08)], 1.8, "server-shelf-b", "#77746a"),
        dab(23, 22, 2.2, 2.2), dab(31, 22, 1.7, 1.7, "#77746a"),
        dab(23, 35, 2.1, 2.1, "#4a4943"), dab(31, 35, 1.6, 1.6, "#bcb9af"),
        dab(23, 50, 2.0, 2.0), dab(31, 50, 1.6, 1.6, "#77746a"),
        r([(40, 22, .1), (51, 21, .08)], 1.2, "server-slot-a", "#77746a", dry=True),
        r([(40, 35, .1), (51, 34, .08)], 1.2, "server-slot-b", "#bcb9af", dry=True),
        r([(40, 50, .1), (51, 49, .08)], 1.2, "server-slot-c", "#77746a", dry=True),
        ground("server", 64),
    ],
    "signal": [
        dab(19, 39, 4.0, 4.0),
        r([(24, 39, .1), (32, 31, .75), (34, 21, .08)], 1.5, "signal-a"),
        r([(25, 43, .1), (38, 38, .75), (46, 27, .08)], 1.0, "signal-b", "#77746a", dry=True),
        r([(24, 48, .1), (41, 47, .75), (57, 38, .08)], .65, "signal-c", "#bcb9af", dry=True), ground("signal"),
    ],
    "skill": [
        r([(9, 51, .1), (22, 43, .8), (34, 47, .9), (47, 37, .8), (61, 40, .08)], 2.1, "skill-hand"),
        r([(36, 37, .1), (43, 27, .75), (53, 17, .08)], 2.4, "skill-tool"),
        m("M 49 12 L 62 16 L 55 25 Z", "#77746a"),
        r([(11, 62, .1), (29, 58, .8), (57, 61, .08)], .65, "skill-ground", "#bcb9af", dry=True),
    ],
    "spark": [
        r([(36, 7, .1), (35, 25, .8), (36, 37, .08)], 2.2, "spark-n"),
        r([(36, 37, .1), (35, 51, .8), (36, 64, .08)], 1.2, "spark-s", "#77746a", dry=True),
        r([(7, 36, .1), (23, 33, .8), (36, 37, .08)], 1.7, "spark-w"),
        r([(36, 37, .1), (51, 33, .8), (66, 36, .08)], .8, "spark-e", "#bcb9af", dry=True),
        r([(16, 15, .1), (26, 25, .8), (36, 37, .08)], .7, "spark-nw", "#bcb9af", dry=True),
        r([(36, 37, .1), (47, 25, .8), (58, 15, .08)], 1.0, "spark-ne", "#77746a", dry=True), dab(36, 37, 3.5, 3.5),
    ],
    "technology": [
        *wheel("technology-wheel", 29, 42, 13),
        r([(44, 58, .1), (44, 42, .75), (46, 27, .08)], 1.6, "technology-stem"),
        *leaf("technology", 45, 34, False, "#4a4943"),
        r([(8, 64, .1), (29, 60, .8), (62, 63, .08)], .65, "technology-ground", "#bcb9af", dry=True),
    ],
    "threshold": [
        r([(12, 60, .1), (12, 38, .8), (15, 18, .9), (36, 10, .85), (57, 18, .9), (60, 39, .8), (59, 60, .08)], 2.0, "threshold-door"),
        r([(36, 12, .1), (35, 35, .8), (36, 60, .08)], 1.1, "threshold-line", "#77746a", dry=True),
        r([(16, 62, .1), (35, 58, .8), (57, 61, .08)], .65, "threshold-ground", "#bcb9af", dry=True),
        dab(50, 37, 2.2, 2.2, "#4a4943"),
    ],
    "tool": [
        r([(10, 57, .1), (24, 44, .75), (41, 28, .9), (59, 11, .08)], 3.0, "tool-handle"),
        m("M 54 7 L 67 12 L 60 22 L 48 16 Z", "#4a4943"),
        r([(9, 64, .1), (28, 60, .8), (59, 63, .08)], .65, "tool-ground", "#bcb9af", dry=True),
    ],
    "transformation": [
        m("M 7 48 C 14 38 25 36 33 43 C 28 52 17 56 8 52 Z", "#4a4943"),
        r([(32, 44, .1), (40, 36, .75), (48, 28, .08)], 1.6, "transformation-rise"),
        *leaf("transformation", 49, 29, False, "#77746a"),
        r([(9, 61, .1), (29, 57, .8), (61, 60, .08)], .65, "transformation-ground", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} science technology/systems glyphs as sumi-e studies")
