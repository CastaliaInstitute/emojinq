#!/usr/bin/env python3
"""Build familiar-color sumi-e variants for semantic PUA pigment glyphs."""

from __future__ import annotations

import colorsys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "pua" / "patterns"
OUTPUT = ROOT / "assets" / "pua-color" / "patterns"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

PIGMENTS = {
    "black": "#262421",
    "blue": "#397da6",
    "brown": "#8b5d3b",
    "gold": "#c6922d",
    "gray": "#777774",
    "green": "#4b8555",
    "orange": "#d47a2c",
    "purple": "#795ca2",
    "red": "#b7463f",
    "silver": "#9ca4aa",
    "white": "#e8e5dc",
    "yellow": "#d6ae32",
}


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def rgb(value: str) -> tuple[float, float, float]:
    return tuple(int(value[index:index + 2], 16) / 255 for index in (1, 3, 5))


def hex_color(values: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{max(0, min(255, round(value * 255))):02x}" for value in values)


def mix(a: tuple[float, float, float], b: tuple[float, float, float], amount: float) -> tuple[float, float, float]:
    return tuple(left * (1 - amount) + right * amount for left, right in zip(a, b))


def shades(base: str, name: str) -> tuple[str, str, str]:
    base_rgb = rgb(base)
    paper = rgb("#f4f1e9")
    ink = rgb("#262421")
    if name == "white":
        return "#77746a", "#d5d2ca", "#ece9e1"
    hue, saturation, lightness = colorsys.rgb_to_hls(*base_rgb)
    main = colorsys.hls_to_rgb(hue, min(.68, lightness * .94 + .04), min(1.0, saturation * .82))
    return hex_color(mix(main, ink, .28)), hex_color(mix(main, paper, .12)), hex_color(mix(main, paper, .48))


def recolor(name: str, source: Path, target: Path) -> None:
    tree = ET.parse(source)
    root = tree.getroot()
    dark, main, light = shades(PIGMENTS[name], name)
    for element in root.iter():
        if local(element.tag) not in {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}:
            continue
        fill = element.get("fill", "").lower()
        if not fill or fill == "none":
            continue
        classes = element.get("class", "").split()
        if "ink-color-wash" not in classes:
            classes.append("ink-color-wash")
            element.set("class", " ".join(classes))
        if fill in {"#262522", "#262421", "#24231f", "#000000"}:
            element.set("fill", dark)
        elif fill in {"#4a4943", "#3f3e39", "#5a5952"}:
            element.set("fill", main)
        else:
            element.set("fill", light)
    root.set("data-color-variant", "sumi-e-color-wash-v1")
    root.set("data-pigment", name)
    title = next((element for element in root if local(element.tag) == "title"), None)
    if title is not None:
        title.text = f"patterns / {name} — familiar-color sumi-e pigment wash"
    target.parent.mkdir(parents=True, exist_ok=True)
    tree.write(target, encoding="utf-8", xml_declaration=True)


def main() -> None:
    for name in sorted(PIGMENTS):
        recolor(name, SOURCE / f"{name}.svg", OUTPUT / f"{name}.svg")
    print(f"built {len(PIGMENTS)} familiar-color PUA pigment SVGs")


if __name__ == "__main__":
    main()
