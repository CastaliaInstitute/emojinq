#!/usr/bin/env python3
"""Visual gates for the book-derived sumi-e benchmark glyphs.

The general metadata contract only proves that an asset entered the intended
pipeline.  This benchmark adds raster evidence for purposeful brushwork,
active negative space, asymmetric composition, and survival at small font
sizes. It deliberately imposes no maximum stroke count: defining anatomy and
toddler recognizability take precedence over economy.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageFont

from style_contract import assert_sumi_e

SHAPES = {"path", "ellipse", "circle"}
DEFAULT_ROOTS = [
    Path("assets/pua/adventure"),
    Path("assets/pua/animals"),
    Path("assets/pua/flora"),
    Path("assets/pua/farm"),
    Path("assets/pua/body"),
    Path("assets/pua/brc"),
    Path("assets/pua/castalia"),
    Path("assets/pua/cave_locations"),
    Path("assets/pua/cosmos"),
    Path("assets/pua/dinosaurs"),
    Path("assets/pua/faerie"),
    Path("assets/pua/herbs"),
    Path("assets/pua/locations"),
    Path("assets/pua/materials"),
    Path("assets/pua/patterns"),
    Path("assets/pua/plants"),
    Path("assets/pua/rockets"),
    Path("assets/pua/sea_creatures"),
    Path("assets/pua/weather_sky"),
]
DEFAULT_STUDIES = [
    *(path for path in sorted(Path("assets/pua/objects").glob("*.svg")) if "sumi-e-naturalist-v2" in path.read_text()),
    *(path for path in sorted(Path("assets/pua/science").glob("*.svg")) if "sumi-e-naturalist-v2" in path.read_text()),
    *(path for path in sorted(Path("assets/pua/people").glob("*.svg")) if "sumi-e-naturalist-v2" in path.read_text()),
]


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def raster_metrics(source: Path, size: int, temp: Path) -> tuple[int, float, float, tuple[int, int, int, int]]:
    output = temp / f"{source.parent.name}-{source.stem}-{size}.png"
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size), "-o", str(output), str(source)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    alpha = Image.open(output).convert("RGBA").getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return 0, 0.0, 0.0, (0, 0, 0, 0)
    pixels = [(x, y) for y in range(size) for x in range(size) if alpha.getpixel((x, y)) > 20]
    centroid_x = sum(x for x, _ in pixels) / len(pixels)
    return len(pixels), len(pixels) / (size * size), centroid_x, bbox


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        action="append",
        default=None,
        help="benchmark directory; defaults to the curated cross-category suite",
    )
    parser.add_argument("--font", type=Path, default=Path("fonts/Emojinq-Regular.ttf"))
    parser.add_argument("--manifest", type=Path, default=Path("assets/pua/manifest.json"))
    args = parser.parse_args()
    roots = args.root or DEFAULT_ROOTS
    files = sorted(path for root in roots for path in root.glob("*.svg"))
    if args.root is None:
        files.extend(DEFAULT_STUDIES)
    if not files:
        raise SystemExit("no sumi-e benchmark SVGs found")
    if shutil.which("rsvg-convert") is None:
        raise SystemExit("rsvg-convert is required for visual benchmark checks")

    entries = json.loads(args.manifest.read_text())
    codepoints = {entry["source"]: entry["codepoints"][0] for entry in entries if len(entry["codepoints"]) == 1}
    font_128 = ImageFont.truetype(str(args.font), 128)
    font_32 = ImageFont.truetype(str(args.font), 32)

    failures: list[str] = []
    dry_count = 0
    asymmetric_count = 0
    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        for source in files:
            manifest_key = f"{source.parent.name}/{source.name}"
            codepoint = codepoints.get(manifest_key)
            if codepoint is None:
                failures.append(f"{source}: missing single-codepoint manifest entry")
                continue
            try:
                assert_sumi_e(source)
            except ValueError as error:
                failures.append(str(error))
                continue
            root = ET.parse(source).getroot()
            marks = [element for element in root.iter() if local(element.tag) in SHAPES]
            dry = [element for element in marks if "ink-dry" in element.get("class", "").split()]
            if len(marks) < 2:
                failures.append(f"{source}: expected at least 2 purposeful brush marks, found {len(marks)}")
            if dry:
                dry_count += 1

            pixels, coverage, centroid_x, bbox = raster_metrics(source, 128, temp)
            if pixels == 0:
                failures.append(f"{source}: blank 128px render")
                continue
            if not 0.01 <= coverage <= 0.20:
                failures.append(f"{source}: ink coverage {coverage:.1%} does not preserve active negative space")
            if min(bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]) < 2:
                failures.append(f"{source}: brushwork clips the em-square margin at {bbox}")
            if abs(centroid_x - 63.5) >= 1.25:
                asymmetric_count += 1

            small_pixels, _, _, small_bbox = raster_metrics(source, 32, temp)
            if small_pixels < 6 or small_bbox[2] - small_bbox[0] < 4 or small_bbox[3] - small_bbox[1] < 4:
                failures.append(f"{source}: gesture does not survive at 32px")
            if font_128.getmask(chr(codepoint)).getbbox() is None:
                failures.append(f"{source}: compiled U+{codepoint:05X} is blank at 128px")
            compiled_small = font_32.getmask(chr(codepoint)).getbbox()
            if compiled_small is None or compiled_small[2] - compiled_small[0] < 4 or compiled_small[3] - compiled_small[1] < 4:
                failures.append(f"{source}: compiled U+{codepoint:05X} does not survive at 32px")

    minimum_dry = round(len(files) * 0.80)
    if dry_count < minimum_dry:
        failures.append(f"benchmark suite: dry-brush hierarchy appears in {dry_count}/{len(files)} glyphs; need {minimum_dry}")
    minimum_asymmetric = round(len(files) * 0.25)
    if asymmetric_count < minimum_asymmetric:
        failures.append(
            f"benchmark suite: only {asymmetric_count}/{len(files)} glyphs have an off-axis ink centroid; need {minimum_asymmetric}"
        )
    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"sumi-e visual benchmarks checked: {len(files)} glyphs; "
        f"dry hierarchy {dry_count}, asymmetric composition {asymmetric_count}, "
        "source and compiled 32px survival complete"
    )


if __name__ == "__main__":
    main()
