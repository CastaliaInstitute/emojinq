"""Deterministic vector sumi-e brush geometry.

The output is a closed SVG path made from the two sides of a pressure-shaped
brush ribbon.  It deliberately avoids SVG filters and constant-width strokes,
so it survives font conversion, animation, and grayscale laser-depth export.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class BrushPoint:
    x: float
    y: float
    pressure: float = 1.0


def _seeded(seed: str, index: int) -> float:
    digest = hashlib.sha256(f"{seed}:{index}".encode()).digest()
    return (int.from_bytes(digest[:4], "big") / 0xFFFFFFFF) * 2.0 - 1.0


def _dedupe(points: Sequence[BrushPoint]) -> list[BrushPoint]:
    out: list[BrushPoint] = []
    for point in points:
        if not out or math.hypot(point.x - out[-1].x, point.y - out[-1].y) > 0.001:
            out.append(point)
    return out


def stroke_path(
    points: Iterable[BrushPoint],
    *,
    width: float = 2.0,
    seed: str = "stroke",
    wobble: float = 0.12,
    taper_start: float = 0.18,
    taper_end: float = 0.12,
) -> str:
    """Return a tapered, slightly irregular filled brush ribbon as SVG `d`.

    `pressure` is relative width.  Width changes are applied to the ribbon
    itself, which is more portable than SVG variable-width stroke proposals.
    The small deterministic normal wobble prevents sterile CAD-perfect edges
    without turning the mark into noisy cartoon squiggle.
    """
    clean = _dedupe(list(points))
    if len(clean) < 2:
        raise ValueError("a brush stroke needs at least two distinct points")

    left: list[tuple[float, float]] = []
    right: list[tuple[float, float]] = []
    count = len(clean)
    for index, point in enumerate(clean):
        prev = clean[max(0, index - 1)]
        nxt = clean[min(count - 1, index + 1)]
        dx = nxt.x - prev.x
        dy = nxt.y - prev.y
        length = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / length, dx / length
        t = index / (count - 1)
        start_factor = taper_start + (1.0 - taper_start) * min(1.0, t * 4.0)
        end_factor = taper_end + (1.0 - taper_end) * min(1.0, (1.0 - t) * 4.0)
        factor = min(start_factor, end_factor)
        local_width = max(0.12, width * point.pressure * factor)
        edge_wobble = wobble * width * _seeded(seed, index)
        half = local_width / 2.0 + edge_wobble
        left.append((point.x + nx * half, point.y + ny * half))
        right.append((point.x - nx * half, point.y - ny * half))

    outline = left + list(reversed(right))
    # Quadratic midpoint interpolation keeps the pressure-shaped silhouette
    # organic.  Straight polygon joins are especially conspicuous at glyph
    # scale and read as cut vinyl rather than a loaded brush.
    midpoints = [
        ((outline[i][0] + outline[(i + 1) % len(outline)][0]) / 2.0,
         (outline[i][1] + outline[(i + 1) % len(outline)][1]) / 2.0)
        for i in range(len(outline))
    ]
    commands = [f"M {midpoints[-1][0]:.3f},{midpoints[-1][1]:.3f}"]
    for index, point in enumerate(outline):
        x, y = midpoints[index]
        commands.append(f"Q {point[0]:.3f},{point[1]:.3f} {x:.3f},{y:.3f}")
    commands.append("Z")
    return " ".join(commands)


def dry_brush_paths(
    points: Iterable[BrushPoint],
    *,
    width: float = 1.2,
    seed: str = "dry",
    breaks: int = 2,
) -> list[str]:
    """Return sparse broken companion marks for a dry-brush edge."""
    source = list(points)
    if len(source) < 4 or breaks < 1:
        return []
    paths: list[str] = []
    span = max(2, (len(source) - 2) // (breaks + 1))
    for index in range(breaks):
        start = 1 + index * span
        end = min(len(source) - 1, start + max(2, span // 2))
        fragment = source[start:end]
        if len(fragment) >= 2:
            paths.append(stroke_path(fragment, width=width, seed=f"{seed}-{index}", wobble=0.2, taper_start=0.05, taper_end=0.35))
    return paths


def svg_path(d: str, *, fill: str = "#262522", class_name: str = "ink-wash") -> str:
    """Wrap generated geometry in the project animation contract."""
    return f'<path class="{class_name}" d="{d}" fill="{fill}"/>'
