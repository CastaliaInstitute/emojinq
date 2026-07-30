#!/usr/bin/env python3
"""Run structural and optional raster checks over the generated Emojinq set."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


def check_svgs(source_dir: Path) -> int:
    files = sorted(source_dir.glob("*.svg"))
    if not files:
        raise SystemExit(f"no SVGs found in {source_dir}")
    arrowed = []
    missing_style = []
    for path in files:
        text = path.read_text()
        if "marker-start" in text or "marker-end" in text:
            arrowed.append(path.name)
        if "data-castalia-style" not in text:
            missing_style.append(path.name)
    if arrowed:
        raise SystemExit(f"arrow markers found in {len(arrowed)} glyphs: {arrowed[:3]}")
    if missing_style:
        raise SystemExit(f"style metadata missing in {len(missing_style)} glyphs")
    return len(files)


def raster_check(source_dir: Path, sample: int, size: int) -> None:
    converter = shutil.which("rsvg-convert")
    if converter is None:
        print("raster check skipped: rsvg-convert is not installed")
        return
    with tempfile.TemporaryDirectory() as temp_dir:
        for source in sorted(source_dir.glob("*.svg"))[:sample]:
            target = Path(temp_dir) / f"{source.stem}.png"
            subprocess.run([converter, "-w", str(size), "-h", str(size), "-o", str(target), str(source)], check=True)
            image = Image.open(target).convert("RGBA")
            alpha = image.getchannel("A")
            bbox = alpha.getbbox()
            if bbox is None:
                raise SystemExit(f"blank raster output: {source.name}")
            if bbox[0] < 1 or bbox[1] < 1 or bbox[2] > size - 1 or bbox[3] > size - 1:
                raise SystemExit(f"clipped raster output: {source.name} bbox={bbox}")
    print(f"raster checked {min(sample, len(list(source_dir.glob('*.svg'))))} glyphs at {size}px")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=Path("assets/gray-all"))
    parser.add_argument("--sample", type=int, default=24)
    parser.add_argument("--size", type=int, default=128)
    args = parser.parse_args()
    count = check_svgs(args.source_dir)
    raster_check(args.source_dir, args.sample, args.size)
    print(f"quality checked {count} SVG glyphs")


if __name__ == "__main__":
    main()
