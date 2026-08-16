#!/usr/bin/env python3
"""Verify reviewed PUA referent candidates in ink and explicit color fallback."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "pua"
COLOR_ASSETS = ROOT / "assets" / "pua-color"
MANIFEST = ASSETS / "manifest.json"
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"
CONCRETE_TRACKS = {"concrete", "referent"}


def visible_bounds(path: Path) -> tuple[int, int, int]:
    with Image.open(path).convert("RGBA") as image:
        points = [
            (x, y)
            for y in range(image.height)
            for x in range(image.width)
            if image.getpixel((x, y))[3] >= 24
        ]
    if not points:
        return 0, 0, 0
    xs, ys = zip(*points)
    return max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, len(points)


def main() -> None:
    renderer = shutil.which("rsvg-convert")
    if not renderer:
        raise SystemExit("rsvg-convert is required for the 32px PUA toddler gate")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    developmental = json.loads(DEVELOPMENTAL.read_text(encoding="utf-8"))
    tracks = {
        entry["source"]: entry["track"]
        for entry in developmental["entries"]
        if entry.get("family") == "pua"
    }
    selected = [entry for entry in manifest if tracks.get(entry["source"]) in CONCRETE_TRACKS]
    unresolved = [
        entry["source"]
        for entry in developmental["entries"]
        if entry.get("family") == "pua" and entry.get("track") == "unreviewed-referent"
    ]
    if unresolved:
        raise SystemExit(f"PUA taxonomy still contains {len(unresolved)} unreviewed referents")
    if not selected:
        raise SystemExit("PUA taxonomy selected no object-scale referent candidates")
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="emojinq-pua-toddler-") as directory:
        raster_root = Path(directory)
        for index, entry in enumerate(selected):
            source = ASSETS / entry["source"]
            root = ET.parse(source).getroot()
            expected_label = entry["label"].replace("/", " / ").replace("_", " ")
            if root.get("aria-label") != expected_label:
                failures.append(f"{source}: semantic identity does not match manifest")
            if root.get("data-object-scale-candidate") != "pua-object-scale-candidate-v2":
                failures.append(f"{source}: object-scale candidate evidence is missing")
            if not root.get("data-naturalist-construction"):
                failures.append(f"{source}: naturalist construction evidence is missing")
            for variant, variant_source in (
                ("ink", source),
                ("color", COLOR_ASSETS / entry["source"] if (COLOR_ASSETS / entry["source"]).exists() else source),
            ):
                png = raster_root / f"{index}-{variant}.png"
                subprocess.run(
                    [renderer, "-w", "32", "-h", "32", str(variant_source), "-o", str(png)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                width, height, pixels = visible_bounds(png)
                if width < 4 or height < 4 or pixels < 12:
                    failures.append(
                        f"{variant_source}: weak 32px {variant} referent ({width}x{height}, {pixels} visible pixels)"
                    )
    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"PUA object-scale candidate gate checked: {len(selected)} reviewed referents "
        "in ink and explicit color fallback at 32px"
    )


if __name__ == "__main__":
    main()
