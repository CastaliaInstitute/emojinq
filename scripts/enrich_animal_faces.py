#!/usr/bin/env python3
"""Replace face-only animal emoji with compact side-profile studies.

OpenMoji's face glyphs are useful semantic references, but a face alone is not
enough for a naturalist animal vocabulary.  This pass keeps the Unicode code
point and label while supplying a small, stroke-only profile with one clear
eye, species cues, body mass, legs, and tail.  ``line_brush.taper`` applies the
shared loaded-middle pressure treatment after the semantic gestures are laid
out.
"""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import taper

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def path(d: str, width: float = 2.0, role: str = "profile") -> dict[str, str]:
    return {
        "d": d,
        "fill": "none",
        "stroke": "#000000",
        "stroke-width": str(width),
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "data-ink-role": f"animal-{role}",
    }


def circle(cx: float, cy: float, radius: float = 1.0, role: str = "eye") -> dict[str, str]:
    return {
        "cx": str(cx), "cy": str(cy), "r": str(radius),
        "fill": "none", "stroke": "#000000", "stroke-width": "1.8",
        "data-ink-role": f"animal-{role}",
    }


# All profiles face left.  The first three marks carry the silhouette; the
# remaining marks are deliberately sparse recognition cues.
PROFILES: dict[str, tuple[str, list[dict[str, str]]]] = {
    "1F42D": ("Mouse Face — side profile", [
        path("M 12 36 C 14 31 18 28 23 29 C 27 29 29 32 30 35 C 38 31 48 32 53 38 C 57 42 56 49 51 52 C 45 56 35 54 29 50 C 26 48 24 46 22 44"),
        path("M 13 36 C 10 35 9 33 11 31 C 13 30 16 30 18 31 M 19 29 C 18 26 19 24 21 23 C 23 24 24 26 23 29", role="head"),
        path("M 51 46 C 59 49 64 55 61 59 C 57 59 54 57 51 54", role="tail"),
        path("M 29 49 C 29 53 27 56 24 57 M 43 52 C 43 55 45 57 48 57", role="leg"),
        circle(17.5, 33.5, .9), path("M 12 36 L 9 37", 1.2, "whisker"),
    ]),
    "1F42E": ("Cow Face — side profile", [
        path("M 13 37 C 15 32 19 29 24 30 C 29 29 33 31 36 34 C 42 31 51 32 56 37 C 59 41 58 49 53 52 C 47 56 35 55 28 51 C 24 48 22 44 21 42"),
        path("M 14 37 C 10 37 9 35 11 33 C 13 32 17 33 20 35 M 20 31 C 18 28 18 25 20 23 C 22 25 23 27 23 30 M 26 30 C 27 27 29 25 31 25 C 32 28 30 30 28 32", role="head"),
        path("M 52 48 C 58 48 63 50 62 54 C 60 56 57 56 54 54", role="tail"),
        path("M 29 50 C 29 54 27 56 24 57 M 45 52 C 45 55 47 57 50 57", role="leg"),
        path("M 34 48 C 35 51 37 52 39 52", 1.3, "udder"), circle(18.5, 35, .85),
    ]),
    "1F42F": ("Tiger Face — side profile", [
        path("M 12 36 C 14 31 18 28 23 29 C 28 29 31 32 33 35 C 40 31 49 32 54 37 C 58 42 57 49 52 52 C 46 55 36 54 29 50 C 26 48 24 45 23 42"),
        path("M 13 36 C 10 35 9 33 11 31 C 14 30 17 31 20 33 M 20 30 C 19 26 20 23 22 21 C 24 24 25 27 24 30", role="head"),
        path("M 51 47 C 58 47 62 44 63 40 C 64 45 62 49 58 51", role="tail"),
        path("M 29 48 C 29 53 27 56 24 57 M 44 51 C 44 55 46 57 49 57", role="leg"),
        path("M 28 33 L 31 36 M 32 31 L 34 35 M 38 33 L 40 36 M 44 33 L 46 36", 1.2, "stripe"), circle(18, 34, .9),
    ]),
    "1F430": ("Rabbit Face — side profile", [
        path("M 13 37 C 15 32 19 29 24 30 C 29 30 32 34 34 38 C 42 32 51 34 55 40 C 58 45 55 51 50 53 C 43 56 34 53 29 49 C 26 46 24 43 22 41"),
        path("M 14 37 C 10 36 9 34 11 32 C 13 31 17 32 20 34 M 21 30 C 19 24 19 17 21 12 C 24 18 25 24 24 30 M 25 30 C 24 23 25 17 28 14 C 29 20 29 26 27 31", role="head"),
        path("M 49 49 C 54 51 58 49 60 46 C 61 50 59 53 55 54", role="tail"),
        path("M 30 48 C 28 53 27 56 23 57 M 43 51 C 44 55 46 57 49 57", role="leg"),
        circle(18, 35, .85), path("M 13 37 L 10 38", 1.2, "whisker"),
    ]),
    "1F431": ("Cat Face — side profile", [
        path("M 12 36 C 15 31 19 29 24 30 C 29 30 32 33 34 36 C 41 31 50 32 55 37 C 59 42 58 49 53 52 C 47 55 37 54 30 50 C 27 48 25 45 23 42"),
        path("M 13 36 C 10 35 9 33 11 31 C 14 30 17 31 20 33 M 20 30 L 21 22 L 26 28 M 25 29 L 30 23 L 30 31", role="head"),
        path("M 52 47 C 59 45 63 39 62 33 C 66 39 65 46 59 51", role="tail"),
        path("M 30 48 C 29 53 27 56 24 57 M 45 51 C 45 55 47 57 50 57", role="leg"),
        circle(18, 34, .9), path("M 13 36 L 9 35 M 13 37 L 9 38", 1.1, "whisker"),
    ]),
    "1F432": ("Dragon Face — side profile", [
        path("M 11 35 C 15 31 20 30 25 32 C 30 33 33 36 36 39 C 42 35 50 36 55 40 C 58 44 57 50 52 52 C 45 55 36 52 30 48 C 27 45 25 42 23 40"),
        path("M 12 35 L 8 34 L 11 32 L 8 30 L 15 30 C 16 26 19 23 23 22 L 21 27 L 27 25 L 25 31", role="head"),
        path("M 51 47 C 57 47 61 44 64 40 C 63 46 60 51 55 53", role="tail"),
        path("M 33 37 C 37 28 45 25 50 29 C 47 32 45 35 44 39 M 37 40 C 41 38 45 39 48 43", role="wing"),
        path("M 30 47 C 29 52 27 55 24 56 M 44 51 C 45 54 47 56 50 56", role="leg"), circle(17, 33, .9),
    ]),
    "1F435": ("Monkey Face — side profile", [
        path("M 13 36 C 15 31 19 29 24 30 C 29 30 32 33 34 36 C 41 31 50 32 54 37 C 58 42 57 49 52 52 C 46 55 36 54 30 50 C 27 48 25 44 23 42"),
        path("M 14 36 C 10 36 9 33 11 31 C 14 30 17 31 20 33 M 20 31 C 18 27 19 24 22 23 C 25 24 26 27 24 30", role="head"),
        path("M 51 46 C 60 45 64 51 61 57 C 59 59 56 58 54 55", role="tail"),
        path("M 30 48 C 29 53 27 56 24 57 M 44 51 C 44 55 46 57 49 57", role="leg"),
        path("M 54 55 C 57 52 60 52 62 54", 1.25, "tail-grip"), circle(18, 34, .9),
    ]),
    "1F436": ("Dog Face — side profile", [
        path("M 12 37 C 15 32 19 30 24 31 C 29 31 32 34 34 37 C 42 32 51 33 56 38 C 59 43 57 50 52 52 C 45 55 36 54 30 50 C 27 47 25 44 23 42"),
        path("M 13 37 C 10 36 9 34 11 32 C 14 31 17 32 20 34 M 21 32 C 18 29 17 25 19 23 C 23 24 25 28 24 31", role="head"),
        path("M 52 47 C 59 48 62 45 64 42 C 65 47 62 52 57 53", role="tail"),
        path("M 30 48 C 29 53 27 56 24 57 M 45 51 C 45 55 47 57 50 57", role="leg"),
        circle(18, 35, .9), path("M 13 37 L 10 38", 1.15, "whisker"),
    ]),
    "1F437": ("Pig Face — side profile", [
        path("M 13 38 C 15 33 20 30 26 31 C 31 31 34 34 36 37 C 43 33 51 34 56 39 C 59 44 57 50 52 52 C 46 55 36 54 30 50 C 27 47 25 44 23 42"),
        path("M 13 38 C 9 38 8 35 10 33 C 12 31 16 32 19 34 M 21 32 C 20 29 21 27 23 26 C 25 28 26 30 25 32", role="head"),
        path("M 52 47 C 58 48 61 45 63 42 C 64 48 61 52 57 53 C 55 52 54 50 52 47", role="tail"),
        path("M 30 48 C 29 53 27 56 24 57 M 45 51 C 45 55 47 57 50 57", role="leg"),
        path("M 11 35 C 13 34 15 34 17 35 M 11 37 C 13 36 15 36 17 37", 1.15, "snout"), circle(20, 35, .85),
    ]),
    "1F438": ("Frog Face — side profile", [
        path("M 13 42 C 16 36 21 33 27 34 C 33 34 36 38 38 42 C 44 38 51 39 55 43 C 58 47 56 52 51 54 C 44 56 35 53 29 49 C 25 47 22 45 20 44"),
        path("M 14 42 C 10 42 9 39 11 37 C 14 35 18 36 21 38 M 20 36 C 19 32 21 29 24 29 C 26 32 26 35 24 37", role="head"),
        path("M 51 50 C 57 51 61 48 63 45 C 64 51 60 55 55 55", role="tail"),
        path("M 30 48 C 27 52 23 55 19 54 C 22 58 27 59 32 55 M 43 51 C 45 55 49 57 53 56", role="hind-leg"),
        circle(18, 39, .9), path("M 14 42 L 10 43", 1.1, "whisker"),
    ]),
    "1F439": ("Hamster Face — side profile", [
        path("M 13 38 C 15 32 20 29 26 30 C 32 30 35 34 36 38 C 44 33 52 35 56 40 C 59 45 57 51 52 53 C 45 55 35 53 29 49 C 25 46 23 43 21 41"),
        path("M 14 38 C 10 37 9 34 11 32 C 14 31 18 32 20 34 M 20 32 C 19 29 21 27 23 27 C 25 29 25 31 24 33", role="head"),
        path("M 52 48 C 57 49 60 47 62 45 C 62 50 59 53 55 54", role="tail"),
        path("M 30 48 C 29 53 27 56 24 57 M 45 51 C 45 55 47 57 50 57", role="leg"),
        circle(18, 36, .9), path("M 14 38 L 10 39", 1.1, "whisker"),
    ]),
    "1F43A": ("Wolf Face — side profile", [
        path("M 11 35 C 14 30 18 27 23 29 C 28 29 31 32 33 35 C 41 30 51 31 56 36 C 60 41 59 49 53 52 C 46 55 36 54 30 50 C 26 47 24 43 22 41"),
        path("M 12 35 C 9 34 8 32 10 30 C 13 29 17 30 20 32 M 20 30 L 20 20 L 26 27 M 25 28 L 31 20 L 30 31", role="head"),
        path("M 53 47 C 60 47 63 43 65 39 C 66 46 62 51 57 53", role="tail"),
        path("M 30 48 C 29 53 27 56 24 57 M 45 51 C 45 55 47 57 50 57", role="leg"),
        path("M 33 33 L 36 36 M 39 32 L 41 35 M 45 32 L 47 35", 1.2, "fur"), circle(17, 33, .9),
    ]),
    "1F43B": ("Bear Face — side profile", [
        path("M 12 38 C 14 31 20 27 27 29 C 33 29 36 33 38 37 C 45 31 53 33 57 39 C 60 45 57 51 52 53 C 45 56 34 54 28 50 C 24 47 22 43 20 41"),
        path("M 13 38 C 9 37 8 34 10 32 C 13 30 17 31 20 34 M 19 31 C 18 27 20 24 23 25 C 25 27 25 30 23 32", role="head"),
        path("M 52 48 C 59 49 62 46 64 43 C 65 49 61 53 57 54", role="tail"),
        path("M 29 49 C 28 54 26 56 23 57 M 45 51 C 45 55 47 57 50 57", role="leg"),
        path("M 34 33 C 39 31 43 32 47 35", 1.25, "shoulder"), circle(18, 35, .9),
    ]),
    "1F43C": ("Panda Face — side profile", [
        path("M 12 38 C 14 32 20 29 26 30 C 32 30 35 34 37 38 C 44 33 52 34 56 39 C 59 44 57 51 52 53 C 45 56 35 54 29 50 C 25 47 23 43 21 41"),
        path("M 13 38 C 9 37 9 34 11 32 C 14 31 17 32 20 34 M 20 32 C 19 29 21 27 23 27 C 25 29 25 31 24 33", role="head"),
        path("M 52 48 C 58 49 61 46 63 43 C 64 49 61 53 56 54", role="tail"),
        path("M 29 49 C 28 54 26 56 23 57 M 45 51 C 45 55 47 57 50 57", role="leg"),
        path("M 20 34 C 22 32 24 33 25 35 C 23 37 21 37 19 36", 1.2, "eye-patch"), circle(21.5, 35, .7),
    ]),
    "1F981": ("Lion Face — side profile", [
        path("M 12 37 C 14 31 19 28 24 30 C 29 30 32 33 34 36 C 42 31 52 32 56 38 C 59 43 58 50 52 53 C 45 56 35 54 29 50 C 26 47 24 44 22 42"),
        path("M 13 37 C 9 36 9 33 11 31 C 14 30 17 31 20 33 M 20 31 C 19 28 21 25 23 24 C 25 26 25 29 24 31", role="head"),
        path("M 16 33 C 14 29 16 25 20 23 C 18 19 22 17 25 20 C 28 17 33 20 32 24 C 36 25 37 29 34 32", role="mane"),
        path("M 52 48 C 59 48 62 45 64 41 C 65 47 62 52 57 53", role="tail"),
        path("M 30 49 C 29 54 27 56 24 57 M 45 51 C 45 55 47 57 50 57", role="leg"), circle(18, 34, .9),
    ]),
    "1F98A": ("Fox Face — side profile", [
        path("M 11 36 C 14 30 19 27 24 29 C 29 29 32 32 34 35 C 42 30 51 32 56 37 C 60 42 58 49 53 52 C 46 56 36 54 29 50 C 26 47 24 43 22 41"),
        path("M 12 36 C 9 35 8 33 10 31 C 13 30 17 31 20 33 M 20 30 L 21 20 L 26 27 M 25 28 L 31 20 L 30 31", role="head"),
        path("M 52 47 C 59 47 63 42 64 36 C 67 42 65 49 59 53 C 56 52 54 50 52 47", role="bushy-tail"),
        path("M 30 48 C 29 53 27 56 24 57 M 45 51 C 45 55 47 57 50 57", role="leg"),
        path("M 54 39 C 58 40 61 42 63 45", 1.2, "tail-fur"), circle(17.5, 33.5, .9), path("M 12 36 L 9 37", 1.15, "whisker"),
    ]),
}


def build(target: Path, codepoint: str, label: str, marks: list[dict[str, str]]) -> None:
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72", "role": "img",
        "aria-label": label, "data-animal-profile": "side-v1",
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-coverage": "complete",
        "data-ink-animation": "draw-v1",
        "data-ink-path-units": "normalized",
    })
    title = ET.SubElement(root, f"{{{NS}}}title")
    title.text = f"{label} — side-profile naturalist study"
    group = ET.SubElement(root, f"{{{NS}}}g", {"id": "side-profile-source"})
    for mark in marks:
        tag = "circle" if "cx" in mark else "path"
        ET.SubElement(group, f"{{{NS}}}{tag}", mark)
    taper(root)
    root.set("data-animal-profile", "side-v1")
    root.set("data-codepoint", codepoint)
    target.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/gray-all"))
    args = parser.parse_args()
    for codepoint, (label, marks) in PROFILES.items():
        target = args.root / f"{codepoint}.svg"
        if target.exists():
            build(target, codepoint, label, marks)
    print(f"enriched {sum((args.root / f'{cp}.svg').exists() for cp in PROFILES)} side-profile animal glyphs")


if __name__ == "__main__":
    main()
