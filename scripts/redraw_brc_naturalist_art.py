#!/usr/bin/env python3
"""Redraw the Black Rock City PUA family as sumi-e playa studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "brc"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522", *, dry=False) -> str:
    d = stroke_path(
        points(*values), width=width, seed=seed, wobble=.26,
        taper_start=.10, taper_end=.08,
    )
    class_name = "ink-dry" if dry else "ink-wash"
    brush_pass = "dry-edge-v2" if dry else "loaded-ribbon-v2"
    return (
        f'<path class="{class_name}" d="{d}" fill="{color}" '
        f'data-ink-brush-pass="{brush_pass}"/>'
    )


def dab(cx, cy, rx, ry, color="#262522") -> str:
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="brc / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>brc / {name} — naturalist sumi-e playa study</title>{''.join(marks)}</svg>
''')


write("art-car", [
    '<path class="ink-wash" d="M12 39 C18 35 25 34 31 34 L48 35 C54 36 59 40 61 46 L58 50 L14 50 C11 47 10 43 12 39 Z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v2"/>',
    ribbon([(22, 36, .10), (28, 28, .72), (39, 27, .92), (48, 36, .08)], 2.0, "art-car-canopy"),
    ribbon([(28, 36, .10), (29, 29, .72), (30, 27, .08)], .75, "art-car-window-post", "#bcb9af", dry=True),
    dab(21, 52, 4.5, 4.2, "#262522"),
    dab(52, 52, 4.2, 3.9, "#262522"),
    dab(21, 52, 1.5, 1.4, "#bcb9af"),
    dab(52, 52, 1.4, 1.3, "#bcb9af"),
    ribbon([(38, 29, .10), (37, 20, .72), (41, 14, .08)], 1.4, "art-car-mast"),
    ribbon([(41, 14, .10), (47, 10, .72), (53, 12, .08)], 1.8, "art-car-banner", "#262522"),
    ribbon([(10, 47, .10), (14, 47, .72), (18, 47, .08)], 1.0, "art-car-bumper-front", "#262522"),
    ribbon([(57, 47, .10), (62, 47, .72), (66, 45, .08)], .8, "art-car-bumper-rear", "#77746a", dry=True),
    ribbon([(14, 59, .10), (28, 57, .72), (43, 59, .90), (59, 57, .08)], .65, "art-car-playa", "#bcb9af", dry=True),
])


write("man", [
    dab(36, 14, 4.1, 4.2, "#262522"),
    ribbon([(36, 19, .10), (36, 31, .84), (35, 43, .08)], 3.8, "man-axis", "#4a4943"),
    ribbon([(35, 27, .10), (25, 20, .72), (15, 11, .08)], 2.1, "man-arm-left"),
    ribbon([(37, 27, .10), (47, 20, .72), (57, 10, .08)], 1.55, "man-arm-right", "#77746a", dry=True),
    ribbon([(35, 42, .10), (27, 53, .72), (20, 63, .08)], 2.0, "man-leg-left"),
    ribbon([(36, 42, .10), (45, 53, .72), (52, 62, .08)], 1.4, "man-leg-right", "#77746a", dry=True),
    ribbon([(11, 64, .10), (25, 62, .72), (40, 64, .90), (56, 62, .08)], .72, "man-playa", "#bcb9af", dry=True),
])


write("shade", [
    ribbon([(10, 31, .10), (22, 23, .72), (37, 21, .94), (52, 25, .72), (63, 32, .08)], 3.0, "shade-canopy"),
    ribbon([(14, 34, .10), (26, 31, .72), (39, 32, .90), (57, 35, .08)], 1.1, "shade-canopy-dry", "#77746a", dry=True),
    ribbon([(15, 33, .10), (15, 45, .72), (16, 58, .08)], 2.0, "shade-post-left"),
    ribbon([(59, 34, .10), (58, 46, .72), (58, 57, .08)], 1.25, "shade-post-right", "#77746a", dry=True),
    ribbon([(35, 28, .10), (35, 42, .72), (35, 56, .08)], 1.0, "shade-post-center", "#4a4943"),
    ribbon([(12, 59, .10), (27, 57, .72), (43, 59, .90), (61, 57, .08)], .72, "shade-ground", "#bcb9af", dry=True),
])


write("temple", [
    ribbon([(36, 8, .08), (32, 19, .72), (29, 31, .94), (24, 44, .82), (19, 58, .08)], 3.2, "temple-ascent-left", "#4a4943"),
    ribbon([(37, 9, .10), (42, 21, .72), (46, 34, .90), (51, 47, .72), (56, 59, .08)], 1.8, "temple-ascent-right", "#77746a", dry=True),
    ribbon([(28, 29, .10), (36, 27, .92), (45, 31, .08)], 2.0, "temple-tier-high"),
    ribbon([(24, 43, .10), (36, 40, .92), (50, 44, .08)], 2.3, "temple-tier-mid", "#4a4943"),
    ribbon([(18, 58, .10), (35, 55, .92), (57, 59, .08)], 2.7, "temple-tier-low", "#262522"),
    ribbon([(31, 18, .10), (36, 15, .72), (41, 19, .08)], .72, "temple-inner-light", "#bcb9af", dry=True),
    ribbon([(12, 64, .10), (27, 62, .72), (43, 64, .90), (61, 62, .08)], .65, "temple-playa", "#77746a", dry=True),
])


print("redrew all 4 BRC PUA glyphs as naturalist sumi-e playa studies")
