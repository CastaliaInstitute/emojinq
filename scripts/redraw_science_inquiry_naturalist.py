#!/usr/bin/env python3
"""Redraw inquiry, learning, and scientific-method glyphs as naturalist sumi-e."""

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


def leaf(name: str, x: float, y: float, flip=False, color="#4a4943") -> list[str]:
    s = -1 if flip else 1
    return [
        m(f"M {x} {y} C {x+7*s} {y-8} {x+17*s} {y-7} {x+21*s} {y-2} C {x+15*s} {y+5} {x+6*s} {y+6} {x} {y} Z", color),
        r([(x+2*s, y, .1), (x+10*s, y-2, .75), (x+18*s, y-3, .08)], .6, f"{name}-vein", "#bcb9af", dry=True),
    ]


def eye(name: str, cx=36, cy=34, scale=1.0) -> list[str]:
    return [
        r([(cx-25*scale, cy, .1), (cx-12*scale, cy-10*scale, .8), (cx, cy-12*scale, .9), (cx+13*scale, cy-8*scale, .8), (cx+25*scale, cy, .08)], 1.8*scale, f"{name}-upper"),
        r([(cx-25*scale, cy, .1), (cx-12*scale, cy+9*scale, .8), (cx, cy+11*scale, .9), (cx+13*scale, cy+8*scale, .8), (cx+25*scale, cy, .08)], .9*scale, f"{name}-lower", "#77746a", dry=True),
        dab(cx, cy, 4.2*scale, 4.2*scale, "#4a4943"),
    ]


def book(name: str, y=27) -> list[str]:
    return [
        r([(7, y, .1), (20, y-5, .8), (34, y, .9), (35, y+27, .08)], 1.7, f"{name}-left"),
        r([(35, y, .1), (49, y-5, .8), (64, y, .9), (62, y+27, .08)], 1.1, f"{name}-right", "#77746a", dry=True),
        r([(8, y+27, .1), (21, y+22, .8), (35, y+27, .9), (49, y+22, .8), (62, y+27, .08)], .75, f"{name}-base", "#bcb9af", dry=True),
    ]


def hook(name: str, x=36, y=13) -> list[str]:
    return [
        r([(x-12, y+6, .1), (x-7, y-2, .75), (x+4, y-4, .9), (x+12, y+2, .8), (x+10, y+11, .9), (x+1, y+17, .8), (x, y+25, .08)], 2.0, f"{name}-hook", "#77746a", dry=True),
        dab(x, y+36, 2.6, 2.6, "#bcb9af"),
    ]


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e inquiry study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "curiosity": [
        *eye("curiosity", 31, 34, .85),
        *hook("curiosity-q", 57, 12),
        ground("curiosity"),
    ],
    "discovery": [
        m("M 8 50 C 17 40 30 38 39 45 C 34 54 21 58 9 54 Z", "#77746a"),
        r([(38, 45, .1), (45, 34, .75), (52, 24, .08)], 1.6, "discovery-lift"),
        dab(56, 18, 4.0, 4.0),
        r([(53, 12, .1), (56, 6, .75), (57, 3, .08)], .65, "discovery-ray", "#bcb9af", dry=True), ground("discovery"),
    ],
    "evidence": [
        *book("evidence", 24),
        dab(50, 47, 6.0, 5.6, "#4a4943"),
        r([(47, 47, .1), (51, 51, .75), (57, 43, .08)], .7, "evidence-check", "#bcb9af", dry=True),
        r([(15, 34, .1), (25, 31, .75), (33, 34, .08)], .7, "evidence-line", "#77746a", dry=True),
    ],
    "example": [
        *leaf("example", 20, 34, False, "#4a4943"),
        r([(20, 35, .1), (19, 49, .75), (20, 60, .08)], 1.4, "example-stem"),
        dab(57, 24, 2.2, 2.2, "#bcb9af"),
        r([(47, 50, .1), (54, 46, .75), (62, 48, .08)], .65, "example-others", "#bcb9af", dry=True), ground("example", 64),
    ],
    "experiment": [
        r([(27, 10, .1), (28, 27, .75), (17, 51, .9), (23, 60, .8), (50, 60, .9), (56, 51, .8), (44, 27, .9), (44, 10, .08)], 2.0, "experiment-flask"),
        r([(28, 28, .1), (36, 31, .8), (44, 28, .08)], 1.2, "experiment-rim"),
        r([(21, 49, .1), (35, 44, .8), (51, 49, .08)], 1.3, "experiment-liquid", "#77746a", dry=True),
        dab(30, 40, 2.4, 2.4, "#4a4943"), dab(43, 36, 1.8, 1.8, "#bcb9af"),
    ],
    "exploration": [
        r([(8, 57, .1), (18, 47, .8), (31, 51, .9), (42, 38, .9), (56, 29, .08)], 2.0, "exploration-path"),
        m("M 52 23 L 65 26 L 58 36 Z", "#4a4943"),
        r([(21, 22, .1), (35, 17, .8), (49, 22, .08)], 1.1, "exploration-compass-a", "#77746a", dry=True),
        r([(35, 8, .1), (35, 18, .75), (36, 28, .08)], .65, "exploration-compass-b", "#bcb9af", dry=True), ground("exploration"),
    ],
    "hypothesis": [
        dab(16, 50, 3.2, 3.2),
        r([(19, 48, .1), (29, 38, .8), (39, 29, .08)], 1.5, "hypothesis-rise", "#77746a", dry=True),
        *leaf("hypothesis", 39, 30, False, "#4a4943"),
        r([(11, 61, .1), (29, 57, .8), (58, 60, .08)], .65, "hypothesis-ground", "#bcb9af", dry=True),
        dab(61, 19, 1.8, 1.8, "#bcb9af"),
    ],
    "idea": [
        m("M 36 9 C 25 9 18 18 20 28 C 21 36 28 39 31 44 L 42 44 C 45 38 52 34 53 25 C 53 16 45 9 36 9 Z", "#77746a"),
        r([(31, 47, .1), (36, 44, .8), (43, 47, .08)], 2.0, "idea-base"),
        r([(30, 54, .1), (36, 52, .8), (43, 54, .08)], .8, "idea-base-dry", "#bcb9af", dry=True),
        r([(35, 15, .1), (37, 23, .75), (36, 33, .08)], .65, "idea-glint", "#bcb9af", dry=True), ground("idea", 63),
    ],
    "if": [
        r([(36, 61, .1), (35, 45, .8), (36, 30, .08)], 2.4, "if-trunk"),
        r([(36, 35, .1), (25, 27, .8), (14, 19, .08)], 1.4, "if-left"),
        r([(36, 35, .1), (48, 27, .8), (60, 19, .08)], .9, "if-right", "#77746a", dry=True),
        dab(13, 18, 3.2, 3.2), dab(61, 18, 2.8, 2.8, "#77746a"), ground("if", 64),
    ],
    "imagination": [
        r([(11, 48, .1), (7, 35, .75), (15, 22, .9), (29, 17, .85), (42, 23, .9), (48, 35, .8), (43, 47, .9), (31, 52, .8), (21, 48, .9), (18, 39, .8), (24, 32, .9), (33, 33, .08)], 1.9, "imagination-spiral"),
        *leaf("imagination", 41, 25, False, "#77746a"),
        dab(61, 15, 2.2, 2.2, "#bcb9af"), ground("imagination"),
    ],
    "inquiry": [
        *eye("inquiry", 31, 34, .8),
        *hook("inquiry-q", 56, 12),
        r([(8, 59, .1), (28, 56, .8), (60, 58, .08)], .65, "inquiry-ground", "#bcb9af", dry=True),
    ],
    "insight": [
        *eye("insight", 34, 38, .82),
        r([(36, 21, .1), (36, 13, .75), (37, 7, .08)], 1.0, "insight-ray-a"),
        r([(49, 26, .1), (56, 20, .75), (61, 17, .08)], .7, "insight-ray-b", "#77746a", dry=True),
        r([(20, 25, .1), (15, 19, .75), (12, 16, .08)], .65, "insight-ray-c", "#bcb9af", dry=True), ground("insight", 63),
    ],
    "knowledge": [
        *book("knowledge", 29),
        r([(35, 42, .1), (35, 30, .75), (37, 19, .08)], 1.5, "knowledge-stem"),
        *leaf("knowledge", 36, 26, True, "#4a4943"),
        dab(55, 17, 2.0, 2.0, "#bcb9af"),
    ],
    "learning": [
        *book("learning", 31),
        r([(35, 37, .1), (44, 27, .75), (54, 18, .08)], 1.5, "learning-rise"),
        m("M 50 13 L 63 16 L 56 25 Z", "#4a4943"),
        r([(18, 43, .1), (27, 40, .75), (34, 43, .08)], .65, "learning-line", "#bcb9af", dry=True),
    ],
    "mastery": [
        r([(7, 59, .1), (21, 43, .75), (34, 25, .9), (47, 43, .75), (61, 59, .08)], 2.5, "mastery-mountain"),
        r([(34, 25, .1), (35, 15, .75), (36, 7, .08)], 1.3, "mastery-pole"),
        m("M 36 8 L 54 12 L 37 20 Z", "#4a4943"),
        r([(13, 64, .1), (32, 60, .8), (59, 63, .08)], .65, "mastery-ground", "#bcb9af", dry=True),
    ],
    "mind": [
        r([(18, 56, .1), (12, 45, .75), (14, 29, .9), (25, 17, .85), (41, 15, .9), (52, 25, .8), (54, 39, .9), (46, 50, .08)], 2.0, "mind-profile"),
        r([(28, 42, .1), (24, 33, .75), (29, 26, .9), (38, 26, .8), (42, 33, .9), (38, 39, .8), (32, 37, .08)], 1.2, "mind-spiral", "#77746a", dry=True),
        dab(33, 33, 2.0, 2.0, "#bcb9af"), ground("mind"),
    ],
    "mistake": [
        r([(8, 47, .1), (20, 36, .8), (31, 42, .08)], 2.2, "mistake-a"),
        r([(39, 37, .1), (50, 27, .8), (63, 32, .08)], 1.4, "mistake-b", "#77746a", dry=True),
        r([(27, 27, .1), (36, 36, .8), (45, 46, .08)], 1.2, "mistake-cross-a"),
        r([(45, 26, .1), (36, 36, .8), (27, 47, .08)], .7, "mistake-cross-b", "#bcb9af", dry=True), ground("mistake"),
    ],
    "model": [
        r([(7, 57, .1), (17, 44, .75), (27, 56, .08)], 1.3, "model-small"),
        r([(34, 58, .1), (47, 34, .8), (63, 57, .08)], 2.4, "model-large"),
        r([(24, 35, .1), (34, 30, .75), (44, 26, .08)], .7, "model-link", "#bcb9af", dry=True),
        dab(47, 28, 2.6, 2.6, "#77746a"), ground("model", 64),
    ],
    "mystery": [
        r([(15, 60, .1), (14, 42, .8), (17, 25, .9), (35, 13, .85), (54, 25, .9), (57, 44, .8), (56, 60, .08)], 2.0, "mystery-door"),
        *hook("mystery-q", 36, 19),
        r([(9, 64, .1), (29, 61, .8), (61, 63, .08)], .65, "mystery-ground", "#bcb9af", dry=True),
    ],
    "paradox": [
        r([(8, 38, .1), (17, 25, .75), (29, 25, .9), (36, 36, .9), (43, 47, .9), (55, 47, .75), (64, 36, .9), (55, 25, .75), (43, 25, .9), (36, 36, .9), (29, 47, .9), (17, 47, .75), (8, 38, .08)], 2.2, "paradox-loop"),
        r([(16, 57, .1), (35, 54, .8), (56, 57, .08)], .65, "paradox-ground", "#bcb9af", dry=True),
    ],
    "pattern": [
        dab(14, 20, 2.8, 2.8), dab(29, 20, 2.5, 2.5, "#77746a"), dab(44, 20, 2.8, 2.8), dab(59, 20, 2.3, 2.3, "#bcb9af"),
        dab(14, 38, 2.3, 2.3, "#77746a"), dab(29, 38, 2.8, 2.8), dab(44, 38, 2.3, 2.3, "#bcb9af"), dab(59, 38, 2.7, 2.7, "#77746a"),
        r([(8, 55, .1), (25, 51, .8), (42, 55, .9), (62, 50, .08)], 1.0, "pattern-thread", "#77746a", dry=True), ground("pattern", 64),
    ],
    "plan": [
        r([(8, 56, .1), (18, 45, .8), (30, 49, .9), (40, 35, .9), (54, 29, .08)], 2.0, "plan-path"),
        dab(9, 56, 3.2, 3.2), dab(31, 48, 2.6, 2.6, "#77746a"), dab(57, 27, 3.0, 3.0, "#4a4943"),
        r([(16, 19, .1), (29, 15, .8), (42, 19, .08)], .8, "plan-map", "#bcb9af", dry=True), ground("plan", 64),
    ],
    "possibility": [
        r([(36, 60, .1), (35, 44, .8), (36, 31, .08)], 2.2, "possibility-trunk"),
        r([(36, 37, .1), (23, 28, .8), (11, 20, .08)], 1.3, "possibility-a"),
        r([(36, 37, .1), (49, 28, .8), (62, 19, .08)], .9, "possibility-b", "#77746a", dry=True),
        r([(36, 43, .1), (23, 47, .8), (12, 53, .08)], .7, "possibility-c", "#bcb9af", dry=True),
        dab(10, 19, 2.7, 2.7), dab(63, 18, 2.5, 2.5, "#77746a"), dab(11, 54, 2.0, 2.0, "#bcb9af"), ground("possibility", 64),
    ],
    "practice": [
        r([(10, 22, .1), (29, 18, .85), (53, 22, .08)], 2.6, "practice-a"),
        r([(11, 38, .1), (30, 34, .85), (54, 38, .08)], 1.5, "practice-b", "#77746a", dry=True),
        r([(12, 54, .1), (31, 50, .85), (55, 54, .08)], .8, "practice-c", "#bcb9af", dry=True),
        dab(61, 52, 2.0, 2.0, "#4a4943"), ground("practice", 64),
    ],
    "proof": [
        dab(11, 36, 3.8, 3.8),
        r([(16, 36, .1), (29, 31, .8), (42, 35, .08)], 2.0, "proof-link"),
        dab(47, 35, 6.0, 5.7, "#77746a"),
        r([(43, 35, .1), (47, 40, .75), (55, 29, .08)], .8, "proof-check", "#bcb9af", dry=True), ground("proof"),
    ],
    "reason": [
        r([(36, 9, .1), (35, 34, .8), (36, 61, .08)], 2.2, "reason-stem"),
        r([(10, 29, .1), (35, 25, .9), (62, 29, .08)], 1.8, "reason-beam"),
        m("M 7 47 C 12 41 22 41 27 47 C 22 54 12 55 7 47 Z", "#4a4943"),
        m("M 48 46 C 53 40 63 40 68 46 C 63 53 53 54 48 46 Z", "#77746a"), ground("reason", 65),
    ],
    "research": [
        *book("research", 31),
        r([(43, 18, .1), (48, 29, .75), (48, 40, .9), (40, 49, .8), (29, 48, .9), (22, 40, .8), (23, 29, .9), (31, 22, .8), (43, 18, .08)], 1.8, "research-lens"),
        r([(43, 47, .1), (51, 54, .75), (59, 61, .08)], 2.4, "research-handle"),
        dab(35, 34, 2.2, 2.2, "#bcb9af"),
    ],
    "result": [
        r([(8, 55, .1), (20, 47, .8), (31, 51, .9), (42, 39, .9), (52, 29, .08)], 2.0, "result-path"),
        m("M 49 30 C 55 21 65 20 69 26 C 65 35 57 39 50 35 Z", "#4a4943"),
        dab(8, 55, 3.0, 3.0, "#77746a"), ground("result", 64),
    ],
    "scenario": [
        r([(36, 60, .1), (35, 44, .8), (36, 31, .08)], 2.0, "scenario-trunk"),
        r([(36, 37, .1), (22, 27, .8), (9, 23, .08)], 1.3, "scenario-a"),
        r([(36, 37, .1), (50, 27, .8), (64, 22, .08)], .8, "scenario-b", "#77746a", dry=True),
        m("M 4 17 C 8 13 16 13 20 17 C 19 24 14 29 6 27 C 3 24 3 20 4 17 Z", "#4a4943"),
        r([(54, 15, .1), (64, 12, .75), (69, 17, .9), (66, 27, .75), (55, 27, .08)], .7, "scenario-frame", "#bcb9af", dry=True), ground("scenario", 64),
    ],
    "science": [
        r([(25, 10, .1), (26, 27, .75), (17, 51, .9), (23, 60, .8), (50, 60, .9), (56, 51, .8), (46, 27, .9), (46, 10, .08)], 2.0, "science-vessel"),
        r([(26, 28, .1), (36, 31, .8), (46, 28, .08)], 1.1, "science-rim"),
        *leaf("science", 35, 42, False, "#4a4943"),
        dab(28, 47, 2.0, 2.0, "#bcb9af"),
    ],
    "study": [
        *book("study", 31),
        *eye("study-eye", 36, 25, .52),
        r([(17, 47, .1), (27, 44, .75), (35, 47, .08)], .65, "study-line", "#bcb9af", dry=True),
    ],
    "synthesis": [
        r([(8, 21, .1), (21, 29, .8), (35, 40, .08)], 1.7, "synthesis-a"),
        r([(64, 20, .1), (51, 29, .8), (36, 40, .08)], 1.0, "synthesis-b", "#77746a", dry=True),
        r([(36, 40, .1), (36, 51, .75), (37, 61, .08)], 2.0, "synthesis-stem"),
        *leaf("synthesis", 36, 47, True, "#4a4943"), ground("synthesis", 65),
    ],
    "test": [
        r([(23, 13, .1), (24, 30, .75), (17, 51, .9), (24, 59, .8), (48, 59, .9), (55, 51, .8), (47, 30, .9), (48, 13, .08)], 1.8, "test-vessel"),
        r([(25, 42, .1), (35, 47, .75), (47, 38, .08)], 1.5, "test-check"),
        r([(24, 31, .1), (36, 34, .8), (47, 31, .08)], .65, "test-liquid", "#bcb9af", dry=True),
    ],
    "then": [
        dab(10, 36, 3.4, 3.4), dab(32, 35, 3.0, 3.0, "#77746a"),
        r([(15, 36, .1), (29, 32, .8), (48, 35, .08)], 2.0, "then-line"),
        m("M 45 28 L 59 35 L 46 43 Z", "#4a4943"),
        r([(10, 58, .1), (29, 54, .8), (58, 57, .08)], .65, "then-ground", "#bcb9af", dry=True),
    ],
    "theory": [
        r([(12, 48, .1), (11, 34, .75), (20, 21, .9), (35, 17, .85), (50, 24, .9), (58, 38, .8), (52, 51, .9), (37, 56, .8), (22, 53, .9), (12, 48, .08)], 1.5, "theory-ring", "#77746a", dry=True),
        dab(20, 23, 3.0, 3.0), dab(50, 27, 2.6, 2.6, "#77746a"), dab(37, 50, 2.2, 2.2, "#bcb9af"),
        r([(20, 23, .1), (50, 27, .8), (37, 50, .08)], .65, "theory-thread", "#bcb9af", dry=True), ground("theory", 64),
    ],
    "wonder": [
        *eye("wonder", 31, 38, .78),
        dab(57, 16, 3.0, 3.0),
        r([(57, 11, .1), (57, 5, .75), (58, 2, .08)], .65, "wonder-ray-a", "#bcb9af", dry=True),
        r([(52, 17, .1), (47, 14, .75), (44, 12, .08)], .65, "wonder-ray-b", "#77746a", dry=True),
        r([(62, 17, .1), (66, 14, .75), (69, 13, .08)], .65, "wonder-ray-c", "#bcb9af", dry=True), ground("wonder", 64),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} science inquiry/method glyphs as sumi-e studies")
