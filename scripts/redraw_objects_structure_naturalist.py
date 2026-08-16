#!/usr/bin/env python3
"""Redraw structural, mechanical, and interface objects as sumi-e studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "objects"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def r(values, width, seed, color="#262522", *, dry=False) -> str:
    # Structural vocabulary depends on supports, shafts, rims, and controls;
    # reinforce those defining strokes without closing the active white space.
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


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="objects / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>objects / {name} — naturalist sumi-e structure study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "beam": [
        r([(8, 27, .1), (27, 24, .85), (48, 27, .95), (64, 23, .08)], 4.0, "beam-host"),
        r([(17, 29, .1), (17, 45, .75), (18, 59, .08)], 2.2, "beam-post-a"),
        r([(54, 27, .1), (53, 43, .75), (54, 57, .08)], 1.3, "beam-post-b", "#77746a", dry=True),
        r([(10, 62, .1), (31, 59, .85), (59, 61, .08)], .7, "beam-ground", "#bcb9af", dry=True),
    ],
    "build": [
        m("M 11 52 L 28 48 L 30 59 L 12 62 Z", "#4a4943"),
        m("M 29 42 L 46 39 L 48 53 L 30 56 Z", "#77746a"),
        m("M 45 29 L 59 26 L 60 42 L 47 46 Z", "#4a4943"),
        r([(13, 47, .1), (30, 37, .8), (45, 27, .9), (59, 14, .08)], 2.2, "build-rise"),
        m("M 55 10 L 65 12 L 60 21 Z", "#262522"),
        r([(8, 65, .1), (29, 62, .85), (55, 64, .08)], .7, "build-ground", "#bcb9af", dry=True),
    ],
    "castle": [
        r([(13, 59, .1), (14, 40, .75), (15, 21, .08)], 2.5, "castle-left"),
        r([(55, 58, .1), (54, 39, .75), (56, 18, .08)], 1.5, "castle-right", "#77746a", dry=True),
        r([(15, 26, .1), (22, 20, .75), (28, 25, .8), (36, 16, .85), (44, 24, .8), (55, 21, .08)], 2.2, "castle-crown"),
        r([(14, 59, .1), (34, 56, .9), (55, 58, .08)], 1.2, "castle-base", "#bcb9af", dry=True),
        m("M 28 57 C 28 46 32 40 37 40 C 43 43 44 50 42 58 Z", "#4a4943"),
        r([(21, 37, .1), (28, 34, .75), (35, 37, .08)], .7, "castle-window", "#77746a", dry=True),
    ],
    "circuit": [
        r([(10, 53, .1), (22, 46, .75), (22, 31, .9), (37, 31, .9), (37, 18, .08)], 2.1, "circuit-host"),
        r([(37, 31, .1), (51, 39, .8), (62, 32, .08)], 1.2, "circuit-branch", "#77746a", dry=True),
        r([(22, 46, .1), (36, 53, .8), (51, 49, .08)], .75, "circuit-return", "#bcb9af", dry=True),
        dab(10, 53, 3.5, 3.5), dab(37, 17, 3.0, 3.0, "#77746a"), dab(62, 32, 3.0, 3.0), dab(51, 49, 2.4, 2.4, "#bcb9af"),
    ],
    "computer": [
        r([(11, 16, .1), (33, 13, .9), (59, 17, .08)], 2.6, "computer-top"),
        r([(11, 16, .1), (11, 34, .75), (13, 51, .08)], 2.0, "computer-left"),
        r([(59, 17, .1), (57, 34, .75), (58, 49, .08)], 1.2, "computer-right", "#77746a", dry=True),
        r([(13, 51, .1), (34, 48, .9), (58, 49, .08)], 1.3, "computer-base", "#bcb9af", dry=True),
        r([(35, 50, .1), (35, 58, .75), (34, 63, .08)], 1.7, "computer-neck"),
        r([(23, 64, .1), (35, 61, .8), (49, 64, .08)], 1.4, "computer-foot", "#77746a", dry=True),
        r([(21, 33, .1), (31, 28, .8), (43, 33, .08)], .85, "computer-screen-mark", "#bcb9af", dry=True),
    ],
    "design": [
        r([(13, 58, .1), (13, 37, .75), (16, 16, .08)], 1.4, "design-paper-left", "#77746a", dry=True),
        r([(16, 16, .1), (34, 13, .85), (54, 17, .08)], 1.8, "design-paper-top"),
        r([(13, 58, .1), (33, 55, .85), (52, 56, .08)], .8, "design-paper-base", "#bcb9af", dry=True),
        r([(24, 47, .1), (35, 24, .9), (47, 48, .08)], 1.6, "design-compass-a"),
        r([(28, 37, .1), (35, 43, .75), (44, 36, .08)], 1.0, "design-compass-b", "#77746a", dry=True),
        dab(35, 24, 2.0, 2.0),
    ],
    "doorframe": [
        r([(12, 59, .1), (13, 39, .75), (21, 23, .9), (36, 17, .85), (51, 25, .75), (59, 45, .08)], 3.0, "doorframe-arch"),
        r([(23, 58, .1), (23, 43, .75), (28, 34, .9), (38, 31, .8), (48, 40, .75), (49, 57, .08)], 1.3, "doorframe-inner", "#77746a", dry=True),
        r([(9, 62, .1), (29, 59, .85), (58, 61, .08)], .75, "doorframe-ground", "#bcb9af", dry=True),
    ],
    "electricity": [
        m("M 40 7 L 22 35 L 34 34 L 27 63 L 53 28 L 39 29 Z", "#262522"),
        r([(13, 22, .1), (8, 29, .75), (5, 38, .08)], .9, "electricity-left", "#77746a", dry=True),
        r([(54, 18, .1), (62, 23, .75), (67, 31, .08)], .7, "electricity-right", "#bcb9af", dry=True),
        r([(45, 52, .1), (51, 57, .75), (56, 63, .08)], .65, "electricity-tail", "#77746a", dry=True),
    ],
    "engine": [
        # A small locomotive is the familiar toddler referent for “engine”:
        # boiler, cab, chimney, cowcatcher, and paired wheels.
        r([(13, 49, .1), (13, 33, .75), (22, 26, .9), (43, 30, .8), (45, 49, .08)], 3.0, "engine-boiler"),
        r([(44, 49, .1), (44, 21, .75), (58, 20, .9), (59, 49, .08)], 2.2, "engine-cab", "#77746a"),
        m("M 20 15 L 30 15 L 28 30 L 21 30 Z", "#262522"),
        r([(10, 50, .1), (32, 48, .85), (61, 50, .08)], 2.3, "engine-chassis"),
        r([(58, 49, .1), (64, 54, .75), (68, 59, .08)], 1.7, "engine-cowcatcher"),
        dab(22, 53, 6.0, 6.0, "#262522"),
        dab(49, 53, 6.0, 6.0, "#4a4943"),
        dab(53, 29, 3.5, 4.0, "#262522"),
        r([(13, 62, .1), (34, 59, .85), (61, 62, .08)], 1.2, "engine-rail", "#77746a", dry=True),
    ],
    "foundation": [
        m("M 8 51 L 22 46 L 28 57 L 12 62 Z", "#4a4943"),
        m("M 25 45 L 41 42 L 47 54 L 29 58 Z", "#77746a"),
        m("M 44 48 L 60 44 L 64 56 L 48 60 Z", "#4a4943"),
        r([(7, 64, .1), (29, 61, .85), (62, 63, .08)], .8, "foundation-ground", "#bcb9af", dry=True),
        r([(13, 38, .1), (34, 35, .9), (59, 38, .08)], 2.5, "foundation-sill"),
        r([(18, 35, .1), (18, 22, .75), (20, 14, .08)], 1.3, "foundation-rise", "#77746a", dry=True),
    ],
    "gallery": [
        r([(11, 19, .1), (30, 16, .85), (51, 19, .08)], 2.2, "gallery-rail"),
        r([(19, 20, .1), (18, 31, .75), (18, 43, .08)], .8, "gallery-cord-a", "#77746a", dry=True),
        r([(43, 18, .1), (43, 28, .75), (43, 37, .08)], .7, "gallery-cord-b", "#bcb9af", dry=True),
        r([(10, 43, .1), (19, 40, .8), (29, 44, .9), (27, 58, .75), (10, 56, .08)], 1.3, "gallery-frame-a"),
        r([(35, 37, .1), (44, 34, .8), (55, 38, .9), (54, 51, .75), (36, 49, .08)], 1.0, "gallery-frame-b", "#77746a", dry=True),
        r([(14, 51, .1), (20, 47, .75), (25, 52, .08)], .65, "gallery-mark-a", "#bcb9af", dry=True),
        dab(46, 44, 2.0, 2.0),
    ],
    "lever": [
        r([(8, 49, .1), (27, 43, .85), (46, 34, .95), (64, 24, .08)], 3.0, "lever-bar"),
        m("M 28 57 L 38 38 L 49 57 Z", "#4a4943"),
        dab(61, 22, 3.0, 3.0, "#77746a"),
        r([(8, 62, .1), (30, 59, .85), (55, 61, .08)], .75, "lever-ground", "#bcb9af", dry=True),
    ],
    "motor": [
        r([(14, 50, .1), (13, 35, .75), (19, 22, .9), (32, 17, .85), (45, 23, .75), (51, 37, .9), (47, 51, .75), (33, 57, .9), (20, 54, .75), (14, 50, .08)], 2.5, "motor-coil"),
        r([(22, 46, .1), (20, 34, .75), (27, 26, .9), (38, 25, .75), (45, 34, .9), (42, 44, .75), (33, 49, .08)], 1.0, "motor-inner", "#77746a", dry=True),
        r([(50, 37, .1), (60, 34, .75), (67, 35, .08)], 2.0, "motor-shaft"),
        dab(33, 37, 3.0, 3.0),
        r([(11, 61, .1), (28, 58, .85), (52, 61, .08)], .7, "motor-ground", "#bcb9af", dry=True),
    ],
    "mural": [
        r([(10, 16, .1), (34, 13, .9), (61, 17, .08)], 2.2, "mural-top"),
        r([(10, 16, .1), (11, 36, .75), (13, 57, .08)], 1.7, "mural-left"),
        r([(61, 17, .1), (58, 37, .75), (59, 54, .08)], 1.0, "mural-right", "#77746a", dry=True),
        r([(13, 57, .1), (34, 54, .85), (59, 54, .08)], .8, "mural-base", "#bcb9af", dry=True),
        r([(19, 45, .1), (27, 31, .8), (38, 42, .95), (50, 27, .08)], 2.7, "mural-gesture"),
        dab(48, 43, 2.2, 2.2, "#77746a"),
    ],
    "pattern": [
        dab(16, 21, 3.2, 3.2), dab(36, 17, 2.6, 2.6, "#77746a"), dab(55, 23, 3.0, 3.0),
        r([(11, 39, .1), (22, 33, .8), (32, 39, .9), (43, 32, .8), (57, 39, .08)], 1.7, "pattern-wave"),
        r([(15, 55, .1), (27, 49, .8), (39, 55, .9), (53, 48, .08)], .8, "pattern-dry", "#bcb9af", dry=True),
    ],
    "pulley": [
        r([(12, 10, .1), (35, 8, .85), (60, 11, .08)], 2.5, "pulley-support"),
        r([(18, 39, .1), (17, 28, .75), (24, 18, .9), (36, 15, .85), (48, 21, .75), (53, 33, .9), (49, 44, .75), (38, 50, .9), (25, 47, .75), (18, 39, .08)], 2.4, "pulley-wheel"),
        dab(36, 33, 3.4, 3.4),
        r([(36, 15, .1), (36, 8, .75), (36, 5, .08)], 1.6, "pulley-hook"),
        r([(53, 32, .1), (56, 46, .75), (56, 61, .08)], 1.3, "pulley-rope", "#77746a", dry=True),
        m("M 48 57 L 64 56 L 65 67 L 49 68 Z", "#262522"),
        r([(48, 57, .1), (56, 53, .75), (64, 56, .08)], 1.4, "pulley-load-rope"),
        r([(19, 39, .1), (13, 48, .75), (10, 57, .08)], .7, "pulley-return", "#bcb9af", dry=True),
    ],
    "pump": [
        m("M 17 29 L 31 27 L 32 60 L 17 61 Z", "#4a4943"),
        r([(16, 29, .1), (25, 24, .8), (36, 28, .08)], 2.4, "pump-head"),
        r([(33, 28, .1), (45, 30, .75), (54, 38, .9), (61, 38, .08)], 2.2, "pump-spout"),
        r([(25, 25, .1), (28, 13, .75), (48, 10, .08)], 2.5, "pump-handle"),
        r([(47, 9, .1), (57, 13, .75), (62, 16, .08)], 1.4, "pump-grip", "#4a4943"),
        r([(58, 41, .1), (55, 49, .75), (58, 55, .08)], .8, "pump-water", "#bcb9af", dry=True),
        m("M 11 59 L 38 58 L 41 65 L 9 66 Z", "#77746a"),
    ],
    "robot": [
        r([(20, 18, .1), (34, 15, .85), (49, 19, .08)], 2.4, "robot-head-top"),
        r([(20, 18, .1), (21, 30, .75), (23, 38, .08)], 1.7, "robot-head-left"),
        r([(49, 19, .1), (48, 29, .75), (47, 38, .08)], 1.0, "robot-head-right", "#77746a", dry=True),
        r([(23, 38, .1), (35, 35, .85), (47, 38, .08)], 1.2, "robot-jaw", "#bcb9af", dry=True),
        dab(28, 27, 2.1, 2.1), dab(42, 27, 1.8, 1.8, "#77746a"),
        m("M 24 42 L 46 40 L 49 59 L 22 61 Z", "#4a4943"),
        r([(22, 47, .1), (13, 53, .75), (8, 58, .08)], 1.3, "robot-arm-left"),
        r([(48, 46, .1), (56, 51, .75), (62, 55, .08)], .8, "robot-arm-right", "#bcb9af", dry=True),
    ],
    "sandbox": [
        r([(10, 35, .1), (32, 31, .9), (59, 35, .08)], 2.2, "sandbox-back"),
        r([(10, 35, .1), (16, 53, .75), (20, 59, .08)], 1.7, "sandbox-left"),
        r([(59, 35, .1), (54, 50, .75), (51, 57, .08)], 1.0, "sandbox-right", "#77746a", dry=True),
        r([(20, 59, .1), (35, 55, .85), (51, 57, .08)], 1.2, "sandbox-front", "#bcb9af", dry=True),
        r([(18, 46, .1), (30, 42, .8), (43, 46, .08)], .85, "sandbox-sand", "#77746a", dry=True),
        r([(52, 15, .1), (45, 29, .75), (38, 48, .08)], 1.9, "sandbox-rake"),
        r([(36, 48, .1), (43, 51, .75), (49, 50, .08)], .7, "sandbox-rake-head", "#bcb9af", dry=True),
    ],
    "save": [
        r([(17, 27, .1), (18, 44, .75), (22, 58, .08)], 2.1, "save-jar-left"),
        r([(52, 27, .1), (51, 43, .75), (48, 56, .08)], 1.2, "save-jar-right", "#77746a", dry=True),
        r([(14, 27, .1), (34, 24, .9), (55, 27, .08)], 2.4, "save-rim"),
        r([(22, 58, .1), (35, 55, .85), (48, 56, .08)], 1.1, "save-base", "#bcb9af", dry=True),
        m("M 29 44 C 31 36 39 33 44 36 C 42 43 37 48 29 44 Z", "#4a4943"),
        r([(34, 35, .1), (31, 28, .75), (27, 23, .08)], .7, "save-stem", "#77746a", dry=True),
    ],
    "screw": [
        m("M 25 10 C 28 4 45 4 49 10 L 47 19 L 27 19 Z", "#4a4943"),
        r([(29, 12, .1), (37, 10, .8), (45, 12, .08)], 1.8, "screw-head-slot", "#262522"),
        r([(37, 18, .1), (36, 34, .75), (37, 51, .9), (36, 64, .08)], 3.2, "screw-shaft"),
        r([(27, 27, .1), (36, 23, .75), (46, 28, .08)], 1.5, "screw-thread-a", "#4a4943"),
        r([(27, 37, .1), (36, 33, .75), (46, 38, .08)], 1.5, "screw-thread-b", "#77746a"),
        r([(28, 47, .1), (36, 43, .75), (45, 48, .08)], 1.45, "screw-thread-c", "#4a4943"),
        r([(29, 57, .1), (36, 53, .75), (43, 58, .08)], 1.3, "screw-thread-d", "#77746a", dry=True),
    ],
    "slide": [
        r([(53, 15, .1), (46, 29, .75), (37, 43, .9), (24, 57, .08)], 3.2, "slide-slope"),
        r([(51, 15, .1), (58, 14, .75), (63, 20, .08)], 1.8, "slide-platform"),
        r([(53, 18, .1), (53, 37, .75), (53, 56, .08)], 1.7, "slide-ladder-left", "#4a4943"),
        r([(63, 20, .1), (63, 38, .75), (63, 57, .08)], 1.5, "slide-ladder-right", "#77746a"),
        r([(53, 29, .1), (58, 27, .75), (63, 29, .08)], 1.3, "slide-rung-a", "#4a4943"),
        r([(53, 40, .1), (58, 38, .75), (63, 40, .08)], 1.25, "slide-rung-b", "#77746a"),
        r([(53, 51, .1), (58, 49, .75), (63, 51, .08)], 1.2, "slide-rung-c", "#4a4943"),
        r([(10, 62, .1), (28, 59, .85), (55, 61, .08)], .75, "slide-ground", "#bcb9af", dry=True),
    ],
    "stage": [
        r([(9, 49, .1), (31, 46, .9), (61, 49, .08)], 3.0, "stage-platform"),
        r([(12, 55, .1), (34, 52, .9), (58, 55, .08)], 1.2, "stage-front", "#77746a", dry=True),
        r([(16, 48, .1), (16, 60, .75), (17, 65, .08)], 1.4, "stage-leg-a"),
        r([(54, 49, .1), (54, 59, .75), (55, 64, .08)], .8, "stage-leg-b", "#bcb9af", dry=True),
        r([(21, 22, .1), (28, 15, .75), (35, 22, .9), (43, 14, .75), (51, 22, .08)], 1.5, "stage-curtain"),
        r([(21, 22, .1), (22, 34, .75), (20, 45, .08)], .75, "stage-curtain-left", "#77746a", dry=True),
    ],
    "steam": [
        r([(19, 58, .1), (27, 53, .8), (37, 56, .9), (48, 52, .08)], 1.8, "steam-water"),
        r([(24, 48, .1), (19, 39, .75), (25, 30, .9), (21, 20, .08)], 1.5, "steam-a"),
        r([(36, 50, .1), (42, 40, .75), (37, 31, .9), (42, 18, .08)], 1.0, "steam-b", "#77746a", dry=True),
        r([(49, 47, .1), (54, 39, .75), (50, 31, .08)], .7, "steam-c", "#bcb9af", dry=True),
    ],
    "swing": [
        r([(8, 17, .1), (28, 14, .9), (51, 17, .95), (64, 13, .08)], 3.0, "swing-branch"),
        r([(24, 18, .1), (24, 37, .75), (25, 55, .08)], 1.2, "swing-rope-a"),
        r([(49, 17, .1), (47, 36, .75), (47, 54, .08)], .8, "swing-rope-b", "#77746a", dry=True),
        r([(23, 56, .1), (35, 53, .85), (48, 55, .08)], 2.3, "swing-seat"),
        r([(10, 64, .1), (30, 61, .85), (56, 63, .08)], .7, "swing-ground", "#bcb9af", dry=True),
    ],
    "switch": [
        r([(13, 17, .1), (34, 14, .9), (57, 18, .08)], 2.1, "switch-top"),
        r([(13, 17, .1), (13, 37, .75), (15, 57, .08)], 1.7, "switch-left"),
        r([(57, 18, .1), (55, 37, .75), (56, 54, .08)], 1.0, "switch-right", "#77746a", dry=True),
        r([(15, 57, .1), (34, 54, .85), (56, 54, .08)], .8, "switch-base", "#bcb9af", dry=True),
        r([(25, 43, .1), (35, 27, .85), (44, 23, .08)], 3.0, "switch-toggle"),
        dab(24, 44, 3.2, 3.2, "#77746a"),
    ],
    "tower": [
        r([(25, 61, .1), (27, 42, .75), (30, 22, .9), (36, 8, .08)], 3.0, "tower-left"),
        r([(47, 60, .1), (44, 41, .75), (41, 22, .9), (36, 8, .08)], 1.6, "tower-right", "#77746a", dry=True),
        r([(25, 61, .1), (36, 58, .85), (47, 60, .08)], 1.8, "tower-base"),
        r([(29, 43, .1), (36, 40, .75), (44, 43, .08)], .75, "tower-band-a", "#bcb9af", dry=True),
        r([(31, 29, .1), (36, 26, .75), (42, 29, .08)], .7, "tower-band-b", "#77746a", dry=True),
        dab(36, 7, 1.8, 1.8),
    ],
    "valve": [
        r([(15, 37, .1), (14, 25, .75), (22, 16, .9), (35, 13, .85), (48, 20, .75), (54, 32, .9), (50, 44, .75), (37, 50, .9), (24, 47, .75), (15, 37, .08)], 2.2, "valve-wheel"),
        r([(35, 14, .1), (35, 49, .9), (36, 62, .08)], 1.5, "valve-stem"),
        r([(16, 35, .1), (35, 32, .85), (53, 34, .08)], 1.0, "valve-cross", "#77746a", dry=True),
        dab(35, 33, 3.2, 3.2),
        r([(25, 63, .1), (36, 60, .8), (48, 63, .08)], .7, "valve-base", "#bcb9af", dry=True),
    ],
    "windowpane": [
        r([(10, 15, .1), (33, 12, .9), (60, 16, .08)], 2.3, "window-top"),
        r([(10, 15, .1), (11, 36, .75), (13, 59, .08)], 1.8, "window-left"),
        r([(60, 16, .1), (58, 37, .75), (59, 57, .08)], 1.0, "window-right", "#77746a", dry=True),
        r([(13, 59, .1), (34, 56, .85), (59, 57, .08)], .85, "window-base", "#bcb9af", dry=True),
        r([(35, 14, .1), (34, 35, .75), (35, 57, .08)], 1.0, "window-mullion"),
        r([(12, 36, .1), (34, 33, .85), (59, 35, .08)], .75, "window-transom", "#77746a", dry=True),
        r([(20, 49, .1), (27, 39, .75), (31, 28, .08)], .65, "window-branch", "#bcb9af", dry=True),
    ],
    "work": [
        r([(13, 52, .1), (31, 48, .85), (54, 51, .08)], 3.0, "work-bench"),
        r([(18, 52, .1), (17, 61, .75), (16, 66, .08)], 1.5, "work-leg-a"),
        r([(50, 51, .1), (51, 60, .75), (52, 64, .08)], .8, "work-leg-b", "#77746a", dry=True),
        r([(53, 12, .1), (44, 23, .75), (33, 38, .08)], 2.5, "work-hammer"),
        m("M 46 10 L 57 7 L 64 15 L 55 21 Z", "#262522"),
        m("M 20 38 L 34 35 L 38 45 L 23 47 Z", "#77746a"),
        r([(9, 65, .1), (31, 62, .85), (58, 64, .08)], .7, "work-ground", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} structural/mechanical object glyphs as sumi-e studies")
