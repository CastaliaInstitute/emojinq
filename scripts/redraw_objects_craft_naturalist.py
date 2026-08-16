#!/usr/bin/env python3
"""Redraw the craft and workshop object plate as naturalist sumi-e studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "objects"


def pts(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def r(values, width, seed, color="#262522", *, dry=False) -> str:
    # Concrete tools and vessels must survive the same 32px recognition test as
    # familiar emoji.  Keep the pressure hierarchy, but do not let secondary
    # anatomy collapse into hairlines.
    width = max(width * 1.35, 1.2)
    d = stroke_path(
        pts(*values), width=width, seed=seed, wobble=.26,
        taper_start=.10, taper_end=.08,
    )
    return (
        f'<path class="{"ink-dry" if dry else "ink-wash"}" d="{d}" '
        f'fill="{color}" data-ink-brush-pass="'
        f'{"dry-edge-v2" if dry else "loaded-ribbon-v2"}"/>'
    )


def m(d: str, color="#4a4943") -> str:
    return (
        f'<path class="ink-wash" d="{d}" fill="{color}" '
        'data-ink-brush-pass="loaded-mass-v2"/>'
    )


def dab(cx, cy, rx, ry, color="#262522") -> str:
    return (
        f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'
    )


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="objects / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>objects / {name} — naturalist sumi-e craft study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "baking": [
        r([(10, 58, .1), (13, 38, .7), (23, 24, .95), (39, 20, .85), (54, 30, .7), (61, 51, .08)], 2.7, "baking-oven"),
        m("M 24 51 C 26 43 34 39 43 43 C 48 46 48 52 45 56 C 36 58 28 56 24 51 Z", "#262522"),
        r([(29, 47, .1), (35, 45, .8), (41, 47, .08)], .75, "baking-loaf-cut", "#bcb9af", dry=True),
        r([(12, 61, .1), (31, 59, .8), (55, 61, .08)], .7, "baking-ground", "#77746a", dry=True),
    ],
    "brewing": [
        r([(16, 35, .1), (18, 50, .8), (27, 58, .95), (43, 58, .8), (52, 48, .8), (54, 34, .08)], 2.8, "brewing-pot"),
        r([(15, 34, .1), (34, 31, .95), (56, 34, .08)], 2.2, "brewing-rim"),
        r([(28, 28, .1), (24, 21, .7), (29, 14, .08)], 1.15, "brewing-steam-a", "#77746a", dry=True),
        r([(41, 28, .1), (46, 20, .7), (42, 11, .08)], .9, "brewing-steam-b", "#bcb9af", dry=True),
        dab(35, 45, 2.1, 2.8, "#77746a"),
    ],
    "brush": [
        r([(13, 58, .1), (27, 46, .75), (40, 32, .95), (56, 14, .08)], 2.4, "brush-handle"),
        m("M 8 63 C 13 54 20 48 29 45 C 25 55 19 62 8 63 Z", "#262522"),
        r([(11, 60, .1), (18, 55, .8), (25, 49, .08)], .72, "brush-bristle-dry", "#bcb9af", dry=True),
        r([(46, 26, .1), (51, 25, .7), (56, 21, .08)], .7, "brush-ferrule", "#77746a", dry=True),
    ],
    "canvas": [
        r([(18, 55, .1), (18, 37, .7), (21, 18, .08)], 2.0, "canvas-left"),
        r([(21, 18, .1), (39, 15, .9), (56, 19, .08)], 2.4, "canvas-top"),
        r([(56, 19, .1), (54, 38, .75), (54, 54, .08)], 1.45, "canvas-right", "#77746a", dry=True),
        r([(18, 55, .1), (36, 58, .9), (54, 54, .08)], 1.1, "canvas-base", "#bcb9af", dry=True),
        r([(36, 57, .1), (32, 63, .7), (28, 67, .08)], 1.5, "canvas-easel-a"),
        r([(38, 57, .1), (44, 64, .7), (49, 67, .08)], .9, "canvas-easel-b", "#77746a", dry=True),
        r([(27, 40, .1), (34, 32, .8), (45, 38, .08)], 1.35, "canvas-mark"),
    ],
    "carving": [
        m("M 13 42 C 25 37 41 38 54 42 L 52 50 C 38 55 24 54 14 49 Z", "#77746a"),
        r([(11, 36, .1), (29, 34, .85), (56, 38, .08)], 2.2, "carving-grain"),
        r([(58, 13, .1), (49, 24, .75), (38, 39, .95), (28, 48, .08)], 2.0, "carving-gouge"),
        m("M 50 17 L 60 9 L 63 13 L 56 22 Z", "#262522"),
        r([(23, 42, .1), (27, 48, .7), (23, 53, .7), (18, 49, .08)], .8, "carving-curl", "#bcb9af", dry=True),
    ],
    "chalk": [
        r([(16, 55, .1), (28, 43, .75), (46, 23, .08)], 4.0, "chalk-stick", "#4a4943"),
        r([(18, 57, .1), (29, 46, .7), (46, 27, .08)], .8, "chalk-dry-core", "#bcb9af", dry=True),
        r([(10, 61, .1), (18, 59, .7), (25, 61, .08)], .7, "chalk-dust", "#77746a", dry=True),
        dab(12, 56, 1.5, 1.1, "#bcb9af"),
    ],
    "clay": [
        m("M 13 53 C 17 41 27 34 39 34 C 51 35 58 44 55 54 C 43 60 25 60 13 53 Z", "#4a4943"),
        r([(17, 51, .1), (30, 47, .75), (44, 50, .9), (55, 46, .08)], 1.4, "clay-thumb"),
        r([(24, 34, .1), (34, 30, .75), (45, 34, .08)], .75, "clay-dry", "#bcb9af", dry=True),
        dab(50, 39, 1.5, 1.2, "#77746a"),
    ],
    "drawing": [
        r([(14, 58, .1), (14, 37, .75), (17, 17, .08)], 1.4, "drawing-paper-left", "#77746a", dry=True),
        r([(17, 17, .1), (34, 14, .85), (54, 18, .08)], 1.55, "drawing-paper-top"),
        r([(54, 18, .1), (51, 37, .75), (52, 55, .08)], .85, "drawing-paper-right", "#bcb9af", dry=True),
        r([(14, 58, .1), (33, 55, .85), (52, 55, .08)], 1.0, "drawing-paper-base", "#77746a", dry=True),
        r([(21, 45, .1), (29, 33, .8), (38, 42, .95), (46, 27, .08)], 2.0, "drawing-gesture"),
        r([(45, 60, .1), (53, 50, .75), (62, 39, .08)], 2.5, "drawing-charcoal"),
    ],
    "dyeing": [
        r([(12, 39, .1), (16, 52, .8), (28, 58, .9), (45, 56, .8), (53, 45, .08)], 2.8, "dyeing-vat"),
        r([(11, 38, .1), (31, 35, .95), (54, 38, .08)], 2.1, "dyeing-rim"),
        r([(29, 36, .1), (35, 26, .8), (45, 18, .9), (58, 14, .08)], 3.0, "dyeing-cloth", "#4a4943"),
        r([(34, 33, .1), (42, 25, .7), (53, 20, .08)], .75, "dyeing-cloth-dry", "#bcb9af", dry=True),
    ],
    "engraving": [
        r([(12, 27, .1), (30, 22, .8), (51, 20, .08)], 2.2, "engraving-plate-top", "#77746a"),
        r([(12, 27, .1), (15, 43, .75), (18, 57, .08)], 1.25, "engraving-plate-left", "#77746a", dry=True),
        r([(51, 20, .1), (54, 34, .75), (57, 50, .08)], 1.1, "engraving-plate-right", "#bcb9af", dry=True),
        r([(18, 57, .1), (36, 53, .8), (57, 50, .08)], 1.4, "engraving-plate-base", "#77746a"),
        r([(20, 45, .1), (27, 35, .75), (35, 42, .9), (44, 29, .08)], 1.0, "engraving-cut", "#bcb9af", dry=True),
        r([(62, 12, .1), (52, 23, .75), (42, 38, .08)], 2.2, "engraving-burin"),
        m("M 57 10 L 64 7 L 67 11 L 62 16 Z", "#262522"),
    ],
    "forging": [
        m("M 10 43 C 18 38 30 38 39 41 L 56 37 L 61 43 L 45 49 L 39 58 L 23 58 L 27 49 L 12 48 Z", "#4a4943"),
        r([(52, 11, .1), (44, 21, .75), (34, 34, .08)], 2.6, "forging-hammer-handle"),
        m("M 42 13 L 52 7 L 62 16 L 54 23 Z", "#262522"),
        r([(35, 28, .1), (29, 20, .7), (24, 15, .08)], .85, "forging-spark-a", "#77746a", dry=True),
        r([(38, 29, .1), (40, 19, .7), (43, 13, .08)], .7, "forging-spark-b", "#bcb9af", dry=True),
    ],
    "frame": [
        r([(14, 57, .1), (15, 38, .75), (18, 16, .08)], 2.5, "frame-left"),
        r([(18, 16, .1), (36, 13, .9), (58, 18, .08)], 2.8, "frame-top"),
        r([(58, 18, .1), (55, 37, .75), (56, 54, .08)], 1.55, "frame-right", "#77746a", dry=True),
        r([(14, 57, .1), (34, 59, .9), (56, 54, .08)], 1.15, "frame-base", "#bcb9af", dry=True),
        r([(24, 46, .1), (32, 34, .8), (43, 42, .08)], 1.15, "frame-subject", "#77746a", dry=True),
    ],
    "handle": [
        r([(15, 53, .1), (14, 35, .75), (23, 22, .95), (37, 18, .85), (51, 26, .75), (56, 43, .08)], 3.3, "handle-curve"),
        r([(23, 52, .1), (23, 38, .75), (29, 30, .9), (39, 29, .75), (48, 38, .08)], 1.35, "handle-inner", "#77746a", dry=True),
        r([(11, 55, .1), (25, 52, .8), (39, 55, .9), (58, 51, .08)], 2.0, "handle-seat"),
    ],
    "joinery": [
        m("M 8 27 L 37 25 L 38 35 L 8 39 Z", "#4a4943"),
        m("M 31 10 L 44 9 L 45 61 L 34 63 Z", "#77746a"),
        r([(11, 31, .1), (22, 29, .75), (35, 30, .08)], .75, "joinery-grain-a", "#bcb9af", dry=True),
        r([(39, 15, .1), (39, 30, .75), (40, 53, .08)], .7, "joinery-grain-b", "#bcb9af", dry=True),
        r([(32, 25, .1), (38, 31, .85), (45, 35, .08)], 1.2, "joinery-lock"),
    ],
    "knife": [
        m("M 8 48 C 22 42 36 32 52 15 C 50 28 43 41 30 50 C 21 55 13 54 8 48 Z", "#4a4943"),
        r([(30, 50, .1), (40, 57, .8), (54, 62, .08)], 4.0, "knife-handle"),
        r([(12, 48, .1), (27, 45, .75), (43, 34, .9), (52, 20, .08)], .72, "knife-edge", "#bcb9af", dry=True),
        r([(36, 52, .1), (41, 48, .7), (45, 46, .08)], 1.0, "knife-bolster", "#77746a", dry=True),
    ],
    "mortar": [
        r([(12, 40, .1), (17, 52, .8), (29, 58, .9), (44, 56, .8), (52, 42, .08)], 3.0, "mortar-bowl"),
        r([(10, 39, .1), (30, 36, .95), (54, 39, .08)], 2.2, "mortar-rim"),
        r([(57, 10, .1), (49, 22, .75), (38, 39, .08)], 4.0, "mortar-pestle", "#4a4943"),
        r([(18, 50, .1), (31, 53, .75), (44, 49, .08)], .72, "mortar-dry", "#bcb9af", dry=True),
    ],
    "oven": [
        r([(10, 59, .1), (11, 39, .7), (21, 23, .95), (37, 17, .85), (53, 26, .75), (60, 49, .08)], 3.0, "oven-dome"),
        m("M 23 57 C 23 44 29 36 37 35 C 46 37 51 46 49 58 Z", "#262522"),
        r([(28, 54, .1), (33, 44, .75), (39, 40, .08)], .85, "oven-mouth-dry", "#77746a", dry=True),
        r([(9, 62, .1), (29, 59, .8), (57, 61, .08)], .72, "oven-ground", "#bcb9af", dry=True),
    ],
    "paint": [
        r([(57, 10, .1), (47, 22, .75), (36, 35, .95), (23, 49, .08)], 2.4, "paint-handle"),
        m("M 14 58 C 16 50 22 44 30 42 C 28 51 23 58 14 58 Z", "#262522"),
        r([(9, 62, .1), (22, 59, .75), (36, 61, .9), (54, 56, .08)], 2.2, "paint-wash", "#77746a", dry=True),
        r([(20, 55, .1), (27, 51, .7), (35, 48, .08)], .7, "paint-bristle", "#bcb9af", dry=True),
    ],
    "pan": [
        r([(10, 39, .1), (15, 51, .75), (28, 57, .9), (43, 54, .8), (50, 43, .08)], 3.0, "pan-bowl"),
        r([(8, 38, .1), (28, 35, .95), (51, 39, .08)], 2.1, "pan-rim"),
        r([(49, 40, .1), (58, 34, .75), (67, 28, .08)], 3.0, "pan-handle"),
        r([(17, 50, .1), (29, 53, .75), (41, 49, .08)], .72, "pan-dry", "#bcb9af", dry=True),
    ],
    "pot": [
        r([(14, 30, .1), (16, 47, .75), (25, 58, .9), (42, 59, .8), (53, 48, .75), (55, 31, .08)], 3.2, "pot-body"),
        r([(12, 30, .1), (33, 27, .95), (58, 31, .08)], 2.5, "pot-rim"),
        r([(20, 22, .1), (33, 19, .8), (48, 22, .08)], 1.7, "pot-lid"),
        dab(34, 16, 2.2, 2.0),
        r([(20, 51, .1), (32, 55, .75), (45, 51, .08)], .72, "pot-dry", "#bcb9af", dry=True),
    ],
    "pottery": [
        r([(25, 19, .1), (22, 31, .75), (27, 42, .95), (24, 53, .08)], 2.5, "pottery-left"),
        r([(45, 18, .1), (48, 31, .75), (43, 42, .9), (47, 53, .08)], 1.65, "pottery-right", "#77746a", dry=True),
        r([(24, 19, .1), (35, 16, .85), (46, 19, .08)], 2.0, "pottery-rim"),
        r([(24, 53, .1), (35, 56, .85), (47, 53, .08)], 2.4, "pottery-foot"),
        r([(10, 63, .1), (32, 60, .9), (60, 63, .08)], 1.1, "pottery-wheel", "#bcb9af", dry=True),
    ],
    "print": [
        # A compact inked block leaves enough white paper around it to read as
        # a printing action instead of a dense square tile.
        m("M 18 16 L 44 13 L 48 38 L 22 41 Z", "#4a4943"),
        r([(22, 22, .1), (31, 28, .8), (40, 20, .08)], 1.0, "print-block-cut", "#bcb9af", dry=True),
        r([(19, 52, .1), (34, 49, .85), (54, 52, .08)], 2.1, "print-impression-top"),
        r([(22, 59, .1), (35, 57, .85), (51, 60, .08)], .85, "print-impression-dry", "#77746a", dry=True),
        dab(56, 44, 2.2, 2.2, "#262522"),
    ],
    "printing": [
        r([(15, 18, .1), (15, 37, .75), (17, 58, .08)], 2.5, "printing-post-left"),
        r([(55, 15, .1), (54, 36, .75), (55, 58, .08)], 1.65, "printing-post-right", "#77746a", dry=True),
        r([(12, 25, .1), (34, 22, .95), (58, 25, .08)], 3.0, "printing-beam"),
        r([(35, 8, .1), (35, 20, .75), (35, 43, .08)], 2.2, "printing-screw"),
        r([(20, 45, .1), (35, 42, .9), (51, 45, .08)], 2.6, "printing-platen"),
        r([(16, 59, .1), (35, 56, .9), (56, 59, .08)], .8, "printing-paper", "#bcb9af", dry=True),
    ],
    "recipe": [
        r([(16, 57, .1), (16, 37, .75), (19, 16, .08)], 1.8, "recipe-left"),
        r([(19, 16, .1), (35, 14, .85), (52, 18, .08)], 2.0, "recipe-top"),
        r([(52, 18, .1), (50, 37, .75), (51, 55, .08)], 1.0, "recipe-right", "#77746a", dry=True),
        r([(16, 57, .1), (33, 55, .85), (51, 55, .08)], .85, "recipe-base", "#bcb9af", dry=True),
        r([(23, 29, .1), (34, 26, .8), (45, 29, .08)], .9, "recipe-line-a", "#77746a", dry=True),
        r([(23, 38, .1), (31, 35, .75), (39, 38, .08)], .75, "recipe-line-b", "#bcb9af", dry=True),
        m("M 40 43 C 45 36 52 36 56 39 C 51 45 46 48 40 43 Z", "#262522"),
    ],
    "repair": [
        r([(11, 39, .1), (16, 51, .8), (29, 58, .9), (45, 55, .8), (53, 40, .08)], 3.0, "repair-bowl"),
        r([(10, 38, .1), (31, 35, .95), (55, 39, .08)], 2.1, "repair-rim"),
        r([(33, 36, .1), (29, 43, .75), (36, 47, .9), (31, 56, .08)], 1.35, "repair-seam"),
        r([(28, 44, .1), (22, 42, .7), (18, 45, .08)], .72, "repair-branch", "#77746a", dry=True),
        dab(38, 48, 1.3, 1.3, "#bcb9af"),
    ],
    "sculpture": [
        m("M 20 58 C 22 49 27 43 31 39 C 25 33 27 20 37 16 C 48 18 50 29 45 37 C 51 41 55 49 55 58 Z", "#4a4943"),
        r([(32, 27, .1), (37, 24, .75), (43, 27, .08)], .75, "sculpture-brow", "#bcb9af", dry=True),
        r([(37, 28, .1), (35, 34, .7), (39, 35, .08)], .75, "sculpture-nose", "#77746a", dry=True),
        r([(28, 58, .1), (38, 55, .8), (50, 58, .08)], 1.5, "sculpture-base"),
    ],
    "sewing": [
        r([(11, 56, .1), (24, 45, .75), (38, 31, .95), (55, 14, .08)], 1.45, "sewing-needle"),
        dab(53, 16, 2.4, 1.6, "#77746a"),
        r([(13, 55, .1), (18, 63, .7), (29, 60, .9), (34, 50, .8), (29, 43, .8), (19, 46, .08)], .9, "sewing-thread", "#77746a", dry=True),
        r([(37, 50, .1), (49, 55, .75), (61, 50, .08)], 2.0, "sewing-cloth"),
        r([(42, 54, .1), (50, 51, .7), (57, 53, .08)], .7, "sewing-stitch", "#bcb9af", dry=True),
    ],
    "smithing": [
        m("M 8 46 C 17 41 29 41 38 44 L 55 39 L 61 45 L 45 51 L 40 59 L 23 59 L 27 51 L 10 51 Z", "#4a4943"),
        r([(19, 14, .1), (29, 24, .75), (40, 37, .08)], 2.8, "smithing-hammer-handle"),
        m("M 10 10 L 21 7 L 30 16 L 21 23 Z", "#262522"),
        r([(42, 35, .1), (49, 28, .7), (55, 24, .08)], .8, "smithing-spark-a", "#77746a", dry=True),
        r([(39, 34, .1), (40, 25, .7), (42, 19, .08)], .7, "smithing-spark-b", "#bcb9af", dry=True),
    ],
    "spinning": [
        r([(36, 12, .1), (35, 29, .75), (37, 49, .08)], 2.2, "spinning-spindle"),
        m("M 29 49 C 31 43 41 42 45 48 C 43 56 32 58 29 49 Z", "#4a4943"),
        r([(35, 16, .1), (24, 18, .75), (17, 27, .9), (20, 38, .8), (31, 40, .08)], 1.1, "spinning-fiber", "#77746a", dry=True),
        r([(37, 50, .1), (46, 56, .75), (57, 57, .08)], .75, "spinning-thread", "#bcb9af", dry=True),
        dab(37, 10, 2.0, 2.0),
    ],
    "stove": [
        r([(16, 26, .1), (17, 43, .75), (17, 60, .08)], 2.4, "stove-left"),
        r([(53, 24, .1), (54, 42, .75), (55, 59, .08)], 1.45, "stove-right", "#77746a", dry=True),
        r([(17, 60, .1), (35, 57, .85), (55, 59, .08)], 1.4, "stove-base", "#77746a"),
        r([(14, 24, .1), (34, 21, .95), (56, 24, .08)], 2.7, "stove-top"),
        m("M 26 40 C 27 34 33 31 38 34 C 43 37 43 45 39 49 C 32 51 26 47 26 40 Z", "#262522"),
        r([(31, 43, .1), (35, 37, .8), (39, 42, .08)], .8, "stove-flame", "#bcb9af", dry=True),
        r([(21, 62, .1), (21, 66, .7), (20, 68, .08)], 1.0, "stove-foot-a"),
        r([(49, 60, .1), (50, 64, .7), (51, 67, .08)], .75, "stove-foot-b", "#77746a", dry=True),
    ],
    "weaving": [
        r([(14, 12, .1), (14, 35, .75), (15, 61, .08)], 2.2, "weaving-post-left"),
        r([(57, 10, .1), (56, 34, .75), (57, 59, .08)], 1.45, "weaving-post-right", "#77746a", dry=True),
        r([(12, 17, .1), (34, 14, .95), (59, 17, .08)], 2.5, "weaving-beam"),
        r([(19, 19, .1), (20, 38, .75), (20, 56, .08)], .72, "weaving-warp-a", "#bcb9af", dry=True),
        r([(31, 17, .1), (31, 37, .75), (32, 57, .08)], .8, "weaving-warp-b", "#77746a", dry=True),
        r([(44, 17, .1), (43, 37, .75), (44, 56, .08)], .7, "weaving-warp-c", "#bcb9af", dry=True),
        r([(17, 35, .1), (34, 31, .9), (55, 35, .08)], 2.0, "weaving-weft"),
        r([(23, 48, .1), (36, 44, .8), (49, 48, .08)], 1.1, "weaving-shuttle", "#4a4943"),
    ],
    "writing": [
        r([(15, 59, .1), (15, 39, .75), (18, 17, .08)], 1.2, "writing-paper-left", "#77746a", dry=True),
        r([(18, 17, .1), (34, 14, .85), (52, 18, .08)], 1.6, "writing-paper-top"),
        r([(15, 59, .1), (33, 56, .85), (52, 57, .08)], .8, "writing-paper-base", "#bcb9af", dry=True),
        r([(62, 9, .1), (52, 21, .75), (42, 34, .95), (32, 48, .08)], 2.2, "writing-brush"),
        m("M 25 56 C 26 49 31 45 38 43 C 36 50 32 56 25 56 Z", "#262522"),
        r([(21, 31, .1), (28, 28, .75), (36, 31, .08)], .8, "writing-mark-a", "#77746a", dry=True),
        r([(20, 39, .1), (27, 37, .75), (33, 39, .08)], .65, "writing-mark-b", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} craft/workshop object glyphs as naturalist sumi-e studies")
