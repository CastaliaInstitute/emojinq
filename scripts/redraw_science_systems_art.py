#!/usr/bin/env python3
"""Replace diagrammatic science symbols with authored sumi-e brush studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def dab(x: float, y: float, r: float, color: str = "#3c3b36") -> str:
    return f'<ellipse class="ink-wash" cx="{x}" cy="{y}" rx="{r}" ry="{r * .88}" fill="{color}"/>'


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/science" / f"{name}.svg"
    original = target.read_text()
    match = re.search(r'data-pua="([^"]+)"', original)
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 8 63 C 22 61 39 64 64 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {match.group(0)} data-castalia-style="sumi-e-brush-art-v4" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>science / {name} — authored sumi-e brush study</title>{''.join(marks)}</svg>
''')


def ribbon(points, width, seed, color="#262522", wobble=.24):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color)


# Algorithm: a left-to-right decision stream that visibly branches and rejoins.
# The open spacing and endpoint tapers preserve a sense of sequence without
# introducing literal arrowheads that would dominate the brush composition.
algorithm = [
    ribbon([(10, 36, .16), (17, 35, .58), (24, 36, .95), (30, 36, .28)], 2.0, "algorithm-entry"),
    ribbon([(30, 36, .2), (37, 27, .68), (45, 23, 1.0), (56, 24, .25)], 1.7, "algorithm-upper-branch"),
    ribbon([(30, 36, .2), (37, 44, .68), (45, 49, 1.0), (56, 48, .25)], 1.7, "algorithm-lower-branch"),
    ribbon([(56, 24, .2), (60, 30, .7), (62, 36, 1.0), (66, 36, .18)], 1.55, "algorithm-upper-return"),
    ribbon([(56, 48, .2), (60, 42, .7), (62, 36, 1.0), (66, 36, .18)], 1.55, "algorithm-lower-return"),
]
for x, y, r in [(10, 36, 2.3), (30, 36, 3.0), (56, 24, 2.2), (56, 48, 2.2), (66, 36, 1.7)]: algorithm.append(dab(x, y, r, "#4a4943"))
write("algorithm", algorithm)


# Network: sparse connected brush dabs, with enough negative space to breathe.
network_nodes = [(16, 35), (24, 21), (35, 16), (47, 23), (57, 36), (45, 49), (30, 52), (25, 38)]
network_edges = [(0, 1), (1, 2), (1, 7), (2, 3), (2, 7), (3, 4), (3, 5), (7, 6), (6, 5), (5, 4), (0, 7)]
network = [ribbon([(*network_nodes[a], .2), ((network_nodes[a][0] + network_nodes[b][0]) / 2 + (a - b) * .35, (network_nodes[a][1] + network_nodes[b][1]) / 2, .82), (*network_nodes[b], .25)], 1.0, f"network-{a}-{b}", "#4a4943", .3) for a, b in network_edges]
network += [dab(x, y, 2.35, "#262522") for x, y in network_nodes]
write("network", network)


# Signal: a crooked mast with three asymmetrical broadcast waves.
signal = [
    ribbon([(36, 56, .18), (35, 47, .72), (36, 38, 1.0), (35, 29, .25)], 2.1, "signal-mast"),
    ribbon([(34, 28, .2), (36, 24, .78), (37, 20, .3)], 1.5, "signal-tip"),
    ribbon([(28, 32, .2), (23, 29, .55), (21, 25, .94), (22, 21, .25)], 1.45, "signal-left-1"),
    ribbon([(24, 36, .2), (17, 32, .62), (14, 26, .9), (15, 19, .2)], 1.1, "signal-left-2"),
    ribbon([(44, 31, .2), (49, 28, .58), (51, 24, .94), (50, 20, .2)], 1.45, "signal-right-1"),
    ribbon([(48, 36, .2), (55, 32, .62), (58, 26, .9), (57, 18, .2)], 1.1, "signal-right-2"),
    dab(36, 28, 2.8, "#3c3b36"),
]
write("signal", signal)


# Technology: a central ink seal with four practical connections.
technology = [
    ribbon([(28, 30, .2), (30, 25, .7), (35, 23, 1.0), (41, 25, .65), (44, 30, .2), (42, 35, .8), (36, 37, 1.0), (30, 35, .3), (28, 30, .2)], 2.0, "technology-core", "#262522", .28),
    ribbon([(29, 29, .2), (23, 24, .65), (17, 21, .25)], 1.25, "technology-nw"),
    ribbon([(43, 29, .2), (50, 24, .65), (56, 20, .25)], 1.25, "technology-ne"),
    ribbon([(30, 35, .2), (24, 42, .65), (18, 48, .25)], 1.25, "technology-sw"),
    ribbon([(42, 35, .2), (49, 42, .65), (56, 48, .25)], 1.25, "technology-se"),
]
technology += [dab(x, y, 2.1, "#4a4943") for x, y in [(17, 21), (56, 20), (18, 48), (56, 48)]]
write("technology", technology)


# Code: a broad sheet-like wash with a few handwritten syntax marks.
code = [
    ribbon([(13, 20, .2), (23, 17, .72), (37, 18, 1.0), (52, 17, .72), (60, 21, .2), (59, 48, .3), (50, 53, .8), (35, 54, 1.0), (20, 52, .5), (13, 48, .2), (13, 20, .2)], 1.55, "code-sheet", "#4a4943", .26),
    ribbon([(26, 29, .18), (22, 32, .58), (20, 36, .92), (24, 41, .25)], 2.35, "code-left", "#262522", .3),
    ribbon([(38, 29, .2), (42, 33, .68), (44, 36, .96), (40, 41, .2)], 2.35, "code-right", "#262522", .3),
    ribbon([(51, 29, .2), (48, 34, .64), (45, 39, .95), (42, 43, .25)], 1.65, "code-slash", "#3c3b36", .3),
    ribbon([(19, 25, .2), (27, 24, .7), (35, 25, .25)], .85, "code-header", "#77746a", .25),
]
write("code", code)


# Hypothesis: a rolled research leaf with a questioning brush mark.
hypothesis = [
    ribbon([(17, 22, .2), (26, 18, .65), (39, 18, 1.0), (53, 21, .7), (59, 28, .25), (58, 45, .3), (51, 51, .76), (36, 54, 1.0), (22, 51, .55), (16, 45, .2), (17, 22, .2)], 1.55, "hypothesis-scroll", "#4a4943", .3),
    ribbon([(34, 30, .2), (36, 27, .7), (41, 28, 1.0), (44, 31, .5), (43, 35, .2), (39, 38, .55), (39, 42, .2)], 1.65, "hypothesis-question", "#262522", .28),
    dab(39, 47, 1.45, "#262522"),
]
write("hypothesis", hypothesis)

print("redrew algorithm, network, signal, technology, code, and hypothesis")
