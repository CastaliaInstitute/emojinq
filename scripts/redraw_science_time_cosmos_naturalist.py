#!/usr/bin/env python3
"""Redraw temporal, directional, and cosmos science glyphs as naturalist sumi-e."""

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


def ground(name: str, y=61) -> str:
    return r([(7, y, .1), (29, y - 3, .85), (63, y - 1, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def ring(name: str, cx=36, cy=35, rx=22, ry=22, color="#262522", width=2.0) -> str:
    return r([
        (cx-rx, cy+5, .1), (cx-rx-1, cy-7, .7), (cx-rx/2, cy-ry+2, .9),
        (cx+3, cy-ry, .85), (cx+rx-2, cy-8, .9), (cx+rx, cy+6, .8),
        (cx+rx/2, cy+ry-1, .9), (cx-4, cy+ry, .85), (cx-rx+2, cy+9, .08)
    ], width, name, color)


def crescent(name: str, x=36, y=32) -> list[str]:
    return [
        r([(x+10, y-18, .1), (x-2, y-20, .75), (x-13, y-12, .9), (x-17, y+2, .85), (x-10, y+15, .9), (x+3, y+19, .75), (x+13, y+12, .08)], 2.2, f"{name}-outer"),
        r([(x+10, y-17, .1), (x+2, y-8, .75), (x+1, y+3, .9), (x+7, y+12, .08)], .8, f"{name}-inner", "#bcb9af", dry=True),
    ]


def arrow(name: str, direction: str) -> list[str]:
    coords = {
        "right": ([(10, 38, .1), (32, 34, .85), (56, 37, .08)], "M 53 29 L 66 36 L 54 45 Z"),
        "left": ([(62, 38, .1), (40, 34, .85), (16, 37, .08)], "M 19 29 L 6 36 L 18 45 Z"),
        "up": ([(36, 61, .1), (33, 39, .85), (36, 17, .08)], "M 28 20 L 36 7 L 44 20 Z"),
        "down": ([(36, 10, .1), (33, 32, .85), (36, 55, .08)], "M 28 52 L 36 66 L 44 53 Z"),
    }
    values, head = coords[direction]
    return [r(values, 2.7, f"{name}-shaft"), m(head, "#4a4943")]


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e time and cosmos study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "century": [
        r([(11, 56, .1), (11, 40, .8), (12, 25, .08)], 1.1, "century-one"),
        r([(27, 58, .1), (27, 38, .8), (29, 20, .08)], 1.6, "century-two", "#77746a", dry=True),
        r([(45, 59, .1), (44, 35, .8), (47, 13, .08)], 2.3, "century-three"),
        m("M 46 22 C 53 15 61 15 66 19 C 61 26 54 29 47 26 Z", "#4a4943"),
        ground("century"),
    ],
    "constellation": [
        dab(12, 48, 3.0, 3.0), dab(25, 27, 2.5, 2.5, "#77746a"), dab(41, 36, 3.2, 3.2), dab(59, 17, 2.4, 2.4, "#4a4943"), dab(62, 52, 2.0, 2.0, "#bcb9af"),
        r([(12, 48, .1), (25, 27, .8), (41, 36, .9), (59, 17, .08)], .75, "constellation-thread", "#77746a", dry=True),
        r([(41, 36, .1), (62, 52, .08)], .6, "constellation-thread-b", "#bcb9af", dry=True),
    ],
    "cosmos": [
        ring("cosmos-ring", 36, 35, 27, 21, "#77746a", 1.5),
        r([(7, 42, .1), (22, 29, .8), (39, 27, .9), (57, 38, .8), (66, 48, .08)], 2.1, "cosmos-sweep"),
        dab(22, 28, 3.0, 3.0), dab(55, 39, 2.4, 2.4, "#4a4943"), dab(40, 14, 1.8, 1.8, "#bcb9af"),
    ],
    "day": [
        dab(36, 27, 9.0, 8.5, "#4a4943"),
        r([(7, 51, .1), (28, 47, .85), (63, 50, .08)], 1.4, "day-horizon"),
        r([(36, 12, .1), (36, 7, .75), (37, 4, .08)], .65, "day-ray-a", "#bcb9af", dry=True),
        r([(20, 24, .1), (14, 22, .75), (9, 23, .08)], .65, "day-ray-b", "#bcb9af", dry=True),
        ground("day", 61),
    ],
    "east": [
        r([(7, 50, .1), (28, 46, .8), (63, 49, .08)], 1.5, "east-horizon"),
        m("M 48 48 C 49 37 56 29 65 27 L 66 48 Z", "#4a4943"),
        r([(46, 33, .1), (53, 25, .75), (62, 20, .08)], .7, "east-ray", "#bcb9af", dry=True),
        *arrow("east", "right"),
    ],
    "eclipse": [
        dab(33, 34, 15.5, 15.5, "#77746a"),
        r([(23, 19, .1), (37, 17, .8), (50, 26, .9), (53, 40, .8), (47, 51, .08)], 2.0, "eclipse-light"),
        m("M 45 20 C 54 27 57 40 50 50 C 47 42 46 30 45 20 Z", "#bcb9af"),
        ground("eclipse"),
    ],
    "era": [
        r([(9, 54, .1), (24, 50, .8), (38, 54, .9), (55, 48, .08)], 2.1, "era-river"),
        r([(20, 58, .1), (21, 42, .75), (22, 28, .08)], 1.4, "era-marker-a"),
        r([(48, 52, .1), (48, 35, .75), (50, 19, .08)], 2.4, "era-marker-b", "#77746a", dry=True),
        dab(22, 25, 3.0, 3.0, "#bcb9af"), dab(50, 16, 4.0, 4.0),
        ground("era", 64),
    ],
    "evening": [
        r([(7, 49, .1), (29, 45, .85), (64, 48, .08)], 1.5, "evening-horizon"),
        m("M 12 48 C 14 37 22 30 31 29 C 33 38 31 44 27 47 Z", "#77746a"),
        *crescent("evening", 53, 26),
        ground("evening", 60),
    ],
    "fall": [
        m("M 8 15 C 16 8 28 10 33 17 C 27 25 17 27 9 21 Z", "#77746a"),
        r([(31, 22, .1), (39, 28, .75), (34, 37, .9), (45, 43, .75), (42, 53, .9), (54, 57, .08)], 1.3, "fall-path"),
        r([(43, 39, .1), (50, 42, .75), (57, 40, .08)], .7, "fall-flutter", "#bcb9af", dry=True),
        ground("fall"),
    ],
    "future": [*arrow("future", "right"), dab(12, 38, 3.0, 3.0, "#77746a"), ground("future")],
    "galaxy": [
        r([(8, 40, .1), (18, 23, .75), (36, 17, .9), (54, 24, .8), (62, 39, .9), (54, 52, .8), (36, 56, .9), (22, 49, .8), (19, 37, .9), (28, 29, .8), (41, 29, .9), (48, 36, .8), (44, 43, .9), (34, 44, .08)], 2.0, "galaxy-spiral"),
        dab(35, 36, 4.0, 3.5), dab(12, 18, 1.8, 1.8, "#bcb9af"), dab(62, 56, 2.0, 2.0, "#77746a"),
    ],
    "history": [
        r([(13, 18, .1), (35, 14, .85), (58, 18, .08)], 2.0, "history-scroll-top"),
        r([(13, 18, .1), (15, 37, .8), (13, 56, .08)], 1.4, "history-scroll-left"),
        r([(58, 18, .1), (56, 37, .8), (58, 56, .08)], .9, "history-scroll-right", "#77746a", dry=True),
        r([(13, 56, .1), (35, 52, .85), (58, 56, .08)], 1.5, "history-scroll-bottom"),
        r([(22, 30, .1), (35, 27, .8), (49, 30, .08)], .75, "history-line-a", "#77746a", dry=True),
        r([(22, 42, .1), (33, 39, .8), (44, 42, .08)], .65, "history-line-b", "#bcb9af", dry=True),
    ],
    "horizon": [
        r([(4, 40, .1), (24, 35, .8), (44, 39, .9), (68, 34, .08)], 2.2, "horizon-near"),
        r([(9, 51, .1), (28, 47, .8), (46, 51, .9), (62, 47, .08)], .8, "horizon-far", "#bcb9af", dry=True),
        dab(54, 20, 5.0, 4.6, "#77746a"),
    ],
    "month": [
        *crescent("month", 34, 32),
        dab(57, 17, 2.3, 2.3, "#77746a"),
        r([(10, 60, .1), (28, 56, .8), (56, 59, .08)], .65, "month-ground", "#bcb9af", dry=True),
    ],
    "morning": [
        r([(7, 50, .1), (29, 46, .85), (64, 49, .08)], 1.5, "morning-horizon"),
        m("M 24 48 C 25 37 31 29 39 28 C 45 33 48 40 48 47 Z", "#4a4943"),
        r([(39, 24, .1), (40, 15, .75), (41, 9, .08)], .75, "morning-ray-a", "#77746a", dry=True),
        r([(24, 32, .1), (18, 27, .75), (13, 24, .08)], .65, "morning-ray-b", "#bcb9af", dry=True),
        ground("morning", 61),
    ],
    "night": [
        *crescent("night", 32, 32),
        dab(58, 16, 2.3, 2.3), dab(55, 35, 1.6, 1.6, "#bcb9af"), dab(12, 24, 1.8, 1.8, "#77746a"),
        ground("night"),
    ],
    "north": [*arrow("north", "up"), r([(8, 62, .1), (29, 58, .85), (62, 61, .08)], .65, "north-ground", "#bcb9af", dry=True)],
    "orbit": [
        r([(9, 38, .1), (16, 24, .75), (34, 18, .9), (54, 24, .8), (63, 38, .9), (55, 51, .8), (36, 56, .9), (18, 50, .8), (9, 38, .08)], 1.5, "orbit-ring", "#77746a", dry=True),
        dab(36, 37, 7.0, 6.5, "#4a4943"), dab(60, 23, 3.0, 3.0),
        r([(59, 21, .1), (64, 17, .75), (68, 18, .08)], .65, "orbit-lift", "#bcb9af", dry=True),
    ],
    "past": [*arrow("past", "left"), dab(61, 38, 3.0, 3.0, "#77746a"), ground("past")],
    "planet": [
        dab(35, 35, 13, 12, "#77746a"),
        r([(6, 43, .1), (22, 35, .8), (41, 32, .9), (64, 36, .08)], 2.0, "planet-ring"),
        r([(13, 48, .1), (31, 43, .8), (54, 44, .08)], .65, "planet-ring-dry", "#bcb9af", dry=True),
    ],
    "present": [
        ring("present-ring", 36, 35, 20, 20, "#77746a", 1.4),
        dab(36, 35, 6.0, 6.0),
        r([(11, 61, .1), (30, 58, .8), (58, 60, .08)], .65, "present-ground", "#bcb9af", dry=True),
    ],
    "season": [
        r([(36, 61, .1), (35, 43, .8), (37, 24, .08)], 2.4, "season-trunk"),
        m("M 36 31 C 28 23 17 22 10 27 C 17 36 27 39 36 34 Z", "#4a4943"),
        m("M 38 28 C 46 20 57 19 64 24 C 59 33 48 36 39 33 Z", "#77746a"),
        r([(52, 36, .1), (58, 44, .75), (61, 53, .08)], .7, "season-fall", "#bcb9af", dry=True),
        ground("season"),
    ],
    "shadow": [
        m("M 18 22 C 27 13 42 13 51 22 C 44 30 28 32 18 22 Z", "#4a4943"),
        r([(35, 28, .1), (35, 40, .75), (36, 55, .08)], 1.6, "shadow-stem"),
        m("M 28 57 C 37 51 53 52 63 59 C 54 65 38 66 28 61 Z", "#bcb9af"),
        ground("shadow", 65),
    ],
    "solar": [
        dab(18, 17, 6.5, 6.5, "#4a4943"),
        r([(18, 8, .1), (18, 3, .08)], 1.5, "solar-ray-n"),
        r([(9, 17, .1), (4, 17, .08)], 1.4, "solar-ray-w", "#77746a"),
        r([(25, 10, .1), (29, 6, .08)], 1.3, "solar-ray-ne", "#77746a"),
        r([(18, 34, .1), (57, 29, .85), (64, 52, .75), (24, 57, .85), (18, 34, .08)], 2.2, "solar-panel-frame", "#77746a"),
        r([(20, 42, .1), (59, 37, .08)], 1.2, "solar-panel-row-a"),
        r([(23, 50, .1), (62, 45, .08)], 1.2, "solar-panel-row-b"),
        r([(34, 32, .1), (40, 55, .08)], 1.2, "solar-panel-col-a"),
        r([(48, 31, .1), (54, 53, .08)], 1.2, "solar-panel-col-b"),
        r([(42, 55, .1), (42, 63, .08)], 1.8, "solar-panel-stand"),
        r([(31, 64, .1), (43, 61, .75), (55, 64, .08)], 1.4, "solar-panel-foot", "#77746a"),
    ],
    "south": [*arrow("south", "down"), r([(8, 10, .1), (29, 7, .85), (62, 9, .08)], .65, "south-sky", "#bcb9af", dry=True)],
    "sunset": [
        r([(6, 47, .1), (29, 43, .85), (65, 46, .08)], 1.6, "sunset-horizon"),
        m("M 27 45 C 29 34 37 27 46 28 C 52 33 54 39 54 44 Z", "#77746a"),
        r([(48, 25, .1), (54, 19, .75), (60, 16, .08)], .65, "sunset-ray", "#bcb9af", dry=True),
        r([(9, 58, .1), (28, 54, .8), (55, 58, .08)], .8, "sunset-reflection", "#bcb9af", dry=True),
    ],
    "timeline": [
        r([(7, 38, .1), (25, 34, .8), (45, 38, .9), (65, 34, .08)], 2.2, "timeline-line"),
        dab(15, 36, 3.6, 3.6), dab(36, 36, 3.0, 3.0, "#77746a"), dab(58, 35, 2.5, 2.5, "#bcb9af"),
        r([(15, 43, .1), (15, 53, .75), (16, 59, .08)], .8, "timeline-mark-a", "#77746a", dry=True),
        r([(58, 28, .1), (58, 20, .75), (59, 14, .08)], .65, "timeline-mark-b", "#bcb9af", dry=True),
        ground("timeline"),
    ],
    "today": [
        dab(36, 26, 7.0, 6.5, "#4a4943"),
        r([(9, 48, .1), (29, 44, .85), (62, 47, .08)], 1.6, "today-horizon"),
        r([(36, 38, .1), (35, 50, .75), (36, 61, .08)], 2.1, "today-mark"),
        r([(17, 59, .1), (35, 56, .8), (53, 59, .08)], .65, "today-ground", "#bcb9af", dry=True),
    ],
    "tomorrow": [
        r([(17, 60, .1), (31, 52, .8), (43, 40, .9), (57, 27, .08)], 2.2, "tomorrow-rise"),
        m("M 53 21 L 66 24 L 59 34 Z", "#4a4943"),
        r([(30, 53, .1), (30, 42, .75), (32, 33, .08)], .9, "tomorrow-stem", "#77746a", dry=True),
        m("M 31 39 C 24 33 17 33 13 37 C 18 43 24 46 31 43 Z", "#77746a"),
        ground("tomorrow"),
    ],
    "universe": [
        ring("universe-outer", 36, 35, 28, 25, "#77746a", 1.4),
        r([(9, 45, .1), (24, 27, .8), (42, 25, .9), (63, 40, .08)], 2.0, "universe-sweep"),
        r([(18, 55, .1), (31, 43, .8), (48, 42, .9), (60, 52, .08)], .75, "universe-sweep-dry", "#bcb9af", dry=True),
        dab(14, 23, 2.4, 2.4), dab(38, 34, 3.2, 3.2, "#4a4943"), dab(59, 17, 1.8, 1.8, "#bcb9af"),
    ],
    "week": [
        *crescent("week", 34, 31),
        dab(10, 53, 2.2, 2.2), dab(19, 55, 2.0, 2.0, "#77746a"), dab(28, 56, 1.8, 1.8, "#bcb9af"),
        dab(40, 56, 2.2, 2.2), dab(50, 54, 2.0, 2.0, "#77746a"), dab(60, 51, 1.8, 1.8, "#bcb9af"), dab(66, 45, 1.7, 1.7),
        ground("week", 64),
    ],
    "west": [
        r([(7, 50, .1), (29, 46, .8), (64, 49, .08)], 1.5, "west-horizon"),
        m("M 7 48 L 8 28 C 17 30 24 38 25 48 Z", "#77746a"),
        r([(10, 28, .1), (16, 22, .75), (23, 19, .08)], .65, "west-ray", "#bcb9af", dry=True),
        *arrow("west", "left"),
    ],
    "year": [
        ring("year-ring", 36, 34, 23, 23, "#77746a", 1.6),
        r([(36, 57, .1), (35, 43, .75), (37, 31, .08)], 1.5, "year-stem"),
        m("M 36 38 C 29 31 21 30 17 34 C 22 41 29 44 36 41 Z", "#4a4943"),
        m("M 38 34 C 45 27 54 26 59 30 C 55 38 47 41 39 38 Z", "#77746a"),
        ground("year", 64),
    ],
    "yesterday": [
        *arrow("yesterday", "left"),
        m("M 47 36 C 49 27 56 20 64 20 L 64 36 Z", "#77746a"),
        r([(10, 59, .1), (29, 55, .8), (56, 58, .08)], .65, "yesterday-ground", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} science time/cosmos glyphs as sumi-e studies")
