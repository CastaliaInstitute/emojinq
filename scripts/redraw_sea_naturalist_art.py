#!/usr/bin/env python3
"""Render the sea-creature PUA family as species-specific vector brush studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "sea_creatures"


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*v) for v in values]


def ribbon(values, width, seed, color="#262522", dry=False) -> str:
    d = stroke_path(p(*values), width=width, seed=seed, wobble=.25, taper_start=.10, taper_end=.10)
    return f'<path class="{"ink-dry" if dry else "ink-wash"}" d="{d}" fill="{color}" data-ink-brush-pass="{"dry-edge-v1" if dry else "loaded-ribbon-v2"}"/>'


def dry(values, width, seed, color="#77746a") -> list[str]:
    return [f'<path class="ink-dry" d="{d}" fill="{color}" data-ink-brush-pass="dry-fragment-v1"/>' for d in dry_brush_paths(p(*values), width=width, seed=seed, breaks=2)]


def mass(d, fill="#bcb9af", detail="loaded-mass-v2") -> str:
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="sea creatures / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>sea creatures / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


write("coral", [
    ribbon([(36, 58, .08), (34, 47, .72), (36, 36, .96), (34, 25, .08)], 2.5, "coral-stem"),
    ribbon([(35, 38, .08), (28, 30, .72), (22, 20, .08)], 1.9, "coral-left", "#4a4943"),
    ribbon([(36, 32, .08), (44, 25, .72), (49, 16, .08)], 2.0, "coral-right"),
    ribbon([(31, 46, .08), (24, 40, .72), (17, 38, .08)], 1.5, "coral-low-left", "#77746a"),
    ribbon([(38, 43, .08), (46, 37, .72), (55, 35, .08)], 1.55, "coral-low-right", "#4a4943"),
    *dry([(22, 20, .08), (25, 15, .72), (28, 12, .08)], .72, "coral-tip-l"),
    *dry([(49, 16, .08), (53, 11, .72), (56, 10, .08)], .72, "coral-tip-r"),
])

write("crab", [
    mass("M 22 31 C 26 24 46 23 51 31 C 54 39 48 46 36 47 C 24 46 18 39 22 31 Z", "#77746a"),
    mass("M 15 30 C 10 26 7 29 9 34 C 11 38 16 38 21 35 L 22 31 Z", "#4a4943"),
    mass("M 57 30 C 62 26 65 29 63 34 C 61 38 56 38 51 35 L 50 31 Z", "#262522"),
    ribbon([(25, 38, .08), (19, 44, .72), (14, 47, .08)], 1.45, "crab-leg-l1"),
    ribbon([(29, 42, .08), (25, 49, .72), (22, 53, .08)], 1.3, "crab-leg-l2", "#4a4943"),
    ribbon([(45, 38, .08), (52, 44, .72), (57, 47, .08)], 1.45, "crab-leg-r1"),
    ribbon([(41, 42, .08), (46, 49, .72), (50, 53, .08)], 1.3, "crab-leg-r2", "#77746a"),
    dab(29, 29, 1.5, 2.0), dab(43, 29, 1.5, 2.0),
    ribbon([(27, 35, .08), (36, 38, .72), (45, 35, .08)], .8, "crab-shell-ridge", "#bcb9af", True),
])

write("dolphin", [
    mass("M 11 39 C 19 30 31 27 44 29 C 51 30 57 34 61 38 C 55 39 51 42 47 46 C 39 52 27 53 18 48 C 14 46 11 43 11 39 Z", "#77746a"),
    mass("M 44 31 L 50 24 L 52 34 Z", "#262522"),
    ribbon([(47, 44, .08), (54, 48, .72), (61, 51, .08)], 2.1, "dolphin-tail-upper"),
    ribbon([(47, 45, .08), (54, 43, .72), (62, 42, .08)], 1.6, "dolphin-tail-lower", "#4a4943"),
    ribbon([(25, 34, .08), (34, 36, .72), (42, 35, .08)], 1.0, "dolphin-back", "#bcb9af", True),
    dab(53, 34, 1.2, 1.0),
])

write("jellyfish", [
    mass("M 18 32 C 18 23 26 17 36 17 C 46 17 54 23 54 32 C 49 35 42 36 36 35 C 29 36 23 35 18 32 Z", "#bcb9af"),
    ribbon([(23, 31, .08), (29, 28, .72), (36, 29, .96), (46, 28, .08)], 1.4, "jelly-cap", "#262522"),
    ribbon([(24, 35, .08), (23, 44, .72), (25, 54, .08)], 1.25, "jelly-tentacle-l", "#77746a"),
    ribbon([(31, 35, .08), (30, 44, .72), (33, 57, .08)], 1.5, "jelly-tentacle-ml"),
    ribbon([(39, 35, .08), (40, 45, .72), (38, 56, .08)], 1.45, "jelly-tentacle-mr", "#4a4943"),
    ribbon([(47, 34, .08), (49, 43, .72), (47, 52, .08)], 1.2, "jelly-tentacle-r", "#77746a"),
])

write("lobster", [
    mass("M 19 34 C 26 28 39 28 49 33 C 54 36 54 43 48 47 C 37 52 23 48 19 42 C 17 39 17 36 19 34 Z", "#77746a"),
    mass("M 13 31 C 8 26 5 29 7 34 C 9 38 14 39 19 36 L 20 33 Z", "#262522"),
    mass("M 53 32 C 59 27 64 29 64 34 C 64 39 58 40 52 37 Z", "#4a4943"),
    ribbon([(24, 43, .08), (19, 50, .72), (14, 54, .08)], 1.4, "lobster-leg-l"),
    ribbon([(31, 46, .08), (29, 53, .72), (27, 57, .08)], 1.25, "lobster-leg-ml", "#4a4943"),
    ribbon([(42, 44, .08), (47, 50, .72), (53, 54, .08)], 1.35, "lobster-leg-r"),
    ribbon([(21, 32, .08), (15, 23, .72), (10, 18, .08)], .9, "lobster-antenna-l", "#77746a", True),
    ribbon([(49, 32, .08), (55, 23, .72), (61, 18, .08)], .9, "lobster-antenna-r", "#262522", True),
    ribbon([(27, 35, .08), (37, 38, .72), (47, 35, .08)], .8, "lobster-shell", "#bcb9af", True),
])

write("manta", [
    mass("M 36 25 C 25 22 15 19 8 23 C 14 31 21 36 29 39 C 32 40 34 44 36 50 C 38 44 40 40 43 39 C 51 36 58 31 64 23 C 57 19 47 22 36 25 Z", "#77746a"),
    ribbon([(14, 24, .08), (25, 27, .72), (36, 31, .96), (48, 27, .72), (60, 23, .08)], 1.6, "manta-wing", "#262522"),
    ribbon([(36, 30, .08), (36, 40, .72), (38, 56, .08)], 1.15, "manta-tail", "#4a4943"),
    dab(33, 28, 1.1, .9), dab(39, 28, 1.1, .9),
])

write("nautilus", [
    mass("M 36 13 C 49 13 58 23 58 36 C 58 49 48 58 36 58 C 23 58 14 49 14 37 C 14 25 23 16 36 13 Z", "#bcb9af"),
    ribbon([(48, 25, .08), (42, 20, .72), (33, 21, .96), (27, 27, .90), (27, 36, .82), (33, 42, .72), (41, 40, .96), (44, 34, .72), (40, 29, .08)], 2.2, "nautilus-spiral"),
    ribbon([(22, 47, .08), (30, 52, .72), (41, 52, .08)], .8, "nautilus-shell-edge", "#77746a", True),
])

write("octopus", [
    mass("M 25 28 C 25 20 30 16 36 16 C 43 16 48 21 48 29 C 48 36 43 39 36 39 C 29 39 24 35 25 28 Z", "#77746a"),
    ribbon([(27, 35, .08), (21, 43, .72), (14, 47, .08)], 2.0, "octopus-arm-1"),
    ribbon([(30, 37, .08), (27, 47, .72), (23, 55, .08)], 2.0, "octopus-arm-2", "#4a4943"),
    ribbon([(34, 38, .08), (33, 48, .72), (32, 57, .08)], 1.85, "octopus-arm-3"),
    ribbon([(38, 38, .08), (40, 48, .72), (44, 56, .08)], 1.85, "octopus-arm-4", "#4a4943"),
    ribbon([(42, 37, .08), (48, 45, .72), (56, 49, .08)], 1.95, "octopus-arm-5"),
    ribbon([(45, 34, .08), (53, 39, .72), (61, 40, .08)], 1.7, "octopus-arm-6", "#4a4943"),
    dab(32, 27, 1.1, 1.3), dab(41, 27, 1.1, 1.3),
    ribbon([(28, 31, .08), (36, 34, .72), (44, 31, .08)], .65, "octopus-face", "#bcb9af", True),
])

write("seahorse", [
    ribbon([(42, 18, .08), (34, 19, .72), (31, 27, .96), (35, 34, .86), (39, 41, .72), (36, 49, .92), (29, 54, .08)], 3.0, "seahorse-body"),
    mass("M 38 17 C 42 13 49 14 52 18 C 54 21 51 24 47 24 L 40 22 Z", "#77746a"),
    ribbon([(47, 18, .08), (54, 17, .72), (61, 19, .08)], 1.1, "seahorse-snout", "#262522"),
    ribbon([(32, 31, .08), (25, 34, .72), (20, 39, .08)], 1.5, "seahorse-fin", "#4a4943"),
    ribbon([(34, 42, .08), (28, 46, .72), (24, 51, .08)], 1.2, "seahorse-tail", "#77746a", True),
    dab(47, 18, 1.0, .9),
])

write("shark", [
    mass("M 10 38 C 19 30 31 27 45 29 C 53 30 59 34 63 39 C 56 40 51 43 45 47 C 35 53 22 52 14 46 C 11 44 9 41 10 38 Z", "#4a4943"),
    mass("M 38 30 L 43 20 L 48 32 Z", "#262522"),
    ribbon([(14, 39, .08), (24, 37, .72), (36, 37, .96), (49, 39, .08)], 1.0, "shark-lateral", "#bcb9af", True),
    ribbon([(45, 46, .08), (54, 51, .72), (62, 50, .08)], 1.7, "shark-tail-l"),
    ribbon([(45, 46, .08), (54, 42, .72), (62, 42, .08)], 1.4, "shark-tail-u", "#77746a"),
    dab(18, 36, 1.1, .9),
])

write("turtle", [
    mass("M 18 35 C 20 24 29 19 39 20 C 50 21 57 29 55 40 C 53 50 43 55 32 53 C 22 51 16 44 18 35 Z", "#77746a"),
    ribbon([(22, 32, .08), (31, 27, .72), (42, 28, .96), (51, 34, .08)], 1.3, "turtle-shell-ridge", "#262522"),
    ribbon([(28, 23, .08), (29, 35, .72), (29, 48, .08)], .9, "turtle-shell-seam", "#bcb9af", True),
    mass("M 53 34 C 58 31 63 33 64 37 C 64 41 59 43 54 41 Z", "#4a4943"),
    ribbon([(23, 42, .08), (17, 48, .72), (12, 50, .08)], 1.65, "turtle-flipper-l"),
    ribbon([(46, 43, .08), (52, 49, .72), (57, 51, .08)], 1.65, "turtle-flipper-r", "#4a4943"),
])

write("whale", [
    mass("M 9 39 C 18 29 30 27 43 29 C 52 30 58 34 63 39 C 58 41 54 45 48 48 C 36 54 21 52 13 47 C 10 45 8 42 9 39 Z", "#77746a"),
    ribbon([(18, 34, .08), (28, 36, .72), (39, 36, .96), (50, 39, .08)], 1.1, "whale-back", "#bcb9af", True),
    ribbon([(47, 46, .08), (55, 52, .72), (62, 51, .08)], 2.0, "whale-tail-l"),
    ribbon([(47, 46, .08), (54, 42, .72), (62, 43, .08)], 1.6, "whale-tail-u", "#4a4943"),
    ribbon([(29, 29, .08), (31, 23, .72), (34, 19, .08)], 1.1, "whale-spout", "#77746a", True),
    dab(18, 35, 1.0, .8),
])

print("redrew all 12 sea-creature PUA glyphs as vector brush studies")
