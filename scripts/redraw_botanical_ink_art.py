#!/usr/bin/env python3
"""Render the flora and herb PUA sets as compact naturalist brush studies.

These glyphs are deliberately built from a small vocabulary of observed marks:
loaded stems, tapered leaves, dry veins, petal gestures, and irregular brush
dabs.  The vocabulary is shared across the set, while the plant structures
remain specific enough to distinguish a fern from a rosemary sprig or an
apple branch.  There are no raster textures, filters, baselines, or diagram
symbols; every visible mark is an SVG path or brush dab.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(
    values: list[tuple[float, float, float]],
    width: float,
    seed: str,
    color: str = "#262522",
    dry: bool = False,
) -> str:
    color = {
        "#dedbd4": "#85827a",
        "#bcb9af": "#716e67",
        "#77746a": "#5d5a54",
    }.get(color.lower(), color)
    # Leaves and veins that look elegant at source size must still read as
    # plant parts on a toddler-scale card. Keep their taper, but do not let the
    # loaded middle collapse below one visible pixel at 32 px.
    width = max(width * 1.30, 1.20)
    return svg_path(
        stroke_path(points(*values), width=width, seed=seed, wobble=.24),
        fill=color,
        class_name="ink-dry" if dry else "ink-wash",
    )


def stem(values: list[tuple[float, float, float]], seed: str, width: float = 1.8, color: str = "#4a4943") -> str:
    return ribbon(values, width, seed, color)


def leaf(
    base: tuple[float, float],
    tip: tuple[float, float],
    width: float,
    seed: str,
    color: str = "#4a4943",
    bend: float = 0.0,
    vein: bool = True,
) -> list[str]:
    """Make one loaded, tapered leaf with an optional dry central vein."""
    bx, by = base
    tx, ty = tip
    dx, dy = tx - bx, ty - by
    length = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / length, dx / length
    mid = (bx + dx * .48 + nx * bend, by + dy * .48 + ny * bend)
    marks = [ribbon([
        (bx, by, .12),
        (mid[0], mid[1], .92),
        (tx, ty, .10),
    ], width, f"{seed}-mass", color)]
    if vein:
        marks.append(ribbon([
            (bx + dx * .15, by + dy * .15, .16),
            (mid[0], mid[1], .62),
            (tx - dx * .10, ty - dy * .10, .05),
        ], max(.28, width * .18), f"{seed}-vein", "#77746a", dry=True))
    return marks


def blade(base: tuple[float, float], tip: tuple[float, float], width: float, seed: str, color: str = "#4a4943") -> str:
    return ribbon([
        (base[0], base[1], .10),
        ((base[0] + tip[0]) * .5, (base[1] + tip[1]) * .5, .82),
        (tip[0], tip[1], .08),
    ], width, seed, color)


def dab(cx: float, cy: float, rx: float, ry: float, color: str = "#262522") -> str:
    # An ellipse is a vector brush-loaded dab, not a UI dot or raster texture.
    color = {"#bcb9af": "#716e67", "#77746a": "#5d5a54"}.get(color.lower(), color)
    return f'<ellipse class="ink-wash" cx="{cx:.2f}" cy="{cy:.2f}" rx="{max(rx * 1.12, 1.2):.2f}" ry="{max(ry * 1.12, 1.1):.2f}" fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'


def flower(cx: float, cy: float, radius: float, petals: int, seed: str, color: str = "#4a4943") -> list[str]:
    marks: list[str] = []
    for index in range(petals):
        angle = 2 * math.pi * index / petals - math.pi / 2
        base = (cx + math.cos(angle) * 1.0, cy + math.sin(angle) * 1.0)
        tip = (cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)
        marks.extend(leaf(base, tip, max(.85, radius * .28), f"{seed}-petal-{index}", color, bend=math.sin(index * 1.7) * .7, vein=False))
    marks.append(dab(cx, cy, radius * .22, radius * .20, "#262522"))
    return marks


def branch_cluster(cx: float, cy: float, count: int, radius: float, seed: str, color: str = "#262522") -> list[str]:
    marks: list[str] = []
    for index in range(count):
        angle = -math.pi * .92 + math.pi * .84 * index / max(1, count - 1)
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        marks.append(dab(x, y, 1.35 - index * .05, 1.15 - index * .04, color if index % 2 else "#4a4943"))
    return marks


def irregular_mass(d: str, fill: str, detail: str = "organic-mass-v1") -> str:
    fill = {"#bcb9af": "#716e67", "#77746a": "#5d5a54"}.get(fill.lower(), fill)
    return f'<path class="ink-wash" fill="{fill}" d="{d}" data-ink-ribbon="{detail}"/>'


def target_path(category: str, name: str) -> tuple[Path, str]:
    target = ROOT / "assets/pua" / category / f"{name}.svg"
    match = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {category}/{name}")
    return target, match.group(0)


def write(category: str, name: str, marks: list[str]) -> None:
    target, codepoint = target_path(category, name)
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="{category} / {name}" {codepoint} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>{category} / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


def flora() -> None:
    write("flora", "apple", [
        '<path class="ink-wash" d="M36 28 C31 23 23 25 20 33 C16 43 22 55 34 59 C46 58 54 48 52 37 C50 27 42 23 36 28 Z" fill="none" stroke="#262522" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" data-ink-brush-pass="loaded-contour-v2"/>',
        ribbon([(32, 30, .12), (25, 38, .92), (31, 53, .10)], 5.8, "apple-body-left", "#bcb9af"),
        ribbon([(39, 30, .12), (47, 38, .88), (40, 53, .10)], 5.2, "apple-body-right", "#77746a"),
        ribbon([(28, 51, .10), (35, 56, .72), (43, 51, .08)], .9, "apple-bottom-lobe", "#4a4943"),
        stem([(36, 27, .10), (35, 21, .72), (38, 15, .08)], "apple-stem", 1.8, "#262522"),
        *leaf((36, 21), (48, 17), 3.2, "apple-leaf", "#4a4943", bend=1.3),
        ribbon([(25, 35, .12), (28, 31, .65), (32, 31, .08)], .55, "apple-highlight", "#77746a", dry=True),
    ])
    write("flora", "berrybush", [
        stem([(17, 57, .10), (28, 43, .92), (39, 30, .72), (51, 17, .08)], "berry-stem", 2.7, "#262522"),
        stem([(30, 41, .10), (22, 35, .74), (17, 27, .08)], "berry-branch-low", 1.25),
        stem([(40, 29, .10), (49, 30, .74), (57, 25, .08)], "berry-branch-high", 1.15),
        *leaf((28, 43), (18, 42), 3.0, "berry-leaf-low", bend=-1.3, color="#77746a"),
        *leaf((40, 29), (51, 33), 2.7, "berry-leaf-high", bend=1.2),
        *branch_cluster(18, 26, 3, 3.8, "berry-cluster-guest", "#77746a"),
        *branch_cluster(53, 18, 6, 6.0, "berry-cluster-host", "#262522"),
    ])
    write("flora", "birch", [
        irregular_mass("M 17 28 C 17 20 24 15 31 17 C 34 10 43 10 47 17 C 54 17 59 23 56 30 C 50 35 42 34 36 31 C 29 36 20 34 17 28 Z", "#716e67", "birch-airy-crown-v1"),
        stem([(36, 61, .12), (34, 48, .72), (36, 34, 1.0), (34, 19, .08)], "birch-trunk", 3.0, "#4a4943"),
        stem([(35, 38, .1), (27, 30, .76), (20, 21, .08)], "birch-left", 1.35),
        stem([(35, 33, .1), (43, 27, .76), (51, 18, .08)], "birch-right", 1.25),
        *leaf((27, 30), (20, 25), 1.55, "birch-leaf-l", bend=-.7, color="#77746a"),
        *leaf((43, 27), (51, 23), 1.55, "birch-leaf-r", bend=.7, color="#77746a"),
        ribbon([(32, 30, .14), (36, 29, .72), (39, 30, .08)], .55, "birch-bark-1", "#77746a", dry=True),
        ribbon([(32, 40, .14), (36, 39, .72), (39, 40, .08)], .55, "birch-bark-2", "#77746a", dry=True),
    ])
    write("flora", "bush", [
        irregular_mass("M 14 47 C 11 39 16 32 24 33 C 27 25 37 23 42 30 C 50 27 59 33 58 42 C 56 51 46 54 36 51 C 27 56 17 53 14 47 Z", "#5d5a54", "bush-cluster-v1"),
        stem([(36, 59, .1), (35, 47, .78), (36, 38, .08)], "bush-trunk", 2.6),
        *leaf((34, 46), (20, 37), 5.0, "bush-left", bend=-1.5, color="#bcb9af"),
        *leaf((35, 44), (35, 30), 5.3, "bush-center", bend=1.0, color="#4a4943"),
        *leaf((37, 46), (53, 36), 5.0, "bush-right", bend=1.5, color="#bcb9af"),
        stem([(30, 48, .1), (25, 43, .78), (20, 41, .08)], "bush-twig-l", .85, "#262522"),
        stem([(42, 48, .1), (48, 42, .78), (54, 40, .08)], "bush-twig-r", .85, "#262522"),
    ])
    write("flora", "fern", [
        stem([(25, 60, .1), (30, 48, .75), (38, 36, 1.0), (48, 20, .08)], "fern-rachis", 1.7),
        *leaf((31, 48), (21, 40), 2.2, "fern-l1", bend=-.9),
        *leaf((33, 43), (23, 34), 2.0, "fern-l2", bend=-.8),
        *leaf((35, 38), (27, 28), 1.8, "fern-l3", bend=-.7),
        *leaf((31, 48), (43, 43), 2.2, "fern-r1", bend=.8),
        *leaf((34, 43), (47, 35), 2.0, "fern-r2", bend=.8),
        *leaf((37, 37), (51, 28), 1.8, "fern-r3", bend=.7),
    ])
    write("flora", "grass", [
        blade((29, 60), (15, 31), 2.4, "grass-l2", "#77746a"),
        blade((29, 60), (25, 15), 3.0, "grass-l1", "#262522"),
        blade((29, 60), (34, 27), 2.1, "grass-c", "#4a4943"),
        blade((30, 60), (46, 20), 2.7, "grass-r1", "#77746a"),
        blade((31, 60), (55, 36), 1.8, "grass-r2", "#4a4943"),
    ])
    write("flora", "maple", [
        stem([(36, 60, .1), (36, 47, .76), (36, 33, .08)], "maple-stem", 1.8),
        *leaf((36, 34), (36, 17), 4.3, "maple-top", bend=0),
        *leaf((35, 34), (23, 25), 3.8, "maple-left", bend=-1.4),
        *leaf((37, 34), (49, 25), 3.8, "maple-right", bend=1.4),
        *leaf((35, 35), (28, 39), 3.0, "maple-low-l", bend=-.8, color="#77746a"),
        *leaf((37, 35), (44, 39), 3.0, "maple-low-r", bend=.8, color="#77746a"),
        ribbon([(36, 33, .12), (36, 25, .72), (36, 19, .08)], .38, "maple-vein", "#77746a", dry=True),
    ])
    write("flora", "palm", [
        stem([(34, 61, .1), (33, 48, .76), (37, 29, .08)], "palm-trunk", 2.8),
        *leaf((37, 29), (17, 21), 3.1, "palm-frond-l", bend=-1.8),
        *leaf((37, 29), (25, 13), 3.0, "palm-frond-l2", bend=-1.0),
        *leaf((37, 29), (37, 10), 3.1, "palm-frond-c", bend=0),
        *leaf((37, 29), (51, 16), 3.0, "palm-frond-r", bend=1.0),
        *leaf((37, 29), (58, 25), 3.1, "palm-frond-r2", bend=1.8),
        ribbon([(33, 42, .12), (36, 41, .72), (37, 42, .08)], .52, "palm-bark-1", "#77746a", dry=True),
        ribbon([(32, 51, .12), (35, 50, .72), (36, 51, .08)], .52, "palm-bark-2", "#77746a", dry=True),
    ])
    write("flora", "pine", [
        ribbon([(36, 17, .14), (31, 23, .92), (24, 29, .08)], 5.3, "pine-loaded-top-left", "#4a4943"),
        ribbon([(36, 18, .14), (41, 23, .92), (48, 30, .08)], 4.7, "pine-loaded-top-right", "#716e67"),
        ribbon([(36, 31, .14), (28, 37, .96), (18, 43, .08)], 6.0, "pine-loaded-mid-left", "#5d5a54"),
        ribbon([(36, 32, .14), (44, 38, .96), (54, 45, .08)], 5.5, "pine-loaded-mid-right", "#4a4943"),
        ribbon([(35, 43, .14), (29, 48, .92), (21, 52, .08)], 4.8, "pine-loaded-low-left", "#716e67"),
        stem([(36, 61, .1), (36, 45, .76), (36, 17, .08)], "pine-trunk", 2.1),
        *leaf((36, 48), (20, 45), 3.2, "pine-lower-l", bend=-1.2), *leaf((36, 48), (52, 45), 3.2, "pine-lower-r", bend=1.2),
        *leaf((36, 40), (23, 36), 2.9, "pine-mid-l", bend=-1.0), *leaf((36, 40), (49, 36), 2.9, "pine-mid-r", bend=1.0),
        *leaf((36, 32), (27, 27), 2.5, "pine-top-l", bend=-.8), *leaf((36, 32), (45, 27), 2.5, "pine-top-r", bend=.8),
        blade((36, 29), (36, 13), 2.2, "pine-leader"),
    ])
    write("flora", "poplar", [
        irregular_mass("M 36 10 C 28 16 25 27 27 38 C 25 47 30 54 36 56 C 43 53 47 45 45 36 C 47 26 43 16 36 10 Z", "#716e67", "poplar-column-crown-v1"),
        stem([(36, 61, .1), (36, 46, .76), (36, 18, .08)], "poplar-trunk", 2.3),
        *leaf((36, 38), (29, 19), 6.0, "poplar-crown-l", bend=-1.3, color="#bcb9af"),
        *leaf((36, 37), (43, 19), 6.0, "poplar-crown-r", bend=1.3, color="#4a4943"),
        *leaf((36, 31), (36, 12), 4.0, "poplar-crown-top", bend=0, color="#77746a"),
        ribbon([(34, 30, .12), (36, 24, .72), (38, 20, .08)], .45, "poplar-vein", "#77746a", dry=True),
    ])
    write("flora", "reed", [
        stem([(20, 61, .1), (23, 43, .76), (30, 23, .08)], "reed-l", 1.25, "#77746a"),
        stem([(29, 61, .1), (34, 39, .92), (45, 14, .08)], "reed-c", 1.75, "#262522"),
        stem([(41, 61, .1), (45, 45, .76), (53, 29, .08)], "reed-r", 1.3, "#4a4943"),
        *branch_cluster(30, 20, 3, 3.2, "reed-head-l", "#77746a"),
        *branch_cluster(46, 12, 6, 5.0, "reed-head-c", "#262522"),
        *branch_cluster(54, 27, 4, 3.5, "reed-head-r", "#4a4943"),
    ])
    write("flora", "snag", [
        stem([(36, 61, .1), (35, 46, .78), (36, 30, .08)], "snag-trunk", 3.6),
        stem([(36, 35, .1), (26, 26, .76), (19, 17, .08)], "snag-left", 2.0),
        stem([(36, 33, .1), (45, 24, .76), (52, 14, .08)], "snag-right", 1.9),
        stem([(35, 43, .1), (28, 38, .76), (23, 31, .08)], "snag-low", 1.45, "#77746a"),
        ribbon([(32, 40, .1), (36, 38, .72), (39, 40, .08)], .55, "snag-scar-1", "#77746a", dry=True),
        ribbon([(32, 49, .1), (35, 47, .72), (39, 49, .08)], .55, "snag-scar-2", "#77746a", dry=True),
    ])
    write("flora", "spruce", [
        irregular_mass("M 36 12 C 32 20 28 26 24 32 L 30 32 C 25 38 21 44 17 50 C 25 48 31 49 36 52 C 42 49 48 49 56 51 C 51 44 47 39 42 33 L 48 33 C 43 27 40 20 36 12 Z", "#716e67", "spruce-layered-crown-v1"),
        stem([(36, 61, .1), (36, 44, .76), (36, 15, .08)], "spruce-trunk", 2.0),
        *leaf((36, 49), (21, 51), 3.2, "spruce-lower-l", bend=-1.0), *leaf((36, 49), (51, 51), 3.2, "spruce-lower-r", bend=1.0),
        *leaf((36, 41), (24, 42), 2.9, "spruce-mid-l", bend=-.8), *leaf((36, 41), (48, 42), 2.9, "spruce-mid-r", bend=.8),
        *leaf((36, 33), (28, 34), 2.5, "spruce-top-l", bend=-.7), *leaf((36, 33), (44, 34), 2.5, "spruce-top-r", bend=.7),
        blade((36, 30), (36, 13), 2.0, "spruce-leader"),
    ])
    write("flora", "stump", [
        irregular_mass("M 24 36 C 29 33 43 33 49 36 L 48 55 C 43 59 29 59 24 55 Z", "#bcb9af"),
        ribbon([(24, 36, .12), (31, 33, .8), (40, 34, 1.0), (49, 36, .08)], 1.8, "stump-top", "#262522"),
        ribbon([(28, 36, .12), (35, 35, .72), (44, 36, .08)], .85, "stump-growth-ring", "#4a4943", dry=True),
        ribbon([(28, 40, .12), (35, 38, .72), (42, 40, .08)], .55, "stump-ring-1", "#77746a", dry=True),
        ribbon([(27, 47, .12), (35, 45, .72), (44, 47, .08)], .55, "stump-ring-2", "#77746a", dry=True),
        ribbon([(26, 54, .12), (34, 52, .72), (46, 54, .08)], .55, "stump-bark", "#4a4943", dry=True),
        ribbon([(29, 54, .12), (23, 58, .72), (17, 60, .08)], 1.5, "stump-root-left", "#262522"),
        ribbon([(43, 54, .12), (49, 58, .72), (56, 60, .08)], 1.5, "stump-root-right", "#4a4943"),
        ribbon([(47, 42, .12), (53, 38, .72), (57, 33, .08)], 1.25, "stump-branch-stub", "#262522"),
    ])
    write("flora", "willow", [
        irregular_mass("M 18 34 C 18 25 26 19 36 20 C 46 17 55 24 55 34 C 52 40 46 42 39 39 C 31 43 22 41 18 34 Z", "#716e67", "willow-crown-v1"),
        stem([(36, 61, .1), (36, 48, .76), (37, 32, .08)], "willow-trunk", 3.0),
        *leaf((37, 34), (20, 27), 5.2, "willow-crown-l", bend=-1.5, color="#bcb9af"),
        *leaf((37, 34), (51, 26), 5.2, "willow-crown-r", bend=1.5, color="#4a4943"),
        *leaf((37, 35), (27, 19), 4.0, "willow-crown-top-l", bend=-1.0, color="#77746a"),
        *leaf((37, 35), (46, 18), 4.0, "willow-crown-top-r", bend=1.0, color="#bcb9af"),
        blade((25, 35), (22, 58), 1.25, "willow-drop-l", "#4a4943"),
        blade((32, 36), (30, 60), 1.25, "willow-drop-m", "#77746a"),
        blade((43, 35), (46, 59), 1.25, "willow-drop-r", "#4a4943"),
        blade((49, 33), (54, 55), 1.25, "willow-drop-far", "#77746a"),
    ])


def herbs() -> None:
    write("herbs", "aloe", [
        *leaf((36, 58), (21, 27), 4.0, "aloe-l", bend=-1.2, color="#4a4943"),
        *leaf((36, 58), (29, 18), 4.5, "aloe-mid-l", bend=-.6, color="#77746a"),
        *leaf((36, 58), (36, 14), 4.8, "aloe-center", bend=0, color="#262522"),
        *leaf((36, 58), (45, 18), 4.5, "aloe-mid-r", bend=.6, color="#77746a"),
        *leaf((36, 58), (53, 28), 4.0, "aloe-r", bend=1.2, color="#4a4943"),
    ])
    write("herbs", "basil", [
        stem([(36, 60, .1), (35, 44, .76), (36, 22, .08)], "basil-stem", 1.9),
        *leaf((35, 47), (20, 36), 3.8, "basil-l-low", bend=-1.2), *leaf((36, 45), (52, 34), 3.8, "basil-r-low", bend=1.2),
        *leaf((35, 35), (23, 25), 3.2, "basil-l-high", bend=-1.0, color="#77746a"), *leaf((36, 34), (48, 23), 3.2, "basil-r-high", bend=1.0, color="#77746a"),
        *flower(36, 19, 4.0, 5, "basil-flower", "#4a4943"),
    ])
    write("herbs", "calendula", [
        stem([(27, 61, .1), (32, 45, .82), (42, 27, .08)], "calendula-stem", 1.8, "#262522"),
        *flower(44, 20, 9.0, 8, "calendula-flower", "#4a4943"),
        *leaf((32, 45), (18, 37), 3.1, "calendula-host-leaf", bend=-1.3, color="#4a4943"),
        *leaf((36, 38), (50, 33), 2.2, "calendula-guest-leaf", bend=1.0, color="#77746a"),
    ])
    write("herbs", "chamomile", [
        stem([(34, 60, .1), (33, 43, .76), (30, 25, .08)], "chamomile-stem-l", 1.25),
        stem([(36, 46, .1), (43, 35, .76), (47, 25, .08)], "chamomile-stem-r", 1.15),
        *flower(30, 22, 7.0, 8, "chamomile-flower-l", "#77746a"),
        *flower(47, 25, 5.5, 7, "chamomile-flower-r", "#77746a"),
        *leaf((34, 46), (23, 42), 1.8, "chamomile-leaf", bend=-.6, color="#4a4943"),
    ])
    write("herbs", "chive", [
        blade((36, 60), (25, 22), 2.4, "chive-l1"), blade((36, 60), (31, 16), 2.6, "chive-l2", "#4a4943"),
        blade((36, 60), (36, 13), 2.7, "chive-c"), blade((36, 60), (42, 15), 2.6, "chive-r1", "#4a4943"),
        blade((36, 60), (49, 24), 2.4, "chive-r2", "#77746a"), *flower(36, 14, 5.0, 6, "chive-flower", "#4a4943"),
    ])
    write("herbs", "cilantro", [
        stem([(36, 60, .1), (34, 45, .76), (32, 29, .08)], "cilantro-stem-l", 1.5),
        stem([(36, 60, .1), (40, 45, .76), (43, 30, .08)], "cilantro-stem-r", 1.5),
        *leaf((32, 30), (22, 24), 2.4, "cilantro-l1", bend=-.8), *leaf((32, 30), (29, 19), 2.4, "cilantro-l2", bend=-.3), *leaf((32, 30), (39, 25), 2.4, "cilantro-l3", bend=.8),
        *leaf((43, 30), (36, 22), 2.4, "cilantro-r1", bend=-.8), *leaf((43, 30), (46, 19), 2.4, "cilantro-r2", bend=.3), *leaf((43, 30), (53, 25), 2.4, "cilantro-r3", bend=.8),
    ])
    write("herbs", "dandelion", [
        stem([(36, 60, .1), (36, 42, .76), (36, 20, .08)], "dandelion-stem", 1.5),
        *flower(36, 17, 8.0, 10, "dandelion-flower", "#77746a"),
        *leaf((36, 57), (24, 47), 3.4, "dandelion-l", bend=-1.3), *leaf((36, 57), (48, 47), 3.4, "dandelion-r", bend=1.3),
    ])
    write("herbs", "dill", [
        stem([(36, 60, .1), (36, 42, .76), (37, 21, .08)], "dill-stem", 1.4),
        *branch_cluster(37, 18, 6, 8.0, "dill-flower", "#4a4943"),
        *leaf((36, 44), (24, 36), 1.8, "dill-leaf-l", bend=-.9, color="#77746a"), *leaf((36, 40), (49, 32), 1.8, "dill-leaf-r", bend=.9, color="#77746a"),
    ])
    write("herbs", "echinacea", [
        stem([(36, 60, .1), (36, 42, .76), (36, 26, .08)], "echinacea-stem", 1.7),
        *flower(36, 22, 9.0, 8, "echinacea-petals", "#77746a"), dab(36, 22, 3.4, 4.2, "#262522"),
        *leaf((36, 45), (24, 39), 2.6, "echinacea-leaf", bend=-.8, color="#4a4943"),
    ])
    write("herbs", "elderberry", [
        stem([(36, 60, .1), (37, 45, .76), (40, 29, .08)], "elder-stem", 1.9),
        stem([(39, 30, .1), (31, 23, .76), (25, 18, .08)], "elder-branch-l", 1.0),
        stem([(39, 30, .1), (47, 24, .76), (53, 18, .08)], "elder-branch-r", 1.0),
        *branch_cluster(25, 18, 5, 4.5, "elder-cluster-l"), *branch_cluster(53, 18, 5, 4.5, "elder-cluster-r"),
        *leaf((37, 44), (24, 37), 3.0, "elder-leaf-l", bend=-1.1, color="#77746a"), *leaf((39, 40), (53, 33), 3.0, "elder-leaf-r", bend=1.1, color="#4a4943"),
    ])
    write("herbs", "garlic", [
        irregular_mass("M 27 43 C 30 39 34 38 36 40 C 39 38 44 40 46 44 L 44 55 C 41 60 31 60 28 55 Z", "#bcb9af"),
        stem([(36, 42, .1), (35, 31, .76), (39, 18, .08)], "garlic-stem", 2.2, "#262522"),
        *leaf((36, 31), (29, 19), 2.6, "garlic-leaf-l", bend=-.8, color="#4a4943"), *leaf((38, 30), (45, 18), 2.6, "garlic-leaf-r", bend=.8, color="#77746a"),
        ribbon([(31, 47, .12), (36, 50, .72), (42, 47, .08)], .5, "garlic-clove", "#77746a", dry=True),
    ])
    write("herbs", "ginger", [
        irregular_mass("M 18 47 C 24 41 31 42 36 44 C 41 40 49 42 55 47 C 51 53 44 52 38 51 C 31 55 23 53 18 47 Z", "#bcb9af"),
        *leaf((29, 43), (27, 24), 3.0, "ginger-leaf-l", bend=-.8, color="#4a4943"), *leaf((39, 44), (43, 21), 3.0, "ginger-leaf-r", bend=.8, color="#77746a"),
        ribbon([(24, 47, .12), (31, 49, .72), (38, 47, .08)], .5, "ginger-root-1", "#77746a", dry=True),
        ribbon([(35, 50, .12), (42, 48, .72), (50, 48, .08)], .5, "ginger-root-2", "#4a4943", dry=True),
    ])
    write("herbs", "lavender", [
        stem([(36, 60, .1), (35, 44, .76), (36, 22, .08)], "lavender-stem", 1.55),
        *leaf((35, 46), (25, 39), 1.9, "lavender-leaf-l", bend=-.8, color="#77746a"), *leaf((36, 43), (47, 36), 1.9, "lavender-leaf-r", bend=.8, color="#77746a"),
        *flower(36, 19, 7.5, 6, "lavender-flower", "#4a4943"),
    ])
    write("herbs", "mint", [
        stem([(36, 60, .1), (35, 46, .76), (36, 28, .08)], "mint-stem", 1.8),
        *leaf((35, 48), (20, 38), 4.0, "mint-l-low", bend=-1.2), *leaf((36, 46), (52, 35), 4.0, "mint-r-low", bend=1.2),
        *leaf((35, 37), (23, 28), 3.2, "mint-l-high", bend=-1.0, color="#77746a"), *leaf((36, 35), (48, 25), 3.2, "mint-r-high", bend=1.0, color="#77746a"),
    ])
    write("herbs", "nettle", [
        stem([(36, 60, .1), (36, 44, .76), (36, 23, .08)], "nettle-stem", 1.7),
        *leaf((36, 48), (22, 38), 3.6, "nettle-l-low", bend=-1.0), *leaf((36, 47), (50, 37), 3.6, "nettle-r-low", bend=1.0),
        *leaf((36, 36), (26, 26), 3.0, "nettle-l-high", bend=-.8, color="#77746a"), *leaf((36, 35), (46, 25), 3.0, "nettle-r-high", bend=.8, color="#77746a"),
        ribbon([(26, 38, .1), (28, 36, .72), (30, 37, .08)], .38, "nettle-edge-l", "#262522", dry=True),
        ribbon([(42, 37, .1), (44, 35, .72), (46, 36, .08)], .38, "nettle-edge-r", "#262522", dry=True),
    ])
    write("herbs", "oregano", [
        stem([(36, 60, .1), (35, 44, .76), (34, 25, .08)], "oregano-stem", 1.7),
        *leaf((35, 45), (23, 36), 3.3, "oregano-l", bend=-1.0, color="#77746a"), *leaf((35, 43), (49, 34), 3.3, "oregano-r", bend=1.0, color="#4a4943"),
        *flower(29, 26, 5.0, 6, "oregano-flower-l", "#77746a"), *flower(43, 25, 5.0, 6, "oregano-flower-r", "#4a4943"),
    ])
    write("herbs", "parsley", [
        stem([(36, 60, .1), (34, 44, .76), (29, 29, .08)], "parsley-stem-l", 1.4),
        stem([(36, 60, .1), (38, 43, .76), (44, 31, .08)], "parsley-stem-r", 1.4),
        *leaf((29, 29), (20, 22), 2.7, "parsley-l1", bend=-.8), *leaf((29, 29), (29, 18), 2.7, "parsley-l2", bend=0), *leaf((29, 29), (39, 23), 2.7, "parsley-l3", bend=.8),
        *leaf((44, 31), (37, 22), 2.7, "parsley-r1", bend=-.8), *leaf((44, 31), (47, 20), 2.7, "parsley-r2", bend=0), *leaf((44, 31), (55, 25), 2.7, "parsley-r3", bend=.8),
    ])
    write("herbs", "plantain", [
        *leaf((36, 59), (21, 39), 4.1, "plantain-l", bend=-1.3), *leaf((36, 59), (28, 28), 4.0, "plantain-l2", bend=-.6),
        *leaf((36, 59), (36, 23), 4.4, "plantain-c", bend=0), *leaf((36, 59), (44, 28), 4.0, "plantain-r2", bend=.6), *leaf((36, 59), (52, 39), 4.1, "plantain-r", bend=1.3),
    ])
    write("herbs", "rosemary", [
        stem([(36, 60, .1), (35, 44, .76), (38, 20, .08)], "rosemary-stem", 1.8),
        *leaf((35, 49), (24, 42), 1.8, "rosemary-l1", bend=-.7), *leaf((36, 46), (48, 39), 1.8, "rosemary-r1", bend=.7),
        *leaf((36, 39), (27, 32), 1.7, "rosemary-l2", bend=-.7, color="#77746a"), *leaf((37, 36), (49, 29), 1.7, "rosemary-r2", bend=.7, color="#77746a"),
        *leaf((38, 30), (31, 24), 1.5, "rosemary-l3", bend=-.6), *leaf((38, 27), (46, 21), 1.5, "rosemary-r3", bend=.6),
    ])
    write("herbs", "sage", [
        stem([(36, 60, .1), (35, 46, .76), (36, 30, .08)], "sage-stem", 1.9),
        *leaf((35, 48), (17, 40), 5.0, "sage-l", bend=-1.6, color="#bcb9af"), *leaf((36, 43), (56, 34), 5.0, "sage-r", bend=1.6, color="#4a4943"),
        ribbon([(20, 40, .12), (28, 43, .72), (34, 46, .08)], .55, "sage-vein-l", "#262522", dry=True),
        ribbon([(39, 42, .12), (47, 39, .72), (54, 35, .08)], .55, "sage-vein-r", "#77746a", dry=True),
    ])
    write("herbs", "thyme", [
        stem([(36, 60, .1), (34, 45, .76), (31, 29, .08)], "thyme-stem-l", 1.35),
        stem([(36, 60, .1), (38, 44, .76), (41, 28, .08)], "thyme-stem-r", 1.35),
        *leaf((33, 45), (24, 38), 1.8, "thyme-l1", bend=-.7), *leaf((35, 39), (27, 32), 1.7, "thyme-l2", bend=-.7),
        *leaf((38, 44), (49, 37), 1.8, "thyme-r1", bend=.7), *leaf((40, 37), (51, 30), 1.7, "thyme-r2", bend=.7),
        *branch_cluster(31, 28, 4, 3.0, "thyme-bloom", "#77746a"),
    ])
    write("herbs", "yarrow", [
        stem([(36, 60, .1), (36, 43, .76), (36, 24, .08)], "yarrow-stem", 1.5),
        *leaf((36, 48), (24, 41), 2.0, "yarrow-l", bend=-.8, color="#4a4943"), *leaf((36, 43), (49, 36), 2.0, "yarrow-r", bend=.8, color="#77746a"),
        *flower(36, 19, 8.0, 9, "yarrow-flower", "#4a4943"),
    ])


if __name__ == "__main__":
    flora()
    herbs()
    print("redrew 37 flora and herb glyphs as naturalist vector brush studies")
