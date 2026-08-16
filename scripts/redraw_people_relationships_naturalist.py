#!/usr/bin/env python3
"""Redraw relationship and community people glyphs as naturalist sumi-e."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def r(values, width, seed, color="#262522", *, dry=False) -> str:
    # Keep paired bodies, joined arms, and support gestures readable at 32px.
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


def figure(name: str, x: float, y: float = 20, scale: float = 1.0, color: str = "#262522") -> list[str]:
    return [
        dab(x, y, 3.3 * scale, 3.6 * scale, color),
        r([(x, y + 4, .1), (x - 1, y + 15, .75), (x + 1, y + 27, .08)], 2.2 * scale, f"{name}-body", color),
        r([(x + 1, y + 27, .1), (x - 6, y + 35, .75), (x - 11, y + 40, .08)], 1.0 * scale, f"{name}-leg-a", color),
        r([(x + 1, y + 27, .1), (x + 7, y + 34, .75), (x + 12, y + 39, .08)], .65 * scale, f"{name}-leg-b", "#77746a", dry=True),
    ]


def ground(name: str) -> str:
    return r([(7, 64, .1), (29, 61, .85), (62, 63, .08)], .65, f"{name}-ground", "#bcb9af", dry=True)


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>people / {name} — naturalist sumi-e relationship study</title>{''.join(marks)}</svg>
''')


GLYPHS = {
    "alliance": figure("alliance-a", 22, 21, .9) + figure("alliance-b", 50, 21, .9, "#77746a") + [
        r([(22, 34, .1), (35, 27, .8), (50, 34, .08)], 1.6, "alliance-joined-arms"),
        r([(18, 15, .1), (35, 9, .85), (54, 14, .08)], .8, "alliance-canopy", "#bcb9af", dry=True),
        ground("alliance"),
    ],
    "care": [
        dab(23, 18, 3.5, 3.8),
        r([(23, 22, .1), (22, 36, .75), (29, 49, .08)], 2.5, "care-standing"),
        dab(49, 36, 3.0, 3.2, "#77746a"),
        r([(48, 40, .1), (43, 49, .75), (46, 58, .08)], 1.5, "care-seated", "#77746a"),
        r([(23, 32, .1), (34, 37, .75), (46, 40, .08)], 1.7, "care-support"),
        r([(29, 49, .1), (39, 54, .75), (49, 52, .08)], .7, "care-lap", "#bcb9af", dry=True),
        ground("care"),
    ],
    "circle": [
        dab(36, 11, 3.0, 3.2), dab(59, 34, 2.8, 3.0, "#77746a"), dab(35, 58, 2.7, 2.9), dab(12, 36, 2.6, 2.8, "#77746a"),
        r([(36, 14, .1), (52, 18, .75), (58, 31, .08)], 1.1, "circle-arc-a"),
        r([(57, 38, .1), (51, 52, .75), (38, 58, .08)], .8, "circle-arc-b", "#77746a", dry=True),
        r([(32, 58, .1), (18, 52, .75), (13, 39, .08)], .7, "circle-arc-c", "#bcb9af", dry=True),
        r([(13, 33, .1), (19, 19, .75), (33, 13, .08)], .8, "circle-arc-d", "#77746a", dry=True),
    ],
    "community": figure("community-a", 18, 29, .75) + figure("community-b", 36, 25, .85, "#4a4943") + figure("community-c", 53, 29, .72, "#77746a") + [
        r([(8, 29, .1), (21, 18, .75), (36, 10, .9), (52, 19, .75), (64, 31, .08)], 2.2, "community-roof"),
        ground("community"),
    ],
    "compassion": figure("compassion-a", 22, 21, .9) + figure("compassion-b", 50, 22, .85, "#77746a") + [
        r([(22, 35, .1), (34, 42, .75), (49, 35, .08)], 1.5, "compassion-arms"),
        m("M 30 43 C 32 37 39 35 43 39 C 45 44 39 49 34 50 C 31 48 29 46 30 43 Z", "#4a4943"),
        r([(18, 15, .1), (35, 10, .85), (53, 15, .08)], .7, "compassion-breath", "#bcb9af", dry=True),
        ground("compassion"),
    ],
    "conflict": figure("conflict-a", 20, 23, .9) + figure("conflict-b", 52, 23, .9, "#77746a") + [
        r([(21, 35, .1), (34, 28, .75), (50, 37, .08)], 1.8, "conflict-strike-a"),
        r([(51, 34, .1), (38, 28, .75), (22, 39, .08)], 1.0, "conflict-strike-b", "#77746a", dry=True),
        r([(33, 18, .1), (36, 12, .75), (39, 18, .08)], .7, "conflict-spark", "#bcb9af", dry=True),
        ground("conflict"),
    ],
    "cooperation": figure("cooperation-a", 20, 23, .85) + figure("cooperation-b", 52, 23, .85, "#77746a") + [
        r([(20, 35, .1), (30, 39, .75), (36, 38, .08)], 1.3, "cooperation-arm-a"),
        r([(52, 35, .1), (43, 39, .75), (36, 38, .08)], .9, "cooperation-arm-b", "#77746a", dry=True),
        r([(27, 42, .1), (36, 39, .85), (46, 42, .08)], 2.0, "cooperation-load"),
        ground("cooperation"),
    ],
    "council": figure("council-a", 17, 23, .7) + figure("council-b", 36, 17, .75, "#4a4943") + figure("council-c", 55, 24, .68, "#77746a") + [
        r([(12, 49, .1), (35, 45, .9), (61, 49, .08)], 2.1, "council-table"),
        r([(22, 55, .1), (35, 52, .85), (50, 55, .08)], .7, "council-table-dry", "#bcb9af", dry=True),
        ground("council"),
    ],
    "cousin": figure("cousin-a", 23, 29, .8) + figure("cousin-b", 49, 29, .8, "#77746a") + [
        r([(23, 25, .1), (25, 16, .75), (35, 12, .9), (47, 17, .75), (49, 25, .08)], 1.2, "cousin-lineage"),
        r([(35, 12, .1), (35, 7, .75), (35, 4, .08)], .8, "cousin-ancestor", "#bcb9af", dry=True),
        r([(23, 42, .1), (35, 37, .75), (49, 42, .08)], .9, "cousin-link", "#77746a", dry=True),
        ground("cousin"),
    ],
    "diversity": [
        dab(14, 30, 2.6, 2.8), dab(31, 20, 3.8, 4.0, "#4a4943"), dab(51, 27, 3.0, 3.2, "#77746a"), dab(62, 38, 2.1, 2.3, "#bcb9af"),
        r([(14, 34, .1), (13, 44, .75), (15, 54, .08)], 1.4, "diversity-a"),
        r([(31, 25, .1), (30, 39, .75), (33, 54, .08)], 2.3, "diversity-b"),
        r([(51, 31, .1), (52, 42, .75), (50, 54, .08)], 1.6, "diversity-c", "#77746a", dry=True),
        r([(62, 41, .1), (61, 48, .75), (62, 55, .08)], .8, "diversity-d", "#bcb9af", dry=True),
        ground("diversity"),
    ],
    "empathy": [
        dab(21, 25, 3.2, 3.4), dab(51, 25, 3.2, 3.4, "#77746a"),
        r([(21, 29, .1), (24, 41, .75), (34, 48, .08)], 2.0, "empathy-a"),
        r([(51, 29, .1), (48, 41, .75), (38, 48, .08)], 1.2, "empathy-b", "#77746a", dry=True),
        r([(28, 35, .1), (36, 31, .75), (44, 35, .08)], 1.0, "empathy-shared-breath"),
        r([(29, 53, .1), (36, 50, .75), (44, 53, .08)], .65, "empathy-base", "#bcb9af", dry=True),
        ground("empathy"),
    ],
    "friend": figure("friend-a", 27, 21, .9) + figure("friend-b", 45, 22, .85, "#77746a") + [
        r([(27, 34, .1), (35, 29, .75), (44, 34, .08)], 1.6, "friend-shoulders"),
        r([(22, 15, .1), (35, 10, .85), (48, 15, .08)], .7, "friend-breath", "#bcb9af", dry=True),
        ground("friend"),
    ],
    "gift": figure("gift-giver", 20, 22, .85) + figure("gift-receiver", 53, 23, .82, "#77746a") + [
        r([(20, 35, .1), (30, 39, .75), (39, 38, .08)], 1.3, "gift-offer"),
        m("M 31 31 L 47 31 L 47 47 L 31 47 Z", "#4a4943"),
        r([(39, 31, .1), (39, 39, .75), (39, 47, .08)], 1.0, "gift-ribbon-v", "#bcb9af", dry=True),
        r([(31, 36, .1), (39, 36, .75), (47, 36, .08)], .85, "gift-ribbon-h", "#262522"),
        m("M 39 31 C 34 30 31 27 32 24 C 35 22 38 26 39 29 Z", "#262522"),
        m("M 39 31 C 43 29 47 24 49 27 C 49 30 44 32 39 31 Z", "#77746a"),
        ground("gift"),
    ],
    "grandparent": [
        dab(25, 18, 3.5, 3.8),
        r([(25, 22, .1), (21, 36, .75), (24, 51, .08)], 2.3, "grandparent-body"),
        r([(23, 31, .1), (17, 42, .75), (13, 55, .08)], 1.3, "grandparent-staff", "#77746a", dry=True),
        dab(49, 35, 2.7, 2.9, "#77746a"),
        r([(49, 39, .1), (48, 48, .75), (50, 57, .08)], 1.4, "grandparent-child"),
        r([(25, 33, .1), (35, 37, .75), (47, 39, .08)], 1.2, "grandparent-reach"),
        ground("grandparent"),
    ],
    "group": figure("group-a", 14, 28, .68) + figure("group-b", 30, 21, .78, "#4a4943") + figure("group-c", 46, 23, .75, "#77746a") + figure("group-d", 56, 29, .62, "#bcb9af") + [
        r([(8, 63, .1), (29, 60, .85), (63, 62, .08)], .65, "group-ground", "#77746a", dry=True),
    ],
    "help": [
        dab(23, 18, 3.4, 3.7),
        r([(23, 22, .1), (22, 36, .75), (28, 49, .08)], 2.3, "help-standing"),
        dab(50, 42, 2.8, 3.0, "#77746a"),
        r([(49, 46, .1), (43, 52, .75), (38, 59, .08)], 1.4, "help-rising", "#77746a"),
        r([(23, 31, .1), (34, 35, .75), (47, 43, .08)], 1.7, "help-pull"),
        r([(48, 51, .1), (56, 55, .75), (63, 54, .08)], .7, "help-foot", "#bcb9af", dry=True),
        ground("help"),
    ],
    "humility": [
        dab(25, 30, 3.3, 3.5),
        r([(25, 34, .1), (31, 42, .75), (41, 44, .08)], 2.0, "humility-bow"),
        r([(25, 39, .1), (18, 48, .75), (14, 57, .08)], 1.2, "humility-kneel"),
        r([(40, 45, .1), (47, 51, .75), (57, 51, .08)], .8, "humility-hands", "#77746a", dry=True),
        m("M 51 47 C 54 43 61 43 64 47 C 61 52 55 53 51 47 Z", "#4a4943"),
        r([(9, 63, .1), (30, 60, .85), (61, 62, .08)], .65, "humility-ground", "#bcb9af", dry=True),
    ],
    "invite": figure("invite-host", 21, 20, .9) + [
        r([(21, 33, .1), (34, 27, .75), (47, 28, .08)], 1.6, "invite-open-arm"),
        r([(51, 58, .1), (51, 39, .75), (53, 20, .08)], 2.0, "invite-door-a"),
        r([(53, 20, .1), (62, 28, .75), (64, 43, .08)], 1.0, "invite-door-b", "#77746a", dry=True),
        r([(44, 61, .1), (54, 58, .75), (64, 60, .08)], .7, "invite-threshold", "#bcb9af", dry=True),
        ground("invite"),
    ],
    "kindness": figure("kindness-giver", 22, 21, .9) + figure("kindness-receiver", 52, 27, .72, "#77746a") + [
        r([(22, 34, .1), (33, 39, .75), (45, 36, .08)], 1.3, "kindness-offer"),
        r([(41, 36, .1), (42, 27, .75), (43, 20, .08)], .9, "kindness-stem", "#77746a", dry=True),
        m("M 42 22 C 36 17 33 12 36 9 C 42 10 45 15 43 21 Z", "#4a4943"),
        m("M 44 21 C 49 15 55 14 57 18 C 54 24 49 26 44 23 Z", "#77746a"),
        ground("kindness"),
    ],
    "neighbor": figure("neighbor-a", 20, 29, .78) + figure("neighbor-b", 52, 29, .78, "#77746a") + [
        r([(7, 28, .1), (19, 17, .8), (31, 28, .08)], 1.7, "neighbor-roof-a"),
        r([(40, 29, .1), (52, 18, .8), (64, 29, .08)], 1.1, "neighbor-roof-b", "#77746a", dry=True),
        r([(28, 45, .1), (36, 40, .75), (44, 45, .08)], .8, "neighbor-wave", "#bcb9af", dry=True),
        ground("neighbor"),
    ],
    "offering": [
        dab(23, 30, 3.2, 3.4),
        r([(23, 34, .1), (29, 43, .75), (39, 47, .08)], 2.0, "offering-bow"),
        r([(23, 39, .1), (17, 49, .75), (14, 58, .08)], 1.1, "offering-kneel"),
        r([(38, 47, .1), (47, 50, .75), (57, 47, .08)], 1.0, "offering-hands"),
        r([(44, 48, .1), (48, 56, .75), (58, 59, .9), (65, 54, .08)], 1.5, "offering-bowl"),
        r([(45, 47, .1), (55, 44, .8), (65, 47, .08)], .8, "offering-rim", "#77746a", dry=True),
        ground("offering"),
    ],
    "orphan": [
        dab(35, 30, 3.0, 3.2),
        r([(35, 34, .1), (34, 45, .75), (36, 56, .08)], 1.8, "orphan-body"),
        r([(36, 45, .1), (29, 54, .75), (24, 59, .08)], .9, "orphan-leg-a"),
        r([(36, 45, .1), (44, 53, .75), (50, 58, .08)], .65, "orphan-leg-b", "#77746a", dry=True),
        r([(14, 25, .1), (22, 15, .75), (34, 11, .9), (47, 15, .75), (58, 25, .08)], .8, "orphan-distant-shelter", "#bcb9af", dry=True),
        ground("orphan"),
    ],
    "peace": figure("peace-a", 21, 24, .82) + figure("peace-b", 52, 24, .82, "#77746a") + [
        r([(21, 37, .1), (32, 42, .75), (44, 38, .08)], 1.2, "peace-hands"),
        r([(36, 39, .1), (36, 28, .75), (38, 18, .08)], .9, "peace-stem", "#77746a", dry=True),
        m("M 37 24 C 30 18 22 18 18 22 C 23 29 30 31 37 27 Z", "#4a4943"),
        m("M 39 22 C 45 16 54 15 58 20 C 53 27 46 29 39 26 Z", "#77746a"),
        ground("peace"),
    ],
    "promise": figure("promise-a", 21, 23, .84) + figure("promise-b", 52, 23, .84, "#77746a") + [
        r([(21, 35, .1), (32, 39, .75), (42, 37, .08)], 1.4, "promise-hand-a"),
        r([(52, 35, .1), (43, 39, .75), (34, 37, .08)], .9, "promise-hand-b", "#77746a", dry=True),
        r([(29, 15, .1), (35, 10, .75), (42, 15, .9), (42, 22, .75), (35, 25, .9), (29, 21, .75), (29, 15, .08)], .8, "promise-ring", "#bcb9af", dry=True),
        ground("promise"),
    ],
    "protection": [
        r([(14, 21, .1), (35, 14, .9), (58, 22, .08)], 2.2, "protection-shield-top"),
        r([(14, 21, .1), (16, 40, .75), (25, 55, .9), (36, 63, .08)], 1.7, "protection-shield-left"),
        r([(58, 22, .1), (56, 40, .75), (47, 55, .9), (36, 63, .08)], 1.0, "protection-shield-right", "#77746a", dry=True),
        dab(36, 31, 3.2, 3.5),
        r([(36, 35, .1), (35, 44, .75), (37, 53, .08)], 1.8, "protection-person"),
        r([(29, 54, .1), (36, 51, .75), (44, 54, .08)], .65, "protection-base", "#bcb9af", dry=True),
    ],
    "share": figure("share-a", 20, 23, .84) + figure("share-b", 52, 23, .84, "#77746a") + [
        r([(20, 36, .1), (30, 41, .75), (36, 40, .08)], 1.3, "share-arm-a"),
        r([(52, 36, .1), (43, 41, .75), (36, 40, .08)], .9, "share-arm-b", "#77746a", dry=True),
        r([(28, 40, .1), (31, 50, .75), (40, 54, .9), (48, 49, .08)], 1.6, "share-bowl"),
        r([(28, 39, .1), (37, 36, .8), (49, 39, .08)], .8, "share-rim", "#bcb9af", dry=True),
        ground("share"),
    ],
    "team": figure("team-a", 16, 27, .75) + figure("team-b", 36, 20, .85, "#4a4943") + figure("team-c", 56, 27, .75, "#77746a") + [
        r([(16, 39, .1), (26, 34, .75), (36, 34, .08)], 1.2, "team-link-a"),
        r([(36, 34, .1), (46, 34, .75), (56, 39, .08)], .8, "team-link-b", "#77746a", dry=True),
        ground("team"),
    ],
    "trade": figure("trade-a", 18, 25, .78) + figure("trade-b", 54, 25, .78, "#77746a") + [
        r([(18, 37, .1), (28, 41, .75), (36, 39, .08)], 1.2, "trade-offer-a"),
        r([(54, 37, .1), (45, 42, .75), (36, 39, .08)], .8, "trade-offer-b", "#77746a", dry=True),
        m("M 29 36 C 31 31 39 29 44 34 C 43 40 35 43 29 36 Z", "#4a4943"),
        dab(46, 29, 2.3, 2.3, "#77746a"),
        ground("trade"),
    ],
    "treaty": figure("treaty-a", 19, 23, .8) + figure("treaty-b", 54, 23, .8, "#77746a") + [
        r([(19, 36, .1), (29, 39, .75), (36, 37, .08)], 1.2, "treaty-hand-a"),
        r([(54, 36, .1), (45, 39, .75), (36, 37, .08)], .8, "treaty-hand-b", "#77746a", dry=True),
        r([(29, 44, .1), (36, 41, .8), (44, 44, .08)], 1.5, "treaty-scroll-top"),
        r([(30, 45, .1), (31, 55, .75), (33, 59, .08)], .75, "treaty-scroll-left", "#bcb9af", dry=True),
        r([(43, 44, .1), (42, 54, .75), (40, 59, .08)], .7, "treaty-scroll-right", "#77746a", dry=True),
        ground("treaty"),
    ],
    "tribe": figure("tribe-a", 17, 30, .7) + figure("tribe-b", 35, 23, .8, "#4a4943") + figure("tribe-c", 54, 30, .7, "#77746a") + [
        r([(8, 28, .1), (20, 17, .75), (35, 10, .9), (51, 18, .75), (64, 29, .08)], 2.0, "tribe-canopy"),
        r([(17, 50, .1), (35, 45, .85), (54, 50, .08)], .75, "tribe-hearth", "#bcb9af", dry=True),
        ground("tribe"),
    ],
    "trust": [
        dab(20, 23, 3.2, 3.5),
        r([(20, 27, .1), (29, 36, .75), (42, 43, .08)], 2.2, "trust-lean"),
        r([(20, 33, .1), (13, 43, .75), (9, 52, .08)], 1.1, "trust-leg"),
        dab(52, 27, 3.2, 3.5, "#77746a"),
        r([(52, 31, .1), (49, 43, .75), (45, 56, .08)], 1.8, "trust-catcher", "#77746a"),
        r([(52, 38, .1), (45, 41, .75), (39, 43, .08)], 1.4, "trust-catch"),
        ground("trust"),
    ],
    "welcome": [
        dab(35, 22, 3.5, 3.8),
        r([(35, 26, .1), (34, 40, .75), (36, 55, .08)], 2.3, "welcome-body"),
        r([(34, 34, .1), (23, 27, .75), (12, 29, .08)], 1.5, "welcome-arm-a"),
        r([(36, 34, .1), (48, 27, .75), (61, 29, .08)], 1.0, "welcome-arm-b", "#77746a", dry=True),
        r([(12, 18, .1), (35, 10, .9), (62, 19, .08)], 1.4, "welcome-doorway"),
        r([(8, 63, .1), (29, 60, .85), (62, 62, .08)], .65, "welcome-ground", "#bcb9af", dry=True),
    ],
}


for glyph_name, glyph_marks in GLYPHS.items():
    write(glyph_name, glyph_marks)

print(f"redrew {len(GLYPHS)} relationship/community people glyphs as sumi-e studies")
