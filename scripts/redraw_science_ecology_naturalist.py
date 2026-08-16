#!/usr/bin/env python3
"""Redraw physical-world and ecology science glyphs as naturalist sumi-e."""

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


def ground(name: str) -> str:
    return r([(7, 64, .1), (29, 61, .85), (62, 63, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e ecology study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "adaptation": [
        m("M 10 42 C 16 30 29 25 39 31 C 34 43 23 49 10 42 Z", "#4a4943"),
        m("M 38 38 C 46 27 59 25 66 33 C 60 44 50 49 39 43 Z", "#77746a"),
        r([(13, 42, .1), (25, 36, .75), (38, 33, .08)], .8, "adaptation-vein-a", "#bcb9af", dry=True),
        r([(40, 42, .1), (50, 36, .75), (61, 33, .08)], .65, "adaptation-vein-b", "#bcb9af", dry=True),
        r([(28, 54, .1), (37, 47, .75), (46, 53, .08)], 1.0, "adaptation-link", "#77746a", dry=True),
        ground("adaptation"),
    ],
    "climate": [
        dab(20, 20, 6.0, 6.0, "#4a4943"),
        m("M 31 35 C 36 27 46 26 51 32 C 58 29 66 34 65 41 C 54 46 41 46 31 41 Z", "#77746a"),
        r([(8, 50, .1), (22, 46, .8), (37, 49, .9), (54, 45, .08)], 1.5, "climate-wind-a"),
        r([(13, 58, .1), (28, 54, .8), (44, 58, .08)], .75, "climate-wind-b", "#bcb9af", dry=True),
        r([(11, 16, .1), (7, 12, .75), (4, 10, .08)], .65, "climate-ray", "#bcb9af", dry=True),
    ],
    "conservation": [
        r([(8, 52, .1), (20, 45, .8), (31, 49, .9), (40, 44, .08)], 2.3, "conservation-hand-a"),
        r([(64, 52, .1), (52, 45, .8), (42, 49, .9), (34, 44, .08)], 1.4, "conservation-hand-b", "#77746a", dry=True),
        r([(36, 45, .1), (36, 34, .75), (38, 21, .08)], 1.8, "conservation-stem"),
        m("M 37 29 C 29 21 20 21 14 26 C 20 35 29 38 37 33 Z", "#4a4943"),
        m("M 39 26 C 46 18 57 17 63 22 C 58 31 49 34 40 31 Z", "#77746a"),
        ground("conservation"),
    ],
    "current": [
        r([(6, 30, .1), (19, 24, .8), (34, 28, .9), (49, 22, .8), (64, 26, .08)], 2.3, "current-a"),
        r([(5, 43, .1), (20, 37, .8), (35, 42, .9), (51, 36, .8), (66, 40, .08)], 1.4, "current-b", "#77746a", dry=True),
        r([(9, 55, .1), (24, 50, .8), (40, 54, .9), (57, 49, .08)], .75, "current-c", "#bcb9af", dry=True),
        m("M 59 20 L 68 23 L 62 31 Z", "#4a4943"),
    ],
    "cycle": [
        r([(16, 52, .1), (9, 39, .75), (13, 25, .9), (25, 15, .85), (41, 13, .9), (55, 22, .75), (62, 36, .08)], 2.5, "cycle-forward"),
        m("M 57 31 L 66 37 L 58 44 Z", "#4a4943"),
        r([(56, 47, .1), (45, 57, .75), (30, 60, .9), (17, 53, .08)], 1.2, "cycle-return", "#77746a", dry=True),
        m("M 20 47 L 11 53 L 20 59 Z", "#77746a"),
        dab(36, 36, 2.2, 2.2, "#bcb9af"),
    ],
    "decay": [
        m("M 14 23 C 25 16 38 20 43 31 C 37 42 25 47 13 40 C 9 34 10 27 14 23 Z", "#77746a"),
        r([(15, 39, .1), (26, 33, .75), (41, 29, .08)], .9, "decay-vein", "#bcb9af", dry=True),
        r([(40, 33, .1), (47, 42, .75), (54, 53, .08)], 1.4, "decay-fall"),
        r([(53, 54, .1), (59, 58, .75), (65, 57, .08)], .65, "decay-fragment", "#bcb9af", dry=True),
        ground("decay"),
    ],
    "disaster": [
        r([(6, 57, .1), (18, 42, .75), (29, 27, .9), (39, 42, .75), (52, 57, .08)], 2.5, "disaster-mountain"),
        m("M 54 10 L 42 32 L 51 30 L 46 51 L 64 25 L 55 27 Z", "#262522"),
        r([(12, 61, .1), (26, 56, .75), (40, 61, .9), (57, 54, .08)], .8, "disaster-break", "#bcb9af", dry=True),
        dab(64, 52, 2.0, 2.0, "#77746a"),
    ],
    "ecosystem": [
        r([(21, 59, .1), (21, 43, .75), (23, 25, .08)], 2.5, "ecosystem-tree"),
        m("M 22 32 C 15 25 7 24 3 28 C 8 36 15 39 22 36 Z", "#4a4943"),
        m("M 24 29 C 32 21 42 20 48 25 C 43 34 34 38 25 34 Z", "#77746a"),
        r([(7, 55, .1), (21, 51, .8), (37, 55, .9), (54, 50, .08)], 1.4, "ecosystem-water"),
        dab(58, 20, 4.5, 4.5, "#77746a"),
        r([(43, 59, .1), (44, 48, .75), (46, 39, .08)], .9, "ecosystem-reed", "#77746a", dry=True),
        ground("ecosystem"),
    ],
    "evolution": [
        m("M 7 47 C 13 39 24 38 31 45 C 25 53 15 56 7 47 Z", "#4a4943"),
        r([(30, 47, .1), (38, 39, .75), (45, 32, .08)], 1.2, "evolution-rise"),
        r([(44, 32, .1), (48, 43, .75), (54, 51, .08)], 1.7, "evolution-leg-a"),
        r([(45, 33, .1), (55, 37, .75), (63, 36, .08)], 1.0, "evolution-arm", "#77746a", dry=True),
        dab(45, 26, 3.0, 3.2, "#77746a"),
        r([(9, 61, .1), (29, 58, .85), (62, 60, .08)], .65, "evolution-ground", "#bcb9af", dry=True),
    ],
    "extinction": [
        r([(11, 47, .1), (23, 39, .75), (36, 43, .9), (49, 35, .08)], 2.4, "extinction-bone"),
        dab(10, 47, 3.5, 3.5), dab(50, 34, 3.2, 3.2, "#77746a"),
        r([(18, 17, .1), (35, 33, .85), (58, 56, .08)], 2.0, "extinction-slash-a"),
        r([(57, 16, .1), (38, 34, .85), (18, 56, .08)], 1.1, "extinction-slash-b", "#77746a", dry=True),
        ground("extinction"),
    ],
    "flow": [
        r([(5, 26, .1), (19, 20, .8), (34, 24, .9), (49, 18, .8), (65, 22, .08)], 2.3, "flow-a"),
        r([(6, 40, .1), (21, 34, .8), (36, 39, .9), (52, 33, .8), (66, 37, .08)], 1.4, "flow-b", "#77746a", dry=True),
        r([(9, 54, .1), (24, 49, .8), (41, 53, .9), (58, 48, .08)], .75, "flow-c", "#bcb9af", dry=True),
        r([(58, 48, .1), (64, 44, .75), (68, 45, .08)], .65, "flow-lift", "#77746a", dry=True),
    ],
    "foodchain": [
        m("M 5 47 C 10 39 20 36 27 42 C 23 50 14 54 5 47 Z", "#4a4943"),
        r([(27, 44, .1), (34, 39, .75), (40, 36, .08)], 1.0, "foodchain-link-a"),
        dab(43, 35, 2.8, 2.8, "#77746a"),
        r([(46, 34, .1), (52, 29, .75), (57, 25, .08)], .8, "foodchain-link-b", "#77746a", dry=True),
        r([(55, 24, .1), (61, 20, .75), (67, 23, .08)], 1.2, "foodchain-bird"),
        r([(55, 25, .1), (60, 29, .75), (66, 28, .08)], .65, "foodchain-wing", "#bcb9af", dry=True),
        ground("foodchain"),
    ],
    "force": [
        r([(8, 49, .1), (24, 40, .75), (42, 29, .9), (59, 18, .08)], 3.2, "force-vector"),
        m("M 55 13 L 66 15 L 60 25 Z", "#262522"),
        m("M 46 50 C 50 42 61 39 67 45 C 64 54 56 58 46 55 Z", "#77746a"),
        r([(11, 59, .1), (28, 55, .8), (49, 59, .08)], .65, "force-ground", "#bcb9af", dry=True),
    ],
    "fossil": [
        r([(10, 53, .1), (11, 28, .75), (25, 13, .9), (47, 14, .85), (61, 31, .75), (57, 53, .9), (38, 61, .75), (18, 59, .08)], 1.4, "fossil-rock", "#77746a", dry=True),
        r([(17, 48, .1), (13, 36, .75), (18, 24, .9), (30, 17, .85), (44, 20, .75), (53, 30, .9), (51, 43, .75), (41, 51, .9), (29, 50, .75), (22, 42, .9), (23, 33, .75), (31, 28, .9), (39, 30, .75), (42, 37, .9), (38, 42, .75), (32, 40, .08)], 2.6, "fossil-ammonite"),
        r([(42, 50, .1), (51, 55, .75), (61, 54, .08)], 1.5, "fossil-tail", "#4a4943"),
        ground("fossil"),
    ],
    "freeze": [
        r([(36, 8, .1), (35, 34, .8), (36, 62, .08)], 2.0, "freeze-axis-a"),
        r([(12, 20, .1), (35, 34, .8), (60, 49, .08)], 1.4, "freeze-axis-b", "#77746a", dry=True),
        r([(60, 19, .1), (36, 34, .8), (12, 50, .08)], 1.0, "freeze-axis-c", "#bcb9af", dry=True),
        r([(26, 16, .1), (35, 21, .75), (45, 15, .08)], .65, "freeze-branch-a", "#77746a", dry=True),
        r([(24, 51, .1), (35, 46, .75), (47, 52, .08)], .65, "freeze-branch-b", "#bcb9af", dry=True),
        dab(36, 34, 2.0, 2.0),
    ],
    "globe": [
        r([(14, 48, .1), (12, 32, .75), (22, 18, .9), (38, 14, .85), (53, 23, .75), (58, 39, .9), (50, 54, .75), (34, 59, .9), (20, 55, .75), (14, 48, .08)], 2.0, "globe-ring"),
        r([(35, 15, .1), (28, 28, .75), (29, 44, .9), (35, 58, .08)], 1.0, "globe-meridian-a", "#77746a", dry=True),
        r([(38, 15, .1), (46, 29, .75), (44, 45, .9), (35, 58, .08)], .7, "globe-meridian-b", "#bcb9af", dry=True),
        r([(14, 36, .1), (35, 32, .9), (57, 37, .08)], .9, "globe-latitude", "#77746a", dry=True),
    ],
    "grow": [
        r([(35, 61, .1), (35, 45, .75), (37, 28, .9), (38, 13, .08)], 2.8, "grow-stem"),
        m("M 36 31 C 27 23 17 22 10 27 C 17 36 27 39 36 34 Z", "#4a4943"),
        m("M 38 25 C 46 17 57 14 64 20 C 59 29 48 34 39 30 Z", "#77746a"),
        r([(17, 29, .1), (26, 30, .75), (35, 32, .08)], .7, "grow-vein-a", "#bcb9af", dry=True),
        r([(40, 28, .1), (49, 23, .75), (58, 20, .08)], .65, "grow-vein-b", "#bcb9af", dry=True),
        ground("grow"),
    ],
    "growth": [
        r([(14, 59, .1), (14, 50, .75), (15, 42, .08)], 1.2, "growth-stage-a"),
        m("M 14 47 C 9 42 4 42 2 45 C 5 50 10 52 14 50 Z", "#77746a"),
        r([(35, 60, .1), (35, 45, .75), (37, 30, .08)], 2.0, "growth-stage-b"),
        m("M 35 38 C 28 31 20 31 16 35 C 21 42 28 45 35 42 Z", "#4a4943"),
        r([(56, 60, .1), (55, 39, .75), (58, 18, .08)], 2.6, "growth-stage-c"),
        m("M 57 29 C 49 21 40 20 35 25 C 41 34 49 37 57 33 Z", "#77746a"),
        ground("growth"),
    ],
    "habitat": [
        r([(19, 60, .1), (20, 44, .75), (22, 27, .08)], 2.4, "habitat-tree"),
        m("M 21 34 C 14 27 7 26 3 30 C 8 37 15 40 21 37 Z", "#4a4943"),
        m("M 24 31 C 31 23 41 22 47 27 C 42 35 34 39 25 35 Z", "#77746a"),
        r([(35, 50, .1), (43, 45, .8), (52, 48, .9), (61, 43, .08)], 1.3, "habitat-nest"),
        r([(36, 55, .1), (46, 51, .8), (58, 54, .08)], .7, "habitat-nest-dry", "#bcb9af", dry=True),
        dab(46, 46, 2.0, 2.2), dab(54, 45, 1.8, 2.0, "#77746a"),
        ground("habitat"),
    ],
    "harvest": [
        r([(21, 60, .1), (21, 43, .75), (23, 24, .08)], 2.0, "harvest-stalk-a"),
        r([(35, 59, .1), (34, 40, .75), (36, 19, .08)], 1.5, "harvest-stalk-b", "#77746a", dry=True),
        r([(50, 59, .1), (48, 42, .75), (51, 27, .08)], .9, "harvest-stalk-c", "#bcb9af", dry=True),
        m("M 22 30 C 16 25 11 25 9 28 C 13 33 17 35 22 34 Z", "#4a4943"),
        m("M 36 25 C 42 19 49 18 52 22 C 48 28 42 31 36 29 Z", "#77746a"),
        r([(9, 63, .1), (31, 60, .85), (59, 62, .08)], .65, "harvest-ground", "#bcb9af", dry=True),
    ],
    "heat": [
        r([(18, 56, .1), (13, 46, .75), (19, 36, .9), (15, 25, .75), (20, 15, .08)], 1.6, "heat-a"),
        r([(36, 58, .1), (42, 47, .75), (36, 36, .9), (41, 24, .75), (36, 12, .08)], 1.1, "heat-b", "#77746a", dry=True),
        r([(53, 55, .1), (48, 46, .75), (54, 36, .9), (50, 27, .08)], .75, "heat-c", "#bcb9af", dry=True),
        r([(9, 63, .1), (30, 60, .85), (59, 62, .08)], .65, "heat-ground", "#bcb9af", dry=True),
    ],
    "melt": [
        r([(13, 20, .1), (30, 15, .8), (51, 20, .9), (57, 36, .75), (50, 47, .9), (36, 51, .75), (23, 46, .9), (13, 34, .08)], 2.0, "melt-ice"),
        r([(28, 48, .1), (27, 56, .75), (30, 62, .08)], 1.2, "melt-drip-a"),
        r([(45, 47, .1), (48, 54, .75), (46, 60, .08)], .75, "melt-drip-b", "#77746a", dry=True),
        r([(11, 64, .1), (29, 61, .85), (55, 63, .08)], .65, "melt-puddle", "#bcb9af", dry=True),
    ],
    "mist": [
        r([(9, 25, .1), (22, 20, .8), (36, 24, .9), (51, 19, .08)], 1.5, "mist-a"),
        r([(5, 39, .1), (20, 34, .8), (35, 39, .9), (52, 33, .8), (66, 37, .08)], 1.1, "mist-b", "#77746a", dry=True),
        r([(10, 52, .1), (25, 47, .8), (41, 51, .9), (58, 46, .08)], .7, "mist-c", "#bcb9af", dry=True),
        dab(58, 21, 1.5, 1.5, "#bcb9af"),
    ],
    "motion": [
        r([(7, 55, .1), (19, 45, .75), (31, 50, .9), (43, 35, .9), (58, 38, .75), (65, 23, .08)], 2.3, "motion-path"),
        dab(10, 54, 3.2, 3.2, "#77746a"),
        m("M 61 18 L 69 21 L 65 29 Z", "#262522"),
        r([(9, 63, .1), (28, 60, .85), (56, 62, .08)], .65, "motion-ground", "#bcb9af", dry=True),
        r([(14, 43, .1), (20, 40, .75), (25, 41, .08)], .65, "motion-echo", "#bcb9af", dry=True),
    ],
    "nature": [
        r([(19, 59, .1), (20, 43, .75), (22, 26, .08)], 2.4, "nature-tree"),
        m("M 21 33 C 14 26 7 25 3 29 C 8 37 15 40 21 36 Z", "#4a4943"),
        m("M 24 30 C 31 22 41 21 47 26 C 42 35 34 38 25 35 Z", "#77746a"),
        r([(32, 55, .1), (42, 43, .75), (51, 32, .9), (62, 50, .08)], 1.8, "nature-mountain"),
        r([(7, 61, .1), (22, 57, .8), (39, 61, .9), (58, 56, .08)], .75, "nature-water", "#bcb9af", dry=True),
        dab(61, 18, 3.5, 3.5, "#77746a"),
    ],
    "pollution": [
        m("M 11 27 C 17 18 28 18 34 24 C 41 18 53 20 57 29 C 48 35 24 36 11 31 Z", "#4a4943"),
        r([(21, 38, .1), (18, 47, .75), (21, 55, .08)], 1.2, "pollution-drip-a"),
        r([(36, 37, .1), (40, 46, .75), (37, 54, .08)], .8, "pollution-drip-b", "#77746a", dry=True),
        r([(52, 36, .1), (49, 44, .75), (52, 51, .08)], .65, "pollution-drip-c", "#bcb9af", dry=True),
        r([(7, 61, .1), (22, 57, .8), (38, 61, .9), (58, 56, .08)], 1.1, "pollution-water"),
        r([(15, 66, .1), (31, 63, .8), (51, 65, .08)], .65, "pollution-ground", "#bcb9af", dry=True),
    ],
    "reservoir": [
        r([(6, 35, .1), (18, 30, .8), (31, 34, .9), (46, 29, .08)], 2.2, "reservoir-water-a"),
        r([(6, 45, .1), (19, 40, .8), (33, 44, .9), (47, 39, .08)], 1.6, "reservoir-water-b", "#77746a"),
        r([(7, 55, .1), (20, 50, .8), (34, 54, .9), (48, 49, .08)], 1.2, "reservoir-water-c", "#bcb9af", dry=True),
        m("M 48 16 L 59 17 L 66 62 L 50 62 Z", "#4a4943"),
        r([(59, 27, .1), (63, 37, .75), (66, 48, .08)], 1.5, "reservoir-spill", "#262522"),
        r([(7, 64, .1), (29, 61, .85), (64, 63, .08)], 1.0, "reservoir-base", "#77746a", dry=True),
    ],
    "resource": [
        r([(16, 29, .1), (18, 45, .75), (25, 57, .9), (41, 59, .75), (52, 48, .9), (54, 31, .08)], 2.4, "resource-vessel"),
        r([(14, 28, .1), (34, 25, .9), (57, 29, .08)], 1.8, "resource-rim"),
        m("M 25 43 C 28 35 38 32 45 37 C 43 45 34 49 25 43 Z", "#4a4943"),
        r([(35, 35, .1), (35, 27, .75), (37, 20, .08)], .8, "resource-stem", "#77746a", dry=True),
        r([(25, 53, .1), (35, 56, .75), (45, 52, .08)], .65, "resource-dry", "#bcb9af", dry=True),
    ],
    "sustainability": [
        r([(16, 52, .1), (9, 39, .75), (13, 25, .9), (25, 15, .85), (41, 13, .9), (55, 22, .75), (62, 36, .08)], 2.3, "sustainability-cycle"),
        m("M 57 31 L 66 37 L 58 44 Z", "#4a4943"),
        r([(56, 47, .1), (45, 57, .75), (30, 60, .9), (17, 53, .08)], 1.1, "sustainability-return", "#77746a", dry=True),
        r([(36, 49, .1), (36, 39, .75), (38, 29, .08)], .9, "sustainability-stem"),
        m("M 37 36 C 30 29 22 29 18 33 C 23 40 30 43 37 39 Z", "#77746a"),
        m("M 39 33 C 45 26 54 25 59 29 C 55 37 47 40 39 37 Z", "#4a4943"),
    ],
    "thaw": [
        r([(11, 25, .1), (28, 20, .8), (48, 25, .9), (54, 40, .75), (47, 50, .9), (34, 54, .75), (22, 49, .9), (11, 37, .08)], 1.8, "thaw-ice"),
        dab(59, 16, 4.5, 4.5, "#4a4943"),
        r([(27, 52, .1), (25, 58, .75), (28, 63, .08)], 1.1, "thaw-drip-a"),
        r([(44, 50, .1), (47, 56, .75), (45, 61, .08)], .7, "thaw-drip-b", "#77746a", dry=True),
        r([(9, 65, .1), (28, 62, .85), (55, 64, .08)], .65, "thaw-puddle", "#bcb9af", dry=True),
        r([(54, 11, .1), (50, 7, .75), (47, 5, .08)], .65, "thaw-ray", "#bcb9af", dry=True),
    ],
    "windmill": [
        r([(27, 64, .1), (31, 45, .75), (34, 31, .08)], 2.4, "windmill-tower-left"),
        r([(45, 64, .1), (41, 45, .75), (38, 31, .08)], 1.8, "windmill-tower-right", "#77746a"),
        r([(27, 63, .1), (36, 60, .75), (45, 63, .08)], 1.6, "windmill-base"),
        dab(36, 30, 4.0, 4.0),
        r([(36, 29, .1), (35, 17, .75), (36, 5, .08)], 3.6, "windmill-blade-n"),
        r([(37, 30, .1), (50, 30, .75), (66, 33, .08)], 3.2, "windmill-blade-e", "#4a4943"),
        r([(36, 31, .1), (36, 43, .75), (33, 55, .08)], 2.8, "windmill-blade-s", "#77746a"),
        r([(35, 30, .1), (22, 31, .75), (6, 27, .08)], 2.5, "windmill-blade-w", "#4a4943"),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} science ecology/physical-world glyphs as sumi-e studies")
