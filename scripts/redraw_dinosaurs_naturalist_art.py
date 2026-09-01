#!/usr/bin/env python3
"""Render the dinosaur PUA family as distinct naturalist sumi-e specimens."""

from __future__ import annotations

import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "dinosaurs"
MANIFEST = ROOT / "assets" / "pua" / "manifest.json"


def pua_attribute(name: str, source: str) -> str:
    """Read the stable private-use code point from the manifest when needed."""
    match = re.search(r'data-pua="([^"]+)"', source)
    if match:
        return match.group(0)
    manifest = json.loads(MANIFEST.read_text())
    rel = f"dinosaurs/{name}.svg"
    for entry in manifest:
        if entry.get("source") == rel:
            return f'data-pua="U+{entry["name"]}"'
    raise SystemExit(f"missing PUA code point in manifest for {name}")


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*v) for v in values]


def ribbon(values, width, seed, color="#262522", dry=False) -> str:
    d = stroke_path(p(*values), width=width, seed=seed, wobble=.24, taper_start=.10, taper_end=.10)
    return f'<path class="{"ink-dry" if dry else "ink-wash"}" d="{d}" fill="{color}" data-ink-brush-pass="{"dry-edge-v1" if dry else "loaded-ribbon-v2"}"/>'


def dry(values, width, seed, color="#77746a") -> list[str]:
    return [f'<path class="ink-dry" d="{d}" fill="{color}" data-ink-brush-pass="dry-fragment-v1"/>' for d in dry_brush_paths(p(*values), width=width, seed=seed, breaks=2)]


def mass(d, fill="#4a4943", detail="loaded-mass-v2") -> str:
    # Pale washes cannot remain tonal after SVG outlines are merged into the
    # monochrome font.  Keep their observed silhouette as a broken-feeling dry
    # contour so the paper remains visible inside bodies, sails, and matrix.
    if fill.lower() in {"#77746a", "#bcb9af", "#dedbd4"}:
        return (
            f'<path class="ink-dry" d="{d}" fill="none" stroke="{fill}" '
            'stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round" '
            'pathLength="1" data-ink-brush-pass="dry-contour-v2"/>'
        )
    return f'<path class="ink-wash" d="{d}" fill="{fill}" data-ink-brush-pass="{detail}"/>'


def dab(cx, cy, rx, ry, fill="#262522") -> str:
    return f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" data-ink-brush-pass="loaded-dab-v1"/>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    cp = pua_attribute(name, source)
    source_ref = (
        "Noun Project pteranodon icon 6594712 by iconfield, https://thenounproject.com/icon/pteranodon-6594712/"
        if name == "pteranodon"
        else "Noun Project Dinosaurs Icon Set 243311 by Icogenix, https://thenounproject.com/browse/collection-icon/dinosaurs-243311/"
    )
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="dinosaurs / {name}" {cp} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized" data-source-reference="{source_ref}; Castalia original redraw" data-reference-record="cards/editorial/noun-project-references.json#dinosaurs/*" data-license-status="reference-only; exact production license not asserted" data-naturalist-construction="full-bodied-{name}-v3" data-intentional-components="semantic-multipart-v1" data-component-review="severity-contact-sheet-2026-08-v1">
<title>dinosaurs / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


write("ankylosaurus", [
    ribbon([(19, 41, .10), (29, 35, .78), (42, 35, 1.0), (53, 40, .08)], 6.2, "anky-armored-back", "#4a4943"),
    mass("M 49 36 C 55 34 61 37 63 41 C 60 45 54 47 49 44 Z", "#262522"),
    ribbon([(20, 41, .10), (13, 43, .72), (8, 48, .08)], 2.0, "anky-tail"),
    dab(7, 49, 3.1, 2.5, "#262522"),
    ribbon([(27, 35, .10), (29, 29, .72), (32, 34, .08)], 1.6, "anky-plate-a", "#77746a", dry=True),
    ribbon([(38, 34, .10), (41, 27, .72), (44, 35, .08)], 1.7, "anky-plate-b", "#4a4943"),
    ribbon([(28, 42, .10), (26, 50, .72), (23, 55, .08)], 1.8, "anky-leg-a"),
    ribbon([(45, 43, .10), (47, 50, .72), (45, 55, .08)], 1.5, "anky-leg-b", "#77746a", dry=True),
])

write("brachiosaurus", [
    ribbon([(13, 44, .10), (25, 39, .76), (38, 40, 1.0), (48, 45, .08)], 4.8, "brachio-body", "#4a4943"),
    ribbon([(47, 44, .10), (50, 34, .72), (50, 23, .94), (55, 13, .08)], 2.8, "brachio-neck"),
    mass("M 53 10 C 57 8 63 9 65 12 C 62 14 57 15 53 14 Z", "#262522"),
    ribbon([(15, 43, .10), (8, 39, .72), (4, 34, .08)], 1.4, "brachio-tail", "#77746a", dry=True),
    ribbon([(24, 43, .10), (22, 53, .72), (20, 61, .08)], 1.7, "brachio-leg-a"),
    ribbon([(41, 44, .10), (42, 54, .72), (41, 62, .08)], 1.45, "brachio-leg-b", "#77746a", dry=True),
    ribbon([(51, 31, .10), (54, 25, .72), (55, 18, .08)], .72, "brachio-neck-light", "#bcb9af", dry=True),
])

write("fossil", [
    mass("M 13 22 C 25 16 45 17 58 24 L 56 53 C 43 58 25 58 14 52 Z", "#bcb9af"),
    ribbon([(18, 44, .10), (27, 39, .72), (37, 34, .96), (49, 29, .08)], 2.2, "fossil-spine"),
    ribbon([(27, 39, .10), (24, 32, .72), (25, 26, .08)], 1.15, "fossil-rib-a", "#4a4943"),
    ribbon([(34, 35, .10), (32, 28, .72), (34, 22, .08)], 1.05, "fossil-rib-b", "#77746a", dry=True),
    ribbon([(41, 32, .10), (41, 25, .72), (44, 21, .08)], .95, "fossil-rib-c", "#4a4943"),
    ribbon([(48, 29, .10), (51, 25, .72), (54, 23, .08)], .80, "fossil-skull", "#77746a", dry=True),
    ribbon([(17, 51, .10), (29, 54, .72), (43, 53, .08)], .72, "fossil-stratum", "#bcb9af", dry=True),
])

write("parasaurolophus", [
    ribbon([(16, 42, .10), (28, 36, .76), (41, 37, 1.0), (49, 42, .08)], 5.7, "para-body", "#4a4943"),
    ribbon([(17, 41, .10), (9, 37, .72), (4, 32, .08)], 1.55, "para-tail", "#77746a", dry=True),
    ribbon([(47, 40, .10), (51, 32, .72), (57, 27, .08)], 2.6, "para-neck"),
    mass("M 54 24 C 59 21 65 23 67 27 C 63 30 58 31 54 29 Z", "#262522"),
    ribbon([(57, 24, .10), (50, 18, .74), (40, 16, .08)], 2.0, "para-crest", "#4a4943"),
    ribbon([(27, 41, .10), (25, 51, .72), (22, 58, .08)], 1.8, "para-leg-a"),
    ribbon([(42, 42, .10), (44, 51, .72), (42, 58, .08)], 1.45, "para-leg-b", "#77746a", dry=True),
])

write("pteranodon", [
    mass("M 34 36 C 30 29 31 23 36 20 C 40 23 41 29 38 36 Z", "#4a4943"),
    ribbon([(35, 33, .08), (26, 27, .72), (16, 19, .96), (7, 17, .08)], 2.25, "ptera-wing-l"),
    ribbon([(38, 33, .08), (47, 27, .72), (57, 19, .96), (67, 17, .08)], 1.65, "ptera-wing-r", "#77746a", dry=True),
    ribbon([(35, 22, .08), (42, 17, .72), (51, 15, .08)], 1.5, "ptera-beak", "#262522"),
    ribbon([(34, 22, .08), (30, 15, .72), (27, 11, .08)], 1.15, "ptera-crest", "#4a4943"),
    ribbon([(35, 36, .08), (31, 44, .72), (27, 49, .08)], 1.0, "ptera-leg-l", "#77746a", dry=True),
    ribbon([(38, 36, .08), (43, 43, .72), (48, 47, .08)], .8, "ptera-leg-r", "#bcb9af", dry=True),
])

write("spinosaurus", [
    ribbon([(15, 42, .10), (28, 36, .76), (42, 37, 1.0), (51, 42, .08)], 5.8, "spino-body", "#4a4943"),
    ribbon([(16, 41, .10), (9, 38, .72), (4, 34, .08)], 1.65, "spino-tail", "#77746a", dry=True),
    mass("M 48 36 C 54 31 63 32 68 36 C 64 40 55 42 49 40 Z", "#262522"),
    ribbon([(23, 36, .10), (27, 23, .72), (31, 35, .08)], 2.1, "spino-sail-a", "#262522"),
    ribbon([(32, 35, .10), (37, 18, .72), (41, 37, .08)], 2.4, "spino-sail-b", "#4a4943"),
    ribbon([(41, 37, .10), (47, 25, .72), (49, 39, .08)], 1.5, "spino-sail-c", "#77746a", dry=True),
    ribbon([(28, 42, .10), (26, 51, .72), (23, 58, .08)], 1.8, "spino-leg-a"),
    ribbon([(44, 42, .10), (46, 51, .72), (43, 58, .08)], 1.5, "spino-leg-b", "#77746a", dry=True),
])

write("stegosaurus", [
    ribbon([(16, 43, .10), (28, 37, .76), (42, 38, 1.0), (52, 43, .08)], 5.8, "stego-body", "#4a4943"),
    ribbon([(17, 42, .10), (9, 40, .72), (4, 36, .08)], 1.7, "stego-tail", "#77746a", dry=True),
    mass("M 49 40 C 55 37 62 39 65 43 C 62 46 56 47 51 45 Z", "#262522"),
    ribbon([(22, 37, .10), (24, 28, .72), (29, 36, .08)], 2.2, "stego-plate-a"),
    ribbon([(30, 36, .10), (34, 23, .72), (39, 37, .08)], 2.5, "stego-plate-b", "#262522"),
    ribbon([(40, 38, .10), (45, 29, .72), (49, 40, .08)], 1.7, "stego-plate-c", "#77746a", dry=True),
    ribbon([(27, 43, .10), (25, 52, .72), (22, 58, .08)], 1.8, "stego-leg-a"),
    ribbon([(44, 43, .10), (46, 52, .72), (43, 58, .08)], 1.45, "stego-leg-b", "#77746a", dry=True),
])

write("triceratops", [
    ribbon([(14, 42, .10), (27, 36, .76), (40, 37, 1.0), (48, 42, .08)], 6.1, "tri-body", "#4a4943"),
    ribbon([(15, 41, .10), (8, 38, .72), (4, 34, .08)], 1.4, "tri-tail", "#77746a", dry=True),
    mass("M 45 30 C 52 25 61 27 64 34 L 59 45 C 52 47 46 42 44 36 Z", "#262522"),
    ribbon([(49, 30, .10), (47, 22, .72), (49, 16, .08)], 2.0, "tri-frill-horn", "#4a4943"),
    ribbon([(57, 34, .10), (64, 30, .72), (69, 29, .08)], 1.8, "tri-brow-horn"),
    ribbon([(59, 39, .10), (65, 40, .72), (69, 42, .08)], 1.1, "tri-nose-horn", "#77746a", dry=True),
    ribbon([(25, 42, .10), (23, 52, .72), (20, 58, .08)], 1.9, "tri-leg-a"),
    ribbon([(42, 42, .10), (44, 52, .72), (42, 58, .08)], 1.55, "tri-leg-b", "#77746a", dry=True),
])

write("tyrannosaurus", [
    ribbon([(15, 40, .10), (28, 34, .76), (41, 36, 1.0), (49, 42, .08)], 4.9, "tyrannosaur-body", "#4a4943"),
    ribbon([(17, 39, .10), (10, 35, .72), (4, 29, .08)], 1.7, "tyrannosaur-tail", "#262522"),
    ribbon([(46, 37, .10), (50, 29, .72), (56, 25, .08)], 2.25, "tyrannosaur-neck"),
    mass("M 54 20 C 59 17 67 19 68 24 C 64 28 58 29 53 27 Z", "#262522"),
    ribbon([(55, 26, .10), (62, 29, .72), (68, 27, .08)], 1.0, "tyrannosaur-jaw", "#77746a", dry=True),
    ribbon([(31, 39, .10), (27, 45, .72), (23, 46, .08)], 1.05, "tyrannosaur-arm", "#77746a", dry=True),
    ribbon([(34, 40, .10), (31, 51, .72), (26, 59, .08)], 1.8, "tyrannosaur-leg-a"),
    ribbon([(45, 41, .10), (48, 51, .72), (45, 59, .08)], 1.45, "tyrannosaur-leg-b", "#4a4943"),
])

write("velociraptor", [
    ribbon([(17, 40, .10), (28, 35, .76), (40, 37, 1.0), (47, 41, .08)], 4.4, "velo-body", "#4a4943"),
    ribbon([(18, 39, .10), (10, 34, .72), (4, 27, .08)], 1.55, "velo-tail"),
    ribbon([(45, 38, .10), (50, 30, .72), (56, 26, .08)], 1.8, "velo-neck"),
    mass("M 53 23 C 59 20 66 22 68 26 C 64 29 58 30 54 28 Z", "#262522"),
    ribbon([(34, 39, .10), (29, 45, .72), (25, 44, .08)], 1.15, "velo-arm", "#77746a", dry=True),
    ribbon([(31, 40, .10), (28, 50, .72), (23, 58, .08)], 1.85, "velo-leg-a"),
    ribbon([(42, 41, .10), (45, 50, .72), (41, 59, .08)], 1.6, "velo-leg-b", "#4a4943"),
    ribbon([(24, 57, .10), (20, 54, .72), (17, 56, .08)], 1.05, "velo-sickle", "#262522"),
    ribbon([(24, 36, .10), (31, 32, .72), (39, 35, .08)], .72, "velo-feather-edge", "#bcb9af", dry=True),
])

def write_compsognathus() -> None:
    """Alias the recognizable standard theropod study into the species PUA.

    Android WebView forces U+1F996 through its color-emoji shaper even when
    Emojinq leads the CSS font stack. Keeping the card identity at U+F146A
    guarantees Emojinq rendering while reusing the standard Unicode anatomy.
    """
    source = ROOT / "assets" / "gray-all" / "1F996.svg"
    if not source.exists():
        raise SystemExit(f"build the standard Unicode corpus before {source.name}")
    tree = ET.parse(source)
    root = tree.getroot()
    root.attrib.pop("id", None)
    root.set("viewBox", "0 0 72 72")
    root.set("role", "img")
    root.set("aria-label", "dinosaurs / compsognathus")
    root.set("data-pua", "U+F146A")
    root.set("data-source-codepoint", "U+1F996")
    root.set("data-castalia-style", "sumi-e-naturalist-v2")
    root.set("data-ink-stroke-system", "filled-brush-mass-v2")
    root.set("data-source-reference", "Noun Project Dinosaurs Icon Set 243311 by Icogenix, https://thenounproject.com/browse/collection-icon/dinosaurs-243311/; Castalia original redraw")
    root.set("data-reference-record", "cards/editorial/noun-project-references.json#dinosaurs/*")
    root.set("data-license-status", "reference-only; exact production license not asserted")
    root.set("data-naturalist-construction", "full-bodied-compsognathus-v3")
    root.set("data-intentional-components", "semantic-multipart-v1")
    root.set("data-component-review", "severity-contact-sheet-2026-08-v1")
    # The Unicode card carries generous general-purpose emoji margins. Scale
    # the anatomy optically for a small moving agent while retaining a safe
    # inset on every edge of the 72-unit Emojinq card.
    scale = 1.3
    offset = 36 * (1 - scale)
    for element in root.iter():
        d = element.get("d")
        if d:
            # line_brush emits only absolute M/L coordinates here, so a
            # dependency-free numeric transform keeps this redraw script
            # runnable with the repository's ordinary Python entry point.
            if re.search(r"[ACHQSTVZachqstvz]", d):
                raise SystemExit("unexpected non-linear command in standard theropod source")
            element.set("d", re.sub(
                r"-?\d+(?:\.\d+)?",
                lambda match: f"{float(match.group()) * scale + offset:.3f}",
                d,
            ))
        if element.get("stroke-width"):
            element.set("stroke-width", f'{float(element.get("stroke-width")) * 1.18:.3f}')
    title = ET.Element("{http://www.w3.org/2000/svg}title")
    title.text = "dinosaurs / compsognathus — standard theropod ink study"
    root.insert(0, title)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree.write(OUT / "compsognathus.svg", encoding="UTF-8", xml_declaration=True)


write_compsognathus()

print("redrew all 11 dinosaur PUA glyphs as distinct naturalist brush studies")
