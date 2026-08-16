#!/usr/bin/env python3
"""Convert filled PUA brush studies into stroke-only centerline SVGs.

This is an authoring filter for the PUA corpus.  Existing stroke-only sources
are copied unchanged; filled masses and ribbons are rasterized only in a
temporary workspace, centerlined with AutoTrace, pressure-shaped, and emitted
as ordinary SVG paths.  The raster is never retained in the output.
"""

from __future__ import annotations

import argparse
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET
from pathlib import Path

from centerline_svg import emit, trace

NS = "http://www.w3.org/2000/svg"
SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}
ET.register_namespace("", NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def is_filled(source: Path) -> bool:
    root = ET.parse(source).getroot()
    for element in root.iter():
        if local(element.tag) not in SHAPES:
            continue
        fill = element.get("fill", "").strip().lower()
        if fill and fill not in {"none", "transparent"}:
            return True
        style = element.get("style", "").lower().replace(" ", "")
        if "fill:" in style and not any(token in style for token in ("fill:none", "fill:transparent")):
            return True
    return False


def copy_stroke(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def centerline(source: Path, target: Path, minimum: float) -> None:
    root = ET.parse(source).getroot()
    codepoint = root.get("data-pua")
    label = root.get("aria-label") or source.stem
    marks = trace(source, size=256, threshold=220, minimum=minimum, speckle=3)
    if not marks:
        raise ValueError("centerline recovery produced no marks")
    emit(source, target, marks, label, codepoint)
    output = ET.parse(target)
    out_root = output.getroot()
    out_root.set("data-castalia-style", "sumi-e-ink-wash-v1")
    out_root.set("data-ink-stroke-system", "tapered-v1")
    out_root.set("data-ink-coverage", "complete")
    out_root.set("data-ink-pressure", "loaded-middle-v1")
    out_root.set("data-ink-path-units", "normalized")
    out_root.set("data-pua-filter", "centerline-autotrace-v2")
    title = next((item for item in out_root if local(item.tag) == "title"), None)
    if title is None:
        title = ET.SubElement(out_root, f"{{{NS}}}title")
    title.text = f"{label} — stroke-only centerline study"
    output.write(target, encoding="utf-8", xml_declaration=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=Path("assets/pua"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--minimum", type=float, default=.55)
    parser.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    args = parser.parse_args()
    sources = sorted(args.source_dir.rglob("*.svg"))
    def process(source: Path) -> tuple[str, str | None]:
        relative = source.relative_to(args.source_dir)
        target = args.output_dir / relative
        try:
            if is_filled(source):
                centerline(source, target, args.minimum)
                return "converted", None
            else:
                copy_stroke(source, target)
                return "copied", None
        except Exception as error:  # keep the batch auditable and continue
            return "failed", f"{relative}: {error}"

    results: list[tuple[str, str | None]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        for result in executor.map(process, sources):
            results.append(result)
    converted = sum(kind == "converted" for kind, _ in results)
    copied = sum(kind == "copied" for kind, _ in results)
    failures = sorted(message for kind, message in results if kind == "failed" and message)
    failed = len(failures)
    manifest = args.output_dir / "centerline-report.txt"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        f"sources={len(sources)}\nconverted={converted}\ncopied_stroke_only={copied}\nfailed={failed}\n"
        + "\n".join(failures)
        + ("\n" if failures else ""),
        encoding="utf-8",
    )
    print(f"PUA centerline batch: {len(sources)} sources, {converted} converted, {copied} copied, {failed} failed")
    if failures:
        for failure in failures[:24]:
            print(f"FAIL {failure}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
