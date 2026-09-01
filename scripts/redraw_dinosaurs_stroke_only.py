#!/usr/bin/env python3
"""Replace the dinosaur studies with stroke-only naturalist constructions.

The image-assisted plate is a species reference, not an asset.  This authoring
pass keeps its identifying anatomy while expressing every mark as a tapered
SVG stroke so the source remains animatable, scalable, and laser-safe.
"""

from __future__ import annotations

import re
import json
import zlib
import xml.etree.ElementTree as ET
from pathlib import Path

from line_brush import brush_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "dinosaurs"
MANIFEST = ROOT / "assets" / "pua" / "manifest.json"

INK = "#262421"
MID = "#4a4943"
LIGHT = "#77746a"


MARK_INDEX = 0


def s(d: str, width: float = 1.15, color: str = INK, label: str = "contour") -> str:
    """Emit one source gesture as pressure-shaped, stroke-only SVG paths."""
    global MARK_INDEX
    source = ET.Element("path", {
        "d": d,
        "fill": "none",
        "stroke": color,
        "stroke-width": str(width),
    })
    seed = zlib.crc32(f"{label}:{d}".encode("utf-8")) & 0x7FFFFFFF
    output = []
    for mark_d, mark_width, mark_color in brush_path(d, source, seed):
        output.append(
            f'<path class="ink-stroke" data-ink-stroke="tapered" pathLength="1" '
            f'data-ink-role="{label}" data-ink-index="{MARK_INDEX}" '
            f'd="{mark_d}" fill="none" stroke-width="{mark_width:.2f}" '
            f'stroke="{color if color else mark_color}" stroke-linecap="round" '
            f'stroke-linejoin="round" />'
        )
        MARK_INDEX += 1
    return "\n    ".join(output)


def eye(x: float, y: float, r: float = 0.9) -> str:
    # A ring remains a stroke, never a filled dot.
    return s(f"M{x-r:.2f} {y} C{x-r:.2f} {y-r:.7f} {x+r:.2f} {y-r:.7f} {x+r:.2f} {y} C{x+r:.2f} {y+r:.7f} {x-r:.2f} {y+r:.7f} {x-r:.2f} {y}", .72, INK, "eye")


ART: dict[str, list[str]] = {
    "ankylosaurus": [
        s("M12 43 C18 35 31 32 43 35 C49 37 53 41 57 42 C61 43 64 41 67 39", 1.65, INK, "back"),
        s("M12 43 C11 47 17 51 25 53 C36 55 47 52 53 47 C58 48 63 49 66 46", 1.4, MID, "belly"),
        s("M12 43 C9 41 9 38 12 36 C15 34 19 35 22 37", 1.25, INK, "head"),
        s("M57 42 C62 42 66 40 68 42 C69 45 66 48 62 48", 1.15, INK, "club-tail"),
        s("M19 36 L20 30 L24 35 L27 28 L31 34 L35 27 L39 34 L44 29 L47 36", 1.0, MID, "armor"),
        s("M22 50 C21 55 20 58 18 61 C20 62 22 61 23 59 M36 52 C36 56 35 59 34 61 C36 62 38 61 39 59 M47 50 C48 54 49 57 48 60 C50 61 52 60 52 58", 1.1, INK, "feet"),
        s("M19 40 C26 38 34 39 42 41 M27 47 C34 49 42 48 49 45 M23 42 C25 44 26 46 27 48 M39 39 C41 41 42 44 42 46", .58, LIGHT, "flank-texture"),
        eye(15, 38, .75),
    ],
    "brachiosaurus": [
        s("M19 50 C24 43 34 40 44 43 C49 45 53 48 57 47 C61 46 64 48 62 51 C57 54 51 53 46 51", 1.45, INK, "back"),
        s("M20 50 C20 54 27 56 34 56 C41 56 46 54 49 51", 1.18, MID, "belly"),
        s("M44 45 C45 37 45 29 44 22 C43 16 45 10 50 7", 1.48, INK, "long-neck"),
        s("M48 8 C52 5 59 6 63 9 C60 12 55 12 50 11", 1.18, INK, "head"),
        s("M23 52 C22 56 21 60 20 62 C22 63 24 62 25 60 M37 54 C37 58 36 61 35 63 C37 64 39 63 40 61 M48 51 C50 55 51 59 50 62 C52 63 54 62 54 60", 1.05, INK, "feet"),
        s("M46 15 C48 19 49 23 49 27 M45 26 C47 29 48 33 48 36 M23 47 C30 45 37 46 42 48 M26 49 C29 51 32 52 35 52 M43 18 C45 20 46 23 46 25", .58, LIGHT, "anatomy"),
        eye(57, 8, .7),
    ],
    "fossil": [
        s("M12 39 C19 35 25 31 31 28 C39 24 47 22 57 24", 1.25, INK, "spine"),
        s("M12 39 C15 42 18 45 21 48 M20 34 C18 39 18 44 20 49 M27 30 C25 36 25 42 28 46 M34 27 C32 33 32 39 35 43 M41 25 C40 31 41 36 44 40 M48 23 C47 28 49 32 52 35", .9, MID, "ribs"),
        s("M12 39 C10 37 9 34 10 31 C12 29 15 30 17 32 M55 24 C59 24 62 26 63 29", .92, INK, "skull-tail"),
        s("M18 48 C25 51 33 52 41 51 C48 50 55 47 60 43", 1.0, LIGHT, "sediment"),
        s("M23 49 C25 46 28 45 31 46 M36 50 C39 47 42 46 45 47 M49 47 C52 44 55 43 58 44", .52, LIGHT, "bone-detail"),
        eye(13, 32, .55),
    ],
    "parasaurolophus": [
        s("M13 43 C20 35 31 33 43 36 C49 38 53 42 58 43 C62 44 65 42 67 40", 1.55, INK, "back"),
        s("M13 43 C12 47 19 51 28 52 C37 53 46 50 51 47 C56 48 61 49 64 46", 1.3, MID, "belly"),
        s("M13 43 C10 41 10 38 13 36 C16 34 20 35 23 37", 1.2, INK, "head"),
        s("M20 36 C27 32 33 31 39 33 C44 32 49 28 54 23 C58 19 61 16 64 14", 1.2, INK, "crest"),
        s("M57 19 C61 17 65 18 67 20 C64 22 60 22 56 22", .75, MID, "crest-tip"),
        s("M22 49 C22 54 21 58 19 61 M37 50 C38 55 37 59 36 61 M48 48 C50 53 51 57 50 60", 1.05, INK, "feet"),
        s("M25 40 C32 38 39 39 46 42 M31 47 C36 48 42 47 47 45 M47 28 C50 28 53 26 56 23 M22 41 C24 43 25 45 26 47", .56, LIGHT, "flank-texture"),
        eye(16, 38, .72),
    ],
    "pteranodon": [
        s("M36 38 C31 32 31 26 35 21 C39 25 40 31 38 38", 1.35, INK, "body"),
        s("M35 29 C28 24 20 19 11 17 C8 16 7 14 9 13 C20 14 30 17 38 24", 1.22, INK, "wing-left"),
        s("M38 29 C46 23 54 17 64 12 C67 10 69 10 68 12 C61 20 51 27 39 34", 1.22, MID, "wing-right"),
        s("M35 22 C37 16 39 10 42 6 C44 5 45 6 44 8 C42 14 40 19 38 24", .95, INK, "beak"),
        s("M35 37 C31 42 28 47 25 51 M38 37 C42 42 46 46 50 49", .9, INK, "feet"),
        s("M29 25 C23 21 17 18 12 17 M46 24 C52 19 58 16 64 13 M25 23 C22 24 19 24 16 23 M49 22 C53 23 57 22 60 20 M35 34 C33 31 31 29 28 27", .48, LIGHT, "wing-ribs"),
        eye(41, 20, .6),
    ],
    "spinosaurus": [
        s("M12 43 C19 35 31 33 43 36 C49 38 53 41 58 42 C62 43 65 41 67 39", 1.55, INK, "back"),
        s("M12 43 C11 47 18 51 27 52 C37 53 46 50 52 46 C57 47 62 48 65 45", 1.3, MID, "belly"),
        s("M12 43 C9 41 10 38 13 36 C17 34 20 36 23 38", 1.2, INK, "head"),
        s("M22 36 L24 22 L29 33 L33 18 L38 34 L43 21 L47 37", 1.0, MID, "sail"),
        s("M22 49 C22 54 21 58 19 61 M37 50 C38 55 37 59 36 61 M48 47 C50 52 51 56 50 59", 1.05, INK, "feet"),
        s("M20 40 C27 38 34 39 42 41 M27 47 C34 49 42 48 49 45 M24 34 C27 35 29 37 30 39 M31 31 C34 34 35 37 35 40 M38 32 C40 35 41 38 41 40", .58, LIGHT, "flank-texture"),
        eye(16, 38, .72),
    ],
    "stegosaurus": [
        s("M11 44 C18 35 31 33 43 36 C50 38 54 42 58 43 C63 44 66 42 68 40", 1.55, INK, "back"),
        s("M11 44 C11 48 18 52 27 53 C37 54 47 51 53 47 C58 48 63 49 66 46", 1.3, MID, "belly"),
        s("M11 44 C8 42 9 39 12 37 C16 35 20 36 23 38", 1.18, INK, "head"),
        s("M18 37 C17 33 18 29 20 27 C22 30 23 33 23 36 M23 35 C23 30 25 25 28 22 C30 27 30 31 30 35 M30 35 C31 29 34 24 37 21 C39 27 38 32 38 36 M38 36 C40 31 44 27 47 25 C48 30 46 35 46 38 M46 38 C49 34 52 32 54 31 C54 35 51 38 49 40", 1.0, INK, "plates"),
        s("M21 50 C21 55 20 59 18 62 C20 63 22 62 23 60 M36 51 C37 56 36 60 35 62 C37 63 39 62 40 60 M48 49 C50 54 51 58 50 61 C52 62 54 61 54 59", 1.08, INK, "feet"),
        s("M21 41 C29 39 37 40 45 42 M28 48 C35 50 43 49 49 46 M25 43 C27 45 28 47 29 49 M39 41 C41 43 42 45 42 47", .55, LIGHT, "flank-texture"),
        eye(15, 39, .72),
    ],
    "triceratops": [
        s("M17 43 C22 35 33 32 44 36 C50 39 54 42 58 43 C62 44 65 42 67 40", 1.5, INK, "back"),
        s("M17 43 C16 48 23 52 31 53 C40 54 48 51 53 47 C58 48 63 49 65 46", 1.28, MID, "belly"),
        s("M17 43 C13 42 11 39 13 36 C16 32 22 32 27 35 L31 40", 1.2, INK, "head"),
        s("M19 36 C17 30 20 25 26 23 C33 21 40 24 43 30 L44 38", 1.05, MID, "frill"),
        s("M24 28 L21 21 C20 19 21 18 23 20 L27 26 M31 25 L31 17 C31 15 33 15 33 17 L34 25 M38 27 L43 21 C44 19 46 20 45 22 L41 29", 1.0, INK, "horns"),
        s("M25 50 C24 55 23 59 21 61 M40 51 C41 56 40 60 39 62", 1.08, INK, "feet"),
        s("M22 40 C29 38 36 39 42 41 M28 47 C35 49 42 48 48 45 M22 31 C25 33 27 35 28 37 M34 27 C36 30 38 33 38 36 M22 42 C24 44 25 46 25 48", .55, LIGHT, "flank-texture"),
        eye(19, 36, .72),
    ],
    "tyrannosaurus": [
        s("M20 43 C27 35 38 32 48 36 C54 39 57 42 61 42 C64 42 67 40 68 42", 1.6, INK, "back"),
        s("M20 43 C20 48 27 52 36 52 C44 53 50 50 54 46 C59 47 63 48 66 45", 1.32, MID, "belly"),
        s("M21 41 C17 37 11 35 7 37 C9 41 15 44 23 44", 1.35, INK, "jaws"),
        s("M9 40 C13 40 17 39 21 40 M12 42 L14 44 M16 41 L18 43 M20 40 L22 42 M13 38 L15 40 M17 38 L19 40", .72, MID, "teeth"),
        s("M38 48 C38 54 37 59 34 63 C36 64 39 63 40 61 M48 47 C50 53 50 58 48 62 C50 63 52 62 53 60", 1.45, INK, "hind-feet"),
        s("M37 39 C33 42 31 45 29 47 M38 41 C35 43 34 46 33 48", .82, MID, "small-arms"),
        s("M27 36 C34 35 42 37 48 40 M30 40 C33 42 34 44 35 46 M43 38 C45 40 46 42 46 44", .56, LIGHT, "flank-texture"),
        eye(13, 38, .68),
    ],
    "velociraptor": [
        s("M17 45 C24 37 35 35 44 39 C50 42 54 44 59 42 C62 41 65 40 67 42", 1.28, INK, "back"),
        s("M17 45 C20 50 27 53 35 52 C43 52 48 49 52 46 C57 48 62 48 65 45", 1.08, MID, "belly"),
        s("M44 39 C47 33 52 29 58 28 C62 28 65 30 66 32 C62 34 58 34 54 33", 1.05, INK, "head"),
        s("M21 45 C18 51 17 56 14 60 C17 61 20 59 22 55", 1.12, INK, "sickle-claw"),
        s("M35 48 C34 53 32 57 29 60 M44 48 C46 53 46 57 44 60", 1.0, INK, "feet"),
        s("M24 39 C28 34 33 32 39 34 M29 43 C34 39 39 38 44 40 M49 36 C53 33 57 32 61 33 M27 41 C30 42 32 44 33 46 M39 38 C41 40 42 42 42 44", .6, LIGHT, "feather-lines"),
        s("M21 48 C25 47 29 47 33 49 M35 51 C38 53 40 55 40 57", .55, MID, "flank-texture"),
        eye(61, 30, .62),
    ],
}


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    original = target.read_text()
    match = re.search(r'data-pua="([^"]+)"', original)
    if not match:
        manifest = json.loads(MANIFEST.read_text())
        entry = next((item for item in manifest if item.get("source") == f"dinosaurs/{name}.svg"), None)
        if not entry:
            raise SystemExit(f"missing PUA code point in manifest for {target}")
        pua = f'data-pua="U+{entry["name"]}"'
    else:
        pua = match.group(0)
    label = f"dinosaurs / {name}"
    source_ref = (
        "Noun Project pteranodon icon 6594712 by iconfield, https://thenounproject.com/icon/pteranodon-6594712/"
        if name == "pteranodon"
        else "Noun Project Dinosaurs Icon Set 243311 by Icogenix, https://thenounproject.com/browse/collection-icon/dinosaurs-243311/"
    )
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" '
        f'role="img" aria-label="{label}" {pua} '
        'data-castalia-style="sumi-e-ink-wash-v1" '
        'data-ink-stroke-system="tapered-v1" data-ink-animation="draw-v1" '
        f'data-ink-path-units="normalized" data-naturalist-construction="species-anatomy-v1" data-source-reference="{source_ref}; Castalia original redraw" data-reference-record="cards/editorial/noun-project-references.json#dinosaurs/*" data-license-status="reference-only; exact production license not asserted" data-intentional-components="semantic-multipart-v1" data-component-review="severity-contact-sheet-2026-08-v1">\n'
        f'  <title>{label} — stroke-only naturalist brush study</title>\n'
        '  <g fill="none" stroke-linecap="round" stroke-linejoin="round">\n'
        + "\n".join(f"    {mark}" for mark in marks)
        + "\n  </g>\n</svg>\n"
    )
    target.write_text(svg)


for dinosaur, marks in ART.items():
    write(dinosaur, marks)
print(f"redrew {len(ART)} dinosaur studies as stroke-only naturalist SVGs")
