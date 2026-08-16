#!/usr/bin/env python3
"""Author three science outliers as expressive vector brush studies."""
from __future__ import annotations

import math
import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def pts(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*v) for v in values]


def loop(cx: float, cy: float, rx: float, ry: float, count: int = 14) -> list[BrushPoint]:
    return [BrushPoint(cx + math.cos(i * 2 * math.pi / count) * rx, cy + math.sin(i * 2 * math.pi / count) * ry, .55 + .5 * (i % 3) / 2) for i in range(count + 1)]


def root_for(name: str) -> tuple[Path, str]:
    target = ROOT / "assets/pua/science" / f"{name}.svg"
    original = target.read_text()
    match = re.search(r'data-pua="([^"]+)"', original)
    if not match:
        raise SystemExit(f"missing PUA codepoint in {target}")
    return target, match.group(0)


def write(name: str, marks: list[str], title: str, transform: str = "") -> None:
    target, cp = root_for(name)
    ground = '<path class="ink-dry" fill="#77746a" d="M 8 63 C 21 60 37 63 51 61 C 58 60 63 61 66 59"/>'
    opening = f'<g transform="{transform}">' if transform else ""
    closing = "</g>" if transform else ""
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {cp} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>science / {name} — authored sumi-e brush study</title>{opening}{''.join(marks)}{closing}{ground}</svg>
''')


search_lens = pts(
    (30, 15, .25), (22, 15, .72), (16, 19, 1.0), (13, 26, .88),
    (14, 34, .62), (19, 40, .35), (27, 43, .2), (35, 42, .42),
    (41, 37, .8), (44, 30, 1.0), (43, 23, .72), (38, 17, .4),
    (30, 15, .25),
)
search = [
    svg_path(stroke_path(search_lens, width=2.35, seed="search-glass", wobble=.28), fill="#262522"),
    svg_path(stroke_path(pts((41, 40, .22), (44, 44, .52), (48, 48, .82), (53, 53, 1.0), (59, 58, .3)), width=3.65, seed="search-handle", wobble=.24), fill="#3d3c37"),
]
search.extend(svg_path(d, fill="#77746a", class_name="ink-dry") for d in dry_brush_paths(search_lens, width=.6, seed="search-dry", breaks=4))
write("search", search, "search")

eye_upper = pts((9, 36, .22), (17, 30, .62), (26, 26, .92), (35, 25, 1.0), (44, 27, .76), (53, 31, .52), (63, 37, .2))
eye_lower = pts((9, 36, .2), (18, 41, .5), (27, 45, .82), (37, 46, .94), (47, 43, .66), (56, 39, .4), (63, 36, .2))
iris = pts((34, 27, .2), (29, 30, .52), (28, 36, .9), (31, 42, .78), (37, 45, .42), (42, 41, .22), (44, 35, .62), (41, 29, .92), (34, 27, .2))
pupil = pts((36, 31, .2), (33, 34, .68), (34, 39, 1.0), (38, 41, .48), (40, 37, .22), (39, 33, .8), (36, 31, .2))
observe = [
    svg_path(stroke_path(eye_upper, width=2.2, seed="eye-upper", wobble=.24), fill="#262522"),
    svg_path(stroke_path(eye_lower, width=1.5, seed="eye-lower", wobble=.28), fill="#3c3b36"),
    svg_path(stroke_path(iris, width=1.2, seed="eye-iris", wobble=.22), fill="#4a4943"),
    svg_path(stroke_path(pupil, width=.9, seed="eye-pupil", wobble=.18), fill="#262522"),
]
observe.extend(svg_path(d, fill="#77746a", class_name="ink-dry") for d in dry_brush_paths(eye_upper, width=.46, seed="eye-dry", breaks=3))
# The broad eye contour was touching the left raster edge at 128px.  Keep the
# drawing's proportions but give the brush mass a small, deliberate margin.
write("observe", observe, "observe", "translate(1 0) scale(.972 1)")

sensor = [
    svg_path(stroke_path(pts((36, 56, .22), (35, 49, .7), (36, 42, 1.0), (35, 36, .72), (36, 33, .18)), width=2.35, seed="sensor-probe", wobble=.24), fill="#262522"),
    svg_path(stroke_path(pts((29, 34, .2), (25, 32, .62), (22, 28, .95), (22, 24, .5), (25, 20, .2)), width=1.5, seed="sensor-left", wobble=.27), fill="#3c3b36"),
    svg_path(stroke_path(pts((43, 34, .2), (47, 32, .62), (50, 28, .95), (50, 24, .5), (47, 20, .2)), width=1.5, seed="sensor-right", wobble=.27), fill="#3c3b36"),
    svg_path(stroke_path(pts((30, 31, .2), (30, 27, .62), (33, 24, .95), (37, 23, 1.0), (41, 25, .76), (43, 29, .4), (42, 33, .2), (38, 36, .45), (34, 36, .82), (30, 31, .2)), width=1.65, seed="sensor-head", wobble=.3), fill="#4a4943"),
    svg_path(stroke_path(pts((35, 22, .18), (36, 18, .72), (38, 15, .2)), width=1.3, seed="sensor-antenna", wobble=.25), fill="#262522"),
    svg_path(stroke_path(pts((27, 59, .2), (34, 58, .72), (41, 59, 1.0), (48, 58, .22)), width=1.35, seed="sensor-base", wobble=.25), fill="#262522"),
]
sensor.extend(svg_path(d, fill="#77746a", class_name="ink-dry") for d in dry_brush_paths(pts((24, 28, .2), (22, 24, .95), (24, 20, .5), (28, 18, .2)), width=.46, seed="sensor-dry", breaks=2))
write("sensor", sensor, "sensor")
print("redrew search, observe, and sensor as authored brush studies")
