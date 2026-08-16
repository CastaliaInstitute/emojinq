#!/usr/bin/env python3
"""Redraw language, writing, and storytelling science glyphs as naturalist sumi-e."""

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


def page(name: str, x1=15, x2=57, y1=13, y2=58) -> list[str]:
    return [
        r([(x1, y1+3, .1), ((x1+x2)/2, y1, .85), (x2, y1+3, .08)], 1.8, f"{name}-top"),
        r([(x1, y1+3, .1), (x1+2, (y1+y2)/2, .8), (x1, y2, .08)], 1.1, f"{name}-left", "#77746a", dry=True),
        r([(x2, y1+3, .1), (x2-2, (y1+y2)/2, .8), (x2, y2, .08)], .8, f"{name}-right", "#bcb9af", dry=True),
        r([(x1, y2, .1), ((x1+x2)/2, y2-3, .85), (x2, y2, .08)], 1.3, f"{name}-bottom", "#77746a", dry=True),
    ]


def line(name: str, y: float, x1=22, x2=50, width=.7, color="#77746a") -> str:
    return r([(x1, y, .1), ((x1+x2)/2, y-2, .8), (x2, y, .08)], width, name, color, dry=True)


def speech(name: str, x: float, y: float, flip=False, color="#4a4943") -> list[str]:
    s = -1 if flip else 1
    return [
        m(f"M {x} {y} C {x+5*s} {y-7} {x+16*s} {y-8} {x+21*s} {y-2} C {x+16*s} {y+5} {x+6*s} {y+6} {x} {y} Z", color),
        r([(x+2*s, y+5, .1), (x+6*s, y+10, .75), (x+9*s, y+13, .08)], .65, f"{name}-tail", "#bcb9af", dry=True),
    ]


def hook(name: str, x=35, y=18, color="#262522") -> list[str]:
    return [
        r([(x-12, y+5, .1), (x-7, y-3, .75), (x+4, y-5, .9), (x+12, y+1, .8), (x+10, y+10, .9), (x+1, y+16, .8), (x, y+24, .08)], 2.3, f"{name}-hook", color),
        dab(x, y+35, 2.8, 2.8, "#77746a"),
    ]


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>science / {name} — naturalist sumi-e language study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "archive": [
        *page("archive-a", 10, 42, 13, 55),
        *page("archive-b", 28, 62, 18, 60),
        r([(22, 32, .1), (36, 29, .8), (51, 32, .08)], 2.0, "archive-tie"),
        dab(36, 31, 3.0, 3.0), ground("archive", 65),
    ],
    "argument": [
        *speech("argument-a", 7, 29, False, "#4a4943"),
        *speech("argument-b", 65, 43, True, "#77746a"),
        r([(28, 32, .1), (36, 37, .8), (44, 42, .08)], 1.2, "argument-clash-a"),
        r([(28, 43, .1), (36, 37, .8), (44, 31, .08)], .75, "argument-clash-b", "#bcb9af", dry=True),
        ground("argument"),
    ],
    "art": [
        r([(12, 55, .1), (25, 43, .75), (40, 29, .9), (58, 12, .08)], 3.0, "art-brush"),
        m("M 54 8 L 66 13 L 59 22 L 48 16 Z", "#77746a"),
        m("M 13 48 C 22 42 34 45 38 53 C 30 60 18 61 11 55 Z", "#4a4943"),
        r([(8, 64, .1), (27, 60, .85), (58, 63, .08)], .65, "art-ground", "#bcb9af", dry=True),
    ],
    "because": [
        dab(11, 38, 4.0, 4.0),
        r([(17, 38, .1), (31, 33, .8), (46, 37, .08)], 2.0, "because-link"),
        m("M 43 30 L 56 37 L 44 45 Z", "#77746a"),
        r([(56, 38, .1), (58, 49, .75), (59, 58, .08)], .9, "because-stem", "#bcb9af", dry=True),
        m("M 57 48 C 50 42 43 43 40 47 C 45 53 51 55 57 52 Z", "#4a4943"), ground("because"),
    ],
    "conclusion": [
        r([(8, 18, .1), (24, 25, .8), (36, 35, .9), (47, 47, .8), (59, 55, .08)], 2.2, "conclusion-a"),
        r([(63, 18, .1), (49, 24, .8), (37, 35, .9), (29, 46, .08)], 1.2, "conclusion-b", "#77746a", dry=True),
        dab(36, 36, 4.2, 4.2), ground("conclusion"),
    ],
    "dialogue": [
        *speech("dialogue-a", 7, 27, False, "#4a4943"),
        *speech("dialogue-b", 65, 44, True, "#77746a"),
        r([(27, 55, .1), (35, 58, .75), (44, 54, .08)], .65, "dialogue-breath", "#bcb9af", dry=True),
        ground("dialogue", 64),
    ],
    "explanation": [
        m("M 36 10 C 26 10 19 18 20 28 C 21 35 27 39 31 42 L 41 42 C 44 37 51 33 52 25 C 52 16 45 10 36 10 Z", "#77746a"),
        r([(31, 45, .1), (36, 43, .8), (42, 45, .08)], 2.0, "explanation-base"),
        line("explanation-line-a", 54, 18, 54, .8), line("explanation-line-b", 61, 24, 49, .65, "#bcb9af"),
        r([(35, 16, .1), (37, 23, .75), (36, 32, .08)], .65, "explanation-glow", "#bcb9af", dry=True),
    ],
    "expression": [
        m("M 10 38 C 17 26 29 21 40 26 C 35 39 24 47 10 44 Z", "#4a4943"),
        r([(40, 34, .1), (50, 27, .75), (62, 29, .08)], 1.5, "expression-breath-a"),
        r([(41, 40, .1), (52, 38, .75), (65, 43, .08)], .8, "expression-breath-b", "#77746a", dry=True),
        r([(15, 57, .1), (31, 54, .8), (55, 57, .08)], .65, "expression-ground", "#bcb9af", dry=True),
    ],
    "grammar": [
        r([(9, 18, .1), (9, 37, .8), (10, 57, .08)], 1.8, "grammar-bracket-a"),
        r([(63, 17, .1), (62, 36, .8), (63, 56, .08)], 1.0, "grammar-bracket-b", "#77746a", dry=True),
        dab(21, 28, 3.2, 3.2), dab(35, 36, 3.0, 3.0, "#4a4943"), dab(50, 45, 2.6, 2.6, "#77746a"),
        r([(21, 28, .1), (35, 36, .8), (50, 45, .08)], .7, "grammar-thread", "#bcb9af", dry=True), ground("grammar", 63),
    ],
    "how": [
        *hook("how", 35, 13),
        r([(10, 58, .1), (22, 51, .8), (31, 56, .08)], 1.4, "how-hand-a"),
        r([(61, 58, .1), (50, 51, .8), (41, 56, .08)], .8, "how-hand-b", "#bcb9af", dry=True),
        ground("how", 65),
    ],
    "legend": [
        *page("legend", 14, 57, 12, 59),
        r([(23, 45, .1), (30, 35, .75), (37, 26, .9), (44, 36, .75), (51, 45, .08)], 1.8, "legend-mountain"),
        dab(48, 21, 3.0, 3.0, "#77746a"), line("legend-line", 52, 22, 48, .65, "#bcb9af"),
    ],
    "meaning": [
        r([(13, 43, .1), (11, 30, .75), (21, 19, .9), (36, 16, .85), (51, 23, .9), (58, 36, .8), (53, 50, .9), (39, 57, .8), (24, 54, .9), (13, 43, .08)], 1.7, "meaning-ring", "#77746a", dry=True),
        dab(36, 36, 5.0, 5.0),
        r([(36, 41, .1), (43, 50, .75), (55, 57, .08)], .8, "meaning-thread", "#bcb9af", dry=True), ground("meaning", 65),
    ],
    "memory": [
        *page("memory", 14, 55, 14, 58),
        r([(23, 29, .1), (34, 25, .8), (47, 29, .08)], 1.4, "memory-mark-a"),
        r([(24, 40, .1), (35, 36, .8), (47, 40, .08)], .8, "memory-mark-b", "#77746a", dry=True),
        m("M 44 48 C 50 40 59 40 64 45 C 59 53 52 56 45 52 Z", "#4a4943"), ground("memory", 64),
    ],
    "metaphor": [
        m("M 10 45 C 17 34 29 31 38 38 C 32 49 21 54 10 49 Z", "#4a4943"),
        r([(37, 41, .1), (45, 34, .75), (52, 25, .08)], 1.4, "metaphor-transform"),
        m("M 54 13 C 47 22 48 31 55 35 C 63 31 64 21 54 13 Z", "#77746a"),
        r([(9, 60, .1), (28, 56, .8), (58, 59, .08)], .65, "metaphor-ground", "#bcb9af", dry=True),
    ],
    "music": [
        r([(45, 15, .1), (44, 32, .8), (45, 50, .08)], 2.2, "music-stem"),
        r([(44, 16, .1), (54, 20, .75), (62, 18, .08)], 1.4, "music-flag"),
        m("M 31 49 C 36 43 45 43 49 48 C 45 55 36 57 31 52 Z", "#4a4943"),
        r([(8, 31, .1), (17, 25, .75), (26, 30, .08)], .8, "music-echo-a", "#77746a", dry=True),
        r([(7, 42, .1), (16, 37, .75), (25, 41, .08)], .65, "music-echo-b", "#bcb9af", dry=True), ground("music"),
    ],
    "noun": [
        m("M 20 47 C 21 33 29 23 40 22 C 50 25 55 36 52 47 C 43 53 30 54 20 47 Z", "#4a4943"),
        r([(10, 60, .1), (30, 56, .85), (61, 59, .08)], 1.0, "noun-ground", "#77746a", dry=True),
        dab(54, 17, 2.2, 2.2, "#bcb9af"),
    ],
    "painting": [
        *page("painting", 12, 60, 9, 62),
        r([(18, 48, .1), (28, 34, .75), (37, 45, .9), (49, 27, .75), (57, 47, .08)], 1.8, "painting-mountain"),
        m("M 38 45 C 45 35 54 34 59 40 C 55 48 47 51 39 48 Z", "#77746a"),
        r([(17, 54, .1), (31, 50, .8), (51, 53, .08)], .65, "painting-water", "#bcb9af", dry=True),
    ],
    "poetry": [
        r([(13, 53, .1), (28, 41, .75), (44, 27, .9), (59, 13, .08)], 2.7, "poetry-brush"),
        m("M 55 9 L 66 14 L 59 22 L 49 17 Z", "#77746a"),
        line("poetry-line-a", 46, 12, 37, 1.1, "#4a4943"), line("poetry-line-b", 55, 9, 33, .75), line("poetry-line-c", 62, 15, 30, .65, "#bcb9af"),
    ],
    "question": [*hook("question", 35, 12), ground("question")],
    "record": [
        *page("record", 13, 58, 12, 60),
        line("record-line-a", 27, 21, 49, .8), line("record-line-b", 37, 21, 45, .65, "#bcb9af"),
        dab(47, 49, 6.0, 5.6, "#4a4943"),
        r([(44, 47, .1), (48, 51, .75), (53, 45, .08)], .65, "record-seal", "#bcb9af", dry=True),
    ],
    "revision": [
        *page("revision", 13, 56, 15, 60),
        r([(18, 34, .1), (23, 23, .75), (37, 18, .9), (50, 24, .8), (55, 36, .08)], 1.8, "revision-loop"),
        m("M 50 31 L 61 37 L 50 44 Z", "#4a4943"), line("revision-line", 49, 22, 46, .65, "#bcb9af"),
    ],
    "rhyme": [
        r([(7, 25, .1), (20, 19, .8), (34, 24, .9), (48, 18, .8), (63, 22, .08)], 1.8, "rhyme-a"),
        r([(7, 43, .1), (20, 37, .8), (34, 42, .9), (48, 36, .8), (63, 40, .08)], 1.1, "rhyme-b", "#77746a", dry=True),
        dab(63, 22, 2.6, 2.6), dab(63, 40, 2.2, 2.2, "#77746a"), ground("rhyme"),
    ],
    "sentence": [
        dab(10, 35, 3.0, 3.0), dab(23, 34, 2.8, 2.8, "#4a4943"), dab(36, 36, 2.5, 2.5, "#77746a"), dab(49, 33, 2.8, 2.8),
        r([(8, 44, .1), (28, 40, .8), (52, 43, .08)], 1.1, "sentence-line"),
        dab(62, 47, 2.4, 2.4, "#77746a"), ground("sentence"),
    ],
    "story": [
        *page("story", 13, 58, 11, 61),
        r([(21, 46, .1), (29, 34, .75), (37, 44, .9), (47, 29, .75), (54, 45, .08)], 1.7, "story-mountain"),
        dab(49, 22, 2.8, 2.8, "#77746a"), line("story-line", 53, 22, 48, .65, "#bcb9af"),
    ],
    "storytelling": [
        *page("storytelling", 8, 47, 13, 60),
        *speech("storytelling-voice", 43, 28, False, "#4a4943"),
        r([(19, 44, .1), (25, 35, .75), (32, 43, .08)], .9, "storytelling-mountain", "#77746a", dry=True),
        ground("storytelling", 64),
    ],
    "style": [
        r([(8, 49, .1), (22, 38, .75), (38, 30, .9), (58, 15, .08)], 3.2, "style-main"),
        r([(12, 57, .1), (27, 48, .75), (43, 41, .08)], 1.1, "style-echo", "#77746a", dry=True),
        r([(23, 62, .1), (38, 57, .75), (53, 52, .08)], .65, "style-breath", "#bcb9af", dry=True),
        dab(62, 12, 2.3, 2.3, "#4a4943"),
    ],
    "symbol": [
        r([(14, 48, .1), (10, 36, .75), (16, 23, .9), (29, 17, .85), (43, 21, .9), (50, 32, .8), (47, 43, .9), (37, 49, .8), (27, 46, .9), (23, 38, .8), (27, 31, .9), (35, 29, .08)], 2.0, "symbol-spiral"),
        dab(36, 29, 3.0, 3.0),
        r([(45, 51, .1), (54, 56, .75), (64, 54, .08)], .7, "symbol-tail", "#bcb9af", dry=True), ground("symbol", 63),
    ],
    "translation": [
        *speech("translation-a", 7, 26, False, "#4a4943"),
        *speech("translation-b", 65, 45, True, "#77746a"),
        r([(28, 29, .1), (36, 34, .8), (44, 40, .08)], 1.4, "translation-cross-a"),
        r([(28, 43, .1), (36, 36, .8), (44, 28, .08)], .75, "translation-cross-b", "#bcb9af", dry=True), ground("translation"),
    ],
    "verb": [
        r([(8, 51, .1), (21, 42, .8), (34, 47, .9), (47, 34, .9), (61, 37, .08)], 2.4, "verb-motion"),
        m("M 57 30 L 68 35 L 61 44 Z", "#4a4943"),
        r([(12, 61, .1), (30, 57, .8), (57, 60, .08)], .65, "verb-ground", "#bcb9af", dry=True),
        r([(20, 34, .1), (27, 30, .75), (33, 31, .08)], .7, "verb-echo", "#77746a", dry=True),
    ],
    "voice": [
        m("M 9 37 C 16 27 28 23 38 28 C 33 40 22 47 9 43 Z", "#4a4943"),
        r([(38, 33, .1), (48, 27, .75), (62, 30, .08)], 1.6, "voice-wave-a"),
        r([(39, 41, .1), (51, 38, .75), (65, 42, .08)], .9, "voice-wave-b", "#77746a", dry=True),
        r([(17, 57, .1), (34, 54, .8), (57, 57, .08)], .65, "voice-ground", "#bcb9af", dry=True),
    ],
    "what": [
        m("M 9 43 C 12 30 21 22 33 21 C 43 25 48 35 45 46 C 35 52 20 52 9 43 Z", "#77746a"),
        *hook("what", 54, 17, "#262522"), ground("what", 64),
    ],
    "when": [
        r([(13, 45, .1), (11, 32, .75), (20, 20, .9), (34, 16, .85), (48, 23, .9), (55, 36, .8), (50, 49, .9), (37, 55, .8), (23, 52, .9), (13, 45, .08)], 1.6, "when-clock", "#77746a", dry=True),
        r([(35, 35, .1), (35, 23, .75), (36, 17, .08)], 1.7, "when-hand-a"),
        r([(35, 35, .1), (44, 40, .75), (51, 44, .08)], 1.0, "when-hand-b"),
        dab(36, 35, 2.5, 2.5), *hook("when-q", 57, 11, "#77746a"),
    ],
    "where": [
        r([(7, 53, .1), (20, 37, .75), (31, 51, .9), (44, 29, .75), (61, 53, .08)], 2.0, "where-mountain"),
        *hook("where-q", 54, 8, "#77746a"), ground("where"),
    ],
    "who": [
        dab(24, 24, 6.0, 6.2, "#4a4943"),
        r([(24, 31, .1), (22, 43, .8), (24, 56, .08)], 2.5, "who-body"),
        r([(24, 38, .1), (14, 45, .75), (8, 50, .08)], .8, "who-arm", "#bcb9af", dry=True),
        *hook("who-q", 51, 13, "#77746a"), ground("who", 64),
    ],
    "why": [
        dab(36, 18, 4.0, 4.0),
        r([(36, 23, .1), (35, 35, .8), (24, 46, .08)], 1.8, "why-branch-a"),
        r([(36, 34, .1), (48, 45, .8), (59, 53, .08)], 1.1, "why-branch-b", "#77746a", dry=True),
        *hook("why-q", 16, 17, "#77746a"), ground("why", 64),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} science language/story glyphs as sumi-e studies")
