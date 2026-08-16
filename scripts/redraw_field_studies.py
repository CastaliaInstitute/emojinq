#!/usr/bin/env python3
"""Author the weakest field-study PUA families as recognizable sumi-e plates.

The earlier family generators began with broad icon-like body masses.  This
pass starts with a gesture and anatomy instead: a pressure-shaped contour,
one or two restrained wash ribbons, and only the marks needed to identify the
species.  Everything remains portable SVG so the same source can be animated,
outlined into the TTF, or exported for bamboo engraving.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
INK = "#262522"
CHARCOAL = "#4a4943"
WASH = "#77746a"
PALE = "#bcb9af"


def ribbon(points, width, seed, color=INK, dry=False):
    d = stroke_path(
        [BrushPoint(*point) for point in points],
        width=width,
        seed=f"field-{seed}",
        wobble=.22 if dry else .16,
        taper_start=.07,
        taper_end=.18,
    )
    cls = "ink-dry" if dry else "ink-wash"
    pass_name = "dry-fragment-v1" if dry else "loaded-ribbon-v2"
    return f'<path class="{cls}" d="{d}" fill="{color}" data-ink-brush-pass="{pass_name}"/>'


def line(d, width=1.1, color=INK, dry=False):
    cls = "ink-dry" if dry else "ink-stroke"
    pass_name = "dry-edge-v1" if dry else "contour-v2"
    # A sub-unit stroke disappears in the bamboo export and is too faint at
    # glyph scale. Keep the authored variation, but never emit a laser-fragile
    # line.
    width = max(1.0, width)
    return (
        f'<path class="{cls}" d="{d}" fill="none" stroke="{color}" '
        f'stroke-width="{width:.2f}" stroke-linecap="round" stroke-linejoin="round" '
        f'pathLength="1" data-ink-brush-pass="{pass_name}"/>'
    )


def contour(points, width=1.7, seed="contour", color=INK):
    return ribbon(points, width, seed, color)


def wash(points, width, seed, color=WASH):
    return ribbon(points, width, seed, color)


def root_for(category, name):
    path = ROOT / "assets" / "pua" / category / f"{name}.svg"
    source = path.read_text()
    match = re.search(r'data-pua="([^"]+)"', source)
    if not match:
        raise ValueError(f"missing PUA code point in {path}")
    pua = match.group(1)
    label = f"{category} / {name}"
    return path, pua, label


def write(category, name, marks):
    path, pua, label = root_for(category, name)
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" data-pua="{pua}" '
        'data-castalia-style="sumi-e-naturalist-v2" '
        'data-ink-stroke-system="filled-brush-mass-v2" '
        'data-ink-animation="wash-v1" data-ink-path-units="normalized" '
        'data-naturalist-construction="gesture-anatomy-v2">\n'
        f'<title>{label} — nineteenth-century naturalist sumi-e brush study</title>'
        + "".join(marks)
        + "</svg>\n"
    )
    path.write_text(svg)


def animal_studies():
    A = {}
    A["calf"] = [
        contour([(10, 32, .10), (16, 28, .60), (25, 27, .92), (36, 25, 1.0), (48, 28, .82), (57, 35, .25)], 2.7, "calf-back"),
        contour([(10, 32, .08), (7, 29, .76), (11, 27, .75), (17, 29, .28)], 2.2, "calf-head", CHARCOAL),
        ribbon([(17, 31, .12), (24, 35, .70), (34, 36, .92), (47, 34, .62), (56, 35, .10)], 3.4, "calf-rib", WASH),
        contour([(19, 34, .08), (18, 45, .70), (17, 56, .08)], 1.6, "calf-leg-a"),
        contour([(30, 34, .08), (31, 46, .70), (30, 57, .08)], 1.5, "calf-leg-b"),
        contour([(44, 33, .08), (46, 44, .70), (45, 56, .08)], 1.5, "calf-leg-c", CHARCOAL),
        line("M 56,35 Q 62,31 63,27 Q 63,25 61,24", 1.3, CHARCOAL),
        line("M 9,28 Q 6,25 8,23", 1.1), line("M 14,28 Q 15,24 18,23", 1.1),
        line("M 11,30 Q 12,31 13,30", .85),
    ]
    A["colony"] = []
    for i, (x, y, s) in enumerate(((17, 37, 1.0), (36, 29, .92), (54, 39, .78))):
        A["colony"] += [
            contour([(x-5*s, y, .08), (x-2*s, y-4*s, .72), (x+3*s, y-4*s, .92), (x+6*s, y, .08)], 1.6*s, f"colony-body-{i}"),
            line(f"M {x-1*s:.1f},{y-3*s:.1f} Q {x+1*s:.1f},{y-7*s:.1f} {x+4*s:.1f},{y-8*s:.1f}", 1.0*s, CHARCOAL),
            line(f"M {x-2*s:.1f},{y-2*s:.1f} Q {x-7*s:.1f},{y-6*s:.1f} {x-8*s:.1f},{y-2*s:.1f}", .95*s, PALE),
            line(f"M {x+2*s:.1f},{y-2*s:.1f} Q {x+7*s:.1f},{y-6*s:.1f} {x+8*s:.1f},{y-2*s:.1f}", .95*s, PALE),
            line(f"M {x-3*s:.1f},{y-1*s:.1f} Q {x:.1f},{y+1*s:.1f} {x+4*s:.1f},{y-1*s:.1f}", .65*s, INK, True),
        ]
    A["flock"] = [
        contour([(5, 34, .08), (10, 29, .68), (17, 30, .88), (23, 34, .08)], 1.6, "flock-a"),
        contour([(26, 25, .08), (32, 20, .68), (39, 21, .88), (45, 25, .08)], 1.6, "flock-b", CHARCOAL),
        contour([(47, 38, .08), (53, 33, .68), (60, 34, .88), (67, 38, .08)], 1.55, "flock-c", WASH),
        line("M 12,30 Q 10,24 12,18 Q 16,25 18,30", 1.4),
        line("M 33,21 Q 31,15 34,9 Q 37,16 38,21", 1.35, CHARCOAL),
        line("M 54,34 Q 54,27 59,21 Q 59,29 58,34", 1.35, WASH),
        line("M 5,34 L 2,33", .85), line("M 45,25 L 48,24", .85, CHARCOAL),
    ]
    A["herd"] = [
        contour([(7, 39, .08), (12, 34, .7), (20, 34, .9), (27, 40, .08)], 2.2, "herd-a", WASH),
        contour([(25, 37, .08), (31, 31, .7), (40, 32, .92), (49, 39, .08)], 2.5, "herd-b", CHARCOAL),
        contour([(46, 40, .08), (53, 35, .7), (61, 37, .08)], 1.8, "herd-c", PALE),
        line("M 11,36 Q 8,31 10,28 M 16,35 Q 19,30 21,29", 1.0),
        line("M 31,33 Q 28,28 30,25 M 36,32 Q 39,27 41,27", 1.0, CHARCOAL),
        line("M 14,41 L 13,56 M 21,41 L 22,57 M 34,40 L 34,56 M 42,40 L 44,56", 1.25),
        line("M 7,39 L 4,37 M 60,37 Q 65,34 66,30", 1.1, CHARCOAL),
    ]
    A["lamb"] = [
        contour([(13, 39, .08), (17, 32, .62), (24, 28, .82), (33, 29, .88), (42, 32, .70), (49, 38, .08)], 2.5, "lamb-wool", PALE),
        contour([(46, 36, .08), (52, 34, .72), (59, 37, .08)], 1.8, "lamb-head", CHARCOAL),
        ribbon([(18, 38, .08), (25, 41, .72), (35, 42, .9), (45, 39, .08)], 2.8, "lamb-shadow", WASH),
        line("M 18,35 Q 23,31 29,32 M 25,29 Q 29,25 33,29 M 34,30 Q 38,27 42,32", .75, INK, True),
        line("M 20,42 L 19,56 M 31,42 L 31,57 M 42,40 L 44,56", 1.35),
        line("M 57,35 Q 60,32 61,29", 1.0),
    ]
    A["migration"] = [
        contour([(7, 35, .08), (12, 30, .68), (18, 31, .86), (24, 35, .08)], 1.45, "migration-a"),
        contour([(27, 27, .08), (32, 22, .68), (38, 23, .86), (44, 27, .08)], 1.5, "migration-b", CHARCOAL),
        contour([(49, 35, .08), (55, 29, .68), (62, 30, .86), (68, 35, .08)], 1.45, "migration-c", WASH),
        line("M 13,30 Q 11,23 14,17 Q 18,24 18,31", 1.2),
        line("M 33,22 Q 31,15 34,9 Q 38,16 38,23", 1.2, CHARCOAL),
        line("M 55,29 Q 54,22 58,17 Q 61,24 61,30", 1.2, WASH),
    ]
    A["pack"] = [
        contour([(7, 39, .08), (14, 34, .64), (23, 35, .9), (31, 40, .08)], 2.3, "pack-a", CHARCOAL),
        contour([(24, 38, .08), (31, 32, .68), (40, 33, .9), (49, 40, .08)], 2.2, "pack-b", WASH),
        contour([(45, 42, .08), (52, 37, .68), (60, 39, .08)], 1.8, "pack-c", PALE),
        line("M 11,35 L 10,29 L 14,33 M 17,34 L 20,28 L 23,35", 1.1),
        line("M 29,33 L 29,28 L 34,32 M 35,32 L 38,27 L 41,34", 1.0, CHARCOAL),
        line("M 12,40 L 11,54 M 20,40 L 21,55 M 31,39 L 31,54 M 40,39 L 42,54", 1.2),
        line("M 49,40 Q 58,47 65,44", 1.1, CHARCOAL),
    ]
    A["predator"] = [
        contour([(9, 38, .08), (17, 31, .68), (28, 29, .92), (40, 32, .78), (53, 38, .08)], 2.8, "predator-body", CHARCOAL),
        contour([(16, 32, .08), (11, 27, .72), (6, 28, .1)], 2.0, "predator-muzzle"),
        line("M 12,27 L 13,22 L 17,26 M 17,29 Q 21,25 24,26", 1.2),
        line("M 24,32 Q 31,28 37,32", .9, PALE, True),
        line("M 22,38 L 20,52 L 17,57 M 39,37 L 42,49 L 46,55", 1.55),
        line("M 49,35 Q 59,40 64,35 Q 65,32 63,30", 1.25, CHARCOAL),
    ]
    A["prey"] = [
        contour([(17, 42, .08), (24, 35, .65), (34, 33, .92), (43, 37, .82), (51, 44, .08)], 2.5, "prey-body", WASH),
        contour([(25, 35, .08), (23, 27, .65), (25, 18, .08)], 1.7, "prey-ear-a"),
        contour([(31, 34, .08), (34, 26, .65), (40, 21, .08)], 1.7, "prey-ear-b", CHARCOAL),
        contour([(20, 37, .08), (15, 35, .7), (11, 33, .08)], 1.5, "prey-muzzle", CHARCOAL),
        line("M 24,42 L 22,54 M 40,43 L 46,54 M 32,34 Q 37,37 42,39", 1.25),
        line("M 44,39 Q 53,34 57,38", 1.0, PALE),
    ]
    A["squirrel"] = [
        contour([(26, 43, .08), (29, 35, .64), (36, 32, .92), (44, 35, .86), (49, 43, .08)], 2.5, "squirrel-body", WASH),
        contour([(29, 35, .08), (24, 31, .72), (19, 32, .08)], 1.8, "squirrel-head", CHARCOAL),
        contour([(25, 31, .08), (25, 24, .68), (29, 19, .08)], 1.35, "squirrel-ear"),
        contour([(44, 43, .08), (51, 37, .64), (56, 29, .82), (55, 20, .70), (50, 14, .08)], 3.2, "squirrel-tail", CHARCOAL),
        line("M 31,35 Q 34,39 39,38 M 32,32 Q 37,29 42,33", .8, PALE, True),
        line("M 29,42 L 25,52 M 42,43 L 48,53 M 28,37 Q 23,40 20,44", 1.2),
        line("M 24,31 Q 25,29 27,30", .85),
    ]
    for name, marks in A.items():
        write("animals", name, marks)


def dinosaur_studies():
    D = {}
    D["ankylosaurus"] = [
        contour([(7, 42, .08), (15, 35, .68), (29, 32, .9), (43, 34, .84), (56, 41, .5), (64, 43, .08)], 2.8, "anky-body", CHARCOAL),
        contour([(50, 40, .08), (61, 38, .72), (67, 34, .08)], 1.8, "anky-tail"),
        line("M 11,35 L 13,30 L 17,34 M 18,33 L 20,28 L 24,32 M 27,32 L 30,27 L 34,31 M 37,33 L 40,29 L 44,33", 1.2, CHARCOAL),
        line("M 17,42 L 16,54 L 13,58 M 30,40 L 29,54 L 27,58 M 45,40 L 47,53 L 50,56", 1.5),
        line("M 18,36 Q 30,33 43,36", .8, PALE, True),
    ]
    D["brachiosaurus"] = [
        contour([(10, 48, .08), (20, 43, .68), (34, 43, .9), (46, 47, .08)], 2.5, "brachio-body", WASH),
        contour([(39, 45, .08), (42, 35, .65), (42, 24, .78), (45, 14, .72), (49, 9, .08)], 2.4, "brachio-neck", CHARCOAL),
        contour([(47, 10, .08), (52, 8, .7), (57, 10, .08)], 1.5, "brachio-head"),
        line("M 14,48 L 13,57 M 24,46 L 23,57 M 37,46 L 38,56", 1.45),
        line("M 46,13 Q 50,12 53,13 M 48,10 L 50,8", .8, PALE),
        line("M 10,47 Q 5,44 3,40", 1.3, CHARCOAL),
    ]
    D["fossil"] = [
        contour([(10, 15, .08), (20, 11, .72), (36, 12, .92), (53, 16, .8), (62, 25, .08)], 1.9, "fossil-slab", PALE),
        line("M 18,37 Q 25,29 34,29 Q 44,29 54,38", 1.25, CHARCOAL),
        line("M 28,30 Q 30,24 28,19 M 34,29 Q 38,23 42,18 M 41,30 Q 47,26 52,22", 1.0),
        line("M 22,34 L 16,29 M 48,34 L 57,29 M 32,30 L 30,39 M 39,30 L 42,39", .9, WASH),
        line("M 11,45 Q 27,48 44,46 Q 56,44 63,47", .75, PALE, True),
    ]
    D["parasaurolophus"] = [
        contour([(10, 42, .08), (20, 36, .68), (34, 35, .9), (47, 39, .72), (61, 43, .08)], 2.4, "para-body", WASH),
        contour([(18, 37, .08), (15, 30, .62), (17, 21, .08)], 1.6, "para-neck"),
        contour([(16, 24, .08), (22, 22, .68), (29, 17, .9), (42, 18, .08)], 1.6, "para-crest", CHARCOAL),
        line("M 18,37 Q 12,34 8,35 M 28,36 Q 30,31 35,30", 1.0),
        line("M 23,42 L 21,55 M 38,41 L 39,55 M 48,40 L 51,54", 1.45),
        line("M 28,35 Q 39,32 49,36", .8, PALE, True),
    ]
    D["pteranodon"] = [
        contour([(36, 38, .08), (30, 32, .68), (24, 25, .8), (14, 17, .08)], 2.0, "ptero-wing-a", CHARCOAL),
        contour([(39, 37, .08), (47, 30, .7), (57, 21, .88), (68, 17, .08)], 2.0, "ptero-wing-b", CHARCOAL),
        contour([(34, 37, .08), (39, 34, .68), (47, 35, .08)], 2.0, "ptero-body", WASH),
        line("M 43,35 Q 51,31 58,29 M 31,33 Q 25,29 20,24", .85, PALE, True),
        line("M 38,34 L 36,27 L 39,23 M 40,35 L 44,28", 1.0),
        line("M 47,35 L 52,39 L 55,43", 1.2),
    ]
    D["spinosaurus"] = [
        contour([(7, 42, .08), (17, 36, .68), (30, 35, .9), (43, 38, .78), (58, 43, .08)], 2.5, "spino-body", CHARCOAL),
        contour([(29, 35, .08), (30, 28, .62), (34, 20, .78), (40, 14, .08)], 2.0, "spino-sail", WASH),
        line("M 34,34 Q 35,27 40,22 Q 47,26 49,37", .85, PALE, True),
        line("M 12,38 L 9,34 M 19,36 L 17,31 M 25,35 L 25,30", 1.0),
        line("M 17,42 L 15,55 M 32,41 L 31,55 M 45,41 L 48,54", 1.45),
    ]
    D["stegosaurus"] = [
        contour([(7, 42, .08), (16, 34, .68), (29, 32, .9), (42, 35, .82), (53, 42, .08)], 2.7, "stego-body", WASH),
        contour([(47, 40, .08), (58, 38, .65), (67, 33, .08)], 1.7, "stego-tail"),
        line("M 13,35 L 14,29 L 18,33 M 19,33 L 21,25 L 26,31 M 27,32 L 30,23 L 35,31 M 36,33 L 40,25 L 44,34 M 45,37 L 49,31 L 52,39", 1.25, CHARCOAL),
        line("M 17,42 L 16,55 M 30,40 L 29,55 M 42,40 L 44,55", 1.45),
    ]
    D["triceratops"] = [
        contour([(13, 41, .08), (23, 34, .68), (36, 33, .9), (48, 38, .7), (59, 42, .08)], 2.6, "trice-body", CHARCOAL),
        contour([(14, 36, .08), (8, 34, .72), (5, 30, .08)], 1.9, "trice-head"),
        line("M 9,32 L 7,24 M 13,33 L 14,25 M 8,34 Q 13,37 19,34", 1.5, CHARCOAL),
        line("M 12,40 L 11,54 M 26,39 L 25,55 M 43,39 L 45,54", 1.45),
        line("M 23,35 Q 34,31 45,35", .8, PALE, True),
    ]
    D["tyrannosaurus"] = [
        contour([(18, 42, .08), (26, 35, .65), (37, 34, .9), (49, 38, .72), (63, 43, .08)], 2.6, "tyrant-body", WASH),
        contour([(20, 37, .08), (14, 33, .64), (10, 29, .08)], 2.0, "tyrant-head", CHARCOAL),
        line("M 11,29 L 9,24 L 14,27 M 14,33 Q 20,30 25,32", 1.2),
        line("M 31,37 L 27,44 L 31,43 M 35,38 L 32,45 L 36,43", 1.0),
        line("M 26,42 L 24,54 M 43,41 L 47,54", 1.55),
        line("M 20,36 Q 34,32 47,37", .8, PALE, True),
    ]
    D["velociraptor"] = [
        contour([(14, 43, .08), (23, 37, .68), (33, 36, .9), (43, 39, .76), (56, 43, .08)], 2.1, "velo-body", CHARCOAL),
        contour([(17, 38, .08), (11, 33, .72), (7, 30, .08)], 1.6, "velo-head"),
        line("M 13,33 L 12,27 L 16,31 M 24,37 Q 28,31 31,27", 1.0),
        line("M 23,42 L 17,51 L 12,54 M 34,41 L 39,50 L 47,52", 1.6),
        line("M 28,39 L 31,46 L 35,44", 1.0, WASH),
        line("M 22,36 Q 34,33 45,37", .75, PALE, True),
    ]
    for name, marks in D.items():
        write("dinosaurs", name, marks)


def sea_studies():
    S = {}
    S["coral"] = [
        contour([(35, 61, .08), (35, 50, .72), (30, 41, .9), (25, 31, .08)], 2.0, "coral-main", CHARCOAL),
        contour([(31, 45, .08), (23, 39, .68), (17, 32, .08)], 1.45, "coral-left"),
        contour([(33, 42, .08), (40, 34, .7), (45, 24, .08)], 1.5, "coral-right", WASH),
        line("M 25,31 L 21,26 M 25,31 L 28,24 M 17,32 L 13,28 M 45,24 L 45,18 M 40,34 L 44,29", 1.1),
        line("M 35,49 Q 42,44 48,40", .75, PALE, True),
    ]
    S["crab"] = [
        contour([(15, 43, .08), (23, 36, .68), (34, 34, .9), (46, 36, .78), (56, 43, .08)], 2.4, "crab-shell", CHARCOAL),
        contour([(14, 39, .08), (7, 32, .65), (3, 35, .08)], 2.0, "crab-claw-a"),
        contour([(56, 39, .08), (64, 32, .65), (69, 35, .08)], 2.0, "crab-claw-b"),
        line("M 18,43 L 11,50 L 8,55 M 23,45 L 19,53 L 18,58 M 46,44 L 52,52 L 55,57 M 51,43 L 60,49 L 64,54", 1.35),
        line("M 23,37 Q 34,41 47,37 M 29,35 L 29,31 M 39,35 L 40,31", .85, PALE),
        line("M 27,31 L 25,27 M 41,31 L 43,27", 1.0, CHARCOAL),
    ]
    S["dolphin"] = [
        contour([(7, 42, .08), (16, 36, .65), (26, 34, .9), (37, 36, .82), (48, 41, .68), (61, 44, .08)], 2.1, "dolphin-body", WASH),
        contour([(26, 35, .08), (31, 27, .68), (40, 24, .08)], 1.5, "dolphin-dorsal"),
        contour([(41, 39, .08), (47, 47, .68), (54, 48, .08)], 1.35, "dolphin-flipper"),
        line("M 12,40 L 6,37 L 2,38 M 27,35 Q 35,31 44,36", 1.0, CHARCOAL),
        line("M 18,39 Q 28,37 39,39", .75, PALE, True),
    ]
    S["jellyfish"] = [
        contour([(13, 33, .08), (18, 27, .68), (27, 24, .9), (38, 25, .9), (48, 29, .7), (53, 34, .08)], 2.1, "jelly-bell", WASH),
        contour([(14, 34, .08), (23, 37, .7), (32, 34, .82), (42, 37, .7), (52, 34, .08)], 1.5, "jelly-lip", CHARCOAL),
        line("M 19,37 Q 17,48 19,59 M 27,36 Q 25,48 27,62 M 35,36 Q 36,50 34,61 M 43,36 Q 47,48 45,59", 1.25),
        line("M 23,28 Q 31,25 40,29", .75, PALE, True),
    ]
    S["lobster"] = [
        contour([(16, 43, .08), (23, 36, .68), (34, 35, .9), (46, 38, .78), (56, 43, .08)], 2.2, "lobster-body", CHARCOAL),
        contour([(17, 40, .08), (9, 34, .68), (4, 29, .08)], 2.0, "lobster-claw-a"),
        contour([(54, 40, .08), (63, 34, .68), (68, 29, .08)], 2.0, "lobster-claw-b"),
        line("M 24,39 Q 30,42 36,38 Q 43,42 49,39", .9, PALE),
        line("M 22,44 L 16,52 M 30,45 L 27,55 M 43,44 L 48,54 M 51,43 L 58,51", 1.25),
        line("M 25,35 L 27,30 M 34,35 L 35,29 M 43,37 L 44,31", .95),
    ]
    S["manta"] = [
        contour([(5, 43, .08), (17, 36, .66), (30, 36, .9), (42, 36, .68), (57, 43, .08)], 2.6, "manta-wings", CHARCOAL),
        contour([(28, 38, .08), (34, 43, .7), (36, 55, .08)], 1.8, "manta-body", WASH),
        line("M 20,39 Q 31,42 44,39 M 32,45 Q 34,48 35,51", .8, PALE, True),
        line("M 6,43 Q 3,46 2,49 M 57,43 Q 62,46 65,49", 1.1),
    ]
    S["nautilus"] = [
        contour([(16, 46, .08), (19, 35, .66), (27, 27, .9), (38, 25, .82), (49, 29, .08)], 2.1, "nautilus-shell", PALE),
        line("M 45,31 Q 35,27 28,33 Q 21,39 28,45 Q 35,50 41,44 Q 46,39 40,35 Q 35,32 32,36", 1.65, CHARCOAL),
        line("M 31,36 Q 34,39 38,38", .8, WASH, True),
        line("M 44,45 Q 52,41 58,44 Q 62,47 66,44", 1.1, CHARCOAL),
    ]
    S["octopus"] = [
        contour([(21, 37, .08), (22, 29, .68), (29, 25, .9), (39, 25, .88), (47, 31, .08)], 2.2, "octopus-mantle", WASH),
        contour([(24, 39, .08), (19, 47, .62), (12, 50, .08)], 1.7, "octopus-arm-a"),
        contour([(29, 39, .08), (27, 50, .65), (23, 57, .08)], 1.65, "octopus-arm-b"),
        contour([(35, 39, .08), (37, 49, .65), (42, 56, .08)], 1.65, "octopus-arm-c"),
        contour([(41, 38, .08), (49, 46, .65), (57, 48, .08)], 1.7, "octopus-arm-d"),
        line("M 27,30 Q 34,27 42,31 M 30,25 Q 33,21 35,18", .8, PALE, True),
    ]
    S["seahorse"] = [
        contour([(37, 17, .08), (31, 22, .62), (32, 30, .8), (39, 34, .88), (39, 42, .62), (34, 49, .08)], 2.0, "seahorse-neck", CHARCOAL),
        contour([(36, 17, .08), (42, 13, .68), (49, 15, .08)], 1.45, "seahorse-head"),
        contour([(36, 42, .08), (29, 47, .65), (26, 54, .08)], 1.55, "seahorse-belly", WASH),
        line("M 37,22 Q 42,24 45,22 M 34,29 Q 39,31 43,29 M 35,36 Q 40,38 43,36", .85, PALE),
        line("M 41,15 Q 45,10 45,7", .9, CHARCOAL),
        line("M 34,49 Q 28,54 23,54", 1.0),
    ]
    S["shark"] = [
        contour([(5, 43, .08), (16, 36, .66), (29, 34, .9), (44, 37, .8), (59, 43, .08)], 2.4, "shark-body", CHARCOAL),
        contour([(31, 35, .08), (35, 26, .7), (39, 35, .08)], 1.7, "shark-dorsal"),
        contour([(43, 38, .08), (49, 31, .7), (55, 37, .08)], 1.25, "shark-tail"),
        line("M 8,41 L 2,38 M 17,37 Q 28,34 40,37 M 22,43 Q 31,46 41,42", .8, PALE, True),
        line("M 20,36 Q 21,40 20,44", .9, CHARCOAL),
    ]
    S["turtle"] = [
        contour([(12, 43, .08), (19, 35, .66), (31, 32, .9), (44, 35, .84), (54, 43, .08)], 2.7, "turtle-shell", WASH),
        contour([(22, 42, .08), (31, 36, .7), (42, 40, .08)], 1.35, "turtle-flank", CHARCOAL),
        line("M 22,35 Q 31,31 42,35 M 31,33 L 31,43 M 20,38 L 25,43 M 42,36 L 38,43", .85, PALE),
        contour([(16, 42, .08), (10, 47, .7), (7, 51, .08)], 1.5, "turtle-front"),
        contour([(46, 41, .08), (53, 47, .7), (57, 50, .08)], 1.5, "turtle-hind"),
        line("M 54,40 Q 61,37 65,40", 1.15, CHARCOAL),
    ]
    S["whale"] = [
        contour([(7, 43, .08), (16, 36, .64), (29, 33, .9), (42, 35, .82), (54, 40, .68), (63, 43, .08)], 2.8, "whale-body", CHARCOAL),
        contour([(42, 38, .08), (47, 46, .68), (54, 47, .08)], 1.6, "whale-flipper"),
        contour([(59, 42, .08), (65, 38, .72), (69, 35, .08)], 1.5, "whale-tail"),
        line("M 17,38 Q 28,34 40,37 M 21,43 Q 32,47 43,43", .8, PALE, True),
        line("M 11,41 Q 7,39 3,40 M 29,34 Q 30,29 28,26 Q 33,28 34,31", 1.05),
    ]
    for name, marks in S.items():
        write("sea_creatures", name, marks)


def adopt_semantic_sea_anchors():
    """Use already-brushed standard studies where the silhouette is decisive.

    Crab, dolphin, jellyfish, lobster, octopus, shark, turtle, and whale have
    stable Unicode counterparts in the generated corpus.  Reusing those
    vector contours gives the PUA concepts an anatomically legible starting
    point; the separate field-detail pass still adds the family-specific
    naturalist marks.  Manta, nautilus, and seahorse remain authored here
    because the standard corpus has no adequate semantic anchor.
    """
    anchors = {
        "crab": "1F980.svg",
        "dolphin": "1F42C.svg",
        "jellyfish": "1FABC.svg",
        "lobster": "1F99E.svg",
        "octopus": "1F419.svg",
        "shark": "1F988.svg",
        "turtle": "1F422.svg",
        "whale": "1F40B.svg",
    }
    for name, filename in anchors.items():
        target = ROOT / "assets" / "pua" / "sea_creatures" / f"{name}.svg"
        source = ROOT / "assets" / "gray-all" / filename
        if not source.exists() or not target.exists():
            continue
        pua = re.search(r'data-pua="([^"]+)"', target.read_text())
        if pua is None:
            continue
        root = ET.parse(source).getroot()
        root.set("viewBox", "0 0 72 72")
        root.set("role", "img")
        root.set("aria-label", f"sea creatures / {name}")
        root.set("data-pua", pua.group(1))
        root.set("data-ink-animation", "wash-v1")
        root.set("data-ink-path-units", "normalized")
        root.set("data-ink-coverage", "complete")
        root.set("data-naturalist-construction", "semantic-anchor-v1")
        root.set("data-field-anchor", "openmoji-brushed-standard")
        for child in list(root):
            if child.tag.rsplit("}", 1)[-1] == "title":
                root.remove(child)
        title = ET.Element("title")
        title.text = f"sea creatures / {name} — naturalist sumi-e brush study"
        root.insert(0, title)
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        ET.ElementTree(root).write(target, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", choices=("all", "animals", "dinosaurs", "sea"), default="all")
    parser.add_argument(
        "--semantic-anchors",
        action="store_true",
        help="replace supported authored sea studies with brushed OpenMoji anchors",
    )
    args = parser.parse_args()
    if args.category in {"all", "animals"}:
        animal_studies()
    if args.category in {"all", "dinosaurs"}:
        dinosaur_studies()
    if args.category in {"all", "sea"}:
        sea_studies()
        if args.semantic_anchors:
            adopt_semantic_sea_anchors()
    print(f"redrew {args.category} as anatomy-led sumi-e field studies")
