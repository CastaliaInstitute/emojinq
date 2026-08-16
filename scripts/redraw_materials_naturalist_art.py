#!/usr/bin/env python3
"""Render the materials PUA family as layered, vector sumi-e material studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "materials"


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*v) for v in values]


def ribbon(values, width, seed, color="#262522", dry=False) -> str:
    color = {
        "#bcb9af": "#74716a",
        "#77746a": "#595751",
    }.get(color.lower(), color)
    width = max(width * 1.28, 1.15)
    d = stroke_path(p(*values), width=width, seed=seed, wobble=.24, taper_start=.12, taper_end=.10)
    return f'<path class="{"ink-dry" if dry else "ink-wash"}" d="{d}" fill="{color}" data-ink-brush-pass="{"dry-edge-v1" if dry else "loaded-ribbon-v2"}"/>'


def dry(values, width, seed, color="#77746a") -> list[str]:
    return [f'<path class="ink-dry" d="{d}" fill="{color}" data-ink-brush-pass="dry-fragment-v1"/>' for d in dry_brush_paths(p(*values), width=width, seed=seed, breaks=2)]


def mass(d, fill="#bcb9af", detail="loaded-mass-v2") -> str:
    return f'<path class="ink-wash" d="{d}" fill="{fill}" data-ink-brush-pass="{detail}"/>'


def dab(cx, cy, rx, ry, fill="#4a4943") -> str:
    return f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" data-ink-brush-pass="loaded-dab-v1"/>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    cp = re.search(r'data-pua="([^"]+)"', source)
    if not cp:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="materials / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>materials / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


write("clay", [
    ribbon([(23, 19, .08), (35, 17, .8), (48, 20, .08)], 2.7, "clay-rim"),
    ribbon([(25, 21, .08), (28, 30, .72), (24, 43, .95), (31, 53, .08)], 1.7, "clay-left", "#4a4943"),
    ribbon([(47, 21, .08), (44, 31, .72), (49, 43, .95), (41, 54, .08)], 1.5, "clay-right", "#77746a", True),
    ribbon([(30, 53, .08), (36, 56, .8), (42, 53, .08)], 1.15, "clay-foot", "#4a4943"),
    ribbon([(27, 36, .08), (36, 39, .8), (46, 36, .08)], .75, "clay-firing", "#77746a", True),
])
write("cloth", [
    ribbon([(14, 27, .08), (27, 22, .76), (42, 25, .95), (58, 21, .08)], 3.4, "cloth-loaded-fold", "#262522"),
    ribbon([(16, 30, .08), (20, 40, .72), (18, 51, .08)], 1.25, "cloth-left-edge", "#4a4943"),
    ribbon([(57, 24, .08), (53, 36, .72), (55, 48, .08)], 1.0, "cloth-right-edge", "#77746a", True),
    ribbon([(19, 51, .08), (32, 47, .72), (44, 51, .92), (55, 48, .08)], 1.55, "cloth-lower-fold", "#4a4943"),
    ribbon([(29, 27, .08), (34, 36, .72), (31, 45, .08)], .85, "cloth-crease", "#77746a", True),
])
write("fiber", [
    ribbon([(14, 39, .08), (23, 27, .72), (36, 25, .96), (49, 31, .9), (58, 41, .08)], 4.2, "fiber-bundle"),
    ribbon([(16, 45, .08), (27, 36, .72), (40, 35, .96), (54, 43, .08)], 1.05, "fiber-strand-1", "#77746a", True),
    ribbon([(20, 51, .08), (31, 43, .72), (44, 43, .96), (57, 48, .08)], .9, "fiber-strand-2", "#bcb9af", True),
])
write("glass", [
    ribbon([(23, 18, .08), (35, 16, .78), (49, 19, .08)], 1.5, "glass-rim", "#262522"),
    ribbon([(24, 20, .08), (25, 34, .72), (27, 49, .08)], 1.0, "glass-left", "#77746a", True),
    ribbon([(49, 20, .08), (47, 35, .72), (46, 49, .08)], 1.2, "glass-right", "#4a4943"),
    ribbon([(27, 49, .08), (36, 53, .76), (46, 49, .08)], 1.15, "glass-base", "#4a4943"),
    ribbon([(30, 23, .08), (29, 31, .72), (31, 39, .08)], .62, "glass-glint", "#77746a", True),
])
write("leather", [
    mass("M 19 29 C 26 25 46 25 53 30 L 54 49 C 47 55 27 55 18 49 Z", "#4a4943"),
    ribbon([(20, 30, .08), (29, 35, .72), (41, 34, .95), (52, 30, .08)], 1.35, "leather-satchel-flap", "#262522"),
    ribbon([(18, 29, .08), (13, 22, .72), (17, 16, .95), (24, 26, .08)], 1.45, "leather-satchel-strap", "#77746a", True),
    ribbon([(27, 42, .08), (35, 45, .72), (45, 42, .08)], 1.0, "leather-stitch", "#bcb9af", True),
])
write("metal", [
    ribbon([(17, 39, .08), (25, 24, .72), (42, 19, .95), (56, 29, .7), (53, 45, .08), (39, 53, .72), (23, 49, .08)], 2.45, "metal-ingot", "#262522"),
    ribbon([(25, 25, .08), (38, 34, .85), (55, 29, .08)], 1.1, "metal-facet-high", "#bcb9af", True),
    ribbon([(38, 34, .08), (39, 51, .78), (23, 48, .08)], 1.0, "metal-facet-low", "#77746a", True),
    ribbon([(29, 22, .08), (37, 20, .8), (44, 23, .08)], .72, "metal-sheen", "#77746a", True),
])
write("paper", [
    ribbon([(18, 17, .08), (30, 15, .72), (43, 17, .95), (54, 16, .08)], 1.65, "paper-top", "#4a4943"),
    ribbon([(18, 18, .08), (17, 34, .72), (19, 52, .08)], 1.2, "paper-left", "#77746a", True),
    ribbon([(54, 17, .08), (52, 30, .72), (55, 43, .95), (49, 52, .08)], 1.4, "paper-torn-right", "#262522"),
    ribbon([(19, 52, .08), (30, 54, .72), (40, 51, .95), (49, 53, .08)], 1.15, "paper-bottom", "#4a4943"),
    ribbon([(42, 17, .08), (45, 25, .72), (52, 29, .08)], .9, "paper-fold", "#77746a", True),
    ribbon([(24, 31, .08), (34, 29, .72), (44, 31, .08)], .62, "paper-fiber", "#77746a", True),
])
write("plastic", [
    ribbon([(29, 17, .08), (36, 15, .78), (44, 18, .08)], 2.0, "plastic-neck", "#262522"),
    ribbon([(29, 19, .08), (28, 26, .72), (23, 33, .95), (22, 46, .72), (29, 54, .08)], 1.55, "plastic-left", "#4a4943"),
    ribbon([(44, 19, .08), (44, 27, .72), (50, 34, .95), (49, 47, .72), (42, 55, .08)], 1.35, "plastic-right", "#77746a", True),
    ribbon([(29, 54, .08), (36, 57, .78), (42, 55, .08)], 1.15, "plastic-base", "#4a4943"),
    ribbon([(28, 34, .08), (36, 32, .72), (46, 34, .08)], .75, "plastic-glint", "#77746a", True),
])
write("sand", [
    ribbon([(10, 50, .08), (23, 40, .72), (37, 42, .95), (49, 36, .72), (63, 48, .08)], 2.8, "sand-dune-host", "#4a4943"),
    ribbon([(16, 54, .08), (30, 48, .72), (44, 51, .95), (59, 48, .08)], 1.05, "sand-dune-guest", "#77746a", True),
    dab(24, 43, 1.2, .8, "#77746a"), dab(39, 45, 1.0, .7, "#4a4943"), dab(53, 41, 1.25, .8, "#77746a"),
])
write("stone", [
    ribbon([(15, 43, .08), (21, 31, .72), (34, 20, .95), (48, 24, .72), (57, 36, .08), (51, 50, .72), (36, 55, .95), (21, 51, .08)], 2.35, "stone-contour", "#262522"),
    ribbon([(34, 21, .08), (36, 36, .8), (22, 50, .08)], 1.05, "stone-facet-left", "#77746a", True),
    ribbon([(36, 36, .08), (49, 25, .8), (56, 36, .08)], .95, "stone-facet-right", "#bcb9af", True),
    ribbon([(36, 36, .08), (49, 49, .8), (36, 54, .08)], .72, "stone-fracture", "#4a4943"),
])
write("thread", [
    ribbon([(22, 23, .08), (36, 19, .8), (50, 23, .08)], 1.8, "thread-top", "#262522"),
    ribbon([(23, 24, .08), (23, 36, .72), (24, 49, .08)], 1.05, "thread-left", "#77746a", True),
    ribbon([(50, 24, .08), (49, 37, .72), (49, 49, .08)], 1.15, "thread-right", "#4a4943"),
    ribbon([(24, 49, .08), (36, 53, .8), (49, 49, .08)], 1.4, "thread-bottom", "#262522"),
    ribbon([(24, 30, .08), (36, 34, .8), (49, 30, .08)], .85, "thread-coil-a", "#77746a", True),
    ribbon([(24, 39, .08), (36, 43, .8), (49, 39, .08)], .8, "thread-coil-b", "#bcb9af", True),
    ribbon([(49, 49, .08), (56, 53, .72), (63, 49, .08)], 1.0, "thread-tail", "#4a4943"),
])

print("redrew all 11 materials PUA glyphs as vector brush studies")
