#!/usr/bin/env python3
"""Build full-body dragonfly faerie PUA glyphs as tapered SVG brushwork.

The faeries are deliberately drawn as a small naturalist plate: four
dragonfly wings, a graceful feminine figure, a few anatomical landmarks, and
pose-specific gestures.  The source geometry is converted through the same
loaded-brush tapering pass as the rest of Emojinq, so the checked-in output is
stroke-only and remains suitable for animation, engraving, and font export.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import taper

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "pua" / "faerie"
MANIFEST = ROOT / "assets" / "pua" / "manifest.json"
SVG_NS = "http://www.w3.org/2000/svg"
INK = "#262522"

ET.register_namespace("", SVG_NS)

# Shoulder → elbow → wrist; hip → knee → pointed foot.  Each pose is still
# recognizably the same anatomy, while the long curved marks keep the set
# useful for draw-on animation.
POSES = {
    0xF1500: ("hover", [(30, 25), (22, 24), (14, 21)], [(42, 25), (50, 21), (59, 15)], [(33, 47), (29, 56), (23, 65)], [(41, 47), (45, 56), (52, 62)]),
    0xF1501: ("reach", [(30, 25), (22, 21), (14, 15)], [(42, 25), (51, 18), (62, 11)], [(33, 47), (28, 57), (20, 64)], [(41, 47), (47, 55), (56, 59)]),
    0xF1502: ("dart", [(30, 25), (22, 27), (13, 30)], [(42, 25), (51, 24), (62, 21)], [(33, 47), (25, 50), (16, 47)], [(41, 47), (51, 49), (62, 44)]),
    0xF1503: ("alight", [(30, 25), (24, 31), (20, 39)], [(42, 25), (49, 31), (54, 39)], [(33, 47), (32, 57), (26, 66)], [(41, 47), (44, 57), (50, 66)]),
    0xF1504: ("dance", [(30, 25), (23, 18), (20, 10)], [(42, 25), (51, 17), (54, 8)], [(33, 47), (25, 53), (17, 52)], [(41, 47), (50, 52), (61, 47)]),
    0xF1505: ("bow", [(30, 27), (22, 32), (14, 32)], [(42, 27), (51, 34), (61, 41)], [(33, 49), (27, 57), (19, 62)], [(41, 49), (48, 56), (60, 59)]),
    0xF1506: ("carry", [(30, 25), (24, 18), (24, 11)], [(42, 25), (50, 18), (51, 10)], [(33, 47), (28, 57), (21, 65)], [(41, 47), (47, 56), (56, 62)]),
    0xF1507: ("spin", [(30, 25), (21, 25), (13, 19)], [(42, 25), (52, 29), (62, 37)], [(33, 47), (24, 51), (15, 45)], [(41, 47), (51, 55), (62, 50)]),
}

SEASONS = {
    0xF1510: ("spring", 0xF1500, [("path", "M8 17 C11 13 15 13 18 17 C15 21 11 21 8 17", 1.1), ("path", "M55 18 C58 14 62 14 65 18 C62 22 58 22 55 18", 1.1)]),
    0xF1511: ("summer", 0xF1501, [("circle", (62, 8, 2.6), 1.0), ("path", "M62 2 V4 M62 12 V14 M56 8 H58 M66 8 H68", 0.75)]),
    0xF1512: ("autumn", 0xF1507, [("path", "M7 17 C12 14 16 16 17 21 C12 23 8 21 7 17", 1.1), ("path", "M56 55 C61 52 65 54 66 59 C61 61 57 59 56 55", 1.1)]),
    0xF1513: ("winter", 0xF1503, [("path", "M10 15 V25 M5 20 H15 M6.5 16.5 L13.5 23.5 M13.5 16.5 L6.5 23.5", 0.8), ("path", "M61 49 V59 M56 54 H66 M57.5 50.5 L64.5 57.5 M64.5 50.5 L57.5 57.5", 0.8)]),
}


def element(root: ET.Element, tag: str, attrs: dict[str, str]) -> None:
    attrs = {"fill": "none", "stroke": INK, "stroke-linecap": "round", "stroke-linejoin": "round", **attrs}
    ET.SubElement(root, f"{{{SVG_NS}}}{tag}", attrs)


def path(root: ET.Element, d: str, width: float) -> None:
    element(root, "path", {"d": d, "stroke-width": f"{width:.2f}"})


def circle(root: ET.Element, cx: float, cy: float, radius: float, width: float) -> None:
    element(root, "circle", {"cx": str(cx), "cy": str(cy), "r": str(radius), "stroke-width": f"{width:.2f}"})


def filled_path(root: ET.Element, d: str, opacity: float = 1.0) -> None:
    """Add one loaded-ink mass that will survive at small emoji sizes."""
    ET.SubElement(root, f"{{{SVG_NS}}}path", {
        "d": d,
        "fill": INK,
        "stroke": "none",
        "fill-opacity": f"{opacity:.2f}",
        "data-ink-brush-pass": "loaded-mass-v1",
    })


def curved_mark(points: list[tuple[float, float]], width: float) -> str:
    """Return one gently irregular cubic mark through three landmarks."""
    (x0, y0), (x1, y1), (x2, y2) = points
    c1 = (x0 + (x1 - x0) * 0.58, y0 + (y1 - y0) * 0.58)
    c2 = (x1 - (x2 - x1) * 0.36, y1 - (y2 - y1) * 0.36)
    c3 = (x1 + (x2 - x1) * 0.36, y1 + (y2 - y1) * 0.36)
    c4 = (x1 + (x2 - x1) * 0.76, y1 + (y2 - y1) * 0.76)
    return (
        f"M{x0:.2f} {y0:.2f} C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {x1:.2f} {y1:.2f} "
        f"C{c3[0]:.2f} {c3[1]:.2f} {c4[0]:.2f} {c4[1]:.2f} {x2:.2f} {y2:.2f}"
    )


def limb(root: ET.Element, points: list[tuple[float, float]], width: float, foot: bool = False) -> None:
    path(root, curved_mark(points, width), width)
    if foot and len(points) == 3:
        # A broken inner knee/ankle contour gives the long leg a little
        # anatomy without outlining it like a tube.
        (x0, y0), (x1, y1), (x2, y2) = points
        path(root, f"M{x0 + 1.2:.2f} {y0 + .8:.2f} C{x1 + 1.0:.2f} {y1 - 1.0:.2f} {x2 + .8:.2f} {y2 - 1.0:.2f} {x2 + .2:.2f} {y2:.2f}", 0.62)


def dragonfly_wings(root: ET.Element) -> None:
    # Two matched pairs leave the thorax on both sides.  The upper pair is
    # longer and slightly narrower; the lower pair opens more horizontally.
    # Small hand-drawn differences keep the result alive while the overall
    # silhouette remains unmistakably four-winged and bilaterally balanced.
    path(root, "M34.5 25.5 C27 18 17 8 5.5 8 C10 18 21 27 34.8 29.5", 1.45)
    path(root, "M37.5 25.5 C45 18 55 8.5 66.5 8 C62 18 51 27 37.2 29.5", 1.45)
    path(root, "M34.7 29 C24 27 13 31 5.5 39 C16 39 26 35 35.2 32", 1.30)
    path(root, "M37.3 29 C48 27 59 31 66.5 39 C56 39 46 35 36.8 32", 1.30)

    # One primary vein and one short cross-vein in each membrane.  These
    # remain sparse enough for sumi-e draw-on animation and small-size use.
    path(root, "M34 26.5 C25 20 16 13 8.5 10", 0.42)
    path(root, "M38 26.5 C47 20 56 13 63.5 10", 0.42)
    path(root, "M34.5 30 C24 30 15 34 8.5 37", 0.40)
    path(root, "M37.5 30 C48 30 57 34 63.5 37", 0.40)
    path(root, "M25 19 C20 17 16 15 12.5 14", 0.30)
    path(root, "M47 19 C52 17 56 15 59.5 14", 0.30)
    path(root, "M24 31 C19 32 15 34 12 36", 0.30)
    path(root, "M48 31 C53 32 57 34 60 36", 0.30)


def body_and_face(root: ET.Element) -> None:
    # The font is normally shown at only 55–70 px. A filled profile and torso
    # retain a recognisable person there; the former contour-only treatment
    # collapsed into a dot and several sticks on the A16.
    filled_path(root, "M31.5 12 C31.5 8.4 33.4 6 36 6 C38.8 6 40.6 8.3 40.5 11.2 C42.2 12.1 42 13.4 40.2 14 C39.7 16.8 38.1 18.5 35.8 18.5 C33.1 18.5 31.4 16 31.5 12 Z")
    # A compact swept hair mark gives the otherwise near-frontal body a
    # faerie identity without widening the head or hiding the wing roots.
    filled_path(root, "M32.6 9.8 C29.8 8.8 29.2 6.3 31.2 4.5 C34 2.7 38.3 3.2 40.5 5.7 C37.2 5.1 34.2 6.4 32.6 9.8 Z", .90)

    # A narrow thorax flows through a human waist into a slender hip. There
    # is no broad dress/tunic mass: the pose-specific legs remain completely
    # visible, while the long central rhythm still recalls a dragonfly.
    filled_path(root, "M33.2 18 C31.5 21.3 30.9 25.2 32.1 29 C33.1 32 33.5 34.6 33 37.3 C32.5 40.4 31.7 43.4 32.2 46.5 C34.5 48 37.5 48 39.8 46.5 C40.3 43.4 39.5 40.4 39 37.3 C38.5 34.6 38.9 32 39.9 29 C41.1 25.2 40.5 21.3 38.8 18 C37.2 19.1 34.8 19.1 33.2 18 Z")
    # Two tiny dry-brush accents suggest eye and chin without hollowing the
    # silhouette or drawing a cartoon face.
    path(root, "M36.8 11.2 q.8 .3 0 1 M39.9 13.7 q.7 .1 1 -.2", 0.46)


def fairy_svg(cp: int, pose_cp: int, ornaments: list[tuple] | None = None) -> str:
    name = POSES[pose_cp][0]
    _, left_arm, right_arm, left_leg, right_leg = POSES[pose_cp]
    root = ET.Element(f"{{{SVG_NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": f"faerie / {name}",
        "data-pua": f"U+{cp:X}",
        "data-ink-animation": "draw-v1",
        "data-ink-path-units": "normalized",
        "data-wing-count": "4",
        "data-wing-symmetry": "bilateral-v2",
        "data-body-form": "long-slender-v2",
    })
    ET.SubElement(root, f"{{{SVG_NS}}}title").text = f"Faerie / {name} — full-body dragonfly-wing sumi-e figure"
    wing_marks = ET.SubElement(root, f"{{{SVG_NS}}}g", {
        "fill": "none", "stroke": INK, "stroke-linecap": "round", "stroke-linejoin": "round"
    })
    dragonfly_wings(wing_marks)
    marks = ET.SubElement(root, f"{{{SVG_NS}}}g", {
        "fill": "none", "stroke": INK, "stroke-linecap": "round", "stroke-linejoin": "round"
    })
    limb(marks, left_arm, 3.15)
    limb(marks, right_arm, 3.15)
    limb(marks, left_leg, 3.45, foot=True)
    limb(marks, right_leg, 3.45, foot=True)

    for ornament in ornaments or []:
        tag, value, width = ornament
        if tag == "circle":
            cx, cy, radius = value
            circle(marks, cx, cy, radius, width)
        else:
            path(marks, value, width)

    # Convert the deliberately sparse source marks to normalized, loaded-
    # middle brush strokes.  This also removes any accidental source shapes
    # that could carry a fill into the production font.
    taper(root)
    # line_brush intentionally converts every SVG primitive into a tapered
    # centerline. Add the filled anatomy after that pass so it remains a
    # loaded ink mass. Insert it between the rear wings and foreground limbs.
    body_mass = ET.Element(f"{{{SVG_NS}}}g", {"fill": INK, "stroke": "none"})
    body_and_face(body_mass)
    root.insert(2, body_mass)
    root.set("data-castalia-style", "sumi-e-ink-wash-v1")
    root.set("data-ink-stroke-system", "tapered-v1")
    root.set("data-ink-coverage", "complete")
    return ET.tostring(root, encoding="unicode") + "\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for cp, (name, *_rest) in POSES.items():
        filename = f"{name}.svg"
        (OUT / filename).write_text(fairy_svg(cp, cp), encoding="utf-8")
        entries.append({"name": f"{cp:X}", "source": f"faerie/{filename}", "codepoints": [cp], "label": f"faerie/{name}"})
    for cp, (name, base, ornaments) in SEASONS.items():
        filename = f"season-{name}.svg"
        (OUT / filename).write_text(fairy_svg(cp, base, ornaments), encoding="utf-8")
        entries.append({"name": f"{cp:X}", "source": f"faerie/{filename}", "codepoints": [cp], "label": f"faerie/season-{name}"})

    manifest = json.loads(MANIFEST.read_text())
    reserved = set(POSES) | set(SEASONS)
    manifest = [item for item in manifest if not (len(item.get("codepoints", [])) == 1 and item["codepoints"][0] in reserved)]
    manifest.extend(entries)
    manifest.sort(key=lambda item: tuple(item.get("codepoints", [])))
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"build_faerie_pua: wrote {len(entries)} full-body dragonfly faeries")


if __name__ == "__main__":
    main()
