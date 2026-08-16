#!/usr/bin/env python3
"""Replace the small animal PUA studies with recognizable stroke-only gestures.

The generated naturalist contact sheet is used as a visual reference, not as a
shipped raster. These constructions keep the silhouette, face, feet, and
species cues in a small number of long brush paths.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "animals"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def p(d: str, width: float = 1.0, color: str = "#262421") -> tuple[str, float, str]:
    return d, width, color


ART: dict[str, tuple[int, str, list[tuple[str, float, str]]]] = {
    "calf.svg": (0xF0000, "animals / calf", [
        p("M10 43 C13 38 14 32 20 28 C27 24 38 24 46 28 C48 24 49 19 53 17 C57 14 62 16 64 19 C62 22 60 25 57 27 C60 29 62 32 62 35 C60 39 56 41 52 41 C50 46 49 52 49 57", 1.34),
        p("M10 43 C13 46 18 47 23 46 C28 45 31 44 35 45 C39 46 43 46 47 44", 1.18),
        p("M20 45 C19 49 18 54 18 58 C20 60 23 59 24 57 M31 45 C31 50 31 55 32 59 C34 60 37 59 37 57 M43 45 C43 50 43 55 44 59 C46 60 49 59 49 57", 1.02),
        p("M49 19 C46 17 43 16 40 17 C41 20 44 23 48 24 M57 17 C60 16 63 17 65 19 C63 21 60 23 58 24", .96),
        p("M53 27 C54 25 55 24 57 24 M54 30 C55 29 56 29 57 30 C56 31 55 31 54 30 M57 34 C59 34 60 34 61 35 C60 37 58 37 57 36", .60, "#4a4943"),
        p("M25 28 C29 26 33 26 37 27 M28 31 C32 29 36 29 40 30 M39 35 C43 33 46 33 49 34 M25 39 C29 37 33 37 36 38", .56, "#4a4943"),
    ]),
    "lamb.svg": (0xF0004, "animals / lamb", [
        p("M18 38 C17 33 20 28 26 27 C33 23 45 24 52 28 C57 31 59 36 57 41 C55 46 49 48 42 47 L28 47 C22 46 19 43 18 38", 1.36),
        p("M22 31 C18 31 15 29 14 26 C15 23 18 22 21 24 C22 21 26 20 29 22 C30 25 28 29 25 30", 1.02),
        p("M15 26 C17 27 19 27 21 26 M25 22 C26 24 26 26 25 28", .54, "#4a4943"),
        p("M26 46 C25 50 25 54 24 57 C26 59 29 59 30 57 M37 47 C37 51 37 55 36 58 C38 60 41 59 42 57 M49 45 C49 49 50 53 52 56 C54 57 56 56 56 54", 1.00),
        p("M29 28 C31 25 33 24 35 26 M34 29 C36 25 39 24 41 26 M40 29 C43 26 46 26 48 28 M47 32 C50 30 53 31 54 34", .62, "#4a4943"),
        p("M23 28 C24 27 25 27 26 28 C25 29 24 29 23 28 M36 30 C38 29 40 29 41 30", .56, "#4a4943"),
    ]),
    "herd.svg": (0xF0003, "animals / herd", [
        p("M7 37 C9 32 14 29 20 30 C25 31 28 35 31 37 C35 33 40 31 46 33 C50 34 53 37 55 39 C58 35 62 34 66 36", 1.22),
        p("M8 37 C10 40 12 42 16 42 L22 41 M32 37 C34 40 36 42 40 42 L46 40 M56 39 C58 42 61 43 65 42", 1.02),
        p("M12 33 C10 30 10 27 12 25 C15 26 17 28 17 30 M18 31 C18 27 20 25 22 24 C24 27 23 30 22 32", .92),
        p("M39 34 C38 30 39 27 42 25 C44 28 44 30 43 33 M46 34 C47 30 49 28 51 28 C52 31 51 33 50 35", .88),
        p("M60 36 C59 32 60 29 63 28 C65 30 65 33 64 35", .82),
        p("M13 42 L13 54 M20 41 L20 53 M36 42 L36 55 M44 41 L44 53 M59 42 L59 54 M64 42 L65 52", .92),
        p("M8 37 C9 36 10 35 12 35 M17 34 C19 33 21 33 23 34 M39 35 C41 34 43 34 45 35 M59 37 C61 36 63 36 65 37", .50, "#4a4943"),
    ]),
    "pack.svg": (0xF0006, "animals / pack", [
        p("M7 43 C11 39 16 37 21 38 C25 39 28 42 31 44 C35 40 40 38 45 39 C50 40 53 43 56 45 C59 41 63 40 66 42", 1.24),
        p("M8 43 C10 46 13 48 17 47 L22 45 M32 44 C34 47 37 49 41 48 L46 45 M57 45 C59 48 62 49 66 47", .98),
        p("M12 39 C10 36 10 33 12 31 L15 34 L18 31 C20 34 19 37 17 39 M39 40 C37 37 38 34 40 32 L43 35 L46 33 C48 36 47 39 45 40 M60 42 C59 39 60 36 62 35 L64 38 L66 37 C68 40 66 42 64 43", .94),
        p("M13 47 L12 56 M20 46 L21 55 M37 48 L36 57 M44 46 L46 55 M60 48 L59 56 M65 47 L66 54", .92),
        p("M16 38 C18 38 20 39 21 40 M43 39 C45 39 47 40 48 41 M63 42 C64 42 65 42 66 43", .48, "#4a4943"),
    ]),
    "predator.svg": (0xF0007, "animals / predator", [
        p("M9 45 C13 39 18 35 25 33 C32 31 39 32 45 35 C49 37 54 36 58 33 C61 31 64 32 65 35 C64 38 61 40 58 41 C57 47 53 51 48 53 C41 56 33 55 26 53 C20 51 14 49 9 45", 1.42),
        p("M9 45 C7 43 7 40 9 38 L13 36 L15 32 L18 36 C21 35 23 36 24 38 C21 41 18 43 15 44", 1.08),
        p("M13 36 L12 32 L16 34 M18 36 L20 32 L22 37", .76),
        p("M28 51 C27 55 25 57 23 58 M38 54 C38 57 37 59 35 60 M49 52 C51 55 53 56 55 56", 1.02),
        p("M52 37 C56 38 58 39 60 39 M29 37 C33 35 37 35 40 37 M24 45 C28 47 31 47 34 46", .54, "#4a4943"),
        p("M17 39 C18 38 19 38 20 39 C19 40 18 40 17 39", .64),
    ]),
    "prey.svg": (0xF0008, "animals / prey", [
        p("M18 45 C21 39 25 34 31 32 C37 30 44 31 49 34 C53 36 57 38 61 37 C63 36 65 37 66 39 C65 41 62 42 59 42 C57 47 53 51 47 53 C39 55 31 54 25 52 C21 50 19 48 18 45", 1.36),
        p("M18 45 C15 43 13 40 14 37 L18 35 L20 30 L23 35 C26 34 29 35 30 37 C28 40 25 42 22 43", 1.02),
        p("M18 35 L16 31 L20 33 M22 35 L24 30 L26 35", .76),
        p("M29 51 C29 55 28 58 26 59 M40 53 C40 56 40 58 38 60 M51 51 C52 55 54 57 56 58", .96),
        p("M23 39 C25 38 27 38 28 39 M35 35 C39 34 42 35 45 36 M47 44 C50 43 52 42 54 40", .54, "#4a4943"),
        p("M23 37 C24 36 25 36 26 37 C25 38 24 38 23 37", .62),
    ]),
    "colony.svg": (0xF0001, "animals / colony", [
        p("M8 30 C10 26 14 25 18 27 C21 29 21 33 18 36 C15 39 10 38 8 35 C7 33 7 31 8 30 M29 23 C31 19 35 18 39 20 C42 22 42 26 39 29 C36 32 31 31 29 28 C28 26 28 24 29 23 M48 38 C50 34 54 33 58 35 C61 37 61 41 58 44 C55 47 50 46 48 43 C47 41 47 39 48 38", .86),
        p("M8 31 C5 29 3 28 2 26 M9 34 C6 35 4 36 2 38 M17 29 C20 27 22 26 24 25 M17 36 C20 37 22 38 24 40 M30 22 C28 20 27 18 27 16 M38 21 C40 18 41 17 43 16 M49 39 C46 38 44 37 42 36 M58 42 C61 43 63 44 65 46", .48, "#4a4943"),
        p("M11 28 C12 24 14 22 16 21 M14 38 C15 41 16 43 18 44 M33 20 C34 16 35 14 37 13 M37 31 C38 34 39 36 41 37 M52 35 C53 31 54 29 56 28 M55 46 C56 48 57 50 59 51", .62),
        p("M12 31 C13 30 14 30 15 31 C14 32 13 32 12 31 M33 24 C34 23 35 23 36 24 C35 25 34 25 33 24 M52 40 C53 39 54 39 55 40 C54 41 53 41 52 40", .50),
    ]),
    "flock.svg": (0xF0002, "animals / flock", [
        p("M6 36 C12 30 18 28 25 30 C21 31 17 33 14 37 C19 35 24 35 29 37 C23 38 18 40 14 43", 1.12),
        p("M28 25 C34 19 40 18 47 21 C43 22 39 24 36 28 C41 26 46 27 50 30 C44 30 39 32 35 35", 1.04),
        p("M48 42 C53 37 59 36 66 39 C62 40 59 42 57 45 C61 44 64 45 67 47 C62 47 58 49 55 51", 1.04),
        p("M16 31 C18 28 19 25 19 22 M37 22 C39 19 40 16 40 13 M57 39 C59 36 60 33 60 30", .56, "#4a4943"),
    ]),
    "migration.svg": (0xF0005, "animals / migration", [
        p("M7 35 C12 30 17 28 23 30 C19 31 16 33 13 36 C17 35 21 36 24 38 C19 38 15 40 12 43", 1.04),
        p("M27 28 C33 22 39 21 45 23 C41 24 37 26 34 30 C39 28 43 29 47 31 C42 31 37 33 33 36", 1.12),
        p("M48 22 C53 17 59 16 65 19 C61 20 57 22 54 25 C58 24 62 25 66 27 C61 27 57 29 53 32", 1.02),
        p("M15 31 C17 28 18 25 18 22 M35 25 C37 22 38 19 38 16 M55 19 C57 16 58 13 58 10", .52, "#4a4943"),
    ]),
}


def write_svg(filename: str, codepoint: int, label: str, marks: list[tuple[str, float, str]]) -> None:
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": label,
        "data-pua": f"U+{codepoint:X}",
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-ink-path-units": "normalized",
        "data-naturalist-construction": "profile-anatomy-v6",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = f"{label} — naturalist brush study"
    group = ET.SubElement(root, f"{{{NS}}}g", {
        "fill": "none", "stroke-linecap": "round", "stroke-linejoin": "round",
    })
    for index, (d, width, color) in enumerate(marks):
        ET.SubElement(group, f"{{{NS}}}path", {
            "class": "ink-stroke",
            "data-ink-stroke": "tapered",
            "data-ink-role": "naturalist-gesture",
            "data-ink-index": str(index),
            "pathLength": "1",
            "d": d,
            "stroke": color,
            "stroke-width": str(width),
        })
    (OUT / filename).write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main() -> None:
    for filename, (codepoint, label, marks) in ART.items():
        write_svg(filename, codepoint, label, marks)
        print(f"redrew {label}: {len(marks)} brush gestures")


if __name__ == "__main__":
    main()
