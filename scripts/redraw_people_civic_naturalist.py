#!/usr/bin/env python3
"""Redraw civic and cultural people concepts as naturalist sumi-e studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def r(values, width, seed, color="#262522", *, dry=False) -> str:
    # Civic figures and their props must survive 32px without becoming dots and
    # hairlines; color still supplies the quieter secondary hierarchy.
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


def figure(name: str, x: float = 24, y: float = 18) -> list[str]:
    return [
        dab(x, y, 3.4, 3.7),
        r([(x, y + 4, .1), (x - 1, y + 17, .75), (x + 1, y + 31, .08)], 2.3, f"{name}-body"),
        r([(x + 1, y + 31, .1), (x - 7, y + 40, .75), (x - 13, y + 46, .08)], 1.1, f"{name}-leg-a"),
        r([(x + 1, y + 31, .1), (x + 9, y + 39, .75), (x + 16, y + 44, .08)], .7, f"{name}-leg-b", "#77746a", dry=True),
    ]


def ground(name: str) -> str:
    return r([(7, 65, .1), (29, 62, .85), (62, 64, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    codepoint = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>people / {name} — naturalist sumi-e civic study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "choice": [
        r([(35, 62, .1), (35, 46, .75), (35, 32, .9), (25, 21, .08)], 2.7, "choice-left"),
        r([(35, 34, .1), (46, 24, .75), (57, 16, .08)], 1.5, "choice-right", "#77746a", dry=True),
        dab(22, 18, 2.8, 2.8), dab(60, 14, 2.4, 2.4, "#77746a"),
        r([(9, 65, .1), (29, 62, .85), (58, 64, .08)], .65, "choice-ground", "#bcb9af", dry=True),
    ],
    "city": [
        r([(9, 60, .1), (10, 43, .75), (12, 26, .08)], 2.2, "city-tower-a"),
        r([(28, 60, .1), (28, 37, .75), (30, 14, .08)], 3.0, "city-tower-b"),
        r([(48, 60, .1), (48, 44, .75), (50, 29, .08)], 1.5, "city-tower-c", "#77746a", dry=True),
        r([(62, 60, .1), (61, 49, .75), (62, 39, .08)], .9, "city-tower-d", "#bcb9af", dry=True),
        r([(7, 63, .1), (28, 60, .85), (64, 62, .08)], .8, "city-ground", "#77746a", dry=True),
        r([(25, 19, .1), (30, 14, .75), (35, 19, .08)], .65, "city-crown", "#bcb9af", dry=True),
    ],
    "clothing": [
        r([(23, 15, .1), (18, 29, .75), (14, 48, .9), (10, 61, .08)], 2.4, "clothing-left"),
        r([(48, 15, .1), (52, 30, .75), (56, 47, .9), (61, 60, .08)], 1.4, "clothing-right", "#77746a", dry=True),
        r([(23, 15, .1), (35, 22, .85), (48, 15, .08)], 2.0, "clothing-collar"),
        r([(10, 61, .1), (35, 57, .9), (61, 60, .08)], 1.2, "clothing-hem", "#bcb9af", dry=True),
        r([(35, 23, .1), (34, 39, .75), (36, 55, .08)], .8, "clothing-fold", "#77746a", dry=True),
    ],
    "constitution": [
        r([(13, 16, .1), (33, 13, .85), (55, 17, .08)], 2.0, "constitution-top"),
        r([(13, 16, .1), (14, 36, .75), (16, 58, .08)], 1.6, "constitution-left"),
        r([(55, 17, .1), (53, 37, .75), (54, 56, .08)], 1.0, "constitution-right", "#77746a", dry=True),
        r([(16, 58, .1), (34, 55, .85), (54, 56, .08)], .8, "constitution-base", "#bcb9af", dry=True),
        r([(23, 29, .1), (34, 26, .75), (46, 29, .08)], .8, "constitution-line-a", "#77746a", dry=True),
        r([(23, 38, .1), (31, 35, .75), (40, 38, .08)], .65, "constitution-line-b", "#bcb9af", dry=True),
        dab(44, 48, 3.4, 3.4),
    ],
    "courage": figure("courage", 22, 19) + [
        r([(22, 33, .1), (35, 30, .75), (47, 24, .08)], 1.4, "courage-arm"),
        r([(52, 56, .1), (47, 47, .75), (51, 38, .9), (47, 29, .75), (54, 18, .9), (61, 31, .75), (58, 43, .9), (62, 53, .08)], 2.1, "courage-flame"),
        r([(49, 46, .1), (54, 40, .75), (58, 47, .08)], .7, "courage-flame-dry", "#bcb9af", dry=True),
        ground("courage"),
    ],
    "culture": [
        r([(17, 30, .1), (19, 45, .75), (27, 56, .9), (42, 58, .75), (52, 47, .9), (54, 31, .08)], 2.6, "culture-vessel"),
        r([(15, 29, .1), (34, 26, .9), (57, 30, .08)], 2.0, "culture-rim"),
        r([(24, 42, .1), (34, 36, .75), (45, 42, .08)], 1.1, "culture-mark"),
        r([(28, 48, .1), (34, 52, .75), (42, 48, .08)], .7, "culture-mark-dry", "#bcb9af", dry=True),
        r([(22, 21, .1), (28, 15, .75), (34, 20, .08)], .8, "culture-breath-a", "#77746a", dry=True),
        r([(39, 20, .1), (46, 13, .75), (52, 18, .08)], .65, "culture-breath-b", "#bcb9af", dry=True),
    ],
    "duty": figure("duty", 23, 18) + [
        r([(23, 32, .1), (35, 27, .75), (47, 31, .08)], 1.5, "duty-shoulder"),
        m("M 42 29 L 57 27 L 61 42 L 45 45 Z", "#4a4943"),
        r([(48, 28, .1), (50, 20, .75), (55, 16, .08)], .8, "duty-strap", "#77746a", dry=True),
        ground("duty"),
    ],
    "festival": [
        r([(8, 23, .1), (28, 19, .85), (51, 22, .95), (64, 18, .08)], 2.2, "festival-line"),
        m("M 18 22 L 25 24 L 21 34 Z", "#4a4943"),
        m("M 35 20 L 42 22 L 38 32 Z", "#77746a"),
        m("M 51 21 L 58 20 L 55 31 Z", "#4a4943"),
        dab(20, 45, 2.8, 3.0), dab(36, 39, 3.2, 3.4, "#4a4943"), dab(53, 46, 2.7, 2.9, "#77746a"),
        r([(20, 49, .1), (20, 56, .75), (21, 62, .08)], 1.1, "festival-person-a"),
        r([(36, 43, .1), (35, 52, .75), (37, 61, .08)], 1.5, "festival-person-b"),
        r([(53, 50, .1), (52, 56, .75), (53, 62, .08)], .8, "festival-person-c", "#77746a", dry=True),
        ground("festival"),
    ],
    "game": [
        dab(19, 22, 3.0, 3.2), dab(54, 23, 3.0, 3.2, "#77746a"),
        r([(19, 26, .1), (18, 37, .75), (21, 48, .08)], 1.9, "game-player-a"),
        r([(54, 27, .1), (53, 38, .75), (51, 48, .08)], 1.2, "game-player-b", "#77746a", dry=True),
        r([(14, 50, .1), (35, 46, .9), (59, 50, .08)], 2.1, "game-board"),
        dab(29, 44, 2.0, 2.0), dab(43, 45, 1.8, 1.8, "#bcb9af"),
        r([(12, 58, .1), (35, 55, .9), (60, 58, .08)], .7, "game-board-dry", "#bcb9af", dry=True),
    ],
    "identity": [
        r([(13, 16, .1), (34, 13, .9), (58, 17, .08)], 2.0, "identity-top"),
        r([(13, 16, .1), (14, 36, .75), (16, 58, .08)], 1.5, "identity-left"),
        r([(58, 17, .1), (56, 37, .75), (57, 55, .08)], .9, "identity-right", "#77746a", dry=True),
        r([(16, 58, .1), (35, 55, .85), (57, 55, .08)], .75, "identity-base", "#bcb9af", dry=True),
        r([(24, 47, .1), (21, 36, .75), (25, 25, .9), (36, 20, .75), (44, 27, .9), (42, 38, .75), (34, 44, .08)], 1.6, "identity-profile"),
        dab(48, 46, 2.0, 2.0, "#77746a"),
    ],
    "justice": [
        r([(35, 10, .1), (35, 32, .75), (36, 61, .08)], 2.4, "justice-stem"),
        r([(12, 27, .1), (35, 23, .9), (61, 27, .08)], 2.0, "justice-beam"),
        r([(18, 27, .1), (15, 40, .75), (11, 48, .08)], .9, "justice-cord-a", "#77746a", dry=True),
        r([(55, 27, .1), (58, 39, .75), (62, 47, .08)], .7, "justice-cord-b", "#bcb9af", dry=True),
        r([(6, 49, .1), (13, 55, .75), (22, 49, .08)], 1.4, "justice-pan-a"),
        r([(51, 48, .1), (60, 54, .75), (67, 48, .08)], .9, "justice-pan-b", "#77746a", dry=True),
        r([(27, 63, .1), (36, 60, .75), (46, 63, .08)], .65, "justice-base", "#bcb9af", dry=True),
    ],
    "language": [
        r([(10, 56, .1), (17, 45, .75), (15, 33, .9), (21, 21, .9), (34, 16, .75), (42, 24, .9), (39, 35, .75), (31, 42, .08)], 2.1, "language-profile"),
        r([(29, 42, .1), (35, 49, .75), (41, 55, .08)], .9, "language-neck", "#77746a", dry=True),
        r([(42, 29, .1), (51, 25, .75), (60, 29, .08)], 1.2, "language-breath-a"),
        r([(44, 39, .1), (55, 35, .75), (64, 40, .08)], .75, "language-breath-b", "#77746a", dry=True),
        r([(8, 62, .1), (25, 59, .85), (45, 61, .08)], .65, "language-ground", "#bcb9af", dry=True),
    ],
    "law": [
        r([(13, 19, .1), (34, 16, .9), (58, 20, .08)], 2.3, "law-pediment"),
        r([(16, 23, .1), (16, 41, .75), (17, 58, .08)], 1.7, "law-column-a"),
        r([(35, 20, .1), (34, 40, .75), (35, 58, .08)], 1.1, "law-column-b", "#77746a", dry=True),
        r([(55, 22, .1), (54, 40, .75), (55, 57, .08)], .8, "law-column-c", "#bcb9af", dry=True),
        r([(12, 61, .1), (34, 58, .9), (60, 61, .08)], 1.8, "law-base"),
        r([(26, 30, .1), (35, 27, .75), (44, 30, .08)], .7, "law-tablet", "#bcb9af", dry=True),
    ],
    "leadership": figure("leadership", 43, 13) + [
        r([(43, 27, .1), (54, 20, .75), (64, 10, .08)], 1.5, "leadership-direction"),
        dab(12, 43, 2.6, 2.8, "#77746a"), dab(25, 48, 2.4, 2.6, "#bcb9af"),
        r([(12, 47, .1), (12, 55, .75), (13, 62, .08)], .9, "leadership-follower-a", "#77746a", dry=True),
        r([(25, 52, .1), (24, 58, .75), (25, 63, .08)], .65, "leadership-follower-b", "#bcb9af", dry=True),
        ground("leadership"),
    ],
    "migration": [
        r([(7, 58, .1), (18, 48, .75), (30, 53, .9), (43, 40, .9), (57, 44, .75), (65, 30, .08)], 2.1, "migration-path"),
        r([(15, 28, .1), (21, 23, .75), (27, 27, .08)], 1.0, "migration-bird-a"),
        r([(31, 20, .1), (38, 14, .75), (45, 19, .08)], .8, "migration-bird-b", "#77746a", dry=True),
        r([(48, 27, .1), (55, 22, .75), (62, 26, .08)], .65, "migration-bird-c", "#bcb9af", dry=True),
        dab(7, 58, 2.3, 2.3, "#77746a"),
        ground("migration"),
    ],
    "name": [
        r([(14, 18, .1), (33, 15, .85), (54, 19, .08)], 2.0, "name-top"),
        r([(14, 18, .1), (15, 36, .75), (17, 55, .08)], 1.4, "name-left"),
        r([(54, 19, .1), (52, 37, .75), (53, 53, .08)], .9, "name-right", "#77746a", dry=True),
        r([(17, 55, .1), (34, 52, .85), (53, 53, .08)], .75, "name-base", "#bcb9af", dry=True),
        r([(23, 30, .1), (32, 25, .75), (43, 30, .9), (36, 40, .75), (25, 38, .08)], 1.2, "name-mark"),
        dab(46, 45, 2.4, 2.4, "#77746a"),
    ],
    "nation": [
        r([(9, 58, .1), (20, 43, .75), (32, 27, .9), (43, 43, .75), (59, 58, .08)], 2.4, "nation-mountain"),
        r([(47, 57, .1), (47, 36, .75), (49, 15, .08)], 1.9, "nation-flagpole"),
        m("M 49 16 C 56 14 63 17 67 22 C 61 27 55 27 49 24 Z", "#4a4943"),
        dab(17, 56, 2.2, 2.3, "#77746a"), dab(29, 53, 2.0, 2.1, "#bcb9af"),
        r([(8, 63, .1), (30, 60, .85), (61, 62, .08)], .65, "nation-ground", "#bcb9af", dry=True),
    ],
    "progress": [
        m("M 9 51 L 23 48 L 24 60 L 10 63 Z", "#77746a"),
        m("M 24 39 L 39 36 L 40 52 L 25 55 Z", "#4a4943"),
        m("M 40 25 L 55 22 L 57 41 L 41 44 Z", "#77746a"),
        r([(13, 47, .1), (27, 37, .75), (42, 25, .9), (59, 12, .08)], 2.0, "progress-rise"),
        m("M 55 8 L 65 10 L 60 18 Z", "#262522"),
        r([(8, 65, .1), (30, 62, .85), (58, 64, .08)], .65, "progress-ground", "#bcb9af", dry=True),
    ],
    "rights": [
        r([(10, 20, .1), (35, 16, .9), (62, 20, .08)], 2.4, "rights-equal-bar"),
        dab(20, 32, 3.0, 3.2), dab(51, 32, 3.0, 3.2, "#77746a"),
        r([(20, 36, .1), (19, 46, .75), (21, 57, .08)], 1.8, "rights-person-a"),
        r([(51, 36, .1), (50, 46, .75), (52, 57, .08)], 1.1, "rights-person-b", "#77746a", dry=True),
        r([(20, 43, .1), (35, 38, .75), (51, 43, .08)], .9, "rights-link", "#bcb9af", dry=True),
        ground("rights"),
    ],
    "role": [
        dab(22, 22, 3.2, 3.5),
        r([(22, 26, .1), (21, 40, .75), (24, 55, .08)], 2.1, "role-person"),
        r([(39, 22, .1), (50, 17, .8), (61, 24, .9), (58, 39, .8), (48, 47, .9), (39, 38, .8), (37, 27, .08)], 1.7, "role-mask"),
        r([(45, 29, .1), (49, 27, .75), (53, 29, .08)], .65, "role-eye", "#bcb9af", dry=True),
        r([(24, 38, .1), (35, 34, .75), (40, 30, .08)], .9, "role-reach", "#77746a", dry=True),
        ground("role"),
    ],
    "rule": [
        r([(15, 12, .1), (15, 35, .75), (16, 61, .08)], 2.5, "rule-standard"),
        r([(16, 21, .1), (35, 18, .9), (59, 22, .08)], 2.0, "rule-measure"),
        r([(26, 20, .1), (26, 27, .75), (27, 33, .08)], .75, "rule-tick-a", "#77746a", dry=True),
        r([(42, 20, .1), (42, 26, .75), (43, 31, .08)], .65, "rule-tick-b", "#bcb9af", dry=True),
        r([(57, 22, .1), (57, 39, .75), (56, 57, .08)], 1.0, "rule-plumb", "#77746a", dry=True),
        dab(56, 59, 2.0, 2.0, "#bcb9af"),
        ground("rule"),
    ],
    "symbol": [
        r([(14, 47, .1), (12, 34, .75), (20, 21, .9), (34, 16, .85), (48, 22, .75), (56, 36, .9), (51, 50, .75), (37, 57, .9), (23, 53, .75), (14, 47, .08)], 2.0, "symbol-ring"),
        r([(25, 45, .1), (34, 25, .85), (44, 46, .08)], 2.0, "symbol-mark"),
        r([(25, 40, .1), (34, 43, .75), (44, 40, .08)], .7, "symbol-cross", "#77746a", dry=True),
        dab(53, 15, 1.7, 1.7, "#bcb9af"),
    ],
    "value": figure("value", 21, 19) + [
        r([(21, 33, .1), (32, 39, .75), (43, 37, .08)], 1.3, "value-offer"),
        r([(43, 36, .1), (49, 29, .75), (57, 36, .9), (52, 45, .75), (44, 43, .08)], 1.8, "value-gem"),
        r([(48, 31, .1), (50, 39, .75), (45, 42, .08)], .65, "value-facet", "#bcb9af", dry=True),
        dab(60, 22, 1.8, 1.8, "#bcb9af"),
        ground("value"),
    ],
    "village": [
        r([(7, 39, .1), (17, 29, .75), (28, 39, .08)], 1.8, "village-roof-a"),
        r([(35, 35, .1), (47, 23, .75), (61, 35, .08)], 2.1, "village-roof-b"),
        r([(9, 40, .1), (10, 51, .75), (11, 59, .08)], 1.2, "village-wall-a"),
        r([(26, 39, .1), (25, 50, .75), (26, 58, .08)], .8, "village-wall-b", "#77746a", dry=True),
        r([(38, 36, .1), (38, 49, .75), (39, 59, .08)], 1.4, "village-wall-c"),
        r([(59, 35, .1), (58, 48, .75), (59, 58, .08)], .8, "village-wall-d", "#bcb9af", dry=True),
        dab(32, 54, 2.2, 2.4, "#77746a"),
        ground("village"),
    ],
    "vote": figure("vote", 20, 18) + [
        r([(20, 32, .1), (31, 38, .75), (42, 39, .08)], 1.2, "vote-arm"),
        m("M 48 18 L 59 16 L 61 28 L 49 30 Z", "#4a4943"),
        r([(47, 18, .1), (42, 28, .75), (38, 39, .08)], .8, "vote-ballot", "#77746a", dry=True),
        r([(39, 43, .1), (51, 40, .8), (64, 43, .08)], 2.0, "vote-box-top"),
        r([(42, 44, .1), (43, 54, .75), (45, 60, .08)], 1.0, "vote-box-left", "#77746a", dry=True),
        r([(61, 43, .1), (59, 53, .75), (58, 59, .08)], .7, "vote-box-right", "#bcb9af", dry=True),
        ground("vote"),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} civic/cultural people glyphs as sumi-e studies")
