#!/usr/bin/env python3
"""Render sage as layered botanical brush gestures."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "assets/pua/herbs/sage.svg"


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*v) for v in values]


def main() -> None:
    original = TARGET.read_text()
    cp = re.search(r'data-pua="([^"]+)"', original)
    if not cp:
        raise SystemExit("missing sage PUA code point")
    stem = p((36, 63, .28), (35, 54, .62), (34, 45, .82), (35, 36, .9), (39, 27, .45), (43, 20, .2))
    branch_l = p((35, 48, .2), (28, 43, .6), (20, 38, .75), (14, 31, .3))
    branch_r = p((35, 41, .2), (43, 37, .65), (52, 32, .8), (60, 25, .28))
    branch_top = p((38, 31, .2), (33, 25, .55), (31, 18, .25))
    leaves = [
        p((29, 43, .25), (24, 41, .75), (19, 42, .45), (21, 38, .18)),
        p((25, 38, .2), (20, 35, .7), (15, 36, .42), (17, 32, .18)),
        p((42, 38, .2), (47, 35, .76), (53, 36, .42), (51, 32, .18)),
        p((47, 33, .2), (52, 29, .72), (58, 30, .44), (56, 26, .18)),
        p((36, 31, .2), (32, 27, .75), (28, 28, .42), (30, 23, .18)),
        p((39, 27, .2), (42, 23, .7), (48, 24, .38), (46, 20, .16)),
    ]
    marks = [
        svg_path(stroke_path(stem, width=2.2, seed="sage-stem", wobble=.18), fill="#262522"),
        svg_path(stroke_path(branch_l, width=1.15, seed="sage-left", wobble=.19), fill="#373631"),
        svg_path(stroke_path(branch_r, width=1.1, seed="sage-right", wobble=.17), fill="#373631"),
        svg_path(stroke_path(branch_top, width=.9, seed="sage-top", wobble=.2), fill="#373631"),
    ]
    for index, leaf in enumerate(leaves):
        marks.append(svg_path(stroke_path(leaf, width=2.3, seed=f"sage-leaf-{index}", wobble=.2), fill="#4f4e47"))
        marks.extend(svg_path(d, fill="#88857a", class_name="ink-dry") for d in dry_brush_paths(leaf, width=.34, seed=f"sage-leaf-dry-{index}", breaks=1))
    marks.extend(svg_path(d, fill="#77746a", class_name="ink-dry") for d in dry_brush_paths(stem, width=.35, seed="sage-stem-dry", breaks=3))
    marks.append('<path class="ink-stroke" d="M 36 60 Q 42 57 48 59" fill="none" stroke="#88857a" stroke-width=".45" stroke-linecap="round" pathLength="1"/>')
    svg = (f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="herbs / sage" {cp.group(0)} data-castalia-style="sumi-e-brush-art-v1" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>herbs / sage — botanical sumi-e brush study</title>{''.join(marks)}</svg>
''')
    TARGET.write_text(svg)
    print(TARGET)


if __name__ == "__main__":
    main()
