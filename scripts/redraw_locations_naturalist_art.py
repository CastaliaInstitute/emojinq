#!/usr/bin/env python3
"""Progressively redraw the 63 location PUA glyphs as sumi-e place studies.

This first authored plate covers landscapes and ecosystems.  Later plates in
this file add buildings, cultural-geographic places, and knowledge spaces.
"""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "locations"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522", *, dry=False) -> str:
    # The original place plate was technically present at 32px but read as
    # hairline notation.  Stronger pressure keeps roofs, roads, trunks, waves,
    # and architectural supports nameable without adding enclosed fill fields.
    width = max(width * 1.45, 1.2)
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


def mass(d: str, color="#4a4943") -> str:
    return (
        f'<path class="ink-wash" d="{d}" fill="{color}" '
        'data-ink-brush-pass="loaded-mass-v2"/>'
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="locations / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>locations / {name} — naturalist sumi-e place study</title>{''.join(marks)}</svg>
''')


write("burrow", [
    ribbon([(8, 47, .10), (20, 39, .72), (34, 38, .94), (48, 42, .72), (61, 50, .08)], 2.4, "burrow-bank"),
    mass("M 24 47 C 27 38 41 37 47 47 C 42 53 30 54 24 47 Z", "#262522"),
    ribbon([(29, 47, .10), (35, 43, .72), (43, 47, .08)], .72, "burrow-inner", "#77746a", dry=True),
    ribbon([(12, 55, .10), (26, 52, .72), (42, 55, .90), (59, 52, .08)], .75, "burrow-ground", "#bcb9af", dry=True),
    ribbon([(53, 43, .10), (57, 36, .72), (61, 32, .08)], .85, "burrow-grass", "#4a4943", dry=True),
])

write("canyon", [
    ribbon([(9, 12, .10), (14, 27, .72), (13, 43, .94), (20, 61, .08)], 3.6, "canyon-left", "#4a4943"),
    ribbon([(63, 10, .10), (55, 25, .72), (56, 42, .90), (48, 61, .08)], 2.3, "canyon-right", "#77746a", dry=True),
    ribbon([(20, 61, .10), (28, 53, .72), (35, 58, .92), (42, 50, .72), (49, 61, .08)], 1.5, "canyon-river"),
    ribbon([(17, 22, .10), (25, 20, .72), (32, 22, .08)], .72, "canyon-strata-left", "#bcb9af", dry=True),
    ribbon([(48, 29, .10), (55, 27, .72), (61, 29, .08)], .65, "canyon-strata-right", "#bcb9af", dry=True),
])

write("cave", [
    ribbon([(7, 59, .10), (10, 37, .68), (22, 20, .94), (38, 14, .86), (55, 23, .72), (65, 50, .08)], 3.2, "cave-arch"),
    mass("M 24 57 C 24 44 30 35 38 34 C 48 36 53 46 51 58 Z", "#4a4943"),
    ribbon([(30, 55, .10), (34, 44, .72), (39, 39, .08)], .85, "cave-inner-edge", "#77746a", dry=True),
    ribbon([(10, 62, .10), (26, 59, .72), (43, 62, .90), (61, 59, .08)], .72, "cave-ground", "#bcb9af", dry=True),
])

write("coast", [
    ribbon([(9, 13, .10), (14, 27, .72), (18, 41, .94), (28, 49, .08)], 3.6, "coast-cliff", "#4a4943"),
    ribbon([(27, 49, .10), (38, 46, .72), (49, 50, .90), (62, 46, .08)], 1.75, "coast-wave-a"),
    ribbon([(25, 57, .10), (38, 54, .72), (51, 58, .90), (64, 53, .08)], 1.0, "coast-wave-b", "#77746a", dry=True),
    ribbon([(14, 29, .10), (22, 26, .72), (30, 29, .08)], .72, "coast-cliff-strata", "#bcb9af", dry=True),
    dab(55, 18, 3.0, 3.0, "#77746a"),
])

write("delta", [
    ribbon([(36, 8, .10), (35, 21, .72), (36, 34, 1.0), (34, 46, .08)], 3.1, "delta-river", "#4a4943"),
    ribbon([(35, 41, .45), (25, 49, 1.0), (12, 59, .08)], 3.0, "delta-branch-left"),
    ribbon([(35, 42, .40), (46, 50, .92), (61, 58, .08)], 2.3, "delta-branch-right", "#4a4943"),
    ribbon([(34, 44, .40), (35, 54, .92), (31, 64, .08)], 1.65, "delta-branch-center", "#77746a", dry=True),
    ribbon([(7, 63, .10), (22, 60, .72), (39, 63, .90), (56, 60, .08)], .72, "delta-sea", "#bcb9af", dry=True),
])

write("den", [
    ribbon([(9, 52, .10), (18, 39, .72), (31, 32, .94), (46, 34, .82), (60, 47, .08)], 3.0, "den-rock"),
    mass("M 24 53 C 25 43 32 38 40 39 C 48 41 52 47 50 54 Z", "#262522"),
    ribbon([(28, 52, .10), (34, 45, .72), (41, 43, .08)], .72, "den-dry-mouth", "#77746a", dry=True),
    ribbon([(12, 59, .10), (27, 57, .72), (43, 59, .90), (59, 56, .08)], .72, "den-ground", "#bcb9af", dry=True),
    ribbon([(53, 41, .10), (58, 35, .72), (62, 33, .08)], .80, "den-scrub", "#4a4943", dry=True),
])

write("glacier", [
    ribbon([(10, 56, .10), (20, 40, .72), (31, 25, .94), (38, 11, .08)], 3.0, "glacier-left", "#4a4943"),
    ribbon([(38, 11, .10), (47, 28, .72), (57, 43, .90), (64, 56, .08)], 1.9, "glacier-right", "#77746a", dry=True),
    ribbon([(21, 40, .10), (31, 43, .72), (39, 35, .90), (49, 42, .08)], 1.2, "glacier-crevasse-a"),
    ribbon([(29, 52, .10), (37, 45, .72), (46, 52, .08)], .85, "glacier-crevasse-b", "#bcb9af", dry=True),
    ribbon([(8, 61, .10), (24, 59, .72), (41, 62, .90), (61, 59, .08)], .72, "glacier-ground", "#77746a", dry=True),
])

write("hive", [
    ribbon([(12, 16, .10), (25, 14, .72), (38, 17, .90), (52, 13, .08)], 2.1, "hive-branch"),
    ribbon([(36, 17, .10), (36, 25, .72), (35, 31, .08)], 1.4, "hive-stem"),
    mass("M 35 28 C 25 30 20 39 22 48 C 24 58 46 61 51 49 C 53 39 46 30 35 28 Z", "#77746a"),
    ribbon([(24, 39, .10), (36, 36, .72), (49, 39, .08)], 1.05, "hive-band-a", "#262522"),
    ribbon([(23, 47, .10), (36, 44, .72), (50, 47, .08)], 1.0, "hive-band-b", "#4a4943"),
    dab(37, 52, 3.8, 2.8, "#262522"),
])

write("jungle", [
    ribbon([(22, 62, .10), (23, 47, .72), (21, 31, .94), (24, 14, .08)], 3.0, "jungle-trunk-host", "#4a4943"),
    ribbon([(46, 62, .10), (43, 48, .72), (45, 33, .90), (42, 20, .08)], 1.75, "jungle-trunk-guest", "#77746a", dry=True),
    ribbon([(22, 25, .10), (13, 19, .72), (7, 14, .08)], 3.2, "jungle-leaf-left"),
    ribbon([(24, 31, .10), (33, 23, .72), (39, 17, .08)], 2.5, "jungle-leaf-mid", "#4a4943"),
    ribbon([(44, 30, .10), (53, 24, .72), (63, 22, .08)], 2.1, "jungle-leaf-right", "#77746a", dry=True),
    ribbon([(34, 10, .10), (37, 25, .72), (34, 41, .90), (38, 57, .08)], .80, "jungle-vine", "#bcb9af", dry=True),
])

write("lake", [
    ribbon([(11, 39, .10), (24, 34, .72), (39, 36, .94), (54, 33, .08)], 1.55, "lake-far-shore"),
    ribbon([(8, 48, .10), (21, 44, .72), (36, 47, .94), (51, 44, .72), (64, 48, .08)], 2.0, "lake-water-host", "#4a4943"),
    ribbon([(13, 56, .10), (27, 53, .72), (42, 56, .90), (59, 52, .08)], .80, "lake-water-dry", "#77746a", dry=True),
    ribbon([(18, 35, .10), (20, 27, .72), (19, 20, .08)], 1.1, "lake-reed-a"),
    ribbon([(23, 35, .10), (26, 29, .72), (29, 25, .08)], .72, "lake-reed-b", "#bcb9af", dry=True),
])

write("park", [
    ribbon([(25, 56, .10), (25, 43, .72), (27, 29, .94), (28, 15, .08)], 3.2, "park-tree-trunk", "#4a4943"),
    ribbon([(27, 27, .10), (18, 21, .72), (10, 22, .08)], 3.4, "park-crown-left"),
    ribbon([(28, 24, .10), (39, 17, .72), (51, 20, .08)], 2.7, "park-crown-right", "#77746a", dry=True),
    ribbon([(35, 45, .10), (46, 43, .72), (58, 45, .08)], 2.2, "park-bench-seat"),
    ribbon([(40, 46, .10), (39, 53, .72), (38, 58, .08)], 1.1, "park-bench-leg", "#4a4943"),
    ribbon([(55, 45, .10), (56, 52, .72), (57, 57, .08)], .80, "park-bench-leg-dry", "#77746a", dry=True),
    ribbon([(9, 62, .10), (25, 59, .72), (43, 62, .90), (62, 59, .08)], .72, "park-ground", "#bcb9af", dry=True),
])

write("pasture", [
    ribbon([(8, 45, .10), (23, 40, .72), (39, 43, .90), (56, 38, .08)], 1.6, "pasture-horizon"),
    ribbon([(15, 57, .10), (26, 52, .72), (39, 55, .90), (54, 50, .08)], 1.15, "pasture-field", "#77746a", dry=True),
    ribbon([(14, 35, .10), (14, 47, .72), (14, 59, .08)], 1.4, "pasture-fence-post-a"),
    ribbon([(46, 34, .10), (46, 45, .72), (46, 56, .08)], 1.0, "pasture-fence-post-b", "#4a4943"),
    ribbon([(12, 43, .10), (27, 41, .72), (46, 43, .08)], .90, "pasture-fence-rail", "#bcb9af", dry=True),
    ribbon([(22, 36, .10), (25, 28, .72), (28, 24, .08)], .80, "pasture-grass", "#4a4943", dry=True),
])

write("plateau", [
    ribbon([(8, 57, .10), (17, 45, .72), (23, 31, .94), (49, 30, .90), (56, 44, .72), (64, 57, .08)], 3.0, "plateau-host", "#4a4943"),
    ribbon([(23, 30, .10), (35, 28, .92), (49, 30, .08)], 1.2, "plateau-rim"),
    ribbon([(17, 46, .10), (28, 43, .72), (40, 45, .08)], .72, "plateau-strata-left", "#bcb9af", dry=True),
    ribbon([(42, 49, .10), (51, 47, .72), (58, 49, .08)], .65, "plateau-strata-right", "#77746a", dry=True),
    ribbon([(8, 62, .10), (25, 60, .72), (43, 62, .90), (62, 60, .08)], .72, "plateau-ground", "#77746a", dry=True),
])

write("reef", [
    ribbon([(36, 63, .10), (35, 50, .72), (31, 39, .94), (25, 30, .72), (23, 20, .08)], 2.5, "reef-coral-host"),
    ribbon([(35, 50, .10), (44, 42, .72), (49, 31, .90), (50, 21, .08)], 2.0, "reef-coral-right", "#4a4943"),
    ribbon([(31, 41, .10), (21, 42, .72), (13, 36, .08)], 1.5, "reef-coral-left", "#77746a", dry=True),
    ribbon([(44, 42, .10), (55, 42, .72), (63, 36, .08)], 1.2, "reef-branch-right", "#4a4943"),
    ribbon([(24, 31, .10), (17, 26, .72), (14, 19, .08)], 1.35, "reef-prong-left"),
    ribbon([(49, 31, .10), (57, 27, .72), (61, 20, .08)], 1.2, "reef-prong-right", "#4a4943"),
    ribbon([(13, 49, .10), (20, 45, .72), (27, 49, .90), (20, 53, .72), (13, 49, .08)], 1.3, "reef-fish"),
    dab(24, 48, 1.2, 1.2, "#262522"),
    ribbon([(9, 16, .10), (23, 13, .72), (39, 16, .90), (57, 12, .08)], .72, "reef-water-high", "#bcb9af", dry=True),
    ribbon([(8, 60, .10), (23, 58, .72), (40, 61, .90), (61, 58, .08)], .72, "reef-seabed", "#77746a", dry=True),
])

write("sand", [
    ribbon([(5, 51, .10), (17, 42, .72), (30, 45, .94), (42, 38, .72), (58, 43, .08)], 2.2, "sand-dune-host", "#4a4943"),
    ribbon([(12, 59, .10), (26, 54, .72), (40, 57, .90), (63, 50, .08)], 1.25, "sand-dune-guest", "#77746a", dry=True),
    ribbon([(19, 36, .10), (27, 32, .72), (36, 34, .08)], .72, "sand-ripple-a", "#bcb9af", dry=True),
    ribbon([(41, 48, .10), (50, 46, .72), (58, 48, .08)], .65, "sand-ripple-b", "#bcb9af", dry=True),
    dab(55, 18, 3.0, 3.0, "#77746a"),
])

write("savanna", [
    ribbon([(35, 58, .10), (35, 45, .72), (37, 31, .94), (38, 18, .08)], 3.0, "savanna-trunk", "#4a4943"),
    ribbon([(37, 24, .10), (26, 20, .72), (14, 22, .08)], 3.5, "savanna-crown-left"),
    ribbon([(38, 22, .10), (49, 18, .72), (61, 21, .08)], 2.5, "savanna-crown-right", "#77746a", dry=True),
    ribbon([(8, 59, .10), (23, 56, .72), (40, 59, .90), (62, 55, .08)], .80, "savanna-horizon", "#bcb9af", dry=True),
    ribbon([(16, 55, .10), (18, 48, .72), (20, 44, .08)], .72, "savanna-grass-a", "#4a4943", dry=True),
    ribbon([(54, 54, .10), (57, 48, .72), (61, 46, .08)], .65, "savanna-grass-b", "#77746a", dry=True),
])

write("shell", [
    ribbon([(15, 47, .10), (15, 34, .72), (23, 23, .94), (36, 18, .86), (49, 23, .72), (57, 34, .94), (55, 47, .72), (45, 55, .94), (31, 55, .72), (20, 49, .08)], 2.6, "shell-contour"),
    ribbon([(44, 43, .10), (42, 33, .72), (34, 29, .94), (27, 33, .82), (28, 41, .90), (35, 44, .72), (39, 39, .90), (37, 35, .08)], 1.5, "shell-spiral", "#4a4943"),
    ribbon([(20, 49, .10), (33, 52, .72), (47, 49, .08)], .72, "shell-lip", "#77746a", dry=True),
    ribbon([(24, 25, .10), (29, 31, .72), (31, 38, .08)], .65, "shell-rib", "#bcb9af", dry=True),
])

write("spring", [
    ribbon([(11, 48, .10), (23, 43, .72), (34, 45, .94), (46, 41, .08)], 2.5, "spring-rock", "#4a4943"),
    ribbon([(34, 45, .10), (39, 50, .72), (48, 52, .90), (59, 49, .08)], 1.8, "spring-water-host"),
    ribbon([(31, 52, .10), (41, 56, .72), (53, 55, .08)], .80, "spring-water-dry", "#77746a", dry=True),
    ribbon([(20, 42, .10), (20, 32, .72), (22, 24, .08)], 1.1, "spring-stem"),
    ribbon([(21, 32, .10), (14, 28, .72), (9, 29, .08)], 1.7, "spring-leaf", "#77746a", dry=True),
    ribbon([(9, 61, .10), (24, 59, .72), (41, 62, .90), (60, 59, .08)], .72, "spring-ground", "#bcb9af", dry=True),
])

write("tide", [
    ribbon([(8, 39, .10), (21, 34, .72), (35, 37, .94), (49, 32, .72), (62, 36, .08)], 2.2, "tide-high"),
    ribbon([(7, 49, .10), (21, 44, .72), (36, 48, .94), (51, 43, .72), (64, 47, .08)], 1.65, "tide-mid", "#4a4943"),
    ribbon([(12, 58, .10), (27, 54, .72), (43, 58, .90), (60, 53, .08)], .85, "tide-low", "#77746a", dry=True),
    dab(52, 16, 3.0, 3.0, "#77746a"),
    ribbon([(53, 13, .10), (57, 16, .72), (53, 19, .08)], .65, "tide-moon-lift", "#bcb9af", dry=True),
])

write("tundra", [
    ribbon([(7, 43, .10), (22, 39, .72), (38, 42, .90), (57, 37, .08)], 1.8, "tundra-horizon", "#4a4943"),
    ribbon([(9, 53, .10), (24, 49, .72), (40, 53, .90), (62, 47, .08)], 1.1, "tundra-snow", "#77746a", dry=True),
    ribbon([(18, 47, .10), (20, 39, .72), (24, 35, .08)], .85, "tundra-shrub-a", "#4a4943", dry=True),
    ribbon([(44, 48, .10), (47, 41, .72), (52, 38, .08)], .72, "tundra-shrub-b", "#77746a", dry=True),
    ribbon([(12, 61, .10), (28, 59, .72), (45, 62, .90), (62, 59, .08)], .65, "tundra-ground", "#bcb9af", dry=True),
])

write("valley", [
    ribbon([(5, 19, .10), (13, 31, .72), (20, 45, .94), (31, 57, .08)], 3.0, "valley-left", "#4a4943"),
    ribbon([(67, 16, .10), (58, 29, .72), (51, 43, .90), (40, 57, .08)], 2.0, "valley-right", "#77746a", dry=True),
    ribbon([(31, 57, .10), (35, 49, .72), (39, 56, .90), (43, 62, .08)], 1.35, "valley-river"),
    ribbon([(13, 33, .10), (22, 31, .72), (30, 34, .08)], .72, "valley-slope-left", "#bcb9af", dry=True),
    ribbon([(44, 39, .10), (53, 36, .72), (61, 38, .08)], .65, "valley-slope-right", "#bcb9af", dry=True),
])

write("wave", [
    ribbon([(8, 48, .10), (19, 38, .72), (30, 32, .94), (42, 34, .86), (52, 28, .94), (59, 18, .72), (63, 29, .90), (56, 41, .72), (44, 48, .94), (28, 51, .72), (14, 48, .08)], 3.1, "wave-host"),
    ribbon([(43, 34, .10), (51, 36, .72), (57, 42, .08)], 1.0, "wave-curl-dry", "#77746a", dry=True),
    ribbon([(14, 58, .10), (28, 55, .72), (43, 58, .90), (60, 54, .08)], .80, "wave-trough", "#bcb9af", dry=True),
    ribbon([(56, 18, .10), (61, 14, .72), (66, 15, .08)], .72, "wave-foam", "#77746a", dry=True),
])


# ---------------------------------------------------------------------------
# Buildings and infrastructure: architecture is stated by load-bearing marks
# plus one activity cue, never by swapping labels on a generic house outline.

write("academy", [
    ribbon([(12, 32, .10), (24, 23, .72), (36, 16, .94), (49, 24, .72), (60, 32, .08)], 2.5, "academy-pediment"),
    ribbon([(15, 34, .10), (36, 32, .92), (58, 34, .08)], 2.0, "academy-entablature", "#4a4943"),
    ribbon([(20, 35, .10), (20, 47, .72), (20, 58, .08)], 1.6, "academy-column-a"),
    ribbon([(34, 34, .10), (34, 46, .72), (34, 58, .08)], 1.25, "academy-column-b", "#77746a", dry=True),
    ribbon([(49, 35, .10), (49, 47, .72), (49, 58, .08)], 1.5, "academy-column-c"),
    ribbon([(14, 59, .10), (35, 57, .92), (58, 59, .08)], 2.1, "academy-base"),
    ribbon([(29, 24, .10), (36, 22, .72), (43, 24, .08)], .72, "academy-book", "#bcb9af", dry=True),
])

write("archive", [
    ribbon([(14, 58, .10), (14, 38, .68), (22, 22, .94), (36, 16, .86), (50, 22, .72), (58, 39, .08)], 2.7, "archive-arch"),
    ribbon([(18, 37, .10), (35, 35, .92), (54, 37, .08)], 2.0, "archive-shelf-top", "#4a4943"),
    ribbon([(18, 48, .10), (35, 46, .92), (54, 48, .08)], 1.35, "archive-shelf-mid"),
    ribbon([(21, 37, .10), (21, 48, .72), (21, 58, .08)], 1.0, "archive-stack-a", "#77746a", dry=True),
    ribbon([(32, 37, .10), (32, 48, .72), (32, 58, .08)], .85, "archive-stack-b", "#bcb9af", dry=True),
    ribbon([(45, 37, .10), (45, 48, .72), (45, 58, .08)], 1.1, "archive-stack-c", "#4a4943"),
    ribbon([(13, 59, .10), (34, 57, .92), (59, 59, .08)], 1.8, "archive-base"),
])

write("bakery", [
    ribbon([(12, 33, .10), (23, 27, .72), (36, 28, .94), (49, 26, .72), (60, 32, .08)], 2.6, "bakery-awning"),
    ribbon([(14, 34, .10), (15, 46, .72), (15, 58, .08)], 1.6, "bakery-left"),
    ribbon([(58, 34, .10), (57, 46, .72), (58, 57, .08)], 1.1, "bakery-right", "#77746a", dry=True),
    ribbon([(22, 47, .10), (30, 42, .72), (40, 43, .94), (49, 48, .08)], 3.7, "bakery-loaf", "#4a4943"),
    ribbon([(28, 43, .10), (32, 39, .72), (35, 36, .08)], .72, "bakery-score-a", "#bcb9af", dry=True),
    ribbon([(39, 43, .10), (42, 39, .72), (44, 37, .08)], .65, "bakery-score-b", "#77746a", dry=True),
    ribbon([(28, 27, .10), (27, 21, .72), (30, 17, .08)], .85, "bakery-steam", "#77746a", dry=True),
    ribbon([(13, 59, .10), (34, 57, .92), (59, 59, .08)], 1.5, "bakery-base"),
])

write("barn", [
    ribbon([(10, 33, .10), (22, 24, .72), (35, 15, .94), (49, 24, .72), (62, 34, .08)], 3.0, "barn-roof"),
    ribbon([(13, 35, .10), (14, 47, .72), (14, 60, .08)], 1.8, "barn-wall-left"),
    ribbon([(59, 35, .10), (58, 47, .72), (59, 59, .08)], 1.3, "barn-wall-right", "#77746a", dry=True),
    ribbon([(25, 59, .10), (25, 47, .72), (36, 40, .94), (47, 47, .72), (47, 59, .08)], 2.0, "barn-door"),
    ribbon([(27, 46, .10), (35, 52, .72), (45, 58, .08)], .85, "barn-door-cross-a", "#77746a", dry=True),
    ribbon([(45, 46, .10), (36, 52, .72), (27, 58, .08)], .85, "barn-door-cross-b", "#bcb9af", dry=True),
    ribbon([(11, 61, .10), (34, 59, .92), (61, 61, .08)], 1.65, "barn-ground"),
])

write("bench", [
    ribbon([(12, 38, .10), (25, 35, .72), (40, 37, .94), (59, 35, .08)], 3.2, "bench-seat", "#4a4943"),
    ribbon([(15, 23, .10), (28, 21, .72), (43, 23, .90), (56, 21, .08)], 2.15, "bench-back"),
    ribbon([(15, 30, .10), (28, 28, .72), (43, 30, .90), (56, 28, .08)], 1.65, "bench-back-lower", "#4a4943"),
    ribbon([(17, 22, .10), (18, 32, .72), (18, 43, .08)], 1.2, "bench-back-post-a", "#4a4943"),
    ribbon([(53, 21, .10), (53, 32, .72), (52, 43, .08)], 1.1, "bench-back-post-b", "#77746a"),
    ribbon([(18, 41, .10), (19, 50, .72), (17, 58, .08)], 1.55, "bench-leg-a"),
    ribbon([(53, 40, .10), (51, 49, .72), (52, 57, .08)], 1.1, "bench-leg-b", "#77746a", dry=True),
    ribbon([(10, 61, .10), (26, 59, .72), (44, 61, .90), (62, 58, .08)], .65, "bench-ground", "#bcb9af", dry=True),
])

write("cafe", [
    ribbon([(10, 31, .10), (22, 27, .72), (36, 29, .94), (51, 26, .72), (62, 31, .08)], 2.5, "cafe-awning"),
    ribbon([(14, 32, .10), (15, 45, .72), (15, 59, .08)], 1.45, "cafe-post-left"),
    ribbon([(58, 32, .10), (57, 45, .72), (58, 57, .08)], 1.0, "cafe-post-right", "#77746a", dry=True),
    ribbon([(23, 45, .10), (29, 49, .72), (37, 48, .94), (42, 43, .72), (41, 37, .08)], 2.0, "cafe-cup"),
    ribbon([(42, 40, .10), (49, 38, .72), (51, 42, .90), (46, 45, .08)], 1.0, "cafe-handle", "#77746a", dry=True),
    ribbon([(24, 54, .10), (36, 52, .92), (49, 54, .08)], 1.45, "cafe-saucer"),
    ribbon([(30, 36, .10), (29, 30, .72), (32, 26, .08)], .72, "cafe-steam", "#bcb9af", dry=True),
])

write("ceiling", [
    ribbon([(8, 14, .10), (23, 12, .72), (39, 14, .94), (63, 12, .08)], 3.2, "ceiling-beam", "#4a4943"),
    ribbon([(36, 14, .10), (36, 24, .72), (35, 32, .08)], 1.35, "ceiling-cord"),
    ribbon([(27, 35, .10), (35, 31, .92), (44, 35, .08)], 2.2, "ceiling-lamp"),
    ribbon([(28, 39, .10), (23, 48, .72), (19, 57, .08)], .95, "ceiling-light-left", "#77746a", dry=True),
    ribbon([(42, 39, .10), (47, 48, .72), (51, 56, .08)], .72, "ceiling-light-right", "#bcb9af", dry=True),
    ribbon([(13, 61, .10), (29, 58, .72), (46, 61, .90), (60, 58, .08)], .65, "ceiling-floor", "#77746a", dry=True),
])

write("crossing", [
    ribbon([(8, 43, .10), (21, 35, .72), (36, 36, .94), (51, 32, .72), (64, 39, .08)], 3.0, "crossing-bridge"),
    ribbon([(12, 46, .10), (12, 53, .72), (11, 60, .08)], 1.35, "crossing-pier-left"),
    ribbon([(57, 42, .10), (58, 50, .72), (57, 57, .08)], 1.0, "crossing-pier-right", "#77746a", dry=True),
    ribbon([(17, 31, .10), (36, 29, .92), (57, 28, .08)], 1.0, "crossing-rail", "#4a4943"),
    ribbon([(8, 53, .10), (22, 49, .72), (36, 53, .90), (51, 48, .72), (65, 51, .08)], 1.25, "crossing-water-a", "#77746a", dry=True),
    ribbon([(12, 62, .10), (26, 58, .72), (41, 62, .90), (59, 57, .08)], .65, "crossing-water-b", "#bcb9af", dry=True),
])

write("dock", [
    ribbon([(9, 44, .10), (22, 40, .72), (38, 42, .94), (59, 38, .08)], 3.4, "dock-deck", "#4a4943"),
    ribbon([(15, 42, .10), (14, 51, .72), (13, 60, .08)], 1.65, "dock-post-a"),
    ribbon([(36, 41, .10), (35, 50, .72), (34, 59, .08)], 1.2, "dock-post-b", "#77746a", dry=True),
    ribbon([(56, 39, .10), (55, 48, .72), (54, 57, .08)], .95, "dock-post-c", "#4a4943"),
    ribbon([(8, 53, .10), (23, 49, .72), (39, 53, .90), (61, 48, .08)], 1.15, "dock-water-a", "#77746a", dry=True),
    ribbon([(12, 62, .10), (28, 58, .72), (44, 62, .90), (62, 57, .08)], .65, "dock-water-b", "#bcb9af", dry=True),
])

write("forum", [
    ribbon([(9, 43, .10), (19, 31, .72), (34, 26, .94), (50, 31, .72), (61, 43, .08)], 2.7, "forum-outer"),
    ribbon([(15, 45, .10), (25, 37, .72), (36, 34, .94), (49, 39, .72), (57, 46, .08)], 1.55, "forum-inner", "#77746a", dry=True),
    ribbon([(19, 53, .10), (31, 48, .72), (43, 50, .90), (54, 55, .08)], 1.4, "forum-seats", "#4a4943"),
    ribbon([(35, 34, .10), (35, 43, .72), (35, 51, .08)], 1.1, "forum-speaker"),
    dab(35, 31, 2.1, 2.1, "#262522"),
    ribbon([(10, 60, .10), (26, 58, .72), (43, 61, .90), (60, 58, .08)], .65, "forum-ground", "#bcb9af", dry=True),
])

write("laboratory", [
    ribbon([(10, 57, .10), (26, 55, .72), (43, 58, .90), (62, 55, .08)], 2.2, "laboratory-bench", "#4a4943"),
    ribbon([(27, 16, .10), (28, 27, .72), (24, 39, .94), (19, 49, .72), (26, 54, .90), (38, 52, .08)], 2.0, "laboratory-flask-left"),
    ribbon([(35, 18, .10), (35, 30, .72), (39, 42, .94), (46, 52, .08)], 1.35, "laboratory-flask-right", "#77746a", dry=True),
    ribbon([(22, 42, .10), (31, 39, .72), (42, 44, .08)], 1.6, "laboratory-liquid", "#4a4943"),
    dab(28, 47, 2.2, 2.2, "#262522"),
    dab(36, 48, 1.5, 1.5, "#77746a"),
    ribbon([(47, 50, .10), (49, 37, .72), (55, 29, .08)], 1.7, "laboratory-microscope-arm"),
    ribbon([(54, 29, .10), (60, 27, .72), (63, 30, .08)], 1.0, "laboratory-microscope-eye", "#77746a", dry=True),
    ribbon([(45, 53, .10), (55, 51, .72), (63, 53, .08)], .72, "laboratory-microscope-foot", "#bcb9af", dry=True),
])

write("library", [
    ribbon([(10, 32, .10), (23, 24, .72), (36, 17, .94), (50, 24, .72), (61, 32, .08)], 2.5, "library-roof"),
    ribbon([(14, 34, .10), (35, 32, .92), (58, 34, .08)], 1.8, "library-entablature"),
    ribbon([(19, 35, .10), (19, 47, .72), (19, 58, .08)], 1.45, "library-column-a"),
    ribbon([(51, 35, .10), (51, 47, .72), (51, 58, .08)], 1.0, "library-column-b", "#77746a", dry=True),
    ribbon([(27, 43, .10), (35, 40, .72), (44, 43, .08)], 2.0, "library-book-top", "#4a4943"),
    ribbon([(27, 43, .10), (28, 52, .72), (35, 55, .08)], 1.0, "library-book-left", "#77746a", dry=True),
    ribbon([(44, 43, .10), (43, 52, .72), (35, 55, .08)], 1.3, "library-book-right"),
    ribbon([(12, 59, .10), (34, 57, .92), (60, 59, .08)], 1.65, "library-base"),
])

write("market", [
    ribbon([(8, 31, .10), (20, 26, .72), (35, 29, .94), (51, 25, .72), (64, 30, .08)], 2.7, "market-awning"),
    ribbon([(12, 32, .10), (13, 45, .72), (13, 59, .08)], 1.5, "market-post-a"),
    ribbon([(59, 31, .10), (58, 45, .72), (59, 57, .08)], 1.0, "market-post-b", "#77746a", dry=True),
    ribbon([(17, 48, .10), (25, 43, .72), (34, 48, .08)], 3.3, "market-basket-a", "#4a4943"),
    ribbon([(38, 49, .10), (47, 43, .72), (56, 49, .08)], 2.6, "market-basket-b", "#77746a", dry=True),
    dab(25, 41, 1.8, 1.6, "#262522"),
    dab(45, 41, 1.6, 1.4, "#4a4943"),
    ribbon([(10, 60, .10), (27, 58, .72), (44, 61, .90), (62, 58, .08)], .65, "market-ground", "#bcb9af", dry=True),
])

write("museum", [
    ribbon([(9, 31, .10), (22, 23, .72), (36, 16, .94), (50, 24, .72), (62, 31, .08)], 2.6, "museum-pediment"),
    ribbon([(13, 33, .10), (35, 31, .92), (59, 33, .08)], 1.8, "museum-entablature"),
    ribbon([(18, 35, .10), (18, 47, .72), (18, 58, .08)], 1.4, "museum-column-a"),
    ribbon([(53, 34, .10), (53, 47, .72), (53, 58, .08)], 1.0, "museum-column-b", "#77746a", dry=True),
    ribbon([(31, 39, .10), (29, 46, .72), (32, 54, .08)], 2.0, "museum-vase-left", "#4a4943"),
    ribbon([(40, 39, .10), (42, 46, .72), (39, 54, .08)], 1.4, "museum-vase-right", "#77746a", dry=True),
    ribbon([(30, 39, .10), (35, 37, .72), (41, 39, .08)], 1.15, "museum-vase-rim"),
    ribbon([(12, 59, .10), (35, 57, .92), (60, 59, .08)], 1.65, "museum-base"),
])

write("post", [
    ribbon([(14, 22, .10), (28, 19, .72), (43, 22, .94), (58, 19, .08)], 3.0, "post-board-top", "#4a4943"),
    ribbon([(15, 22, .10), (15, 31, .72), (16, 40, .08)], 1.5, "post-board-left"),
    ribbon([(57, 21, .10), (56, 30, .72), (56, 39, .08)], 1.0, "post-board-right", "#77746a", dry=True),
    ribbon([(16, 40, .10), (35, 38, .92), (56, 40, .08)], 1.8, "post-board-base"),
    ribbon([(35, 40, .10), (35, 50, .72), (34, 61, .08)], 2.2, "post-stem"),
    ribbon([(25, 29, .10), (34, 27, .72), (47, 29, .08)], .72, "post-writing-a", "#bcb9af", dry=True),
    ribbon([(29, 34, .10), (36, 32, .72), (45, 34, .08)], .65, "post-writing-b", "#77746a", dry=True),
    ribbon([(26, 62, .10), (34, 59, .72), (44, 62, .08)], 1.0, "post-foot", "#4a4943", dry=True),
])

write("sidewalk", [
    ribbon([(14, 63, .10), (22, 49, .72), (31, 35, .94), (38, 20, .08)], 2.8, "sidewalk-edge-left", "#4a4943"),
    ribbon([(58, 62, .10), (51, 49, .72), (45, 35, .90), (40, 21, .08)], 1.7, "sidewalk-edge-right", "#77746a", dry=True),
    ribbon([(19, 54, .10), (35, 52, .72), (53, 54, .08)], .85, "sidewalk-joint-low", "#bcb9af", dry=True),
    ribbon([(25, 43, .10), (36, 41, .72), (48, 43, .08)], .72, "sidewalk-joint-mid", "#77746a", dry=True),
    ribbon([(31, 32, .10), (37, 31, .72), (44, 32, .08)], .65, "sidewalk-joint-high", "#bcb9af", dry=True),
    ribbon([(11, 59, .10), (8, 52, .72), (7, 47, .08)], .72, "sidewalk-grass", "#4a4943", dry=True),
])

write("sign", [
    ribbon([(35, 61, .10), (35, 48, .72), (36, 34, .94), (35, 18, .08)], 2.4, "sign-post"),
    ribbon([(34, 22, .10), (24, 18, .72), (13, 21, .08)], 3.0, "sign-left-board", "#4a4943"),
    ribbon([(37, 31, .10), (48, 27, .72), (61, 30, .08)], 2.4, "sign-right-board", "#77746a", dry=True),
    ribbon([(15, 21, .10), (20, 17, .72), (24, 18, .08)], .72, "sign-left-tip", "#bcb9af", dry=True),
    ribbon([(58, 30, .10), (62, 26, .72), (65, 28, .08)], .65, "sign-right-tip", "#77746a", dry=True),
    ribbon([(25, 62, .10), (35, 59, .72), (46, 62, .08)], 1.0, "sign-ground", "#bcb9af", dry=True),
])

write("silo", [
    ribbon([(23, 25, .10), (27, 17, .72), (36, 12, .94), (45, 18, .72), (49, 26, .08)], 2.4, "silo-roof"),
    ribbon([(23, 27, .10), (22, 42, .72), (23, 58, .08)], 2.0, "silo-left"),
    ribbon([(49, 27, .10), (50, 42, .72), (49, 57, .08)], 1.35, "silo-right", "#77746a", dry=True),
    ribbon([(23, 35, .10), (36, 33, .92), (49, 35, .08)], 1.0, "silo-band-a", "#4a4943"),
    ribbon([(23, 46, .10), (36, 44, .92), (49, 46, .08)], .75, "silo-band-b", "#bcb9af", dry=True),
    ribbon([(22, 58, .10), (35, 56, .92), (50, 58, .08)], 1.7, "silo-base"),
    ribbon([(16, 61, .10), (31, 59, .72), (47, 62, .90), (58, 59, .08)], .65, "silo-ground", "#77746a", dry=True),
])

write("store", [
    ribbon([(10, 31, .10), (22, 26, .72), (36, 29, .94), (51, 25, .72), (63, 30, .08)], 2.8, "store-awning"),
    ribbon([(13, 33, .10), (14, 46, .72), (14, 59, .08)], 1.6, "store-left"),
    ribbon([(59, 32, .10), (58, 46, .72), (59, 58, .08)], 1.0, "store-right", "#77746a", dry=True),
    ribbon([(23, 38, .10), (23, 48, .72), (23, 58, .08)], 1.4, "store-door-left"),
    ribbon([(38, 39, .10), (48, 37, .72), (55, 40, .08)], 1.4, "store-window-top", "#4a4943"),
    ribbon([(39, 51, .10), (47, 48, .72), (55, 50, .08)], .85, "store-window-bottom", "#77746a", dry=True),
    dab(28, 47, 1.3, 1.2, "#262522"),
    ribbon([(11, 60, .10), (34, 58, .92), (61, 60, .08)], 1.6, "store-base"),
])

write("street", [
    ribbon([(10, 64, .10), (20, 51, .72), (29, 38, .94), (35, 23, .08)], 3.0, "street-edge-left", "#4a4943"),
    ribbon([(62, 63, .10), (53, 50, .72), (44, 38, .90), (37, 23, .08)], 1.8, "street-edge-right", "#77746a", dry=True),
    ribbon([(36, 25, .10), (36, 35, .72), (36, 46, .08)], .85, "street-center-high", "#bcb9af", dry=True),
    ribbon([(36, 53, .10), (36, 59, .72), (36, 64, .08)], 1.1, "street-center-low", "#4a4943"),
    ribbon([(13, 37, .10), (12, 28, .72), (15, 20, .08)], 1.2, "street-lamp-post"),
    ribbon([(15, 20, .10), (20, 17, .72), (24, 19, .08)], .90, "street-lamp-arm", "#77746a", dry=True),
    dab(24, 20, 1.8, 1.6, "#262522"),
])

write("theater", [
    ribbon([(10, 59, .10), (11, 43, .72), (12, 27, .08)], 2.2, "theater-left"),
    ribbon([(61, 59, .10), (60, 43, .72), (60, 27, .08)], 1.4, "theater-right", "#77746a", dry=True),
    ribbon([(10, 28, .10), (23, 20, .72), (36, 17, .94), (50, 21, .72), (62, 28, .08)], 2.7, "theater-proscenium"),
    ribbon([(17, 30, .10), (24, 39, .72), (29, 52, .08)], 3.0, "theater-curtain-left", "#4a4943"),
    ribbon([(55, 30, .10), (48, 39, .72), (43, 52, .08)], 2.1, "theater-curtain-right", "#77746a", dry=True),
    ribbon([(29, 52, .10), (36, 49, .72), (43, 52, .08)], 1.0, "theater-stage", "#262522"),
    ribbon([(11, 60, .10), (35, 58, .92), (61, 60, .08)], 1.65, "theater-base"),
    ribbon([(30, 30, .10), (36, 27, .72), (43, 30, .08)], .72, "theater-light", "#bcb9af", dry=True),
])

write("tower", [
    ribbon([(27, 58, .10), (29, 45, .72), (31, 31, .94), (34, 17, .08)], 3.0, "tower-left", "#4a4943"),
    ribbon([(45, 58, .10), (43, 45, .72), (41, 31, .90), (38, 17, .08)], 1.8, "tower-right", "#77746a", dry=True),
    ribbon([(32, 17, .10), (36, 11, .72), (40, 17, .08)], 2.0, "tower-cap"),
    ribbon([(30, 33, .10), (36, 31, .92), (42, 33, .08)], 1.0, "tower-band-a", "#4a4943"),
    ribbon([(28, 46, .10), (36, 44, .92), (44, 46, .08)], .80, "tower-band-b", "#bcb9af", dry=True),
    ribbon([(25, 59, .10), (36, 57, .92), (47, 59, .08)], 1.8, "tower-base"),
    ribbon([(36, 10, .10), (36, 5, .72), (36, 2, .08)], .72, "tower-beacon", "#77746a", dry=True),
])

write("workshop", [
    ribbon([(10, 33, .10), (23, 25, .72), (36, 19, .94), (50, 25, .72), (62, 33, .08)], 2.6, "workshop-roof"),
    ribbon([(13, 35, .10), (14, 47, .72), (14, 59, .08)], 1.5, "workshop-left"),
    ribbon([(59, 34, .10), (58, 47, .72), (59, 58, .08)], 1.0, "workshop-right", "#77746a", dry=True),
    ribbon([(19, 49, .10), (34, 46, .72), (51, 49, .08)], 2.4, "workshop-bench", "#4a4943"),
    ribbon([(35, 44, .10), (42, 35, .72), (50, 29, .08)], 1.8, "workshop-hammer-handle"),
    ribbon([(47, 28, .10), (54, 30, .72), (58, 34, .08)], 2.2, "workshop-hammer-head", "#262522"),
    ribbon([(23, 47, .10), (23, 55, .72), (22, 61, .08)], .90, "workshop-bench-leg", "#77746a", dry=True),
    ribbon([(11, 60, .10), (34, 58, .92), (61, 60, .08)], 1.5, "workshop-base", "#bcb9af", dry=True),
])


# ---------------------------------------------------------------------------
# Cultural-geographic studies use characteristic built or landscape forms as
# compact place cues.  They are not flags, borders, or claims of completeness.

write("china", [
    ribbon([(7, 56, .10), (18, 45, .72), (29, 38, .94), (42, 41, .72), (59, 31, .08)], 2.5, "china-mountain-wall", "#4a4943"),
    ribbon([(18, 45, .10), (18, 39, .72), (21, 35, .08)], 1.2, "china-watchtower-a"),
    ribbon([(42, 41, .10), (43, 34, .72), (47, 31, .08)], 1.0, "china-watchtower-b", "#77746a", dry=True),
    ribbon([(14, 25, .10), (25, 20, .72), (37, 22, .94), (50, 18, .08)], 1.8, "china-roof"),
    ribbon([(20, 29, .10), (35, 26, .72), (52, 28, .08)], .75, "china-roof-dry", "#bcb9af", dry=True),
    ribbon([(9, 62, .10), (26, 59, .72), (44, 62, .90), (62, 58, .08)], .65, "china-ground", "#77746a", dry=True),
])

write("egypt", [
    ribbon([(14, 57, .10), (26, 37, .72), (38, 16, .08)], 3.0, "egypt-pyramid-left", "#4a4943"),
    ribbon([(38, 16, .10), (49, 37, .72), (60, 57, .08)], 1.8, "egypt-pyramid-right", "#77746a", dry=True),
    ribbon([(15, 57, .10), (36, 54, .92), (61, 57, .08)], 1.8, "egypt-pyramid-base"),
    ribbon([(27, 39, .10), (36, 36, .72), (45, 39, .08)], .72, "egypt-course", "#bcb9af", dry=True),
    ribbon([(8, 64, .10), (23, 61, .72), (39, 64, .90), (58, 60, .08)], .72, "egypt-nile", "#77746a", dry=True),
    dab(58, 15, 3.0, 3.0, "#4a4943"),
])

write("europe", [
    ribbon([(29, 10, .10), (22, 17, .72), (24, 27, .94), (16, 34, .72), (22, 43, .90), (31, 45, .72), (34, 56, .90), (42, 61, .08)], 2.7, "europe-west-south", "#4a4943"),
    ribbon([(29, 10, .10), (39, 14, .72), (47, 22, .90), (57, 25, .72), (51, 35, .90), (55, 44, .72), (46, 51, .08)], 1.8, "europe-north-east", "#77746a", dry=True),
    ribbon([(24, 28, .10), (34, 31, .72), (47, 27, .08)], 1.1, "europe-center"),
    ribbon([(38, 45, .10), (43, 53, .72), (47, 60, .08)], .85, "europe-peninsula", "#4a4943"),
    ribbon([(12, 56, .10), (23, 53, .72), (32, 56, .08)], .65, "europe-island-water", "#bcb9af", dry=True),
])

write("greece", [
    ribbon([(10, 31, .10), (22, 23, .72), (35, 17, .94), (49, 24, .72), (61, 31, .08)], 2.5, "greece-pediment"),
    ribbon([(14, 33, .10), (35, 31, .92), (58, 33, .08)], 1.7, "greece-entablature"),
    ribbon([(19, 35, .10), (19, 45, .72), (18, 54, .08)], 1.35, "greece-column-a"),
    ribbon([(35, 34, .10), (35, 44, .72), (35, 54, .08)], 1.0, "greece-column-b", "#77746a", dry=True),
    ribbon([(52, 35, .10), (52, 45, .72), (52, 54, .08)], 1.25, "greece-column-c"),
    ribbon([(11, 59, .10), (25, 56, .72), (40, 59, .90), (61, 55, .08)], .80, "greece-sea", "#77746a", dry=True),
    ribbon([(13, 64, .10), (28, 61, .72), (44, 64, .90), (60, 60, .08)], .65, "greece-sea-dry", "#bcb9af", dry=True),
])

write("inca", [
    ribbon([(8, 59, .10), (17, 47, .72), (25, 36, .94), (34, 22, .72), (43, 36, .90), (54, 45, .72), (63, 57, .08)], 2.8, "inca-mountain", "#4a4943"),
    ribbon([(13, 52, .10), (26, 49, .72), (39, 52, .08)], 1.4, "inca-terrace-low"),
    ribbon([(21, 42, .10), (31, 39, .72), (44, 42, .08)], 1.1, "inca-terrace-mid", "#77746a", dry=True),
    ribbon([(29, 32, .10), (36, 29, .72), (43, 32, .08)], .85, "inca-terrace-high", "#bcb9af", dry=True),
    ribbon([(11, 63, .10), (26, 60, .72), (43, 63, .90), (61, 59, .08)], .65, "inca-ground", "#77746a", dry=True),
])

write("india", [
    ribbon([(13, 58, .10), (13, 43, .72), (15, 31, .08)], 1.8, "india-left"),
    ribbon([(58, 58, .10), (58, 43, .72), (56, 31, .08)], 1.2, "india-right", "#77746a", dry=True),
    ribbon([(15, 32, .10), (24, 27, .72), (35, 29, .94), (47, 26, .72), (57, 32, .08)], 2.5, "india-roof-line"),
    ribbon([(28, 29, .10), (29, 21, .72), (35, 15, .94), (42, 22, .72), (43, 29, .08)], 2.0, "india-dome"),
    ribbon([(34, 15, .10), (35, 10, .72), (36, 7, .08)], .85, "india-finial"),
    ribbon([(28, 58, .10), (28, 46, .72), (35, 39, .94), (43, 47, .72), (43, 58, .08)], 1.35, "india-arch", "#4a4943"),
    ribbon([(10, 60, .10), (35, 57, .92), (62, 60, .08)], 1.7, "india-base"),
    ribbon([(18, 39, .10), (23, 37, .72), (28, 39, .08)], .65, "india-screen", "#bcb9af", dry=True),
])

write("japan", [
    ribbon([(14, 27, .10), (27, 22, .72), (41, 24, .94), (57, 20, .08)], 3.0, "japan-torii-top"),
    ribbon([(20, 34, .10), (35, 31, .92), (52, 33, .08)], 1.8, "japan-torii-cross"),
    ribbon([(24, 33, .10), (23, 46, .72), (22, 59, .08)], 1.7, "japan-post-left"),
    ribbon([(49, 32, .10), (49, 45, .72), (50, 58, .08)], 1.15, "japan-post-right", "#77746a", dry=True),
    ribbon([(55, 47, .10), (60, 42, .72), (65, 43, .08)], 1.1, "japan-blossom-branch", "#4a4943"),
    dab(61, 40, 1.6, 1.5, "#77746a"),
    ribbon([(10, 63, .10), (26, 60, .72), (43, 63, .90), (61, 59, .08)], .65, "japan-ground", "#bcb9af", dry=True),
])

write("mali", [
    ribbon([(13, 59, .10), (14, 44, .72), (17, 27, .08)], 3.0, "mali-tower-left", "#4a4943"),
    ribbon([(55, 59, .10), (54, 44, .72), (51, 26, .08)], 2.0, "mali-tower-right", "#77746a", dry=True),
    ribbon([(18, 36, .10), (30, 31, .72), (42, 33, .94), (51, 37, .08)], 2.5, "mali-mosque-body"),
    ribbon([(22, 35, .10), (22, 48, .72), (22, 59, .08)], 1.3, "mali-buttress-a"),
    ribbon([(42, 34, .10), (43, 47, .72), (43, 59, .08)], .95, "mali-buttress-b", "#77746a", dry=True),
    ribbon([(12, 60, .10), (34, 57, .92), (58, 60, .08)], 1.8, "mali-base"),
    ribbon([(17, 27, .10), (22, 25, .72), (26, 27, .08)], .72, "mali-beam-a", "#bcb9af", dry=True),
    ribbon([(47, 27, .10), (52, 24, .72), (57, 27, .08)], .65, "mali-beam-b", "#bcb9af", dry=True),
])

write("maya", [
    ribbon([(10, 59, .10), (23, 56, .72), (49, 57, .90), (62, 59, .08)], 2.7, "maya-tier-low"),
    ribbon([(16, 49, .10), (27, 46, .72), (45, 47, .90), (57, 50, .08)], 2.2, "maya-tier-mid"),
    ribbon([(22, 39, .10), (31, 36, .72), (41, 37, .90), (51, 40, .08)], 1.8, "maya-tier-high", "#4a4943"),
    ribbon([(29, 31, .10), (35, 25, .72), (43, 32, .08)], 2.0, "maya-temple-top"),
    ribbon([(35, 26, .10), (35, 37, .72), (35, 49, .94), (35, 58, .08)], 1.05, "maya-stair", "#77746a", dry=True),
    ribbon([(12, 63, .10), (28, 61, .72), (45, 64, .90), (61, 61, .08)], .65, "maya-ground", "#bcb9af", dry=True),
    dab(57, 19, 2.8, 2.8, "#77746a"),
])

write("persia", [
    ribbon([(12, 58, .10), (13, 43, .72), (16, 31, .08)], 1.8, "persia-left"),
    ribbon([(59, 58, .10), (58, 43, .72), (56, 31, .08)], 1.2, "persia-right", "#77746a", dry=True),
    ribbon([(16, 32, .10), (25, 25, .72), (35, 28, .94), (47, 24, .72), (57, 32, .08)], 2.5, "persia-roof"),
    ribbon([(25, 58, .10), (25, 46, .72), (35, 37, .94), (46, 46, .72), (46, 58, .08)], 2.0, "persia-iwan", "#4a4943"),
    ribbon([(28, 49, .10), (35, 46, .72), (43, 49, .08)], .72, "persia-inner-arch", "#bcb9af", dry=True),
    ribbon([(11, 60, .10), (35, 57, .92), (61, 60, .08)], 1.7, "persia-base"),
    dab(57, 17, 2.7, 2.7, "#77746a"),
])

write("rome", [
    ribbon([(10, 30, .10), (23, 25, .72), (38, 27, .94), (53, 24, .72), (63, 30, .08)], 2.6, "rome-crown"),
    ribbon([(12, 32, .10), (13, 45, .72), (14, 58, .08)], 1.55, "rome-left"),
    ribbon([(61, 31, .10), (59, 45, .72), (58, 57, .08)], 1.0, "rome-right", "#77746a", dry=True),
    ribbon([(19, 57, .10), (19, 47, .72), (24, 41, .94), (29, 48, .72), (29, 57, .08)], 1.6, "rome-arch-a"),
    ribbon([(32, 57, .10), (32, 46, .72), (37, 40, .94), (43, 47, .72), (43, 57, .08)], 1.45, "rome-arch-b", "#4a4943"),
    ribbon([(46, 57, .10), (46, 48, .72), (51, 42, .90), (56, 49, .08)], 1.0, "rome-arch-c", "#77746a", dry=True),
    ribbon([(10, 60, .10), (35, 57, .92), (62, 60, .08)], 1.65, "rome-base"),
    ribbon([(17, 36, .10), (34, 34, .72), (52, 36, .08)], .72, "rome-course", "#bcb9af", dry=True),
])

write("viking", [
    ribbon([(8, 49, .10), (22, 54, .72), (39, 54, 1.0), (57, 48, .08)], 5.0, "viking-hull", "#4a4943"),
    ribbon([(35, 49, .10), (35, 35, .72), (35, 19, .08)], 1.9, "viking-mast"),
    ribbon([(35, 21, .10), (24, 27, .72), (18, 41, .90), (34, 39, .08)], 2.8, "viking-sail-left"),
    ribbon([(36, 22, .10), (46, 28, .72), (52, 41, .08)], 1.5, "viking-sail-right", "#77746a", dry=True),
    ribbon([(57, 48, .10), (63, 43, .72), (66, 37, .08)], 1.7, "viking-prow"),
    ribbon([(12, 60, .10), (27, 57, .72), (43, 60, .90), (61, 56, .08)], .80, "viking-wave", "#77746a", dry=True),
    ribbon([(19, 47, .10), (25, 45, .72), (31, 47, .08)], .65, "viking-shield", "#bcb9af", dry=True),
])

write("tradition", [
    ribbon([(18, 50, .10), (21, 38, .72), (30, 31, .94), (41, 32, .82), (50, 40, .72), (52, 50, .08)], 2.8, "tradition-vessel"),
    ribbon([(18, 50, .10), (34, 55, .92), (52, 50, .08)], 2.0, "tradition-vessel-base", "#4a4943"),
    ribbon([(24, 38, .10), (35, 35, .72), (47, 39, .08)], .85, "tradition-band", "#bcb9af", dry=True),
    ribbon([(9, 38, .10), (10, 25, .68), (20, 14, .90), (34, 10, .82), (49, 14, .90), (60, 25, .72), (62, 38, .08)], 1.15, "tradition-circle", "#77746a", dry=True),
    ribbon([(35, 28, .10), (31, 23, .72), (35, 17, .94), (39, 23, .08)], 1.6, "tradition-flame", "#4a4943"),
])

# Knowledge and connective spaces remain diagrammatic by meaning, but their
# axes, nodes, pages, and weave are individually loaded brush gestures.

write("encyclopedia", [
    ribbon([(10, 21, .10), (22, 18, .72), (35, 22, .94), (35, 56, .08)], 2.0, "encyclopedia-left-page"),
    ribbon([(36, 22, .10), (49, 18, .72), (62, 21, .08)], 1.5, "encyclopedia-right-top", "#77746a", dry=True),
    ribbon([(62, 21, .10), (61, 38, .72), (61, 56, .08)], 1.2, "encyclopedia-right-edge"),
    ribbon([(10, 21, .10), (10, 38, .72), (11, 56, .08)], 1.4, "encyclopedia-left-edge", "#4a4943"),
    ribbon([(11, 56, .10), (23, 53, .72), (35, 57, .94), (48, 53, .72), (61, 56, .08)], 1.7, "encyclopedia-page-base"),
    ribbon([(18, 31, .10), (26, 29, .72), (32, 31, .08)], .72, "encyclopedia-line-a", "#bcb9af", dry=True),
    ribbon([(41, 31, .10), (49, 29, .72), (56, 31, .08)], .65, "encyclopedia-line-b", "#77746a", dry=True),
    dab(50, 43, 3.4, 3.4, "#4a4943"),
])

write("graph", [
    ribbon([(13, 58, .10), (13, 45, .72), (14, 31, .94), (14, 17, .08)], 1.8, "graph-y"),
    ribbon([(13, 58, .10), (27, 57, .72), (43, 58, .94), (61, 56, .08)], 1.8, "graph-x", "#4a4943"),
    ribbon([(18, 51, .10), (27, 45, .72), (36, 47, .94), (44, 36, .72), (53, 38, .90), (61, 24, .08)], 2.2, "graph-curve"),
    dab(27, 45, 1.6, 1.5, "#77746a"),
    dab(44, 36, 1.5, 1.4, "#4a4943"),
    dab(60, 24, 1.4, 1.3, "#77746a"),
    ribbon([(18, 54, .10), (31, 52, .72), (44, 54, .08)], .65, "graph-grid", "#bcb9af", dry=True),
])

write("net", [
    ribbon([(11, 20, .10), (11, 38, .72), (12, 58, .08)], 2.0, "net-pole-left"),
    ribbon([(61, 20, .10), (60, 39, .72), (60, 58, .08)], 1.35, "net-pole-right", "#77746a", dry=True),
    ribbon([(12, 28, .10), (24, 33, .72), (36, 37, .94), (49, 33, .72), (60, 28, .08)], 1.6, "net-top"),
    ribbon([(12, 39, .10), (24, 44, .72), (36, 48, .94), (49, 44, .72), (60, 39, .08)], 1.0, "net-bottom", "#77746a", dry=True),
    ribbon([(20, 31, .10), (25, 40, .72), (30, 47, .08)], 1.0, "net-weave-a", "#4a4943"),
    ribbon([(33, 35, .10), (36, 43, .72), (39, 48, .08)], .95, "net-weave-b", "#77746a"),
    ribbon([(47, 31, .10), (48, 40, .72), (45, 47, .08)], 1.0, "net-weave-c", "#4a4943"),
    ribbon([(17, 31, .10), (27, 39, .72), (38, 44, .90), (51, 43, .72), (57, 38, .08)], .95, "net-cross-a", "#77746a"),
    ribbon([(18, 42, .10), (28, 37, .72), (39, 35, .90), (50, 38, .72), (56, 45, .08)], .9, "net-cross-b", "#4a4943"),
])

write("network", [
    dab(12, 39, 2.5, 2.4, "#262522"),
    dab(25, 21, 2.3, 2.2, "#4a4943"),
    dab(42, 27, 2.6, 2.4, "#262522"),
    dab(58, 15, 2.1, 2.0, "#77746a"),
    dab(57, 49, 2.4, 2.2, "#4a4943"),
    dab(31, 56, 2.0, 1.9, "#77746a"),
    ribbon([(13, 38, .10), (19, 29, .72), (25, 22, .08)], 1.25, "network-link-a"),
    ribbon([(27, 22, .10), (34, 25, .72), (41, 27, .08)], 1.0, "network-link-b", "#77746a", dry=True),
    ribbon([(43, 26, .10), (51, 20, .72), (57, 15, .08)], .85, "network-link-c", "#bcb9af", dry=True),
    ribbon([(43, 29, .10), (50, 39, .72), (57, 48, .08)], 1.25, "network-link-d"),
    ribbon([(55, 49, .10), (43, 53, .72), (32, 56, .08)], .90, "network-link-e", "#77746a", dry=True),
    ribbon([(29, 55, .10), (20, 48, .72), (13, 40, .08)], 1.0, "network-link-f", "#4a4943"),
])

write("rug", [
    ribbon([(15, 14, .10), (35, 12, .92), (57, 15, .08)], 2.7, "rug-top", "#4a4943"),
    ribbon([(14, 15, .10), (13, 36, .72), (15, 58, .08)], 1.8, "rug-left"),
    ribbon([(57, 15, .10), (59, 36, .72), (57, 58, .08)], 1.2, "rug-right", "#77746a", dry=True),
    ribbon([(15, 58, .10), (35, 60, .92), (57, 58, .08)], 2.3, "rug-bottom"),
    ribbon([(36, 24, .10), (47, 36, .72), (36, 49, .94), (24, 36, .72), (36, 24, .08)], 1.7, "rug-diamond"),
    ribbon([(36, 29, .10), (42, 36, .72), (36, 43, .94), (30, 36, .72), (36, 29, .08)], .72, "rug-inner", "#bcb9af", dry=True),
    ribbon([(13, 61, .10), (11, 65, .72), (9, 67, .08)], .65, "rug-fringe-left", "#77746a", dry=True),
    ribbon([(58, 61, .10), (61, 65, .72), (64, 67, .08)], .65, "rug-fringe-right", "#bcb9af", dry=True),
])


print("redrew all 63 location PUA glyphs as naturalist sumi-e studies")
