#!/usr/bin/env python3
"""Redraw everyday roles and role-adjacent people concepts as sumi-e studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def r(values, width, seed, color="#262522", *, dry=False) -> str:
    # At toddler icon size, limbs and held tools must remain distinct enough to
    # carry the role.  Preserve the loaded/dry hierarchy but prevent hairlines.
    width = max(width * 1.35, 1.2)
    d = stroke_path(points(*values), width=width, seed=seed, wobble=.26, taper_start=.10, taper_end=.08)
    return (
        f'<path class="{"ink-dry" if dry else "ink-wash"}" d="{d}" fill="{color}" '
        f'data-ink-brush-pass="{"dry-edge-v2" if dry else "loaded-ribbon-v2"}"/>'
    )


def m(d: str, color="#4a4943") -> str:
    return f'<path class="ink-wash" d="{d}" fill="{color}" data-ink-brush-pass="loaded-mass-v2"/>'


def dab(cx, cy, rx, ry, color="#262522") -> str:
    return f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'


def person(name: str, x: float = 33, y: float = 15, scale: float = 1.0) -> list[str]:
    return [
        dab(x, y, 3.7 * scale, 4.0 * scale),
        r([(x, y + 5, .1), (x - 2, y + 19, .8), (x + 1, y + 34, .08)], 2.7 * scale, f"{name}-body"),
        r([(x + 1, y + 34, .1), (x - 7, y + 43, .75), (x - 13, y + 49, .08)], 1.4 * scale, f"{name}-leg-a"),
        r([(x + 1, y + 34, .1), (x + 9, y + 42, .75), (x + 16, y + 47, .08)], .85 * scale, f"{name}-leg-b", "#77746a", dry=True),
    ]


def ground(name: str) -> str:
    return r([(8, 65, .1), (29, 62, .85), (58, 64, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>people / {name} — naturalist sumi-e role study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "art": [
        r([(11, 56, .1), (21, 44, .8), (31, 48, .9), (41, 34, .95), (55, 39, .08)], 2.8, "art-gesture"),
        r([(13, 30, .1), (23, 21, .75), (35, 25, .08)], 1.2, "art-guest", "#77746a", dry=True),
        dab(53, 19, 3.0, 3.0, "#4a4943"),
        r([(8, 63, .1), (27, 60, .85), (55, 62, .08)], .65, "art-ground", "#bcb9af", dry=True),
    ],
    "artist": person("artist", 24, 15) + [
        r([(24, 29, .1), (37, 23, .75), (51, 16, .08)], 1.4, "artist-arm"),
        r([(51, 15, .1), (55, 34, .75), (55, 55, .08)], 1.5, "artist-brush"),
        m("M 48 56 C 50 47 56 41 63 39 C 61 49 57 56 48 56 Z", "#4a4943"),
        ground("artist"),
    ],
    "astronaut": [
        r([(21, 26, .1), (20, 16, .75), (27, 8, .9), (38, 7, .85), (47, 15, .75), (48, 27, .08)], 2.4, "astronaut-helmet"),
        r([(24, 25, .1), (34, 22, .85), (45, 25, .08)], 1.0, "astronaut-visor", "#77746a", dry=True),
        m("M 24 31 L 45 29 L 49 51 L 22 53 Z", "#4a4943"),
        r([(22, 36, .1), (13, 43, .75), (8, 51, .08)], 1.4, "astronaut-arm-a"),
        r([(47, 35, .1), (56, 40, .75), (63, 47, .08)], .9, "astronaut-arm-b", "#77746a", dry=True),
        r([(28, 52, .1), (24, 60, .75), (21, 65, .08)], 1.2, "astronaut-leg-a"),
        r([(42, 51, .1), (46, 59, .75), (51, 64, .08)], .75, "astronaut-leg-b", "#bcb9af", dry=True),
        dab(35, 41, 1.8, 1.8, "#bcb9af"),
    ],
    "babysitter": person("babysitter", 25, 14, .95) + [
        dab(48, 36, 2.8, 3.0, "#77746a"),
        r([(47, 40, .1), (46, 49, .75), (48, 57, .08)], 1.6, "babysitter-child"),
        r([(25, 29, .1), (35, 36, .75), (45, 40, .08)], 1.4, "babysitter-reach"),
        r([(47, 50, .1), (41, 58, .75), (37, 63, .08)], .7, "babysitter-child-leg", "#bcb9af", dry=True),
        ground("babysitter"),
    ],
    "baker": person("baker", 25, 15) + [
        dab(19, 10, 4.0, 3.3, "#77746a"),
        dab(26, 7, 4.4, 3.7, "#4a4943"),
        dab(34, 10, 4.0, 3.3, "#77746a"),
        r([(16, 13, .1), (26, 11, .8), (38, 13, .08)], 1.8, "baker-hat-band"),
        r([(24, 30, .1), (35, 39, .75), (48, 42, .08)], 1.3, "baker-arm"),
        m("M 42 45 C 44 38 54 36 60 41 C 62 47 55 52 45 50 Z", "#4a4943"),
        r([(47, 44, .1), (52, 42, .75), (57, 44, .08)], .65, "baker-loaf-cut", "#bcb9af", dry=True),
        ground("baker"),
    ],
    "builder": person("builder", 24, 16) + [
        r([(16, 14, .1), (24, 9, .8), (33, 14, .08)], 2.0, "builder-hat"),
        r([(24, 30, .1), (37, 35, .75), (49, 42, .08)], 1.4, "builder-arm"),
        r([(58, 13, .1), (50, 24, .75), (40, 38, .08)], 2.3, "builder-hammer"),
        m("M 50 10 L 61 8 L 65 15 L 55 20 Z", "#4a4943"),
        ground("builder"),
    ],
    "citizen": person("citizen", 33, 18) + [
        r([(14, 28, .1), (24, 19, .75), (34, 12, .9), (45, 20, .75), (56, 29, .08)], 1.8, "citizen-roof", "#77746a", dry=True),
        r([(14, 29, .1), (13, 42, .75), (14, 55, .08)], .9, "citizen-house-left", "#bcb9af", dry=True),
        r([(56, 29, .1), (55, 42, .75), (56, 55, .08)], .7, "citizen-house-right", "#bcb9af", dry=True),
        ground("citizen"),
    ],
    "cleaner": person("cleaner", 24, 14) + [
        r([(58, 10, .1), (49, 28, .75), (38, 55, .08)], 2.0, "cleaner-broom"),
        m("M 30 61 C 33 53 40 49 47 50 C 45 58 39 63 30 61 Z", "#4a4943"),
        r([(24, 30, .1), (35, 37, .75), (45, 39, .08)], 1.2, "cleaner-arm"),
        r([(11, 64, .1), (29, 62, .8), (52, 64, .08)], .65, "cleaner-ground", "#bcb9af", dry=True),
    ],
    "cook": person("cook", 23, 15) + [
        dab(17, 10, 4.0, 3.3, "#77746a"),
        dab(24, 7, 4.4, 3.7, "#4a4943"),
        dab(32, 10, 4.0, 3.3, "#77746a"),
        r([(14, 13, .1), (24, 11, .8), (36, 13, .08)], 1.7, "cook-hat-band"),
        r([(23, 30, .1), (35, 37, .75), (47, 40, .08)], 1.2, "cook-arm"),
        r([(41, 42, .1), (45, 53, .75), (55, 57, .9), (64, 51, .08)], 2.1, "cook-pot"),
        r([(41, 41, .1), (52, 38, .8), (65, 41, .08)], 1.5, "cook-rim"),
        r([(48, 35, .1), (45, 27, .75), (49, 21, .08)], .7, "cook-steam", "#bcb9af", dry=True),
        ground("cook"),
    ],
    "creator": person("creator", 22, 16) + [
        r([(22, 31, .1), (34, 35, .75), (45, 31, .08)], 1.3, "creator-arm"),
        r([(61, 9, .1), (52, 20, .75), (42, 36, .08)], 2.2, "creator-brush"),
        m("M 34 45 C 36 38 42 34 49 33 C 47 41 42 46 34 45 Z", "#4a4943"),
        r([(51, 27, .1), (57, 23, .75), (63, 24, .08)], .7, "creator-spark", "#bcb9af", dry=True),
        ground("creator"),
    ],
    "destroyer": person("destroyer", 27, 16) + [
        r([(24, 31, .1), (38, 25, .75), (51, 16, .08)], 1.6, "destroyer-arm"),
        r([(58, 8, .1), (49, 21, .75), (39, 37, .08)], 2.7, "destroyer-hammer"),
        m("M 50 6 L 62 5 L 66 13 L 55 18 Z", "#4a4943"),
        r([(38, 54, .1), (46, 48, .75), (53, 54, .9), (61, 47, .08)], 2.0, "destroyer-break"),
        r([(8, 64, .1), (28, 61, .8), (58, 63, .08)], .65, "destroyer-ground", "#bcb9af", dry=True),
    ],
    "firefighter": person("firefighter", 22, 16) + [
        m("M 13 16 C 14 7 29 5 33 15 L 30 19 L 14 19 Z", "#4a4943"),
        r([(13, 17, .1), (22, 15, .8), (33, 17, .08)], 1.7, "firefighter-helmet-brim"),
        dab(22, 18, 2.5, 2.7, "#bcb9af"),
        m("M 17 24 L 28 24 L 32 48 L 14 49 Z", "#77746a"),
        r([(15, 38, .1), (23, 36, .75), (30, 38, .08)], 1.35, "firefighter-reflective-stripe", "#262522"),
        r([(22, 30, .1), (34, 38, .75), (45, 41, .08)], 1.3, "firefighter-arm"),
        r([(43, 42, .1), (50, 37, .75), (57, 38, .08)], 2.4, "firefighter-hose"),
        r([(56, 38, .1), (61, 43, .75), (65, 48, .08)], 1.6, "firefighter-water", "#77746a"),
        m("M 57 63 C 53 57 59 53 61 48 C 67 54 70 58 66 64 Z", "#4a4943"),
        r([(59, 61, .1), (62, 56, .75), (65, 61, .08)], 1.2, "firefighter-flame-core", "#bcb9af", dry=True),
        ground("firefighter"),
    ],
    "farmer": person("farmer", 23, 17) + [
        r([(11, 14, .1), (23, 10, .8), (37, 14, .08)], 2.6, "farmer-hat-brim"),
        m("M 17 11 C 19 4 30 3 34 11 Z", "#4a4943"),
        r([(23, 32, .1), (36, 39, .75), (47, 40, .08)], 1.6, "farmer-arm"),
        r([(55, 17, .1), (54, 34, .75), (55, 57, .08)], 2.0, "farmer-stalk"),
        r([(54, 28, .1), (47, 23, .75), (42, 24, .08)], 1.5, "farmer-leaf-a", "#4a4943"),
        r([(55, 38, .1), (62, 33, .75), (66, 34, .08)], 1.35, "farmer-leaf-b", "#77746a"),
        dab(55, 15, 2.6, 3.4, "#262522"),
        ground("farmer"),
    ],
    "food": [
        r([(11, 40, .1), (17, 52, .8), (29, 58, .9), (44, 55, .8), (52, 41, .08)], 2.7, "food-bowl"),
        r([(9, 39, .1), (31, 36, .95), (55, 39, .08)], 2.0, "food-rim"),
        m("M 20 37 C 22 30 31 27 37 32 C 35 39 27 42 20 37 Z", "#4a4943"),
        m("M 37 37 C 41 29 50 28 55 34 C 51 40 44 41 37 37 Z", "#77746a"),
        r([(25, 31, .1), (21, 24, .75), (24, 18, .08)], .7, "food-steam-a", "#bcb9af", dry=True),
        r([(43, 30, .1), (47, 22, .75), (44, 15, .08)], .65, "food-steam-b", "#77746a", dry=True),
    ],
    "fool": person("fool", 34, 19) + [
        r([(20, 17, .1), (28, 7, .75), (35, 16, .9), (44, 6, .75), (52, 17, .08)], 1.8, "fool-cap"),
        dab(27, 7, 1.7, 1.7, "#77746a"), dab(45, 6, 1.6, 1.6, "#bcb9af"),
        r([(29, 36, .1), (35, 39, .75), (42, 36, .08)], .75, "fool-smile", "#bcb9af", dry=True),
        r([(18, 54, .1), (34, 51, .8), (51, 54, .08)], 1.2, "fool-cape", "#77746a", dry=True),
        ground("fool"),
    ],
    "guardian": person("guardian", 23, 15) + [
        r([(22, 30, .1), (35, 36, .75), (45, 43, .08)], 1.3, "guardian-arm"),
        r([(44, 27, .1), (57, 23, .8), (64, 31, .9), (61, 47, .8), (53, 57, .9), (45, 47, .8), (42, 34, .08)], 2.1, "guardian-shield"),
        r([(49, 35, .1), (54, 32, .75), (59, 35, .08)], .65, "guardian-shield-mark", "#bcb9af", dry=True),
        ground("guardian"),
    ],
    "health": [
        r([(35, 60, .1), (35, 43, .75), (37, 24, .08)], 2.7, "health-stem"),
        m("M 35 33 C 27 24 17 23 10 29 C 17 38 27 41 35 36 Z", "#4a4943"),
        m("M 38 29 C 46 20 57 18 64 24 C 58 34 48 38 39 34 Z", "#77746a"),
        r([(18, 30, .1), (26, 32, .75), (34, 34, .08)], .7, "health-vein-a", "#bcb9af", dry=True),
        r([(40, 32, .1), (49, 27, .75), (58, 24, .08)], .65, "health-vein-b", "#bcb9af", dry=True),
        r([(29, 14, .1), (36, 11, .75), (43, 14, .08)], 1.1, "health-cross-a"),
        r([(36, 7, .1), (36, 13, .75), (36, 19, .08)], .8, "health-cross-b", "#77746a", dry=True),
    ],
    "healer": person("healer", 23, 16) + [
        r([(21, 26, .1), (28, 31, .75), (27, 39, .9), (22, 43, .08)], 1.5, "healer-stethoscope-left"),
        r([(27, 26, .1), (34, 31, .75), (34, 40, .9), (29, 44, .08)], 1.35, "healer-stethoscope-right", "#77746a"),
        dab(26, 45, 2.5, 2.5, "#262522"),
        m("M 42 35 L 59 34 L 60 53 L 42 54 Z", "#77746a"),
        r([(46, 44, .1), (56, 44, .08)], 1.7, "healer-cross-horizontal"),
        r([(51, 39, .1), (51, 49, .08)], 1.7, "healer-cross-vertical"),
        ground("healer"),
    ],
    "hero": person("hero", 31, 15) + [
        r([(30, 29, .1), (19, 33, .75), (9, 29, .08)], 1.4, "hero-arm-a"),
        r([(33, 28, .1), (45, 22, .75), (58, 13, .08)], 1.0, "hero-arm-b", "#77746a", dry=True),
        m("M 35 22 C 48 28 55 39 56 51 C 46 47 39 40 34 30 Z", "#4a4943"),
        ground("hero"),
    ],
    "leader": person("leader", 36, 13) + [
        r([(35, 27, .1), (47, 20, .75), (58, 10, .08)], 1.5, "leader-raised-arm"),
        dab(15, 45, 2.7, 2.9, "#77746a"), dab(26, 49, 2.4, 2.6, "#bcb9af"),
        r([(14, 49, .1), (13, 57, .75), (14, 63, .08)], .9, "leader-follower-a", "#77746a", dry=True),
        r([(25, 53, .1), (24, 59, .75), (25, 64, .08)], .65, "leader-follower-b", "#bcb9af", dry=True),
        ground("leader"),
    ],
    "learning": person("learning", 24, 16) + [
        r([(24, 31, .1), (34, 38, .75), (45, 40, .08)], 1.2, "learning-arm"),
        r([(39, 38, .1), (48, 35, .8), (58, 39, .08)], 1.4, "learning-book-spine"),
        r([(39, 39, .1), (41, 50, .75), (48, 55, .08)], 1.0, "learning-page-a", "#77746a", dry=True),
        r([(58, 39, .1), (56, 49, .75), (49, 55, .08)], .7, "learning-page-b", "#bcb9af", dry=True),
        r([(43, 45, .1), (48, 42, .75), (54, 45, .08)], .65, "learning-mark", "#bcb9af", dry=True),
        ground("learning"),
    ],
    "mechanic": person("mechanic", 23, 16) + [
        r([(15, 14, .1), (23, 9, .8), (32, 14, .08)], 1.9, "mechanic-cap"),
        r([(23, 30, .1), (34, 36, .75), (45, 38, .08)], 1.2, "mechanic-arm"),
        r([(47, 26, .1), (56, 31, .75), (58, 41, .9), (52, 49, .75), (42, 48, .9), (38, 39, .75), (42, 30, .08)], 1.7, "mechanic-wheel"),
        dab(49, 38, 2.4, 2.4),
        r([(47, 38, .1), (54, 44, .75), (62, 51, .08)], 1.8, "mechanic-wrench"),
        r([(58, 48, .1), (63, 46, .75), (66, 49, .08)], 1.4, "mechanic-wrench-jaw", "#4a4943"),
        ground("mechanic"),
    ],
    "mentor": person("mentor", 22, 14, .95) + [
        dab(49, 34, 3.0, 3.2, "#77746a"),
        r([(49, 38, .1), (48, 49, .75), (50, 59, .08)], 1.6, "mentor-student"),
        r([(22, 29, .1), (34, 31, .75), (46, 36, .08)], 1.4, "mentor-guide"),
        r([(49, 48, .1), (42, 56, .75), (37, 62, .08)], .7, "mentor-student-leg", "#bcb9af", dry=True),
        ground("mentor"),
    ],
    "nurse": person("nurse", 26, 16) + [
        r([(18, 14, .1), (26, 9, .8), (34, 14, .08)], 1.8, "nurse-cap"),
        r([(22, 12, .1), (26, 10, .75), (30, 12, .08)], .7, "nurse-cap-mark", "#bcb9af", dry=True),
        m("M 38 37 L 54 35 L 57 52 L 40 55 Z", "#4a4943"),
        r([(43, 44, .1), (49, 42, .75), (55, 44, .08)], 1.7, "nurse-cross-a"),
        r([(49, 38, .1), (49, 44, .75), (49, 50, .08)], 1.7, "nurse-cross-b"),
        r([(26, 31, .1), (36, 38, .75), (42, 42, .08)], 1.1, "nurse-arm"),
        ground("nurse"),
    ],
    "police": person("police", 25, 16) + [
        r([(15, 15, .1), (25, 9, .8), (36, 15, .08)], 2.2, "police-cap"),
        r([(14, 16, .1), (25, 13, .8), (38, 16, .08)], 1.0, "police-brim", "#77746a", dry=True),
        r([(25, 30, .1), (37, 35, .75), (46, 42, .08)], 1.2, "police-arm"),
        r([(45, 28, .1), (57, 25, .8), (63, 33, .9), (60, 47, .8), (53, 55, .9), (46, 46, .8), (43, 34, .08)], 1.8, "police-shield"),
        dab(53, 36, 1.8, 1.8, "#bcb9af"),
        ground("police"),
    ],
    "repair": person("repair", 22, 16) + [
        r([(22, 31, .1), (34, 37, .75), (45, 40, .08)], 1.2, "repair-arm"),
        r([(58, 17, .1), (50, 28, .75), (39, 43, .08)], 2.6, "repair-wrench-handle"),
        r([(51, 20, .1), (58, 15, .75), (65, 19, .08)], 2.0, "repair-wrench-jaw"),
        r([(44, 48, .1), (49, 55, .75), (58, 56, .9), (63, 49, .08)], 1.7, "repair-bowl"),
        r([(50, 51, .1), (54, 47, .75), (58, 51, .08)], .65, "repair-seam", "#bcb9af", dry=True),
        ground("repair"),
    ],
    "safety": [
        r([(9, 56, .1), (10, 38, .75), (19, 23, .9), (34, 16, .85), (49, 23, .75), (59, 42, .08)], 2.8, "safety-shelter"),
        dab(35, 34, 3.5, 3.8),
        r([(35, 39, .1), (34, 48, .75), (36, 57, .08)], 2.0, "safety-person"),
        r([(27, 58, .1), (35, 55, .8), (45, 58, .08)], .8, "safety-person-base", "#77746a", dry=True),
        r([(8, 62, .1), (29, 59, .85), (59, 61, .08)], .65, "safety-ground", "#bcb9af", dry=True),
    ],
    "science": person("science", 22, 16) + [
        r([(22, 31, .1), (34, 37, .75), (45, 39, .08)], 1.2, "science-arm"),
        r([(52, 18, .1), (51, 30, .75), (47, 42, .9), (42, 52, .75), (49, 58, .9), (59, 54, .75), (56, 43, .9), (52, 31, .08)], 1.6, "science-flask"),
        r([(44, 48, .1), (50, 51, .75), (57, 48, .08)], .75, "science-liquid", "#77746a", dry=True),
        dab(59, 29, 1.8, 1.8, "#bcb9af"),
        ground("science"),
    ],
    "seeker": person("seeker", 25, 16) + [
        r([(50, 12, .1), (49, 34, .75), (51, 63, .08)], 1.4, "seeker-staff", "#77746a", dry=True),
        r([(25, 31, .1), (35, 35, .75), (47, 34, .08)], 1.2, "seeker-arm"),
        r([(8, 60, .1), (18, 49, .75), (30, 53, .9), (42, 43, .08)], 1.4, "seeker-path", "#bcb9af", dry=True),
        dab(59, 12, 2.0, 2.0, "#bcb9af"),
        ground("seeker"),
    ],
    "service": person("service", 24, 16) + [
        r([(24, 31, .1), (35, 39, .75), (47, 42, .08)], 1.3, "service-arm"),
        r([(43, 42, .1), (47, 51, .75), (56, 55, .9), (64, 50, .08)], 1.8, "service-bowl"),
        r([(43, 41, .1), (53, 38, .8), (65, 41, .08)], 1.3, "service-rim"),
        dab(55, 35, 2.0, 2.0, "#77746a"),
        r([(10, 64, .1), (29, 61, .8), (59, 63, .08)], .65, "service-ground", "#bcb9af", dry=True),
    ],
    "stewardship": person("stewardship", 22, 17) + [
        r([(22, 31, .1), (34, 38, .75), (45, 40, .08)], 1.2, "stewardship-arm"),
        r([(51, 60, .1), (51, 45, .75), (53, 28, .08)], 2.2, "stewardship-tree"),
        m("M 52 35 C 44 27 35 26 29 31 C 35 40 44 43 52 39 Z", "#4a4943"),
        m("M 54 31 C 60 24 66 24 69 28 C 65 35 60 38 54 35 Z", "#77746a"),
        r([(8, 64, .1), (31, 61, .85), (61, 63, .08)], .65, "stewardship-ground", "#bcb9af", dry=True),
    ],
    "work": person("work", 22, 16) + [
        r([(22, 31, .1), (34, 37, .75), (45, 39, .08)], 1.2, "work-arm"),
        r([(56, 12, .1), (48, 24, .75), (39, 39, .08)], 2.3, "work-hammer"),
        m("M 49 9 L 60 7 L 65 15 L 54 20 Z", "#4a4943"),
        r([(37, 50, .1), (49, 47, .8), (63, 50, .08)], 2.5, "work-bench"),
        r([(42, 51, .1), (41, 59, .75), (40, 64, .08)], .8, "work-bench-leg", "#77746a", dry=True),
        ground("work"),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} people role glyphs as naturalist sumi-e studies")
