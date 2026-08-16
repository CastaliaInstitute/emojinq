#!/usr/bin/env python3
"""Redraw social, emotional, ethical, and humanities glyphs as naturalist sumi-e."""

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


def ring(name: str, cx=36, cy=35, rx=20, ry=22, color="#77746a", width=1.6) -> str:
    return r([
        (cx-rx, cy+5, .1), (cx-rx, cy-8, .75), (cx-rx/2, cy-ry+2, .9),
        (cx+3, cy-ry, .85), (cx+rx-2, cy-8, .9), (cx+rx, cy+6, .8),
        (cx+rx/2, cy+ry-1, .9), (cx-3, cy+ry, .85), (cx-rx+2, cy+8, .08)
    ], width, name, color, dry=color != "#262522")


def face(name: str, mood: str, cx=36, cy=34) -> list[str]:
    marks = [ring(f"{name}-face", cx, cy, 19, 21, "#77746a", 1.5)]
    if mood == "surprise":
        marks += [dab(cx-7, cy-4, 2.0, 2.2), dab(cx+7, cy-4, 2.0, 2.2, "#4a4943"), ring(f"{name}-mouth", cx, cy+10, 4, 5, "#262522", 1.2)]
    else:
        marks += [dab(cx-7, cy-5, 2.0, 2.0), dab(cx+7, cy-5, 1.8, 1.8, "#77746a")]
        if mood == "up":
            marks.append(r([(cx-10, cy+7, .1), (cx, cy+14, .8), (cx+10, cy+7, .08)], 1.3, f"{name}-mouth"))
        elif mood == "down":
            marks.append(r([(cx-10, cy+14, .1), (cx, cy+7, .8), (cx+10, cy+14, .08)], 1.1, f"{name}-mouth", "#77746a", dry=True))
        elif mood == "flat":
            marks.append(r([(cx-9, cy+10, .1), (cx, cy+8, .8), (cx+9, cy+10, .08)], .9, f"{name}-mouth", "#bcb9af", dry=True))
    return marks


def person(name: str, x=36, y=17, color="#4a4943") -> list[str]:
    return [
        dab(x, y, 4.2, 4.4, color),
        r([(x, y+6, .1), (x-1, y+21, .8), (x, y+38, .08)], 2.4, f"{name}-body", color),
        r([(x-1, y+17, .1), (x-10, y+24, .75), (x-16, y+29, .08)], .9, f"{name}-arm-a", "#77746a", dry=True),
        r([(x+1, y+17, .1), (x+10, y+23, .75), (x+17, y+27, .08)], .65, f"{name}-arm-b", "#bcb9af", dry=True),
    ]


def leaf(name: str, x: float, y: float, flip=False, color="#4a4943") -> list[str]:
    s = -1 if flip else 1
    return [
        m(f"M {x} {y} C {x+7*s} {y-8} {x+17*s} {y-7} {x+21*s} {y-2} C {x+15*s} {y+5} {x+6*s} {y+6} {x} {y} Z", color),
        r([(x+2*s, y, .1), (x+10*s, y-2, .75), (x+18*s, y-3, .08)], .6, f"{name}-vein", "#bcb9af", dry=True),
    ]


def heart(name: str, x=36, y=34, color="#77746a", scale=1.0) -> str:
    return m(
        f"M {x} {y+20*scale} C {x-9*scale} {y+12*scale} {x-19*scale} {y+4*scale} {x-18*scale} {y-6*scale} "
        f"C {x-17*scale} {y-14*scale} {x-7*scale} {y-16*scale} {x} {y-8*scale} "
        f"C {x+6*scale} {y-17*scale} {x+17*scale} {y-14*scale} {x+19*scale} {y-5*scale} "
        f"C {x+21*scale} {y+5*scale} {x+10*scale} {y+13*scale} {x} {y+20*scale} Z", color)


def balance(name: str, left="#4a4943", right="#77746a") -> list[str]:
    return [
        r([(36, 9, .1), (35, 34, .8), (36, 62, .08)], 2.1, f"{name}-stem"),
        r([(9, 28, .1), (35, 24, .9), (63, 28, .08)], 1.8, f"{name}-beam"),
        r([(17, 29, .1), (14, 42, .75), (10, 49, .08)], .75, f"{name}-cord-a", "#77746a", dry=True),
        r([(56, 29, .1), (59, 41, .75), (63, 48, .08)], .65, f"{name}-cord-b", "#bcb9af", dry=True),
        m("M 5 50 C 10 45 19 45 24 50 C 20 56 10 58 5 50 Z", left),
        m("M 50 49 C 55 44 64 44 68 49 C 64 55 55 57 50 49 Z", right), ground(name, 65),
    ]


def bowl(name: str, fill_count: int) -> list[str]:
    marks = [
        r([(12, 38, .1), (35, 34, .9), (60, 38, .08)], 2.0, f"{name}-rim"),
        r([(14, 39, .1), (19, 54, .8), (36, 60, .9), (53, 55, .8), (58, 39, .08)], 1.5, f"{name}-bowl", "#77746a", dry=True),
    ]
    positions = [(24, 45), (36, 43), (48, 46), (30, 52), (43, 52)]
    colors = ["#262522", "#4a4943", "#77746a", "#262522", "#bcb9af"]
    marks += [dab(*positions[i], 2.6, 2.6, colors[i]) for i in range(fill_count)]
    marks.append(ground(name, 65))
    return marks


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e social study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "anger": [
        *face("anger", "flat"),
        r([(21, 24, .1), (28, 28, .75), (33, 29, .08)], 1.2, "anger-brow-a"),
        r([(51, 24, .1), (44, 28, .75), (39, 29, .08)], .8, "anger-brow-b", "#77746a", dry=True),
        r([(16, 9, .1), (11, 4, .75), (8, 3, .08)], .65, "anger-spark", "#bcb9af", dry=True), ground("anger", 64),
    ],
    "awe": [
        *face("awe", "surprise", 32, 37),
        dab(58, 12, 3.0, 3.0),
        r([(58, 7, .1), (58, 3, .75), (59, 2, .08)], .65, "awe-ray-a", "#bcb9af", dry=True),
        r([(53, 13, .1), (48, 10, .75), (45, 8, .08)], .65, "awe-ray-b", "#77746a", dry=True),
        r([(63, 13, .1), (67, 10, .75), (69, 9, .08)], .65, "awe-ray-c", "#bcb9af", dry=True), ground("awe", 65),
    ],
    "beauty": [
        r([(36, 61, .1), (35, 45, .8), (37, 29, .08)], 2.0, "beauty-stem"),
        *leaf("beauty-a", 36, 37, True, "#4a4943"), *leaf("beauty-b", 38, 30, False, "#77746a"),
        dab(37, 20, 4.0, 4.0, "#bcb9af"), ground("beauty", 64),
    ],
    "belief": [
        *person("belief", 25, 18),
        r([(25, 37, .1), (39, 28, .8), (55, 18, .08)], 1.5, "belief-gaze"),
        dab(58, 16, 3.8, 3.8), ground("belief", 64),
    ],
    "border": [
        r([(36, 7, .1), (34, 31, .8), (36, 65, .08)], 2.4, "border-line"),
        r([(7, 28, .1), (20, 24, .8), (31, 27, .08)], 1.0, "border-left", "#77746a", dry=True),
        r([(41, 45, .1), (53, 41, .8), (65, 44, .08)], .65, "border-right", "#bcb9af", dry=True), ground("border", 67),
    ],
    "calm": [
        *face("calm", "flat"),
        r([(9, 61, .1), (23, 56, .8), (37, 60, .9), (53, 55, .08)], .8, "calm-water", "#bcb9af", dry=True),
    ],
    "capital": [
        r([(12, 59, .1), (12, 36, .8), (35, 17, .9), (60, 36, .8), (59, 59, .08)], 2.0, "capital-house"),
        r([(23, 58, .1), (23, 39, .75), (24, 27, .08)], 1.1, "capital-column-a"),
        r([(36, 58, .1), (35, 37, .75), (36, 25, .08)], 1.5, "capital-column-b", "#77746a", dry=True),
        r([(49, 58, .1), (49, 39, .75), (50, 28, .08)], .65, "capital-column-c", "#bcb9af", dry=True), ground("capital", 64),
    ],
    "chaos": [
        r([(6, 51, .1), (19, 24, .8), (34, 53, .9), (48, 18, .8), (66, 47, .08)], 2.4, "chaos-a"),
        r([(9, 19, .1), (25, 47, .8), (40, 15, .9), (59, 57, .08)], 1.3, "chaos-b", "#77746a", dry=True),
        r([(12, 61, .1), (29, 56, .8), (52, 61, .08)], .65, "chaos-ground", "#bcb9af", dry=True), dab(64, 13, 2.0, 2.0),
    ],
    "community": [
        *person("community-a", 22, 22, "#77746a"), *person("community-b", 37, 15, "#4a4943"), *person("community-c", 52, 23, "#77746a"),
        ground("community", 64),
    ],
    "contradiction": [
        r([(8, 20, .1), (24, 35, .8), (42, 51, .08)], 2.4, "contradiction-a"),
        r([(63, 18, .1), (47, 34, .8), (29, 53, .08)], 1.3, "contradiction-b", "#77746a", dry=True),
        dab(36, 36, 3.0, 3.0, "#bcb9af"), ground("contradiction"),
    ],
    "courage": [
        *person("courage", 19, 22),
        r([(31, 58, .1), (43, 42, .75), (54, 24, .9), (66, 58, .08)], 2.1, "courage-mountain"),
        r([(8, 64, .1), (28, 60, .8), (61, 63, .08)], .65, "courage-ground", "#bcb9af", dry=True),
    ],
    "culture": [
        r([(10, 58, .1), (10, 37, .8), (36, 17, .9), (62, 37, .8), (61, 58, .08)], 2.0, "culture-roof"),
        r([(20, 58, .1), (20, 42, .75), (21, 32, .08)], 1.0, "culture-post-a", "#77746a", dry=True),
        r([(51, 58, .1), (51, 42, .75), (52, 32, .08)], .65, "culture-post-b", "#bcb9af", dry=True),
        r([(25, 47, .1), (35, 42, .8), (46, 47, .08)], 1.3, "culture-shared"), ground("culture", 64),
    ],
    "demand": [
        *bowl("demand", 1),
        r([(36, 31, .1), (35, 20, .75), (36, 11, .08)], 1.6, "demand-up"),
        m("M 29 17 L 36 6 L 44 17 Z", "#4a4943"),
    ],
    "destiny": [
        r([(8, 57, .1), (19, 47, .8), (31, 51, .9), (42, 37, .9), (56, 25, .08)], 2.0, "destiny-path"),
        dab(59, 21, 4.0, 4.0),
        r([(56, 14, .1), (59, 8, .75), (60, 5, .08)], .65, "destiny-ray", "#bcb9af", dry=True), ground("destiny", 64),
    ],
    "discipline": [
        r([(12, 20, .1), (31, 16, .85), (56, 20, .08)], 2.5, "discipline-a"),
        r([(13, 37, .1), (32, 33, .85), (57, 37, .08)], 1.4, "discipline-b", "#77746a", dry=True),
        r([(14, 54, .1), (33, 50, .85), (58, 54, .08)], .75, "discipline-c", "#bcb9af", dry=True), ground("discipline", 64),
    ],
    "diversity": [
        dab(13, 27, 5.0, 4.7), dab(33, 18, 4.2, 5.2, "#77746a"), dab(56, 28, 5.3, 4.2, "#4a4943"),
        r([(13, 34, .1), (13, 48, .75), (14, 58, .08)], 1.4, "diversity-a"),
        r([(33, 25, .1), (34, 42, .75), (35, 58, .08)], .9, "diversity-b", "#77746a", dry=True),
        r([(56, 34, .1), (55, 47, .75), (56, 57, .08)], .65, "diversity-c", "#bcb9af", dry=True), ground("diversity", 64),
    ],
    "doubt": [
        *face("doubt", "flat", 29, 37),
        r([(48, 22, .1), (53, 14, .75), (62, 15, .9), (66, 22, .75), (61, 29, .9), (56, 34, .08)], 1.3, "doubt-hook", "#77746a", dry=True),
        dab(55, 43, 2.2, 2.2, "#bcb9af"), ground("doubt", 65),
    ],
    "duty": [
        r([(36, 8, .1), (35, 34, .8), (36, 63, .08)], 2.8, "duty-pillar"),
        r([(17, 18, .1), (35, 14, .85), (56, 18, .08)], 1.4, "duty-cap"),
        r([(18, 61, .1), (35, 57, .85), (55, 61, .08)], .8, "duty-base", "#77746a", dry=True),
        dab(56, 43, 2.2, 2.2, "#bcb9af"), ground("duty", 65),
    ],
    "empire": [
        r([(7, 59, .1), (7, 37, .8), (22, 20, .9), (36, 36, .08)], 2.0, "empire-left"),
        r([(36, 36, .1), (50, 20, .8), (65, 37, .9), (64, 59, .08)], 1.4, "empire-right", "#77746a", dry=True),
        r([(16, 58, .1), (16, 40, .75), (17, 29, .08)], 1.0, "empire-column-a"),
        r([(36, 58, .1), (35, 39, .75), (36, 28, .08)], .8, "empire-column-b", "#77746a", dry=True),
        r([(55, 58, .1), (55, 40, .75), (56, 29, .08)], .65, "empire-column-c", "#bcb9af", dry=True),
        m("M 28 16 L 36 7 L 44 16 L 41 21 L 31 21 Z", "#4a4943"), ground("empire", 64),
    ],
    "evaporation": [
        r([(10, 58, .1), (26, 54, .8), (43, 58, .9), (61, 53, .08)], 1.5, "evaporation-water"),
        r([(22, 48, .1), (18, 39, .75), (23, 30, .9), (20, 20, .08)], 1.2, "evaporation-a"),
        r([(39, 48, .1), (44, 39, .75), (39, 30, .9), (43, 18, .08)], .8, "evaporation-b", "#77746a", dry=True),
        r([(55, 47, .1), (51, 39, .75), (56, 31, .08)], .65, "evaporation-c", "#bcb9af", dry=True), ground("evaporation", 64),
    ],
    "fairness": [*balance("fairness", "#77746a", "#77746a")],
    "fear": [
        *face("fear", "surprise"),
        r([(14, 14, .1), (9, 8, .75), (7, 5, .08)], .65, "fear-shiver-a", "#bcb9af", dry=True),
        r([(58, 15, .1), (64, 9, .75), (67, 7, .08)], .65, "fear-shiver-b", "#77746a", dry=True), ground("fear", 65),
    ],
    "frontier": [
        r([(7, 58, .1), (22, 42, .75), (37, 54, .9), (52, 31, .75), (66, 57, .08)], 2.2, "frontier-mountains"),
        r([(52, 31, .1), (58, 22, .75), (64, 15, .08)], 1.2, "frontier-flagpole"),
        m("M 61 11 L 69 14 L 64 21 Z", "#4a4943"), ground("frontier", 64),
    ],
    "generosity": [
        heart("generosity-heart", 36, 27, "#77746a", .72),
        r([(7, 59, .1), (20, 51, .8), (34, 56, .9), (48, 47, .08)], 1.5, "generosity-hand"),
        r([(37, 54, .1), (49, 55, .75), (62, 50, .08)], .65, "generosity-give", "#bcb9af", dry=True), ground("generosity", 65),
    ],
    "gift": [
        m("M 14 32 L 59 32 L 58 40 L 15 40 Z", "#77746a"),
        r([(17, 34, .1), (35, 30, .85), (57, 34, .08)], 1.8, "gift-top"),
        r([(17, 34, .1), (18, 48, .75), (19, 57, .08)], 1.2, "gift-left", "#77746a", dry=True),
        r([(57, 34, .1), (56, 47, .75), (54, 57, .08)], .75, "gift-right", "#bcb9af", dry=True),
        r([(19, 57, .1), (35, 54, .85), (54, 57, .08)], 1.1, "gift-bottom"),
        r([(36, 31, .1), (35, 45, .75), (36, 59, .08)], 1.4, "gift-tie-v"),
        r([(17, 40, .1), (35, 36, .85), (57, 40, .08)], 1.2, "gift-tie-h", "#bcb9af", dry=True),
        m("M 36 31 C 31 30 26 26 27 22 C 31 20 35 25 36 29 Z", "#262522"),
        m("M 36 31 C 41 29 46 21 50 24 C 51 28 43 31 36 31 Z", "#77746a"),
        r([(14, 61, .1), (35, 59, .85), (59, 61, .08)], .55, "gift-ground", "#bcb9af", dry=True),
    ],
    "guide": [
        *person("guide", 20, 23),
        r([(31, 43, .1), (43, 34, .8), (57, 24, .08)], 1.8, "guide-path"),
        m("M 53 18 L 66 21 L 59 31 Z", "#4a4943"), ground("guide", 64),
    ],
    "harm": [
        heart("harm-heart", 30, 31, "#77746a", .75),
        r([(15, 15, .1), (34, 34, .8), (57, 58, .08)], 2.0, "harm-slash-a"),
        r([(57, 14, .1), (37, 34, .8), (18, 58, .08)], .9, "harm-slash-b", "#bcb9af", dry=True), ground("harm", 64),
    ],
    "harmony": [
        r([(7, 28, .1), (20, 21, .8), (34, 27, .9), (48, 20, .8), (65, 25, .08)], 1.8, "harmony-a"),
        r([(7, 44, .1), (20, 37, .8), (34, 43, .9), (48, 36, .8), (65, 41, .08)], 1.0, "harmony-b", "#77746a", dry=True),
        r([(14, 57, .1), (31, 53, .8), (56, 56, .08)], .65, "harmony-ground", "#bcb9af", dry=True),
    ],
    "hero": [
        *person("hero", 35, 17),
        m("M 21 32 C 27 24 35 24 40 30 C 34 38 27 40 21 35 Z", "#4a4943"),
        r([(35, 55, .1), (25, 63, .75), (18, 66, .08)], 1.0, "hero-leg-a"),
        r([(36, 55, .1), (47, 62, .75), (55, 65, .08)], .65, "hero-leg-b", "#bcb9af", dry=True),
        r([(52, 13, .1), (58, 8, .75), (63, 10, .08)], .65, "hero-star", "#bcb9af", dry=True),
    ],
    "holiday": [
        r([(36, 7, .1), (35, 25, .8), (36, 37, .08)], 1.8, "holiday-spark-n"),
        r([(7, 35, .1), (22, 32, .8), (36, 36, .08)], 1.4, "holiday-spark-w"),
        r([(36, 36, .1), (51, 32, .8), (66, 35, .08)], .8, "holiday-spark-e", "#77746a", dry=True),
        r([(16, 15, .1), (26, 25, .8), (36, 36, .08)], .65, "holiday-spark-nw", "#bcb9af", dry=True),
        dab(36, 36, 4.0, 4.0),
        r([(12, 59, .1), (29, 55, .8), (56, 58, .08)], 1.0, "holiday-feast", "#77746a", dry=True), ground("holiday", 65),
    ],
    "honesty": [
        r([(9, 36, .1), (22, 25, .8), (36, 22, .9), (51, 26, .8), (64, 36, .08)], 1.8, "honesty-eye-a"),
        r([(9, 36, .1), (23, 46, .8), (36, 49, .9), (52, 45, .8), (64, 36, .08)], .9, "honesty-eye-b", "#77746a", dry=True),
        dab(36, 36, 4.5, 4.5), ground("honesty"),
    ],
    "hope": [
        r([(35, 61, .1), (35, 47, .75), (37, 34, .08)], 2.1, "hope-stem"),
        *leaf("hope", 36, 41, True, "#4a4943"),
        r([(8, 52, .1), (24, 47, .8), (39, 51, .9), (57, 45, .08)], .8, "hope-horizon", "#bcb9af", dry=True),
        dab(59, 21, 3.4, 3.4, "#77746a"), ground("hope", 64),
    ],
    "journey": [
        r([(7, 57, .1), (18, 47, .8), (30, 51, .9), (42, 38, .9), (57, 28, .08)], 2.1, "journey-path"),
        m("M 53 22 L 66 25 L 59 35 Z", "#4a4943"),
        dab(8, 57, 3.0, 3.0, "#77746a"), ground("journey", 64),
    ],
    "joy": [*face("joy", "up"), r([(10, 61, .1), (28, 56, .8), (56, 60, .08)], .65, "joy-ground", "#bcb9af", dry=True)],
    "justice": [*balance("justice", "#4a4943", "#77746a")],
    "lie": [
        r([(9, 36, .1), (22, 25, .8), (36, 22, .9), (51, 26, .8), (64, 36, .08)], 1.5, "lie-eye-a", "#77746a", dry=True),
        r([(9, 36, .1), (23, 46, .8), (36, 49, .9), (52, 45, .8), (64, 36, .08)], .8, "lie-eye-b", "#bcb9af", dry=True),
        r([(15, 16, .1), (35, 35, .8), (58, 58, .08)], 2.4, "lie-slash"), ground("lie", 64),
    ],
    "love": [heart("love", 36, 32, "#77746a", .85), r([(10, 62, .1), (28, 57, .8), (56, 61, .08)], .65, "love-ground", "#bcb9af", dry=True)],
    "mentor": [
        *person("mentor-a", 23, 18), *person("mentor-b", 50, 27, "#77746a"),
        r([(30, 36, .1), (38, 31, .75), (45, 34, .08)], 1.0, "mentor-link"), ground("mentor", 65),
    ],
    "other": [
        *person("other", 46, 19, "#77746a"),
        ring("other-circle", 46, 37, 18, 25, "#bcb9af", .8),
        dab(13, 48, 2.4, 2.4, "#bcb9af"), ground("other", 65),
    ],
    "path": [
        r([(7, 59, .1), (17, 48, .8), (28, 52, .9), (39, 39, .9), (53, 33, .8), (65, 18, .08)], 2.2, "path-main"),
        r([(10, 64, .1), (28, 60, .8), (55, 63, .08)], .65, "path-ground", "#bcb9af", dry=True),
    ],
    "performance": [
        m("M 12 24 C 21 15 34 15 42 23 C 34 31 21 34 12 27 Z", "#4a4943"),
        m("M 36 42 C 45 34 58 35 64 43 C 57 52 45 54 37 47 Z", "#77746a"),
        r([(28, 52, .1), (35, 58, .75), (43, 53, .08)], .8, "performance-smile", "#bcb9af", dry=True), ground("performance", 64),
    ],
    "poverty": [*bowl("poverty", 0), dab(36, 47, 1.6, 1.6, "#bcb9af")],
    "price": [
        r([(16, 23, .1), (27, 17, .8), (48, 17, .9), (57, 23, .8), (55, 38, .9), (53, 51, .8), (36, 55, .9), (18, 51, .8), (17, 36, .9), (16, 23, .08)], 1.8, "price-tag", "#77746a", dry=True),
        r([(17, 29, .1), (34, 25, .85), (55, 29, .08)], 1.1, "price-string"),
        dab(36, 38, 4.0, 4.0),
        r([(11, 62, .1), (30, 58, .8), (58, 61, .08)], .65, "price-ground", "#bcb9af", dry=True),
    ],
    "pride": [
        *person("pride", 35, 17),
        r([(19, 35, .1), (27, 29, .75), (35, 32, .08)], 1.4, "pride-arm-a"),
        r([(36, 32, .1), (46, 27, .75), (55, 34, .08)], .8, "pride-arm-b", "#77746a", dry=True),
        m("M 25 11 L 35 4 L 45 11 L 41 16 L 29 16 Z", "#4a4943"), ground("pride", 65),
    ],
    "promise": [
        r([(8, 50, .1), (20, 41, .8), (33, 47, .08)], 1.8, "promise-hand-a"),
        r([(64, 49, .1), (52, 40, .8), (39, 47, .08)], 1.1, "promise-hand-b", "#77746a", dry=True),
        r([(32, 45, .1), (36, 39, .75), (40, 45, .08)], 2.0, "promise-knot"),
        heart("promise-heart", 36, 22, "#bcb9af", .42), ground("promise", 64),
    ],
    "protection": [
        r([(36, 8, .1), (47, 15, .8), (59, 19, .9), (57, 38, .85), (49, 52, .9), (36, 63, .9), (23, 53, .85), (15, 39, .9), (13, 19, .8), (25, 15, .75), (36, 8, .08)], 2.2, "protection-shield", "#77746a", dry=True),
        *person("protection-person", 36, 23),
    ],
    "relic": [
        m("M 24 16 C 31 10 43 12 48 19 C 52 30 46 44 38 53 C 29 47 20 35 21 24 C 21 21 22 18 24 16 Z", "#77746a"),
        r([(29, 25, .1), (35, 21, .75), (42, 24, .08)], .7, "relic-mark", "#bcb9af", dry=True),
        r([(12, 61, .1), (30, 57, .8), (58, 60, .08)], 1.0, "relic-ground", "#4a4943"),
    ],
    "respect": [
        *person("respect-a", 24, 20), *person("respect-b", 50, 20, "#77746a"),
        r([(23, 37, .1), (32, 43, .75), (40, 44, .08)], 1.1, "respect-bow-a"),
        r([(50, 37, .1), (43, 43, .75), (36, 45, .08)], .65, "respect-bow-b", "#bcb9af", dry=True), ground("respect", 65),
    ],
    "responsibility": [
        *person("responsibility", 35, 22),
        m("M 18 19 C 26 12 45 12 54 19 C 47 27 27 28 18 22 Z", "#77746a"),
        r([(21, 21, .1), (28, 26, .75), (34, 30, .08)], .8, "responsibility-load-a", "#bcb9af", dry=True), ground("responsibility", 65),
    ],
    "risk": [
        r([(8, 58, .1), (20, 43, .75), (33, 27, .9), (46, 43, .75), (59, 58, .08)], 2.2, "risk-mountain"),
        r([(34, 26, .1), (43, 18, .75), (54, 16, .08)], .8, "risk-edge", "#bcb9af", dry=True),
        dab(57, 14, 3.0, 3.0), ground("risk", 64),
    ],
    "ritual": [
        m("M 36 12 C 29 22 30 31 36 35 C 44 31 45 22 36 12 Z", "#4a4943"),
        r([(36, 35, .1), (35, 45, .75), (36, 56, .08)], 1.5, "ritual-candle"),
        r([(17, 57, .1), (27, 52, .8), (36, 56, .9), (46, 51, .8), (58, 56, .08)], 1.2, "ritual-bowl", "#77746a", dry=True), ground("ritual", 64),
    ],
    "rule": [
        r([(11, 16, .1), (31, 12, .85), (57, 16, .08)], 2.3, "rule-a"),
        r([(12, 36, .1), (32, 32, .85), (58, 36, .08)], 1.4, "rule-b", "#77746a", dry=True),
        r([(13, 56, .1), (33, 52, .85), (59, 56, .08)], .75, "rule-c", "#bcb9af", dry=True),
        r([(10, 63, .1), (29, 59, .8), (58, 62, .08)], .65, "rule-ground", "#bcb9af", dry=True),
    ],
    "sadness": [
        *face("sadness", "down"),
        m("M 56 39 C 51 46 52 54 58 57 C 64 53 64 46 56 39 Z", "#bcb9af"), ground("sadness", 65),
    ],
    "scarcity": [*bowl("scarcity", 1), r([(55, 25, .1), (61, 18, .75), (66, 16, .08)], .65, "scarcity-dry", "#bcb9af", dry=True)],
    "self": [
        *person("self", 36, 17), ring("self-circle", 36, 37, 22, 28, "#77746a", 1.2), ground("self", 66),
    ],
    "shame": [
        *face("shame", "down"),
        r([(16, 18, .1), (25, 24, .75), (35, 25, .08)], 1.4, "shame-cover-a"),
        r([(56, 18, .1), (47, 24, .75), (37, 25, .08)], .8, "shame-cover-b", "#bcb9af", dry=True), ground("shame", 65),
    ],
    "spirit": [
        r([(36, 62, .1), (30, 51, .75), (35, 41, .9), (29, 30, .75), (36, 18, .9), (43, 30, .75), (38, 41, .9), (44, 51, .75), (36, 62, .08)], 2.0, "spirit-flame"),
        r([(11, 58, .1), (28, 54, .8), (55, 57, .08)], .65, "spirit-ground", "#bcb9af", dry=True), dab(36, 38, 2.5, 2.5, "#77746a"),
    ],
    "stewardship": [
        r([(8, 56, .1), (21, 48, .8), (35, 53, .9), (49, 44, .08)], 1.5, "stewardship-hand"),
        r([(36, 49, .1), (36, 39, .75), (38, 29, .08)], 1.7, "stewardship-stem"),
        *leaf("stewardship", 37, 36, True, "#4a4943"),
        r([(15, 63, .1), (31, 59, .8), (58, 62, .08)], .65, "stewardship-ground", "#bcb9af", dry=True),
    ],
    "supply": [*bowl("supply", 4), r([(60, 31, .1), (60, 21, .75), (61, 12, .08)], .8, "supply-down", "#77746a", dry=True), m("M 54 25 L 61 36 L 68 25 Z", "#77746a")],
    "surplus": [*bowl("surplus", 5), dab(61, 25, 2.6, 2.6), dab(65, 33, 2.0, 2.0, "#bcb9af")],
    "surprise": [*face("surprise", "surprise"), r([(9, 61, .1), (28, 56, .8), (56, 60, .08)], .65, "surprise-ground", "#bcb9af", dry=True)],
    "tradition": [
        *person("tradition-a", 23, 25, "#77746a"), *person("tradition-b", 36, 18), *person("tradition-c", 50, 26, "#bcb9af"),
        r([(19, 54, .1), (35, 49, .8), (54, 54, .08)], 1.0, "tradition-thread", "#77746a", dry=True), ground("tradition", 65),
    ],
    "trust": [
        r([(7, 50, .1), (20, 41, .8), (33, 47, .08)], 1.8, "trust-hand-a"),
        r([(65, 49, .1), (52, 40, .8), (39, 47, .08)], 1.1, "trust-hand-b", "#77746a", dry=True),
        r([(31, 45, .1), (36, 39, .75), (41, 45, .08)], 2.0, "trust-knot"),
        dab(36, 26, 3.0, 3.0, "#bcb9af"), ground("trust", 64),
    ],
    "truth": [
        r([(9, 36, .1), (22, 25, .8), (36, 22, .9), (51, 26, .8), (64, 36, .08)], 1.9, "truth-eye-a"),
        r([(9, 36, .1), (23, 46, .8), (36, 49, .9), (52, 45, .8), (64, 36, .08)], 1.0, "truth-eye-b", "#77746a", dry=True),
        dab(36, 36, 4.8, 4.8),
        r([(36, 17, .1), (36, 10, .75), (37, 5, .08)], .65, "truth-ray", "#bcb9af", dry=True), ground("truth"),
    ],
    "village": [
        r([(5, 58, .1), (5, 43, .75), (16, 32, .9), (27, 43, .75), (27, 58, .08)], 1.7, "village-house-a"),
        r([(24, 58, .1), (24, 36, .75), (39, 21, .9), (54, 36, .75), (54, 58, .08)], 2.1, "village-house-b"),
        r([(48, 58, .1), (48, 45, .75), (58, 36, .9), (67, 45, .75), (67, 58, .08)], .9, "village-house-c", "#77746a", dry=True), ground("village", 64),
    ],
    "wealth": [*bowl("wealth", 5), dab(18, 29, 2.6, 2.6), dab(34, 25, 3.0, 3.0, "#77746a"), dab(51, 28, 2.4, 2.4, "#bcb9af")],
    "wisdom": [
        *person("wisdom", 23, 21, "#77746a"),
        r([(35, 49, .1), (45, 39, .75), (55, 27, .08)], 1.6, "wisdom-staff"),
        *leaf("wisdom", 53, 28, True, "#4a4943"),
        r([(11, 64, .1), (30, 60, .8), (59, 63, .08)], .65, "wisdom-ground", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} science social/humanities glyphs as sumi-e studies")
