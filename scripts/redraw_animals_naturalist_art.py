#!/usr/bin/env python3
"""Render the animal PUA family as small 19th-century naturalist ink plates.

The animals are built as actual poses rather than pictographic tokens: a loaded
mass establishes weight, then a few dry brush contours describe joints, fur,
feathers, and the characteristic anatomy that makes the animal readable.
Everything remains vector SVG so the marks can animate and scale cleanly.
"""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "animals"


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*v) for v in values]


def ribbon(values, width, seed, color="#262522", dry=False) -> str:
    d = stroke_path(p(*values), width=width, seed=seed, wobble=.36, taper_start=.13, taper_end=.16)
    brush = "dry-edge-v1" if dry else "loaded-ribbon-v2"
    return f'<path class="{"ink-dry" if dry else "ink-wash"}" d="{d}" fill="{color}" data-ink-brush-pass="{brush}"/>'


def dry(values, width, seed, color="#77746a") -> list[str]:
    return [f'<path class="ink-dry" d="{d}" fill="{color}" data-ink-brush-pass="dry-fragment-v1"/>' for d in dry_brush_paths(p(*values), width=width, seed=seed, breaks=2)]


def mass(d, fill="#77746a", detail="loaded-mass-v2") -> str:
    return f'<path class="ink-wash" d="{d}" fill="{fill}" data-ink-brush-pass="{detail}"/>'


def dab(cx, cy, rx, ry, fill="#262522") -> str:
    return f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" data-ink-brush-pass="loaded-dab-v1"/>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    cp = re.search(r'data-pua="([^"]+)"', source)
    if not cp:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="animals / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>animals / {name} — nineteenth-century naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


write("calf", [
    mass("M 24 31 C 31 27 44 27 53 31 C 59 34 61 39 60 44 C 58 50 51 52 43 51 C 35 52 25 49 20 44 C 17 40 19 34 24 31 Z", "#77746a"),
    mass("M 22 35 C 17 35 12 32 11 28 C 13 25 17 24 21 25 L 25 21 C 28 22 30 25 29 29 C 28 33 26 35 22 35 Z", "#4a4943"),
    mass("M 27 29 C 25 25 25 21 28 18 C 32 21 33 25 31 29 Z", "#262522"),
    ribbon([(25, 44, .08), (24, 51, .76), (22, 58, .08)], 2.0, "calf-foreleg"),
    ribbon([(36, 47, .08), (36, 53, .72), (34, 59, .08)], 1.75, "calf-hindleg", "#4a4943"),
    ribbon([(49, 45, .08), (51, 52, .72), (50, 58, .08)], 1.7, "calf-backleg", "#262522"),
    ribbon([(56, 36, .08), (62, 40, .72), (65, 37, .08)], 1.35, "calf-tail", "#4a4943"),
    dab(17.5, 28, .75, .65, "#dedbd4"),
    *dry([(28, 33, .08), (36, 31, .72), (46, 33, .08)], .8, "calf-flank"),
    *dry([(29, 39, .08), (35, 41, .72), (42, 40, .08)], .65, "calf-rib"),
])

write("colony", [
    # Three overlapping penguins read as a colony without becoming three dots.
    mass("M 10 45 C 9 37 12 30 18 28 C 24 27 28 32 28 40 C 28 48 23 54 17 54 C 12 53 10 50 10 45 Z", "#4a4943"),
    mass("M 27 42 C 26 32 30 25 37 24 C 44 24 48 31 47 40 C 47 49 42 55 36 55 C 30 54 27 50 27 42 Z", "#77746a"),
    mass("M 44 45 C 44 36 49 30 55 30 C 62 31 65 38 63 46 C 61 53 56 56 50 54 C 46 53 44 50 44 45 Z", "#bcb9af"),
    mass("M 31 38 C 33 33 39 32 43 36 C 44 42 42 49 37 51 C 33 49 31 44 31 38 Z", "#dedbd4"),
    ribbon([(13, 42, .08), (9, 45, .72), (7, 49, .08)], 1.45, "colony-flipper-a", "#262522"),
    ribbon([(45, 41, .08), (50, 44, .72), (54, 43, .08)], 1.25, "colony-flipper-b", "#4a4943"),
    ribbon([(17, 53, .08), (16, 58, .72), (14, 60, .08)], 1.05, "colony-foot-a", "#262522"),
    ribbon([(36, 54, .08), (35, 59, .72), (33, 61, .08)], 1.05, "colony-foot-b", "#4a4943"),
    dab(17, 35, .7, .65, "#dedbd4"), dab(36, 31, .7, .65, "#262522"), dab(54, 36, .7, .65, "#262522"),
    *dry([(31, 47, .08), (37, 48, .72), (42, 46, .08)], .7, "colony-belly"),
])

write("flock", [
    mass("M 10 35 C 16 29 22 28 27 31 C 23 35 18 38 12 38 Z", "#4a4943"),
    mass("M 29 26 C 35 20 42 20 47 24 C 43 29 37 32 31 31 Z", "#77746a"),
    mass("M 49 38 C 55 32 61 32 66 36 C 62 41 56 43 50 42 Z", "#4a4943"),
    ribbon([(15, 34, .08), (11, 25, .72), (13, 17, .08)], 2.25, "flock-wing-a"),
    ribbon([(17, 34, .08), (22, 26, .72), (27, 23, .08)], 1.5, "flock-wing-a-feather", "#77746a", True),
    ribbon([(34, 27, .08), (32, 17, .72), (36, 10, .08)], 2.0, "flock-wing-b"),
    ribbon([(37, 27, .08), (43, 19, .72), (49, 18, .08)], 1.35, "flock-wing-b-feather", "#4a4943", True),
    ribbon([(54, 39, .08), (54, 30, .72), (59, 23, .08)], 2.0, "flock-wing-c", "#77746a"),
    ribbon([(56, 39, .08), (62, 33, .72), (67, 32, .08)], 1.2, "flock-wing-c-feather", "#4a4943", True),
    dab(21, 32, .65, .6, "#dedbd4"), dab(40, 25, .65, .6, "#262522"), dab(59, 37, .65, .6, "#dedbd4"),
])

write("herd", [
    # A staggered line of cattle/bison: heads and legs keep the group legible.
    mass("M 10 38 C 15 32 25 31 33 35 C 38 38 40 45 36 49 C 29 52 18 51 12 47 C 9 44 8 41 10 38 Z", "#77746a"),
    mass("M 29 35 C 35 28 46 28 54 33 C 59 37 60 44 56 48 C 49 51 38 49 33 45 Z", "#4a4943"),
    mass("M 49 38 C 55 32 64 33 67 38 C 69 42 66 46 61 47 C 56 48 51 46 48 43 Z", "#bcb9af"),
    mass("M 9 37 C 5 35 4 30 7 27 L 12 29 L 16 25 C 19 29 17 34 13 37 Z", "#262522"),
    mass("M 30 34 C 27 30 28 25 31 22 L 36 26 L 40 22 C 42 27 39 32 35 35 Z", "#262522"),
    ribbon([(16, 46, .08), (15, 53, .72), (13, 59, .08)], 1.8, "herd-leg-a"),
    ribbon([(25, 47, .08), (26, 54, .72), (24, 60, .08)], 1.7, "herd-leg-b", "#262522"),
    ribbon([(40, 45, .08), (40, 53, .72), (38, 59, .08)], 1.8, "herd-leg-c", "#77746a"),
    ribbon([(50, 46, .08), (52, 53, .72), (50, 59, .08)], 1.65, "herd-leg-d", "#262522"),
    dab(10, 31, .7, .6, "#dedbd4"), dab(33, 28, .7, .6, "#dedbd4"), dab(58, 38, .7, .6, "#262522"),
    *dry([(19, 37, .08), (26, 39, .72), (32, 38, .08)], .7, "herd-flank"),
])

write("lamb", [
    mass("M 17 39 C 16 31 22 26 30 25 C 38 22 48 25 52 32 C 57 39 53 49 46 52 C 37 56 25 53 19 48 C 17 46 16 42 17 39 Z", "#bcb9af"),
    mass("M 47 34 C 52 31 60 32 63 36 C 64 40 61 44 55 44 L 49 42 Z", "#4a4943"),
    ribbon([(23, 45, .08), (22, 52, .72), (20, 58, .08)], 1.8, "lamb-foreleg"),
    ribbon([(37, 48, .08), (38, 54, .72), (36, 60, .08)], 1.75, "lamb-hindleg", "#262522"),
    ribbon([(50, 43, .08), (55, 48, .72), (61, 48, .08)], 1.15, "lamb-tail", "#4a4943"),
    ribbon([(19, 34, .08), (24, 29, .72), (31, 29, .08)], .9, "lamb-wool-top", "#77746a", True),
    ribbon([(25, 38, .08), (33, 35, .72), (42, 37, .08)], .85, "lamb-wool-rib-a", "#77746a", True),
    ribbon([(27, 45, .08), (35, 47, .72), (44, 44, .08)], .8, "lamb-wool-rib-b", "#77746a", True),
    dab(56, 36, .75, .65, "#dedbd4"),
])

write("migration", [
    # Swallows in three different wing phases, not identical chevrons.
    mass("M 9 35 C 14 30 19 30 24 33 C 20 36 15 38 10 38 Z", "#4a4943"),
    mass("M 29 25 C 34 21 40 22 44 25 C 40 29 35 31 30 30 Z", "#77746a"),
    mass("M 49 40 C 54 35 60 35 65 38 C 61 42 55 44 50 43 Z", "#4a4943"),
    ribbon([(14, 34, .08), (10, 26, .72), (12, 19, .08)], 1.9, "migration-wing-1"),
    ribbon([(16, 34, .08), (21, 29, .72), (27, 28, .08)], 1.15, "migration-feather-1", "#bcb9af", True),
    ribbon([(34, 25, .08), (31, 17, .72), (35, 11, .08)], 1.8, "migration-wing-2", "#262522"),
    ribbon([(37, 25, .08), (43, 20, .72), (49, 20, .08)], 1.15, "migration-feather-2", "#4a4943", True),
    ribbon([(54, 41, .08), (55, 32, .72), (60, 26, .08)], 1.9, "migration-wing-3", "#77746a"),
    ribbon([(56, 41, .08), (62, 37, .72), (67, 37, .08)], 1.15, "migration-feather-3", "#bcb9af", True),
    dab(20, 33, .55, .5, "#dedbd4"), dab(40, 25, .55, .5, "#262522"), dab(60, 39, .55, .5, "#dedbd4"),
])

write("pack", [
    mass("M 8 42 C 11 34 20 30 28 33 C 35 35 39 41 37 47 C 32 52 19 53 11 48 C 8 46 7 44 8 42 Z", "#4a4943"),
    mass("M 27 39 C 31 31 40 28 48 32 C 54 35 57 41 54 47 C 48 52 37 51 30 47 Z", "#77746a"),
    mass("M 47 44 C 52 37 60 36 66 40 C 69 43 68 47 64 49 C 58 51 51 49 47 47 Z", "#bcb9af"),
    mass("M 8 39 L 7 30 L 14 34 L 20 29 L 22 37 L 17 42 Z", "#262522"),
    mass("M 29 36 L 29 27 L 35 31 L 42 27 L 43 35 L 38 39 Z", "#4a4943"),
    ribbon([(14, 47, .08), (13, 54, .72), (11, 60, .08)], 1.7, "pack-leg-a"),
    ribbon([(25, 48, .08), (27, 54, .72), (26, 60, .08)], 1.6, "pack-leg-b", "#262522"),
    ribbon([(37, 47, .08), (37, 54, .72), (35, 59, .08)], 1.7, "pack-leg-c", "#77746a"),
    ribbon([(48, 48, .08), (50, 54, .72), (49, 59, .08)], 1.55, "pack-leg-d", "#262522"),
    ribbon([(52, 43, .08), (59, 48, .72), (66, 47, .08)], 1.2, "pack-tail", "#4a4943"),
    dab(17, 36, .65, .58, "#dedbd4"), dab(38, 33, .65, .58, "#dedbd4"), dab(58, 41, .65, .58, "#262522"),
    *dry([(19, 40, .08), (27, 42, .72), (33, 41, .08)], .65, "pack-flank"),
])

write("predator", [
    # A crouched cat/wolf profile, with shoulder, haunch, muzzle, and paws.
    mass("M 19 39 C 25 32 36 30 45 34 C 52 36 58 39 63 37 C 67 36 68 39 65 42 C 59 47 52 45 47 43 C 43 50 32 54 23 51 C 17 49 15 44 19 39 Z", "#4a4943"),
    mass("M 17 38 C 12 37 9 34 10 30 L 14 25 L 20 29 L 26 25 L 28 32 C 26 36 22 38 17 38 Z", "#262522"),
    ribbon([(29, 46, .08), (27, 53, .72), (23, 59, .08)], 2.0, "predator-forepaw"),
    ribbon([(43, 44, .08), (45, 51, .72), (43, 58, .08)], 1.9, "predator-hindpaw", "#77746a"),
    ribbon([(51, 40, .08), (58, 46, .72), (65, 47, .08)], 1.3, "predator-tail"),
    ribbon([(27, 34, .08), (33, 37, .72), (39, 35, .08)], .9, "predator-shoulder", "#bcb9af", True),
    ribbon([(33, 44, .08), (38, 47, .72), (44, 45, .08)], .8, "predator-rib", "#77746a", True),
    dab(18, 31, .8, .7, "#dedbd4"),
    *dry([(11, 41, .08), (17, 43, .72), (23, 42, .08)], .75, "predator-fur"),
])

write("prey", [
    # A hare in a compact alert crouch: long ears, haunch, forepaw, and tail.
    mass("M 21 44 C 21 36 27 31 35 31 C 44 31 51 37 52 44 C 52 51 46 55 37 55 C 28 55 22 51 21 44 Z", "#bcb9af"),
    mass("M 25 35 C 20 31 20 24 22 17 C 28 21 31 27 30 33 C 33 27 38 23 43 24 C 42 31 38 36 32 38 Z", "#77746a"),
    mass("M 20 40 C 15 40 12 37 13 34 C 16 32 20 33 23 35 L 28 37 C 27 40 24 41 20 40 Z", "#4a4943"),
    ribbon([(28, 48, .08), (26, 54, .72), (23, 59, .08)], 1.7, "prey-forepaw"),
    ribbon([(43, 48, .08), (47, 54, .72), (51, 57, .08)], 1.7, "prey-hindfoot", "#4a4943"),
    ribbon([(48, 37, .08), (56, 39, .72), (62, 36, .08)], 1.15, "prey-tail", "#77746a"),
    ribbon([(30, 40, .08), (36, 43, .72), (43, 41, .08)], .8, "prey-rib", "#77746a", True),
    dab(18, 35, .7, .6, "#262522"),
])

write("squirrel", [
    mass("M 25 42 C 26 34 32 29 40 30 C 48 31 52 38 50 46 C 48 53 40 57 33 54 C 27 52 24 48 25 42 Z", "#77746a"),
    mass("M 30 34 C 27 30 28 24 33 21 C 39 19 45 22 46 28 C 47 32 44 35 40 37 Z", "#4a4943"),
    mass("M 43 45 C 48 40 54 34 55 27 C 56 20 52 15 48 14 C 44 13 41 16 42 20 C 43 23 48 25 50 29 C 52 34 48 38 44 41 C 40 44 39 47 43 45 Z", "#4a4943"),
    ribbon([(30, 45, .08), (27, 52, .72), (24, 58, .08)], 1.8, "squirrel-foot"),
    ribbon([(42, 47, .08), (46, 53, .72), (51, 56, .08)], 1.65, "squirrel-hindfoot", "#262522"),
    ribbon([(29, 39, .08), (24, 42, .72), (20, 45, .08)], 1.25, "squirrel-forepaw", "#262522"),
    ribbon([(47, 18, .08), (52, 23, .72), (54, 29, .08)], 1.1, "squirrel-tail-fold", "#bcb9af", True),
    ribbon([(29, 23, .08), (30, 19, .72), (33, 17, .08)], 1.0, "squirrel-ear", "#262522"),
    dab(37, 27, .75, .65, "#dedbd4"),
    *dry([(31, 37, .08), (37, 39, .72), (43, 38, .08)], .7, "squirrel-rib"),
    *dry([(45, 23, .08), (50, 26, .72), (52, 31, .08)], .75, "squirrel-tail-fur"),
])


def append_detail(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    target.write_text(source.replace("</svg>", "".join(marks) + "</svg>"))


# Fine contour work is deliberately sparse: it gives the studies the feel of
# a field plate without turning them into hatching or a second outline.
append_detail("calf", [
    ribbon([(28, 32, .08), (35, 30, .72), (45, 31, .08)], .55, "calf-back-contour", "#262522", True),
    ribbon([(25, 40, .08), (32, 43, .72), (42, 44, .08)], .5, "calf-belly-contour", "#262522", True),
    ribbon([(28, 47, .08), (30, 50, .72), (30, 54, .08)], .48, "calf-knee", "#262522", True),
    ribbon([(45, 45, .08), (47, 48, .72), (47, 52, .08)], .48, "calf-knee-back", "#262522", True),
])
append_detail("colony", [
    ribbon([(13, 34, .08), (17, 40, .72), (21, 47, .08)], .55, "colony-belly-a", "#262522", True),
    ribbon([(31, 31, .08), (36, 38, .72), (41, 49, .08)], .55, "colony-belly-b", "#262522", True),
    ribbon([(49, 36, .08), (53, 41, .72), (58, 49, .08)], .5, "colony-belly-c", "#262522", True),
])
append_detail("flock", [
    ribbon([(13, 34, .08), (17, 32, .72), (22, 33, .08)], .5, "flock-body-a", "#262522", True),
    ribbon([(32, 25, .08), (37, 23, .72), (42, 25, .08)], .5, "flock-body-b", "#262522", True),
    ribbon([(51, 39, .08), (56, 37, .72), (61, 39, .08)], .5, "flock-body-c", "#262522", True),
])
append_detail("herd", [
    ribbon([(18, 35, .08), (25, 34, .72), (31, 37, .08)], .55, "herd-back-a", "#262522", True),
    ribbon([(37, 33, .08), (44, 32, .72), (51, 35, .08)], .55, "herd-back-b", "#262522", True),
    ribbon([(10, 43, .08), (17, 46, .72), (25, 47, .08)], .5, "herd-belly-a", "#262522", True),
    ribbon([(34, 42, .08), (42, 45, .72), (51, 45, .08)], .5, "herd-belly-b", "#262522", True),
])
append_detail("lamb", [
    ribbon([(22, 32, .08), (28, 28, .72), (35, 27, .08)], .55, "lamb-wool-contour-a", "#262522", True),
    ribbon([(29, 34, .08), (37, 31, .72), (45, 34, .08)], .5, "lamb-wool-contour-b", "#262522", True),
    ribbon([(30, 42, .08), (38, 40, .72), (48, 42, .08)], .5, "lamb-wool-contour-c", "#262522", True),
])
append_detail("pack", [
    ribbon([(14, 37, .08), (22, 35, .72), (29, 38, .08)], .55, "pack-shoulder-a", "#262522", True),
    ribbon([(34, 35, .08), (41, 33, .72), (49, 36, .08)], .55, "pack-shoulder-b", "#262522", True),
    ribbon([(15, 44, .08), (23, 47, .72), (31, 46, .08)], .48, "pack-belly-a", "#262522", True),
])
append_detail("predator", [
    ribbon([(23, 37, .08), (29, 33, .72), (36, 34, .08)], .6, "predator-shoulder-contour", "#262522", True),
    ribbon([(21, 45, .08), (29, 48, .72), (37, 48, .08)], .52, "predator-belly-contour", "#262522", True),
    ribbon([(48, 38, .08), (53, 41, .72), (58, 41, .08)], .48, "predator-rib-contour", "#262522", True),
])
append_detail("prey", [
    ribbon([(27, 38, .08), (34, 34, .72), (42, 35, .08)], .5, "prey-back-contour", "#262522", True),
    ribbon([(28, 47, .08), (35, 50, .72), (44, 49, .08)], .5, "prey-belly-contour", "#262522", True),
    ribbon([(23, 26, .08), (25, 29, .72), (27, 33, .08)], .45, "prey-ear-edge", "#262522", True),
])
append_detail("squirrel", [
    ribbon([(30, 35, .08), (36, 32, .72), (43, 34, .08)], .55, "squirrel-back-contour", "#262522", True),
    ribbon([(29, 47, .08), (35, 50, .72), (43, 48, .08)], .5, "squirrel-belly-contour", "#262522", True),
    ribbon([(48, 17, .08), (51, 21, .72), (53, 26, .08)], .5, "squirrel-tail-contour", "#262522", True),
])

# Broad, pressure-shaped passes keep the animals from looking like flat
# vector stickers.  These sit inside the silhouettes like a loaded brush laid
# down in one motion; the narrow contour fragments above remain the anatomy.
append_detail("calf", [
    ribbon([(23, 34, .08), (30, 30, .58), (40, 30, .9), (51, 34, .55), (57, 40, .08)], 4.4, "calf-loaded-back", "#6b6961"),
    ribbon([(23, 43, .08), (31, 46, .72), (42, 47, .92), (51, 44, .08)], 2.0, "calf-loaded-belly", "#9a978d"),
])
append_detail("colony", [
    ribbon([(13, 35, .08), (17, 31, .72), (21, 37, .95), (21, 46, .08)], 3.2, "colony-loaded-a", "#383733"),
    ribbon([(31, 31, .08), (37, 27, .72), (43, 33, .95), (42, 47, .08)], 3.0, "colony-loaded-b", "#5c5a53"),
    ribbon([(49, 36, .08), (54, 33, .72), (60, 39, .95), (58, 49, .08)], 2.7, "colony-loaded-c", "#9a978d"),
])
append_detail("herd", [
    ribbon([(12, 37, .08), (19, 34, .7), (28, 36, .92), (35, 42, .08)], 3.9, "herd-loaded-a", "#67655e"),
    ribbon([(33, 34, .08), (41, 31, .72), (50, 35, .92), (56, 42, .08)], 4.0, "herd-loaded-b", "#383733"),
])
append_detail("lamb", [
    ribbon([(21, 35, .08), (27, 29, .68), (37, 27, .92), (48, 33, .08)], 4.6, "lamb-loaded-wool-a", "#aaa79d"),
    ribbon([(21, 43, .08), (30, 48, .75), (42, 48, .9), (51, 41, .08)], 3.0, "lamb-loaded-wool-b", "#858279"),
])
append_detail("pack", [
    ribbon([(12, 38, .08), (20, 34, .72), (29, 37, .92), (36, 43, .08)], 3.8, "pack-loaded-a", "#383733"),
    ribbon([(31, 37, .08), (39, 32, .72), (48, 36, .92), (53, 43, .08)], 3.7, "pack-loaded-b", "#65635c"),
])
append_detail("predator", [
    ribbon([(20, 39, .08), (28, 34, .72), (38, 34, .92), (48, 39, .08)], 4.5, "predator-loaded-shoulder", "#383733"),
    ribbon([(24, 46, .08), (32, 49, .72), (42, 47, .08)], 2.4, "predator-loaded-haunch", "#65635c"),
])
append_detail("prey", [
    ribbon([(24, 41, .08), (30, 34, .7), (39, 34, .92), (48, 41, .08)], 4.0, "prey-loaded-back", "#aaa79d"),
    ribbon([(28, 48, .08), (36, 52, .72), (45, 49, .08)], 2.1, "prey-loaded-haunch", "#858279"),
])
append_detail("squirrel", [
    ribbon([(28, 40, .08), (33, 34, .72), (41, 35, .92), (48, 41, .08)], 4.3, "squirrel-loaded-body", "#5e5c55"),
    ribbon([(44, 42, .08), (51, 36, .68), (55, 28, .92), (51, 19, .08)], 3.8, "squirrel-loaded-tail", "#383733"),
])

def plate_stroke(values, width, seed, color="#262522") -> str:
    """A loaded, pressure-shaped stroke for the final non-round silhouettes."""
    return ribbon(values, width, f"plate-{seed}", color)


def plate_etch(values, width, seed, color="#4a4943") -> str:
    return ribbon(values, width, f"etch-{seed}", color, True)


# Final silhouettes are stroke-led rather than oval-led.  The earlier mass
# pass is intentionally superseded here: these are closer to a naturalist's
# quick plate study, where a few long loaded strokes carry the anatomy.
PLATES = {
    "calf": [
        plate_stroke([(23, 37, .08), (29, 31, .55), (40, 30, .92), (51, 34, .72), (57, 40, .08)], 8.0, "calf-body", "#77746a"),
        plate_stroke([(24, 36, .08), (20, 31, .72), (16, 28, .08)], 4.2, "calf-neck", "#4a4943"),
        plate_stroke([(16, 28, .08), (12, 29, .72), (16, 33, .08)], 2.8, "calf-head"),
        plate_stroke([(27, 42, .08), (26, 50, .72), (23, 58, .08)], 2.0, "calf-leg-a"),
        plate_stroke([(39, 44, .08), (39, 52, .72), (37, 59, .08)], 1.85, "calf-leg-b", "#4a4943"),
        plate_stroke([(51, 41, .08), (53, 49, .72), (51, 57, .08)], 1.75, "calf-leg-c"),
        plate_stroke([(53, 35, .08), (61, 40, .72), (65, 37, .08)], 1.3, "calf-tail", "#4a4943"),
        plate_etch([(29, 34, .08), (38, 33, .72), (48, 35, .08)], .7, "calf-rib"),
        plate_etch([(29, 43, .08), (35, 45, .72), (43, 44, .08)], .62, "calf-belly"),
        dab(14, 29, .65, .55, "#dedbd4"),
    ],
    "colony": [
        plate_stroke([(15, 31, .08), (12, 37, .72), (14, 47, .92), (18, 54, .08)], 7.2, "colony-penguin-a", "#4a4943"),
        plate_stroke([(34, 25, .08), (29, 34, .72), (31, 46, .92), (36, 55, .08)], 8.0, "colony-penguin-b", "#77746a"),
        plate_stroke([(53, 31, .08), (48, 39, .72), (50, 49, .92), (55, 55, .08)], 7.0, "colony-penguin-c", "#bcb9af"),
        plate_stroke([(14, 40, .08), (9, 44, .72), (7, 49, .08)], 1.45, "colony-flipper-a"),
        plate_stroke([(48, 40, .08), (54, 43, .72), (58, 41, .08)], 1.3, "colony-flipper-c", "#4a4943"),
        plate_etch([(30, 33, .08), (35, 39, .72), (39, 48, .08)], .62, "colony-belly-b"),
        plate_etch([(12, 34, .08), (16, 40, .72), (18, 47, .08)], .58, "colony-belly-a"),
        dab(15, 30, .6, .55, "#dedbd4"), dab(35, 25, .6, .55, "#262522"), dab(53, 31, .6, .55, "#262522"),
    ],
    "flock": [
        plate_stroke([(10, 35, .08), (16, 31, .72), (23, 34, .08)], 3.4, "flock-body-a", "#4a4943"),
        plate_stroke([(30, 26, .08), (36, 22, .72), (43, 25, .08)], 3.4, "flock-body-b", "#77746a"),
        plate_stroke([(50, 39, .08), (56, 35, .72), (64, 39, .08)], 3.2, "flock-body-c", "#4a4943"),
        plate_stroke([(14, 33, .08), (10, 25, .72), (12, 17, .08)], 2.0, "flock-wing-a"),
        plate_stroke([(17, 33, .08), (22, 27, .72), (27, 25, .08)], 1.0, "flock-feather-a", "#77746a"),
        plate_stroke([(34, 25, .08), (32, 17, .72), (36, 10, .08)], 2.0, "flock-wing-b", "#262522"),
        plate_stroke([(38, 25, .08), (44, 20, .72), (50, 20, .08)], 1.0, "flock-feather-b", "#4a4943"),
        plate_stroke([(54, 39, .08), (55, 30, .72), (60, 23, .08)], 2.0, "flock-wing-c", "#77746a"),
        dab(21, 32, .55, .5, "#dedbd4"), dab(41, 24, .55, .5, "#262522"), dab(59, 37, .55, .5, "#dedbd4"),
    ],
    "herd": [
        plate_stroke([(11, 39, .08), (17, 34, .62), (26, 35, .92), (34, 41, .08)], 7.0, "herd-cow-a", "#77746a"),
        plate_stroke([(31, 36, .08), (38, 30, .62), (48, 33, .92), (56, 41, .08)], 7.5, "herd-cow-b", "#4a4943"),
        plate_stroke([(50, 40, .08), (56, 35, .62), (64, 39, .08)], 5.5, "herd-cow-c", "#bcb9af"),
        plate_stroke([(10, 37, .08), (6, 31, .72), (8, 27, .08)], 1.2, "herd-horn-a"),
        plate_stroke([(14, 36, .08), (17, 29, .72), (20, 26, .08)], 1.2, "herd-horn-a2"),
        plate_stroke([(31, 34, .08), (28, 28, .72), (31, 23, .08)], 1.25, "herd-horn-b"),
        plate_stroke([(35, 33, .08), (40, 27, .72), (43, 25, .08)], 1.2, "herd-horn-b2"),
        plate_stroke([(17, 43, .08), (16, 52, .72), (14, 59, .08)], 1.8, "herd-leg-a"),
        plate_stroke([(26, 44, .08), (27, 53, .72), (25, 60, .08)], 1.7, "herd-leg-b", "#262522"),
        plate_stroke([(40, 43, .08), (41, 52, .72), (39, 59, .08)], 1.8, "herd-leg-c"),
        plate_stroke([(50, 43, .08), (53, 52, .72), (51, 59, .08)], 1.7, "herd-leg-d", "#262522"),
        plate_etch([(18, 37, .08), (25, 39, .72), (31, 40, .08)], .6, "herd-flank-a"),
        plate_etch([(38, 34, .08), (45, 36, .72), (51, 39, .08)], .6, "herd-flank-b"),
        dab(11, 33, .6, .55, "#dedbd4"), dab(33, 30, .6, .55, "#dedbd4"),
    ],
    "lamb": [
        plate_stroke([(20, 37, .08), (24, 29, .62), (34, 26, .92), (45, 29, .72), (52, 37, .08)], 8.5, "lamb-wool-a", "#bcb9af"),
        plate_stroke([(20, 43, .08), (27, 49, .65), (38, 51, .9), (48, 45, .08)], 5.5, "lamb-wool-b", "#77746a"),
        plate_stroke([(50, 35, .08), (56, 34, .72), (62, 38, .08)], 3.6, "lamb-head", "#4a4943"),
        plate_stroke([(24, 45, .08), (23, 52, .72), (20, 59, .08)], 1.8, "lamb-leg-a"),
        plate_stroke([(38, 48, .08), (39, 54, .72), (37, 60, .08)], 1.75, "lamb-leg-b", "#262522"),
        plate_stroke([(49, 42, .08), (55, 48, .72), (61, 48, .08)], 1.1, "lamb-tail", "#4a4943"),
        plate_etch([(24, 33, .08), (31, 30, .72), (40, 31, .08)], .65, "lamb-wool-a"),
        plate_etch([(27, 41, .08), (34, 44, .72), (44, 42, .08)], .65, "lamb-wool-b"),
        dab(57, 36, .65, .55, "#dedbd4"),
    ],
    "migration": [
        plate_stroke([(9, 35, .08), (15, 31, .72), (23, 34, .08)], 3.0, "migration-bird-a", "#4a4943"),
        plate_stroke([(30, 26, .08), (36, 22, .72), (44, 25, .08)], 3.0, "migration-bird-b", "#77746a"),
        plate_stroke([(50, 40, .08), (56, 36, .72), (65, 39, .08)], 3.0, "migration-bird-c", "#4a4943"),
        plate_stroke([(13, 33, .08), (9, 26, .72), (11, 19, .08)], 1.8, "migration-wing-a"),
        plate_stroke([(17, 33, .08), (22, 28, .72), (27, 28, .08)], .9, "migration-feather-a", "#bcb9af"),
        plate_stroke([(34, 25, .08), (32, 17, .72), (35, 11, .08)], 1.8, "migration-wing-b", "#262522"),
        plate_stroke([(38, 25, .08), (44, 20, .72), (49, 20, .08)], .9, "migration-feather-b", "#4a4943"),
        plate_stroke([(54, 41, .08), (55, 32, .72), (60, 26, .08)], 1.8, "migration-wing-c", "#77746a"),
        dab(20, 33, .5, .45, "#dedbd4"), dab(40, 25, .5, .45, "#262522"), dab(60, 39, .5, .45, "#dedbd4"),
    ],
    "pack": [
        plate_stroke([(10, 42, .08), (16, 35, .62), (25, 36, .92), (35, 42, .08)], 6.8, "pack-wolf-a", "#4a4943"),
        plate_stroke([(29, 39, .08), (35, 32, .62), (44, 33, .92), (53, 41, .08)], 7.0, "pack-wolf-b", "#77746a"),
        plate_stroke([(48, 44, .08), (55, 38, .62), (63, 41, .08)], 5.0, "pack-wolf-c", "#bcb9af"),
        plate_stroke([(10, 38, .08), (9, 30, .72), (14, 34, .08)], 1.6, "pack-ear-a"),
        plate_stroke([(17, 36, .08), (20, 29, .72), (23, 36, .08)], 1.5, "pack-ear-a2"),
        plate_stroke([(30, 35, .08), (30, 28, .72), (35, 32, .08)], 1.5, "pack-ear-b"),
        plate_stroke([(37, 33, .08), (42, 27, .72), (44, 34, .08)], 1.45, "pack-ear-b2"),
        plate_stroke([(15, 45, .08), (13, 54, .72), (11, 60, .08)], 1.7, "pack-leg-a"),
        plate_stroke([(25, 46, .08), (27, 54, .72), (26, 60, .08)], 1.6, "pack-leg-b", "#262522"),
        plate_stroke([(38, 44, .08), (38, 53, .72), (36, 59, .08)], 1.7, "pack-leg-c"),
        plate_stroke([(48, 46, .08), (51, 54, .72), (50, 59, .08)], 1.6, "pack-leg-d", "#262522"),
        plate_etch([(17, 40, .08), (24, 42, .72), (31, 40, .08)], .6, "pack-flank-a"),
        dab(17, 36, .6, .5, "#dedbd4"), dab(37, 33, .6, .5, "#dedbd4"),
    ],
    "predator": [
        plate_stroke([(18, 41, .08), (25, 34, .62), (35, 33, .92), (46, 37, .72), (58, 40, .08)], 8.0, "predator-body", "#4a4943"),
        plate_stroke([(22, 37, .08), (17, 31, .72), (12, 29, .08)], 4.0, "predator-neck", "#262522"),
        plate_stroke([(13, 30, .08), (9, 33, .72), (14, 36, .08)], 2.7, "predator-muzzle"),
        plate_stroke([(28, 45, .08), (26, 53, .72), (23, 59, .08)], 2.0, "predator-forepaw"),
        plate_stroke([(43, 43, .08), (45, 51, .72), (43, 58, .08)], 1.9, "predator-hindpaw", "#77746a"),
        plate_stroke([(50, 38, .08), (58, 45, .72), (65, 46, .08)], 1.25, "predator-tail"),
        plate_etch([(25, 37, .08), (32, 35, .72), (39, 36, .08)], .65, "predator-shoulder"),
        plate_etch([(25, 44, .08), (34, 47, .72), (43, 45, .08)], .6, "predator-rib"),
        dab(13, 31, .65, .55, "#dedbd4"),
    ],
    "prey": [
        plate_stroke([(23, 43, .08), (28, 35, .62), (37, 33, .92), (47, 39, .72), (51, 46, .08)], 7.4, "prey-haunch", "#bcb9af"),
        plate_stroke([(28, 36, .08), (24, 28, .72), (24, 18, .08)], 2.9, "prey-ear-a", "#77746a"),
        plate_stroke([(31, 35, .08), (35, 28, .72), (42, 25, .08)], 2.8, "prey-ear-b", "#4a4943"),
        plate_stroke([(23, 38, .08), (18, 36, .72), (14, 34, .08)], 2.5, "prey-muzzle", "#4a4943"),
        plate_stroke([(29, 47, .08), (27, 54, .72), (24, 59, .08)], 1.7, "prey-forepaw"),
        plate_stroke([(43, 47, .08), (47, 54, .72), (52, 57, .08)], 1.65, "prey-hindfoot", "#4a4943"),
        plate_stroke([(47, 40, .08), (55, 41, .72), (62, 38, .08)], 1.1, "prey-tail", "#77746a"),
        plate_etch([(29, 40, .08), (36, 37, .72), (44, 39, .08)], .6, "prey-rib"),
        dab(18, 35, .6, .5, "#262522"),
    ],
    "squirrel": [
        plate_stroke([(27, 42, .08), (31, 35, .62), (39, 34, .92), (47, 39, .72), (48, 47, .08)], 7.2, "squirrel-body", "#77746a"),
        plate_stroke([(29, 36, .08), (25, 31, .72), (20, 32, .08)], 3.4, "squirrel-head", "#4a4943"),
        plate_stroke([(24, 32, .08), (25, 25, .72), (29, 20, .08)], 1.9, "squirrel-ear"),
        plate_stroke([(44, 44, .08), (50, 37, .52), (55, 29, .8), (54, 21, .62), (49, 15, .08)], 5.0, "squirrel-tail", "#4a4943"),
        plate_stroke([(29, 45, .08), (26, 53, .72), (23, 59, .08)], 1.8, "squirrel-foot"),
        plate_stroke([(41, 47, .08), (45, 53, .72), (50, 56, .08)], 1.7, "squirrel-hindfoot", "#262522"),
        plate_stroke([(29, 39, .08), (24, 42, .72), (20, 45, .08)], 1.25, "squirrel-forepaw"),
        plate_etch([(31, 38, .08), (37, 36, .72), (43, 39, .08)], .6, "squirrel-back"),
        plate_etch([(48, 18, .08), (52, 23, .72), (54, 29, .08)], .7, "squirrel-tail-fur"),
        dab(25, 32, .6, .5, "#dedbd4"),
    ],
}


for _name, _marks in PLATES.items():
    write(_name, _marks)

print("redrew all 10 animal PUA glyphs as stroke-led nineteenth-century naturalist studies")


# A final anatomy pass: irregular wash silhouettes prevent the thin-stroke
# version from becoming skeletal, while keeping every contour asymmetrical and
# species-cued.  No ellipse or geometric oval is used for a primary body.
ANATOMICAL = {
    "calf": [
        mass("M 18 38 C 23 32 31 28 41 29 C 49 30 56 34 59 39 C 61 43 58 47 52 49 C 45 51 38 49 31 48 C 26 50 20 46 18 43 C 17 41 17 39 18 38 Z", "#77746a"),
        mass("M 20 37 C 15 37 10 34 9 30 C 12 27 16 28 19 29 L 22 24 L 27 27 C 29 31 27 35 24 36 Z", "#4a4943"),
        ribbon([(25, 44, .08), (24, 51, .72), (22, 59, .08)], 2.0, "anatomy-calf-foreleg"),
        ribbon([(37, 46, .08), (38, 53, .72), (36, 60, .08)], 1.85, "anatomy-calf-hindleg", "#262522"),
        ribbon([(49, 44, .08), (52, 51, .72), (50, 58, .08)], 1.75, "anatomy-calf-backleg"),
        ribbon([(55, 35, .08), (62, 40, .72), (65, 37, .08)], 1.2, "anatomy-calf-tail", "#4a4943"),
        ribbon([(28, 32, .08), (35, 30, .72), (44, 32, .08)], .65, "anatomy-calf-back", "#262522", True),
        ribbon([(27, 41, .08), (34, 44, .72), (44, 43, .08)], .6, "anatomy-calf-rib", "#262522", True),
        dab(15, 30, .65, .55, "#dedbd4"),
    ],
    "colony": [
        mass("M 11 45 C 10 38 12 31 17 28 C 22 29 25 35 24 44 C 24 50 21 54 17 55 C 13 53 11 50 11 45 Z", "#4a4943"),
        mass("M 29 44 C 28 35 30 27 36 24 C 42 27 45 34 44 44 C 43 51 40 55 36 56 C 31 53 29 50 29 44 Z", "#77746a"),
        mass("M 47 46 C 46 38 49 31 55 30 C 61 33 64 40 62 47 C 60 53 56 56 52 55 C 49 53 47 50 47 46 Z", "#bcb9af"),
        ribbon([(17, 28, .08), (15, 25, .72), (16, 22, .08)], 1.7, "anatomy-colony-beak-a"),
        ribbon([(36, 25, .08), (34, 22, .72), (36, 19, .08)], 1.7, "anatomy-colony-beak-b", "#262522"),
        ribbon([(55, 31, .08), (53, 28, .72), (55, 26, .08)], 1.5, "anatomy-colony-beak-c", "#4a4943"),
        ribbon([(13, 42, .08), (9, 46, .72), (7, 50, .08)], 1.25, "anatomy-colony-flipper-a"),
        ribbon([(45, 42, .08), (51, 45, .72), (56, 43, .08)], 1.2, "anatomy-colony-flipper-c", "#4a4943"),
        ribbon([(13, 48, .08), (17, 51, .72), (20, 49, .08)], .55, "anatomy-colony-belly-a", "#dedbd4", True),
        ribbon([(31, 46, .08), (36, 50, .72), (40, 48, .08)], .6, "anatomy-colony-belly-b", "#dedbd4", True),
        dab(17, 35, .65, .55, "#dedbd4"), dab(36, 31, .65, .55, "#262522"), dab(55, 36, .65, .55, "#262522"),
    ],
    "flock": [
        mass("M 9 35 C 14 29 20 30 25 33 C 21 36 16 38 10 38 Z", "#4a4943"),
        mass("M 29 26 C 34 20 41 21 46 25 C 42 29 36 32 30 31 Z", "#77746a"),
        mass("M 49 39 C 54 33 61 33 66 37 C 62 41 56 43 50 42 Z", "#4a4943"),
        ribbon([(12, 33, .08), (8, 27, .72), (11, 20, .08)], 2.0, "anatomy-flock-wing-a"),
        ribbon([(16, 33, .08), (22, 27, .72), (27, 26, .08)], 1.1, "anatomy-flock-feather-a", "#77746a", True),
        ribbon([(33, 25, .08), (31, 18, .72), (35, 11, .08)], 1.9, "anatomy-flock-wing-b", "#262522"),
        ribbon([(37, 25, .08), (43, 20, .72), (49, 20, .08)], 1.0, "anatomy-flock-feather-b", "#4a4943", True),
        ribbon([(53, 39, .08), (54, 31, .72), (60, 24, .08)], 1.9, "anatomy-flock-wing-c", "#77746a"),
        ribbon([(57, 39, .08), (63, 35, .72), (67, 35, .08)], 1.0, "anatomy-flock-feather-c", "#4a4943", True),
        ribbon([(10, 35, .08), (7, 34, .72), (5, 35, .08)], .7, "anatomy-flock-beak-a"),
        dab(19, 32, .55, .5, "#dedbd4"), dab(40, 25, .55, .5, "#262522"), dab(59, 38, .55, .5, "#dedbd4"),
    ],
    "herd": [
        mass("M 9 39 C 14 33 22 32 30 35 C 36 38 38 44 34 48 C 28 51 18 50 12 46 C 9 44 8 41 9 39 Z", "#77746a"),
        mass("M 29 36 C 35 29 45 29 53 33 C 59 37 60 43 56 47 C 49 50 39 48 33 45 Z", "#4a4943"),
        mass("M 50 40 C 55 35 63 34 67 38 C 69 42 66 46 61 47 C 56 47 52 45 49 43 Z", "#bcb9af"),
        ribbon([(10, 37, .08), (7, 31, .72), (9, 27, .08)], 1.1, "anatomy-herd-horn-a"),
        ribbon([(14, 36, .08), (18, 29, .72), (20, 26, .08)], 1.1, "anatomy-herd-horn-a2"),
        ribbon([(31, 34, .08), (29, 28, .72), (32, 24, .08)], 1.15, "anatomy-herd-horn-b"),
        ribbon([(35, 33, .08), (40, 27, .72), (43, 25, .08)], 1.1, "anatomy-herd-horn-b2"),
        ribbon([(15, 45, .08), (14, 53, .72), (12, 60, .08)], 1.8, "anatomy-herd-leg-a"),
        ribbon([(25, 46, .08), (26, 54, .72), (24, 60, .08)], 1.7, "anatomy-herd-leg-b", "#262522"),
        ribbon([(40, 44, .08), (40, 53, .72), (38, 59, .08)], 1.8, "anatomy-herd-leg-c"),
        ribbon([(50, 45, .08), (52, 53, .72), (50, 59, .08)], 1.65, "anatomy-herd-leg-d", "#262522"),
        ribbon([(18, 38, .08), (25, 40, .72), (31, 39, .08)], .6, "anatomy-herd-flank-a", "#262522", True),
        ribbon([(38, 35, .08), (45, 38, .72), (51, 37, .08)], .6, "anatomy-herd-flank-b", "#262522", True),
        dab(11, 33, .6, .5, "#dedbd4"), dab(33, 30, .6, .5, "#dedbd4"), dab(58, 39, .6, .5, "#262522"),
    ],
    "lamb": [
        mass("M 17 39 C 18 31 24 26 32 25 C 40 23 49 27 53 34 C 56 42 52 49 45 52 C 36 55 25 52 19 47 C 17 45 16 42 17 39 Z", "#bcb9af"),
        mass("M 49 35 C 54 32 61 33 64 37 C 64 41 61 44 56 44 L 50 42 Z", "#4a4943"),
        ribbon([(23, 45, .08), (22, 52, .72), (20, 59, .08)], 1.8, "anatomy-lamb-leg-a"),
        ribbon([(37, 48, .08), (38, 54, .72), (36, 60, .08)], 1.75, "anatomy-lamb-leg-b", "#262522"),
        ribbon([(49, 42, .08), (55, 48, .72), (61, 48, .08)], 1.15, "anatomy-lamb-tail", "#4a4943"),
        ribbon([(21, 34, .08), (28, 29, .72), (36, 29, .08)], .85, "anatomy-lamb-wool-a", "#262522", True),
        ribbon([(26, 40, .08), (34, 37, .72), (44, 39, .08)], .8, "anatomy-lamb-wool-b", "#262522", True),
        ribbon([(27, 46, .08), (36, 48, .72), (45, 45, .08)], .75, "anatomy-lamb-wool-c", "#262522", True),
        dab(58, 37, .7, .55, "#dedbd4"),
    ],
    "pack": [
        mass("M 8 41 C 12 34 20 31 28 34 C 35 36 38 42 35 47 C 30 52 19 52 11 48 C 8 46 7 43 8 41 Z", "#4a4943"),
        mass("M 27 39 C 31 31 40 29 48 33 C 54 36 56 42 53 47 C 48 51 37 50 30 46 Z", "#77746a"),
        mass("M 47 44 C 52 37 60 36 66 40 C 69 43 67 47 63 49 C 57 50 51 49 47 47 Z", "#bcb9af"),
        ribbon([(10, 38, .08), (9, 31, .72), (14, 34, .08)], 1.55, "anatomy-pack-ear-a"),
        ribbon([(17, 35, .08), (20, 29, .72), (23, 36, .08)], 1.45, "anatomy-pack-ear-a2"),
        ribbon([(30, 36, .08), (30, 29, .72), (35, 33, .08)], 1.45, "anatomy-pack-ear-b"),
        ribbon([(38, 33, .08), (42, 27, .72), (44, 34, .08)], 1.4, "anatomy-pack-ear-b2"),
        ribbon([(14, 46, .08), (12, 54, .72), (10, 60, .08)], 1.7, "anatomy-pack-leg-a"),
        ribbon([(25, 46, .08), (27, 54, .72), (26, 60, .08)], 1.6, "anatomy-pack-leg-b", "#262522"),
        ribbon([(38, 45, .08), (38, 53, .72), (36, 59, .08)], 1.7, "anatomy-pack-leg-c"),
        ribbon([(48, 47, .08), (51, 54, .72), (50, 59, .08)], 1.6, "anatomy-pack-leg-d", "#262522"),
        ribbon([(49, 42, .08), (58, 48, .72), (66, 47, .08)], 1.2, "anatomy-pack-tail", "#4a4943"),
        ribbon([(17, 39, .08), (24, 41, .72), (31, 40, .08)], .6, "anatomy-pack-flank", "#262522", True),
        dab(17, 36, .6, .5, "#dedbd4"), dab(37, 33, .6, .5, "#dedbd4"), dab(58, 41, .6, .5, "#262522"),
    ],
    "predator": [
        mass("M 18 39 C 24 32 35 30 44 34 C 51 36 57 40 63 38 C 67 37 68 40 65 43 C 59 47 52 45 47 43 C 43 50 33 54 23 51 C 17 49 15 44 18 39 Z", "#4a4943"),
        mass("M 17 38 C 12 37 9 34 10 30 L 14 25 L 20 29 L 26 25 L 28 32 C 26 36 22 38 17 38 Z", "#262522"),
        ribbon([(29, 46, .08), (27, 53, .72), (23, 59, .08)], 2.0, "anatomy-predator-forepaw"),
        ribbon([(43, 44, .08), (45, 51, .72), (43, 58, .08)], 1.9, "anatomy-predator-hindpaw", "#77746a"),
        ribbon([(51, 40, .08), (58, 46, .72), (65, 47, .08)], 1.3, "anatomy-predator-tail"),
        ribbon([(25, 35, .08), (32, 33, .72), (39, 35, .08)], .7, "anatomy-predator-shoulder", "#bcb9af", True),
        ribbon([(28, 44, .08), (36, 47, .72), (44, 45, .08)], .65, "anatomy-predator-rib", "#262522", True),
        dab(17, 31, .7, .55, "#dedbd4"),
    ],
    "prey": [
        mass("M 21 43 C 21 36 27 31 35 31 C 44 31 51 37 52 44 C 52 51 46 55 37 55 C 28 55 22 51 21 43 Z", "#bcb9af"),
        mass("M 25 35 C 20 31 20 24 22 17 C 28 21 31 27 30 33 C 33 27 38 23 43 24 C 42 31 38 36 32 38 Z", "#77746a"),
        mass("M 20 40 C 15 40 12 37 13 34 C 16 32 20 33 23 35 L 28 37 C 27 40 24 41 20 40 Z", "#4a4943"),
        ribbon([(29, 48, .08), (26, 54, .72), (23, 59, .08)], 1.7, "anatomy-prey-forepaw"),
        ribbon([(43, 48, .08), (47, 54, .72), (51, 57, .08)], 1.7, "anatomy-prey-hindfoot", "#4a4943"),
        ribbon([(47, 37, .08), (56, 39, .72), (62, 36, .08)], 1.15, "anatomy-prey-tail", "#77746a"),
        ribbon([(28, 39, .08), (35, 35, .72), (43, 36, .08)], .65, "anatomy-prey-back", "#262522", True),
        ribbon([(28, 46, .08), (36, 50, .72), (44, 48, .08)], .6, "anatomy-prey-belly", "#262522", True),
        dab(18, 35, .7, .55, "#262522"),
    ],
    "squirrel": [
        mass("M 25 41 C 27 34 33 29 40 30 C 48 31 52 38 50 46 C 48 53 40 57 33 54 C 27 52 24 47 25 41 Z", "#77746a"),
        mass("M 29 35 C 26 31 27 25 32 22 C 38 19 44 22 46 28 C 46 32 43 35 39 37 Z", "#4a4943"),
        mass("M 43 45 C 49 40 55 34 56 27 C 57 20 53 15 49 14 C 45 14 42 17 43 21 C 44 24 49 26 51 30 C 52 35 48 39 44 42 C 40 44 39 47 43 45 Z", "#4a4943"),
        ribbon([(30, 45, .08), (27, 53, .72), (24, 59, .08)], 1.8, "anatomy-squirrel-foot"),
        ribbon([(42, 47, .08), (46, 53, .72), (51, 56, .08)], 1.7, "anatomy-squirrel-hindfoot", "#262522"),
        ribbon([(29, 39, .08), (24, 42, .72), (20, 45, .08)], 1.25, "anatomy-squirrel-forepaw", "#262522"),
        ribbon([(47, 17, .08), (51, 22, .72), (53, 29, .08)], .7, "anatomy-squirrel-tail-fur", "#bcb9af", True),
        ribbon([(30, 35, .08), (36, 32, .72), (43, 34, .08)], .65, "anatomy-squirrel-rib", "#262522", True),
        dab(37, 27, .7, .55, "#dedbd4"),
    ],
}

# Keep the stroke-led PLATES written above as the production studies.  The
# ANATOMICAL alternatives remain nearby as reference experiments, but their
# large oval body masses read as assembled pictograms rather than irreversible
# brush gestures and must not overwrite the plate treatment.

# Species-specific dry marks: short broken touches that follow the body rather
# than forming a repeated hatch pattern.  They are important at full glyph
# size because they turn a flat wash into a drawn animal.
append_detail("calf", [
    *dry([(23, 34, .08), (29, 31, .48), (36, 31, .86), (44, 33, .5), (51, 36, .08)], .72, "calf-fur"),
    *dry([(28, 40, .08), (34, 42, .62), (40, 42, .9), (47, 40, .08)], .56, "calf-flank"),
])
append_detail("colony", [
    *dry([(13, 35, .08), (16, 39, .62), (19, 46, .9), (20, 50, .08)], .6, "colony-feather-a"),
    *dry([(31, 32, .08), (35, 37, .62), (39, 45, .9), (40, 50, .08)], .62, "colony-feather-b"),
    *dry([(49, 37, .08), (53, 41, .62), (57, 47, .9), (58, 51, .08)], .55, "colony-feather-c"),
])
append_detail("flock", [
    *dry([(12, 33, .08), (15, 31, .62), (20, 32, .9), (23, 34, .08)], .52, "flock-feather-a"),
    *dry([(32, 25, .08), (36, 22, .62), (41, 23, .9), (45, 25, .08)], .52, "flock-feather-b"),
    *dry([(52, 39, .08), (56, 36, .62), (61, 37, .9), (65, 39, .08)], .52, "flock-feather-c"),
])
append_detail("herd", [
    *dry([(13, 36, .08), (19, 35, .62), (25, 37, .9), (31, 40, .08)], .7, "herd-coat-a"),
    *dry([(34, 34, .08), (40, 32, .62), (47, 34, .9), (53, 38, .08)], .7, "herd-coat-b"),
])
append_detail("lamb", [
    *dry([(20, 35, .08), (26, 30, .62), (34, 28, .9), (43, 31, .08)], .72, "lamb-wool-a"),
    *dry([(22, 42, .08), (29, 46, .62), (37, 47, .9), (46, 44, .08)], .68, "lamb-wool-b"),
])
append_detail("pack", [
    *dry([(12, 38, .08), (18, 35, .62), (25, 37, .9), (32, 41, .08)], .7, "pack-fur-a"),
    *dry([(31, 37, .08), (37, 33, .62), (44, 35, .9), (51, 40, .08)], .68, "pack-fur-b"),
])
append_detail("predator", [
    *dry([(20, 39, .08), (27, 34, .62), (35, 34, .9), (44, 37, .08)], .76, "predator-fur-a"),
    *dry([(23, 45, .08), (31, 48, .62), (39, 47, .9), (45, 44, .08)], .64, "predator-fur-b"),
])
append_detail("prey", [
    *dry([(24, 41, .08), (30, 35, .62), (37, 34, .9), (46, 39, .08)], .64, "prey-fur-a"),
    *dry([(28, 47, .08), (34, 50, .62), (42, 49, .9), (48, 45, .08)], .58, "prey-fur-b"),
])
append_detail("squirrel", [
    *dry([(28, 39, .08), (33, 34, .62), (39, 33, .9), (46, 37, .08)], .7, "squirrel-fur-a"),
    *dry([(46, 20, .08), (50, 24, .62), (52, 29, .9), (49, 35, .08)], .72, "squirrel-tail-fur"),
])

print("redrew all 10 animal PUA glyphs as irregular nineteenth-century naturalist brush studies")
