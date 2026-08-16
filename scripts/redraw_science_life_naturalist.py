#!/usr/bin/env python3
"""Redraw life, health, and biological science glyphs as naturalist sumi-e."""

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
    return r([(7, 63, .1), (29, 59, .85), (63, 62, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def leaf(x: float, y: float, flip=False, color="#4a4943") -> str:
    s = -1 if flip else 1
    return m(
        f"M {x} {y} C {x + 7*s} {y - 8} {x + 16*s} {y - 7} {x + 20*s} {y - 2} "
        f"C {x + 14*s} {y + 5} {x + 6*s} {y + 5} {x} {y} Z",
        color,
    )


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e life study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "ancestor": [
        r([(36, 62, .1), (36, 44, .8), (35, 27, .08)], 2.8, "ancestor-trunk"),
        r([(35, 37, .1), (24, 28, .8), (14, 19, .08)], 1.7, "ancestor-branch-a"),
        r([(36, 33, .1), (47, 25, .8), (58, 16, .08)], 1.1, "ancestor-branch-b", "#77746a", dry=True),
        dab(13, 18, 4.3, 4.3), dab(59, 15, 3.8, 3.8, "#77746a"), dab(35, 25, 3.2, 3.2, "#4a4943"),
        ground("ancestor"),
    ],
    "being": [
        dab(36, 15, 5.2, 5.5),
        r([(36, 22, .1), (34, 39, .85), (36, 57, .08)], 3.3, "being-body"),
        r([(34, 32, .1), (22, 39, .8), (12, 46, .08)], 1.4, "being-arm-a"),
        r([(36, 31, .1), (48, 37, .8), (60, 43, .08)], .9, "being-arm-b", "#77746a", dry=True),
        r([(35, 55, .1), (27, 63, .75), (21, 66, .08)], 1.1, "being-leg-a"),
        r([(37, 55, .1), (46, 62, .75), (53, 65, .08)], .65, "being-leg-b", "#bcb9af", dry=True),
    ],
    "body": [
        dab(35, 13, 5.0, 5.2),
        m("M 29 21 C 23 29 24 42 29 50 L 24 64 L 34 65 L 36 48 L 40 65 L 50 63 L 43 49 C 48 38 47 27 41 21 Z", "#4a4943"),
        r([(29, 27, .1), (18, 36, .8), (10, 42, .08)], 1.2, "body-arm-a", "#77746a", dry=True),
        r([(42, 27, .1), (53, 34, .8), (63, 39, .08)], .7, "body-arm-b", "#bcb9af", dry=True),
    ],
    "care": [
        m("M 36 54 C 28 47 18 40 18 30 C 18 22 27 20 33 27 C 38 18 49 20 53 29 C 55 38 45 48 36 54 Z", "#77746a"),
        r([(8, 62, .1), (25, 57, .85), (45, 61, .9), (64, 55, .08)], 1.2, "care-hand"),
        r([(20, 31, .1), (28, 25, .75), (35, 29, .08)], .65, "care-breath", "#bcb9af", dry=True),
    ],
    "cause": [
        dab(15, 37, 5.0, 5.0),
        r([(21, 37, .1), (34, 31, .85), (48, 35, .08)], 2.5, "cause-arrow"),
        m("M 45 28 L 59 35 L 47 43 Z", "#4a4943"),
        r([(10, 55, .1), (29, 51, .8), (57, 54, .08)], .65, "cause-ground", "#bcb9af", dry=True),
    ],
    "clinic": [
        r([(12, 61, .1), (12, 25, .75), (36, 11, .9), (60, 25, .75), (60, 61, .08)], 2.8, "clinic-building"),
        r([(12, 26, .1), (35, 23, .85), (60, 26, .08)], 2.0, "clinic-eave", "#77746a"),
        m("M 31 29 L 41 29 L 41 36 L 49 36 L 49 46 L 41 46 L 41 55 L 31 55 L 31 46 L 23 46 L 23 36 L 31 36 Z", "#4a4943"),
        r([(10, 64, .1), (35, 61, .8), (62, 64, .08)], 1.0, "clinic-ground", "#77746a", dry=True),
    ],
    "death": [
        r([(36, 61, .1), (36, 44, .8), (35, 27, .08)], 2.7, "death-trunk"),
        r([(35, 39, .1), (24, 31, .8), (13, 25, .08)], 1.4, "death-branch-a"),
        r([(36, 35, .1), (47, 27, .8), (60, 24, .08)], .8, "death-branch-b", "#77746a", dry=True),
        leaf(33, 24, False, "#bcb9af"),
        r([(9, 63, .1), (29, 60, .85), (61, 62, .08)], .65, "death-ground", "#bcb9af", dry=True),
    ],
    "effect": [
        r([(9, 36, .1), (23, 31, .8), (37, 35, .08)], 1.2, "effect-arrow", "#77746a", dry=True),
        m("M 34 28 L 48 35 L 36 43 Z", "#77746a"),
        r([(48, 35, .1), (55, 28, .75), (62, 20, .08)], 2.8, "effect-rise"),
        dab(63, 18, 4.4, 4.4),
        ground("effect"),
    ],
    "exercise": [
        dab(37, 13, 4.6, 4.8),
        r([(36, 20, .1), (33, 35, .85), (39, 47, .08)], 3.0, "exercise-body"),
        r([(34, 28, .1), (21, 20, .8), (10, 23, .08)], 1.7, "exercise-arm-a"),
        r([(35, 28, .1), (48, 23, .8), (62, 27, .08)], 1.0, "exercise-arm-b", "#77746a", dry=True),
        r([(38, 46, .1), (25, 55, .8), (14, 64, .08)], 1.5, "exercise-leg-a"),
        r([(39, 47, .1), (51, 53, .8), (62, 61, .08)], .8, "exercise-leg-b", "#bcb9af", dry=True),
    ],
    "generation": [
        r([(12, 60, .1), (12, 48, .75), (13, 38, .08)], 1.1, "generation-one"),
        leaf(12, 42, False, "#bcb9af"),
        r([(35, 61, .1), (35, 43, .8), (36, 27, .08)], 2.0, "generation-two"),
        leaf(35, 34, True, "#77746a"),
        r([(59, 60, .1), (58, 37, .8), (60, 15, .08)], 2.7, "generation-three"),
        leaf(59, 24, True, "#4a4943"),
        ground("generation"),
    ],
    "hygiene": [
        r([(15, 50, .1), (21, 58, .8), (32, 59, .9), (39, 51, .08)], 2.1, "hygiene-hand"),
        r([(38, 51, .1), (45, 46, .75), (52, 39, .08)], 1.1, "hygiene-thumb", "#77746a", dry=True),
        m("M 21 15 C 14 24 15 32 22 35 C 30 31 31 23 21 15 Z", "#4a4943"),
        m("M 43 11 C 37 19 38 27 44 30 C 51 26 52 18 43 11 Z", "#77746a"),
        dab(59, 31, 2.3, 2.3, "#bcb9af"),
        ground("hygiene"),
    ],
    "medicine": [
        m("M 27 9 L 45 9 L 46 18 L 26 18 Z", "#4a4943"),
        r([(26, 18, .1), (21, 28, .75), (21, 56, .9), (50, 58, .75), (52, 29, .9), (46, 18, .08)], 2.7, "medicine-bottle"),
        r([(27, 39, .1), (46, 39, .08)], 2.0, "medicine-cross-horizontal"),
        r([(36, 29, .1), (36, 49, .08)], 2.0, "medicine-cross-vertical"),
        dab(59, 49, 4.2, 2.4, "#77746a"),
        r([(56, 47, .1), (62, 51, .08)], 1.1, "medicine-pill-band", "#bcb9af", dry=True),
    ],
    "migration": [
        r([(6, 29, .1), (14, 22, .8), (23, 29, .08)], 2.0, "migration-bird-a"),
        r([(23, 29, .1), (31, 20, .8), (41, 26, .08)], 1.5, "migration-bird-b", "#77746a", dry=True),
        r([(42, 26, .1), (51, 16, .8), (65, 21, .08)], .8, "migration-bird-c", "#bcb9af", dry=True),
        r([(9, 52, .1), (25, 47, .8), (42, 52, .9), (59, 46, .08)], 1.3, "migration-wind"),
        ground("migration"),
    ],
    "nutrition": [
        r([(35, 25, .1), (25, 19, .75), (14, 27, .9), (12, 42, .85), (20, 55, .75), (34, 60, .9), (48, 55, .75), (57, 42, .9), (55, 28, .75), (45, 20, .9), (35, 25, .08)], 3.0, "nutrition-apple"),
        r([(36, 24, .1), (36, 15, .75), (39, 8, .08)], 2.0, "nutrition-stem"),
        leaf(42, 15, False, "#4a4943"),
        r([(18, 62, .1), (35, 59, .85), (54, 62, .08)], 1.0, "nutrition-ground", "#bcb9af", dry=True),
    ],
    "origin": [
        m("M 36 23 C 26 29 23 41 30 49 C 37 55 48 49 50 39 C 51 29 44 20 36 14 C 35 17 35 20 36 23 Z", "#4a4943"),
        r([(35, 48, .1), (35, 55, .75), (36, 62, .08)], 1.4, "origin-root"),
        r([(35, 56, .1), (26, 61, .75), (19, 63, .08)], .8, "origin-root-a", "#77746a", dry=True),
        r([(36, 57, .1), (47, 60, .75), (56, 61, .08)], .65, "origin-root-b", "#bcb9af", dry=True),
        dab(39, 34, 2.0, 2.0, "#bcb9af"),
    ],
    "prevention": [
        r([(36, 10, .1), (47, 17, .8), (59, 20, .9), (57, 38, .85), (49, 52, .9), (36, 63, .9), (23, 53, .85), (15, 39, .9), (13, 20, .8), (25, 17, .75), (36, 10, .08)], 2.4, "prevention-shield", "#77746a", dry=True),
        r([(36, 23, .1), (35, 39, .85), (36, 52, .08)], 2.6, "prevention-stem"),
        leaf(35, 34, True, "#262522"),
        r([(19, 26, .1), (28, 21, .75), (37, 23, .08)], .65, "prevention-glint", "#bcb9af", dry=True),
    ],
    "recovery": [
        r([(7, 56, .1), (18, 49, .8), (29, 52, .9), (38, 43, .9), (47, 33, .8), (59, 26, .08)], 2.4, "recovery-rise"),
        m("M 55 20 L 67 23 L 60 33 Z", "#4a4943"),
        r([(29, 52, .1), (29, 41, .75), (31, 31, .08)], 1.0, "recovery-stem", "#77746a", dry=True),
        leaf(30, 37, False, "#77746a"),
        ground("recovery"),
    ],
    "renewal": [
        r([(17, 54, .1), (10, 43, .75), (12, 29, .9), (23, 18, .8), (39, 15, .9), (54, 23, .75), (61, 36, .08)], 2.2, "renewal-cycle"),
        m("M 57 31 L 66 37 L 58 44 Z", "#4a4943"),
        r([(36, 57, .1), (36, 46, .75), (38, 36, .08)], 1.3, "renewal-stem"),
        leaf(37, 42, True, "#77746a"),
        ground("renewal"),
    ],
    "repair": [
        r([(10, 40, .1), (23, 32, .8), (34, 38, .08)], 2.5, "repair-broken-a"),
        r([(38, 35, .1), (49, 27, .8), (62, 32, .08)], 1.5, "repair-broken-b", "#77746a", dry=True),
        r([(32, 29, .1), (36, 36, .8), (40, 43, .08)], 1.0, "repair-bind-a"),
        r([(28, 44, .1), (35, 37, .8), (43, 30, .08)], .7, "repair-bind-b", "#bcb9af", dry=True),
        dab(36, 36, 2.4, 2.4), ground("repair"),
    ],
    "resilience": [
        r([(15, 60, .1), (25, 48, .8), (31, 34, .9), (25, 22, .8), (15, 16, .08)], 2.4, "resilience-bend"),
        r([(31, 35, .1), (43, 31, .75), (57, 34, .08)], 1.1, "resilience-wind", "#77746a", dry=True),
        leaf(29, 30, False, "#4a4943"),
        r([(9, 63, .1), (27, 60, .85), (55, 62, .08)], .65, "resilience-ground", "#bcb9af", dry=True),
    ],
    "species": [
        r([(35, 61, .1), (35, 45, .8), (36, 31, .08)], 2.5, "species-trunk"),
        r([(35, 43, .1), (23, 34, .8), (13, 23, .08)], 1.6, "species-branch-a"),
        r([(36, 40, .1), (48, 31, .8), (61, 23, .08)], 1.0, "species-branch-b", "#77746a", dry=True),
        leaf(13, 23, False, "#4a4943"), leaf(60, 23, True, "#77746a"),
        dab(35, 29, 3.2, 3.2, "#bcb9af"), ground("species"),
    ],
    "therapy": [
        m("M 36 55 C 27 47 16 39 16 28 C 16 20 25 17 32 25 C 37 15 50 18 54 27 C 57 38 46 48 36 55 Z", "#77746a"),
        r([(10, 62, .1), (24, 55, .8), (37, 59, .9), (55, 51, .08)], 1.4, "therapy-hand"),
        r([(36, 47, .1), (36, 37, .75), (38, 29, .08)], .9, "therapy-stem", "#bcb9af", dry=True),
        leaf(37, 35, True, "#4a4943"),
    ],
    "vaccine": [
        m("M 18 29 L 51 29 L 51 43 L 18 43 Z", "#77746a"),
        r([(18, 29, .1), (34, 27, .85), (51, 30, .08)], 1.7, "vaccine-barrel-top"),
        r([(18, 43, .1), (34, 41, .85), (51, 43, .08)], 1.7, "vaccine-barrel-base"),
        r([(7, 36, .1), (18, 35, .85)], 2.3, "vaccine-plunger"),
        r([(7, 28, .1), (7, 36, .75), (7, 45, .08)], 2.0, "vaccine-plunger-grip"),
        r([(51, 36, .1), (61, 35, .75), (68, 34, .08)], 1.6, "vaccine-needle"),
        r([(26, 31, .1), (26, 41, .08)], 1.1, "vaccine-mark-a", "#bcb9af", dry=True),
        r([(35, 31, .1), (35, 41, .08)], 1.1, "vaccine-mark-b", "#bcb9af", dry=True),
    ],
    "well": [
        r([(13, 32, .1), (35, 28, .9), (60, 32, .08)], 2.5, "well-rim"),
        r([(15, 33, .1), (17, 54, .8), (36, 61, .9), (55, 55, .8), (58, 33, .08)], 2.0, "well-bowl"),
        r([(23, 52, .1), (35, 48, .8), (48, 52, .08)], 1.1, "well-water", "#77746a", dry=True),
        m("M 36 38 C 31 43 31 49 36 52 C 42 49 42 43 36 38 Z", "#4a4943"),
        r([(9, 64, .1), (29, 61, .85), (61, 63, .08)], .65, "well-ground", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} science life/health glyphs as sumi-e studies")
