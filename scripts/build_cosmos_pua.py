#!/usr/bin/env python3
"""Generate the cosmos PUA glyph set (F1440+) as tapered-ink SVGs.

These are PICTORIAL astronomy glyphs, not astrological sigils: a three
year old should read each one as a picture of the thing. Planets are
brushed disks with recognisable surface markings, Saturn's ring visibly
passes behind its disk, and the spacecraft are drawn as machines.

Each glyph is described as a set of brush strokes: a centerline polyline
with a width profile. Strokes are smoothed with Catmull-Rom, jittered
slightly for a hand feel, and emitted as filled tapered outlines — the
same visual system (sumi-e-ink-wash-v1 / tapered-v1) as the rest of the
PUA library. Deterministic per code point, so rebuilds are reproducible.

Usage: python3 scripts/build_cosmos_pua.py            # writes assets/pua/cosmos/
       python3 scripts/build_cosmos_pua.py --manifest # also updates assets/pua/manifest.json
"""

from __future__ import annotations

import argparse
import json
import math
import random
import zlib
from pathlib import Path

INK = "#262522"
CANVAS = 72
STYLE = "sumi-e-naturalist-v2"
STROKE_SYSTEM = "filled-brush-mass-v2"
BLOCK_START = 0xF1440

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "pua" / "cosmos"
MANIFEST = ROOT / "assets" / "pua" / "manifest.json"


# ── geometry ──────────────────────────────────────────────────────────

def catmull_rom(pts, samples_per_seg=14, closed=False):
    if closed:
        ext = [pts[-1]] + list(pts) + [pts[0], pts[1]]
    else:
        ext = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for s in range(samples_per_seg):
            t = s / samples_per_seg
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(tuple(pts[-1]))
    return out


def interp_widths(widths, n):
    if len(widths) == 1:
        return [widths[0]] * n
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(widths) - 1)
        k = min(int(t), len(widths) - 2)
        f = t - k
        out.append(widths[k] * (1 - f) + widths[k + 1] * f)
    return out


def stroke_outline(pts, widths, rng, closed=False, jitter=0.35, wobble=0.12):
    """Centerline + widths → filled outline polygon(s)."""
    center = catmull_rom(pts, closed=closed)
    n = len(center)
    ws = interp_widths(widths, n)
    left, right = [], []
    phase = rng.uniform(0.0, 2.0 * math.pi)
    secondary_phase = rng.uniform(0.0, 2.0 * math.pi)
    for i in range(n):
        a = center[max(0, i - 1)] if not closed else center[(i - 1) % n]
        b = center[min(n - 1, i + 1)] if not closed else center[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        progress = i / max(1, n - 1)
        # A calligraphic hand does not hold a perfectly constant pressure.
        pressure = (
            1.0
            + 0.10 * math.sin(progress * 2.0 * math.pi + phase)
            + 0.035 * math.sin(progress * 7.0 * math.pi + secondary_phase)
        )
        w = ws[i] * pressure * (1 + rng.uniform(-wobble, wobble))
        jx = nx * rng.uniform(-jitter, jitter)
        jy = ny * rng.uniform(-jitter, jitter)
        cx, cy = center[i][0] + jx, center[i][1] + jy
        left.append((cx + nx * w / 2, cy + ny * w / 2))
        right.append((cx - nx * w / 2, cy - ny * w / 2))
    if closed:
        return [left, list(reversed(right))]
    return [left + list(reversed(right))]


def dot(cx, cy, r, rng, segs=10):
    pts = []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        rr = r * (1 + rng.uniform(-0.12, 0.12))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return [pts]


def poly_to_d(poly):
    d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in poly) + " Z"
    return d


def signed_area(pts):
    total = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        total += x0 * y1 - x1 * y0
    return total / 2.0


# ── construction helpers ──────────────────────────────────────────────
# The cosmos set is mostly disks, rings and arcs, so the point lists are
# generated rather than typed by hand. Every helper below is pure and
# deterministic: it returns plain point lists for the S()/L()/Pat() items.

def circ(cx, cy, r, n=14, phase=0.0):
    """Points around a circle, travelling clockwise in screen space."""
    return [
        (cx + r * math.cos(2 * math.pi * i / n + phase),
         cy + r * math.sin(2 * math.pi * i / n + phase))
        for i in range(n)
    ]


def oval(cx, cy, rx, ry, rot=0.0, n=14):
    """Points around a rotated ellipse, travelling clockwise."""
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def earc(cx, cy, rx, ry, a0, a1, n=11, rot=0.0):
    """Sampled elliptical arc from a0 to a1 degrees (0 = right, 90 = down)."""
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = []
    for i in range(n):
        t = math.radians(a0 + (a1 - a0) * i / (n - 1))
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def occlusion_angle(rx, ry, radius):
    """|cos t| where a rx/ry ellipse crosses a circle of the given radius.

    Rotating the ellipse about the shared centre does not change |P|, so
    this boundary holds for tilted rings too. Returns None when the whole
    ellipse clears the disk.
    """
    denom = rx * rx - ry * ry
    if abs(denom) < 1e-9:
        return None
    value = (radius * radius - ry * ry) / denom
    if not 0.0 < value < 1.0:
        return None
    return math.sqrt(value)


def spiral(cx, cy, r0, growth, t0, t1, n=7, phase=0.0):
    pts = []
    for i in range(n):
        t = t0 + (t1 - t0) * i / (n - 1)
        r = r0 * math.exp(growth * t)
        pts.append((cx + r * math.cos(t + phase), cy + r * math.sin(t + phase)))
    return pts


def lump(cx, cy, r, seed=0.0, n=9):
    """An irregular rock outline — deterministic, no RNG needed."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (0.76 + 0.32 * abs(math.sin(a * 1.7 + seed)))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


# ── stroke shorthand ──────────────────────────────────────────────────
# S(points, widths)            open tapered stroke
# L(points, width_or_widths)   closed loop stroke (outline ring)
# D(cx, cy, r)                 dot — reads as a highlight hole over ink
# Pat(points)                  solid ink patch (continent, spot, rock)

def S(pts, widths):
    return ("stroke", pts, widths)


def L(pts, widths):
    return ("loop", pts, widths if isinstance(widths, list) else [widths])


def D(cx, cy, r):
    return ("dot", cx, cy, r)


def Pat(pts):
    return ("patch", pts)


def Blob(cx, cy, r, n=9):
    """A solid ink blob that always fills, even where it crosses a stroke."""
    return Pat(lump(cx, cy, r, seed=0.6, n=n))


# ── item builders (splice with * into a glyph's stroke list) ──────────

def rays(cx, cy, r0, spec, w0=2.6, w1=0.35, bend=0.0):
    """Tapering rays leaving a body: spec is a list of (angle_deg, length)."""
    out = []
    for angle, length in spec:
        t = math.radians(angle)
        c, s = math.cos(t), math.sin(t)
        px, py = -s, c
        mid = r0 + length * 0.52
        out.append(S([
            (cx + c * r0, cy + s * r0),
            (cx + c * mid + px * bend, cy + s * mid + py * bend),
            (cx + c * (r0 + length), cy + s * (r0 + length)),
        ], [w0, w0 * 0.5, w1]))
    return out


def tilted_ring(cx, cy, rx, ry, disk_r, rot=0.0, w_front=2.8, w_back=1.9,
                gap=1.0, front_overhang=6.0):
    """A ring seen edge-on: front arc drawn whole, back arc broken by the disk.

    The near half sweeps unbroken across the planet; the far half is cut
    where the disk occludes it, which is the whole reason Saturn reads as
    Saturn instead of as a disk with a line through it.
    """
    cosine = occlusion_angle(rx, ry, disk_r + gap)
    front = [S(earc(cx, cy, rx, ry, -front_overhang, 180 + front_overhang, 19, rot=rot),
               [w_front * 0.7, w_front, w_front * 1.1, w_front, w_front * 0.7])]
    if cosine is None:
        return front + [S(earc(cx, cy, rx, ry, 180, 360, 19, rot=rot),
                          [w_back * 0.7, w_back, w_back * 0.7])]
    cut = math.degrees(math.acos(max(-1.0, min(1.0, cosine))))
    left_end = 360 - cut          # e.g. 227° for a classic Saturn tilt
    right_end = 180 + cut         # e.g. 313°
    back = [
        S(earc(cx, cy, rx, ry, 180, left_end - 2, 11, rot=rot),
          [w_back, w_back * 0.75, 0.5]),
        S(earc(cx, cy, rx, ry, 360, right_end + 2, 11, rot=rot),
          [w_back, w_back * 0.75, 0.5]),
    ]
    return front + back


def upright_ring(cx, cy, rx, ry, disk_r, rot=0.0, w=2.0, gap=1.0, overhang=7.0):
    """A ring tipped on its side — the Uranus case: near arc below, far arc above."""
    cosine = occlusion_angle(rx, ry, disk_r + gap)
    if cosine is None:
        cut = 45.0
    else:
        cut = math.degrees(math.acos(max(-1.0, min(1.0, cosine))))
    near0, near1 = cut - overhang, 180 - cut + overhang
    far0, far1 = 180 + cut + 3, 360 - cut - 3
    return [
        S(earc(cx, cy, rx, ry, near0, near1, 15, rot=rot),
          [0.6, w * 0.9, w, w * 0.9, 0.6]),
        S(earc(cx, cy, rx, ry, far0, far1, 15, rot=rot),
          [0.55, w * 0.85, w * 0.9, w * 0.85, 0.55]),
    ]


def panel(x0, y0, x1, y1, w=1.8, cols=2, rows=0):
    """A solar array: a rounded rectangle plus its cell grid."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    items = [L([(x0, y0), (mx, y0), (x1, y0), (x1, my),
                (x1, y1), (mx, y1), (x0, y1), (x0, my)], w)]
    for i in range(1, cols):
        x = x0 + (x1 - x0) * i / cols
        items.append(S([(x, y0 + 0.9), (x, y1 - 0.9)], [w * 0.5, w * 0.5]))
    for j in range(1, rows):
        y = y0 + (y1 - y0) * j / rows
        items.append(S([(x0 + 0.9, y), (x1 - 0.9, y)], [w * 0.45, w * 0.45]))
    return items


def sparkle(cx, cy, r, w=1.5):
    """A tiny four-ray star for use inside larger scenes."""
    return [
        S([(cx, cy), (cx, cy - r * 0.6), (cx, cy - r)], [w, w * 0.5, 0.25]),
        S([(cx, cy), (cx, cy + r * 0.6), (cx, cy + r)], [w, w * 0.5, 0.25]),
        S([(cx, cy), (cx - r * 0.6, cy), (cx - r, cy)], [w, w * 0.5, 0.25]),
        S([(cx, cy), (cx + r * 0.6, cy), (cx + r, cy)], [w, w * 0.5, 0.25]),
    ]


def belt(cx, cy, rx, ry, spec):
    """Rocks scattered along an elliptical arc — the asteroid belt."""
    out = []
    for index, (angle, radius, offset) in enumerate(spec):
        t = math.radians(angle)
        px = cx + (rx + offset) * math.cos(t)
        py = cy + (ry + offset) * math.sin(t)
        out.append(Pat(lump(px, py, radius, seed=index * 0.9, n=8)))
    return out


def haze(cx, cy, r, spans, w=1.2):
    """A broken outer ring — reads as atmosphere rather than a hard limb."""
    return [
        S(earc(cx, cy, r, r, a0, a1, 9), [0.35, w, w * 0.9, 0.35])
        for a0, a1 in spans
    ]


def wash_outline(pts, spans, widths):
    """A closed contour drawn as broken open strokes — soft wash, not a rim.

    A nebula has no edge. Breaking the contour is what keeps it from
    reading as one more lump of rock.
    """
    curve = catmull_rom(pts, closed=True)
    n = len(curve)
    out = []
    for a, b in spans:
        i0, i1 = int(n * a), int(n * b)
        seg = curve[i0:i1] if i1 > i0 else curve[i0:] + curve[:i1]
        step = max(1, len(seg) // 9)
        seg = seg[::step]
        if len(seg) < 3:
            continue
        out.append(S(seg, widths))
    return out


SUN_RAYS = [(6, 11.5), (27, 8.0), (48, 12.5), (66, 7.5), (88, 11.0), (107, 9.0),
            (126, 12.0), (147, 8.0), (166, 11.5), (185, 9.5), (204, 12.0),
            (223, 7.5), (243, 11.0), (262, 9.0), (281, 12.5), (300, 8.0),
            (320, 11.0), (341, 9.5)]

ECLIPSE_RAYS = [(4, 7.0), (26, 10.5), (47, 12.0), (63, 8.5), (82, 11.5),
                (101, 12.0), (122, 8.0), (141, 10.0), (163, 6.5), (182, 8.5),
                (201, 6.0), (222, 9.0), (241, 6.5), (262, 8.0), (283, 6.0),
                (302, 9.5), (322, 6.5), (343, 9.0)]

BELT_SPEC = [(178, 3.4, 0.0), (191, 2.0, -3.5), (200, 4.6, 1.5), (211, 2.4, -2.5),
             (221, 3.2, 2.5), (232, 5.0, -1.0), (244, 2.2, 3.0), (255, 3.8, -2.0),
             (266, 1.9, 2.0), (276, 4.4, -1.5), (288, 2.6, 2.8), (299, 3.6, -2.5),
             (310, 2.1, 1.5), (321, 4.8, -1.0), (333, 2.4, 2.5), (345, 3.0, -3.0),
             (357, 3.6, 0.5)]

CONSTELLATION_STARS = [(13, 20, 3.4), (28, 31, 2.2), (25, 50, 2.9),
                       (44, 19, 1.9), (50, 38, 3.0), (61, 55, 2.4)]
CONSTELLATION_LINKS = [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (2, 4)]


def constellation_links():
    out = []
    for a, b in CONSTELLATION_LINKS:
        x0, y0, _ = CONSTELLATION_STARS[a]
        x1, y1, _ = CONSTELLATION_STARS[b]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        nx, ny = -(y1 - y0), (x1 - x0)
        ln = math.hypot(nx, ny) or 1.0
        bow = 0.9
        out.append(S([(x0, y0), (mx + nx / ln * bow, my + ny / ln * bow), (x1, y1)],
                     [0.5, 0.85, 0.5]))
    return out


GLYPHS = {
    # ── the sun ───────────────────────────────────────────────────────
    "sun": [
        L(circ(36, 36, 18.5, 18), 3.3),
        *rays(36, 36, 20.0, SUN_RAYS, w0=2.8, w1=0.35, bend=0.6),
        S(earc(36, 36, 12, 12, 200, 300, 9), [0.4, 1.2, 0.4]),
        S(earc(36, 36, 13, 13, 40, 130, 9), [0.4, 1.1, 0.4]),
        S([(25, 40), (31, 42.5), (37, 41)], [0.5, 1.1, 0.4]),
    ],
    # ── the planets ───────────────────────────────────────────────────
    "mercury": [
        L(circ(36, 36, 20.0, 18), 3.0),
        L(circ(43, 28, 5.6, 12), 1.6),
        L(circ(43, 28, 2.5, 9), 1.1),
        L(circ(28, 44, 3.8, 10), 1.4),
        L(circ(31, 30, 2.7, 9), 1.2),
        L(circ(40, 47, 3.0, 9), 1.2),
        Blob(35, 37, 1.2), Blob(24, 35, 1.0), Blob(46, 40, 1.0),
        Blob(31, 51, 0.9), Blob(49, 32, 0.85),
        S(earc(36, 36, 15.5, 15.5, 118, 242, 11), [0.35, 1.6, 0.35]),
    ],
    "venus": [
        L(circ(36, 36, 21.5, 18), 3.1),
        S([(18.5, 30), (27, 26.5), (38, 28.5), (48, 25.8), (53, 28)],
          [1.0, 2.6, 2.0, 2.4, 0.6]),
        S([(17.5, 37), (26, 34.5), (38, 37), (50, 34), (54, 36.5)],
          [0.9, 2.9, 2.3, 2.6, 0.6]),
        S([(19, 44), (29, 41.5), (40, 44), (50, 41)], [0.9, 2.5, 2.0, 0.6]),
        S([(23, 50), (33, 48), (44, 50)], [0.8, 2.0, 0.5]),
        S([(24, 24), (33, 22.5), (43, 24)], [0.7, 1.6, 0.5]),
        S([(46, 26.5), (50, 24.5), (50.5, 27.5), (47.5, 28.5)],
          [1.4, 1.0, 0.8, 0.3]),
        S([(26, 47), (22, 45), (21.5, 48.5), (25, 50)], [1.2, 0.9, 0.7, 0.3]),
    ],
    "earth": [
        L(circ(36, 36, 21.5, 18), 3.1),
        Pat([(27, 22), (31, 26), (28.5, 31), (31, 35), (28, 43), (24.5, 46),
             (22.5, 40), (25, 32), (22, 26)]),
        Pat([(38, 25), (47, 24), (52, 30), (46, 34), (48, 41), (42, 49),
             (37.5, 44), (41.5, 36), (36, 30)]),
        Pat([(29, 50), (35.5, 49), (37, 53.5), (31, 55.5), (27.5, 53)]),
        S([(17.5, 38), (27, 40), (36, 40.5), (45, 40), (54.5, 38)],
          [0.5, 0.9, 1.0, 0.9, 0.45]),
        Blob(52, 45, 1.1), Blob(20, 46, 0.95), Blob(33, 21, 0.9),
    ],
    "mars": [
        L(circ(36, 36, 21.0, 18), 3.0),
        S(earc(36, 36, 17, 17, 205, 335, 13), [0.5, 2.6, 4.2, 2.6, 0.5]),
        S(earc(36, 36, 12.5, 12.5, 212, 328, 11), [0.35, 1.1, 0.35]),
        Pat([(24, 40), (31, 38), (36, 41), (33, 46), (26, 46), (22, 44)]),
        Pat([(41, 44), (48, 42), (50, 47), (45, 51), (40, 49)]),
        Pat([(40, 32), (46, 31), (48, 35), (43, 37)]),
        Blob(30, 52, 1.4), Blob(52, 38, 1.2), Blob(22, 33, 1.0),
    ],
    "jupiter": [
        L(circ(36, 36, 26.5, 20), 2.5),
        S([(22, 17), (31, 16), (40, 17), (50, 16.5)], [0.45, 1.1, 1.25, 0.4]),
        S([(17, 23.5), (26, 22), (36, 23.5), (46, 22), (55, 23.5)],
          [0.6, 2.2, 2.8, 2.0, 0.5]),
        S([(14.5, 29), (25, 30.5), (36, 29), (47, 30.5), (57.5, 29)],
          [0.5, 1.35, 1.6, 1.2, 0.45]),
        S([(13.5, 36.5), (24, 35), (36, 36.5), (48, 35), (58.5, 36.5)],
          [0.6, 2.8, 3.4, 2.6, 0.5]),
        S([(14.5, 43.5), (24, 45), (34, 43.5), (39, 44.5)], [0.5, 1.6, 1.8, 0.4]),
        S([(56, 44.5), (58.2, 43.5)], [1.1, 0.4]),
        Pat(oval(47.5, 45, 7.0, 5.0, rot=-12, n=14)),
        S([(17.5, 50), (27, 51.5), (37, 50), (47, 51.5), (54.5, 50)],
          [0.5, 1.7, 2.0, 1.5, 0.45]),
        S([(23, 56), (32, 57), (41, 56), (49, 55)], [0.45, 1.1, 1.2, 0.4]),
    ],
    "saturn": [
        L(circ(35, 36, 20.5, 18), 3.1),
        S([(20, 30.5), (28, 29), (35, 30.5), (43, 29), (49, 30.5)],
          [0.7, 1.8, 2.0, 1.5, 0.5]),
        S([(21, 43), (29, 44.5), (36, 43), (44, 44.5), (49, 43)],
          [0.6, 1.6, 1.8, 1.4, 0.5]),
        S([(24, 24), (31, 23), (39, 24)], [0.5, 1.2, 0.4]),
        # One bold ring, not two competing ellipses: the break where the
        # planet occludes the far side is the whole point of the glyph.
        *tilted_ring(35, 36, 30.5, 11.0, 20.5, rot=-14, w_front=3.6, w_back=2.7),
    ],
    "uranus": [
        L(circ(36, 36, 21.5, 18), 3.0),
        S([(20, 28.5), (30, 27.5), (42, 28.5), (51, 27.5)], [0.5, 1.1, 1.0, 0.4]),
        S([(16.8, 36), (26, 35), (38, 36.5), (50, 35), (55, 36)],
          [0.5, 1.0, 1.3, 0.9, 0.4]),
        S([(21, 44), (31, 45), (43, 44), (51, 45)], [0.5, 1.0, 1.0, 0.4]),
        S([(26, 51), (36, 52), (46, 50.5)], [0.4, 0.9, 0.35]),
        *upright_ring(36, 36, 7.5, 29.0, 21.5, rot=10, w=2.2),
    ],
    "neptune": [
        L(circ(36, 36, 22.5, 20), 3.1),
        S([(22, 24), (32, 22.5), (43, 24.5)], [0.5, 1.4, 0.4]),
        S([(17, 30), (27, 28), (39, 30), (50, 28), (55, 29.5)],
          [0.6, 2.0, 1.8, 1.6, 0.5]),
        S([(15.5, 37), (26, 35.5), (38, 37.5), (50, 35.5), (56.5, 37)],
          [0.6, 2.4, 2.6, 2.0, 0.5]),
        S([(18, 44.5), (28, 43), (40, 45), (51, 43)], [0.5, 1.8, 1.8, 0.5]),
        S([(23, 51), (33, 50), (44, 52)], [0.5, 1.4, 0.4]),
        Pat(oval(27, 45.5, 7.0, 4.8, rot=-8, n=14)),
        S([(43, 30), (48, 32.5)], [0.9, 0.35]),
    ],
    "pluto": [
        L(circ(36, 36, 20.0, 18), 2.9),
        L([(36, 52), (30, 47), (26, 42), (25, 37), (27, 33.5), (31, 33),
           (34, 35.5), (36, 39), (38, 35.5), (41, 33), (45, 33.5), (47, 37),
           (46, 42), (42, 47)], 1.9),
        S([(21, 29), (30, 27.5), (40, 29)], [0.5, 1.1, 0.4]),
        Blob(28, 26, 1.3), Blob(45, 26, 1.1), Blob(50, 45, 1.0), Blob(22, 45, 1.0),
    ],
    # ── moons and small bodies ────────────────────────────────────────
    "moon": [
        L(circ(36, 36, 20.0, 18), 2.9),
        S(earc(36, 36, 15.5, 15.5, -62, 62, 13), [0.5, 2.6, 4.8, 2.6, 0.5]),
        L(circ(28, 30, 4.5, 11), 1.5),
        L(circ(31, 45, 3.3, 10), 1.3),
        L(circ(23, 39, 2.6, 9), 1.2),
        L(circ(37, 25, 2.4, 9), 1.1),
        L(circ(34, 50, 2.2, 9), 1.0),
        Blob(42, 31, 1.1), Blob(24, 47, 0.9),
    ],
    "comet": [
        Pat([(52, 13.5), (57, 15), (58.5, 20), (56, 25), (51, 26.5), (47, 23),
             (46, 17.5), (48.5, 14.5)]),
        L(circ(52, 20, 10.5, 14), 1.4),
        S([(46, 25), (38, 32), (28, 42), (19, 53), (12, 62)],
          [8.5, 7.0, 5.0, 2.8, 0.4]),
        S([(48, 27.5), (43, 37), (37, 49), (31, 58), (27, 64)],
          [5.5, 4.0, 2.6, 1.4, 0.35]),
        S([(37, 35), (30, 43)], [0.8, 0.25]),
        S([(31, 47), (24, 55)], [0.7, 0.25]),
        Blob(22, 50, 0.9), Blob(17, 58, 0.8),
    ],
    "asteroid": [
        L([(36, 17), (45, 19), (52, 25), (55, 33), (53, 42), (47, 50), (39, 55),
           (30, 55), (22, 50), (17, 42), (16, 33), (20, 24), (27, 19)], 3.1),
        L(circ(30, 30, 4.8, 11), 1.6),
        L(circ(43, 42, 3.7, 10), 1.4),
        L(circ(36, 48, 2.8, 9), 1.2),
        Blob(46, 29, 1.3), Blob(24, 42, 1.1),
        S([(21, 44), (26, 48)], [1.2, 0.5]),
        S([(48, 37), (50, 43)], [1.0, 0.4]),
        S([(31, 21), (37, 24)], [0.9, 0.35]),
    ],
    "star": [
        S([(36, 36), (36.5, 22), (35.5, 8)], [6.2, 2.4, 0.35]),
        S([(36, 36), (35.5, 50), (36.5, 63)], [6.2, 2.2, 0.35]),
        S([(36, 36), (22, 35.5), (9, 36.5)], [6.2, 2.2, 0.35]),
        S([(36, 36), (50, 36.5), (64, 35.5)], [6.2, 2.4, 0.35]),
        S([(36, 36), (43, 29), (48.5, 23.5)], [3.4, 1.2, 0.3]),
        S([(36, 36), (29, 43), (23.5, 48.5)], [3.4, 1.2, 0.3]),
        S([(36, 36), (29, 29), (24.5, 24.5)], [3.1, 1.1, 0.3]),
        S([(36, 36), (43, 43), (47.5, 47.5)], [3.1, 1.1, 0.3]),
    ],
    "galaxy": [
        Pat(oval(36, 36, 6.2, 4.3, rot=-22, n=14)),
        S(spiral(36, 36, 7.0, 0.46, 0.2, 2.85, 8, phase=0.0),
          [5.0, 4.1, 3.3, 2.4, 1.6, 1.0, 0.5, 0.28]),
        S(spiral(36, 36, 7.0, 0.46, 0.2, 2.85, 8, phase=math.pi),
          [5.0, 4.1, 3.3, 2.4, 1.6, 1.0, 0.5, 0.28]),
        S(spiral(36, 36, 6.5, 0.40, 0.9, 2.1, 5, phase=1.05),
          [2.0, 1.4, 0.9, 0.5, 0.25]),
        S(spiral(36, 36, 6.5, 0.40, 0.9, 2.1, 5, phase=1.05 + math.pi),
          [2.0, 1.4, 0.9, 0.5, 0.25]),
        D(19, 21, 1.2), D(57, 51, 1.0), D(52, 60, 0.85), D(16, 50, 0.8),
    ],
    "io": [
        L(circ(36, 36, 19.5, 18), 2.8),
        Pat([(26, 30), (32, 29), (34, 34), (29, 37), (24, 35)]),
        Pat([(41, 40), (48, 39), (49, 45), (43, 47), (39, 44)]),
        Pat([(31, 46), (37, 45), (38, 50), (32, 51)]),
        Pat([(42, 26), (47, 28), (45, 32), (40, 31)]),
        Blob(23, 43, 1.2), Blob(35, 38.5, 1.0), Blob(51, 34, 1.0),
        S([(24, 20), (20, 14), (18.5, 9)], [1.5, 0.9, 0.3]),
        S([(24.5, 20), (27.5, 13.5), (29.5, 9)], [1.5, 0.9, 0.3]),
        S([(18.5, 10.5), (24, 7.5), (29.5, 10.5)], [0.7, 1.3, 0.6]),
        Blob(24, 5.5, 0.8),
    ],
    "europa": [
        L(circ(36, 36, 19.5, 18), 2.8),
        S([(19.5, 29.5), (30, 33), (42, 34), (52.5, 31.5)], [0.5, 1.1, 1.0, 0.4]),
        S([(21, 46), (32, 42), (44, 41), (52.5, 43.5)], [0.5, 1.1, 1.0, 0.4]),
        S([(26.5, 21.5), (31, 32), (34, 45), (33, 53)], [0.4, 0.95, 0.95, 0.35]),
        S([(46, 21.5), (42, 32), (40, 44), (42, 52)], [0.4, 0.95, 0.95, 0.35]),
        S([(21, 38), (33, 37), (45, 38), (54, 37)], [0.4, 0.85, 0.85, 0.35]),
        S([(30, 53), (38, 50), (48, 49)], [0.4, 0.75, 0.3]),
        S([(28, 25), (38, 24), (47, 26)], [0.4, 0.75, 0.3]),
        Blob(36, 36, 0.85),
    ],
    "ganymede": [
        L(circ(36, 36, 19.5, 18), 2.8),
        S([(21, 28), (32, 26), (44, 27.5)], [0.5, 1.2, 0.4]),
        S([(21.5, 31), (32, 29), (44, 30.5)], [0.5, 1.05, 0.4]),
        S([(23, 34), (33, 32), (44, 33.5)], [0.4, 0.9, 0.35]),
        S([(30, 45), (40, 43), (51, 45)], [0.4, 1.1, 0.4]),
        S([(30.5, 48), (40, 46), (50, 48)], [0.4, 0.95, 0.35]),
        S([(32, 51), (40, 49.5), (48, 51)], [0.4, 0.8, 0.3]),
        S([(22, 40), (25, 48), (29, 54)], [0.4, 0.95, 0.35]),
        L(circ(45, 36, 4.6, 11), 1.5),
        D(45, 36, 1.3),
        Blob(27, 40.5, 1.1), Blob(37, 52, 0.95),
    ],
    "titan": [
        L(circ(36, 36, 17.0, 16), 2.8),
        S(earc(36, 36, 13, 13, 40, 140, 11), [0.4, 2.4, 0.4]),
        S([(23, 31), (33, 29.5), (45, 31)], [0.4, 1.1, 0.35]),
        S([(21.5, 37), (33, 35.5), (46, 37)], [0.4, 1.2, 0.35]),
        S([(24, 43), (34, 42), (45, 43.5)], [0.4, 0.95, 0.3]),
        *haze(36, 36, 22.0, [(8, 56), (66, 108), (118, 154), (164, 210),
                             (220, 256), (266, 302), (314, 356)], w=1.4),
        S([(50, 15), (54, 11)], [0.7, 0.25]),
        S([(20, 55), (16, 60)], [0.7, 0.25]),
        S([(58, 44), (63, 47)], [0.7, 0.25]),
    ],
    # ── spacecraft and deep sky (second run) ──────────────────────────
    "satellite": [
        S([(29.5, 29), (36, 29), (42.5, 29)], [2.6, 2.6, 2.6]),
        S([(42, 28.5), (42, 36), (42, 43.5)], [2.6, 2.6, 2.6]),
        S([(42.5, 43), (36, 43), (29.5, 43)], [2.6, 2.6, 2.6]),
        S([(30, 43.5), (30, 36), (30, 28.5)], [2.6, 2.6, 2.6]),
        S([(33, 32), (39, 32)], [0.9, 0.9]),
        S([(33, 40), (39, 40)], [0.9, 0.9]),
        *panel(8.5, 31, 27.5, 41, w=1.9, cols=3, rows=2),
        *panel(44.5, 31, 63.5, 41, w=1.9, cols=3, rows=2),
        S([(27.5, 36), (30, 36)], [1.7, 1.7]),
        S([(42, 36), (44.5, 36)], [1.7, 1.7]),
        S([(36, 43), (36, 48)], [1.6, 1.3]),
        S(earc(36, 50, 6.8, 6.8, 192, 348, 11), [0.6, 2.4, 2.4, 0.6]),
        S([(36, 29), (36, 22.5)], [1.3, 0.6]),
        Blob(36, 21, 1.5),
    ],
    "space-station": [
        S([(7, 24), (36, 24), (65, 24)], [2.3, 2.7, 2.3]),
        S([(8, 21), (36, 21), (64, 21)], [0.9, 1.0, 0.9]),
        S([(8, 27), (36, 27), (64, 27)], [0.9, 1.0, 0.9]),
        S([(12, 21), (17, 27)], [0.7, 0.7]),
        S([(22, 27), (27, 21)], [0.7, 0.7]),
        S([(45, 21), (50, 27)], [0.7, 0.7]),
        S([(55, 27), (60, 21)], [0.7, 0.7]),
        *panel(9, 6, 25, 16, w=1.7, cols=3),
        *panel(47, 6, 63, 16, w=1.7, cols=3),
        *panel(9, 31, 25, 41, w=1.7, cols=3),
        *panel(47, 31, 63, 41, w=1.7, cols=3),
        S([(17, 16), (17, 21)], [1.1, 1.1]),
        S([(55, 16), (55, 21)], [1.1, 1.1]),
        S([(17, 27), (17, 31)], [1.1, 1.1]),
        S([(55, 27), (55, 31)], [1.1, 1.1]),
        S([(36, 27), (36, 45.5)], [1.8, 1.6]),
        L([(26, 46), (34, 45.5), (44, 46), (49, 49), (50, 52), (49, 55),
           (44, 58), (34, 58.5), (26, 58), (22, 55), (21, 52), (22, 49)], 2.3),
        S([(32, 46.5), (32, 58)], [1.2, 1.2]),
        S([(41, 46.5), (41, 57.8)], [1.2, 1.2]),
        S([(50, 52), (55.5, 52)], [1.6, 1.3]),
        Blob(57, 52, 1.9),
        S([(24, 61), (48, 61.5)], [0.7, 0.25]),
    ],
    "probe": [
        S(earc(42, 31, 17.5, 17.5, 62, 298, 17),
          [0.8, 2.6, 3.6, 2.6, 0.8]),
        S([(50.2, 46.5), (51, 31), (50.2, 15.5)], [1.0, 1.7, 1.0]),
        S([(50.2, 16.5), (54.5, 30)], [0.8, 0.35]),
        S([(50.2, 45.5), (54.5, 32)], [0.8, 0.35]),
        Blob(55.5, 31, 2.2),
        S([(24.5, 31), (21, 31)], [1.6, 1.6]),
        *panel(8, 24, 21, 38, w=2.1, cols=2, rows=2),
        S([(13, 38), (11, 49), (9.5, 59)], [1.5, 1.0, 0.3]),
        Blob(9, 61, 1.4),
        S([(18, 24), (17, 17), (16, 12)], [1.1, 0.7, 0.25]),
        S([(31, 20), (33, 14)], [0.7, 0.25]),
    ],
    "rover": [
        S([(8, 62), (30, 62.8), (52, 62.4), (64, 61.8)], [1.2, 1.5, 1.3, 0.5]),
        L([(12, 38), (24, 36.5), (38, 36.5), (52, 38), (59, 42), (59, 48),
           (50, 50.5), (30, 51), (14, 50), (10, 45)], 2.7),
        S([(16, 42.5), (30, 41.5), (44, 42)], [0.9, 0.8, 0.5]),
        L(circ(13, 54.5, 4.7, 11), 1.7), D(13, 54.5, 1.2),
        L(circ(22, 54.5, 4.7, 11), 1.7), D(22, 54.5, 1.2),
        L(circ(31, 54.5, 4.7, 11), 1.7), D(31, 54.5, 1.2),
        L(circ(40, 54.5, 4.7, 11), 1.7), D(40, 54.5, 1.2),
        L(circ(49, 54.5, 4.7, 11), 1.7), D(49, 54.5, 1.2),
        L(circ(58, 54.5, 4.7, 11), 1.7), D(58, 54.5, 1.2),
        S([(13, 50), (22, 50)], [1.0, 1.0]),
        S([(40, 50), (49, 50)], [1.0, 1.0]),
        S([(50, 38), (50, 25)], [2.1, 1.7]),
        L([(43, 17), (49.5, 16), (56, 17), (56, 23), (49.5, 24), (43, 23)], 2.1),
        D(46.5, 20, 1.3), D(52.5, 20, 1.3),
        S([(20, 37), (14, 28), (12, 21)], [1.4, 1.0, 0.3]),
        S([(56, 20), (61, 18)], [0.8, 0.3]),
    ],
    "meteor": [
        Pat([(18, 11.5), (22.5, 13), (24, 17.5), (21.5, 22), (16.5, 22.5),
             (13, 19), (13.5, 14)]),
        S([(22, 21), (32, 31), (44, 43), (55, 54), (62, 61)],
          [9.0, 7.0, 4.5, 2.2, 0.35]),
        S([(19.5, 24), (27, 35), (36, 47), (43, 57)], [5.0, 3.4, 1.9, 0.3]),
        S([(35, 33), (41, 39)], [0.8, 0.25]),
        S([(43, 43), (49, 50)], [0.7, 0.25]),
        S([(13, 10), (9, 6)], [0.9, 0.3]),
        S([(11, 17), (6, 17)], [0.9, 0.3]),
        S([(19, 9), (19, 4.5)], [0.9, 0.3]),
        S([(24, 12), (28.5, 8.5)], [0.8, 0.3]),
    ],
    "asteroid-belt": [
        S(earc(36, 46, 27, 22, 176, 359, 15), [0.3, 0.65, 0.7, 0.65, 0.3]),
        *belt(36, 46, 27, 22, BELT_SPEC),
        Blob(21, 30, 0.8), Blob(52, 31, 0.75), Blob(36, 22.5, 0.7),
    ],
    "nebula": [
        *wash_outline(
            [(34, 9), (44, 14), (50, 12), (57, 20), (59, 30), (63, 38), (56, 46),
             (52, 56), (41, 58), (30, 62), (22, 54), (12, 50), (10, 38), (14, 27),
             (11, 18), (22, 15)],
            [(0.015, 0.19), (0.23, 0.40), (0.44, 0.60), (0.64, 0.81), (0.855, 0.99)],
            [0.5, 2.4, 3.0, 2.2, 0.5]),
        S([(63, 38), (67, 33), (68, 28)], [2.0, 1.0, 0.3]),
        S([(12, 50), (7, 54), (4, 58)], [2.0, 1.0, 0.3]),
        S([(41, 58), (44, 63), (46, 67.5)], [1.8, 1.0, 0.3]),
        S([(22, 15), (16, 10), (12, 6)], [1.8, 1.0, 0.3]),
        S([(22, 28), (32, 24), (44, 27), (52, 34)], [0.8, 1.9, 1.6, 0.5]),
        S([(18, 40), (28, 36), (40, 38), (50, 44)], [0.8, 1.9, 1.6, 0.5]),
        S([(24, 48), (34, 45), (46, 49)], [0.7, 1.4, 0.4]),
        *sparkle(30, 32, 4.0, w=1.7),
        *sparkle(45.5, 42, 3.4, w=1.5),
        *sparkle(22, 45, 2.8, w=1.3),
        *sparkle(48, 24, 3.0, w=1.4),
    ],
    "black-hole": [
        Pat(circ(36, 36, 8.0, 18)),
        L(circ(36, 36, 14.5, 20), 2.8),
        # A near edge-on accretion disc, far flatter than Saturn's ring, so
        # the two glyphs never trade places at small sizes.
        *tilted_ring(36, 36, 30.0, 4.5, 14.5, rot=-7, w_front=2.1, w_back=1.35,
                     front_overhang=3.0),
        S([(63, 43), (68, 46)], [0.9, 0.3]),
        S([(9, 29), (4, 26)], [0.9, 0.3]),
        S([(50, 20), (55, 15)], [0.8, 0.3]),
        S([(22, 52), (17, 57)], [0.8, 0.3]),
    ],
    "eclipse": [
        L(circ(36, 36, 20.0, 20), 2.7),
        S(earc(31.5, 32.5, 16.0, 16.0, 68, 292, 19), [1.0, 5.5, 6.5, 5.0, 0.8]),
        *rays(36, 36, 22.0, ECLIPSE_RAYS, w0=1.8, w1=0.25, bend=0.5),
    ],
    "ceres": [
        L(circ(36, 36, 19.0, 18), 2.8),
        L(circ(42, 30, 4.3, 11), 1.5),
        L(circ(42, 30, 1.9, 8), 1.0),
        *rays(42, 30, 5.4, [(15, 2.6), (70, 2.4), (125, 2.6), (185, 2.4),
                            (240, 2.6), (300, 2.4)], w0=0.9, w1=0.25),
        L(circ(27, 44, 4.1, 10), 1.4),
        L(circ(30, 28, 2.8, 9), 1.2),
        Blob(45, 45, 1.3), Blob(24, 34, 1.1), Blob(36, 51, 1.0),
        S(earc(36, 36, 15, 15, 112, 248, 11), [0.4, 2.2, 0.4]),
    ],
    "phobos": [
        L([(36, 15), (47, 18), (56, 26), (59, 36), (55, 47), (46, 55), (34, 57),
           (23, 53), (15, 44), (13, 33), (18, 22), (26, 16)], 3.1),
        L(circ(24, 32, 9.5, 14), 2.3),
        L(circ(24, 32, 4.4, 11), 1.4),
        D(24, 32, 1.7),
        L(circ(45, 42, 4.2, 10), 1.5),
        L(circ(41, 24, 3.0, 9), 1.3),
        Blob(50, 31, 1.3), Blob(33, 48, 1.2), Blob(20, 46, 1.0),
        S([(31, 19), (36, 30), (40, 42)], [0.6, 1.0, 0.4]),
        S([(39, 18), (44, 29), (48, 39)], [0.5, 0.9, 0.35]),
    ],
    "constellation": [
        *constellation_links(),
        *[Blob(x, y, r, n=10) for x, y, r in CONSTELLATION_STARS],
        *sparkle(13, 20, 6.5, w=1.2),
        *sparkle(50, 38, 6.0, w=1.1),
    ],
}

ORDER = [
    "sun", "mercury", "venus", "earth", "mars",
    "jupiter", "saturn", "uranus", "neptune", "pluto",
    "moon", "comet", "asteroid", "star", "galaxy",
    "io", "europa", "ganymede", "titan",
    "satellite", "space-station", "probe", "rover", "meteor",
    "asteroid-belt", "nebula", "black-hole", "eclipse", "ceres",
    "phobos", "constellation",
]

CATEGORY = "cosmos"


def build_svg(name):
    cp = BLOCK_START + ORDER.index(name)
    rng = random.Random(zlib.crc32(f"{CATEGORY}/{name}/U+{cp:05X}".encode()))
    primary_polys = []
    dry_polys = []
    items = GLYPHS[name]
    for index, item in enumerate(items):
        polys = []
        if item[0] == "stroke":
            polys.extend(stroke_outline(item[1], item[2], rng))
        elif item[0] == "loop":
            pts = list(item[1])
            # Normalise winding so every ring composes the same way with the
            # strokes drawn over it: outer contour negative, hole positive.
            if signed_area(pts) < 0:
                pts.reverse()
            widths = item[2] * len(pts) if len(item[2]) == 1 else item[2]
            polys.extend(stroke_outline(pts, widths, rng, closed=True))
        elif item[0] == "dot":
            polys.extend(dot(item[1], item[2], item[3], rng))
        elif item[0] == "patch":
            smoothed = catmull_rom(item[1], closed=True)
            smoothed = [
                (x + rng.uniform(-0.22, 0.22), y + rng.uniform(-0.22, 0.22))
                for x, y in smoothed
            ]
            # Solid ink shares the strokes' winding so overlaps never cancel.
            if signed_area(smoothed) > 0:
                smoothed.reverse()
            polys.append(smoothed)
        # Keep the structural contour and major masses loaded.  Peripheral
        # strokes and the final observational detail become the lighter,
        # broken hierarchy that must remain distinct in source even though
        # both roles compile to monochrome outlines.
        is_dry = index == len(items) - 1 or (item[0] == "stroke" and index % 4 == 3)
        (dry_polys if is_dry else primary_polys).extend(polys)
    primary_d = " ".join(poly_to_d(poly) for poly in primary_polys)
    dry_d = " ".join(poly_to_d(poly) for poly in dry_polys)
    transforms = {
        "jupiter": "translate(2.16 2.16) scale(.94)",
        "space-station": "translate(5.04 5.04) scale(.86)",
    }
    opening = f'<g transform="{transforms[name]}">' if name in transforms else ""
    closing = "</g>" if opening else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}" role="img" '
        f'aria-label="{CATEGORY} / {name}" data-pua="U+{cp:05X}" '
        f'data-castalia-style="{STYLE}" data-ink-stroke-system="{STROKE_SYSTEM}" '
        'data-ink-animation="wash-v1" data-ink-path-units="normalized">'
        f'<title>{CATEGORY} / {name} — tapered-stroke synthesis</title>'
        f'{opening}<path class="ink-wash" d="{primary_d}" fill="{INK}" data-ink-brush-pass="loaded-ribbon-v2"/>'
        f'<path class="ink-dry" d="{dry_d}" fill="#77746a" data-ink-brush-pass="dry-edge-v2"/>{closing}</svg>'
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", action="store_true", help="update assets/pua/manifest.json")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in ORDER:
        (OUT_DIR / f"{name}.svg").write_text(build_svg(name))
    print(f"wrote {len(ORDER)} glyphs → {OUT_DIR}")

    if args.manifest:
        entries = json.loads(MANIFEST.read_text())
        entries = [e for e in entries if not e.get("label", "").startswith(CATEGORY + "/")]
        for i, name in enumerate(ORDER):
            cp = BLOCK_START + i
            entries.append({
                "name": f"{cp:05X}",
                "source": f"{CATEGORY}/{name}.svg",
                "codepoints": [cp],
                "label": f"{CATEGORY}/{name}",
            })
        MANIFEST.write_text(json.dumps(entries, indent=2) + "\n")
        print(f"manifest updated: {len(entries)} entries")


if __name__ == "__main__":
    main()
