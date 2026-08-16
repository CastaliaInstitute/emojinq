#!/usr/bin/env python3
"""Replace the remaining stick-like body action glyphs with ink studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "body"


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*v) for v in values]


def ribbon(values, width, seed, color="#262522", dry=False) -> str:
    d = stroke_path(p(*values), width=width, seed=f"action-{seed}", wobble=.34, taper_start=.12, taper_end=.15)
    brush = "dry-edge-v1" if dry else "loaded-ribbon-v2"
    cls = "ink-dry" if dry else "ink-wash"
    return f'<path class="{cls}" d="{d}" fill="{color}" data-ink-brush-pass="{brush}"/>'


def dry(values, width, seed, color="#77746a") -> list[str]:
    return [f'<path class="ink-dry" d="{d}" fill="{color}" data-ink-brush-pass="dry-fragment-v1"/>' for d in dry_brush_paths(p(*values), width=width, seed=f"action-{seed}", breaks=2)]


def mass(d, fill="#77746a") -> str:
    return f'<path class="ink-wash" d="{d}" fill="{fill}" data-ink-brush-pass="loaded-mass-v2"/>'


def dab(cx, cy, rx, ry, fill="#262522") -> str:
    return f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" data-ink-brush-pass="loaded-dab-v1"/>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    cp = re.search(r'data-pua="([^"]+)"', source)
    if not cp:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="body / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>body / {name} — nineteenth-century naturalist gesture study</title>{''.join(marks)}</svg>
''')


# Push: a forward-leaning figure whose bent knees, shoulders, forearms, and
# hands visibly transfer weight into an irregular stone.
write("push", [
    mass("M 16 15 C 18 11 23 11 26 14 C 28 16 27 19 24 21 C 21 22 18 20 17 18 Z", "#262522"),
    mass("M 21 24 C 25 22 31 24 34 28 C 37 33 37 39 33 43 C 29 45 23 42 21 38 C 19 33 19 27 21 24 Z", "#4a4943"),
    ribbon([(22, 21, .08), (24, 24, .72), (27, 27, .08)], 1.7, "push-neck", "#77746a"),
    ribbon([(25, 39, .08), (22, 45, .72), (17, 51, .92), (11, 55, .08)], 3.7, "push-back-leg"),
    ribbon([(31, 40, .08), (34, 46, .72), (40, 51, .92), (48, 53, .08)], 3.5, "push-front-leg", "#262522"),
    ribbon([(11, 55, .08), (15, 56, .72), (20, 54, .08)], 1.55, "push-back-foot", "#77746a", True),
    ribbon([(47, 53, .08), (52, 55, .72), (56, 53, .08)], 1.5, "push-front-foot", "#262522", True),
    ribbon([(24, 27, .08), (30, 28, .62), (37, 31, .9), (47, 34, .08)], 3.5, "push-upper-arm"),
    ribbon([(25, 33, .08), (31, 34, .62), (38, 37, .9), (47, 39, .08)], 3.1, "push-lower-arm", "#77746a"),
    mass("M 50 25 C 56 22 63 24 65 30 C 67 36 65 43 61 47 C 56 50 50 47 48 42 C 46 36 47 29 50 25 Z", "#bcb9af"),
    ribbon([(49, 30, .08), (56, 33, .72), (62, 38, .08)], .75, "push-stone-grain", "#77746a", True),
    ribbon([(28, 27, .08), (34, 30, .72), (40, 32, .08)], .82, "push-shoulder-fold", "#bcb9af", True),
    ribbon([(28, 35, .08), (34, 37, .72), (41, 39, .08)], .72, "push-sleeve-fold", "#dedbd4", True),
    ribbon([(46, 34, .08), (49, 35, .72), (52, 35, .08)], .6, "push-fingers-a", "#262522", True),
    ribbon([(46, 39, .08), (49, 40, .72), (52, 40, .08)], .55, "push-fingers-b", "#262522", True),
    dab(22, 16, .62, .52, "#dedbd4"),
])

# Reach: an upright figure with a curved spine, lifted shoulder, clear elbow,
# long forearm, and a hand arriving at a leaf rather than a straight stick.
write("reach", [
    mass("M 26 12 C 29 9 34 10 36 13 C 37 16 35 19 32 20 C 29 20 26 18 25 16 Z", "#262522"),
    mass("M 26 23 C 30 20 36 22 38 27 C 40 33 39 39 35 43 C 31 45 26 42 25 37 C 24 32 24 26 26 23 Z", "#4a4943"),
    ribbon([(31, 20, .08), (31, 22, .72), (32, 25, .08)], 1.65, "reach-neck", "#77746a"),
    ribbon([(30, 40, .08), (27, 47, .72), (22, 53, .9), (16, 57, .08)], 3.0, "reach-back-leg"),
    ribbon([(35, 40, .08), (38, 47, .72), (43, 53, .9), (49, 55, .08)], 2.9, "reach-front-leg", "#262522"),
    ribbon([(15, 57, .08), (19, 58, .72), (24, 56, .08)], 1.35, "reach-back-foot", "#77746a", True),
    ribbon([(48, 55, .08), (53, 56, .72), (57, 54, .08)], 1.3, "reach-front-foot", "#262522", True),
    ribbon([(28, 27, .08), (34, 26, .55), (40, 22, .82), (47, 17, .08)], 3.0, "reach-raised-arm", "#262522"),
    ribbon([(27, 31, .08), (23, 35, .68), (20, 40, .08)], 1.55, "reach-resting-arm", "#77746a"),
    mass("M 54 10 C 59 8 64 10 66 13 C 63 17 58 18 53 15 Z", "#77746a"),
    ribbon([(47, 17, .08), (51, 14, .72), (56, 13, .08)], .78, "reach-finger-a", "#262522", True),
    ribbon([(47, 18, .08), (51, 16, .72), (56, 15, .08)], .55, "reach-finger-b", "#262522", True),
    ribbon([(29, 27, .08), (35, 25, .72), (41, 21, .08)], .75, "reach-shoulder-fold", "#bcb9af", True),
    ribbon([(29, 36, .08), (34, 38, .72), (37, 40, .08)], .68, "reach-torso-fold", "#dedbd4", True),
    dab(31, 14, .62, .52, "#dedbd4"),
])

# Walk: a three-quarter coat study with a planted rear leg, lifted knee,
# counter-swinging arms, and a face turned in the direction of travel.
write("walk", [
    mass("M 31 10 C 34 7 39 8 41 11 C 43 14 41 17 38 19 C 35 20 32 17 31 15 Z", "#262522"),
    mass("M 29 22 C 33 19 39 20 42 24 C 45 29 44 36 40 41 C 36 44 30 42 28 37 C 26 32 27 25 29 22 Z", "#4a4943"),
    ribbon([(36, 18, .08), (36, 21, .72), (36, 24, .08)], 1.65, "walk-neck", "#77746a"),
    ribbon([(32, 39, .08), (28, 46, .62), (22, 52, .88), (15, 57, .08)], 3.7, "walk-planted-leg"),
    ribbon([(38, 39, .08), (43, 44, .62), (48, 43, .88), (54, 38, .08)], 3.35, "walk-lifted-leg", "#262522"),
    ribbon([(15, 57, .08), (20, 58, .72), (25, 56, .08)], 1.5, "walk-planted-foot", "#77746a", True),
    ribbon([(53, 38, .08), (57, 37, .72), (61, 39, .08)], 1.35, "walk-lifted-foot", "#262522", True),
    ribbon([(31, 27, .08), (25, 31, .72), (20, 37, .08)], 1.9, "walk-back-arm", "#77746a"),
    ribbon([(40, 26, .08), (46, 31, .72), (52, 36, .08)], 1.9, "walk-front-arm", "#262522"),
    ribbon([(30, 25, .08), (34, 31, .72), (35, 37, .08)], .72, "walk-coat-fold-a", "#bcb9af", True),
    ribbon([(39, 27, .08), (37, 33, .72), (38, 39, .08)], .7, "walk-coat-fold-b", "#dedbd4", True),
    ribbon([(23, 48, .08), (28, 50, .72), (32, 49, .08)], .62, "walk-knee-fold", "#bcb9af", True),
    *dry([(29, 23, .08), (34, 22, .62), (40, 24, .9), (42, 29, .08)], .62, "walk-coat-edge"),
    dab(36, 12, .62, .52, "#dedbd4"),
])

print("redrew push, reach, and walk as anatomical naturalist gesture studies")
