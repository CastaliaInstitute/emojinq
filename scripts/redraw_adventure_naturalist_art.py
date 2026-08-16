#!/usr/bin/env python3
"""Redraw the Colossal Cave adventure objects as compact sumi-e studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "adventure"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(
    values: list[tuple[float, float, float]],
    width: float,
    seed: str,
    color: str = "#262522",
    *,
    dry: bool = False,
) -> str:
    d = stroke_path(
        points(*values), width=width, seed=seed, wobble=.25,
        taper_start=.10, taper_end=.08,
    )
    class_name = "ink-dry" if dry else "ink-wash"
    brush_pass = "dry-edge-v2" if dry else "loaded-ribbon-v2"
    return (
        f'<path class="{class_name}" d="{d}" fill="{color}" '
        f'data-ink-brush-pass="{brush_pass}"/>'
    )


def mass(d: str, color: str = "#4a4943") -> str:
    return (
        f'<path class="ink-wash" d="{d}" fill="{color}" '
        'data-ink-brush-pass="loaded-mass-v2"/>'
    )


def dab(cx: float, cy: float, rx: float, ry: float, color: str = "#262522") -> str:
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="adventure / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>adventure / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


# The cave's black rod bears a star.  One loaded diagonal carries its weight;
# the dry echo and unequal rays make it feel potent rather than diagrammatic.
write("black-rod", [
    ribbon([(14, 58, .08), (25, 47, .68), (37, 34, 1.0), (49, 21, .82), (58, 12, .08)], 3.8, "rod-host"),
    ribbon([(18, 59, .10), (29, 48, .72), (41, 35, .84), (52, 23, .08)], .75, "rod-dry-edge", "#77746a", dry=True),
    ribbon([(57, 12, .10), (62, 7, .72), (65, 5, .08)], 1.3, "rod-star-ray-a", "#4a4943"),
    ribbon([(58, 12, .10), (64, 13, .72), (68, 15, .08)], .95, "rod-star-ray-b", "#77746a", dry=True),
    ribbon([(57, 12, .10), (57, 6, .72), (56, 3, .08)], .72, "rod-star-ray-c", "#bcb9af", dry=True),
])


# A handled cave lamp: open handle, loaded reservoir, short wick, and a pale
# glow gesture.  The body is deliberately not enclosed by a uniform contour.
write("brass-lamp", [
    ribbon([(25, 25, .10), (25, 16, .68), (31, 10, .92), (40, 11, .84), (47, 19, .72), (47, 26, .08)], 1.75, "lamp-handle"),
    ribbon([(25, 27, .10), (35, 25, .86), (47, 28, .08)], 2.6, "lamp-cap", "#262522"),
    ribbon([(27, 29, .10), (24, 39, .72), (25, 49, .08)], 1.35, "lamp-left-upright", "#4a4943"),
    ribbon([(45, 29, .10), (48, 39, .72), (47, 48, .08)], 1.0, "lamp-right-upright", "#77746a", dry=True),
    ribbon([(23, 50, .10), (34, 54, .96), (48, 50, .08)], 4.0, "lamp-reservoir", "#4a4943"),
    ribbon([(36, 47, .10), (34, 41, .72), (37, 35, .08)], 1.3, "lamp-flame", "#262522"),
    ribbon([(29, 34, .10), (35, 31, .72), (42, 34, .08)], .68, "lamp-glass-glint", "#bcb9af", dry=True),
])


# Facets are stated as separate pressure gestures.  A dark lower facet anchors
# the jewel while the incomplete dry perimeter keeps the paper inside it.
write("emerald", [
    ribbon([(36, 9, .08), (47, 17, .72), (57, 27, .08)], 2.1, "emerald-upper-right"),
    ribbon([(36, 9, .08), (26, 17, .72), (17, 29, .08)], 1.45, "emerald-upper-left", "#77746a", dry=True),
    ribbon([(17, 29, .08), (21, 44, .72), (35, 60, .08)], 2.0, "emerald-lower-left", "#4a4943"),
    ribbon([(57, 27, .08), (53, 44, .72), (35, 60, .08)], 1.35, "emerald-lower-right", "#77746a", dry=True),
    ribbon([(17, 29, .10), (35, 34, .94), (57, 27, .08)], 1.15, "emerald-shoulder"),
    ribbon([(36, 10, .10), (35, 34, .92), (35, 59, .08)], 1.25, "emerald-spine", "#4a4943"),
    mass("M 35 34 L 53 44 L 35 59 L 24 46 Z", "#bcb9af"),
    ribbon([(24, 19, .10), (35, 34, .72), (48, 17, .08)], .72, "emerald-dry-facet", "#77746a", dry=True),
])


# Gold is conveyed by a dense, irregular loaded stone and glancing dry planes,
# not by literal colour or a coin symbol.
write("gold-nugget", [
    mass("M 17 43 C 14 35 21 27 29 27 C 33 19 44 21 47 27 C 56 26 61 34 57 42 C 55 50 45 54 37 51 C 29 57 19 53 17 43 Z", "#4a4943"),
    ribbon([(21, 39, .10), (29, 32, .72), (38, 31, .92), (48, 34, .08)], 1.0, "nugget-plane-a", "#dedbd4", dry=True),
    ribbon([(25, 47, .10), (35, 44, .72), (46, 46, .08)], .85, "nugget-plane-b", "#bcb9af", dry=True),
    ribbon([(36, 25, .10), (40, 31, .72), (39, 37, .08)], .72, "nugget-cleft", "#262522"),
    ribbon([(52, 32, .10), (56, 37, .72), (53, 43, .08)], .65, "nugget-edge", "#77746a", dry=True),
])


# Two keys cross at different angles.  Their bows remain open loops and their
# teeth are short lifted accents, so the pair survives without a solid badge.
write("keys", [
    ribbon([(19, 15, .08), (27, 13, .72), (33, 19, .94), (31, 27, .82), (24, 31, .94), (17, 27, .72), (15, 20, .82), (19, 15, .08)], 1.8, "key-a-bow"),
    ribbon([(28, 27, .10), (37, 37, .72), (48, 48, .94), (58, 58, .08)], 2.2, "key-a-shaft"),
    ribbon([(48, 48, .10), (53, 43, .72), (56, 46, .08)], 1.15, "key-a-tooth-a"),
    ribbon([(53, 53, .10), (58, 49, .72), (61, 52, .08)], .85, "key-a-tooth-b", "#77746a", dry=True),
    ribbon([(48, 14, .08), (55, 17, .72), (57, 24, .90), (52, 30, .78), (45, 28, .90), (42, 21, .72), (48, 14, .08)], 1.3, "key-b-bow", "#77746a", dry=True),
    ribbon([(46, 28, .10), (38, 37, .72), (30, 47, .08)], 1.45, "key-b-shaft", "#4a4943"),
    ribbon([(34, 43, .10), (29, 39, .72), (26, 42, .08)], .72, "key-b-tooth", "#bcb9af", dry=True),
])


# The little bird is a perched living subject: a loaded back and breast, small
# head, lifted beak, tail flick, and only one fully stated leg.
write("little-bird", [
    ribbon([(20, 42, .10), (29, 34, .76), (40, 35, 1.0), (49, 42, .08)], 5.2, "bird-body", "#4a4943"),
    dab(48, 31, 4.0, 3.6, "#262522"),
    dab(49, 30, .72, .72, "#eeeeea"),
    ribbon([(51, 31, .10), (57, 29, .72), (62, 31, .08)], 1.25, "bird-beak"),
    ribbon([(22, 41, .10), (15, 37, .72), (10, 33, .08)], 2.0, "bird-tail-host", "#262522"),
    ribbon([(23, 43, .10), (15, 43, .72), (9, 46, .08)], 1.0, "bird-tail-dry", "#77746a", dry=True),
    ribbon([(32, 42, .10), (30, 50, .72), (28, 56, .08)], 1.15, "bird-leg"),
    ribbon([(27, 56, .10), (33, 56, .72), (38, 55, .08)], .72, "bird-perch", "#77746a", dry=True),
    ribbon([(30, 36, .10), (36, 39, .72), (42, 38, .08)], .65, "bird-wing-edge", "#bcb9af", dry=True),
])


# The silver chest is built from four unequal loaded boards and an arcing lid.
# A pale inner seam suggests metal sheen without filling the empty interior.
write("silver-chest", [
    ribbon([(14, 34, .10), (18, 24, .72), (28, 18, .94), (42, 18, .86), (54, 24, .72), (59, 34, .08)], 2.3, "chest-lid"),
    ribbon([(13, 35, .10), (27, 36, .72), (43, 35, .94), (59, 36, .08)], 2.1, "chest-lid-seam", "#4a4943"),
    ribbon([(14, 37, .10), (14, 48, .72), (15, 58, .08)], 1.8, "chest-left"),
    ribbon([(59, 37, .10), (58, 48, .72), (58, 57, .08)], 1.25, "chest-right", "#77746a", dry=True),
    ribbon([(15, 57, .10), (29, 58, .72), (44, 56, .94), (58, 57, .08)], 2.4, "chest-base", "#262522"),
    mass("M 32 34 C 35 32 40 33 42 36 L 41 45 C 38 48 33 46 31 43 Z", "#4a4943"),
    ribbon([(22, 41, .10), (31, 40, .72), (41, 41, .08)], .72, "chest-silver-glint", "#bcb9af", dry=True),
])


print("redrew all 7 adventure PUA glyphs as naturalist sumi-e object studies")
