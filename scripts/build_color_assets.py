#!/usr/bin/env python3
"""Layer muted OpenMoji color washes beneath Emojinq's sumi-e strokes."""

from __future__ import annotations

import argparse
import colorsys
import copy
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
COLOR = re.compile(r"^#([0-9a-fA-F]{6})$")
SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}
AUTHORED_REPLACEMENT_WASH = {
    # These silhouettes intentionally depart from the upstream geometry, so
    # their familiar pigment must follow the authored ink instead of leaving
    # the former OpenMoji shape visible behind it.
    "1F330.svg": "#6a462f",  # chestnut shell
    "1F35E.svg": "#f1b31c",  # warm bread crust
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def wash_color(value: str) -> str:
    """Soften a source color without changing its familiar hue family."""
    match = COLOR.match(value)
    if not match:
        return value
    red, green, blue = (int(match.group(1)[index:index + 2], 16) / 255 for index in (0, 2, 4))
    hue, saturation, lightness = colorsys.rgb_to_hls(red, green, blue)
    saturation *= 0.78
    lightness = 0.12 + lightness * 0.76
    red, green, blue = colorsys.hls_to_rgb(hue, lightness, saturation)
    # A trace of warm paper keeps bright emoji color from reading as flat UI art.
    paper = (0xF4 / 255, 0xF1 / 255, 0xE9 / 255)
    mixed = [channel * 0.88 + paper_channel * 0.12 for channel, paper_channel in zip((red, green, blue), paper)]
    return "#" + "".join(f"{round(channel * 255):02x}" for channel in mixed)


def prepare_wash(element: ET.Element) -> None:
    painted = any(
        key in element.attrib and element.get(key) not in {"none", "currentColor"}
        for key in ("fill", "stroke")
    )
    if local(element.tag) in SHAPES or painted:
        classes = set(element.get("class", "").split())
        classes.add("ink-wash")
        classes.add("ink-color-wash")
        element.set("class", " ".join(sorted(classes)))
        element.set("data-ink-wash", "true")
        if local(element.tag) in SHAPES:
            element.set("opacity", f"{float(element.get('opacity', '1')) * 0.76:.3f}")
        for key in ("fill", "stroke"):
            if key in element.attrib and element.get(key) not in {"none", "currentColor"}:
                element.set(key, wash_color(element.get(key, "")))
    for child in list(element):
        prepare_wash(child)


def build_one(color_source: Path, ink_source: Path, target: Path) -> None:
    color_root = ET.parse(color_source).getroot()
    ink_root = ET.parse(ink_source).getroot()
    output = ET.Element(f"{{{NS}}}svg", {
        "viewBox": ink_root.get("viewBox", "-6 -6 84 84"),
        "role": "img",
        "aria-label": ink_root.get("aria-label", color_source.stem),
        "data-castalia-style": "sumi-e-ink-wash-v1",
        # The color variant's outer contract describes the wash-plus-ink
        # composition even when an individual monochrome underdrawing uses
        # filled brush masses internally.
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-coverage": ink_root.get("data-ink-coverage", "complete"),
        "data-color-source": "openmoji-color",
        "data-color-variant": "sumi-e-color-wash-v1",
    })
    title = ET.SubElement(output, f"{{{NS}}}title")
    title.text = f"{color_source.stem} — familiar emoji color as restrained sumi-e wash"

    wash_group = ET.SubElement(output, f"{{{NS}}}g", {
        "id": "color-wash",
        "opacity": "0.92",
    })
    replacement = next(
        (element for element in ink_root.iter() if element.get("id") == "food-recognition-replacement"),
        None,
    )
    familiar = AUTHORED_REPLACEMENT_WASH.get(color_source.name)
    if replacement is not None and familiar:
        silhouette = next(
            (
                element
                for element in replacement
                if local(element.tag) == "path" and element.get("d", "").strip().upper().endswith("Z")
            ),
            None,
        )
        if silhouette is None:
            raise ValueError(f"authored replacement lacks a closed wash silhouette: {ink_source}")
        copied = copy.deepcopy(silhouette)
        copied.set("class", "ink-wash ink-color-wash")
        copied.set("fill", wash_color(familiar))
        copied.set("stroke", "none")
        copied.set("opacity", "0.64")
        copied.set("data-ink-wash", "true")
        copied.set("data-color-geometry", "authored-recognition-silhouette-v1")
        wash_group.append(copied)
    else:
        # OpenMoji places skin and hair fills beside the main color group, so
        # retain every painted group except its conventional black line layer.
        for child in list(color_root):
            if child.get("id", "").lower() == "line":
                continue
            copied = copy.deepcopy(child)
            prepare_wash(copied)
            wash_group.append(copied)

    # A faint offset pass gives the wash a pooled, non-mechanical edge.
    echo = copy.deepcopy(wash_group)
    echo.set("id", "color-wash-echo")
    echo.set("opacity", "0.11")
    echo.set("transform", "translate(.45 -.25)")
    output.insert(list(output).index(wash_group), echo)

    ink_group = ET.SubElement(output, f"{{{NS}}}g", {"id": "sumi-ink"})
    for child in list(ink_root):
        if local(child.tag) == "title":
            continue
        if child.get("data-color-copy") == "omit":
            continue
        ink_group.append(copy.deepcopy(child))

    target.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(output).write(target, encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--color-source-dir", type=Path, default=Path(".cache/openmoji/color/svg"))
    parser.add_argument("--ink-dir", type=Path, default=Path("assets/gray-all"))
    parser.add_argument("--manifest", type=Path, default=Path("assets/gray-all/manifest.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("assets/color-all"))
    args = parser.parse_args()

    entries = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    built = []
    for item in entries:
        color_source = args.color_source_dir / item["source"]
        ink_source = args.ink_dir / item["source"]
        if not color_source.exists() or not ink_source.exists():
            continue
        build_one(color_source, ink_source, args.output_dir / item["source"])
        built.append({**item, "color_wash": True})
    (args.output_dir / "manifest.json").write_text(json.dumps(built, indent=2) + "\n", encoding="utf-8")
    print(f"built {len(built)} sumi-e color-wash SVGs in {args.output_dir}")


if __name__ == "__main__":
    main()
