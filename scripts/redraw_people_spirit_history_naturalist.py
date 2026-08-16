#!/usr/bin/env python3
"""Redraw final spiritual, narrative, and historical people glyphs as sumi-e."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def r(values, width, seed, color="#262522", *, dry=False) -> str:
    # Historical portraits and ritual objects need visible shoulders, hands,
    # and attributes at icon size while retaining tapered brush pressure.
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


def portrait(name: str, x: float = 27, y: float = 18) -> list[str]:
    return [
        dab(x, y, 4.2, 4.5),
        r([(x - 4, y + 5, .1), (x - 8, y + 17, .75), (x - 5, y + 29, .08)], 1.8, f"{name}-shoulder-a"),
        r([(x + 4, y + 5, .1), (x + 10, y + 16, .75), (x + 14, y + 28, .08)], 1.0, f"{name}-shoulder-b", "#77746a", dry=True),
        r([(x - 6, y + 29, .1), (x + 3, y + 26, .8), (x + 15, y + 28, .08)], .8, f"{name}-robe", "#bcb9af", dry=True),
    ]


def ground(name: str) -> str:
    return r([(7, 64, .1), (29, 61, .85), (62, 63, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>people / {name} — naturalist sumi-e spirit and history study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "ancestor": [
        dab(36, 17, 3.8, 4.0),
        r([(36, 21, .1), (35, 35, .75), (37, 49, .08)], 2.4, "ancestor-body"),
        r([(37, 35, .1), (25, 42, .75), (15, 48, .08)], 1.3, "ancestor-branch-a"),
        r([(37, 35, .1), (48, 41, .75), (59, 46, .08)], .9, "ancestor-branch-b", "#77746a", dry=True),
        r([(36, 49, .1), (29, 58, .75), (21, 64, .08)], 1.2, "ancestor-root-a"),
        r([(36, 49, .1), (45, 57, .75), (53, 63, .08)], .7, "ancestor-root-b", "#bcb9af", dry=True),
        r([(21, 12, .1), (35, 7, .85), (52, 12, .08)], .7, "ancestor-breath", "#bcb9af", dry=True),
    ],
    "aristotle": portrait("aristotle") + [
        r([(38, 29, .1), (47, 34, .75), (57, 33, .08)], 1.1, "aristotle-hand"),
        r([(45, 35, .1), (50, 45, .75), (59, 49, .9), (65, 44, .08)], 1.5, "aristotle-scroll"),
        r([(45, 34, .1), (55, 31, .8), (65, 34, .08)], .75, "aristotle-scroll-rim", "#77746a", dry=True),
        r([(49, 42, .1), (55, 39, .75), (61, 42, .08)], .65, "aristotle-mark", "#bcb9af", dry=True),
        ground("aristotle"),
    ],
    "buddha": [
        dab(36, 16, 4.4, 4.7),
        dab(36, 9, 2.0, 2.0, "#77746a"),
        r([(35, 21, .1), (32, 35, .75), (36, 45, .08)], 2.5, "buddha-body"),
        r([(17, 55, .1), (25, 44, .75), (36, 47, .9), (47, 43, .75), (57, 55, .08)], 2.2, "buddha-lotus"),
        r([(13, 58, .1), (27, 54, .8), (43, 58, .9), (60, 54, .08)], .8, "buddha-lotus-dry", "#bcb9af", dry=True),
        r([(28, 30, .1), (36, 34, .75), (44, 30, .08)], .75, "buddha-hands", "#77746a", dry=True),
    ],
    "confucius": portrait("confucius", 25, 18) + [
        r([(37, 28, .1), (45, 34, .75), (54, 35, .08)], 1.1, "confucius-hand"),
        r([(46, 25, .1), (57, 22, .8), (64, 26, .08)], 1.7, "confucius-tablet-top"),
        r([(47, 26, .1), (48, 42, .75), (50, 54, .08)], 1.0, "confucius-tablet-left", "#77746a", dry=True),
        r([(63, 26, .1), (61, 41, .75), (62, 53, .08)], .7, "confucius-tablet-right", "#bcb9af", dry=True),
        r([(52, 35, .1), (57, 32, .75), (61, 35, .08)], .65, "confucius-mark", "#77746a", dry=True),
        ground("confucius"),
    ],
    "curie": portrait("curie", 24, 19) + [
        r([(36, 29, .1), (45, 35, .75), (53, 37, .08)], 1.1, "curie-hand"),
        r([(55, 20, .1), (54, 31, .75), (49, 43, .9), (45, 52, .75), (53, 57, .9), (63, 53, .75), (59, 43, .9), (55, 32, .08)], 1.5, "curie-flask"),
        r([(47, 49, .1), (54, 52, .75), (61, 49, .08)], .7, "curie-liquid", "#bcb9af", dry=True),
        dab(62, 23, 1.8, 1.8, "#77746a"), dab(66, 16, 1.2, 1.2, "#bcb9af"),
        ground("curie"),
    ],
    "diaper": [
        r([(14, 18, .1), (35, 14, .9), (59, 19, .08)], 2.0, "diaper-top"),
        r([(14, 18, .1), (20, 35, .75), (30, 55, .08)], 1.7, "diaper-left"),
        r([(59, 19, .1), (52, 35, .75), (42, 55, .08)], 1.0, "diaper-right", "#77746a", dry=True),
        r([(30, 55, .1), (36, 51, .75), (42, 55, .08)], 1.4, "diaper-base"),
        r([(19, 29, .1), (35, 37, .85), (54, 28, .08)], .8, "diaper-fold", "#bcb9af", dry=True),
        dab(18, 20, 1.7, 1.7), dab(55, 20, 1.5, 1.5, "#77746a"),
    ],
    "dream": [
        dab(24, 45, 3.3, 3.5),
        r([(24, 49, .1), (35, 53, .75), (48, 51, .08)], 2.0, "dream-sleeper"),
        r([(16, 55, .1), (32, 59, .8), (53, 56, .08)], 1.0, "dream-bed", "#77746a", dry=True),
        dab(42, 28, 1.6, 1.6, "#77746a"), dab(49, 21, 2.0, 2.0, "#bcb9af"),
        r([(43, 16, .1), (51, 10, .75), (61, 14, .9), (64, 23, .75), (58, 29, .9), (50, 27, .08)], 1.0, "dream-cloud", "#77746a", dry=True),
        r([(8, 64, .1), (29, 61, .85), (59, 63, .08)], .65, "dream-ground", "#bcb9af", dry=True),
    ],
    "faith": [
        r([(15, 53, .1), (13, 39, .75), (20, 24, .9), (34, 17, .85), (49, 24, .75), (57, 40, .9), (53, 54, .75), (36, 61, .9), (22, 57, .08)], 2.1, "faith-vessel"),
        r([(36, 49, .1), (31, 40, .75), (35, 31, .9), (32, 23, .75), (38, 15, .9), (44, 25, .75), (41, 35, .9), (45, 43, .08)], 2.0, "faith-flame"),
        r([(32, 53, .1), (37, 50, .75), (43, 53, .08)], .7, "faith-base", "#bcb9af", dry=True),
        dab(56, 16, 1.6, 1.6, "#bcb9af"),
    ],
    "hildegard": portrait("hildegard", 24, 19) + [
        r([(37, 29, .1), (46, 34, .75), (54, 35, .08)], 1.0, "hildegard-hand"),
        r([(55, 58, .1), (55, 43, .75), (57, 27, .08)], 1.8, "hildegard-stem"),
        m("M 55 36 C 47 29 39 29 34 34 C 40 42 47 44 55 40 Z", "#4a4943"),
        m("M 58 31 C 63 25 68 25 70 29 C 66 35 62 37 58 35 Z", "#77746a"),
        r([(52, 18, .1), (57, 13, .75), (63, 17, .9), (62, 23, .75), (56, 25, .9), (52, 18, .08)], .75, "hildegard-vision", "#bcb9af", dry=True),
        ground("hildegard"),
    ],
    "hypatia": portrait("hypatia", 23, 19) + [
        r([(35, 29, .1), (44, 34, .75), (52, 36, .08)], 1.0, "hypatia-hand"),
        r([(48, 21, .1), (58, 17, .8), (66, 23, .9), (65, 34, .8), (57, 40, .9), (48, 35, .8), (46, 26, .08)], 1.5, "hypatia-astrolabe"),
        r([(56, 18, .1), (56, 39, .85), (57, 51, .08)], .8, "hypatia-axis", "#77746a", dry=True),
        r([(47, 28, .1), (56, 26, .75), (65, 28, .08)], .65, "hypatia-cross", "#bcb9af", dry=True),
        ground("hypatia"),
    ],
    "ibnsina": portrait("ibnsina", 23, 19) + [
        r([(35, 29, .1), (44, 35, .75), (52, 37, .08)], 1.0, "ibnsina-hand"),
        r([(46, 38, .1), (50, 49, .75), (59, 54, .9), (66, 49, .08)], 1.7, "ibnsina-bowl"),
        r([(45, 37, .1), (55, 34, .8), (66, 37, .08)], .8, "ibnsina-rim", "#77746a", dry=True),
        r([(55, 34, .1), (55, 26, .75), (58, 20, .08)], .75, "ibnsina-herb", "#bcb9af", dry=True),
        m("M 57 23 C 62 18 67 18 69 21 C 66 26 62 28 57 26 Z", "#4a4943"),
        ground("ibnsina"),
    ],
    "laozi": portrait("laozi", 25, 20) + [
        r([(22, 23, .1), (18, 30, .75), (21, 38, .08)], .9, "laozi-beard-a", "#77746a", dry=True),
        r([(27, 23, .1), (30, 31, .75), (27, 40, .08)], .7, "laozi-beard-b", "#bcb9af", dry=True),
        r([(51, 13, .1), (50, 35, .75), (52, 62, .08)], 1.5, "laozi-staff", "#77746a", dry=True),
        r([(38, 31, .1), (44, 36, .75), (50, 35, .08)], 1.0, "laozi-hand"),
        r([(52, 17, .1), (58, 13, .75), (63, 15, .08)], .65, "laozi-leaf", "#bcb9af", dry=True),
        ground("laozi"),
    ],
    "legacy": [
        r([(19, 61, .1), (20, 45, .75), (22, 26, .08)], 2.5, "legacy-tree"),
        m("M 21 33 C 14 26 7 25 3 29 C 8 36 14 39 21 36 Z", "#4a4943"),
        m("M 23 29 C 31 21 41 20 47 25 C 42 34 33 38 24 34 Z", "#77746a"),
        dab(52, 37, 2.8, 3.0, "#77746a"),
        r([(52, 41, .1), (51, 50, .75), (53, 59, .08)], 1.4, "legacy-child"),
        r([(22, 42, .1), (34, 43, .75), (49, 40, .08)], 1.0, "legacy-gift", "#77746a", dry=True),
        ground("legacy"),
    ],
    "maimonides": portrait("maimonides", 24, 19) + [
        r([(36, 29, .1), (45, 34, .75), (53, 36, .08)], 1.0, "maimonides-hand"),
        r([(46, 38, .1), (54, 35, .8), (64, 39, .08)], 1.4, "maimonides-book"),
        r([(46, 39, .1), (48, 50, .75), (54, 55, .08)], .8, "maimonides-page-a", "#77746a", dry=True),
        r([(64, 39, .1), (62, 49, .75), (55, 55, .08)], .65, "maimonides-page-b", "#bcb9af", dry=True),
        r([(58, 28, .1), (55, 23, .75), (59, 18, .9), (63, 24, .08)], 1.0, "maimonides-lamp"),
        ground("maimonides"),
    ],
    "meaning": [
        r([(15, 48, .1), (13, 35, .75), (20, 22, .9), (34, 17, .85), (48, 23, .75), (55, 37, .9), (50, 51, .75), (36, 58, .9), (23, 54, .08)], 2.0, "meaning-ring"),
        dab(35, 37, 4.5, 4.5, "#4a4943"),
        r([(35, 20, .1), (35, 29, .75), (35, 37, .08)], .8, "meaning-axis-a", "#77746a", dry=True),
        r([(35, 42, .1), (35, 50, .75), (36, 57, .08)], .65, "meaning-axis-b", "#bcb9af", dry=True),
        dab(55, 16, 1.6, 1.6, "#bcb9af"),
    ],
    "memory": [
        r([(17, 25, .1), (19, 42, .75), (26, 56, .9), (41, 59, .75), (52, 47, .9), (54, 28, .08)], 2.5, "memory-vessel"),
        r([(15, 24, .1), (34, 21, .9), (57, 25, .08)], 1.8, "memory-rim"),
        r([(44, 45, .1), (43, 35, .75), (35, 31, .9), (28, 35, .75), (29, 43, .9), (36, 47, .75), (40, 42, .9), (38, 37, .08)], 1.1, "memory-spiral", "#77746a", dry=True),
        r([(26, 53, .1), (35, 56, .75), (44, 52, .08)], .65, "memory-dry", "#bcb9af", dry=True),
    ],
    "myth": [
        r([(8, 39, .1), (22, 34, .8), (35, 39, .9), (49, 33, .8), (63, 37, .08)], 2.0, "myth-book"),
        r([(9, 40, .1), (12, 53, .75), (18, 59, .08)], 1.2, "myth-page-a"),
        r([(62, 38, .1), (59, 51, .75), (53, 57, .08)], .8, "myth-page-b", "#77746a", dry=True),
        r([(35, 37, .1), (34, 27, .75), (40, 20, .9), (38, 12, .75), (44, 7, .08)], 1.5, "myth-rising"),
        r([(42, 10, .1), (50, 8, .75), (57, 12, .08)], .7, "myth-wing", "#bcb9af", dry=True),
        dab(45, 7, 1.8, 1.8),
    ],
    "newton": portrait("newton", 24, 19) + [
        r([(36, 29, .1), (45, 34, .75), (53, 36, .08)], 1.0, "newton-hand"),
        r([(54, 57, .1), (54, 42, .75), (56, 25, .08)], 1.6, "newton-tree"),
        m("M 55 32 C 48 25 39 25 35 30 C 41 38 48 41 55 36 Z", "#4a4943"),
        m("M 58 29 C 63 23 68 23 70 27 C 67 33 63 35 58 33 Z", "#77746a"),
        dab(65, 41, 2.4, 2.4),
        r([(65, 31, .1), (66, 36, .75), (65, 41, .08)], .65, "newton-fall", "#bcb9af", dry=True),
        ground("newton"),
    ],
    "path": [
        r([(7, 61, .1), (18, 48, .75), (30, 54, .9), (42, 39, .9), (56, 43, .75), (65, 27, .08)], 2.3, "path-main"),
        dab(8, 61, 2.3, 2.3, "#77746a"), dab(65, 24, 2.0, 2.0),
        r([(13, 31, .1), (21, 23, .75), (30, 31, .08)], 1.0, "path-hill", "#77746a", dry=True),
        ground("path"),
    ],
    "pilgrimage": [
        dab(28, 17, 3.4, 3.7),
        r([(28, 21, .1), (25, 35, .75), (30, 49, .08)], 2.4, "pilgrimage-body"),
        r([(30, 49, .1), (22, 58, .75), (16, 63, .08)], 1.2, "pilgrimage-leg-a"),
        r([(30, 49, .1), (40, 57, .75), (49, 61, .08)], .75, "pilgrimage-leg-b", "#77746a", dry=True),
        r([(51, 10, .1), (50, 34, .75), (52, 63, .08)], 1.4, "pilgrimage-staff", "#77746a", dry=True),
        r([(28, 34, .1), (39, 36, .75), (49, 34, .08)], 1.1, "pilgrimage-hand"),
        r([(8, 64, .1), (29, 61, .85), (61, 63, .08)], .65, "pilgrimage-ground", "#bcb9af", dry=True),
    ],
    "place": [
        r([(13, 52, .1), (12, 38, .75), (20, 25, .9), (35, 20, .85), (49, 27, .75), (56, 41, .9), (51, 55, .75), (36, 62, .9), (22, 58, .08)], 2.2, "place-marker"),
        dab(35, 40, 5.0, 5.0, "#4a4943"),
        r([(20, 61, .1), (35, 57, .75), (52, 60, .08)], .7, "place-ground", "#bcb9af", dry=True),
        dab(55, 18, 1.5, 1.5, "#bcb9af"),
    ],
    "prayer": [
        r([(18, 56, .1), (23, 43, .75), (30, 29, .9), (35, 14, .08)], 2.6, "prayer-hand-a"),
        r([(53, 56, .1), (48, 43, .75), (41, 29, .9), (35, 14, .08)], 1.5, "prayer-hand-b", "#77746a", dry=True),
        r([(24, 49, .1), (35, 45, .75), (47, 49, .08)], .8, "prayer-fold", "#bcb9af", dry=True),
        r([(9, 63, .1), (29, 60, .85), (60, 62, .08)], .65, "prayer-ground", "#bcb9af", dry=True),
    ],
    "purpose": [
        r([(14, 48, .1), (12, 35, .75), (20, 22, .9), (34, 17, .85), (48, 23, .75), (55, 37, .9), (50, 51, .75), (36, 58, .9), (23, 54, .08)], 2.0, "purpose-ring"),
        dab(35, 37, 3.6, 3.6, "#4a4943"),
        r([(8, 61, .1), (19, 51, .75), (29, 44, .9), (35, 37, .08)], 2.0, "purpose-path"),
        m("M 30 33 L 40 35 L 35 44 Z", "#262522"),
        r([(49, 18, .1), (55, 13, .75), (61, 16, .08)], .65, "purpose-breath", "#bcb9af", dry=True),
    ],
    "rest": [
        dab(20, 45, 3.3, 3.5),
        r([(20, 49, .1), (33, 53, .75), (48, 50, .08)], 2.2, "rest-body"),
        r([(14, 55, .1), (31, 59, .8), (54, 55, .08)], 1.0, "rest-ground", "#77746a", dry=True),
        r([(54, 58, .1), (54, 42, .75), (56, 25, .08)], 1.6, "rest-tree"),
        m("M 55 33 C 48 26 39 26 35 31 C 41 38 48 41 55 37 Z", "#4a4943"),
        m("M 58 30 C 63 24 68 24 70 28 C 67 34 63 36 58 34 Z", "#77746a"),
        r([(8, 64, .1), (29, 61, .85), (62, 63, .08)], .65, "rest-horizon", "#bcb9af", dry=True),
    ],
    "ritual": [
        dab(18, 28, 2.8, 3.0), dab(36, 21, 3.2, 3.4, "#4a4943"), dab(54, 29, 2.7, 2.9, "#77746a"),
        r([(18, 32, .1), (17, 43, .75), (20, 53, .08)], 1.5, "ritual-person-a"),
        r([(36, 25, .1), (35, 38, .75), (37, 52, .08)], 2.0, "ritual-person-b"),
        r([(54, 33, .1), (53, 43, .75), (54, 53, .08)], .9, "ritual-person-c", "#77746a", dry=True),
        m("M 29 53 C 31 46 40 44 46 49 C 46 55 38 59 30 57 Z", "#4a4943"),
        r([(11, 61, .1), (35, 58, .9), (61, 61, .08)], .7, "ritual-circle", "#bcb9af", dry=True),
    ],
    "rumi": portrait("rumi", 25, 18) + [
        r([(23, 14, .1), (25, 8, .75), (31, 11, .08)], 1.0, "rumi-cap", "#77746a", dry=True),
        r([(37, 29, .1), (47, 22, .75), (58, 14, .08)], 1.2, "rumi-arm-a"),
        r([(20, 30, .1), (12, 39, .75), (5, 46, .08)], .8, "rumi-arm-b", "#bcb9af", dry=True),
        r([(14, 55, .1), (27, 43, .75), (40, 53, .9), (54, 59, .08)], 2.4, "rumi-whirl"),
        r([(17, 60, .1), (35, 56, .85), (57, 60, .08)], .7, "rumi-ground", "#bcb9af", dry=True),
    ],
    "secret": [
        r([(10, 56, .1), (17, 45, .75), (15, 33, .9), (21, 21, .9), (34, 16, .75), (42, 24, .9), (39, 35, .75), (31, 42, .08)], 2.1, "secret-profile"),
        r([(29, 42, .1), (35, 49, .75), (41, 55, .08)], .9, "secret-neck", "#77746a", dry=True),
        r([(42, 33, .1), (51, 31, .75), (59, 34, .08)], .9, "secret-whisper", "#77746a", dry=True),
        dab(61, 34, 1.7, 1.7, "#bcb9af"),
        r([(8, 62, .1), (25, 59, .85), (45, 61, .08)], .65, "secret-ground", "#bcb9af", dry=True),
    ],
    "shadow": [
        dab(23, 17, 3.5, 3.8),
        r([(23, 21, .1), (22, 36, .75), (25, 51, .08)], 2.4, "shadow-person"),
        r([(25, 51, .1), (17, 59, .75), (11, 64, .08)], 1.1, "shadow-leg-a"),
        r([(25, 51, .1), (34, 58, .75), (42, 62, .08)], .7, "shadow-leg-b", "#77746a", dry=True),
        m("M 30 55 C 42 50 56 52 66 60 C 54 65 41 64 30 59 Z", "#77746a"),
        r([(32, 58, .1), (45, 56, .75), (59, 60, .08)], .65, "shadow-dry", "#bcb9af", dry=True),
        ground("shadow"),
    ],
    "shelter": [
        r([(8, 57, .1), (10, 39, .75), (20, 24, .9), (36, 17, .85), (52, 25, .75), (62, 44, .08)], 2.8, "shelter-roof"),
        dab(36, 37, 3.3, 3.5),
        r([(36, 41, .1), (35, 50, .75), (37, 59, .08)], 1.9, "shelter-person"),
        r([(29, 59, .1), (36, 56, .75), (44, 59, .08)], .7, "shelter-base", "#77746a", dry=True),
        r([(8, 63, .1), (29, 60, .85), (62, 62, .08)], .65, "shelter-ground", "#bcb9af", dry=True),
    ],
    "shrine": [
        r([(10, 25, .1), (34, 21, .9), (61, 25, .08)], 2.8, "shrine-roof"),
        r([(16, 29, .1), (16, 45, .75), (17, 59, .08)], 1.8, "shrine-post-a"),
        r([(55, 28, .1), (54, 44, .75), (55, 58, .08)], 1.0, "shrine-post-b", "#77746a", dry=True),
        r([(13, 34, .1), (34, 31, .85), (58, 34, .08)], 1.3, "shrine-beam"),
        m("M 30 49 C 32 43 40 41 45 45 C 45 51 38 55 31 53 Z", "#4a4943"),
        r([(12, 62, .1), (34, 59, .9), (59, 61, .08)], .7, "shrine-ground", "#bcb9af", dry=True),
    ],
    "socrates": portrait("socrates", 24, 19) + [
        r([(20, 23, .1), (17, 30, .75), (20, 38, .08)], .9, "socrates-beard", "#77746a", dry=True),
        r([(36, 29, .1), (45, 34, .75), (53, 35, .08)], 1.0, "socrates-hand"),
        r([(46, 24, .1), (54, 19, .75), (62, 23, .08)], 1.1, "socrates-dialogue-a"),
        r([(48, 32, .1), (58, 28, .75), (66, 33, .08)], .7, "socrates-dialogue-b", "#bcb9af", dry=True),
        m("M 49 43 C 52 38 61 37 65 42 C 64 48 56 51 50 48 Z", "#4a4943"),
        ground("socrates"),
    ],
    "spirit": [
        r([(36, 61, .1), (28, 51, .75), (30, 40, .9), (24, 29, .75), (34, 15, .9), (45, 28, .75), (42, 40, .9), (48, 49, .75), (36, 61, .08)], 2.5, "spirit-flame"),
        r([(32, 50, .1), (36, 42, .75), (40, 49, .08)], .75, "spirit-core", "#77746a", dry=True),
        r([(15, 57, .1), (25, 53, .75), (34, 57, .08)], .65, "spirit-breath-a", "#bcb9af", dry=True),
        r([(42, 59, .1), (52, 55, .75), (61, 59, .08)], .65, "spirit-breath-b", "#77746a", dry=True),
        dab(56, 18, 1.7, 1.7, "#bcb9af"),
    ],
    "story": [
        r([(8, 38, .1), (22, 33, .8), (35, 38, .9), (49, 32, .8), (63, 36, .08)], 2.0, "story-book"),
        r([(9, 39, .1), (12, 52, .75), (18, 58, .08)], 1.2, "story-page-a"),
        r([(62, 37, .1), (59, 50, .75), (53, 56, .08)], .8, "story-page-b", "#77746a", dry=True),
        r([(35, 36, .1), (36, 25, .75), (42, 16, .9), (50, 12, .08)], 1.4, "story-rising"),
        dab(52, 11, 1.9, 1.9),
        r([(42, 23, .1), (49, 19, .75), (57, 22, .08)], .65, "story-breath", "#bcb9af", dry=True),
    ],
    "stroller": [
        r([(15, 30, .1), (33, 22, .8), (51, 28, .9), (56, 43, .08)], 2.2, "stroller-canopy"),
        r([(15, 31, .1), (21, 47, .75), (34, 52, .9), (55, 44, .08)], 1.7, "stroller-body"),
        dab(27, 57, 4.0, 4.0), dab(49, 54, 3.6, 3.6, "#77746a"),
        r([(55, 29, .1), (62, 24, .75), (66, 20, .08)], 1.2, "stroller-handle", "#77746a", dry=True),
        r([(8, 64, .1), (29, 61, .85), (62, 63, .08)], .65, "stroller-ground", "#bcb9af", dry=True),
    ],
    "temple": [
        r([(10, 27, .1), (34, 22, .9), (62, 27, .08)], 2.8, "temple-roof"),
        r([(16, 32, .1), (16, 45, .75), (17, 59, .08)], 1.7, "temple-column-a"),
        r([(35, 29, .1), (34, 44, .75), (35, 59, .08)], 1.1, "temple-column-b", "#77746a", dry=True),
        r([(56, 31, .1), (55, 45, .75), (56, 58, .08)], .8, "temple-column-c", "#bcb9af", dry=True),
        r([(12, 62, .1), (34, 59, .9), (60, 61, .08)], 1.5, "temple-base"),
        r([(25, 18, .1), (34, 13, .75), (44, 18, .08)], .75, "temple-breath", "#bcb9af", dry=True),
    ],
    "trickster": [
        dab(34, 23, 3.8, 4.0),
        r([(22, 19, .1), (33, 13, .8), (46, 19, .08)], 1.8, "trickster-mask"),
        r([(34, 27, .1), (32, 40, .75), (36, 53, .08)], 2.4, "trickster-body"),
        r([(33, 35, .1), (22, 29, .75), (13, 31, .08)], 1.2, "trickster-arm-a"),
        r([(35, 35, .1), (48, 29, .75), (60, 31, .08)], .8, "trickster-arm-b", "#77746a", dry=True),
        r([(36, 53, .1), (47, 58, .75), (58, 53, .9), (63, 44, .08)], 1.5, "trickster-tail"),
        r([(8, 64, .1), (29, 61, .85), (61, 63, .08)], .65, "trickster-ground", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} final people glyphs as naturalist sumi-e studies")
